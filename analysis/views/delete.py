from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from analysis.models import Report
from projects.mixins import ProjectsListMixin


class ReportDeleteView(LoginRequiredMixin, generic.DeleteView, ProjectsListMixin):
    template_name = 'analysis/delete.html'
    model = Report
    pk_url_kwarg = 'report_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.project_id != kwargs.get('project_id'):
            return HttpResponseRedirect(self.get_success_url())
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('projects:analysis:reports', kwargs={'project_id': self.kwargs.get('project_id')})

    def get_context_data(self, **kwargs):
        context = super(ReportDeleteView, self).get_context_data(**kwargs)
        self.set_projects(context)
        return context