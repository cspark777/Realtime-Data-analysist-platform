from django.urls import path

from schemas import views

app_name = 'schemas'

urlpatterns = [
    path('', views.SchemaView.as_view(), name='schemas_list'),
    path('new/', views.SchemaCreateView.as_view(), name='new_schema'),
    path('<int:schema_id>/edit/', views.SchemaEditView.as_view(), name='edit_schema'),
    path('<int:schema_id>/delete/', views.SchemaDeleteView.as_view(), name='delete_schema'),
    path('<int:schema_id>/duplicate/', views.duplicate_schema, name='duplicate_schema'),
    path('<int:schema_id>/export/', views.export_schema, name='export_schema'),
]
