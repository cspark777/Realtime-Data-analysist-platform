from django.urls import path

from integration import views

app_name = 'integration'

urlpatterns = [
    path('', views.DataSourceView.as_view(), name='data_source_list'),
    path('new/', views.DataSourceCreateView.as_view(), name='new_data_source'),
    path('<int:data_source_id>/edit/', views.DataSourceEditView.as_view(), name='edit_data_source'),
    path('<int:data_source_id>/delete/', views.DataSourceDeleteView.as_view(), name='delete_data_source'),
    path('<int:data_source_id>/duplicate/', views.duplicate_data_source, name='duplicate_data_source'),
    path('download_configuration/', views.download_configuration, name='download_configuration'),
    path('import/', views.ImportView.as_view(), name='data_source_import'),
    path('import_table/', views.ImportTableView.as_view(), name='data_table_import'),
    path('import_schema/', views.ImportSchemaView.as_view(), name='data_schema_import'),
    path('import_stream/', views.ImportStreamView.as_view(), name='data_stream_import'),
    path('search/', views.SearchView.as_view(), name='data_source_search'),
    path('extract/', views.ExtractView.as_view(), name='data_source_extract'),
    path('upload/', views.FileUploadView.as_view(), name='file_upload'),
    path('stream_upload/', views.StreamDataUploadView.as_view(), name='stream_upload'),
    path('schema_validation/', views.DataSchemaValidateView.as_view(), name='data_schema_validation'),
]
