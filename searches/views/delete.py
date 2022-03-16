from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from searches.models import Search
from projects.mixins import ProjectsListMixin


class SearchDeleteView(LoginRequiredMixin, generic.DeleteView, ProjectsListMixin):
    template_name = 'searches/delete.html'
    model = Search
    pk_url_kwarg = 'search_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.project_id != kwargs.get('project_id'):
            return HttpResponseRedirect(self.get_success_url())
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('projects:searches:index', kwargs={'project_id': self.kwargs.get('project_id')})

    def get_context_data(self, **kwargs):
        context = super(SearchDeleteView, self).get_context_data(**kwargs)
        self.set_projects(context)
        return context
