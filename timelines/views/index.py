from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projects.mixins import set_projects
from timelines.models import Timeline


@login_required
def timelines_index(request, project_id):
    timeline_list = Timeline.objects.filter(project_id=project_id).order_by('id')
    context = {'timeline_list': timeline_list}
    set_projects(context, request=request)
    return render(request, 'timelines/index.html', context)
