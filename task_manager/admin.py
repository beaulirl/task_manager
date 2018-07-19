# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Project, Description, TaskComment, Task, Status

admin.site.register(Project)
admin.site.register(Description)
admin.site.register(TaskComment)
admin.site.register(Task)
admin.site.register(Status)

