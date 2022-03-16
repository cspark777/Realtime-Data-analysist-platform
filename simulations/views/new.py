import json

from re import search

from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .base import SimulationBaseView
from simulations.models import Simulation
from simulations.forms import SimulationForm


class SimulationCreateView(SimulationBaseView, CreateView):
    template_name = 'simulation/new.html'
    model = Simulation
    form_class = SimulationForm

    def get_success_url(self):
        return "/react" + str(reverse_lazy('projects:simulations:simulations_list',
                            kwargs={'project_id': self.kwargs.get('project_id')}))

    def post(self, request, *args, **kwargs):
        self.object = None
        if self.request.is_ajax():
            form = self.get_form()
            form.is_valid()
            steps_values = [form.data[key] for key in form.data if key.startswith('event_new_')]
            for value in steps_values:
                try:
                    json.loads(value)
                    if value.isdigit():
                        raise ValueError
                except (json.JSONDecodeError, ValueError):
                    form.add_error("steps", "Invalid JSON")
            form, contexts = self.check_json_is_valid(form, self.request.FILES)
            if form.is_valid():
                return self.form_valid(form, contexts)
            return JsonResponse({"error": form.errors}, status=400)
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SimulationCreateView, self).get_context_data(**kwargs)
        self.set_projects(context)
        context = self.context_update(context, self.kwargs.get('project_id'))
        return context

    def form_valid(self, form, contexts):
        data = self.request.POST
        simulation = self.model()
        cleaned_data = {
            'name': data.get('name'),
            'description': data.get('description') or "",
            'replicas': data.get('replicas', 1),
            'created_by': self.request.user,
            'project_id': self.kwargs.get('project_id'),
            'run_type': data.get('run_type'),
            'run_count': data.get('run_count', 1),
            'run_time': data.get('run_time', 0),
            'type_event': data.get('type_event'),
        }

        avro_error = self.validate_avro_steps(self.request.POST)
        if avro_error:
            return JsonResponse({'error': {'Message failed validation': {'err': avro_error}}}, status=400)

        try:
            self.save_object(obj=simulation, **cleaned_data)
        except Exception as error:
            return self.form_invalid(form, exception=error)

        data = self.filter_contains(initial_dict=data, filter_by='delete', not_contains=True)
        ordering_data = self.filter_contains(initial_dict=data, filter_by='ordering')
        steps_data = self.filter_contains(initial_dict=data, filter_by='_')
        new_steps = self.filter_contains(initial_dict=steps_data, filter_by='_new_')
        new_count_steps = len(ordering_data.values())
        steps_list = [None for _ in range(new_count_steps)]
        for new_id in range(1, new_count_steps + 1):
            for key, value in new_steps.items():
                if 'ordering_new_' in key and value == str(new_id):
                    steps_list[new_id - 1] = search(r'\d+$', key).group(0)

        self.process_new_steps(steps_list, new_steps, simulation, form, contexts, self.form_invalid)

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, **kwargs):
        form.errors['exception'] = kwargs.get('exception')
        return super().form_invalid(form)
