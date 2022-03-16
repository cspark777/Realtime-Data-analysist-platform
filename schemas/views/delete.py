from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from schemas.models import Schema
from schemas.views.base import SchemaBaseView


class SchemaDeleteView(SchemaBaseView, DeleteView):
    template_name = 'schemas/delete.html'
    model = Schema
    pk_url_kwarg = 'schema_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.project_id != kwargs.get('project_id'):
            return HttpResponseRedirect(self.get_success_url())
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('projects:schemas:schemas_list', kwargs={'project_id': self.kwargs.get('project_id')})

    def get_context_data(self, **kwargs):
        context = super(SchemaDeleteView, self).get_context_data(**kwargs)
        self.set_projects(context)
        return context
