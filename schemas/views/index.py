from django.views.generic import ListView

from schemas.models import Schema
from schemas.views.base import SchemaBaseView


class SchemaView(SchemaBaseView, ListView):
    template_name = 'schemas/index.html'
    model = Schema
    paginate_by = 10
    context_object_name = 'schemas'

    def get_queryset(self):
        return self.model.objects.filter(project=self.kwargs.get('project_id'))

    def get_context_data(self, *args, **kwargs):
        context = super(SchemaView, self).get_context_data(*args, **kwargs)
        self.set_projects(context)
        return context
