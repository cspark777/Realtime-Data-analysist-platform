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


class SearchBaseView(LoginRequiredMixin, ProjectsListMixin):
    """Base class for Search views"""

    @staticmethod
    def save_object(obj, **kwargs):
        for key, value in kwargs.items():
            # if key == 'limit' and not value:
            #     value = 0
            setattr(obj, key, value)
        obj.save()

    @staticmethod
    def filter_contains(initial_dict, filter_by, is_contains=True):
        if is_contains:
            return {name: value for name, value in initial_dict.items() if name.__contains__(filter_by)}
        return {name: value for name, value in initial_dict.items() if not name.__contains__(filter_by)}

    @staticmethod
    def filter_endswith(initial_dict, filter_by):
        return {name.replace(filter_by, ''): value for name, value in initial_dict.items() if name.endswith(filter_by)}

    def form_invalid(self, form, **kwargs):
        form.errors['exception'] = kwargs.get('exception')
        return super().form_invalid(form)
