# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-05 08:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crml_api', '0002_review_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='reviewed_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]