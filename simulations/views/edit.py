import json

from re import search
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from core.utils import generate_avro
from .base import SimulationBaseView
from simulations.models import Simulation, Step
from simulations.forms import SimulationForm


class SimulationEditView(SimulationBaseView, UpdateView):
    template_name = 'simulation/edit.html'
    model = Simulation
    form_class = SimulationForm
    pk_url_kwarg = 'simulation_id'
    context_object_name = 'simulation'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.project_id != kwargs.get('project_id'):
            return HttpResponseRedirect(self.get_success_url())
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.is_ajax():
            form = self.get_form()
            form.is_valid()
            steps_values = {key: form.data[key] for key in form.data.keys() if key.startswith('event_')}
            for value in steps_values.values():
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

    def get_success_url(self):
        return "/react" + str(reverse_lazy('projects:simulations:simulations_list',
                            kwargs={'project_id': self.kwargs.get('project_id')}))

    def get_context_data(self, **kwargs):
        context = super(SimulationEditView, self).get_context_data(**kwargs)
        self.set_projects(context)
        context['steps'] = self.object.step_set.order_by('ordering')
        context = self.context_update(context, self.kwargs.get('project_id'))
        return context

    def form_valid(self, form, contexts):
        data = self.request.POST
        simulation = self.object
        cleaned_data = {
            'name': data.get('name'),
            'description': data.get('description') or "",
            'run_type': data.get('run_type', simulation.run_type),
            'run_count': data.get('run_count', 1),
            'run_time': data.get('run_time', 0),
        }

        avro_error = self.validate_avro_steps(self.request.POST)
        if avro_error:
            return JsonResponse({'error': {'Message failed validation': {'err': avro_error}}}, status=400)

        try:
            self.save_object(obj=simulation, **cleaned_data)
        except Exception as error:
            return self.form_invalid(form, exception=error)

        steps = simulation.step_set.all()
        initial_count_steps = steps.count()
        ordering_data = self.filter_contains(initial_dict=data, filter_by='ordering')
        delete_steps = self.filter_contains(initial_dict=ordering_data, filter_by='delete')
        delete_steps = list(map(lambda key: int(key.rsplit('_', 1)[1]), delete_steps.keys()))
        ordering_data = self.filter_contains(initial_dict=ordering_data, filter_by='delete', not_contains=True)
        steps_data = self.filter_contains(initial_dict=data, filter_by='_')
        new_steps = {key: self.request.POST[key] for key in self.request.POST if
                     '_new_' in key and not key.startswith('delete_')}
        old_steps = {name: value for name, value in steps_data.items() if name not in new_steps}
        new_count_steps = len(ordering_data.values())
        new_steps_list = [search(r'\d+$', key).group(0) for key in new_steps if 'name_' in key]

        if new_count_steps < initial_count_steps and not delete_steps:
            error = 'Duplicate key value violates unique constraint "simulations_step__ordering'
            return self.form_invalid(form, exception=error)

        for step in steps:
            step_id = step.id
            if step_id in delete_steps:
                step.delete()
                continue
            step_info = self.filter_endswith(initial_dict=old_steps, filter_by='_%s' % step_id)
            if 'definition_type' in step_info and step_info['definition_type'] == Step.DEFINITION_SCHEMA:
                # Schemed fields require converting to json
                avro = generate_avro(step_info.get('topic'))
                schema_data = self.filter_startswith(initial_dict=step_info, filter_by='schema_')
                self.convert_schema_types(schema_data, avro)
                step_info['event'] = json.dumps(schema_data)

            # if simulation.type_event == Simulation.STATIC_EVENT:
            #     step_info = self.set_uuid_to_events(step_info)
            # if simulation.type_event == Simulation.UNIQUE_EVENT:
            #     step_info = self.set_clear_events(step_info)

            try:
                self.save_object(obj=step, **step_info)
            except Exception as error:
                return self.form_invalid(form, exception=error)

        self.process_new_steps(new_steps_list, new_steps, simulation, form, contexts, self.form_invalid)

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, **kwargs):
        form.errors['exception'] = kwargs.get('exception')
        return super().form_invalid(form)
