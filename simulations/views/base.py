import json
import time
import uuid

from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin

from core.utils import generate_avro, validate_message_avro, get_schema_fields, validate_json_regexp
from projects.mixins import ProjectsListMixin
from simulations.models import Simulation, Step
from streams.models import Stream
from schemas.models import SchemaField


class SimulationBaseView(LoginRequiredMixin, ProjectsListMixin):
    """Base class for Simulation views"""

    def process_new_steps(self, steps_list, new_steps, simulation, form, contexts, form_invalid):
        for new_id in steps_list:
            step_info = self.filter_endswith(initial_dict=new_steps, filter_by='_new_%s' % new_id)
            step_info['simulation'] = simulation

            if 'event' not in step_info and ('definition_type' not in step_info or
                                             step_info['definition_type'] == Step.DEFINITION_JSON):
                self.create_simulations_from_file(contexts['event_new_%s' % new_id], step_info)
            else:
                if step_info['definition_type'] == Step.DEFINITION_SCHEMA:
                    avro = generate_avro(step_info.get('topic'))
                    schema_data = self.filter_startswith(initial_dict=step_info, filter_by='schema_')
                    self.convert_schema_types(schema_data, avro)
                    step_info['event'] = json.dumps(schema_data)

                step = Step()

                # if simulation.type_event == Simulation.STATIC_EVENT:
                #     step_info = self.set_uuid_to_events(step_info)
                # if simulation.type_event == Simulation.UNIQUE_EVENT:
                #     step_info = self.set_clear_events(step_info)

                try:
                    self.save_object(obj=step, **step_info)
                except Exception as error:
                    return form_invalid(form, exception=error)

    def validate_avro_steps(self, data):
        modified_steps = {}
        for key in data:
            if not key.startswith('delete_'):
                key_parts = key.split('_')
                step_id = key_parts[-1]
                key_name = '_'.join(key_parts[:-1])
                if step_id.isdigit():
                    if step_id not in modified_steps:
                        modified_steps[step_id] = {}
                    modified_steps[step_id][key_name] = self.request.POST[key]

        for step_data in modified_steps.values():
            avro = generate_avro(step_data.get('topic'))
            is_regexp = step_data.get('is_regexp') == 'True'
            if avro:
                event = step_data.get('event')
                if event is None:
                    schema_data = self.filter_startswith(initial_dict=step_data, filter_by='schema_')
                    if not is_regexp:
                        self.convert_schema_types(schema_data, avro)
                    event = json.dumps(schema_data)
                try:
                    # Ignore regexp for now, needs to be updated
                    # Event is null only if it is a file, don't validate
                    if event:
                        if not is_regexp:
                            validate_message_avro(event, avro)
                        else:
                            regexp_error = validate_json_regexp(event, avro['fields'])
                            if regexp_error:
                                return regexp_error
                except Exception as exception:
                    return str(exception)
        return ''

    @staticmethod
    def convert_schema_types(data, avro):
        """Schema fields are returned as strings in simulations by default.
        This method removes blank strings and converts str to int if needed."""
        fields = avro['fields']
        field_types = {item['name']: item['type'] for item in fields}
        keys_to_remove = []

        for field, value in data.items():
            if field in field_types:
                if not value and 'null' in field_types[field]:
                    keys_to_remove.append(field)
                elif SchemaField.INT in field_types[field]:
                    try:
                        data[field] = int(data[field])
                    except ValueError:
                        pass
                elif SchemaField.FLOAT in field_types[field]:
                    try:
                        data[field] = float(data[field])
                    except ValueError:
                        pass

        for key in keys_to_remove:
            if key in data:
                del data[key]

        return data

    def set_uuid_to_events(self, steps):
        if not isinstance(steps, (list, tuple)):
            new_steps = (steps,)
        else:
            new_steps = steps

        for step in new_steps:
            event = json.loads(step.get('event'))
            event = self.set_timestamp_uuid(event)
            step['event'] = json.dumps(event)

        if not isinstance(steps, (list, tuple)) and new_steps:
            new_steps = new_steps[0]
        return new_steps

    @staticmethod
    def check_json_is_valid(form, files):
        contexts = {}
        if any(map(lambda x: x.startswith('event_new_'), files)):
            for filename in filter(lambda x: x.startswith('event_new_'), files):
                contexts[filename] = files.get(filename).file.read()
                try:
                    events = json.loads(contexts[filename])
                except (json.JSONDecodeError, ValueError):
                    form.add_error("steps", "Invalid JSON in file")
        return form, contexts

    @staticmethod
    def context_update(context, project_id):
        context['schema_fields'] = get_schema_fields(project_id)
        context['topics'] = list(Stream.objects.filter(project_id=project_id).values('name', 'display_name'))
        context['delay_types'] = [list(choice) for choice in Step.DELAY_CHOICES]
        context['definition_types'] = [list(choice) for choice in Step.DEFINITION_CHOICES]
        context['run_type_choices'] = [list(choice) for choice in Simulation.RUN_TYPE_CHOICES]
        return context

    @staticmethod
    def filter_contains(initial_dict, filter_by, not_contains=False):
        if not_contains:
            return {name: value for name, value in initial_dict.items() if not name.__contains__(filter_by)}
        return {name: value for name, value in initial_dict.items() if name.__contains__(filter_by)}

    @staticmethod
    def filter_endswith(initial_dict, filter_by):
        return {name.replace(filter_by, ''): value for name, value in initial_dict.items() if name.endswith(filter_by)}

    @staticmethod
    def filter_startswith(initial_dict, filter_by):
        return {name.replace(filter_by, ''): value for name, value in initial_dict.items() if name.startswith(filter_by)}

    @staticmethod
    def save_object(obj, **kwargs):
        for key, value in kwargs.items():
            setattr(obj, key, value)
        obj.save()

    @staticmethod
    def set_clear_events(steps):
        if not isinstance(steps, (list, tuple)):
            new_steps = (steps,)
        else:
            new_steps = steps

        for step in new_steps:
            event = json.loads(step.get('event'))
            event.pop('uuid', None)
            event.pop('timestamp', None)
            step['event'] = json.dumps(event)

        if not isinstance(steps, (list, tuple)) and new_steps:
            new_steps = new_steps[0]
        return new_steps

    @staticmethod
    def set_timestamp_uuid(event):
        if 'uuid' not in event:
            event['uuid'] = str(uuid.uuid4())
        if 'timestamp' not in event:
            event['timestamp'] = int(time.time() * 1000)
        return event

    @transaction.atomic
    def create_simulations_from_file(self, context, step_info):
        events = json.loads(context)
        for ordering, event in enumerate(events, start=int(step_info.get('ordering', 1))):
            step = Step()

            event = self.set_timestamp_uuid(event)

            step_info['event'] = json.dumps(event)
            step_info['ordering'] = ordering
            self.save_object(obj=step, **step_info)
