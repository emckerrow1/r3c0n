# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-19 08:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Metric_Count',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Metrics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_count', models.IntegerField(default=0)),
                ('ip', models.CharField(max_length=15, unique=True)),
                ('count', models.ManyToManyField(through='blog.Metric_Count', to='blog.Post')),
            ],
        ),
        migrations.AddField(
            model_name='metric_count',
            name='ip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Metrics'),
        ),
        migrations.AddField(
            model_name='metric_count',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post'),
        ),
    ]
