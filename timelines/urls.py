from django.urls import path

from . import views

app_name = 'timelines'


urlpatterns = [

    path('', views.timelines_index, name='index'),
    path('new/', views.TimelineCreateView.as_view(), name='new'),
    path('<int:timeline_id>/edit/', views.TimelineEditView.as_view(), name='edit_timeline'),
    path('<int:timeline_id>/delete/', views.TimelineDeleteView.as_view(), name='delete'),
    path('<int:pk>/show/', views.TimelineShowView.as_view(), name='show'),

]
