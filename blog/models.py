# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone

from validators import validate_file_extension

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    image_file = models.ImageField(default=False, upload_to='%Y/%m/')
    upload_file = models.FileField(default=False, upload_to='%Y/%m/', validators=[validate_file_extension])
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        email_subscribers(self.title, self.upload_file)
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
    visit_count = models.IntegerField(default=1)

class Subscribers(models.Model):
    email = models.CharField(max_length=200, unique=True)
    subscribed_at = models.DateTimeField(default=timezone.now)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)

    def unsubscribe(self):
        self.unsubscribed_at = timezone.now()
        self.save()

# functions
def send_email(_from, to, subject, main_msg):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = _from
    msg['To'] = to

    html = """\
    <html>
      <head></head>
      <body>
        <p>Hello, <strong>%s</strong><br><br>
        <p>%s</p> <br><br>
        <a href='r3c0n-infosec.com/?unsubscribe=true&email=%s'>Unsubscribe</a><br><br>
        All the best,<br>
        <strong>The R3c0n-Infosec Team</strong>
      </body>
    </html>
    """ % (to, main_msg, to)
    html = MIMEText(html, 'html')
    msg.attach(html)

    mail = smtplib.SMTP('smtp.mail.com', 587)
    mail.ehlo()
    mail.starttls()

    mail.login('lanemainlane@mail.com', 'milkyno1')
    mail.sendmail(_from, to, msg.as_string())
    mail.quit()

def email_subscribers(title, upload_url):
    for subscriber in Subscribers.objects.filter(unsubscribed_at__isnull=True):
        main_msg = 'Hope you are well. <br> A new blog post has been published that you may be interested in.<br> The new blog post is titled %s and can be found on at <a href="http://r3c0n-infosec.com/%s">%s</a><br><br>We are also looking for feedback, if you have any suggestions or ideas we would love to hear please get in touch.' % (title, upload_url, title)
        send_email('lanemainlane@mail.com', subscriber.email, 'R3c0n-Infosec - a new blog has been published', main_msg)
        print subscriber.email, title, upload_url
