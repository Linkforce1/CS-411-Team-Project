import re
import crypt
from django.shortcuts import render, redirect
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django import forms
from django.http import HttpResponseRedirect
from main.serializers import UsersSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from main.models import Users, Rooms

LOGIN_COOKIE = 'music_party_logged_in'

class login_form(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='password', max_length=100)

class delete_form(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='password', max_length=100)
    room_name = forms.CharField(label='room_name', max_length=100)

class update_form(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='password', max_length=100)
    room_name = forms.CharField(label='room_name', max_length=100)
    new_room_name = forms.CharField(label='new_room_name', max_length=100)

class room_search_form(forms.Form):
    search = forms.CharField(label='search', max_length=100)

class sign_up_form(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    nickname = forms.CharField(label='Nickname', max_length=100)
    password = forms.CharField(label='password', max_length=100)
    confirm_password = forms.CharField(label='confirm password', max_length=100)

class room_form(forms.Form):
    room_name = forms.CharField(label='room_name', max_length=100)
    private = forms.BooleanField()
    duration = forms.IntegerField()

def login_check(login_stat, user_id):
    this = Users.objects.filter(ID = user_id)
    if this.first():
        if login_stat and login_stat == crypt.crypt(this.first().Email, 'abc'):
            return 1
    return 0;


def home(request):
    return HttpResponseRedirect('/welcome');

def user_home(request, user_id):
    if not login_check(request.COOKIES.get(LOGIN_COOKIE, None), user_id):
        return HttpResponseRedirect('/welcome');
    # return HttpResponse(Users.objects.get(ID=user_id).Nickname)
    return render(
        request,
        'home.html', {'user': Users.objects.get(ID=user_id)}
    )

def create(request, user_id):
    if not login_check(request.COOKIES.get(LOGIN_COOKIE, None), user_id):
        return HttpResponseRedirect('/welcome');
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
            room = Rooms(idRoomNumber = Rooms.room_counter, RoomName = room_name, Access = 'public', Host = '???')
            room.save()
            return redirect('user_home', user_id=user_id)
            return JsonResponse(form.data, status=201)
    else:
        form = room_form()
    return render(
        request,
        'create.html', {'form': form, 'id': user_id}
    )

def delete(request):
    form = delete_form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            room_name = request.POST.get('room_name')
            res = Users.objects.filter(Email = email).filter(Password = password)
            if res:
                pending_rooms = Rooms.objects.filter(RoomName = room_name)
                if pending_rooms.first() and pending_rooms.first().Host == res.first().Nickname:
                    pending_rooms.first().delete()
            return HttpResponse("Done")
    else:
        form = delete_form()
    return render(
        request,
        'delete.html', {'form': form}
    )

def public_rooms(request):
    rooms = Rooms.objects.filter(Access='public').order_by('RoomName')
    return render(request,
                'public_rooms.html',
                {'rooms': rooms}
    )
def update(request):
    form = update_form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            room_name = request.POST.get('room_name')
            new_room_name = request.POST.get('new_room_name')
            res = Users.objects.filter(Email = email).filter(Password = password)
            if res:
                pending_rooms = Rooms.objects.filter(RoomName = room_name)
                if pending_rooms.first() and pending_rooms.first().Host == res.first().Nickname:
                    pending_rooms.update(RoomName=new_room_name)
            return HttpResponse("Done")
    else:
        form = update_form()
    return render(
        request,
        'update.html', {'form': form}
    )

def join(request):
    form = room_search_form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            room_name = request.POST.get('search')
            print(room_name)
            res = Rooms.objects.filter(RoomName = room_name)
            return render(
                request,
                    'res.html', {'res':res}
            )
    else:
        form = room_search_form()
    return render(
        request,
        'join.html', {'form':form }
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
                    response = render(
                        request,
                        'home.html', {'user': user}
                    )
                     # redirect('user_home', user_id=user.ID)
                    response.set_cookie(LOGIN_COOKIE, crypt.crypt(email, 'abc'))
                    return response
                else:
                    return HttpResponse("Password is incorrect.")
            else:
                return HttpResponse("Email is invalid.")

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

def profile(request, user_id):
    if not login_check(request.COOKIES.get(LOGIN_COOKIE, None), user_id):
        return HttpResponseRedirect('/welcome');
    d = {
        'user': Users.objects.get(ID=user_id),
        'users': Users.objects.all(),
        'rooms': Rooms.objects.all(),
    }
    return render(request, 'profile.html', d)


def party(request):
    return render(request, 'party.html')
