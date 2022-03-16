import requests

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.utils import get_database_data
from kpis.models import KPI
from kpis.utils import get_payload_interval, get_payload_interval_period
from projects.mixins import set_projects
from pydruid.db import connect


druid_host, druid_port = get_database_data()


@login_required
def kpi_current(request, project_id):
    conn = connect(host=druid_host, port=druid_port, path='/druid/v2/sql/', scheme='http')
    curs = conn.cursor()

    intervals = {
        "last_minute_counter": [get_payload_interval(1)],
        "last_ten_minutes_counter": [get_payload_interval(10)],
        "last_thirty_minutes_counter": [get_payload_interval(30)],
        "last_hour_counter": [get_payload_interval(60)],
        # "last_twelve_hours_counter": [get_payload_interval(60 * 12)],
        "last_day_counter": [get_payload_interval(60 * 24)],
        "last_week_counter": [get_payload_interval(60 * 24 * 7)],
        "last_thirty_days_counter": [get_payload_interval(60 * 24 * 30)],
        "last_year_counter": [get_payload_interval(60 * 34 * 365)],

        "last_minute": [get_payload_interval_period(0, 1)],
        "last_ten_minutes": [get_payload_interval_period(1, 10)],
        "last_thirty_minutes": [get_payload_interval_period(10, 30)],
        "last_hour": [get_payload_interval_period(30, 60)],
        # "last_twelve_hours": [get_payload_interval_period(60, 60 * 12)],
        "last_day": [get_payload_interval_period(60, 60 * 24)],
        "last_week": [get_payload_interval_period(60*24, 60 * 24 * 7)],
        "last_thirty_days": [get_payload_interval_period(60*24*7, 60 * 24 * 30)],
        "last_year": [get_payload_interval_period(60*24*30, 60 * 34 * 365)],
        "all_time": ["1970-01-01T00:00:00.000/2030-01-03T00:00:00.000"]
    }

    counters = []
    measurements = []

    for interval in intervals:
        print(f"Generating KPIs for interval [{interval}]")
        # Group All KPIs
        payload_counters = {
            "queryType": "groupBy",
            "dataSource": "DATA_kpis",
            "granularity": "day",
            "dimensions": ["category_name", "metric", "slice_field", "slice_value"],
            "aggregations": [
                {"type": "floatSum", "name": "sum_kpi_value", "fieldName": "kpi_value"},
                {"type": "floatLast", "name": "last_kpi_value", "fieldName": "kpi_value"},
                {"type": "floatMax", "name": "max_kpi_value",  "fieldName": "kpi_value"},
                {"type": "floatMin", "name": "min_kpi_value", "fieldName": "kpi_value"},
            ],
            "intervals": intervals[interval],
            'filter': {
                "type": "selector",
                "dimension": "project_id",
                "value": project_id,
            },
        }

        print(f"Druid query payload is [{payload_counters}]")

        url = f'http://{druid_host}:{druid_port}/druid/v2/?pretty'
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload_counters)

        if response.status_code == 200:
            data = response.json()
            for row in data:
                event = row["event"]
                is_new_row = True
                new_row = dict()

                # See if we already have the row in the array and update in place with the additional interval data
                for r in [*counters, *measurements]:
                    if r["category_name"] == event.get("category_name") and r["metric"] == event.get("metric") and \
                       r['slice_field'] == event.get('slice_field') and r['slice_value'] == event.get('slice_value'):
                        new_row = r
                        is_new_row = False

                new_row.update({
                    "category_name": event.get("category_name"),
                    "metric": event.get("metric"),
                    "slice_field": event.get("slice_field"),
                    "slice_value": event.get("slice_value"),
                    f"kpi_value": event.get("sum_kpi_value"),
                    f"last_kpi_value": event.get("last_kpi_value"),
                    f"max_kpi_value_{interval}": event.get("max_kpi_value"),
                    f"min_kpi_value_{interval}": event.get("min_kpi_value"),
                    f"kpi_value_{interval}": event.get("sum_kpi_value"),
                    f"last_kpi_value_{interval}": event.get("last_kpi_value")
                })

                if is_new_row:
                    try:
                        kpi = KPI.objects.get(category=event.get("category_name"), metric=event.get("metric"))
                        new_row['kpi_id'] = kpi.id
                        if kpi.indicator_type == KPI.TYPE_COUNTER:
                            counters.append(new_row)
                        else:
                            measurements.append(new_row)
                    except KPI.DoesNotExist:
                        pass

    context = {
        'counters': counters,
        'measurements': measurements,
        'kpi_over_time_window_rows': [],
        'kpi_over_time_cumulative_rows': [],
        'project_id': project_id
    }

    set_projects(context, request=request)
    return render(request, 'kpis/current.html', context)
