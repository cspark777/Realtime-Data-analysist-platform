from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from projects.models import Project
from .base import ProjectBaseView


class ProjectDeleteView(ProjectBaseView, DeleteView):
    template_name = 'projects/delete.html'
    model = Project
    success_url = reverse_lazy('projects:projects_list')
    pk_url_kwarg = 'project_id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        if self.object.is_current:
            current_project = self.model.objects.first()
            if current_project:
                current_project.is_current = True
                current_project.save()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super(ProjectDeleteView, self).get_context_data(**kwargs)
        self.set_projects(context)
        return context
