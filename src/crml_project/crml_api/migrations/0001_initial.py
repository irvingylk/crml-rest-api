# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-01 05:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_content', models.CharField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('discussion_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('content', models.CharField(default='', max_length=5000)),
                ('content_length', models.IntegerField(default=0)),
                ('is_inline_discussion', models.BooleanField(default=False)),
                ('reviewed', models.BooleanField(default=False)),
                ('creation_time', models.DateTimeField()),
                ('reviewed_time', models.DateTimeField(default=None, null=True)),
                ('project', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DiscussionTag',
            fields=[
                ('tag_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=100)),
                ('project', models.CharField(max_length=100)),
                ('file_path', models.FilePathField(max_length=200, path='(\\/[a-zA-Z0-9]+)*')),
                ('prob', models.DecimalField(decimal_places=3, max_digits=4)),
                ('reason', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_src', models.CharField(max_length=1000)),
                ('image_alt', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_content', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_content', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('people_content', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('algorithm', models.CharField(max_length=200)),
                ('extraction_method', models.CharField(max_length=500)),
                ('evaluation_method', models.CharField(max_length=500)),
                ('training_size', models.IntegerField()),
                ('testing_size', models.IntegerField()),
                ('avg_sa_f1', models.DecimalField(decimal_places=3, default=None, max_digits=4, null=True)),
                ('avg_og_f1', models.DecimalField(decimal_places=3, default=None, max_digits=4, null=True)),
                ('avg_ts_f1', models.DecimalField(decimal_places=3, default=None, max_digits=4, null=True)),
                ('avg_lg_f1', models.DecimalField(decimal_places=3, default=None, max_digits=4, null=True)),
                ('avg_pc_f1', models.DecimalField(decimal_places=3, default=None, max_digits=4, null=True)),
                ('avg_ot_f1', models.DecimalField(decimal_places=3, default=None, max_digits=4, null=True)),
                ('avg_avg_f1s', models.DecimalField(decimal_places=3, default=None, max_digits=4, null=True)),
                ('lower_extreme', models.DecimalField(decimal_places=3, default=None, max_digits=4, null=True)),
                ('lower_quartile', models.DecimalField(decimal_places=3, default=None, max_digits=4, null=True)),
                ('median', models.DecimalField(decimal_places=3, default=None, max_digits=4, null=True)),
                ('upper_quartile', models.DecimalField(decimal_places=3, default=None, max_digits=4, null=True)),
                ('upper_extreme', models.DecimalField(decimal_places=3, default=None, max_digits=4, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PullRequest',
            fields=[
                ('pr_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('project', models.CharField(default='', max_length=100)),
                ('commit_hash', models.CharField(default='', max_length=100)),
                ('creation_time', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('reviewId', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('review_content', models.CharField(default='', max_length=5000)),
                ('review_content_length', models.IntegerField(default=0)),
                ('is_inline_review', models.BooleanField(default=False)),
                ('extracted', models.BooleanField(default=False)),
                ('reviewed', models.BooleanField(default=False)),
                ('changed', models.BooleanField(default=False)),
                ('reviewed_time', models.DateTimeField(default=None, null=True)),
                ('project', models.CharField(default='', max_length=100)),
                ('trainings_size', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tagId', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(max_length=500)),
                ('value', models.DecimalField(decimal_places=5, max_digits=10)),
                ('reviewId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crml_api.Review')),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='predicted',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews_predicted', to='crml_api.Tag'),
        ),
        migrations.AddField(
            model_name='review',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_true', to='crml_api.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together=set([('algorithm', 'extraction_method', 'evaluation_method', 'training_size', 'testing_size')]),
        ),
        migrations.AddField(
            model_name='people',
            name='reviewId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crml_api.Review'),
        ),
        migrations.AddField(
            model_name='link',
            name='reviewId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crml_api.Review'),
        ),
        migrations.AddField(
            model_name='issue',
            name='reviewId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crml_api.Review'),
        ),
        migrations.AddField(
            model_name='image',
            name='reviewId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crml_api.Review'),
        ),
        migrations.AlterUniqueTogether(
            name='file',
            unique_together=set([('owner', 'project', 'file_path')]),
        ),
        migrations.AddField(
            model_name='discussion',
            name='pr',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='crml_api.PullRequest'),
        ),
        migrations.AddField(
            model_name='discussion',
            name='predicted',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tag_predicted', to='crml_api.DiscussionTag'),
        ),
        migrations.AddField(
            model_name='discussion',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag_true', to='crml_api.DiscussionTag'),
        ),
        migrations.AddField(
            model_name='code',
            name='reviewId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crml_api.Review'),
        ),
        migrations.AlterUniqueTogether(
            name='training',
            unique_together=set([('reviewId', 'feature')]),
        ),
    ]
