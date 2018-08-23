# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-21 16:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crml_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Training_m1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(max_length=500)),
                ('value', models.PositiveIntegerField()),
                ('reviewId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crml_api.Review')),
            ],
        ),
        migrations.CreateModel(
            name='Training_m2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(max_length=500)),
                ('value', models.PositiveIntegerField()),
                ('reviewId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crml_api.Review')),
            ],
        ),
        migrations.CreateModel(
            name='Training_m3',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(max_length=500)),
                ('value', models.BooleanField(default=False)),
                ('reviewId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crml_api.Review')),
            ],
        ),
        migrations.CreateModel(
            name='Training_m4',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(max_length=500)),
                ('value', models.BooleanField(default=False)),
                ('reviewId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crml_api.Review')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='training_m4',
            unique_together=set([('reviewId', 'feature')]),
        ),
        migrations.AlterUniqueTogether(
            name='training_m3',
            unique_together=set([('reviewId', 'feature')]),
        ),
        migrations.AlterUniqueTogether(
            name='training_m2',
            unique_together=set([('reviewId', 'feature')]),
        ),
        migrations.AlterUniqueTogether(
            name='training_m1',
            unique_together=set([('reviewId', 'feature')]),
        ),
    ]
