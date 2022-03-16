"""admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from account.views import UserLoginView, UserHelpView, OrganisationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', UserLoginView.as_view()),
    path('help', UserHelpView.as_view(), name="help"),
    path('projects/', include('projects.urls', namespace='projects')),
    path('account/', include('account.urls', namespace='account')),
    path('api/v1/', include('api.urls', namespace='api')),
    path('api/v1/', include('streamprocessors.api.urls')),
    path('api/v1/', include('streams.api.urls')),
    path('api/v1/', include('schemas.api.urls')),
    path('api/v1/', include('datadictionaries.api.urls')),
    path('api/v1/', include('kpis.api.urls')),
    path('api/v1/', include('functions.api.urls')),
    path('api/v1/', include('account.api.urls')),
    path('api/v1/', include('searches.api.urls')),
    path('core/', include('core.urls', namespace='core')),
    path('organisation/<invite_key>/', OrganisationView.as_view(), name='organsiation'),

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
