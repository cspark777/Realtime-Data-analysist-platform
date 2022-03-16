from re import search
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import CreateView
from django.urls import reverse_lazy

from core.utils import get_schema_fields
from timelines.forms import TimelineForm
from timelines.models import Timeline, TimelineItem
from streams.models import Stream
from .base import TimelineBaseView


class TimelineCreateView(TimelineBaseView, CreateView):
    template_name = 'timelines/new.html'
    model = Timeline
    form_class = TimelineForm

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            form = self.get_form()
            form.is_valid()
            if form.is_valid():
                return self.form_valid(form)
            return JsonResponse({"error": form.errors}, status=400)
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('projects:timelines:index', kwargs={'project_id': self.kwargs.get('project_id')})

    def form_valid(self, form):
        project_id = self.kwargs.get('project_id')
        cleaned_data = form.cleaned_data

        timeline_in_db = Timeline.objects.filter(name=cleaned_data.get('name'))

        if timeline_in_db.exists():
            error = 'This timeline exists in another project!'
            return self.render_to_response(self.get_context_data(error=error))

        timeline_data = {
            'project_id': project_id,
            'created_by_id': self.request.user.id,
        }
        cleaned_data.update(timeline_data)
        timeline = Timeline.objects.create(**cleaned_data)

        new_timelineitems = {key: self.request.POST[key] for key in self.request.POST if
                             '_new_' in key and not key.startswith('delete_')}
        new_timelineitems_list = [search(r'\d+$', key).group(0) for key in new_timelineitems if 'key_' in key]
        for new_id in new_timelineitems_list:
            timeline_info = self.filter_endswith(initial_dict=new_timelineitems, filter_by='_new_%s' % new_id)
            timeline_info['timeline'] = timeline
            timelineitem = TimelineItem()
            try:
                self.save_object(obj=timelineitem, **timeline_info)
            except Exception as error:
                return self.form_invalid(form, exception=error)

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        project_id = self.kwargs.get('project_id')
        context = super(TimelineCreateView, self).get_context_data(**kwargs)
        context['schema_fields'] = get_schema_fields(project_id)
        context['title_object'] = self.model._meta.model_name
        context['streams'] = list(
            Stream.objects.filter(project_id=project_id).values('name', 'display_name')
        )
        self.set_projects(context)
        return context

    def form_invalid(self, form, **kwargs):
        form.errors['exception'] = kwargs.get('exception')
        return super().form_invalid(form)

    @staticmethod
    def filter_contains(initial_dict, filter_by, is_contains=True):
        if is_contains:
            return {name: value for name, value in initial_dict.items() if name.__contains__(filter_by)}
        return {name: value for name, value in initial_dict.items() if not name.__contains__(filter_by)}

    @staticmethod
    def filter_endswith(initial_dict, filter_by):
        return {name.replace(filter_by, ''): value for name, value in initial_dict.items() if name.endswith(filter_by)}

    @staticmethod
    def save_object(obj, **kwargs):
        for key, value in kwargs.items():
            setattr(obj, key, value)
        obj.save()
