# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-11 17:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crml_api', '0018_auto_20181010_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='pullrequest',
            name='pr_time',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
