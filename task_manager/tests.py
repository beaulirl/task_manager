# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.test import TestCase, Client

from .models import Project, Task, Status, Comment


class TestAPI(TestCase):

    client = Client()

    def test_get_tasks(self):
        """Test getting all tasks."""
        project = Project.objects.create(name='test_project_get_0')
        status = Status.objects.create(name='review')
        task_maker = User.objects.create(username='Elena')
        task_author = User.objects.create(username='Anna')
        Task.objects.create(
            name='test_e',
            project=project,
            status=status,
            task_maker=task_maker,
            task_author=task_author
        )
        project_1 = Project.objects.create(name='test_project_get_1')
        status_1 = Status.objects.create(name='done')
        task_maker_1 = User.objects.create(username='Alex')
        task_author_1 = User.objects.create(username='Roman')
        Task.objects.create(name='test_d', project=project_1, status=status_1, task_maker=task_maker_1,
                            task_author=task_author_1)

        response = self.client.get('/api/v1/tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 2)

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

    def test_get_tasks_with_wrong_params(self):
        """Test getting filtered tasks according to params."""
        project = Project.objects.create(name='test_project_0')
        status = Status.objects.create(name='review')
        task_maker = User.objects.create(username='Roman')
        task_author = User.objects.create(username='Alex')
        Task.objects.create(
            name='test_a',
            project=project,
            status=status,
            task_maker=task_maker,
            task_author=task_author
        )
        response = self.client.get('/api/v1/tasks/?wrong_status=review&wrong_task_maker=Roman&wrong_task_author=Alex')
        self.assertEqual(response.content, 'Error: wrong get params')
        self.assertEqual(response.status_code, 400)

    def test_get_task_info(self):
        """Test getting task info by id."""
        project = Project.objects.create(name='test_project_1')
        status = Status.objects.create(name='ready')
        task_maker = User.objects.create(username='Arseniy')
        task_author = User.objects.create(username='Alex')
        task = Task(name='test_s', project=project, status=status, task_maker=task_maker, task_author=task_author)
        task.save()
        response = self.client.get('/api/v1/tasks/1/', content_type='application/json')
        self.assertEqual(json.loads(response.content)['task_id'], 1)
        self.assertEqual(response.status_code, 200)

    def test_get_task_info_error(self):
        """Test getting task info return error response."""
        response = self.client.get('/api/v1/tasks/1/')
        self.assertEqual(response.content, 'Error: there is no task with id 1')
        self.assertEqual(response.status_code, 400)

    def test_update_task(self):
        """Test updating task."""
        project = Project.objects.create(name='test_project_2')
        status = Status.objects.create(name='ready for dev')
        task_maker = User.objects.create(username='Alla')
        task_author = User.objects.create(username='Jane')
        Task.objects.create(
            name='test_f',
            project=project,
            status=status,
            task_maker=task_maker,
            task_author=task_author
        )
        updated_status = Status.objects.create(name='dev')
        response = self.client.put(
            '/api/v1/tasks/1/',
            data=json.dumps({'status': 'dev'}),
            content_type='application/json'
        )
        updated_task = Task.objects.get(pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_task.status, updated_status)

    def test_update_task_error(self):
        """Test updating task return error response if there is no such task_id."""
        response = self.client.put(
            '/api/v1/tasks/1/',
            data=json.dumps({'status': 'dev'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_update_task_error_value(self):
        """Test updating task return error response if there is no such updated fields."""
        project = Project.objects.create(name='test_project_2')
        status = Status.objects.create(name='ready for dev')
        task_maker = User.objects.create(username='Alla')
        task_author = User.objects.create(username='Jane')
        Task.objects.create(name='test_f', project=project, status=status, task_maker=task_maker,
                            task_author=task_author)
        response = self.client.put(
            '/api/v1/tasks/1/',
            data=json.dumps({'status': 'dev'}),
            content_type='application/json'
        )
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
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(pk=1)
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
                'task_maker': '1',
                'task_author': '2',
                'project': 'test_project_4'
            }),
            content_type='application/json'
        )
        task = Task.objects.get(name='t1')
        self.assertEqual(task.name, 't1')
        self.assertEqual(response.status_code, 201)

    def test_create_task_error(self):
        """Test creating task return error response if there is no task name in post data."""
        Project.objects.create(name='test_project_4')
        Status.objects.create(name='review')
        User.objects.create(username='Anna')
        User.objects.create(username='Elena')
        response = self.client.post(
            '/api/v1/tasks/',
            data=json.dumps({
                'status': 'review',
                'task_maker': '1',
                'task_author': '2',
                'project': 'test_project_4'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.content, 'Error: there is no task name in post params')
        self.assertEqual(response.status_code, 400)

    def test_create_task_error_value(self):
        """Test creating task return error response if there is no such status."""
        Project.objects.create(name='test_project_4')
        User.objects.create(username='Anna')
        User.objects.create(username='Elena')
        response = self.client.post(
            '/api/v1/tasks/',
            data=json.dumps({
                'status': 'review',
                'name': 'task_5',
                'task_maker': '1',
                'task_author': '2',
                'project': 'test_project_4'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.content, 'Error: there is no status with such name')
        self.assertEqual(response.status_code, 400)

    def test_create_task_error_post_param(self):
        """Test creating task return error response if there is no task_maker in post params."""
        Project.objects.create(name='test_project_4')
        User.objects.create(username='Anna')
        User.objects.create(username='Elena')
        response = self.client.post(
            '/api/v1/tasks/',
            data=json.dumps({
                'status': 'review',
                'name': 'task_5',
                'task_author': '2',
                'project': 'test_project_4'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.content, 'Error: no such field task_maker in post params')
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
        comment = Comment.objects.get(task__pk=1)
        self.assertEqual(comment.task.name, 'test_d')
        self.assertEqual(response.status_code, 201)

    def test_add_comment_param_error(self):
        """Test adding comment."""
        project = Project.objects.create(name='test_project_5')
        status = Status.objects.create(name='done')
        task_maker = User.objects.create(username='Any')
        task_author = User.objects.create(username='Rick')
        task = Task(name='test_d', project=project, status=status, task_maker=task_maker, task_author=task_author)
        task.save()
        response = self.client.post(
            '/api/v1/tasks/1/comments/',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.content, 'Error: there is no comment in post params')
        self.assertEqual(response.status_code, 400)

    def test_add_comment_error(self):
        """Test adding comment with wrong task_id."""
        response = self.client.post(
            '/api/v1/tasks/1/comments/',
            data=json.dumps({'comment': 'my_comment'}),
            content_type='application/json'
        )
        self.assertEqual(response.content, 'Error: there is no task with id 1')
        self.assertEqual(response.status_code, 400)

    def test_add_comment_error_method(self):
        """Test adding comment with wrong HTTP method."""
        response = self.client.get(
            '/api/v1/tasks/1/comments/'
        )
        self.assertEqual(response.content, 'Error: wrong HTTP method')
        self.assertEqual(response.status_code, 400)
