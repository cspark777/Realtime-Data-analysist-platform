from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.db import IntegrityError


from collaboration.forms import CollaborationForm
from collaboration.models import Collaboration
from collaboration.views.base import CollaborationBaseView


class CollaborationCreateView(CollaborationBaseView, CreateView):
    template_name = 'collaboration/new.html'
    model = Collaboration
    form_class = CollaborationForm


    def form_valid(self, form):
        obj = form.save(commit=False)
        context = self.get_context_data()
        user = get_user_model().objects.filter(email=form.cleaned_data.get("email"))
        if user.exists():
            obj.user = user[0]
        try:
            obj.project = context['current_project']
            obj.save()
        except IntegrityError as error:
            return self.form_invalid(form, exception='User already added as a collaborator')
        except Exception as error:
            return self.form_invalid(form, exception=error)


        return HttpResponseRedirect(self.get_success_url())
