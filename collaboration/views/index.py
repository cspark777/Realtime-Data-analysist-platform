from django.views.generic import ListView

from collaboration.models import Collaboration
from collaboration.views.base import CollaborationBaseView


class CollaborationView(CollaborationBaseView, ListView):
    template_name = 'collaboration/index.html'
    model = Collaboration
    paginate_by = 10
    context_object_name = 'collaboration_objects'

    def get_queryset(self):
        return self.model.objects.filter(project=self.kwargs.get('project_id'))

    def get_context_data(self, *args, **kwargs):
        context = super(CollaborationView, self).get_context_data(*args, **kwargs)
        self.set_projects(context)
        return context
