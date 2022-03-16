from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

from projects.mixins import ProjectsListMixin
from schemas.models import SchemaField
import json
from core.utils import validate_json_regexp


class SchemaBaseView(LoginRequiredMixin, ProjectsListMixin):
    """Base class for Schemas views"""

    @staticmethod
    def save_object(obj, **kwargs):
        for key, value in kwargs.items():
            setattr(obj, key, value)
        obj.save()

    @transaction.atomic
    def create_schema_fields_from_file(self, uploaded_data, schema):
        if uploaded_data:
            schema_field_objects = []
            for each in uploaded_data["fields"]:
                print (each)
                schema_field_objects.append(
                    SchemaField(name=each["name"], type_field=each["type"], schema=schema))
            if schema_field_objects:
                SchemaField.objects.bulk_create(schema_field_objects)

    def process_new_fields(self, new_fields, schema, form, form_invalid, uploaded_data):
        for new_id, fields in new_fields.items():
            field_info = self.filter_endswith(initial_dict=fields, filter_by='_new_%s' % new_id)
            field_info['schema'] = schema

            schema_field = SchemaField()

            try:
                self.save_object(obj=schema_field, **field_info)
            except Exception as error:
                return form_invalid(form, exception=error)
        try:
            self.create_schema_fields_from_file(uploaded_data, schema)
        except Exception as error:
            error = ("Invalid JSON File")
            return form_invalid(form, exception=error)

    @staticmethod
    def check_json_is_valid(form, file):
        contexts = {}
        data = file.read()
        filename = file.name
        json_data = None
        try:
            json_data = json.loads(data)
            json_data["fields"]
        except (json.JSONDecodeError, ValueError):
            return False, filename
        #model_fields = [each.name for each in SchemaField._meta.get_fields()]
        mandate_fieds = ["name", "type"]
        for each in json_data["fields"]:
            if set(mandate_fieds) != set(each.keys()):
                return False, filename
        return json_data, filename


    @staticmethod
    def get_fields_forms(new_fields):
        fields = {}
        for key, value in new_fields.items():
            try:
                count = int(key.rsplit('_', 1)[1])
            except (ValueError, IndexError):
                continue
            if not fields.get(count):
                fields[count] = {key: value}
            else:
                fields[count][key] = value
        return fields

    @staticmethod
    def filter_contains(initial_dict, filter_by, not_contains=False):
        if not_contains:
            return {name: value for name, value in initial_dict.items() if not name.__contains__(filter_by)}
        return {name: value for name, value in initial_dict.items() if name.__contains__(filter_by)}

    @staticmethod
    def filter_endswith(initial_dict, filter_by):
        return {name.replace(filter_by, ''): value for name, value in initial_dict.items() if name.endswith(filter_by)}
