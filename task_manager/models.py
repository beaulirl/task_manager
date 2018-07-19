# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

STATUS = (
    (0, 'ready_for_dev'),
    (1, 'review'),
    (2, 'test'),
    (3, 'ready_for_deployment'),
    (4, 'done'),
)


class Project(models.Model):
    name = models.CharField(max_length=200)


class Status(models.Model):
    name = models.IntegerField(choices=STATUS)


class Task(models.Model):
    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    task_maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_maker')
    task_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_author')


class Description(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    text = models.TextField()


class TaskComment(models.Model):
    comment = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
