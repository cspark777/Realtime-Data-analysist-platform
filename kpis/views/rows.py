import json
import requests

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from kpis.models import KPI
from core.utils import get_database_data
from kpis.utils import interval_to_payload
from streams.utils import parse_simple_time_interval
from .base import KPIBaseView


druid_host, druid_port = get_database_data()


@login_required
def get_kpis_rows(request, **kwargs):
    interval = request.GET.get('interval_field', "1 hour")
    slice_field = request.GET.get('slice_field')
    slice_value = request.GET.get('slice_value')
    interval_value, interval_type = parse_simple_time_interval(interval)
    interval_payload = interval_to_payload(interval_value, interval_type)

    kpi = KPI.objects.get(id=kwargs.get('KPI_id'))
    payload_filter = KPIBaseView.get_payload_filter(slice_field, slice_value, kpi.metric)

    payload = {
        'queryType': 'scan',
        'dataSource': 'DATA_kpis',
        'granularity': 'all',
        'intervals': [interval_payload],
        "filter": payload_filter,
        'limit': '1000',
        'order': 'descending'
    }
    response = requests.post(f'http://{druid_host}:{druid_port}/druid/v2/?pretty',
                             headers={'Content-Type': 'application/json'}, json=payload)
    rows = list()
    if response.status_code == 200:
        data = response.json()
        for i in range(len(data)):
            for item in data[i]['events']:
                rows.append(item)
    return HttpResponse(json.dumps({'data': rows}), content_type='application/json')
