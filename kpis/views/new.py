from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.urls import reverse_lazy

from kpis.models import KPI
from kpis.forms import KPIForm
from .base import KPIBaseView


class KPICreateView(KPIBaseView, CreateView):
    template_name = 'kpis/new.html'
    model = KPI
    form_class = KPIForm

    def get_success_url(self):
        return reverse_lazy('projects:streamprocessors:kpis:kpi_list',
                            kwargs={'project_id': self.kwargs.get('project_id')})

    def form_valid(self, form):
        print("Saving!")
        cleaned_data = form.cleaned_data
        kwargs_to_create = {
            'category': cleaned_data.get('category'),
            'metric': cleaned_data.get('metric'),
            'indicator_type': cleaned_data.get('indicator_type'),
            'created_by': self.request.user,
            'project_id': self.kwargs.get('project_id'),
        }
        print(kwargs_to_create)
        self.model.objects.create(**kwargs_to_create)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(KPICreateView, self).get_context_data(**kwargs)
        self.set_projects(context)
        return context
