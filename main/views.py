import re
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from django import forms
from django.http import HttpResponseRedirect
class login_form(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='password', max_length=100)

class sign_up_form(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    user_name = forms.CharField(label='User name', max_length=100)
    password = forms.CharField(label='password', max_length=100)
    confirm_password = forms.CharField(label='confirm password', max_length=100)

def home(request):
    return HttpResponse("Hello, Django!")

def hello_there(request, name):
    return render(
        request,
        'hello/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

def hello_world(request):
    return HttpResponse("Hello World!, this is my first Web Appliction!")

def login(request):
    if request.method == 'POST':
        form = login_form(request.POST)
        if form.is_valid():
            return HttpResponse('Done!')
    else:
        form = login_form()
    return render(
        request,
        'login.html', {'form':form}
    )

def signup(request):
    if request.method == 'POST':
        form = sign_up_form(request.POST)
        if form.is_valid():
            return HttpResponse('Done!')
    else:
        form = sign_up_form()
    return render(
        request,
        'login.html', {'form':form}
    )

def welcome(request):
    return render(
        request,
        'welcome.html'
    )
