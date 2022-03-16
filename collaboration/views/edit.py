from django.http import HttpResponseRedirect
from django.views.generic import UpdateView
from django.db import IntegrityError

from collaboration.forms import CollaborationForm
from collaboration.models import Collaboration
from collaboration.views.base import CollaborationBaseView
from django.contrib.auth import get_user_model


class CollaborationEditView(CollaborationBaseView, UpdateView):
    template_name = 'collaboration/edit.html'
    model = Collaboration
    form_class = CollaborationForm
    pk_url_kwarg = 'collaboration_id'
    context_object_name = 'collaboration'

    def get_context_data_as(self, **kwargs):
        context = super(CollaborationEditView, self).get_context_data(**kwargs)
        context['title_object'] = self.model._meta.model_name
        self.set_projects(context)
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        user = get_user_model().objects.filter(email=form.cleaned_data.get("email"))
        if user.exists():
            obj.user = user[0]
        try:
            obj.save()
        except IntegrityError as error:
            return self.form_invalid(form, exception='User already added as a collaborator')
        except Exception as error:
            return self.form_invalid(form, exception=error)

        return HttpResponseRedirect(self.get_success_url())
