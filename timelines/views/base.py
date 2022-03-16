from django.contrib.auth.mixins import LoginRequiredMixin

from projects.mixins import ProjectsListMixin


class TimelineBaseView(LoginRequiredMixin, ProjectsListMixin):
    """Base class for Simulation views"""
