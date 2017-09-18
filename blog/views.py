# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from models import Post

# Create your views here.
def home(request):
    posts = Post.objects.all()
    all_posts = _get_all_post()
    return render(request, 'home.html', {
        'all_posts':all_posts,
        'posts':posts,
    })

def article(request, year, month, file_name):
    file_name = year+'/'+month+'/'+file_name+'.html'
    post = Post.objects.get(upload_file=file_name)
    all_posts = _get_all_post()
    return render(request, 'article.html', {
        'all_posts':all_posts,
        'post':post,
    })

def _get_all_post():
	posts = Post.objects.all()
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
