from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from analysis.views.utils import method_duplicate_duplicate_report
from projects.models import Project
from simulations.views import method_duplicate_simulation
from streamprocessors.views import method_duplicate_streamprocessor


@login_required
def duplicate_project(request, project_id):
    project = Project.objects.get(pk=project_id, created_by=request.user)
    streams = project.stream_set.all()
    streamprocessors = project.streamprocessor_set.all()
    simulations = project.simulation_set.all()
    kpis = project.kpi_set.all()
    reports = project.report_set.all()

    project.pk = None
    project.save()

    for stream in streams:
        stream.pk = None
        stream.project = project
        stream.save()

    for streamprocessor in streamprocessors:
        method_duplicate_streamprocessor(project.id, streamprocessor)

    for simulation in simulations:
        method_duplicate_simulation(project.id, simulation)

    for kpi in kpis:
        kpi.pk = None
        kpi.project = project
        kpi.save()

    for report in reports:
        method_duplicate_duplicate_report(project.id, report)

    return HttpResponseRedirect(reverse_lazy('projects:projects_details', kwargs={'project_id': project.id}))
