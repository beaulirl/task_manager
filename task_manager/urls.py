from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^tasks/$', views.index, name='index'),
    url(r'^tasks/(?P<task_id>[0-9]+)/$', views.task_detail, name='task_detail'),
    url(r'^tasks/(?P<task_id>[0-9]+)/comments/$', views.add_comment, name='add_comment'),
]
