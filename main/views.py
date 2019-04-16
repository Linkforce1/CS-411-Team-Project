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
from django.db import connection

class login_form(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='password', max_length=100)

class sign_up_form(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    nickname = forms.CharField(label='Nickname', max_length=100)
    password = forms.CharField(label='password', max_length=100)
    confirm_password = forms.CharField(label='confirm password', max_length=100)

class update_form(forms.Form):
    GENDER_CHOICES = [
        ('male', 'male'),
        ('female', 'female'),
    ]
    gender = forms.ChoiceField(label='gender', required=False, choices=GENDER_CHOICES)
    nickname = forms.CharField(label='Nickname', required=False, max_length=100)
    new_password = forms.CharField(label='new_password', required=False, max_length=100)
    prev_password = forms.CharField(label='input the previous password', max_length=100)


class room_form(forms.Form):
    room_name = forms.CharField(label='room_name', max_length=100)
    private = forms.BooleanField(required=False)
    duration = forms.IntegerField()

class room_search_form(forms.Form):
    search = forms.CharField(label='search', max_length=100)

def home(request):
    return HttpResponseRedirect('/welcome');

def user_home(request, user_id):
    # print("test", Users.objects.get(ID=user_id))
    # cursor = connection.cursor()
    # cursor.execute("UPDATE main_users SET Phone = 1 WHERE ID = %s", [user_id])
    # cursor.execute("DELETE main_users WHERE ID = %s", )
    
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

def update(request, user_id):
    form = update_form(request.POST or None)
    if request.method == 'POST':
        #data = request.POST.copy()
        #serializer = UsersSerializer(data = data)
        if form.is_valid():
            user = Users.objects.get(ID=user_id)
            if request.POST.get('prev_password') == user.Password:
                nickname = request.POST.get('nickname')
                if nickname == "":
                    nickname = user.Nickname
                new_password = request.POST.get('new_password')
                if new_password == "":
                    new_password = user.Password
                gender = request.POST.get('gender')

                Users.objects.filter(ID=user_id).update(Nickname=nickname, Password=new_password, Gender=gender)
                return redirect('profile', user_id=user_id)
            else:
                messages.error(request,'Password is incorrect.')

    else:
        form = update_form()
        #return JsonResponse(form.errors, status=400)
    return render(
        request,
        'update.html', {'form':form, 'id': user_id}
    )


def yourRooms(request, user_id):
    # cur = connection.cursor()
    # cur.execute('SELECT * FROM main_users WHERE ID = %s', [user_id])
    # user = cur.fetchone()
    # print("test", user[3])
    for user in Users.objects.raw('SELECT * FROM main_users WHERE ID = %s', [user_id]):
    # user = Users.objects.get(ID=user_id)
        rooms = []
        # ? ? ?
        for guest in Guest.objects.filter(User=user):
            rooms.append(guest.Room)

        # test = Rooms.objects.none()
        # print(test)

        # for room in Rooms.objects.raw('SELECT * FROM main_rooms WHERE HOST = %s', [user.Nickname]):
        #     # print(room)
        #     test.add(room)
        # print(test)
        hostRooms = Rooms.objects.filter(Host=user.Nickname)
        print(hostRooms)
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

            flag = 0
            for room in Rooms.objects.raw('SELECT * FROM main_rooms WHERE RoomName = %s', [room_name]):
                flag = 1
            if flag == 1:
                messages.error(request, "Room Name already exists")

            if flag == 0:

                private = request.POST.get('private')
                if private == None:
                    access = "public"
                else:
                    access = "private"
                duration = request.POST.get('duration')


                for user in Users.objects.raw('SELECT * FROM main_users WHERE ID = %s', [user_id]):

                    # host = Users.objects.get(ID=user_id).Nickname
                    room = Rooms(idRoomNumber = Rooms.room_counter, RoomName = room_name, Access = access, Host = user.Nickname)
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

def leaveRoom(request, room_id, user_id):
    room = Rooms.objects.get(idRoomNumber=room_id)
    user = Users.objects.get(ID=user_id)
    # cursor = connection.cursor()
    # # cursor.execute("UPDATE main_users SET Phone = 1 WHERE ID = %s", [user_id])
    # cursor.execute("DELETE main_guest WHERE Room_id = %s AND User_id = %s", [room_id], [user_id])
    Guest.objects.filter(Room=room, User=user).delete()
    return redirect('user_home', user_id=user_id)


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
            flag = 0
            for user in Users.objects.raw('SELECT * FROM main_users WHERE Email = %s', [email]):
                flag = 1
                if user.Password == password:
                    return redirect('user_home', user_id=user.ID)
                else:
                    messages.error(request,'Password is incorrect.')
                # print("for the testing : ", test)
            # flag = 0
            # for user in Users.objects.raw('SELECT * FROM main_users'):
            #      if user.Email == email:
            #          flag = 1
            #          if user.Password == password:
            #              return redirect('user_home', user_id=user.ID)
            #          else:
            #              messages.error(request,'Password is incorrect.')
            if flag == 0:
                messages.error(request,'Email does not exist.')

            # # check if the login is valid or not
            # if Users.objects.filter(Email=email).exists():
            #     user = Users.objects.get(Email=email)
            #     print(user)
            #     if user.Password == password:
            #         return redirect('user_home', user_id=user.ID)
            #     else:
            #         messages.error(request,'Password is incorrect.')
            #        # return redirect('login')
            #        # return HttpResponse("Password is incorrect.")
            # else:
            #     messages.error(request,'Email does not exist.')
            #   #  return HttpResponse("Email is invalid.")

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

            flag = 0
            for user in Users.objects.raw('SELECT * FROM main_users WHERE Email = %s', [email]):
                flag = 1
                
            if flag == 1:
                messages.error(request, "Email already exists")
            else:
                for user in Users.objects.raw('SELECT * FROM main_users WHERE Nickname = %s', [nickname]):
                    flag = 2
                if flag == 2:
                    messages.error(request, "Nickname already exists")
            
            if flag == 0:
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
