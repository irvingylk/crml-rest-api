# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-15 03:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crml_api', '0020_auto_20181012_0824'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='f1',
            field=models.DecimalField(decimal_places=3, default=None, max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='project',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
