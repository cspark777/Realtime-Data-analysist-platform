import json
import re

from django.conf import settings
from pydruid.db import connect
from avro_validator.schema import Schema as AvroSchema

from streams.models import Stream
from schemas.models import SchemaField, Schema
from streamprocessors.models import StreamProcessorStep


data_prefix = 'data_{extra}'.format


def get_database_data():
    druid_url = settings.DRUID_URL or ':'
    return druid_url.split(':')


def run_druid_query(query):
    """
    Method used to connect to Druid and execute Query
    """
    kafka_url = settings.KAFKA_URL
    druid_host, druid_port = get_database_data()
    conn = connect(host=druid_host, port=druid_port, path='/druid/v2/sql/', scheme='http')
    curs = conn.cursor()
    return curs.execute(query)


def generate_avro(topic, operator=None):
    avro = None
    try:
        schema = Stream.objects.get(name=topic).schema
        if schema:
            avro = []
            for entry in schema.schemafield_set.values('name', 'type_field', 'required'):
                data = {
                    'name': entry['name'],
                    'type': ['null', entry['type_field']] if not entry['required'] else entry['type_field'],
                }

                if entry['type_field'] == SchemaField.DATE:
                    data['type'] = {'type': ['null', 'string'] if not entry['required'] else 'string',
                                    'logicalType': 'timestamp-micros'}

                if not entry['required']:
                    data['default'] = None
                avro.append(data)

            set_additional_value(avro, operator)
            for field in avro:
                normalized_data_field(field)
            avro = {
                'namespace': f'{topic}.avro',
                'type': 'record',
                'name': f'{topic}_{"_".join(schema.name.split())}',
                'fields': avro,
            }
            print(avro)
    except:
        pass
    return avro

def generate_schema_avro(schema):
    avro = None
    topic= schema.name
    if schema:
        avro = []
        for entry in schema.schemafield_set.values('name', 'type_field', 'required'):
            data = {
                'name': entry['name'],
                'type': entry['type_field'],
            }
            avro.append(data)
        avro = {
            'namespace': f'{topic}.avro',
            'type': 'record',
            'name': f'{topic}_{"_".join(schema.name.split())}',
            'fields': avro,
        }
    return avro


def set_additional_value(avro, operator):
    if not get_field_exists(avro, operator) and operator:
        avro.append({'name': DATA_prefix(extra=operator), 'type': 'float'})


def get_field_exists(avro, operator):
    try:
        exists_field = next(filter(lambda f: f.get('name') in (operator, data_prefix(extra=operator)), avro))
    except StopIteration:
        exists_field = None

    if exists_field:
        normalized_data_field(exists_field)
    return exists_field


def normalized_data_field(exists_field):
    additional_fields = map(lambda func: (func[0], data_prefix(extra=func[0])), StreamProcessorStep.FUNCTIONS)
    additional_fields = [item for sublist in additional_fields for item in sublist]

    name = exists_field.get('name', '')

    if not name.startswith(data_prefix(extra='')) and name in additional_fields:
        exists_field['name'] = data_prefix(extra=name)


def validate_message_avro(message, avro):
    avro = json.dumps(avro)
    message = json.loads(message)
    schema = AvroSchema(avro)
    parsed_schema = schema.parse()
    parsed_schema.validate(message)


def validate_json_regexp(event_str, types):
    event = json.loads(event_str)
    types = {item['name']: item['type'] for item in types}

    for field, expr in event.items():
        try:
            re.compile(expr)
        except:
            return f'Regexp validation failed for field {field}'

        if types[field] in (SchemaField.INT, SchemaField.FLOAT):
            if any(c.isalpha() for c in expr) or \
             expr.count('[') != expr.count(']') or \
             expr.count('{') != expr.count('}'):
                return f'Regexp validation failed for field {field}. Provide a correct expression for {types[field]}'

    return ''


def get_schema_fields(project_id):
    schema_fields = {}
    streams = Stream.objects.filter(project_id=project_id)
    for stream in streams:
        fields = SchemaField.objects.filter(schema=stream.schema)
        schema_fields[stream.name] = list(fields.values_list('name', flat=True))
    return schema_fields
