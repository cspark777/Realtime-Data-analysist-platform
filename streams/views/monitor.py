import copy

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from pydruid.db import connect

from analysis.models import ReportItem
from core.utils import get_database_data
from projects.mixins import set_projects
from streams.models import Stream
from streamprocessors.views import execute_druid_query, render_not_found
from streamprocessors.druid_utils import correct_schema_names
from streams.utils import parse_simple_time_interval


druid_host, druid_port = get_database_data()

@login_required
def stream_monitor(request, project_id, stream_id):
    query = 'SELECT DISTINCT * FROM '
    stream = Stream.objects.filter(pk=stream_id, project_id=project_id)
    if stream.exists():
        stream = stream.first()
        stream_name = stream.name
        display_stream_name = stream.display_name
        query += f"\"{stream_name}\""
    else:
        return HttpResponseRedirect(reverse_lazy('projects:streams:index', kwargs={'project_id': project_id}))

    context_no_events = {'stream_name': display_stream_name}
    set_projects(context_no_events, request=request)

    query += " ORDER BY __time DESC LIMIT 1000"
    conn = connect(host=druid_host, port=druid_port, path='/druid/v2/sql/', scheme='http')
    curs = conn.cursor()
    try:
        source_data_keys, source_data_rows = correct_schema_names(execute_druid_query(query, curs), stream.schema)
        source_data_rows_count = len(source_data_rows)
    except:
        return render(request, 'streams/monitor_streams.html', context_no_events)

    source_data_keys_group = [item for item in source_data_keys if item not in ('_0', 'count', 'uuid')]
    interval = request.GET.get('interval_field', '')
    interval_message = 'Example: 2 years, 1 hour, 99 seconds'
    precision = "minute"
    time_window = ''
    if interval:
        interval_value, interval_type = parse_simple_time_interval(interval)
        if interval_value == 'error':
            interval_message = interval_type
        else:
            time_window = f" WHERE __time > TIMESTAMPADD({interval_type}, -{interval_value}, CURRENT_TIMESTAMP)"

    # Build Events Over Time Data
    query = "select DATE_TRUNC('" + precision + "', __time) as tm, count(*) as CNT from \"" + stream_name + "\" " \
        + time_window + " group by DATE_TRUNC('" + precision + "', __time)"

    try:
        events_over_time_window_keys, events_over_time_window_rows = execute_druid_query(query, curs)
    except:
        print("EXCEPTION In Executing Query")
        return render(request, 'streams/monitor_streams.html', context_no_events)

    events_accumulated = copy.deepcopy(events_over_time_window_rows)
    for i in range(1, len(events_accumulated)):
        events_accumulated[i]['CNT'] += events_accumulated[i-1]['CNT']

    group_by_field = request.POST.get('group_by_field', source_data_keys_group[0] if len(source_data_keys_group) else '')
    events_grouped_by_keys = {}
    events_grouped_by_rows = {}
    if group_by_field != "":
        query = 'select "' + group_by_field + '" as key, count(*) as CNT from \"' + stream_name + '\"' + time_window + ' group by "' + group_by_field + '" order by 2 desc LIMIT 10'
        try:
            events_grouped_by_keys, events_grouped_by_rows = execute_druid_query(query, curs)
        except:
            return render(request, 'streams/monitor_streams.html', context_no_events)

    report_items = ReportItem.objects.filter(record_type=stream_name)
    summary_report = report_items.filter(type=ReportItem.SUMMARY).first()
    data_table = report_items.filter(type=ReportItem.DATA_TABLE).first()
    source_data_keys_monitor = [key for key in source_data_keys if key != 'uuid']

    context = {
        'source_data_keys': source_data_keys_group,
        'source_data_rows': source_data_rows,
        'source_data_rows_count': source_data_rows_count,
        'source_data_keys_monitor': source_data_keys_monitor,
        'events_over_time_window_rows': events_over_time_window_rows,
        'events_over_time_window_keys': events_over_time_window_keys,
        'events_over_time_cumulative_rows': events_accumulated,
        'events_grouped_by_keys': events_grouped_by_keys,
        'events_grouped_by_rows': events_grouped_by_rows,
        'group_by_field': group_by_field,
        'selected_interval': interval,
        'interval_message': interval_message,
        'interval_values': ['minute', 'hour', 'day'],
        'stream_name': display_stream_name,
        'stream_id': stream_id,
        'analysis_url': reverse_lazy('projects:streamprocessors:source_events',
                                     kwargs={'project_id': project_id, 'object_id': stream_id}) + f'?interval_field={interval}',
        'summary_report': summary_report,
        'data_table': data_table,
    }
    set_projects(context, request=request)

    return render(request, 'streams/monitor_streams.html', context)
