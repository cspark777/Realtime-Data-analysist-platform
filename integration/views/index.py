from django.views.generic import ListView

from integration.models import DataSource
from integration.views.base import DataSourceBaseView


class DataSourceView(DataSourceBaseView, ListView):
    template_name = 'integration/index.html'
    model = DataSource
    paginate_by = 10
    context_object_name = 'data_source'

    def get_queryset(self):
        return self.model.objects.filter(project=self.kwargs.get('project_id'))

    def get_context_data(self, *args, **kwargs):
        context = super(DataSourceView, self).get_context_data(*args, **kwargs)
        self.set_projects(context)
        context["datasource_exists"] = DataSource.objects.filter(project=self.kwargs.get('project_id')).exists()
        return context
