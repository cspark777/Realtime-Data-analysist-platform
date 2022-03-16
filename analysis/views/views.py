from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from analysis.models import Report
from .utils import method_duplicate_duplicate_report


@login_required
def duplicate_report(request, project_id, report_id):
    report = Report.objects.get(pk=report_id)
    if report.project_id == report_id:
        method_duplicate_duplicate_report(project_id, report)

    return HttpResponseRedirect(reverse_lazy('projects:analysis:reports', kwargs={'project_id': project_id}))
