from django.urls import reverse_lazy
from django.views.generic import UpdateView

from projects.forms import ProjectForm
from projects.models import Project
from .base import ProjectBaseView


class ProjectEditView(ProjectBaseView, UpdateView):
    template_name = 'projects/edit.html'
    model = Project
    form_class = ProjectForm
    pk_url_kwarg = 'project_id'
    success_url = reverse_lazy('projects:current_project')
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super(ProjectEditView, self).get_context_data(**kwargs)
        context['title_object'] = self.model._meta.model_name
        self.set_projects(context)
        return context
