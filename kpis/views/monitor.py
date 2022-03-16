import copy
import requests

from django.views.generic import TemplateView
from django.urls import reverse_lazy

from kpis.models import KPI
from core.utils import get_database_data
from kpis.utils import interval_to_payload
from streams.utils import parse_simple_time_interval
from .base import KPIBaseView


druid_host, druid_port = get_database_data()


class KPIMonitorCounterView(KPIBaseView, TemplateView):
    template_name = 'kpis/monitor_counter.html'

    def get_context_data(self, **kwargs):
        interval = self.request.GET.get('interval_field', "1 hour")
        slice_field = self.request.GET.get('slice_field')
        slice_value = self.request.GET.get('slice_value')
        interval_value, interval_type = parse_simple_time_interval(interval)
        interval_payload = interval_to_payload(interval_value, interval_type)

        kpi = KPI.objects.get(id=kwargs['KPI_id'])
        filters = self.get_payload_filter(slice_field, slice_value, kpi.metric)

        payload = {
            'queryType': 'scan',
            'dataSource': 'DATA_kpis',
            'granularity': 'all',
            'intervals': [interval_payload],
            'limit': '1000',
            'order': 'descending',
            'filter': filters
        }
        response = requests.post(f'http://{druid_host}:{druid_port}/druid/v2/?pretty',
                                 headers={'Content-Type': 'application/json'}, json=payload)
        rows = list()
        kpis_data_keys = list()
        source_data_rows_count = 0
        if response.status_code == 200:
            data = response.json()
            if data:  # build table only if we have data for selected interval
                for i in range(len(data)):
                    for item in data[i]['events']:
                        rows.append(item)
                kpis_data_keys = data[0]['columns']
                source_data_rows_count = len(rows)

        payload = {
            'queryType': 'groupBy',
            'dataSource': 'DATA_kpis',
            'granularity': 'minute',
            'intervals': [interval_payload],
            "filter": filters,
            "aggregations": [
                {
                    "type": "doubleSum",
                    "name": "increment",
                    "expression": "CAST(\"kpi_value\", 'DOUBLE')"
                }
            ],
            'limit': '750',
            'order': 'descending'
        }
        response = requests.post(f'http://{druid_host}:{druid_port}/druid/v2/?pretty',
                                 headers={'Content-Type': 'application/json'}, json=payload)
        kpi_over_time_window_rows = list()
        kpis_grouped_by_rows = list()
        kpis_accumulated = list()
        if response.status_code == 200:
            data = response.json()
            for item in data:
                obj = {"INC": item['event']['increment'], 'tm': item['timestamp']}
                kpi_over_time_window_rows.append(obj)
            kpis_accumulated = copy.deepcopy(kpi_over_time_window_rows)
            for i in range(1, len(kpis_accumulated)):
                kpis_accumulated[i]['INC'] += kpis_accumulated[i - 1]['INC']
        kpis_data_keys = [key for key in kpis_data_keys if key not in ('project_id', 'uuid', 'event')]
        slicing = f'&slice_field={slice_field}&slice_value={slice_value}' if (slice_field and slice_value) else ''
        analysis_url = reverse_lazy('projects:streamprocessors:kpis:get_kpis_rows',
            kwargs={'project_id': kwargs.get('project_id'), 'KPI_id': kwargs.get('KPI_id')}) + \
                    f'?interval_field={interval}{slicing}'
        slicing_enabled = slice_field and slice_value
        if not slicing_enabled:
            kpis_data_keys = [key for key in kpis_data_keys if key not in ('slice_field', 'slice_value')]
        context = {
            'kpi_data_rows': rows,
            'kpi_data_rows_count': source_data_rows_count,
            'kpi_data_keys_monitor': kpis_data_keys,
            'kpi_over_time_window_rows': kpi_over_time_window_rows,
            'kpis_grouped_by_rows': kpis_grouped_by_rows,
            'kpi_over_time_cumulative_rows': kpis_accumulated,
            'slice_field': slice_field,
            'slice_value': slice_value,
            'slicing_enabled': slicing_enabled,
            'selected_interval': interval,
            'interval_values': ['minute', 'hour', 'day'],
            'analysis_url': analysis_url,
            'project_id': kwargs.get('project_id'),
            'kpi': kpi
        }
        self.set_projects(context)
        return context


class KPIMonitorMeasurementView(KPIBaseView, TemplateView):
    template_name = 'kpis/monitor_measurement.html'

    def get_context_data(self, **kwargs):
        interval = self.request.GET.get('interval_field', "1 hour")
        slice_field = self.request.GET.get('slice_field')
        slice_value = self.request.GET.get('slice_value')
        interval_value, interval_type = parse_simple_time_interval(interval)
        interval_payload = interval_to_payload(interval_value, interval_type)

        kpi = KPI.objects.get(id=kwargs['KPI_id'])
        filters = self.get_payload_filter(slice_field, slice_value, kpi.metric)

        payload = {
            'queryType': 'scan',
            "dataSource": {
                "type": "table",
                "name": "DATA_kpis"
            },
            'granularity': 'all',
            'intervals': [interval_payload],
            'limit': '1000',
            'order': 'descending',
            'filter': filters
        }

        response = requests.post(f'http://{druid_host}:{druid_port}/druid/v2/?pretty',
                                 headers={'Content-Type': 'application/json'}, json=payload)
        rows = list()
        source_data_rows_count = 0
        if response.status_code == 200:
            data = response.json()
            if data:
                for i in range(len(data)):
                    for item in data[i]['events']:
                        rows.append({'TM': item['__time'], 'VAL': item['kpi_value']})
                source_data_rows_count = len(rows)

        kpis_data_keys = ['__time', 'category_name', 'metric', 'kpi_value']
        slicing = f'&slice_field={slice_field}&slice_value={slice_value}' if (slice_field and slice_value) else ''
        analysis_url = reverse_lazy('projects:streamprocessors:kpis:get_kpis_rows',
                           kwargs={'project_id': kwargs.get('project_id'), 'KPI_id': kwargs.get('KPI_id')}) + \
                                   f'?interval_field={interval}{slicing}'
        slicing_enabled = slice_field and slice_value
        if not slicing_enabled:
            kpis_data_keys = [key for key in kpis_data_keys if key not in ('slice_field', 'slice_value')]
        context = {
            'kpi_data_rows': rows,
            'kpi_data_rows_count': source_data_rows_count,
            'kpi_data_keys_monitor': kpis_data_keys,
            'slice_field': slice_field,
            'slice_value': slice_value,
            'slicing_enabled': slicing_enabled,
            'selected_interval': interval,
            'analysis_url': analysis_url,
            'project_id': kwargs.get('project_id'),
            'kpi': kpi
        }
        self.set_projects(context)
        return context
