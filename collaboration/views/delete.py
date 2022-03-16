from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from collaboration.models import Collaboration
from collaboration.views.base import CollaborationBaseView


class CollaborationDeleteView(CollaborationBaseView, DeleteView):
    template_name = 'collaboration/delete.html'
    model = Collaboration
    pk_url_kwarg = 'collaboration_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.project_id != kwargs.get('project_id'):
            return HttpResponseRedirect(self.get_success_url())
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
