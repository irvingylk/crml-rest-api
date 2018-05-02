# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-30 12:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crml_api', '0009_auto_20180430_2034'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
            ],
        ),
        migrations.RemoveField(
            model_name='code',
            name='code_content',
        ),
        migrations.AlterField(
            model_name='code',
            name='reviewId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crml_api.Review'),
        ),
        migrations.AddField(
            model_name='code',
            name='codeContents',
            field=models.ManyToManyField(to='crml_api.CodeContent'),
        ),
    ]