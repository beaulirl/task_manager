# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-19 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0003_auto_20180719_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.IntegerField(choices=[(0, 'ready_for_dev'), (1, 'review'), (2, 'test'), (3, 'ready_for_deployment'), (4, 'done')]),
        ),
    ]
