# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-30 18:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crml_api', '0013_auto_20180501_0344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='code_content',
            field=models.CharField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='image',
            name='image_alt',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='image',
            name='image_src',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='issue',
            name='issue_content',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='link',
            name='link_content',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='people',
            name='people_content',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='review',
            name='reviewId',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_content',
            field=models.CharField(max_length=5000),
        ),
    ]