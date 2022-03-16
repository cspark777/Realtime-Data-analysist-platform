from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from projects.mixins import ProjectsListMixin

from datadictionaries.models import DataDictionary


class DataDictionariesList(LoginRequiredMixin, generic.ListView, ProjectsListMixin):
    template_name = 'datadictionary/index.html'
    model = DataDictionary
    paginate_by = 10
    context_object_name = 'datadictionaries'

    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user, project=self.kwargs.get('project_id'))

    def get_context_data(self, *args, **kwargs):
        context = super(DataDictionariesList, self).get_context_data(*args, **kwargs)
        self.set_projects(context)
        print(context)
        return context
