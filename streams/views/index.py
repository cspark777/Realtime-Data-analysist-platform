import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.utils import get_database_data
from projects.mixins import set_projects
from streamprocessors.druid_utils import get_payload_interval
from streams.models import Stream


@login_required
def stream_index(request, project_id):
    stream_list = Stream.objects.filter(project_id=project_id).order_by('id')
    druid_host, druid_port = get_database_data()

    event_counts = []

    for stream in stream_list:
        # query = SELECT COUNT(*) as cnt FROM {stream.name}
        payload = {
            "queryType": "timeseries",
            "dataSource": {"type": "table", "name": stream.name},
            "intervals": [get_payload_interval(default=True)],
            "granularity": {"type": "all"},
            "aggregations": [{"type": "count", "name": "cnt"}],
            "postAggregations": [],
        }
        response = requests.post(f'http://{druid_host}:{druid_port}/druid/v2/?pretty',
                                 headers={'Content-Type': 'application/json'}, json=payload)

        if response.status_code == 200:
            try:
                data = response.json()
                cnt = data[0]['result']['cnt']
                event_counts.append(cnt)
            except:
                event_counts.append(0)
        else:
            event_counts.append(0)

    context = {'stream_list': stream_list, 'event_counts': event_counts}
    set_projects(context, request=request)
    return render(request, 'streams/index.html', context)
