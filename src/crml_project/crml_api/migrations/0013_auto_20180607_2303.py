# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-07 13:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crml_api', '0012_auto_20180607_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='predicted',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='reviews_predicted', to='crml_api.Tag'),
        ),
    ]