from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .base import StreamBaseView
from streams.forms import StreamForm
from streams.models import Stream
from streams.utils import DATA_server_stream_create


kafka_url = settings.KAFKA_URL


class StreamCreateView(StreamBaseView, CreateView):
    template_name = 'streams/new.html'
    model = Stream
    form_class = StreamForm

    def get_initial(self):
        initial = super(StreamCreateView, self).get_initial()
        initial['project_id'] = self.kwargs.get('project_id')
        return initial

    def get_success_url(self):
        return "/react" + str(reverse_lazy('projects:streams:index', kwargs={'project_id': self.kwargs.get('project_id')}))

    def form_valid(self, form):
        project_id = self.kwargs.get('project_id')
        cleaned_data = form.cleaned_data

        name = f'{project_id}_{self.request.user.id}_{cleaned_data.get("display_name", "").strip().replace(" ", "_")}'
        stream_in_db = Stream.objects.filter(name=name)

        if stream_in_db.exists():
            error = 'This stream exists in another project!'
            return self.render_to_response(self.get_context_data(error=error))

        stream_data = {
            'project_id': project_id,
            'created_by_id': self.request.user.id,
        }
        cleaned_data.update(stream_data)
        stream = Stream.objects.create(**cleaned_data)

        DATA_server_stream_create(stream, project_id)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(StreamCreateView, self).get_context_data(**kwargs)
        context['title_object'] = self.model._meta.model_name
        self.set_projects(context)
        return context
