from django.views.generic import ListView

from functions.models import Function
from functions.views.base import FunctionBaseView

from django.conf import settings

class FunctionView(FunctionBaseView, ListView):
    template_name = 'functions/index.html'
    model = Function
    paginate_by = 10
    context_object_name = 'functions'

    def get_queryset(self):
        return self.model.objects.filter(project=self.kwargs.get('project_id'))

    def get_context_data(self, *args, **kwargs):
        context = super(FunctionView, self).get_context_data(*args, **kwargs)
        self.set_projects(context)
        return context


   