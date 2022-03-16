import re

from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from datadictionaries.models import DataDictionary
from streamprocessors.forms import StreamProcessorForm
from streamprocessors.models import StreamProcessor, StreamProcessorStep
from .base import StreamProcessorBaseView


class StreamProcessorNewView(StreamProcessorBaseView, CreateView):
    template_name = 'streamprocessors/new.html'
    model = StreamProcessor
    form_class = StreamProcessorForm

    def get_success_url(self):
        return "/react" + str(reverse_lazy('projects:streamprocessors:streamprocessors_list',
                                       kwargs={'project_id': self.kwargs.get('project_id')}))

    def get_context_data(self, **kwargs):
        context = super(StreamProcessorNewView, self).get_context_data(**kwargs)
        context = self.context_update(context, self.kwargs.get('project_id'))
        context['data_dictionaries'] = list(
            DataDictionary.objects.filter(project=self.kwargs.get('project_id')).values('name')
        )
        self.set_projects(context)
        return context

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            types = [self.request.POST[key] for key in self.request.POST if key.startswith('steptype_new_')]
            names = [self.request.POST[key] for key in self.request.POST if key.startswith('name_')]
            self.object = None
            form = self.get_form()
            form.is_valid()
            if list(types).count('inbound') > 1:
                form.add_error("steps", "Can't be same types for Inbound Event - Stream.")
            if list(types).count('outbound') > 1:
                form.add_error("steps", "Can't be same types for Outbound Event - Stream.")
            if len(set(names)) != len(names):
                form.add_error("name", "Can't be same step names.")
            if 'inboundtimer' in types and 'lookup' not in types:
                form.add_error("name", "Inbound Timer Task should be followed by Stream Lookup")
            first_step = self.request.POST.get('steptype_new_0')
            if first_step not in (
                    StreamProcessorStep.INBOUND, StreamProcessorStep.INBOUNDTIMER, StreamProcessorStep.INBOUNDHTTP,
                    StreamProcessorStep.INBOUNDKPI):
                form.add_error("steps", "Inbound Event must be the first step.")
            if form.is_valid():
                return self.form_valid(form)
            return JsonResponse({"error": form.errors}, status=400)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = self.model()
        streamprocessor = self.object
        streamprocessor.owning_user = self.request.user
        cleaned_data = form.cleaned_data
        cleaned_data['project_id'] = self.kwargs.get('project_id')
        data = self.request.POST
        cleaned_data['delay_on_uuid_failure'] = data.get('delay_on_uuid_failure', 0)
        cleaned_data['retry_on_uuid_failure_count'] = data.get('retry_on_uuid_failure_count', 0)

        ordering_data = self.filter_contains(initial_dict=self.request.POST, filter_by='ordering')
        ordering_data = self.filter_contains(initial_dict=ordering_data, filter_by='delete', is_contains=False)
        steps_data = self.filter_contains(initial_dict=self.request.POST, filter_by='_')
        steps_data = self.filter_contains(initial_dict=steps_data, filter_by='delete', is_contains=False)
        steps_data = self.filter_contains(initial_dict=steps_data, filter_by='block', is_contains=False)
        new_blocks = {key: self.request.POST[key] for key in self.request.POST
                      if re.match("^(block_).*(_new_)[0-9]+$", key)}
        new_blocks_ids = set(map(lambda i: int(i.rsplit('_', 1)[1]), new_blocks.keys()))

        try:
            self.save_object(obj=streamprocessor, **cleaned_data)
        except Exception as error:
            return self.form_invalid(form, exception=error)

        new_steps = self.filter_contains(initial_dict=steps_data, filter_by='_new_')
        new_count_steps = list(map(lambda i: int(i.rsplit('_', 1)[1]), ordering_data.keys()))
        if new_count_steps and new_steps:
            self.process_new_steps(new_count_steps, new_steps, streamprocessor, form, self.form_invalid,
                                   new_blocks_ids, new_blocks)

        return HttpResponseRedirect(self.get_success_url())

    def get_steps_forms(self):
        steps_forms = self.filter_contains(initial_dict=self.request.POST, filter_by='_')
        steps = {}
        for key, value in steps_forms.items():
            try:
                count = int(key.rsplit('_', 1)[1])
            except ValueError:
                continue
            if not steps.get(count):
                steps[count] = {key: value}
            else:
                steps[count][key] = value
        return list(steps.values())

    def form_invalid(self, form, **kwargs):
        exception = kwargs.get('exception')
        steps_forms = self.get_steps_forms()
        form.errors['exception'] = exception
        return self.render_to_response(self.get_context_data(form=form, steps_forms=steps_forms))
