from django.urls import path

from collaboration import views

app_name = 'collaboration'

urlpatterns = [
    path('', views.CollaborationView.as_view(), name='collaboration_list'),
    path('new/', views.CollaborationCreateView.as_view(), name='new_collaboration'),
    path('<int:collaboration_id>/edit/', views.CollaborationEditView.as_view(), name='edit_collaboration'),
    path('<int:collaboration_id>/delete/', views.CollaborationDeleteView.as_view(), name='delete_collaboration'),
]
