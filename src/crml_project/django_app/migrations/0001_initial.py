# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-02 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Project', models.CharField(max_length=100, null=True, verbose_name='Project')),
                ('PR', models.CharField(max_length=100, null=True, verbose_name='PR')),
                ('CommitHash', models.CharField(max_length=100, null=True, verbose_name='CommitHash')),
                ('Prob', models.FloatField(null=True, verbose_name='Prob')),
                ('Reason', models.CharField(max_length=255, null=True, verbose_name='Reason')),
                ('Date', models.DateField(null=True, verbose_name='Date')),
            ],
        ),
        migrations.CreateModel(
            name='Pr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.CharField(max_length=100, null=True, verbose_name='Project')),
                ('pr', models.CharField(max_length=100, null=True, verbose_name='PR')),
                ('commithash', models.CharField(max_length=100, null=True, verbose_name='CommitHash')),
                ('date', models.DateField(null=True, verbose_name='Date')),
            ],
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Project', models.CharField(max_length=100, null=True, verbose_name='Project')),
                ('File', models.CharField(max_length=100, null=True, verbose_name='File')),
                ('Prob', models.FloatField(null=True, verbose_name='Prob')),
                ('Reason', models.CharField(max_length=255, null=True, verbose_name='Reason')),
                ('Release', models.CharField(max_length=100, null=True, verbose_name='Release')),
                ('Date', models.DateField(null=True, verbose_name='Date')),
                ('COMM', models.FloatField(null=True, verbose_name='COMM')),
                ('ADEV', models.FloatField(null=True, verbose_name='ADEV')),
                ('DDEV', models.FloatField(null=True, verbose_name='DDEV')),
                ('ADD', models.FloatField(null=True, verbose_name='ADD')),
                ('DEL', models.FloatField(null=True, verbose_name='DEL')),
                ('SCTR', models.FloatField(null=True, verbose_name='SCTR')),
                ('OWN', models.FloatField(null=True, verbose_name='OWN')),
                ('MINOR', models.FloatField(null=True, verbose_name='MINOR')),
                ('NCOMM', models.FloatField(null=True, verbose_name='NCOMM')),
                ('NADEV', models.FloatField(null=True, verbose_name='NADEV')),
                ('NDDEV', models.FloatField(null=True, verbose_name='NDDEV')),
                ('NSCTR', models.FloatField(null=True, verbose_name='NSCTR')),
                ('NS', models.FloatField(null=True, verbose_name='NS')),
                ('ND', models.FloatField(null=True, verbose_name='ND')),
                ('NF', models.FloatField(null=True, verbose_name='NF')),
                ('Entropy', models.FloatField(null=True, verbose_name='Entropy')),
                ('LA', models.FloatField(null=True, verbose_name='LA')),
                ('LD', models.FloatField(null=True, verbose_name='LD')),
                ('LT', models.FloatField(null=True, verbose_name='LT')),
                ('FIX', models.FloatField(null=True, verbose_name='FIX')),
                ('NDEV', models.FloatField(null=True, verbose_name='NDEV')),
                ('AGE', models.FloatField(null=True, verbose_name='AGE')),
                ('NUC', models.FloatField(null=True, verbose_name='NUC')),
                ('EXP', models.FloatField(null=True, verbose_name='EXP')),
                ('REXP', models.FloatField(null=True, verbose_name='REXP')),
                ('SEXP', models.FloatField(null=True, verbose_name='SEXP')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.CharField(max_length=100, null=True, verbose_name='Project')),
                ('pr', models.CharField(max_length=100, null=True, verbose_name='PR')),
                ('commentid', models.CharField(max_length=100, null=True, verbose_name='CommentID')),
                ('reviewmsg', models.CharField(max_length=255, null=True, verbose_name='ReviewMSG')),
                ('reviewtag', models.CharField(max_length=100, null=True, verbose_name='ReviewTag')),
                ('date', models.DateField(null=True, verbose_name='Date')),
            ],
        ),
    ]