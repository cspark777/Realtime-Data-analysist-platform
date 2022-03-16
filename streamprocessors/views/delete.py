from django.views.generic import DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .base import StreamProcessorBaseView
from streamprocessors.models import StreamProcessor


class StreamProcessorDeleteView(StreamProcessorBaseView, DeleteView):
    template_name = 'streamprocessors/delete.html'
    model = StreamProcessor
    pk_url_kwarg = 'streamprocessor_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.project_id != kwargs.get('project_id'):
            return HttpResponseRedirect(self.get_success_url())
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return "/react" + str(reverse_lazy('projects:streamprocessors:streamprocessors_list',
                            kwargs={'project_id': self.kwargs.get('project_id')}))

    def get_context_data(self, **kwargs):
        context = super(StreamProcessorDeleteView, self).get_context_data(**kwargs)
        self.set_projects(context)
        return context
