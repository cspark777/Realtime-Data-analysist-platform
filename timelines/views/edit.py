import json

from re import search
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from core.utils import get_schema_fields
from timelines.forms import TimelineForm
from timelines.models import Timeline, TimelineItem
from streams.models import Stream
from .base import TimelineBaseView


class TimelineEditView(TimelineBaseView, UpdateView):
    template_name = 'timelines/edit.html'
    model = Timeline
    form_class = TimelineForm
    pk_url_kwarg = 'timeline_id'
    context_object_name = 'timeline'

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
            form.is_valid()
            contexts = dict()
            if any(map(lambda x: x.startswith('key_new_'), self.request.FILES)):
                for filename in filter(lambda x: x.startswith('key_new_'), self.request.FILES):
                    contexts[filename] = self.request.FILES.get(filename).file.read()
                    try:
                        events = json.loads(contexts[filename])
                    except (json.JSONDecodeError, ValueError):
                        form.add_error("steps", "Invalid JSON in file")
            if form.is_valid():
                return self.form_valid(form, contexts)
            return JsonResponse({"error": form.errors}, status=400)
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('projects:timelines:index',
                            kwargs={'project_id': self.kwargs.get('project_id')})

    def get_context_data(self, **kwargs):
        project_id = self.kwargs.get('project_id')
        context = super(TimelineEditView, self).get_context_data(**kwargs)
        context['schema_fields'] = get_schema_fields(project_id)
        context['timelineitems'] = self.object.timelineitem_set.order_by('ordering')
        context['streams'] = list(
            Stream.objects.filter(project_id=project_id).values('name', 'display_name')
        )
        self.set_projects(context)
        return context

    def form_valid(self, form, contexts):
        data = self.request.POST
        timeline = self.object
        cleaned_data = {
            'name': data.get('name'),
            'description': data.get('description') or "",
        }

        try:
            self.save_object(obj=timeline, **cleaned_data)
        except Exception as error:
            return self.form_invalid(form, exception=error)

        timelineitems = timeline.timelineitem_set.all()
        initial_count_timelineitems = timelineitems.count()
        ordering_data = self.filter_contains(initial_dict=data, filter_by='ordering')
        delete_timelineitems = self.filter_contains(initial_dict=ordering_data, filter_by='delete')
        delete_timelineitems = list(map(lambda key: int(key.rsplit('_', 1)[1]), delete_timelineitems.keys()))
        ordering_data = self.filter_contains(initial_dict=ordering_data, filter_by='delete', is_contains=False)
        timelineitems_data = self.filter_contains(initial_dict=data, filter_by='_')
        new_timelineitems = {key: self.request.POST[key] for key in self.request.POST if
                     '_new_' in key and not key.startswith('delete_')}
        old_timelineitems = {name: value for name, value in timelineitems_data.items() if name not in new_timelineitems}
        new_count_timelineitems = len(set(ordering_data.values()))
        new_timelineitems_list = [search(r'\d+$', key).group(0) for key in new_timelineitems if 'key_' in key]
        if new_count_timelineitems < initial_count_timelineitems and not delete_timelineitems:
            error = 'Duplicate key value violates unique constraint "timeline_timelineitems__ordering'
            return self.form_invalid(form, exception=error)
        for timelineitem in timelineitems:
            timeline_id = timelineitem.id
            if timeline_id in delete_timelineitems:
                timelineitem.delete()
                continue
            timeline_info = self.filter_endswith(initial_dict=old_timelineitems, filter_by='_%s' % timeline_id)

            try:
                self.save_object(obj=timelineitem, **timeline_info)
            except Exception as error:
                return self.form_invalid(form, exception=error)
        for new_id in new_timelineitems_list:
            timeline_info = self.filter_endswith(initial_dict=new_timelineitems, filter_by='_new_%s' % new_id)
            timeline_info['timeline'] = timeline
            if 'key' not in timeline_info:
                self.create_timelines_from_file(contexts['key_new_%s' % new_id], timeline_info)
            else:
                timelineitem = TimelineItem()
                try:
                    self.save_object(obj=timelineitem, **timeline_info)
                except Exception as error:
                    return self.form_invalid(form, exception=error)

        return HttpResponseRedirect(self.get_success_url())

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

    @transaction.atomic
    def create_timelines_from_file(self, context, timeline_info):
        events = json.loads(context)
        for ordering, event in enumerate(events, start=int(timeline_info.get('ordering', 1))):
            timelineitem = TimelineItem()
            timeline_info['event'] = json.dumps(event)
            timeline_info['ordering'] = ordering
            self.save_object(obj=timelineitem, **timeline_info)

    def form_invalid(self, form, **kwargs):
        form.errors['exception'] = kwargs.get('exception')
        return super().form_invalid(form)
