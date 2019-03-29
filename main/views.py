import re
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django import forms
from django.http import HttpResponseRedirect, Http404
from main.serializers import UsersSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from main.models import Users, Rooms
class login_form(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='password', max_length=100)

class sign_up_form(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    nickname = forms.CharField(label='Nickname', max_length=100)
    password = forms.CharField(label='password', max_length=100)
    confirm_password = forms.CharField(label='confirm password', max_length=100)

class room_form(forms.Form):
    room_name = forms.CharField(label='room_name', max_length=100)
    private = forms.BooleanField()
    duration = forms.IntegerField()

def home(request):
    return HttpResponseRedirect("/welcome")

def user_home(request):

    return render(
        request,
        'home.html'
    )

def create(request):
    form = room_form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            if not Rooms.room_counter:
                Rooms.room_counter = 1
            else:
                Rooms.room_counter += 1
            room_name = request.POST.get('room_name')
            private = request.POST.get('private')
            if private=='on':
                private='private'
            else:
                private = 'public'
            #duration = request.POST.get('duration')
            room = Rooms(idRoomNumber = Rooms.room_counter, RoomName = room_name, Access = private, Host = '???')
            room.save()
            return JsonResponse(form.data, status=201)
    else:
        form = room_form()
    return render(
        request,
        'create.html', {'form': form}
    )

def login(request):
    form = login_form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            auth_user = Users.objects.filter(Email=email).filter(Password=password)
            if not auth_user:
                raise Http404("This is not a valid username or password. Please try again")
            else:    
                return HttpResponseRedirect('/user_home')
    else:
        form = login_form()
    return render(
        request,
        'login.html', {'form':form}
    )

def signup(request):
    form = sign_up_form(request.POST or None)
    #serializer = UsersSerializer(data = form)
    if request.method == 'POST':
        #data = request.POST.copy()
        #serializer = UsersSerializer(data = data)
        if form.is_valid():
            email = request.POST.get('email')
            nickname = request.POST.get('nickname')
            password = request.POST.get('password')
            person = Users(Email = email, Nickname = nickname, Password = password)
            person.save()
            #serializer.save()
            return JsonResponse(form.data,status=201)
    else:
        form = sign_up_form()
        #return JsonResponse(form.errors, status=400)
    return render(
        request,
        'signup.html', {'form':form}
    )

def welcome(request):
    return render(
        request,
        'welcome.html'
    )

def profile(request):
    return render(request, 'profile.html')
    
