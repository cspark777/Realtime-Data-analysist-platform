from . import views
from django.urls import include, path

app_name = 'datadictionaries'

urlpatterns = [
    # Processors
    path('', views.DataDictionariesList.as_view(), name='datadictionaries_list'),
    path('new/', views.DataDictionaryCreateView.as_view(), name='datadictionaries_new'),
    path('<int:datadictionary_id>/delete/', views.DataDictionaryDeleteView.as_view(), name='datadictionary_delete'),
    path('<int:datadictionary_id>/edit/', views.DataDictionaryEditView.as_view(), name='datadictionary_edit'),
    path('<int:datadictionary_id>/duplicate/', views.duplicate_datadictionary, name='datadictionary_duplicate'),
]
