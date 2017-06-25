from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list/',
        views.request_list, name='Request_list'),
    url(r'^new/',
        views.request_new, name='Request_new'),
    url(r'^cancel/(?P<req_id>\d+)',
        views.request_cancel, name='Request_cancel'),
    url(r'^approve/(?P<req_id>\d+)',
        views.request_approve, name='Request_approve'),
]
