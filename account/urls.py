from django.urls import path
from django.contrib.auth.views import LogoutView

from account import views

app_name = 'account'


urlpatterns = [
    path('', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('sign-up/', views.UserCreateView.as_view(), name='signup'),
    path('edit/<int:pk>/', views.UserEditView.as_view(), name='edit'),
    path('validate-developer-key/', views.validate_developer_key, name='validate-developer-key'),

    path('<int:user_id>/workflow/', views.WorkflowTasksView.as_view(), name='workflow-tasks'),
    path('<int:user_id>/workflow/<workflow_id>/delete/', views.WorkflowDeleteView.as_view(), name='workflow-delete'),
    path('organisation/<invite_key>/', views.OrganisationView.as_view(), name='organsiation_invite'),

]
