import json
import requests

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from streams.models import Stream


kafka_url = settings.KAFKA_URL


@login_required
def reset_druid_stream(request, project_id, stream_id):
    stream = Stream.objects.filter(id=stream_id, project_id=project_id, created_by=request.user)
    if stream.exists():
        stream = stream.first()
        server_url = settings.DATA_SERVER + 'druid_stream_reset'
        data = json.dumps({
            'broker_url': kafka_url,
            'database_url': settings.DRUID_URL,
            'project_id': project_id,
            'stream_name': stream.name,
        })
        requests.post(server_url, data=data)
    return HttpResponseRedirect(reverse_lazy('projects:streams:index', kwargs={'project_id': project_id}))
