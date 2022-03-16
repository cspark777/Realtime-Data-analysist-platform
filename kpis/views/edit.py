from django.http import HttpResponseRedirect
from django.views.generic import UpdateView
from django.urls import reverse_lazy

from kpis.forms import KPIForm
from kpis.models import KPI
from .base import KPIBaseView


class KPIEditView(KPIBaseView, UpdateView):
    template_name = 'kpis/edit.html'
    model = KPI
    form_class = KPIForm
    pk_url_kwarg = 'KPI_id'
    context_object_name = 'KPI'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.project_id != kwargs.get('project_id'):
            return HttpResponseRedirect(self.get_success_url())
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('projects:streamprocessors:kpis:kpi_list',
                            kwargs={'project_id': self.kwargs.get('project_id')})

    def form_valid(self, form):
        kpi = self.object
        cleaned_data = form.cleaned_data

        try:
            print(self)
            self.save_object(obj=kpi, **cleaned_data)
        except Exception as error:
            return self.form_invalid(form, exception=error)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(KPIEditView, self).get_context_data(**kwargs)
        self.set_projects(context)
        return context

    @staticmethod
    def save_object(obj, **kwargs):
        for key, value in kwargs.items():
            setattr(obj, key, value)
        obj.save()

    def form_invalid(self, form, **kwargs):
        form.errors['exception'] = kwargs.get('exception')
        return super().form_invalid(form)
