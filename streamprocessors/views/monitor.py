import json
from datetime import datetime

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from pydruid.db import connect

from analysis.models import Report, ReportItem
from core.utils import get_database_data, generate_avro
from datadictionaries.models import DataDictionary
from projects.mixins import set_projects
from projects.models import Project
from simulations.models import Simulation
from streamprocessors.druid_utils import get_payload_interval, execute_druid_query, correct_schema_names
from streamprocessors.forms import TestSimulateForm
from streamprocessors.kafka_utils import send_kafka_message
from streamprocessors.models import StreamProcessor, StreamProcessorStep, WorkflowTask
from streams.models import Stream
from streams.utils import parse_simple_time_interval
from .base import StreamProcessorBaseView
from django.views.generic import DetailView
from streamprocessors.forms import StreamProcessorForm

kafka_url = settings.KAFKA_URL
druid_host, druid_port = get_database_data()


class StreamProcessorMonitorView(StreamProcessorBaseView, DetailView):
    template_name = 'streamprocessors/monitor.html'
    model = StreamProcessor
    pk_url_kwarg = 'streamprocessor_id'

    @login_required
    def streamprocessor_monitor(request, project_id, streamprocessor_id):

        url = reverse_lazy('projects:streamprocessors:monitor',
                        kwargs={'project_id': project_id,
                                'streamprocessor_id': streamprocessor_id})
        return redirect(url)

    def get_context_data(self, **kwargs):
        context = super(StreamProcessorMonitorView, self).get_context_data(**kwargs)
        self.set_projects(context)
        return context

