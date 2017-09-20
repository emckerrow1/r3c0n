# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from models import Post
from models import Metrics
from models import Metric_Count

from forms import AddArticleForm

import re

# Create your views here.
def home(request):
    #_create_metrics(request, 'home')
    if request.user.is_superuser:
        posts = Post.objects.all()
        if request.method == 'POST':
            if 'Publish' in request.POST:
                post = Post.objects.get(id=request.POST['Publish'])
                post.publish()
    else:
        posts = Post.objects.filter(published_date__isnull=False)

    all_posts = _get_all_post()
    return render(request, 'home.html', {
        'all_posts':all_posts,
        'posts':posts,
    })

def article(request, year, month, file_name):
    file_name = year+'/'+month+'/'+file_name+'.html'
    post = Post.objects.get(upload_file=file_name)
    #_create_metrics(request, post)
    all_posts = _get_all_post()
    return render(request, 'article.html', {
        'all_posts':all_posts,
        'post':post,
    })

@login_required(login_url="login")
def metrics(request):
    if not request.user.is_superuser:
        return HttpResponse(status=404)
    metrics = Metrics.objects.all()
    all_posts = _get_all_post()
    return render(request, 'metrics.html', {
        'all_posts':all_posts,
        'metrics':metrics,
    })

@login_required(login_url="login")
def add_article(request):
    if not request.user.is_superuser:
        return HttpResponse(status=404)

    form = AddArticleForm()
    if request.method == 'POST':
        form = AddArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    all_posts = _get_all_post()
    return render(request, 'add_article.html', {
        'all_posts':all_posts,
        'form':form,
    })

# command functions

def _get_all_post():
    posts = Post.objects.filter(published_date__isnull=False)
    all_posts = {}
    for post in posts:
        post_url = post.upload_file.url.split("/")
        if post_url[2] in all_posts:
            if post_url[3] in all_posts[post_url[2]]:
                all_posts[post_url[2]][post_url[3]].append({post.title: "/article/"+ post.upload_file.url.lstrip('/media').rstrip('.html') })
            else:
                all_posts[post_url[2]][post_url[3]]= [{post.title: "/article/"+ post.upload_file.url.lstrip('/media').rstrip('.html') }]
        else:
            all_posts[post_url[2]] = { post_url[3]: [{post.title: "/article/"+ post.upload_file.url.lstrip('/media').rstrip('.html') }] }

    return all_posts

def _get_client_ip(request):  
    ip = None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
        return ip

def _create_metrics(request, page):
    ip = _get_client_ip(request)
    if ip:
        if page == 'home':
            metric, created = Metrics.objects.get_or_create(ip=ip)
            metric.home_count += 1 
            metric.save()
        else:
            metric, created = Metrics.objects.get_or_create(ip=ip)
            metric_count, created = Metric_Count.objects.get_or_create(post=page, ip=metric)
            if not created:
                metric_count.visit_count += 1 
                metric_count.save()

