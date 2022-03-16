import json
import requests

from django.conf import settings


ALLOWED_INTERVAL_TYPES = ('second', 'minute', 'hour', 'day', 'week', 'year')


def parse_simple_time_interval(interval):
    interval_splitted = interval.split()
    if len(interval_splitted) != 2:
        return 'error', 'Too many interval words (2 expected)'
    interval_value, interval_type = interval_splitted
    try:
        interval_value = int(interval_value)
        if interval_value < 1:
            return 'error', 'Interval value must be at least 1'
    except ValueError:
        return 'error', 'Wrong number format'

    interval_type = interval_type.lower().rstrip('s')

    if interval_type not in ALLOWED_INTERVAL_TYPES:
        return 'error', 'Illegal interval type. Use: ' + '(s), '.join(ALLOWED_INTERVAL_TYPES) + '(s)'

    return interval_value, interval_type


def DATA_server_stream_create(stream, project_id):
    server_url = settings.DATA_SERVER + 'druid_kafka_connector'
    print("Connecting to " + server_url)
    data = json.dumps({
        'stream_name': stream.name,
        'project_id': project_id,
        'broker_url': settings.KAFKA_URL,
        'database_url': settings.DRUID_URL,
        'is_countable': stream.is_countable,
        'dimensions': stream.schema.to_druid_dimensions(),
    })
    print(data)
    requests.post(server_url, data=data)
    return None
