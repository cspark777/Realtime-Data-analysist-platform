from django.urls import path

from kpis import views

app_name = 'kpis'

urlpatterns = [
    path('', views.KPIView.as_view(), name='kpi_list'),
    path('<int:KPI_id>/edit/', views.KPIEditView.as_view(), name='edit_kpi'),
    path('current', views.kpi_current, name='current'),
    path('monitor/<int:KPI_id>/counter/', views.KPIMonitorCounterView.as_view(), name='monitor_kpi_counter'),
    path('monitor/<int:KPI_id>/measurement/', views.KPIMonitorMeasurementView.as_view(), name='monitor_kpi_measurement'),
    path('new/', views.KPICreateView.as_view(), name='new_kpi'),
    path('<int:KPI_id>/delete/', views.KPIDeleteView.as_view(), name='delete_kpi'),
    path('<int:KPI_id>/rows/', views.get_kpis_rows, name='get_kpis_rows'),
    path('<int:KPI_id>/report_data/', views.get_report_data, name='get_report_data'),
]
