# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-04 12:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crml_api', '0022_auto_20180501_2302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewed',
            name='reviewId',
        ),
        migrations.RemoveField(
            model_name='reviewtag',
            name='reviewId',
        ),
        migrations.RemoveField(
            model_name='reviewtag',
            name='tag',
        ),
        migrations.AddField(
            model_name='review',
            name='reviewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='review',
            name='tag',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='crml_api.Tag'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='reviewId',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='Reviewed',
        ),
        migrations.DeleteModel(
            name='ReviewTag',
        ),
    ]
