# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-15 03:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crml_api', '0021_auto_20181015_0342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='algorithm',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='avg_avg_f1s',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='avg_lg_f1',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='avg_og_f1',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='avg_ot_f1',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='avg_pc_f1',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='avg_sa_f1',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='avg_ts_f1',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='evaluation_method',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='extraction_method',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='lower_extreme',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='lower_quartile',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='median',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='testing_size',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='upper_extreme',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='upper_quartile',
        ),
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together=set([('project', 'training_size')]),
        ),
    ]