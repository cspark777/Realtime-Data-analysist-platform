from django.urls import path, include

from projects import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectsView.as_view(), name='projects_list'),
    path('current_project', views.ProjectView.as_view(), name='current_project'),
    path('<int:project_id>/details/', views.ProjectView.as_view(), name='projects_details'),
    path('<int:project_id>/edit/', views.ProjectEditView.as_view(), name='edit_project'),
    path('<int:project_id>/duplicate/', views.duplicate_project, name='duplicate_project'),
    path('new/', views.ProjectCreateView.as_view(), name='new_project'),
    path('<int:project_id>/delete/', views.ProjectDeleteView.as_view(), name='delete_project'),
    path('<int:project_id>/export/', views.export_project, name='export_project'),
    path('<int:project_id>/api_endpoints/', views.ProjectView.as_view(template_name="projects/api_endpoints.html"), name='api_endpoints'),
    path('import/', views.import_project, name='import_project'),

    path('<int:project_id>/streams/', include('streams.urls', namespace='streams')),
    path('<int:project_id>/streamprocessors/', include('streamprocessors.urls', namespace='streamprocessors')),
    path('<int:project_id>/simulations/', include('simulations.urls', namespace='simulations')),
    path('<int:project_id>/analysis/', include('analysis.urls', namespace='analysis')),
    path('<int:project_id>/timelines/', include('timelines.urls', namespace='timelines')),
    path('<int:project_id>/datadictionaries/', include('datadictionaries.urls', namespace='datadictionaries')),
    path('<int:project_id>/schemas/', include('schemas.urls', namespace='schemas')),
    path('<int:project_id>/functions/', include('functions.urls', namespace='functions')),
    path('<int:project_id>/integration/', include('integration.urls', namespace='integration')),
    path('<int:project_id>/searches/', include('searches.urls', namespace='searches')),
    path('<int:project_id>/collaboration/', include('collaboration.urls', namespace='collaboration')),
]
