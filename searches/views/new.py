from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, resolve, reverse
from django.views import generic

from core.utils import get_schema_fields
from searches.forms import SearchForm
from searches.models import Search
from streams.models import Stream
from .base import SearchBaseView


class SearchCreateView(SearchBaseView, generic.CreateView):
    template_name = 'searches/new.html'
    model = Search
    form_class = SearchForm

    def get(self, request, *args, **kwargs):
        if not Stream.objects.filter(project_id=kwargs.get('project_id')).exists():
            return HttpResponseRedirect(self.get_success_url())
        return super(SearchCreateView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('projects:searches:index', kwargs={'project_id': self.kwargs.get('project_id')})

    def get_context_data(self, **kwargs):
        context = super(SearchCreateView, self).get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        streams = Stream.objects.filter(project_id=project_id)
        context['stream_names'] = list(streams.values('name', 'display_name'))
        context['schema_fields'] = get_schema_fields(project_id)
        context['init_fields'] = list(context['schema_fields'].values())[0]
        context['page'] = resolve(self.request.path_info).url_name
        self.set_projects(context)
        return context

    def form_valid(self, form):
        kwargs_to_create = {
            **form.cleaned_data,
            'project_id': self.kwargs.get('project_id'),
        }
        self.model.objects.create(**kwargs_to_create)

        return HttpResponseRedirect(self.get_success_url())
