# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.models import User
from django.test import TestCase, Client

from .models import Project, Task, Status


class TestAPI(TestCase):

    client = Client()

    def test_get_tasks(self):
        """Test getting all tasks."""
        response = self.client.get('/api/v1/tasks/')
        self.assertEqual(response.status_code, 200)

    def test_get_tasks_with_params(self):
        """Test getting filtered tasks according to params."""
        project = Project.objects.create(name='test_project_0')
        status = Status.objects.create(name='review')
        task_maker = User.objects.create(username='Roman')
        task_author = User.objects.create(username='Alex')
        task = Task(name='test_a', project=project, status=status, task_maker=task_maker, task_author=task_author)
        task.save()
        response = self.client.get('/api/v1/tasks/?status=review&task_maker=Roman&task_author=Alex')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_get_task_info(self):
        """Test updating task."""
        project = Project.objects.create(name='test_project_1')
        status = Status.objects.create(name='ready')
        task_maker = User.objects.create(username='Arseniy')
        task_author = User.objects.create(username='Alex')
        task = Task(name='test_s', project=project, status=status, task_maker=task_maker, task_author=task_author)
        task.save()
        response = self.client.get('/api/v1/tasks/1/')
        self.assertEqual(response.status_code, 200)

    def test_get_task_info_error(self):
        """Test getting task info return error response."""
        response = self.client.get('/api/v1/tasks/1/')
        self.assertEqual(response.status_code, 400)

    def test_update_task(self):
        """Test updating task."""
        project = Project.objects.create(name='test_project_2')
        status = Status.objects.create(name='ready for dev')
        task_maker = User.objects.create(username='Alla')
        task_author = User.objects.create(username='Jane')
        task = Task(name='test_f', project=project, status=status, task_maker=task_maker, task_author=task_author)
        task.save()
        response = self.client.put('/api/v1/tasks/1/', data='{"status": "dev"}')
        self.assertEqual(response.status_code, 201)

    def test_update_task_error(self):
        """Test updating task return error response."""
        response = self.client.put('/api/v1/tasks/1/', data='{"status": "dev"}')
        self.assertEqual(response.status_code, 400)

    def test_delete_task(self):
        """Test deleting task."""
        project = Project.objects.create(name='test_project_3')
        status = Status.objects.create(name='test')
        task_maker = User.objects.create(username='Enny')
        task_author = User.objects.create(username='Edgar')
        task = Task(name='test_d', project=project, status=status, task_maker=task_maker, task_author=task_author)
        task.save()
        response = self.client.delete('/api/v1/tasks/1/')
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        """Test creating task."""
        Project.objects.create(name='test_project_4')
        Status.objects.create(name='review')
        User.objects.create(username='Anna')
        User.objects.create(username='Elena')
        response = self.client.post(
            '/api/v1/tasks/',
            data=json.dumps({
                'status': 'review',
                'name': 't1',
                'task_maker': 'Anna',
                'task_author': 'Elena',
                'project': 'test_project_4'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    def test_create_task_error(self):
        """Test creating task return error response."""
        Project.objects.create(name='test_project_4')
        Status.objects.create(name='review')
        User.objects.create(username='Anna')
        User.objects.create(username='Elena')
        response = self.client.post(
            '/api/v1/tasks/',
            data=json.dumps({
                'status': 'review',
                'task_maker': 'Anna',
                'task_author': 'Elena',
                'project': 'test_project_4'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_add_comment(self):
        """Test adding comment."""
        project = Project.objects.create(name='test_project_5')
        status = Status.objects.create(name='done')
        task_maker = User.objects.create(username='Any')
        task_author = User.objects.create(username='Rick')
        task = Task(name='test_d', project=project, status=status, task_maker=task_maker, task_author=task_author)
        task.save()
        response = self.client.post(
            '/api/v1/tasks/1/comments/',
            data=json.dumps({'comment': 'my_comment'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    def test_add_comment_error(self):
        """Test adding comment with wrong task_id."""
        response = self.client.post(
            '/api/v1/tasks/1/comments/',
            data=json.dumps({'comment': 'my_comment'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
