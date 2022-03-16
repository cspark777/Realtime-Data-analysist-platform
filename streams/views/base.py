from django.contrib.auth.mixins import LoginRequiredMixin

from projects.mixins import ProjectsListMixin


class StreamBaseView(LoginRequiredMixin, ProjectsListMixin):
    """Base class for StreamProcessor views"""
