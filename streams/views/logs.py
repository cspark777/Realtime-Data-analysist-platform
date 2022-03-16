import copy

from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from pydruid.db import connect

from analysis.models import ReportItem
from core.utils import get_database_data
from projects.mixins import set_projects
from streamprocessors.models import StreamProcessor
from streamprocessors.views import execute_druid_query, render_not_found


druid_host, druid_port = get_database_data()


@login_required
def stream_logs(request, project_id):
    query = 'SELECT DISTINCT * FROM '
    stream_name = 'DATA_logs'
    query += stream_name + " WHERE project_id = " + str(project_id)
    if hasattr(get_user_model(), 'role') and request.user.role == get_user_model().USER:
        query += ' AND message_type != code_exception'

    query += " ORDER BY __time DESC"
    conn = connect(host=druid_host, port=druid_port, path='/druid/v2/sql/', scheme='http')
    curs = conn.cursor()
    try:
        source_data_keys, source_data_rows = execute_druid_query(query, curs)
        source_data_rows_count = len(source_data_rows)
    except:
        return render_not_found(request, stream_name)

    source_data_keys = list(source_data_keys)
    if 'project_id' in source_data_keys:
        source_data_keys.remove('project_id')

    for obj in source_data_rows:
        if '_0' in obj.keys():
            obj['_0'] = datetime.strptime(obj['_0'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%m-%d-%Y %H:%M')
        if 'streamprocessor_id' in obj.keys() and obj['streamprocessor_id'].isdigit():
            try:
                streamprocess = StreamProcessor.objects.get(id=obj['streamprocessor_id'])
                obj['streamprocessor_id'] = streamprocess.name
            except:
                pass

    source_data_keys_group = [item for item in source_data_keys if item not in ('_0', 'count', 'uuid')]
    interval = request.POST.get('interval_field', "hour")

    # Build Events Over Time Data
    query = "select DATE_TRUNC('" + interval + "', __time) as tm, count(*) as CNT from " + stream_name + \
            " group by DATE_TRUNC('" + interval + "', __time)"
    try:
        events_over_time_window_keys, events_over_time_window_rows = execute_druid_query(query, curs)
    except:
        return render_not_found(request, stream_name)

    events_accumulated = copy.deepcopy(events_over_time_window_rows)
    for i in range(1, len(events_accumulated)):
        events_accumulated[i]['CNT'] += events_accumulated[i - 1]['CNT']

    group_by_field = request.POST.get('group_by_field',
                                      source_data_keys_group[0] if len(source_data_keys_group) else '')
    events_grouped_by_keys = {}
    events_grouped_by_rows = {}
    if group_by_field != "":
        query = "select " + group_by_field + " as key, count(*) as CNT from " + stream_name + " group by " + group_by_field + " order by 2 desc LIMIT 10"
        try:
            events_grouped_by_keys, events_grouped_by_rows = execute_druid_query(query, curs)
        except:
            return render_not_found(request, stream_name)

    report_items = ReportItem.objects.filter(record_type=stream_name)
    summary_report = report_items.filter(type=ReportItem.SUMMARY).first()
    data_table = report_items.filter(type=ReportItem.DATA_TABLE).first()

    context = {
        'source_data_keys': source_data_keys_group,
        'source_data_rows': source_data_rows,
        'source_data_rows_count': source_data_rows_count,
        'source_data_keys_monitor': list(source_data_keys),
        'events_over_time_window_rows': events_over_time_window_rows,
        'events_over_time_window_keys': events_over_time_window_keys,
        'events_over_time_cumulative_rows': events_accumulated,
        'events_grouped_by_keys': events_grouped_by_keys,
        'events_grouped_by_rows': events_grouped_by_rows,
        'group_by_field': group_by_field,
        'selected_interval': interval,
        'interval_values': ['minute', 'hour', 'day'],
        'stream_name': stream_name,
        'stream_id': 'logs',
        'analysis_url': reverse_lazy('projects:streamprocessors:source_events',
                                     kwargs={'project_id': project_id, 'object_id': 'logs'}),
        'summary_report': summary_report,
        'data_table': data_table,
    }
    set_projects(context, request=request)

    return render(request, 'streams/logs.html', context)






