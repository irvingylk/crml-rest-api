# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-05 06:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crml_api', '0013_commit'),
    ]

    operations = [
        migrations.AddField(
            model_name='commit',
            name='project',
            field=models.CharField(default='django/django', max_length=50),
            preserve_default=False,
        ),
    ]
