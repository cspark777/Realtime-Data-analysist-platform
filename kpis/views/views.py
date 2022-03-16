import requests
from django.http import JsonResponse

from core.utils import get_database_data
from kpis.models import KPI
from kpis.utils import get_kpi_report_payload

druid_host, druid_port = get_database_data()


def get_report_data(request, **kwargs):
    interval = request.GET.get('interval_field', "1 year")
    kpi_id = kwargs.get('KPI_id')
    kpi = KPI.objects.get(id=kpi_id)

    payload = get_kpi_report_payload(kpi, interval)
    response = requests.post(f'http://{druid_host}:{druid_port}/druid/v2/?pretty',
                             headers={'Content-Type': 'application/json'}, json=payload)
    rows = []
    if response.status_code == 200:
        data = response.json()
        if data:
            if kpi.indicator_type == KPI.TYPE_MEASUREMENT:
                for entry in data:
                    for item in entry['events']:
                        rows.append({'time': item['__time'], 'value': item['kpi_value']})
            else:
                for item in data:
                    rows.append({'time': item['timestamp'], 'value': item['event']['increment']})

    data = {
        'kpi_data_rows': rows,
        'kpi_data_rows_count': len(rows),
        'kpi_type': kpi.indicator_type
    }

    return JsonResponse(data=data)
