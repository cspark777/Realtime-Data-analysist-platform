from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from functions.forms import FunctionForm
from functions.models import Function
from functions.views.base import FunctionBaseView
from schemas.models import Schema


class FunctionCreateView(FunctionBaseView, CreateView):
    template_name = 'functions/new.html'
    model = Function
    form_class = FunctionForm

    def get_success_url(self):
        return reverse_lazy('projects:functions:functions_list', kwargs={'project_id': self.kwargs.get('project_id')})

    def get_context_data(self, **kwargs):
        context = super(FunctionCreateView, self).get_context_data(**kwargs)
        self.set_projects(context)
        context['schemas'] = Schema.objects.filter(project=context.get('current_project')).values_list('id', 'name')
        return context

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        cleaned_data['project_id'] = self.kwargs.get('project_id')
        Function = self.model()

        try:
            self.save_object(obj=Function, **cleaned_data)
        except Exception as error:
            return self.form_invalid(form, exception=error)

        data = self.request.POST
        data = self.filter_contains(initial_dict=data, filter_by='delete', not_contains=True)
        fields = self.filter_contains(initial_dict=data, filter_by='_new_')

        new_fields = self.get_fields_forms(fields)

        self.process_new_fields(new_fields, Function, form, self.form_invalid)

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, **kwargs):
        form.errors['exception'] = kwargs.get('exception')
        return super().form_invalid(form)
