from dateutil.parser import *
from django.views import View
from django.views.generic.base import ContextMixin
from django.shortcuts import render

from core.utils import run_druid_query
from projects.mixins import set_projects
from timelines.models import Timeline
from timelines.utils import template_replace
from .base import TimelineBaseView


class TimelineShowView(TimelineBaseView, View, ContextMixin):
    model = Timeline
    template_name = 'timelines/show.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        timeline_obj = self.model.objects.get(created_by=self.request.user, pk=self.kwargs.get('pk'))
        unique_key_value = set(list(timeline_obj.timelineitem_set.all().values_list("key", flat=True).distinct()))
        unique_key_value_list = list()
        for each in unique_key_value:
            row = dict()
            row['id'] = each
            row['value'] = ''
            unique_key_value_list.append(row)
        context["unique_key_value"] = unique_key_value_list
        context["timeline_obj"] = timeline_obj
        set_projects(context, request=request)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        timeline_obj = self.model.objects.get(created_by=self.request.user, pk=self.kwargs.get('pk'))
        unique_key_value = set(list(timeline_obj.timelineitem_set.all().values_list("key", flat=True).distinct()))
        key_value_dict = dict()
        for each in unique_key_value:
            key_value_dict[each] = request.POST.get("{}_field".format(each))
        show_data = list()
        for item in timeline_obj.timelineitem_set.all():
            query = "select * from {} where {} = {}".format(f'"{item.stream}"', item.key, key_value_dict[item.key])
            try:
                results = run_druid_query(query)
            except Exception as e:
                print("E", e)
                results = list()
            for each in results:
                row = dict()
                title = template_replace(item.title_field, each)
                description = template_replace(item.description_field, each)
                row['title'] = title
                row['desc'] = description
                row["date_time"] = parse(getattr(each, '_0'))
                show_data.append(row)
        sorted_data = sorted(show_data, key=lambda x: x['date_time'], reverse=True)
        context = dict()
        set_projects(context, request=request)
        context["show_data"] = sorted_data
        context["timeline_obj"] = timeline_obj
        filled_values = list()
        for each in unique_key_value:
            row = dict()
            row['id'] = each
            row['value'] = key_value_dict[each]
            filled_values.append(row)
        context["unique_key_value"] = filled_values
        return render(request, self.template_name, context)
