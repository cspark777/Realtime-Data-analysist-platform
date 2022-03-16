from . import views
from django.urls import include, path


app_name = 'streamprocessors'

urlpatterns = [

    # Processors
    path('', views.StreamProcessorIndexView.as_view(), name='streamprocessors_list'),
    path('deploy/<int:streamprocessor_id>/<str:status>/', views.StreamProcessorIndexView.as_view(), name='streamprocessors_after_run'),
    path('new', views.StreamProcessorNewView.as_view(), name='new'),
    path('testsimulate', views.streamprocessor_test, name='test'),
    path('<int:streamprocessor_id>/edit/', views.StreamProcessorEditView.as_view(), name='edit'),
    path('<int:streamprocessor_id>/duplicate/', views.duplicate_streamprocessor, name='duplicate'),
    path('<int:streamprocessor_id>/logs/', views.view_logs, name='view_logs'),
    path('<int:streamprocessor_id>/delete/', views.StreamProcessorDeleteView.as_view(), name='delete'),
    path('<int:streamprocessor_id>/run/', views.streamprocessor_run, name='run'),
    path('<int:streamprocessor_id>/stop/', views.streamprocessor_stop, name='stop'),
    path('<int:streamprocessor_id>/monitor/', views.StreamProcessorMonitorView.as_view(), name='monitor'),

    path('kpis/', include('kpis.urls')),

    path('source/<str:object_id>/', views.source_events, name='source_events'),
    path('source/summary/<str:object_id>/', views.source_events_summary, name='source_events_summary'),
    path('source/headers', views.get_logs_headers, name='get_logs_headers'),
    path('source/rows', views.get_logs_rows, name='get_logs_rows'),
    path('source/<int:streamprocessor_id>/logs/', views.source_logs, name='source_logs'),
    path('all-logs/', views.Logs.as_view(), name='all-logs'),
]
