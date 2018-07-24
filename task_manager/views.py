# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse


from .models import Project, Task, Status, Comment, Description


def index(request):
    return HttpResponse('This is start page, please, find correct URLs for using API in README.md')


def get_or_create(request):
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
    task = Task.objects.select_related().get(pk=int(task_id))
    comments = Comment.objects.filter(task__pk=int(task_id))
    descriptions = Description.objects.filter(task__pk=int(task_id))
    result = {
        'task_id': task.pk,
        'task_author': task.task_author.username,
        'task_status': task.status.name,
        'task_maker': task.task_maker.username,
        'comments': [comment.comment for comment in comments],
        'descriptions': [description.text for description in descriptions]
    }
    return JsonResponse(result)


def update_task(request, task_id):
    try:
        Task.objects.get(pk=int(task_id))
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('Error: there is no task with id {}'.format(task_id))
    put_params = json.loads(request.body)
    updated_dict = {}
    for key, model, field in (
            ('task_maker', User, 'pk'),
            ('status', Status, 'name')):
        if key in put_params.keys():
            updated_value = get_or_none(model, put_params, key, field)
            if not updated_value:
                return HttpResponseBadRequest('Error: there is no such {}'.format(key))
            updated_dict[key] = updated_value
    Task.objects.filter(pk=int(task_id)).update(**updated_dict)
    return HttpResponse(status=200)


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
        if not filter_dict:
            return HttpResponseBadRequest('Error: wrong get params')
        tasks = Task.objects.filter(**filter_dict)
    else:
        tasks = Task.objects.all()
    task_results = []
    for task in tasks:
        comments = Comment.objects.filter(task__pk=int(task.pk))
        descriptions = Description.objects.filter(task__pk=int(task.pk))
        result = {
            'task_id': task.pk,
            'task_author': task.task_author.username,
            'task_status': task.status.name,
            'task_maker': task.task_maker.username,
            'comments': [comment.comment for comment in comments],
            'descriptions': [description.text for description in descriptions]
        }
        task_results.append(result)
    return JsonResponse(task_results, safe=False)


def create_task(request):
    post_params = json.loads(request.body)
    if not post_params.get('name'):
        return HttpResponseBadRequest('Error: there is no task name in post params')
    create_dict = {}
    for key, model, field in (
            ('task_maker', User, 'pk'),
            ('task_author', User, 'pk'),
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
    param = int(params[key]) if field == 'pk' else params[key]
    query = {field: param}
    try:
        param = model.objects.get(**query)
    except ObjectDoesNotExist:
        param = None
    return param


def add_comment(request, task_id):
    if request.method != 'POST':
        return HttpResponseBadRequest('Error: wrong HTTP method')
    text = json.loads(request.body).get('comment')
    if not text:
        return HttpResponseBadRequest('Error: there is no comment in post params')
    try:
        task = Task.objects.get(pk=int(task_id))
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('Error: there is no task with id {}'.format(task_id))
    comment = Comment(comment=text, task=task, author=task.task_maker)
    comment.save()
    return HttpResponse(status=201)
