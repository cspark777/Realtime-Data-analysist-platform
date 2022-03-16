from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views import generic

from projects.mixins import ProjectsListMixin

from datadictionaries.models import DataDictionary


class DataDictionaryDeleteView(LoginRequiredMixin, generic.DeleteView, ProjectsListMixin):
    template_name = 'datadictionary/delete.html'
    model = DataDictionary
    pk_url_kwarg = 'datadictionary_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.project_id != kwargs.get('project_id'):
            return HttpResponseRedirect(self.get_success_url())
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('projects:datadictionaries:datadictionaries_list',
                            kwargs={'project_id': self.kwargs.get('project_id')})

    def get_context_data(self, **kwargs):
        context = super(DataDictionaryDeleteView, self).get_context_data(**kwargs)
        self.set_projects(context)
        return context