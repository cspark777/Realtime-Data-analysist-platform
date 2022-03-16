from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    path('', views.ReportView.as_view(), name='reports'),
    path('list', views.ReportView.as_view(), name='reports_readonly'),
    path('new', views.ReportCreateView.as_view(), name='reports_new'),
    
    path('reports/<int:report_id>/edit', views.ReportEditView.as_view(), name='reports_edit'),
    path('reports/<int:report_id>/duplicate', views.duplicate_report, name='reports_duplicate'),
    path('reports/<int:report_id>/delete', views.ReportDeleteView.as_view(), name='reports_delete'),
    path('reports/<int:report_id>/show', views.show_report, name='reports_show'),
]
