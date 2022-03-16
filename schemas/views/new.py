from rest_framework import views
from rest_framework.permissions import IsAuthenticated

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages

from schemas.forms import SchemaForm
from schemas.models import Schema, SchemaField
from schemas.views.base import SchemaBaseView
from streams.models import Stream
from streams.utils import DATA_server_stream_create


class SchemaCreateView(SchemaBaseView, CreateView):
    template_name = 'schemas/new.html'
    model = Schema
    form_class = SchemaForm

    def get_success_url(self):
        return reverse_lazy('projects:schemas:schemas_list', kwargs={'project_id': self.kwargs.get('project_id')})

    def get_context_data(self, **kwargs):
        context = super(SchemaCreateView, self).get_context_data(**kwargs)
        self.set_projects(context)
        context['field_types'] = list(map(lambda avro: list(avro), SchemaField.AVRO_TYPES))
        context['new_field_types'] = [list(item) for item in SchemaField.CATEGORICAL_TYPES]
        return context

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        project_id = self.kwargs.get('project_id')
        cleaned_data['project_id'] = project_id
        uploaded_data = None
        if self.request.FILES.get('file'):
            uploaded_data, filename = self.check_json_is_valid(form, self.request.FILES['file'])
            if not uploaded_data:
                error = ("Invalid JSON File")
                return self.form_invalid(form, exception=error)
        schema = self.model()
        data = self.request.POST
        create_stream = data.get('create_stream')

        if create_stream == 'yes':
            name = f'{project_id}_{self.request.user.id}_{cleaned_data.get("name", "").strip().replace(" ", "_")}'
            stream_in_db = Stream.objects.filter(name=name)

            if stream_in_db.exists():
                error = 'The stream with provided name already exists!'
                return self.form_invalid(form, exception=error)

        try:
            self.save_object(obj=schema, **cleaned_data)
        except Exception as error:
            return self.form_invalid(form, exception=error)

        data = self.filter_contains(initial_dict=data, filter_by='delete', not_contains=True)
        fields = self.filter_contains(initial_dict=data, filter_by='_new_')

        new_fields = self.get_fields_forms(fields)

        self.process_new_fields(new_fields, schema, form, self.form_invalid, uploaded_data)

        if create_stream == 'yes':
            stream_data = {
                'project_id': project_id,
                'created_by_id': self.request.user.id,
                'display_name': schema.name,
                'schema_id': schema.id,
            }
            stream = Stream.objects.create(**stream_data)
            DATA_server_stream_create(stream, project_id)
        if uploaded_data:
            msg = 'File Loaded: {}'.format(filename)
            messages.info(self.request, msg)
            success_url = reverse_lazy('projects:schemas:edit_schema', kwargs={'project_id': self.kwargs.get('project_id'), 'schema_id':schema.id})
        else:
            success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    def form_invalid(self, form, **kwargs):
        form.errors['exception'] = kwargs.get('exception')
        return super().form_invalid(form)


class SchemaCreateAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.POST
        return
