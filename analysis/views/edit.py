from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from analysis.forms import ReportForm
from analysis.models import Report, ReportItem
from kpis.models import KPI
from projects.mixins import ProjectsListMixin
from searches.models import Search
from streams.models import Stream
from schemas.models import Schema, SchemaField


class ReportEditView(LoginRequiredMixin, generic.UpdateView, ProjectsListMixin):
    template_name = 'analysis/edit.html'
    model = Report
    form_class = ReportForm
    pk_url_kwarg = 'report_id'
    context_object_name = 'report'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.project_id != kwargs.get('project_id'):
            return HttpResponseRedirect(self.get_success_url())
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('projects:analysis:reports', kwargs={'project_id': self.kwargs.get('project_id')})

    default_fields = (
        'expression',
        'filter_field',
        'filter_value',
        'limit',
        'x_value',
        'y_value',
    )

    def get_context_data(self, **kwargs):
        context = super(ReportEditView, self).get_context_data(**kwargs)

        project_id = self.kwargs.get('project_id')
        schema_fields = {}
        streams = Stream.objects.filter(project_id=project_id)
        for stream in streams:
            fields = SchemaField.objects.filter(schema=stream.schema)
            schema_fields[stream.name] = list(fields.values('name'))

        context['schema_fields'] = schema_fields
        context['report_name'] = self.object.name
        context['report_items'] = self.object.reportitem_set.order_by('ordering')
        context['report_types'] = ReportItem.REPORT_ITEM_TYPES
        context['time_window_choices'] = ReportItem.TIME_WINDOW_CHOICES
        context['filter_type_choices'] = ReportItem.FILTER_TYPES
        context['plot_type_choices'] = ReportItem.PLOT_TYPES
        context['report_types_data'] = ReportItem.REPORT_ITEM_TYPES_DATA
        context['record_types'] = list(streams.values('name', 'display_name'))
        context['saved_searches'] = list(Search.objects.filter(project_id=project_id).values_list('name', flat=True))
        context['kpi_categories'] = list(KPI.objects.filter(project_id=project_id).values_list('category', flat=True).
                                         distinct().order_by())

        metric_values = list(
            KPI.objects.filter(project_id=project_id).values_list('category', 'id', 'metric'))
        category_metrics = dict()
        for entry in metric_values:
            if entry[0] not in category_metrics:
                category_metrics[entry[0]] = []
            category_metrics[entry[0]].append({'id': str(entry[1]), 'name': entry[2]})

        context['kpi_metrics'] = category_metrics

        self.set_projects(context)
        return context

    def form_valid(self, form):
        report = self.object
        cleaned_data = form.cleaned_data

        try:
            self.save_object(obj=report, **cleaned_data)
        except Exception as error:
            return self.form_invalid(form, exception=error)

        report_items = report.reportitem_set.all()
        initial_count_report_items = report_items.count()
        ordering_data = self.filter_contains(initial_dict=self.request.POST, filter_by='ordering')
        report_items_data = self.filter_contains(initial_dict=self.request.POST, filter_by='_')
        delete_report_items = self.filter_contains(initial_dict=ordering_data, filter_by='delete')
        delete_report_items = list(map(lambda key: int(key.rsplit('_', 1)[1]), delete_report_items.keys()))
        ordering_data = self.filter_contains(initial_dict=ordering_data, filter_by='delete', is_contains=False)
        new_report_items = self.filter_contains(initial_dict=report_items_data, filter_by='_new_')
        old_report_items = {name: value for name, value in report_items_data.items() if name not in new_report_items}
        new_count_report_items = len(ordering_data.values())

        if new_count_report_items < initial_count_report_items and not delete_report_items:
            error = 'Error. Please try again'
            return self.form_invalid(form, exception=error)

        for report_item in report_items:
            report_item_id = report_item.id

            if report_item_id in delete_report_items:
                report_item.delete()
                continue

            report_item_info = self.filter_endswith(initial_dict=old_report_items, filter_by='_%s' % report_item_id)
            try:
                self.set_default_values(obj=report_item)
                self.save_object(obj=report_item, **report_item_info)
            except Exception as error:
                return self.form_invalid(form, exception=error)

        for new_id in range(new_count_report_items - initial_count_report_items):
            report_item_info = self.filter_endswith(initial_dict=new_report_items, filter_by='_new_%s' % new_id)
            limit = report_item_info.get('limit')
            if not limit and limit is not None:
                report_item_info.pop('limit')
            report_item_info['report'] = report
            report_item = ReportItem()

            try:
                self.save_object(obj=report_item, **report_item_info)
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
            if key == 'limit' and not value:
                value = 0
            setattr(obj, key, value)
        obj.save()

    def set_default_values(self, obj):
        for field in self.default_fields:
            setattr(obj, field, 0 if field == 'limit' else None)
        obj.save()

    def form_invalid(self, form, **kwargs):
        form.errors['exception'] = kwargs.get('exception')
        return super().form_invalid(form)