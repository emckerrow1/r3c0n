from django.contrib.auth.forms import AuthenticationForm
from django import forms
from models import Post

class LoginForm(AuthenticationForm):
	username = forms.CharField(label="Username", max_length=30, 
							   widget=forms.TextInput(attrs={'class': 'form-control',
							   								 'name': 'username'}))
	password = forms.CharField(label="Password", max_length=30, 
							   widget=forms.PasswordInput(attrs={'class': 'form-control',
							   									 'name': 'password'}))

class AddArticleForm(forms.ModelForm):
	class Meta:
		model = Post
		exclude = ['created_date', 'published_date']

	def __init__(self, *args, **kwargs):		
		super(AddArticleForm, self).__init__(*args, **kwargs)