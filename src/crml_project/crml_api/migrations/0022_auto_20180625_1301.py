# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-25 13:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crml_api', '0021_auto_20180625_1257'),
    ]

    operations = [
        migrations.RenameField(
            model_name='performance',
            old_name='algorithmn',
            new_name='algorithm',
        ),
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together=set([('algorithm', 'size')]),
        ),
    ]