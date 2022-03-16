from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from searches.models import Search
from .utils import method_duplicate_search


@login_required
def duplicate_search(request, project_id, search_id):
    search = Search.objects.get(pk=search_id)
    if search.project_id == project_id:
        method_duplicate_search(project_id, search)

    return HttpResponseRedirect(reverse_lazy('projects:searches:index', kwargs={'project_id': project_id}))
