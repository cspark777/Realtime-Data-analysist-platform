from django.urls import path
from . import views

app_name = 'searches'

urlpatterns = [
    path('', views.SearchView.as_view(), name='index'),
    path('list', views.SearchView.as_view(), name='index_readonly'),
    path('new', views.SearchCreateView.as_view(), name='create'),
    path('search', views.SearchCreateView.as_view(), name='search'),
    path('extract', views.SearchCreateView.as_view(), name='extract'),
    path('forecast', views.forecast, name='forecast'),
    path('<int:search_id>/edit', views.SearchEditView.as_view(), name='edit'),
    path('<int:search_id>/show', views.SearchEditView.as_view(), name='show'),
    path('<int:search_id>/duplicate', views.duplicate_search, name='duplicate'),
    path('<int:search_id>/delete', views.SearchDeleteView.as_view(), name='delete'),
]
