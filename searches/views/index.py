from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import resolve

from searches.models import Search
from projects.mixins import ProjectsListMixin
from streams.models import Stream


class SearchView(LoginRequiredMixin, generic.ListView, ProjectsListMixin):
    model = Search
    paginate_by = 10
    context_object_name = 'searches'

    def get_template_names(self):
        current_url = resolve(self.request.path_info).url_name
        return ['searches/index.html'] if current_url == 'index' else ['searches/index_readonly.html']

    def get_queryset(self):
        return self.model.objects.filter(project=self.kwargs.get('project_id'))

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        self.set_projects(context)
        context['can_create'] = Stream.objects.filter(project=context['current_project'].id).exists()
        return context
