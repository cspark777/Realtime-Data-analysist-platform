import re

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from functions.models import Function, FunctionEndpoint
from kpis.models import KPI
from projects.mixins import ProjectsListMixin
from schemas.models import Schema
from searches.models import Search
from streamprocessors.models import StreamProcessorStep, WorkflowTask
from streams.models import Stream


class StreamProcessorBaseView(LoginRequiredMixin, ProjectsListMixin):
    """Base class for StreamProcessor views"""

    def process_new_steps(self, steps_list, new_steps, streamprocessor, form, form_invalid,
                          new_blocks_ids, new_blocks):
        for new_id in steps_list:
            step_info = self.filter_endswith(initial_dict=new_steps, filter_by='_new_%s' % new_id)
            step_info['streamprocessor'] = streamprocessor

            task_info, task_info_to_db, workflow_task = {}, {}, None
            task_info, task_info_to_db = self.get_workflowtask_info(step_info, task_info, task_info_to_db)

            step_info = {k: v for k, v in step_info.items() if k not in task_info}

            step = StreamProcessorStep()

            try:
                created_step = self.save_object(obj=step, **step_info)
            except Exception as error:
                return form_invalid(form, exception=error)

            if task_info:
                task_info_to_db['streamprocessor_step'] = step
                workflow_task = WorkflowTask()
                try:
                    self.save_object(obj=workflow_task, **task_info_to_db)
                except Exception as error:
                    return form_invalid(form, exception=error)

            if self.step_with_block(created_step.steptype) and new_blocks_ids and new_blocks:
                self.process_new_blocks(new_blocks_ids, new_blocks, created_step, new_id, form, form_invalid)

    def process_new_blocks(self, new_block_count, new_blocks, parent_step, new_steps_id, form, form_invalid):
        step_child = parent_step.get_children()
        step_id = parent_step.id

        for new_block_id in new_block_count:
            pattern_0 = f"^(block_parent_{step_id}).*(_new_{new_block_id})$"
            step_info_0 = {key.replace(f'block_parent_{step_id}_', '', 1): value for key, value in new_blocks.items()
                           if re.match(pattern_0, key)}

            if step_child or step_info_0:
                step_info = step_info_0
            elif not step_child and new_steps_id:
                pattern = f"^(block_parent_new_{new_steps_id}).*(_new_{new_block_id})$"
                step_info = {key.replace(f'block_parent_new_{new_steps_id}_', '', 1): value
                             for key, value in new_blocks.items()
                             if re.match(pattern, key)}
            else:
                continue

            if step_info:
                step_info = self.filter_endswith(initial_dict=step_info, filter_by='_new_%s' % new_block_id)
                step_info['parent'] = parent_step
                new_child = StreamProcessorStep()
                try:
                    self.save_object(obj=new_child, **step_info)
                except Exception as error:
                    return form_invalid(form, exception=error)
            else:
                continue

    def get_workflowtask_info(self, step_info, task_info, task_info_to_db):
        if 'task_recipient_id' in step_info:
            task_info = self.filter_contains(initial_dict=step_info, filter_by='task_')
            task_info_to_db = self.filter_startswith(initial_dict=task_info, filter_by='task_')
        return task_info, task_info_to_db

    @staticmethod
    def context_update(context, project_id):
        step_type_options = {}
        step_types = list(map(lambda step: list(step), list(StreamProcessorStep.STEP_TYPES)))
        context['step_types'] = step_types
        step_type_options['inbound'] = list(filter(lambda item: item[0].startswith('inbound'), step_types))
        step_type_options['outbound'] = list(filter(lambda item: item[0].startswith('outbound'), step_types))
        step_type_options['processor'] = list(filter(lambda item: item[1].startswith('Processor'), step_types))
        context['step_type_options'] = step_type_options
        step_types_data = StreamProcessorStep.STEP_TYPES_DATA
        step_types_data.update(WorkflowTask.STEP_TYPES_DATA)
        context['step_types_data'] = step_types_data
        context['kpi_action_choices'] = list(map(lambda step: list(step), list(StreamProcessorStep.INCREMENT_KEY_TYPES)))
        context['kpi_measurement_choices'] = list(map(lambda step: list(step), list(StreamProcessorStep.UPDATE_KEY_TYPES)))
        context['schemas'] = list(Schema.objects.filter(project_id=project_id).values_list('name', flat=True))
        context['searches'] = list(Search.objects.filter(project_id=project_id).values_list('name', flat=True))
        context['kpi_categories'] = list(KPI.objects.filter(project_id=project_id).values_list('category', flat=True).
                                         distinct().order_by())

        metric_values = list(KPI.objects.filter(project_id=project_id).values_list('category', 'metric', 'indicator_type'))
        category_metrics = dict()
        for entry in metric_values:
            if entry[0] not in category_metrics:
                category_metrics[entry[0]] = []
            category_metrics[entry[0]].append({'name': entry[1], 'type': entry[2]})
        context['category_metrics'] = category_metrics

        streams = Stream.objects.filter(project_id=project_id)
        context['topics'] = list(streams.values('name', 'display_name'))
        schemas = streams.values_list(
            'name', 'schema__name', 'schema__schemafield__name', 'schema__schemafield__type_field'
        )
        schemas_fields = []
        for schema in schemas:
            stream, sch_name, field, field_type = schema
            check_scheme = next(filter(lambda i: i.get('stream') == stream, schemas_fields), {})
            check_fields = check_scheme.get('fields', {})
            if check_scheme and field not in check_fields and not check_fields:
                check_scheme['fields'] = [{'name': field, 'value': field_type}] if field else {}
            elif check_scheme and field not in check_fields and field:
                check_scheme['fields'].append({'name': field, 'value': field_type})
            else:
                schemas_fields.append(
                    {'stream': stream, 'schema': sch_name, 'fields': [{'name': field, 'value': field_type}] if field else []}
                )
        context['schemas_fields'] = schemas_fields
        context['functions'] = list(Function.objects.filter(project_id=project_id).values('name'))
        context['function_endpoints'] = list(
            FunctionEndpoint.objects.filter(Function__project_id=project_id).values('name', 'name', 'Function__name'))
        context['recipients'] = list(map(lambda user: [
            user.get('id'), f"{user.get('first_name')} {user.get('last_name')} < {user.get('email')} >"],
                                         get_user_model().objects.values('id', 'email', 'first_name', 'last_name')))

        return context

    @staticmethod
    def filter_contains(initial_dict, filter_by, is_contains=True):
        if is_contains:
            return {name: value for name, value in initial_dict.items() if name.__contains__(filter_by)}
        return {name: value for name, value in initial_dict.items() if not name.__contains__(filter_by)}

    @staticmethod
    def filter_endswith(initial_dict, filter_by):
        return {name.replace(filter_by, ''): value for name, value in initial_dict.items() if name.endswith(filter_by)}

    @staticmethod
    def filter_startswith(initial_dict, filter_by):
        return {name.replace(filter_by, ''): value for name, value in initial_dict.items() if
                name.startswith(filter_by)}

    @staticmethod
    def save_object(obj, **kwargs):
        for key, value in kwargs.items():
            setattr(obj, key, value)
        obj.save()
        return obj

    def process_old_blocks(self, block_old_steps, parent_step, delete_steps, form, form_invalid):
        blocks_lookup = parent_step.get_children()
        for block in blocks_lookup:
            block_id = block.id
            if block_id in delete_steps:
                block.delete()
                continue

            step_id = parent_step.id
            pattern = f"^(block_parent_{step_id}).*(_{block_id})$"
            block_info = {key.replace(f'block_parent_{step_id}_', '', 1): value
                          for key, value in block_old_steps.items()
                          if re.match(pattern, key)}

            if block_info:
                block_info = self.filter_endswith(initial_dict=block_info, filter_by='_%s' % block_id)
                try:
                    self.save_object(obj=block, **block_info)
                except Exception as error:
                    return form_invalid(form, exception=error)
            else:
                continue

    @staticmethod
    def step_with_block(step_type: str) -> bool:
        return step_type in (
            StreamProcessorStep.FILTER,
            StreamProcessorStep.LOOKUP,
            StreamProcessorStep.SELECTFIELDS,
            StreamProcessorStep.MAP_EVENT,
        )
