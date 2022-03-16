from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import ProjectModelMixin
from streams.models import Stream


class Report(ProjectModelMixin):
    name = models.CharField(
        _('Name'),
        max_length=200,
    )

    description = models.TextField(
        _('Description'),
        blank=True,
        null=True,
    )

    dsl = models.TextField(
        _('Dsl'),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')
        ordering = ('id',)

    def __str__(self):
        return self.name


class ReportItem(models.Model):
    DATA_TABLE = 'data_table'
    SAVED_SEARCH = 'saved_search'
    BAR_CHART = 'bar_chart'
    HISTOGRAM = 'histogram'
    SCATTER_PLOT = 'scatter_plot'
    METRICS = 'metrics'
    SERIES_CHART = 'series_chart'
    SUMMARY = 'summary'
    EXTERNAL_SOURCE = 'external_source'
    REPORT_ITEM_TYPES = (
        (DATA_TABLE, 'Data Table'),
        (SAVED_SEARCH, 'Saved Search'),
        (BAR_CHART, 'Bar Chart'),
        (HISTOGRAM, 'Histogram'),
        (SERIES_CHART, 'Time Series Chart'),
        (SCATTER_PLOT, 'X/Y Scatter Plot'),
        (METRICS, 'Metrics'),
        (SUMMARY, 'Summary'),
        (EXTERNAL_SOURCE, 'External Source'),
    )

    FILTER_NONE = 'filter_none'
    FILTER_LESS_THAN = 'less_than'
    FILTER_GREATER_THAN = 'greater_than'
    FILTER_EQUAL = 'equal'
    FILTER_TYPES = (
        (FILTER_NONE, 'No Filter'),
        (FILTER_LESS_THAN, 'Less Than'),
        (FILTER_GREATER_THAN, 'Greater Than'),
        (FILTER_EQUAL, 'Equal'),
    )

    ALL_TIME = 'all_time'
    LAST_MINUTE = 'last_minute'
    LAST_10_MINUTES = 'last_10_minutes'
    LAST_HOUR = 'last_hour'
    LAST_DAY = 'last_day'
    LAST_WEEK = 'last_week'
    LAST_YEAR = 'last_year'
    TIME_WINDOW_CHOICES = (
        (ALL_TIME, 'All Time'),
        (LAST_MINUTE, 'Last Minute'),
        (LAST_10_MINUTES, 'Last 10 Minutes'),
        (LAST_HOUR, 'Last Hour'),
        (LAST_DAY, 'Last Day'),
        (LAST_WEEK, 'Last Week'),
        (LAST_YEAR, 'Last Year'),
    )

    PLOT_EVENTS_OVER_TIME = 'events_over_time'
    PLOT_EVENTS_OVER_TIME_CUMULATIVE = 'events_over_time_cumulative'
    PLOT_VALUE_FROM_EVENT = 'value_from_report'
    PLOT_TYPES = (
        (PLOT_EVENTS_OVER_TIME, 'Count Of Events Over Time'),
        (PLOT_EVENTS_OVER_TIME_CUMULATIVE, 'Count Of Events Over Time (Cumulative)'),
        (PLOT_VALUE_FROM_EVENT, 'A Value From The Event'),
    )

    REPORT_ITEM_TYPES_DATA = {
        DATA_TABLE: {
            'report_item_type_name': 'data_table',
            'fields': [
                {
                    'name': 'record_type',
                    'input_type': 'select',
                    'choices': []
                },
                {
                    'name': 'filter_field',
                    'placeholder': 'Filter Field',
                    'input_type': 'schema_field_select',
                    'choices': []
                },
                {
                    'name': 'filter_type',
                    'placeholder': 'Filter Type',
                    'input_type': 'select',
                    'choices': [list(x) for x in FILTER_TYPES]
                },
                {
                    'name': 'filter_value',
                    'placeholder': 'Filter Value',
                    'input_type': 'text',
                    'choices': []
                },
            ]
        },
        SAVED_SEARCH: {
            'report_item_type_name': 'saved_search',
            'fields': [
                {
                    'name': 'search_name',
                    'input_type': 'select',
                    'choices': []
                },
                # {
                #     'name': 'filter_field',
                #     'placeholder': 'Filter Field',
                #     'input_type': 'schema_field_select',
                #     'choices': []
                # },
                # {
                #     'name': 'filter_type',
                #     'placeholder': 'Filter Type',
                #     'input_type': 'select',
                #     'choices': [list(x) for x in FILTER_TYPES]
                # },
                # {
                #     'name': 'filter_value',
                #     'placeholder': 'Filter Value',
                #     'input_type': 'text',
                #     'choices': []
                # },
            ]
        },
        BAR_CHART: {
            'report_item_type_name': 'bar_chart',
            'fields': [
                {
                    'name': 'record_type',
                    'input_type': 'select',
                    'choices': []
                },
                {
                    'name': 'x_value',
                    'placeholder': 'Field To Plot',
                    'input_type': 'schema_field_select',
                    'choices': []
                },
                {
                    'name': 'filter_field',
                    'placeholder': 'Filter Field',
                    'input_type': 'schema_field_select',
                    'choices': []
                },
                {
                    'name': 'filter_type',
                    'placeholder': 'Filter Type',
                    'input_type': 'select',
                    'choices': [list(x) for x in FILTER_TYPES]
                },
                {
                    'name': 'filter_value',
                    'placeholder': 'Filter Value',
                    'input_type': 'text',
                    'choices': []
                },
                {
                    'name': 'time_window',
                    'placeholder': 'Time Window',
                    'input_type': 'select',
                    'choices': [list(x) for x in TIME_WINDOW_CHOICES]
                },
            ]
        },
        HISTOGRAM: {
            'report_item_type_name': 'histogram',
            'fields': [
                {
                    'name': 'record_type',
                    'input_type': 'select',
                    'choices': []
                },
                {
                    'name': 'x_value',
                    'placeholder': 'Field To Plot',
                    'input_type': 'schema_field_select',
                    'choices': []
                },
                {
                    'name': 'filter_field',
                    'placeholder': 'Filter Field',
                    'input_type': 'schema_field_select',
                    'choices': []
                },
                {
                    'name': 'filter_type',
                    'placeholder': 'Filter Type',
                    'input_type': 'select',
                    'choices': [list(x) for x in FILTER_TYPES]
                },
                {
                    'name': 'filter_value',
                    'placeholder': 'Filter Value',
                    'input_type': 'text',
                    'choices': []
                },
                {
                    'name': 'time_window',
                    'placeholder': 'Time Window',
                    'input_type': 'select',
                    'choices': [list(x) for x in TIME_WINDOW_CHOICES]
                },
            ]
        },
        SCATTER_PLOT: {
            'report_item_type_name': 'scatter_plot',
            'fields': [
                {
                    'name': 'record_type',
                    'input_type': 'select',
                    'choices': []
                },
                {
                    'name': 'x_value',
                    'placeholder': 'Field To Plot (X)',
                    'input_type': 'schema_field_select',
                    'choices': []
                },
                {
                    'name': 'y_value',
                    'placeholder': 'Field To Plot (Y)',
                    'input_type': 'schema_field_select',
                    'choices': []
                },
                {
                    'name': 'time_window',
                    'placeholder': 'Time Window',
                    'input_type': 'select',
                    'choices': [list(x) for x in TIME_WINDOW_CHOICES]
                },
            ],
        },
        METRICS: {
            'report_item_type_name': 'metrics',
            'fields': [
                {
                    'name': 'record_type',
                    'input_type': 'select',
                    'choices': []
                },
                {
                    'name': 'kpi_category',
                    'input_type': 'select',
                    'choices': []
                },
                {
                    'name': 'kpi_metric',
                    'input_type': 'select',
                    'choices': []
                },
                {
                    'name': 'time_window',
                    'input_type': 'text',
                    'choices': []
                },
                # {
                #     'name': 'filter_field',
                #     'placeholder': 'Filter Field',
                #     'input_type': 'schema_field_select',
                #     'choices': []
                # },
                # {
                #     'name': 'filter_type',
                #     'placeholder': 'Filter Type',
                #     'input_type': 'select',
                #     'choices': [list(x) for x in FILTER_TYPES]
                # },
                # {
                #     'name': 'filter_value',
                #     'placeholder': 'Filter Value',
                #     'input_type': 'text',
                #     'choices': []
                # },
            ]
        },
        SERIES_CHART: {
            'report_item_type_name': 'series_chart',
            'fields': [
                {
                    'name': 'record_type',
                    'input_type': 'select',
                    'choices': []
                },
                {
                    'name': 'plot_type',
                    'placeholder': 'Plot Type',
                    'input_type': 'select',
                    'choices': [list(x) for x in PLOT_TYPES]
                },
                {
                    'name': 'y_value',
                    'placeholder': 'Field To Plot',
                    'input_type': 'schema_field_select',
                    'choices': []
                },
                {
                    'name': 'filter_field',
                    'placeholder': 'Filter Field',
                    'input_type': 'schema_field_select',
                    'choices': []
                },
                {
                    'name': 'filter_type',
                    'placeholder': 'Filter Type',
                    'input_type': 'select',
                    'choices': [list(x) for x in FILTER_TYPES]
                },
                {
                    'name': 'filter_value',
                    'placeholder': 'Filter Value',
                    'input_type': 'text',
                    'choices': []
                },
                {
                    'name': 'time_window',
                    'placeholder': 'Time Window',
                    'input_type': 'select',
                    'choices': [list(x) for x in TIME_WINDOW_CHOICES]
                },
            ],
        },
        SUMMARY: {
            'report_item_type_name': 'summary',
            'fields': [
                {
                    'name': 'record_type',
                    'input_type': 'select',
                    'choices': []
                },
                {
                    'name': 'x_value',
                    'placeholder': 'Fields',
                    'input_type': 'schema_field_select',
                    'choices': []
                },
                {
                    'name': 'time_window',
                    'placeholder': 'Time Window',
                    'input_type': 'select',
                    'choices': [list(x) for x in TIME_WINDOW_CHOICES]
                },
            ]
        },
        EXTERNAL_SOURCE: {
            'report_item_type_name': 'external_source',
            'fields': [
                {
                    'name': 'external_url',
                    'placeholder': 'External url',
                    'input_type': 'text',
                    'choices': []
                },
            ]
        },
    }

    name = models.CharField(
        _('Name'),
        max_length=200,
    )

    description = models.TextField(
        _('Description'),
        blank=True,
        null=True,
    )

    type = models.TextField(
        _('Type'),
        blank=True,
        null=True,
        choices=REPORT_ITEM_TYPES,
    )

    ordering = models.IntegerField(
        _('Ordering records'),
        default=1,
    )

    record_type = models.TextField(
        _('Record Type'),
        blank=True,
        null=True,
    )

    filter_field = models.TextField(
        _('Filter Field'),
        blank=True,
        null=True,
    )

    filter_value = models.TextField(
        _('Filter Value'),
        blank=True,
        null=True,
    )

    limit = models.IntegerField(
        _('Limit'),
        default=0,
    )

    x_value = models.TextField(
        _('X Value'),
        blank=True,
        null=True,
    )

    y_value = models.TextField(
        _('Y Value'),
        blank=True,
        null=True,
    )

    expression = models.TextField(
        _('Expression'),
        blank=True,
        null=True,
    )

    report = models.ForeignKey(
        'analysis.Report',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    filter_type = models.CharField(
        _('Filter type'),
        max_length=20,
        null=True,
        blank=True,
        choices=FILTER_TYPES,
        default=FILTER_NONE
    )

    time_window = models.CharField(
        _('Time window'),
        max_length=20,
        null=True,
        blank=True,
        choices=TIME_WINDOW_CHOICES
    )

    plot_type = models.CharField(
        _('Plot type'),
        max_length=30,
        null=True,
        blank=True,
        choices=PLOT_TYPES
    )

    search_name = models.CharField(
        _('Search Name'),
        max_length=200,
        null=True,
        blank=True
    )

    kpi_category = models.CharField(
        _('Metric Category'),
        max_length=200,
        null=True,
        blank=True
    )

    kpi_metric = models.CharField(
        _('Metric Name'),
        max_length=200,
        null=True,
        blank=True
    )

    external_url = models.CharField(
        _('External Url'),
        max_length=200,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('ReportItem')
        verbose_name_plural = _('ReportItems')
        ordering = ('id',)

    def __str__(self):
        return self.name
