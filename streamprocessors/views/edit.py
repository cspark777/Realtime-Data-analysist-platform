import re
from re import search

from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from datadictionaries.models import DataDictionary
from streamprocessors.forms import StreamProcessorForm
from streamprocessors.models import StreamProcessor, StreamProcessorStep, WorkflowTask
from .base import StreamProcessorBaseView


class StreamProcessorEditView(StreamProcessorBaseView, UpdateView):
    template_name = 'streamprocessors/edit.html'
    model = StreamProcessor
    form_class = StreamProcessorForm
    pk_url_kwarg = 'streamprocessor_id'
    context_object_name = 'streamprocessor'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.project_id != kwargs.get('project_id'):
            return HttpResponseRedirect(self.get_success_url())
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return "/react" + str(reverse_lazy('projects:streamprocessors:streamprocessors_list',
                            kwargs={'project_id': self.kwargs.get('project_id')}))

    default_fields = (
        'broker_id',
        'database_id',
        'category_name',
        'expression',
        'field',
        'filter_value',
        'lookup_field',
        'lookup_value',
        'metric',
        'record',
        'record_type',
        'subtype',
        'topic',
        'value',
        'destination',
        'source',
        'key_type',
        'key_value',
        'time_window',
        'result_placement',
        'operator',
        'column_name',
        'lookup_stream',
        'field_to_process',
        'event_type',
    )

    def get_context_data(self, **kwargs):
        context = super(StreamProcessorEditView, self).get_context_data(**kwargs)
        context['steps'] = self.object.streamprocessorstep_set.order_by('ordering')
        context = self.context_update(context, self.kwargs.get('project_id'))
        context['data_dictionaries'] = list(DataDictionary.objects.filter(project=self.object.project).values('name'))
        self.set_projects(context)
        return context

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            types = [self.request.POST[key] for key in self.request.POST if key.startswith('steptype_')]
            names = [self.request.POST[key] for key in self.request.POST if key.startswith('name_')]
            self.object = self.get_object()
            form = self.get_form()
            form.is_valid()
            if list(types).count('inbound') > 1:
                form.add_error("name", "Can't be same types for Inbound Event - Stream.")
            if list(types).count('outbound') > 1:
                form.add_error("name", "Can't be same types for Outbound Event - Stream.")
            if len(set(names)) != len(names):
                form.add_error("name", "Can't be same step names.")
            if 'inboundtimer' in types and 'lookup' not in types:
                form.add_error("name", "Inbound Timer Task should be followed by Stream Lookup")
            first_step = None
            step_types = {key: self.request.POST[key] for key in self.request.POST.keys() if
                          key.startswith('steptype_')}
            if step_types:
                keys = list(step_types.keys())
                first_step = step_types[keys[0]]
            if first_step not in (StreamProcessorStep.INBOUND, StreamProcessorStep.INBOUNDTIMER,
                                  StreamProcessorStep.INBOUNDHTTP, StreamProcessorStep.INBOUNDKPI):
                form.add_error("name", "Inbound Event must be the first step.")
            if form.is_valid():
                return self.form_valid(form)
            return JsonResponse({"error": form.errors}, status=400)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        streamprocessor = self.object
        cleaned_data = form.cleaned_data
        data = self.request.POST
        cleaned_data['delay_on_uuid_failure'] = data.get('delay_on_uuid_failure', 50)
        cleaned_data['retry_on_uuid_failure_count'] = data.get('retry_on_uuid_failure_count', 10)

        steps = streamprocessor.streamprocessorstep_set.all()
        steps = [i for i in steps]
        initial_count_steps = len(steps)
        ordering_data = {key: self.request.POST for key in self.request.POST if key.startswith('ordering_')}
        delete_steps = set([int(search(r'\d+$', key).group(0)) for key in self.request.POST
                            if 'delete_' in key])
        try:
            self.save_object(obj=streamprocessor, **cleaned_data)
        except Exception as error:
            return self.form_invalid(form, exception=error)
        new_steps = {key: self.request.POST[key] for key in self.request.POST
                     if '_new_' in key and not key.startswith('delete_') and 'block' not in key}

        new_blocks = {key: self.request.POST[key] for key in self.request.POST
                      if re.match("^(block_).*(_new_)[0-9]+$", key)}
        old_steps = {key: self.request.POST[key] for key in self.request.POST
                     if '_' in key and '_new_' not in key and 'block' not in key}

        block_old_steps = {key: self.request.POST[key] for key in self.request.POST
                           if re.match("^(block_parent_)[0-9]+.*(_)[0-9]+$", key)}
        new_count_steps = len(set(ordering_data))

        new_steps_ids = set(map(lambda i: int(i.rsplit('_', 1)[1]), new_steps.keys()))
        new_blocks_ids = set(map(lambda i: int(i.rsplit('_', 1)[1]), new_blocks.keys()))

        if new_count_steps < initial_count_steps and not delete_steps:
            error = 'Duplicate key value violates unique constraint "streamprocessors_step__ordering'
            return self.form_invalid(form, exception=error)

        for step in steps:
            step_id = step.id
            if step_id in delete_steps:
                step.delete()
                continue
            step_info = self.filter_endswith(initial_dict=old_steps, filter_by='_%s' % step_id)

            task_info, task_info_to_db, workflow_task = {}, {}, None
            task_info, task_info_to_db = self.get_workflowtask_info(step_info, task_info, task_info_to_db)

            step_info = {k: v for k, v in step_info.items() if k not in task_info}

            exist_workflow = WorkflowTask.objects.filter(streamprocessor_step=step).first()
            if exist_workflow and not task_info:
                exist_workflow.delete()

            if task_info:
                workflow_task = step.workflowtask_set.first()
                if not workflow_task:
                    workflow_task = WorkflowTask()
                task_info_to_db['streamprocessor_step'] = step
                try:
                    self.save_object(obj=workflow_task, **task_info_to_db)
                except Exception as error:
                    return self.form_invalid(form, exception=error)

            try:
                self.set_default_values(obj=step)
                created_step = self.save_object(obj=step, **step_info)
            except Exception as error:
                return self.form_invalid(form, exception=error)

            if self.step_with_block(created_step.steptype):
                if block_old_steps:
                    self.process_old_blocks(block_old_steps, created_step, delete_steps,
                                            form, self.form_invalid)
                if new_blocks_ids and new_blocks:
                    self.process_new_blocks(new_blocks_ids, new_blocks, created_step, created_step.id,
                                            form, self.form_invalid)

        if new_steps_ids and new_steps:
            self.process_new_steps(new_steps_ids, new_steps, streamprocessor, form, self.form_invalid,
                                   new_blocks_ids, new_blocks)

        return HttpResponseRedirect(self.get_success_url())

    def set_default_values(self, obj):
        for field in self.default_fields:
            default_value = None if field != 'event_type' else ''
            setattr(obj, field, default_value)
        obj.save()

    def form_invalid(self, form, **kwargs):
        form.errors['exception'] = kwargs.get('exception')
        return super().form_invalid(form)
