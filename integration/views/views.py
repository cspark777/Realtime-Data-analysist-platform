import time
import csv
import json
from io import StringIO

from rest_framework import views, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from integration.models import DataSource, ImportData
from projects.mixins import ProjectsListMixin
from projects.mixins import set_projects
from schemas.models import Schema, SchemaField
from streamprocessors.kafka_utils import send_kafka_message
from streams.models import Stream
from streams.utils import DATA_server_stream_create


@login_required
def duplicate_data_source(request, project_id, data_source_id):
    data_source = DataSource.objects.get(pk=data_source_id)
    print(data_source.stream.project_id, project_id)
    if data_source.stream.project_id == project_id:
        data_source.pk = None
        data_source.save()

    return HttpResponseRedirect(
        reverse_lazy('projects:integration:data_source_list', kwargs={'project_id': project_id}))


def method_duplicate_schema(project_id, data_source):
    data_source.pk = None
    data_source.save()


@login_required
def download_configuration(request, project_id):
    data_source = DataSource.objects.filter(stream__project__id=project_id)
    rendered = render_to_string('integration/configuration_template.txt', {'source': data_source})
    response = HttpResponse(rendered, content_type='application/text')
    response['Content-Disposition'] = 'attachment; filename=configuration.conf'
    return response


class ExtractView(ProjectsListMixin, TemplateView):
    template_name = 'integration/extract.html'

    def get_context_data(self, **kwargs):
        context = dict()
        set_projects(context, request=self.request)
        return context


class ImportView(ExtractView):
    template_name = 'integration/wizard_data_upload.html'


class FileUploadView(views.APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        content_type = file.content_type
        if file and content_type in ('text/csv', 'application/json'):
            for data in ImportData.objects.filter(
                project_id=kwargs.get('project_id'),
                user=request.user,
            ):
                data.delete()
            ImportData.objects.create(
                project_id=kwargs.get('project_id'),
                user=request.user,
                file=file,
                content_type=content_type,
            )
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ImportTableView(ProjectsListMixin, TemplateView):
    template_name = 'integration/import_table.html'

    def get_context_data(self, **kwargs):
        context = dict()
        set_projects(context, request=self.request)
        data = ImportData.objects.filter(
            project_id=kwargs.get('project_id'),
            user=self.request.user,
        ).order_by('-id').first()
        ret_data = []
        count = 0
        if data.content_type == 'text/csv':
            content = list(csv.reader(StringIO(data.file.read().decode('utf-8')), delimiter=','))
            keys = []
            counter = 0
            count = len(content) - 1
            for line in content:
                if not keys:
                    keys = [*line]
                else:
                    ret_data.append(dict(zip(keys, line)))
                    counter += 1
                    if counter >= 1000:
                        break
        elif data.content_type == 'application/json':
            file_data = json.load(data.file)
            ret_data = file_data[:1000]
            for line in ret_data:
                line.update((key, f'{value}') for key, value in line.items() if value in (True, False))
            count = len(file_data)
        try:
            table_headers = list(ret_data[0].keys())
        except Exception:
            table_headers = []
        data.headers = table_headers
        data.count = count
        data.save()
        context['table_data'] = ret_data
        context['table_headers'] = table_headers
        return context


class ImportSchemaView(ProjectsListMixin, TemplateView):
    template_name = 'integration/import_schema.html'

    def get_context_data(self, **kwargs):
        context = dict()
        set_projects(context, request=self.request)
        schemas = Schema.objects.filter(project_id=kwargs.get('project_id'))
        schemas_list = [
            {'name': schema.name, 'fields': list(schema.schemafield_set.all().values('name')), 'id': schema.id}
            for schema in schemas
        ]
        context['schemas'] = schemas_list
        context['field_types'] = [list(item) for item in SchemaField.AVRO_TYPES]
        data = ImportData.objects.filter(
            project_id=kwargs.get('project_id'),
            user=self.request.user,
        ).order_by('-id').first()
        context['table_headers'] = data.headers if data else []
        return context


class DataSchemaValidateView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id')
        data = request.data
        create = data.get('create_definition')
        new_schema_name = data.get('new_schema_name')
        import_data = ImportData.objects.filter(
            project_id=kwargs.get('project_id'),
            user=self.request.user,
        ).order_by('-id').first()
        import_data_headers = import_data.headers
        new_headers = [
            header for header in import_data_headers if header in [x.rpartition('_')[2] for x in data.keys()]
        ]
        if create == 'yes' and not Stream.objects.filter(project_id=project_id, display_name=new_schema_name).exists():
            import_data.use_schema = ImportData.NEW
            import_data.save()
            schema_fields = []
            schema = Schema.objects.create(
                project_id=project_id,
                name=new_schema_name,
            )
            for header in new_headers:
                new_schema_field = {
                    name.replace(f"_{header}", ""): value for name, value in data.items() if name.endswith(header)
                }
                new_schema_field['schema'] = schema
                schema_fields.append(new_schema_field)
            new_schema_fields = [SchemaField(**field) for field in schema_fields]
            SchemaField.objects.bulk_create(new_schema_fields)
            stream_data = {
                'project_id': project_id,
                'created_by_id': request.user.id,
                'display_name': schema.name,
                'schema_id': schema.id,
            }
            stream = Stream.objects.create(**stream_data)
            DATA_server_stream_create(stream, project_id)
            return Response(data={'schema': schema.id}, status=status.HTTP_200_OK)
        elif create == 'no':
            current_schema_name = data.get('schema_type')
            current_schema = Schema.objects.filter(
                project_id=project_id,
                name=current_schema_name,
            ).order_by('-id').first()
            stream_data = {
                header: value for name, value in data.items() for header in new_headers if name.endswith(header)
            }
            import_data.stream_data = stream_data
            import_data.use_schema = ImportData.EXISTING
            import_data.save()
            return Response(data={'schema': current_schema.id}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ImportStreamView(ExtractView):
    template_name = 'integration/import_stream.html'

    def get_context_data(self, **kwargs):
        context = dict()
        set_projects(context, request=self.request)
        schema = self.request.GET.get('schema')
        context['streams'] = Stream.objects.filter(
            project_id=kwargs.get('project_id'),
            schema=schema,
        ).values('name', 'display_name')
        data = ImportData.objects.filter(
            project_id=kwargs.get('project_id'),
            user=self.request.user,
        ).order_by('-id').first()
        context['counter'] = data.count
        return context


class StreamDataUploadView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        import_data = ImportData.objects.filter(
            project_id=kwargs.get('project_id'),
            user=self.request.user,
        ).order_by('-id').first()
        stream_name = request.data.get('stream_name')
        if Stream.objects.filter(name=stream_name).exists():
            file_data = []
            if import_data.content_type == 'text/csv':
                content = csv.reader(StringIO(import_data.file.read().decode('utf-8')), delimiter=',')
                keys = []
                for line in content:
                    if not keys:
                        keys = [*line]
                    else:
                        file_data.append(dict(zip(keys, line)))
            elif import_data.content_type == 'application/json':
                file_data = json.load(import_data.file)
            if file_data:
                stream_data = import_data.stream_data
                time.sleep(5)
                for line in file_data:
                    if import_data.use_schema == ImportData.EXISTING:
                        line = {stream_data.get(name): value for name, value in line.items()}
                    line['project_id'] = kwargs.get('project_id')
                    send_kafka_message(stream_name, json.dumps(line))
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SearchView(ExtractView):
    template_name = 'integration/search.html'
