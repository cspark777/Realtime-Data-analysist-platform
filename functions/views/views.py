from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.conf import settings

from functions.models import Function, FunctionEndpoint
import json
import requests


@login_required
def duplicate_Function(request, project_id, function_id):
    function = Function.objects.get(pk=function_id)

    if function.project_id == project_id:
        method_duplicate_Function(project_id, function_id)

    return HttpResponseRedirect(reverse_lazy('projects:functions:functions_list', kwargs={'project_id': project_id}))


def method_duplicate_Function(project_id, function_id):
    fields = FunctionEndpoint.objects.filter(Function=function_id)
    function = Function()

    function.project_id = project_id
    function.save()

    for field in fields:
        field.pk = None
        field.Function = function
        field.save()


def handle_function(project_id, function_id, docker_image):
    server_url = f"http://{settings.DATA_SERVER}/run_function"

    data = {
        'project_id': project_id,
        'function_id': function_id,
        'function_docker_image': docker_image,
        'broker_url': settings.KAFKA_URL,
        'replicas': '3',
    }

    data = json.dumps(data)

    return requests.post(server_url, data=data)


def run_Function(request, project_id, function_id):
    function = Function.objects.get(pk=function_id)
    docker_image = function.docker_image

    response = handle_function(project_id, function_id, docker_image)
    status = response.status_code
    return HttpResponseRedirect(reverse_lazy('projects:functions:functions_list', kwargs={'project_id': project_id}))
