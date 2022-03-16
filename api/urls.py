from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from groups.api import views as group_views

from api.views import (
    ConfigDetail,
    Streams,
    StreamProcessors,
    FunctionViewSet,
    FunctionEndpointViewSet,
    StreamViewSet,
    StreamProcessorViewSet,
    SimulationViewSet,
    UserView,
    StreamEventView,
    OrganisationView,
    SiteConfigurationView,
    StreamProcessorActionView,
    SimulationActionView,
    ProjectViewSet, FunctionActionView,
)

app_name = "api"

router = routers.DefaultRouter()
router.register(
    r"function_endpoints", FunctionEndpointViewSet, basename="function_endpoints"
)
router.register(r"functions", FunctionViewSet, basename="functions")
router.register(r"streams", StreamViewSet)
router.register(r"streamprocessors", StreamProcessorViewSet)
router.register(r"simulations", SimulationViewSet)
router.register(r"projects", ProjectViewSet)

# GROUPS
router.register(r"stream_groups", group_views.StreamGroupViewSet, basename="stream_groups")
router.register(r"streamprocessor_groups", group_views.StreamProcessorGroupViewSet)
router.register(r"simulation_groups", group_views.SimulationGroupViewSet)

urlpatterns = [
    url(r"^", include(router.urls)),
    path("config/", ConfigDetail.as_view()),
    path("cli/streams/", Streams.as_view()),
    path("cli/streamprocessors/", StreamProcessors.as_view()),
    path("streamprocessor_action/run", StreamProcessorActionView.as_view(action="run")),
    path(
        "streamprocessor_action/stop", StreamProcessorActionView.as_view(action="stop")
    ),
    path("simulation_action/run", SimulationActionView.as_view()),
    path("simulation_action/stop", SimulationActionView.as_view()),
    path("function_action/run", FunctionActionView.as_view()),
    path("me/", UserView.as_view()),
    path("stream_events/", StreamEventView.as_view()),
    path("site_configuration/", SiteConfigurationView.as_view()),
    path("organisation/<int:pk>/", OrganisationView.as_view()),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
