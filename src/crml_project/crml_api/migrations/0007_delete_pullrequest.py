# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-02 07:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crml_api', '0006_auto_20181002_0703'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PullRequest',
        ),
    ]
