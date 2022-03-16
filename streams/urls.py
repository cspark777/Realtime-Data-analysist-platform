from django.urls import path

from streams import views

app_name = 'streams'


urlpatterns = [
    # Streams
    path('', views.stream_index, name='index'),
    path('new/', views.StreamCreateView.as_view(), name='new'),
    path('logs/', views.stream_logs, name='logs'),
    path('<int:stream_id>/reset', views.reset_druid_stream, name='reset'),
    path('<int:stream_id>/monitor', views.stream_monitor, name='monitor'),
    path('<int:stream_id>/analyse', views.stream_analyse, name='analyse'),
    path('<int:stream_id>/edit/', views.StreamEditView.as_view(), name='edit'),
    path('<int:stream_id>/delete/', views.StreamDeleteView.as_view(), name='delete'),
]
