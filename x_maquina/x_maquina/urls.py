"""x_maquina URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import (include, url, handler400, handler403,
                              handler404, handler500)
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.home, name="Home"),
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include('user.urls', namespace="user")),
    url(r'^request/', include('request.urls', namespace="request")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'x_maquina.views.bad_request'
handler403 = 'x_maquina.views.permission_denied'
handler404 = 'x_maquina.views.page_not_found'
handler500 = 'x_maquina.views.server_error'
