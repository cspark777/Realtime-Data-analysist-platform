from django.http import HttpResponseRedirect
from django.views.generic import DeleteView
from django.urls import reverse_lazy

from kpis.models import KPI
from .base import KPIBaseView


class KPIDeleteView(KPIBaseView, DeleteView):
    template_name = 'kpis/delete.html'
    model = KPI
    pk_url_kwarg = 'KPI_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.project_id != kwargs.get('project_id'):
            return HttpResponseRedirect(self.get_success_url())
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('projects:streamprocessors:kpis:kpi_list',
                            kwargs={'project_id': self.kwargs.get('project_id')})

    def get_context_data(self, **kwargs):
        context = super(KPIDeleteView, self).get_context_data(**kwargs)
        self.set_projects(context)
        return context
