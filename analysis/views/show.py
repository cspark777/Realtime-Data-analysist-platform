import copy

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from pydruid.db import connect

from analysis.models import Report, ReportItem
from core.utils import get_database_data
from projects.mixins import set_projects
from searches.models import Search
from streamprocessors.views import execute_druid_query, render_not_found
from streams.models import Stream
from .utils import filter_value_to_sql, time_window_to_sql

druid_host, druid_port = get_database_data()


@login_required
def show_report(request, project_id, report_id):
    report = Report.objects.filter(pk=report_id, project_id=project_id)
    if not report.exists():
        return HttpResponseRedirect(reverse_lazy('projects:analysis:reports', kwargs={'project_id': project_id}))
    report = report.first()

    conn = connect(host=druid_host, port=druid_port, path='/druid/v2/sql/', scheme='http')
    curs = conn.cursor()

    report_items = report.reportitem_set.all().order_by('ordering')

    source_data = {}
    searches = {}
    schema_fields = {}
    broken_reports = []

    for report_item in report_items:
        if report_item.type == ReportItem.METRICS:
            continue
        if report_item.type == ReportItem.DATA_TABLE and report_item.record_type:
            try:
                stream = Stream.objects.get(name=report_item.record_type, project_id=project_id)
                schema_fields[report_item.id] = stream.schema.list_fields()
            except Stream.DoesNotExist:
                pass

        if report_item.type == ReportItem.SAVED_SEARCH:
            search = Search.objects.filter(name=report_item.search_name).first()
            stream = Stream.objects.filter(name=search.stream).first()
            searches[report_item.id] = search
            schema_fields[report_item.id] = stream.schema.list_fields()
            continue

        if not report_item.record_type or report_item.type == ReportItem.EXTERNAL_SOURCE:
            continue

        table = f'"{report_item.record_type}"'
        # Time window
        time_window = (" WHERE __time > " + time_window_to_sql(report_item.time_window))\
            if (report_item.time_window and report_item.time_window != ReportItem.ALL_TIME) else ''
        # Filter
        if report_item.filter_type != ReportItem.FILTER_NONE and report_item.filter_field and report_item.filter_value:
            filter_part = report_item.filter_field + filter_value_to_sql(report_item.filter_type) + f"'{report_item.filter_value}'"
            filter_query = ((' AND ' if time_window else ' WHERE ') + filter_part)
        else:
            filter_query = ''
        # Result query
        if report_item.type == ReportItem.HISTOGRAM:
            query = "SELECT " + report_item.x_value + " AS key, count(*) as CNT from " + table + \
                    time_window + filter_query + " GROUP BY " + report_item.x_value + " ORDER BY 1"
        elif report_item.type == ReportItem.SUMMARY and report_item.x_value:
            query = 'SELECT COUNT(CAST("' + report_item.x_value + '" AS FLOAT)) as total, MIN(CAST("' + report_item.x_value + '" AS FLOAT)) as min_val, ' +\
                    'MAX(CAST("' + report_item.x_value + '" AS FLOAT)) as max_val, ' + 'AVG(CAST("' + report_item.x_value + '" AS FLOAT)) as avg_val' + \
                    ' FROM ' + table + time_window + filter_query
        elif report_item.type == ReportItem.SERIES_CHART and report_item.plot_type != ReportItem.PLOT_VALUE_FROM_EVENT:
            # Build Events Over Time Data
            precision = 'minute'
            query = "select DATE_TRUNC('" + precision + "', __time) as tm, count(*) as CNT from " + table + \
                    time_window + " group by DATE_TRUNC('" + precision + "', __time) ORDER BY tm ASC"

        else:
            query = 'SELECT DISTINCT * FROM ' + table + time_window + filter_query + ' ORDER BY __time ASC'
        try:
            source_data_keys, source_data_rows = execute_druid_query(query, curs)
            if report_item.type == ReportItem.DATA_TABLE:
                source_data[report_item.id] = list(source_data_keys)
            elif report_item.type == ReportItem.SERIES_CHART and report_item.plot_type == ReportItem.PLOT_EVENTS_OVER_TIME_CUMULATIVE:
                events_accumulated = copy.deepcopy(source_data_rows)
                for i in range(1, len(events_accumulated)):
                    events_accumulated[i]['CNT'] += events_accumulated[i - 1]['CNT']
                source_data[report_item.id] = events_accumulated
            else:
                source_data[report_item.id] = source_data_rows
        except:
            broken_reports.append(report_item)

    summary = report_items.filter(type=ReportItem.SUMMARY).first()
    summary_url = ''
    if summary and summary.record_type:
        streams = Stream.objects.filter(name=summary.record_type)
        if streams.exists():
            stream_id = streams.first().id
            summary_url = reverse_lazy('projects:streamprocessors:source_events_summary',
                                       kwargs={'project_id': project_id,
                                               'object_id': stream_id}) + f'?fields={summary.expression}'

    context = {
        'source_data': source_data,
        'report': report,
        'analysis_url': reverse_lazy('projects:streamprocessors:source_events',
                                     kwargs={'project_id': project_id, 'object_id': report_id}),
        'summary_url': summary_url,
        'report_items': report_items,
        'searches': searches,
        'broken_reports': broken_reports,
        'schema_fields': schema_fields
    }

    set_projects(context, request=request)

    return render(request, 'analysis/show.html', context)