# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-13 03:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crml_api', '0012_auto_20180912_1622'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='performance_m1',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='performance_m1',
            name='algorithm',
        ),
        migrations.DeleteModel(
            name='Performance_m1',
        ),
    ]
