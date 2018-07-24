from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/v1/tasks$', views.get_or_create, name='get_or_create'),
    url(r'^api/v1/tasks/(?P<task_id>[0-9]+)$', views.task_detail, name='task_detail'),
    url(r'^api/v1/tasks/(?P<task_id>[0-9]+)/comments$', views.add_comment, name='add_comment'),
]
