from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from projects.forms import ProjectForm
from projects.models import Project
from .base import ProjectBaseView


class ProjectCreateView(ProjectBaseView, CreateView):
    template_name = 'projects/new.html'
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('projects:current_project')

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        kwargs_to_create = {
            'name': cleaned_data.get('name'),
            'description': cleaned_data.get('description'),
            'created_by': self.request.user,
            'druid_url': settings.DRUID_URL,
            'kafka_url': settings.KAFKA_URL_PUBLIC
        }
        self.model.objects.filter(created_by=self.request.user).update(is_current=False)
        self.model.objects.create(**kwargs_to_create)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        context['title_object'] = self.model._meta.model_name
        context['new_project'] = True
        self.set_projects(context)
        return context
