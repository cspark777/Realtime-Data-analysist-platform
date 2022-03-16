from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic import DetailView

from projects.models import Project
from streamprocessors.models import WorkflowTask
from .base import ProjectBaseView


class ProjectView(ProjectBaseView, DetailView):
    template_name = 'projects/index.html'
    model = Project
    context_object_name = 'project'
    pk_url_kwarg = 'project_id'

    def get(self, request, *args, **kwargs):
        user = request.user
        if kwargs.get(self.pk_url_kwarg):
            try:
                self.object = self.get_object()
            except Http404:
                return HttpResponseRedirect(reverse_lazy('projects:current_project'))
            self.model.objects.filter(created_by=user).update(is_current=False)
            self.object.is_current = True
            self.object.save()
        else:
            self.object = self.model.objects.filter(is_current=True, created_by=user).first()
        context = self.get_context_data(object=self.object)
        self.set_projects(context)
        workflow_tasks_count = WorkflowTask.objects.filter(recipient=user).count()
        context['workflow_tasks_count'] = workflow_tasks_count
        return self.render_to_response(context)

    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user)
