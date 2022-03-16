from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from projects.mixins import ProjectsListMixin
from collaboration.models import Collaboration


class CollaborationBaseView(LoginRequiredMixin, ProjectsListMixin):
    """Base class for Schemas views"""

    def get_context_data(self, **kwargs):
        context = super(CollaborationBaseView, self).get_context_data(**kwargs)
        self.set_projects(context)
        return context

    def get_success_url(self):
        return reverse_lazy('projects:collaboration:collaboration_list', kwargs={'project_id': self.kwargs.get('project_id')})

    def form_invalid(self, form, **kwargs):
        form.errors['exception'] = kwargs.get('exception')
        return super().form_invalid(form)
