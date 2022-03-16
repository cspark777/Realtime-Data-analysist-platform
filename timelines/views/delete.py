from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from timelines.models import Timeline
from .base import TimelineBaseView


class TimelineDeleteView(TimelineBaseView, DeleteView):
    template_name = 'timelines/delete.html'
    model = Timeline
    pk_url_kwarg = 'timeline_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.project_id != kwargs.get('project_id'):
            return HttpResponseRedirect(self.get_success_url())
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('projects:timelines:index',
                            kwargs={'project_id': self.kwargs.get('project_id')})

    def get_context_data(self, **kwargs):
        context = super(TimelineDeleteView, self).get_context_data(**kwargs)
        unique_key_value = list(self.object.timelineitem_set.values_list("key", flat=True).distinct())
        context["unique_key_value"] = unique_key_value
        self.set_projects(context)
        return context
