import json

from django import template

from streamprocessors.models import StreamProcessorStep

register = template.Library()
DEFAULT_VALUE = str()


@register.filter(name='lookup')
def lookup(obj, key):
    return getattr(obj, key) or DEFAULT_VALUE


@register.filter
def get_value_in_qs(queryset, key):
    return ', '.join(queryset.values_list(key, flat=True))


@register.filter
def get_popover_attrs(step_type):
    return StreamProcessorStep.STEP_TYPES_DATA.get(step_type, {}).get('popover')


@register.filter
def get_step_type_field(fields, field_name):
    fields = map(lambda i: i.get('fields'), fields.values())
    exists_fields = list(filter(lambda field: any(map(lambda j: j.get('name') == field_name, field)), fields))
    if exists_fields:
        exists_fields = list(filter(lambda field: field.get('name') == field_name, exists_fields[0]))
    return exists_fields[0] if exists_fields else DEFAULT_VALUE


@register.filter
def get_step_type_block_field(fields, field_name):
    fields = list(filter(lambda field: field[0].get('name') == 'block', map(lambda i: i.get('fields'), fields.values())))[0]
    exists_fields = list(filter(lambda y: y.get('name') == 'event_field_name', list(map(lambda x: x.get('fields'), fields))[0]))
    return exists_fields[0] if exists_fields else DEFAULT_VALUE


@register.filter
def get_item(obj, field):
    return obj.get(field, {})


@register.filter
def get_item_str(s, field):
    return json.loads(s).get(field, {})


@register.filter
def at_index(indexable, i):
    return indexable[i]
