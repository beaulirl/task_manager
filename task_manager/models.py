# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200, default='inner')

    def natural_key(self):
        return self.name

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=200, default='new')

    class Meta:
        verbose_name_plural = 'Statuses'

    def natural_key(self):
        return self.name

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=200, default='task')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    task_maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_maker')
    task_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_author')

    def natural_key(self):
        return self.name, self.project.name, self.status.name, self.task_maker.username, self.task_author.username

    def __str__(self):
        return self.name


class Description(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    text = models.TextField()


class Comment(models.Model):
    comment = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    def natural_key(self):
        return self.comment
