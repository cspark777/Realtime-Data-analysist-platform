from datetime import datetime
from dateutil.relativedelta import relativedelta

from kpis.models import KPI
from streams.utils import parse_simple_time_interval


def get_kpi_report_payload(kpi, interval):
    interval_value, interval_type = parse_simple_time_interval(interval)
    interval_payload = interval_to_payload(interval_value, interval_type)

    filters = {
        'type': 'and',
        'fields': [
            {
                "type": "selector",
                "dimension": "category_name",
                "value": kpi.category
            },
            {
                "type": "selector",
                "dimension": "metric",
                "value": kpi.metric
            },
        ]
    }

    if kpi.indicator_type == KPI.TYPE_MEASUREMENT:
        return {
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

    else:
        return {
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


def get_payload_interval(minutes):
    current_datetime = datetime.now()
    before_datetime = current_datetime - relativedelta(minutes=minutes)
    current_iso = current_datetime.isoformat()
    before_iso = before_datetime.isoformat()
    return f'{before_iso}/{current_iso}'


def get_payload_interval_period(minutes_to, minutes_from):
    current_datetime = datetime.now()
    datetime_from = current_datetime - relativedelta(minutes=minutes_from)
    datetime_to = current_datetime - relativedelta(minutes=minutes_to)
    from_iso = datetime_from.isoformat()
    to_iso = datetime_to.isoformat()
    return f'{from_iso}/{to_iso}'


def interval_to_payload(interval_value, interval_type):
    args = {interval_type+'s': interval_value}
    current_datetime = datetime.now()
    before_datetime = current_datetime - relativedelta(**args)
    current_iso = current_datetime.isoformat()
    before_iso = before_datetime.isoformat()
    return f'{before_iso}/{current_iso}'
