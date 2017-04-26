from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list/',
        views.request_list, name='Request_list'),
]
