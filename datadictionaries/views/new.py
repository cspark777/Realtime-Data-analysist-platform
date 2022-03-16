from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.views import generic

from projects.mixins import ProjectsListMixin

from datadictionaries.models import DataDictionary
from datadictionaries.forms import DataDictionaryForm

from .views import save_datadictionary


class DataDictionaryCreateView(LoginRequiredMixin, generic.CreateView, ProjectsListMixin):
    template_name = 'datadictionary/new.html'
    model = DataDictionary
    form_class = DataDictionaryForm

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form, {})
            return JsonResponse({"error": form.errors}, status=400)
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DataDictionaryCreateView, self).get_context_data(**kwargs)
        self.set_projects(context)
        return context

    def get_success_url(self):
        return reverse_lazy('projects:datadictionaries:datadictionaries_list',
                            kwargs={'project_id': self.kwargs.get('project_id')})

    def form_valid(self, form, contexts):
        data = self.request.POST
        datadictionary = self.model()
        cleaned_data = {
            'name': data.get('name'),
            'description': data.get('description') or "",
            'created_by': self.request.user,
            'project_id': self.kwargs.get('project_id'),
        }

        return save_datadictionary(self, form, data, datadictionary, cleaned_data)

    def form_invalid(self, form, **kwargs):
        form.errors['exception'] = kwargs.get('exception')
        return super().form_invalid(form)
