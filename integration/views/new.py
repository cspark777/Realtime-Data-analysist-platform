from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from integration.forms import DataSourceForm
from integration.models import DataSource
from integration.views.base import DataSourceBaseView
from streams.models import Stream
from streams.utils import DATA_server_stream_create


class DataSourceCreateView(DataSourceBaseView, CreateView):
    template_name = 'integration/new.html'
    model = DataSource
    form_class = DataSourceForm

    def get_success_url(self):
        return reverse_lazy('projects:integration:data_source_list', kwargs={'project_id': self.kwargs.get('project_id')})

    def get_context_data(self, **kwargs):
        context = super(DataSourceCreateView, self).get_context_data(**kwargs)
        self.set_projects(context)
        context['source_types'] = list(map(lambda avro: list(avro), DataSource.SOURCE_TYPES))
        return context

    def get_form(self,form_class=None):
        form = super(DataSourceCreateView, self).get_form(form_class=None)
        form.fields["stream"].queryset = form.fields["stream"].queryset.filter(project__pk=self.kwargs.get('project_id'))
        return form

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        project_id = self.kwargs.get('project_id')
        cleaned_data['project_id'] = project_id
        schema = self.model()
        data = self.request.POST
        create_stream = data.get('create_stream')
        if create_stream == 'yes':
            name = f'{self.request.user.id}_{cleaned_data.get("name", "").strip().replace(" ", "_")}'
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

        self.process_new_fields(new_fields, schema, form, self.form_invalid)

        if create_stream == 'yes':
            stream_data = {
                'project_id': project_id,
                'created_by_id': self.request.user.id,
                'display_name': schema.name,
                'schema_id': schema.id,
            }
            stream = Stream.objects.create(**stream_data)
            DATA_server_stream_create(stream, project_id)

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, **kwargs):
        form.errors['exception'] = kwargs.get('exception')
        return super().form_invalid(form)
