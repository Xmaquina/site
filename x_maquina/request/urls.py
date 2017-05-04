from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list/',
        views.request_list, name='Request_list'),
    url(r'^new/',
        views.request_new, name='Request_new'),
]
