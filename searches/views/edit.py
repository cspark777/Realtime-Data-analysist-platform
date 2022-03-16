import json

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, resolve, reverse
from django.views import generic

from core.utils import get_schema_fields
from searches.forms import SearchForm
from searches.models import Search
from streams.models import Stream
from .base import SearchBaseView


class SearchEditView(SearchBaseView, generic.UpdateView):
    model = Search
    form_class = SearchForm
    pk_url_kwarg = 'search_id'
    context_object_name = 'search'

    def get_template_names(self):
        url_name = resolve(self.request.path).url_name
        if url_name == 'edit':
            return ['searches/edit.html']
        else:
            return ['searches/show.html']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.project_id != kwargs.get('project_id'):
            return HttpResponseRedirect(self.get_success_url())
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('projects:searches:index', kwargs={'project_id': self.kwargs.get('project_id')})

    def get_context_data(self, **kwargs):
        context = super(SearchEditView, self).get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        streams = Stream.objects.filter(project_id=project_id)
        context['stream_names'] = list(streams.values('name', 'display_name'))
        context['schema_fields'] = get_schema_fields(project_id)
        context['search_data'] = json.loads(self.get_object().search_data)
        context['page'] = resolve(self.request.path_info).url_name
        self.set_projects(context)
        return context

    def form_valid(self, form):
        search = self.object
        cleaned_data = form.cleaned_data
        print(cleaned_data)
        try:
            self.save_object(obj=search, **cleaned_data)
        except Exception as error:
            return self.form_invalid(form, exception=error)

        return HttpResponseRedirect(self.get_success_url())
