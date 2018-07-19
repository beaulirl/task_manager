# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse

from .models import Project, Description, TaskComment, Task, Status


def index(request):
    if request.method == 'GET':
        return get_tasks()
    elif request.method == 'POST':
        return create_task(request)


def task_detail(request):
    if request.method == 'GET':
        get_task_info()
    elif request.method == 'PUT':
        update_task()
    elif request.method == 'DELETE':
        delete_task()
    return HttpResponse('Details')


def get_task_info():
    pass


def update_task():
    pass


def delete_task():
    pass


def get_tasks():
    tasks = Task.objects.all()
    data = serializers.serialize('json', tasks)
    return HttpResponse(data, content_type='application/json')


def create_task(request):
    asg = request.body
    return HttpResponse(asg, content_type='application/json')

