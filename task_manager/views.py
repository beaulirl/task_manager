# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import json

from django.core.exceptions import ObjectDoesNotExist

from django.core import serializers
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest

from .models import Project, Task, Status, TaskComment


def index(request):
    if request.method == 'GET':
        return get_tasks(request)
    elif request.method == 'POST':
        return create_task(request)


def task_detail(request, task_id):
    if request.method == 'GET':
        return get_task_info(task_id)
    elif request.method == 'PUT':
        return update_task(request, task_id)
    elif request.method == 'DELETE':
        return delete_task(task_id)
    return HttpResponse('Details')


def get_task_info(task_id):
    task = Task.objects.get(pk=int(task_id))
    data = serializers.serialize('json', [task, ])
    return HttpResponse(data, content_type='application/json')


def update_task(request, task_id):
    task = Task.objects.get(pk=int(task_id))
    put_params = json.loads(request.body)
    current_status = task.status
    updated_status = get_or_none(Status, put_params, 'stat') if 'stat' in put_params.keys() else current_status
    if not updated_status:
        return HttpResponseBadRequest(status=400)
    current_task_maker = task.task_maker
    updated_task_maker = get_or_create(
        User, put_params, 't_m', field='username'
    ) if 't_m' in put_params.keys() else current_task_maker
    Task.objects.filter(pk=int(task_id)).update(status=updated_status, task_maker=updated_task_maker)
    return HttpResponse(status=201)


def delete_task(task_id):
    Task.objects.filter(pk=int(task_id)).delete()
    return HttpResponse(status=200)


def get_tasks(request):
    tasks = Task.objects.all()
    if request.GET:
        filter_dict = {}
        for param, key, model, field in (
                ('task_maker', 't_m', User, 'username'),
                ('task_author', 't_a', User, 'username'),
                ('status', 'stat', Status, 'name'),
                ('project', 'pr', Project, 'name')
        ):
            if request.GET.get(key):
                value = get_or_none(model, request.GET, key, field=field)
                if value:
                    filter_dict[param] = value
        tasks = Task.objects.filter(**filter_dict)
    data = serializers.serialize('json', tasks)
    return HttpResponse(data, content_type='application/json')


def create_task(request):
    post_params = json.loads(request.body)
    project = get_or_create(Project, post_params, 'project')
    status = get_or_none(Status, post_params, 'status')
    if not status:
        return HttpResponseBadRequest(status=400)
    task_maker = get_or_create(User, post_params, 't_m', field='username')
    task_author = get_or_create(User, post_params, 't_a', field='username')
    task = Task(
        name=post_params['name'],
        project=project,
        status=status,
        task_maker=task_maker,
        task_author=task_author
    )
    task.save()
    return HttpResponse(status=201)


def get_or_create(model, params, key, field='name'):
    query = {field: params[key]}
    try:
        param = model.objects.get(**query)
    except ObjectDoesNotExist:
        if model == User:
            param = User.objects.create_user(**query)
        else:
            param = model(**query)
        param.save()
    return param


def get_or_none(model, params, key, field='name'):
    query = {field: params[key]}
    try:
        param = model.objects.get(**query)
    except ObjectDoesNotExist:
        param = None
    return param


def add_comment(request, task_id):
    if request.method == 'GET':
        return HttpResponseBadRequest(status=400)
    text = json.loads(request.body)['comment']
    task = Task.objects.get(pk=int(task_id))
    comment = TaskComment(comment=text, task=task)
    comment.save()
    return HttpResponse(status=201)
