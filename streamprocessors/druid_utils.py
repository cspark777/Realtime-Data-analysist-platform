from datetime import datetime

import requests
from dateutil.relativedelta import relativedelta

from core.utils import get_database_data


def get_payload_interval(event_time=None, default=False):
    """ If time is not set, the output will be ± 10 years - 2010-02-28T06:34:11.512730/2030-02-28T06:34:11.512730.
        If uses default time interval - the output will be Druid default interval.
    """
    if default:
        return "-146136543-09-08T08:23:32.096Z/146140482-04-24T15:36:27.903Z"
    if event_time:
        event_time = str(event_time)
        if all(map(lambda i: i.isdigit(), event_time)):
            event_time = event_time[:10]
            current_datetime = datetime.fromtimestamp(int(event_time))
        else:
            current_datetime = datetime.fromisoformat(event_time)
        current_iso = (current_datetime + relativedelta(microseconds=1000)).isoformat()
    else:
        current_datetime = datetime.now()
        current_iso = (current_datetime + relativedelta(years=10)).isoformat()

    before_iso = (current_datetime - relativedelta(years=10)).isoformat()
    return f"{before_iso}/{current_iso}"


def suffix(day):
    return 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')


def execute_druid_query(query, curs):
    print("About to execute query: ", query)
    curs.execute(query)
    return rows_to_json(curs)


def rows_to_json(curs):
    json_objects = []
    keys = {}
    for row in curs:
        record = {}
        for field in row._fields:
            record[field] = getattr(row, field)
            keys = row._fields
        json_objects.append(record)
    #print('rows_to_json:', json_objects)
    return keys, json_objects


def correct_schema_names(data, schema):
    keys, rows = data
    keys = list(keys)
    schema_fields = sorted([*schema.list_fields(), '__time', 'uuid'])
    keys_to_replace = dict()
    new_rows = []

    for i in range(len(keys)):
        if keys[i][0] == '_' and keys[i][1:].isdigit():
            try:
                index = int(keys[i][1:])
                keys_to_replace[keys[i]] = schema_fields[index]
                keys[i] = schema_fields[index]
            except ValueError:
                pass

    for i in range(len(rows)):
        new_row = {}
        for key, value in rows[i].items():
            if key in keys_to_replace:
                new_row[keys_to_replace[key]] = value
            else:
                new_row[key] = value
        new_rows.append(new_row)

    if '__time' in keys:
        index = keys.index('__time')
        keys[0], keys[index] = keys[index], keys[0]

    return keys, new_rows


def get_exception_messages(_dimension: str, _id: int, _message_type: str):
    """ query = SELECT DISTINCT * FROM DATA_logs
               WHERE _dimension=_id
               AND message_type=_message_type
    """
    payload = {
        "queryType": "groupBy",
        "dataSource": {
            "type": "table",
            "name": "DATA_logs"
        },
        "intervals": {
            "type": "intervals",
            "intervals": [get_payload_interval(default=True)],
        },
        "filter": {
            "type": "and",
            "fields": [
                {
                    "type": "selector",
                    "dimension": _dimension,
                    "value": f"{_id}",
                },
                {
                    "type": "selector",
                    "dimension": "message_type",
                    "value": _message_type,
                }
            ]
        },
        "granularity": {
            "type": "all"
        },
        "dimensions": [
            {
                "type": "default",
                "dimension": "message",
                "outputName": "message",
                "outputType": "STRING"
            }
        ],
        "limitSpec": {
            "type": "NoopLimitSpec"
        },
        "descending": False
    }
    druid_host, druid_port = get_database_data()
    response = requests.post(f'http://{druid_host}:{druid_port}/druid/v2/?pretty',
                             headers={'Content-Type': 'application/json'}, json=payload)

    if response.status_code == 200:
        try:
            data = response.json()
            return list(map(lambda msg: msg.get('event').get('message'), data))
        except:
            return None
    else:
        return None
