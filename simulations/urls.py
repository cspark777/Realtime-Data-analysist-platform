from django.urls import path

from simulations import views

app_name = 'simulations'

urlpatterns = [
    path('', views.SimulationView.as_view(), name='simulations_list'),
    path('', views.SimulationView.as_view(), name='simulations_list_react'),
    path('<int:simulation_id>/edit/', views.SimulationEditView.as_view(), name='edit_simulation'),
    path('<int:simulation_id>/duplicate/', views.duplicate_simulation, name='duplicate_simulation'),
    path('new/', views.SimulationCreateView.as_view(), name='new_simulation'),
    path('<int:simulation_id>/delete/', views.SimulationDeleteView.as_view(), name='delete_simulation'),
    path('<int:simulation_id>/run/', views.SimulationView.as_view(), name='run_simulation'),
    path('<int:simulation_id>/stop/', views.SimulationView.as_view(), name='stop_simulation'),
]
