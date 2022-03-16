from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from analysis.models import Report, ReportItem
from analysis.forms import ReportForm
from kpis.models import KPI
from projects.mixins import ProjectsListMixin
from searches.models import Search
from streams.models import Stream
from schemas.models import SchemaField


class ReportCreateView(LoginRequiredMixin, generic.CreateView, ProjectsListMixin):
    template_name = 'analysis/new.html'
    model = Report
    form_class = ReportForm

    def get_success_url(self):
        return reverse_lazy('projects:analysis:reports', kwargs={'project_id': self.kwargs.get('project_id')})

    def get_context_data(self, **kwargs):
        context = super(ReportCreateView, self).get_context_data(**kwargs)
        schema_fields = {}
        project_id = self.kwargs.get('project_id')
        streams = Stream.objects.filter(project_id=project_id)
        for stream in streams:
            fields = SchemaField.objects.filter(schema=stream.schema)
            schema_fields[stream.name] = list(fields.values('name'))

        context['schema_fields'] = schema_fields
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
        cleaned_data = form.cleaned_data
        kwargs_to_create = {
            'name': cleaned_data.get('name'),
            'description': cleaned_data.get('description'),
            'dsl': cleaned_data.get('dsl'),
            'project_id': self.kwargs.get('project_id'),
        }
        report = self.model.objects.create(**kwargs_to_create)

        # Report items
        ordering_data = self.filter_contains(initial_dict=self.request.POST, filter_by='ordering')
        report_items_data = self.filter_contains(initial_dict=self.request.POST, filter_by='_')
        ordering_data = self.filter_contains(initial_dict=ordering_data, filter_by='delete', is_contains=False)
        new_report_items = self.filter_contains(initial_dict=report_items_data, filter_by='_new_')
        new_count_report_items = len(ordering_data.values())

        for new_id in range(new_count_report_items):
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

    def form_invalid(self, form, **kwargs):
        form.errors['exception'] = kwargs.get('exception')
        return super().form_invalid(form)

    @staticmethod
    def save_object(obj, **kwargs):
        for key, value in kwargs.items():
            if key == 'limit' and not value:
                value = 0
            setattr(obj, key, value)
        obj.save()

    @staticmethod
    def filter_contains(initial_dict, filter_by, is_contains=True):
        if is_contains:
            return {name: value for name, value in initial_dict.items() if name.__contains__(filter_by)}
        return {name: value for name, value in initial_dict.items() if not name.__contains__(filter_by)}

    @staticmethod
    def filter_endswith(initial_dict, filter_by):
        return {name.replace(filter_by, ''): value for name, value in initial_dict.items() if name.endswith(filter_by)}
