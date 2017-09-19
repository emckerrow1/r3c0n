# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    image_file = models.ImageField(default=False, upload_to='%Y/%m/')
    upload_file = models.FileField(default=False, upload_to='%Y/%m/')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Metrics(models.Model):
    ip = models.CharField(max_length=15, unique=True)
    home_count = models.IntegerField(default=0)
    count = models.ManyToManyField(Post, through='Metric_Count')

class Metric_Count(models.Model):
    post = models.ForeignKey(Post)
    ip = models.ForeignKey(Metrics)
    count = models.IntegerField(default=1)