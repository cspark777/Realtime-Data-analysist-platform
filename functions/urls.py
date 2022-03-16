from django.urls import path

from functions import views

app_name = 'functions'

urlpatterns = [
    path('', views.FunctionView.as_view(), name='functions_list'),
    path('new/', views.FunctionCreateView.as_view(), name='new'),
    path('<int:function_id>/edit/', views.FunctionEditView.as_view(), name='edit'),
    path('<int:function_id>/delete/', views.FunctionDeleteView.as_view(), name='delete'),
    path('<int:function_id>/duplicate/', views.duplicate_Function, name='duplicate'),
    path('<int:function_id>/run/', views.run_Function, name='run'),
    path('<int:function_id>/stop/', views.FunctionEditView.as_view(), name='stop'),
    path('<int:function_id>/view_logs/', views.FunctionEditView.as_view(), name='view_logs'),
]
 