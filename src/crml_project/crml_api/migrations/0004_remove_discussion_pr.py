# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-01 05:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crml_api', '0003_auto_20181001_0546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discussion',
            name='pr',
        ),
    ]