# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-01 05:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crml_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discussion',
            name='pr',
        ),
        migrations.RemoveField(
            model_name='discussion',
            name='predicted',
        ),
        migrations.RemoveField(
            model_name='discussion',
            name='tag',
        ),
        migrations.DeleteModel(
            name='Discussion',
        ),
        migrations.DeleteModel(
            name='DiscussionTag',
        ),
        migrations.DeleteModel(
            name='PullRequest',
        ),
    ]
