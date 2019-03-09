import re
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse

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