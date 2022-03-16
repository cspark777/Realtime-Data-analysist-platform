from django.contrib.auth.mixins import LoginRequiredMixin

from projects.mixins import ProjectsListMixin
from integration.models import DataSource


class DataSourceBaseView(LoginRequiredMixin, ProjectsListMixin):
    """Base class for Schemas views"""

    @staticmethod
    def save_object(obj, **kwargs):
        for key, value in kwargs.items():
            setattr(obj, key, value)
        obj.save()

    def process_new_fields(self, new_fields, schema, form, form_invalid):
        for new_id, fields in new_fields.items():
            field_info = self.filter_endswith(initial_dict=fields, filter_by='_new_%s' % new_id)
            field_info['schema'] = schema

            schema_field = SchemaField()

            try:
                self.save_object(obj=schema_field, **field_info)
            except Exception as error:
                return form_invalid(form, exception=error)

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
