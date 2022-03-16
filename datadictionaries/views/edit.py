from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.views import generic

from projects.mixins import ProjectsListMixin

from datadictionaries.models import DataDictionary
from datadictionaries.forms import DataDictionaryForm
from .views import save_datadictionary


class DataDictionaryEditView(LoginRequiredMixin, generic.UpdateView, ProjectsListMixin):
    template_name = 'datadictionary/edit.html'
    model = DataDictionary
    form_class = DataDictionaryForm
    pk_url_kwarg = 'datadictionary_id'
    context_object_name = 'datadictionary'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.project_id != kwargs.get('project_id'):
            return HttpResponseRedirect(self.get_success_url())
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.is_ajax():
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form, {})
            return JsonResponse({"error": form.errors}, status=400)
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('projects:datadictionaries:datadictionaries_list',
                            kwargs={'project_id': self.kwargs.get('project_id')})

    def get_context_data(self, **kwargs):
        context = super(DataDictionaryEditView, self).get_context_data(**kwargs)
        context['items'] = self.object.items.all()
        self.set_projects(context)
        return context

    def form_valid(self, form, contexts):
        data = self.request.POST
        datadictionary = self.object
        cleaned_data = {
            'name': data.get('name'),
            'description': data.get('description') or "",
        }

        return save_datadictionary(self, form, data, datadictionary, cleaned_data)

    def form_invalid(self, form, **kwargs):
        form.errors['exception'] = kwargs.get('exception')
        return super().form_invalid(form)
