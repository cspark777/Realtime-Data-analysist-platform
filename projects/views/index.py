from django.db.models import Q
from django.views.generic import ListView

from projects.models import Project
from .base import ProjectBaseView


class ProjectsView(ProjectBaseView, ListView):
    template_name = 'projects/projects_list.html'
    model = Project
    paginate_by = 10
    context_object_name = 'projects'

    def get_queryset(self):
        return self.model.objects.filter(
            Q(created_by=self.request.user) | Q(collaboration__email=self.request.user)
        )

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectsView, self).get_context_data(*args, **kwargs)
        self.set_projects(context)
        context["list_project"] = True
        return context
