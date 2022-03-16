from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
import json

from schemas.models import Schema, SchemaField
from core.utils import generate_schema_avro


@login_required
def duplicate_schema(request, project_id, schema_id):
    schema = Schema.objects.get(pk=schema_id)

    if schema.project_id == project_id:
        method_duplicate_schema(project_id, schema)

    return HttpResponseRedirect(reverse_lazy('projects:schemas:schemas_list', kwargs={'project_id': project_id}))


def method_duplicate_schema(project_id, schema):
    fields = SchemaField.objects.filter(schema=schema)

    schema.pk = None
    schema.project_id = project_id
    schema.save()

    for field in fields:
        field.pk = None
        field.schema = schema
        field.save()

@login_required
def export_schema(request, project_id, schema_id):
    schema = get_object_or_404(Schema, pk=schema_id)
    avro = generate_schema_avro(schema)
    try:
        avro = json.dumps(avro, indent=2)
    except:
        avro = []
    filename = '{}.avro'.format(schema.name)
    response = HttpResponse(avro, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    return response
