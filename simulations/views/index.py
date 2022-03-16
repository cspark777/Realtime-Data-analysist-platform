import json

import requests
from django.conf import settings
from django.core import serializers
from django.urls import reverse_lazy
from django.views.generic import ListView

from core.utils import generate_avro
from simulations.models import Simulation
from streamprocessors.druid_utils import get_exception_messages
from .base import SimulationBaseView


def handle_simulation(request, project_id, simulation_id):
    server_url = settings.DATA_SERVER
    data = (
        {
            'project_id': project_id,
            'simulation_id': simulation_id,
            'user': request.user.id,
        }
    )

    simulation = Simulation.objects.filter(pk=simulation_id, created_by=request.user,
                                           project_id=project_id).first()
    is_running = False

    status_runner = str()
    counter = 0
    if 'stop' in request.path:
        server_url += 'stop_simulation'
        status_runner = 'stopped'
        is_running = False
    if 'run' in request.path:
        server_url += 'run_simulation'
        dsl = {}
        if simulation:
            steps = simulation.step_set.order_by('ordering')
            dsl = {
                'simulation_metrics': {
                    'run_type': simulation.run_type,
                    'run_count': simulation.run_count,
                    'run_time': simulation.run_time,
                }
            }
            steps_data = json.loads(serializers.serialize('json', steps))
            steps_data = list(map(lambda i: i.get('fields'), steps_data))
            for step_data in steps_data:
                avro = generate_avro(step_data.get('topic'))
                step_data['AVRO'] = avro
            dsl['steps'] = steps_data
            counter = 1
        data = {
            **data,
            'dsl_data': dsl,
            'broker_url': settings.KAFKA_URL,
            'replicas': simulation.replicas,
        }
        status_runner = 'run'
        is_running = True

    if simulation:
        simulation.completed += counter
        simulation.is_running = is_running
        simulation.save()

    data = json.dumps(data)
    response = requests.post(server_url, data=data)
    return response, status_runner


class SimulationView(SimulationBaseView, ListView):
    template_name = 'simulation/index.html'
    model = Simulation
    paginate_by = 10
    context_object_name = 'simulations'

    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user, project=self.kwargs.get('project_id'))

    def get_context_data(self, *args, **kwargs):
        context = super(SimulationView, self).get_context_data(*args, **kwargs)
        self.set_projects(context)
        context['websocket_server'] = settings.WEBSOCKET_SERVER
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        simulation_id = self.kwargs.get('simulation_id')
        project_id = self.kwargs.get('project_id')
        if simulation_id:
            response, status_runner = handle_simulation(request, project_id, simulation_id)
            status = response.status_code
            if status == 409:
                context['reason'] = response.json().get('reason')
            context['status'] = status
            context['status_runner'] = status_runner
            context['redirect_url'] = reverse_lazy('projects:simulations:simulations_list_react',
                                                   kwargs={'project_id': project_id})

            context['message'] = get_exception_messages(_dimension="simulation_id",
                                                        _id=simulation_id, _message_type="exception")
        return self.render_to_response(context)

    def simulation_invalid(self, **kwargs):
        exception = kwargs.get('exception')
        return self.render_to_response(self.get_context_data(exception=exception))
