# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-12 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crml_api', '0009_auto_20180906_1236'),
    ]

    operations = [
        migrations.RenameField(
            model_name='performance_m2',
            old_name='avg_f1',
            new_name='avg_avg_f1s',
        ),
        migrations.RenameField(
            model_name='performance_m2',
            old_name='ck_f1',
            new_name='lower_extreme',
        ),
        migrations.RenameField(
            model_name='performance_m2',
            old_name='tx_f1',
            new_name='ts_f1',
        ),
        migrations.RenameField(
            model_name='performance_m2',
            old_name='it_f1',
            new_name='upper_extreme',
        ),
        migrations.RenameField(
            model_name='performance_m2',
            old_name='ld_f1',
            new_name='upper_quartile',
        ),
        migrations.RemoveField(
            model_name='performance_m2',
            name='rs_f1',
        ),
        migrations.RemoveField(
            model_name='performance_m2',
            name='sl_f1',
        ),
        migrations.RemoveField(
            model_name='performance_m2',
            name='sp_f1',
        ),
        migrations.RemoveField(
            model_name='performance_m2',
            name='tr_f1',
        ),
        migrations.RemoveField(
            model_name='performance_m2',
            name='vr_f1',
        ),
        migrations.AddField(
            model_name='performance_m2',
            name='lower_quartile',
            field=models.DecimalField(decimal_places=3, default=None, max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='performance_m2',
            name='median',
            field=models.DecimalField(decimal_places=3, default=None, max_digits=4, null=True),
        ),
    ]
