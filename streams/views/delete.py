import json
import requests

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from .base import StreamBaseView
from streams.models import Stream
from streamprocessors.models import StreamProcessor


kafka_url = settings.KAFKA_URL


class StreamDeleteView(StreamBaseView, DeleteView):
    template_name = 'streams/delete.html'
    model = Stream
    pk_url_kwarg = 'stream_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.project_id != kwargs.get('project_id'):
            return HttpResponseRedirect(self.get_success_url())
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return "/react" + str(reverse_lazy('projects:streams:index', kwargs={'project_id': self.kwargs.get('project_id')}))

    def get_context_data(self, **kwargs):
        context = super(StreamDeleteView, self).get_context_data(**kwargs)
        self.set_projects(context)
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        stream_name = self.object.name

        filter_topics = Q()
        filter_topics.add(Q(streamprocessorstep__record_type=stream_name), Q.OR)
        filter_topics.add(Q(streamprocessorstep__topic=stream_name), Q.OR)
        filter_topics.add(Q(streamprocessorstep__lookup_stream=stream_name), Q.OR)
        stream_processors = StreamProcessor.objects.filter(filter_topics)
        if stream_processors.exists():
            stream_processors = map(lambda i: f'"{i}"', stream_processors.values_list('name', flat=True))
            stream_processors = ", ".join(set(stream_processors))
            error = f'Stream processor/s {stream_processors} use this stream.'
            return self.render_to_response(self.get_context_data(error=error))

        project_id = self.kwargs.get('project_id')

        success_url = self.get_success_url()
        self.object.delete()
        data = {
            'stream_name': self.object.name,
            'broker_url': kafka_url,
            'database_url': settings.DRUID_URL,
        }
        server_url = settings.DATA_SERVER + 'druid_kafka_connector'
        if project_id:
            data['project_id'] = project_id
        print("Connecting to " + server_url)
        data = json.dumps(data)
        requests.delete(server_url, data=data)
        return HttpResponseRedirect(success_url)
