from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from simulations.models import Simulation, Step


@login_required
def duplicate_simulation(request, project_id, simulation_id):
    simulation = Simulation.objects.get(pk=simulation_id)

    if simulation.project_id == project_id:
        method_duplicate_simulation(project_id, simulation)

    return HttpResponseRedirect(reverse_lazy('projects:simulations:simulations_list', kwargs={'project_id': project_id}))


def method_duplicate_simulation(project_id, simulation):
    steps = Step.objects.filter(simulation=simulation)

    simulation.pk = None
    simulation.project_id = project_id
    simulation.save()

    for step in steps:
        step.pk = None
        step.simulation = simulation
        step.save()
