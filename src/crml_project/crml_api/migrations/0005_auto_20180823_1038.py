# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-23 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crml_api', '0004_auto_20180823_0805'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance_m1',
            name='sl_f1',
            field=models.DecimalField(decimal_places=3, default=None, max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='performance_m2',
            name='sl_f1',
            field=models.DecimalField(decimal_places=3, default=None, max_digits=4, null=True),
        ),
    ]
