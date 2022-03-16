from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from groups.api.views import ORGANISATION_SHARED_STREAMS
from groups.models import StreamGroup
from .base import StreamBaseView
from streams.forms import StreamForm
from streams.models import Stream


class StreamEditView(StreamBaseView, UpdateView):
    template_name = "streams/edit.html"
    model = Stream
    form_class = StreamForm
    pk_url_kwarg = "stream_id"
    context_object_name = "stream"

    def get_initial(self):
        initial = super(StreamEditView, self).get_initial()
        initial["project_id"] = self.kwargs.get("project_id")
        return initial

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.project_id != kwargs.get("project_id"):
            return HttpResponseRedirect(self.get_success_url())
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return "/react" + str(
            reverse_lazy(
                "projects:streams:index",
                kwargs={"project_id": self.kwargs.get("project_id")},
            )
        )

    def form_valid(self, form):
        stream = self.object
        cleaned_data = form.cleaned_data
        changed_data = form.changed_data
        stream_data = {
            "name": cleaned_data.get("name"),
            "description": cleaned_data.get("description"),
            "broker_id": cleaned_data.get("broker_id"),
            "project_id": self.kwargs.get("project_id"),
        }
        for key, value in stream_data.items():
            if key in changed_data:
                setattr(stream, key, value)

        if stream.share:
            group, _ = StreamGroup.objects.get_or_create(
                name=ORGANISATION_SHARED_STREAMS,
                organisation=self.request.user.organisation,
                is_organisation_shared=True,
            )

            stream.group = group

        stream.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(StreamEditView, self).get_context_data(**kwargs)
        self.set_projects(context)
        return context
