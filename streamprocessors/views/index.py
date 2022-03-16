from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView

from streamprocessors.druid_utils import get_exception_messages
from streamprocessors.models import StreamProcessor
from .base import StreamProcessorBaseView


class StreamProcessorIndexView(StreamProcessorBaseView, ListView):
    template_name = 'streamprocessors/index.html'
    model = StreamProcessor

    def get(self, request, *args, **kwargs):
        get = super(StreamProcessorIndexView, self).get(request, *args, **kwargs)
        project_id = self.kwargs.get('project_id')
        stream_processor_id = self.kwargs.get('streamprocessor_id')
        if stream_processor_id:
            stream_processor = StreamProcessor.objects.filter(pk=stream_processor_id, project=project_id)
            if not stream_processor.exists():
                return HttpResponseRedirect(reverse_lazy('projects:streamprocessors:streamprocessors_list',
                                                         kwargs={'project_id': self.kwargs.get('project_id')}))
        return get

    def get_queryset(self):
        return self.model.objects.filter(project=self.kwargs.get('project_id'))

    def get_context_data(self, *args, **kwargs):
        context = super(StreamProcessorIndexView, self).get_context_data(*args, **kwargs)
        status = self.kwargs.get('status', '')
        context['status'] = status
        context['websocket_server'] = settings.WEBSOCKET_SERVER
        project_id = self.kwargs.get('project_id')
        context["stream_processor_exist"] = StreamProcessor.objects.filter(project=project_id).exists()
        stream_processor_id = self.kwargs.get('streamprocessor_id')
        if stream_processor_id:
            context['message'] = get_exception_messages(_dimension='streamprocessor_id',
                                                        _id=stream_processor_id, _message_type="exception")
        if status:
            context['redirect_url'] = reverse_lazy('projects:streamprocessors:streamprocessors_list',
                                                   kwargs={'project_id': project_id})
        self.set_projects(context)
        return context
