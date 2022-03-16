from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from integration.forms import DataSourceForm
from integration.models import DataSource
from integration.views.base import DataSourceBaseView
from streams.models import Stream


class DataSourceEditView(DataSourceBaseView, UpdateView):
    template_name = 'integration/edit.html'
    model = DataSource
    form_class = DataSourceForm
    pk_url_kwarg = 'data_source_id'
    context_object_name = 'data_source'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.project_id != kwargs.get('project_id'):
            return HttpResponseRedirect(self.get_success_url())
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('projects:integration:data_source_list', kwargs={'project_id': self.kwargs.get('project_id')})

    def get_context_data(self, **kwargs):
        context = super(DataSourceEditView, self).get_context_data(**kwargs)
        self.set_projects(context)
        #context['fields'] = self.object.schemafield_set.order_by('id')
        #context['field_types'] = list(map(lambda avro: list(avro), SchemaField.AVRO_TYPES))
        return context

    def get_form(self,form_class=None):
        form = super(DataSourceEditView, self).get_form(form_class=None)
        form.fields["stream"].queryset = form.fields["stream"].queryset.filter(project__pk=self.kwargs.get('project_id'))
        return form

    def form_valid(self, form):
        data = self.request.POST
        schema = self.object
        cleaned_data = form.cleaned_data

        try:
            self.save_object(obj=schema, **cleaned_data)
        except Exception as error:
            return self.form_invalid(form, exception=error)

        """#fields = schema.schemafield_set.all()

        all_fields = self.filter_contains(initial_dict=data, filter_by='type_field')

        delete_fields = self.filter_contains(initial_dict=all_fields, filter_by='delete')
        delete_fields = list(map(lambda key: int(key.rsplit('_', 1)[1]), delete_fields.keys()))

        all_fields = self.filter_contains(initial_dict=all_fields, filter_by='delete', not_contains=True)

        fields_data = self.filter_contains(initial_dict=data, filter_by='_')
        new_fields = {key: value for key, value in data.items() if '_new_' in key and not key.startswith('delete_')}

        old_fields = {name: value for name, value in fields_data.items() if name not in new_fields}

        if not all_fields:
            fields.delete()

        for field in fields:
            field_id = field.id
            if field_id in delete_fields:
                field.delete()
                continue
            field_info = self.filter_endswith(initial_dict=old_fields, filter_by='_%s' % field_id)

            try:
                self.save_object(obj=field, **field_info)
            except Exception as error:
                return self.form_invalid(form, exception=error)

        new_fields = self.get_fields_forms(new_fields)

        self.process_new_fields(new_fields, schema, form, self.form_invalid)"""

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, **kwargs):
        form.errors['exception'] = kwargs.get('exception')
        return super().form_invalid(form)
