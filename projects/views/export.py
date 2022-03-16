from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy

from projects.models import Project


@login_required
def export_project(request, project_id):
    project = Project.objects.filter(pk=project_id, created_by=request.user)
    if not project.exists():
        return HttpResponseRedirect(reverse_lazy('projects:projects_details', kwargs={'project_id': project_id}))
    project = project.first()

    streamprocessor_set = project.streamprocessor_set.all()
    simulation_set = project.simulation_set.all()
    report_set = project.report_set.all()
    schema_set = project.schema_set.all()
    timeline_set = project.timeline_set.all()

    data = [
        *schema_set,
        *project.stream_set.all(),
        *timeline_set,
        *streamprocessor_set,
        *simulation_set,
        *project.kpi_set.all(),
        *report_set,
    ]

    for schema in schema_set:
        data = [*data, *schema.schemafield_set.all()]

    for timeline in timeline_set:
        data = [*data, *timeline.timelineitem_set.all()]

    for streamprocessor in streamprocessor_set:
        data = [*data, *streamprocessor.streamprocessorstep_set.all()]
        for step in streamprocessor.streamprocessorstep_set.all():
            if step.get_children():
                data = [*data, *step.get_children()]

    for simulation in simulation_set:
        data = [*data, *simulation.step_set.all()]

    for report in report_set:
        data = [*data, *report.reportitem_set.all()]

    serializer = serializers.serialize('json', data, indent=2)
    response = HttpResponse(serializer, content_type='application/json')
    file_name = '_'.join(project.name.split()).lower()
    response['Content-Disposition'] = 'attachment; filename=%s.json' % file_name
    return response

