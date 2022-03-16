from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import resolve

from analysis.models import Report
from projects.mixins import ProjectsListMixin


class ReportView(LoginRequiredMixin, generic.ListView, ProjectsListMixin):
    model = Report
    paginate_by = 10
    context_object_name = 'reports'

    def get_template_names(self):
        current_url = resolve(self.request.path_info).url_name
        return ['analysis/index.html'] if current_url == 'reports' else ['analysis/index_readonly.html']

    def get_queryset(self):
        return self.model.objects.filter(project=self.kwargs.get('project_id'))

    def get_context_data(self, *args, **kwargs):
        context = super(ReportView, self).get_context_data(*args, **kwargs)
        self.set_projects(context)
        return context