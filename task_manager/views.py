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
    return HttpResponseBadRequest()


def task_detail(request, task_id):
    if request.method == 'GET':
        return get_task_info(task_id)
    elif request.method == 'PUT':
        return update_task(request, task_id)
    elif request.method == 'DELETE':
        return delete_task(task_id)
    return HttpResponseBadRequest()


def get_task_info(task_id):
    try:
        Task.objects.get(pk=int(task_id))
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('Error: there is no task with id {}'.format(task_id))
    task_comment = TaskComment.objects.prefetch_related('task').filter(task__pk=int(task_id))
    data = serializers.serialize('json', task_comment, use_natural_foreign_keys=True)

    return HttpResponse(data, content_type='application/json')


def update_task(request, task_id):
    try:
        Task.objects.get(pk=int(task_id))
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('Error: there is no task with id {}'.format(task_id))
    put_params = json.loads(request.body)
    updated_dict = {}
    for key, model, field in (
            ('task_maker', User, 'username'),
            ('status', Status, 'name')):
        if key in put_params.keys():
            updated_value = get_or_none(model, put_params, key, field)
            if not updated_value:
                return HttpResponseBadRequest('Error: there is no such {}'.format(key))
            updated_dict[key] = updated_value
    Task.objects.filter(pk=int(task_id)).update(**updated_dict)
    return HttpResponse(status=201)


def delete_task(task_id):
    Task.objects.filter(pk=int(task_id)).delete()
    return HttpResponse(status=200)


def get_tasks(request):
    if request.GET:
        filter_dict = {}
        for key, field in (
                ('task_maker', 'username'),
                ('task_author', 'username'),
                ('status', 'name'),
                ('project', 'name')
        ):
            if request.GET.get(key):
                filter_dict['{}__{}'.format(key, field)] = request.GET[key]
        tasks = Task.objects.filter(**filter_dict)
    else:
        tasks = Task.objects.all()
    data = serializers.serialize('json', tasks, use_natural_foreign_keys=True)
    return HttpResponse(data, content_type='application/json')


def create_task(request):
    post_params = json.loads(request.body)
    if not post_params.get('name'):
        return HttpResponseBadRequest('Error: there is no task name in post params')
    create_dict = {}
    for key, model, field in (
            ('task_maker', User, 'username'),
            ('task_author', User, 'username'),
            ('status', Status, 'name'),
            ('project', Project, 'name')
    ):
        if not post_params.get(key):
            return HttpResponseBadRequest('Error: no such field {} in post params'.format(key))
        value = get_or_none(model, post_params, key, field)
        if not value:
            return HttpResponseBadRequest('Error: there is no {} with such name'.format(key))
        create_dict[key] = value
    task = Task(name=post_params['name'], **create_dict)
    task.save()
    return HttpResponse(status=201)


def get_or_none(model, params, key, field='name'):
    query = {field: params[key]}
    try:
        param = model.objects.get(**query)
    except ObjectDoesNotExist:
        param = None
    return param


def add_comment(request, task_id):
    if request.method != 'POST':
        return HttpResponseBadRequest('Error: wrong HTTP method')
    text = json.loads(request.body)['comment']
    try:
        task = Task.objects.get(pk=int(task_id))
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('Error: there is no task with id {}'.format(task_id))
    comment = TaskComment(comment=text, task=task)
    comment.save()
    return HttpResponse(status=201)

