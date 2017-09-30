"""r3c0n_infosec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.views import static
from django.conf.urls import url
from django.contrib import admin
from blog import views
from blog import forms
from r3c0n_infosec import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^admin/$', auth_views.login, {"template_name": "admin_panel.html",
                                       "authentication_form": forms.LoginForm,
                                       },name="login"),
    url(r'^logout/$', auth_views.logout, {'next_page': '/admin'}),
    url(r'^admin/metrics/$', views.metrics),
    url(r'^admin/add/$', views.add_article),
    url(r'^about/$', views.about),
    url(r'^$', views.home),
    url(r'^article/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<file_name>.*)/$', views.article),
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),

    url(r'^api/subscribe$', views.api_subscribe),
    url(r'^api/unsubscribe$', views.api_unsubscribe),
]
