import re
from django.shortcuts import render, redirect
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django import forms
from django.http import HttpResponseRedirect
from main.serializers import UsersSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from main.models import Users, Rooms, Guest
from django.contrib import messages

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

class room_search_form(forms.Form):
    search = forms.CharField(label='search', max_length=100)

def home(request):
    return HttpResponseRedirect('/welcome');

def user_home(request, user_id):
    return render(
        request,
        'home.html', {'user': Users.objects.get(ID=user_id)}
    )

def profile(request, user_id):
    d = {
        'user': Users.objects.get(ID=user_id),
        'users': Users.objects.all(),
        'rooms': Rooms.objects.all(),
        'guests': Guest.objects.all(),
    }
    return render(request, 'profile.html', d)


def yourRooms(request, user_id):
    user = Users.objects.get(ID=user_id)
    rooms = []
    for guest in Guest.objects.filter(User=user):
        rooms.append(guest.Room)
    hostRooms = Rooms.objects.filter(Host=user.Nickname)
    return render(
        request,
        'yourRooms.html', {'rooms': rooms, 'hostRooms': hostRooms, 'user': user}
    )

def create(request, user_id):
    form = room_form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            if not Rooms.room_counter:
                Rooms.room_counter = 1
            else:
                Rooms.room_counter += 1
            room_name = request.POST.get('room_name')
            private = request.POST.get('private')
            duration = request.POST.get('duration')
            host = Users.objects.get(ID=user_id).Nickname
            room = Rooms(idRoomNumber = Rooms.room_counter, RoomName = room_name, Access = '??', Host = host)
            room.save()
            return redirect('user_home', user_id=user_id)
            # return JsonResponse(form.data, status=201)
    else:
        form = room_form()
    return render(
        request,
        'create.html', {'form': form, 'id': user_id}
    )

def join(request, user_id):
    form = room_search_form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            room_name = request.POST.get('search')
            rooms = Rooms.objects.filter(RoomName__contains = room_name)
            return render(
                request,
                'res.html',
                {'rooms':rooms, 'user_id': user_id}
            )
    else:
        form = room_search_form()
    return render(
        request,
        'join.html', {'form':form, 'user_id': user_id}
    )

def addGuest(request, room_id, user_id):
    room = Rooms.objects.get(idRoomNumber=room_id)
    user = Users.objects.get(ID=user_id)
    if Guest.objects.filter(Room=room, User=user).exists():
        return redirect('party', room_id=room_id, user_id=user_id)
    else:
        guest = Guest(User = user, Room = room)
        guest.save()
        return redirect('party', room_id=room_id, user_id=user_id)

        
def party(request, room_id, user_id):
    room = Rooms.objects.get(idRoomNumber = room_id)
    d = {
        'user': Users.objects.get(ID=user_id),
        'room': room,
        'guests': Guest.objects.filter(Room = room),
    }
    return render(request, 'party.html', d)


def public_rooms(request):
    rooms = Rooms.objects.filter(Access='public').order_by('RoomName')
    return render(request,
                'public_rooms.html',
                {'rooms': rooms}
    )

def login(request):
    form = login_form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')

            # check if the login is valid or not
            if Users.objects.filter(Email=email).exists():
                user = Users.objects.get(Email=email)
                if user.Password == password:
                    return redirect('user_home', user_id=user.ID)
                else:
                    messages.error(request,'Password is incorrect.')
                   # return redirect('login')
                   # return HttpResponse("Password is incorrect.")
            else:
                messages.error(request,'Email does not exist.')
              #  return HttpResponse("Email is invalid.")

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
            if not Users.user_counter:
                Users.user_counter = 1
            else:
                Users.user_counter += 1
            email = request.POST.get('email')
            nickname = request.POST.get('nickname')
            password = request.POST.get('password')
            person = Users(ID = Users.user_counter, Email = email, Nickname = nickname, Password = password)
            person.save()
            #serializer.save()
            # return JsonResponse(form.data,status=201)
            return redirect('welcome')
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
