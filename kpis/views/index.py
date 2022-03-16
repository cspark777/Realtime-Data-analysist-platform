from django.views.generic import ListView

from kpis.models import KPI
from .base import KPIBaseView


class KPIView(KPIBaseView, ListView):
    template_name = 'kpis/index.html'
    model = KPI
    paginate_by = 10
    context_object_name = 'kpis'

    def get_queryset(self):
        return self.model.objects.filter(project=self.kwargs.get('project_id'))

    def get_context_data(self, *args, **kwargs):
        context = super(KPIView, self).get_context_data(*args, **kwargs)
        self.set_projects(context)
        return context
