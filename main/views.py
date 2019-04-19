import re
import crypt
from . import recommendation

from django.shortcuts import render, redirect
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django import forms
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect, Http404
from main.serializers import UsersSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from main.models import Users, Rooms, Guest
from django.contrib import messages
from django.db import connection


import json
import requests
from . import spotifyAuth

class login_form(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='password', max_length=100)

# class delete_form(forms.Form):
#     email = forms.CharField(label='Email', max_length=100)
#     password = forms.CharField(label='password', max_length=100)
#     room_name = forms.CharField(label='room_name', max_length=100)

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

LOGIN_COOKIE = 'music_party_logged_in'
UID_COOKIE = 'music_party_uid'
REC_COOKIE = 'music_party_rec'


def login_check(login_stat, user_id):
    this = Users.objects.filter(ID = user_id)
    if this.first():
        if login_stat and login_stat == crypt.crypt(this.first().Email, 'abc'):
            return 1
    return 0;

def login(request):
    form = login_form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            if Users.objects.filter(Email=email).exists():
                user = Users.objects.get(Email=email)
                if user.Password == password:
                    # auth_header = spotifyAuth.getTracksAuth()
                    # response = HttpResponseRedirect(auth_header)
                    # response.set_cookie(LOGIN_COOKIE, crypt.crypt(email, 'abc'))
                    # response.set_cookie(UID_COOKIE, user.ID)
                    # print(request.COOKIES.get(UID_COOKIE, None))

                    response = render(
                        request,
                        'home.html', {'user': user}
                    )
                    response.set_cookie(LOGIN_COOKIE, crypt.crypt(email, 'abc'))
                    response.delete_cookie(REC_COOKIE)

                    return response
                    # redirect('user_home', user_id=user.ID)
                else:
                    messages.error(request, 'Password is incorrect.')
            else:
                messages.error(request, 'Email does not exist.')
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
    return render(
        request,
        'signup.html', {'form':form}
    )

def welcome(request):
    return render(
        request,
        'welcome.html'
    )

def home(request):
    return HttpResponseRedirect('/welcome');

# for spotify login
def user_home(request):
    form = login_form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            if Users.objects.filter(Email=email).exists():
                user = Users.objects.get(Email=email)
                if user.Password == password:
                    auth_header = spotifyAuth.getTracksAuth()
                    response = HttpResponseRedirect(auth_header)
                     # redirect('user_home', user_id=user.ID)
                    response.set_cookie(LOGIN_COOKIE, crypt.crypt(email, 'abc'))
                    response.set_cookie(UID_COOKIE, user.ID)
                    return response
                else:
                    messages.error(request, 'Password is incorrect.')
            else:
                messages.error(request, 'Email does not exist.')
    else:
        form = login_form()
    return render(
        request,
        'login2.html', {'form':form}
    )

# true user home
def user_home2(request, user_id):
    if not login_check(request.COOKIES.get(LOGIN_COOKIE, None), user_id):
        return HttpResponseRedirect('/welcome');
    return render(
        request,
        'home.html',
        {'user': Users.objects.raw('SELECT * FROM main_users WHERE ID = %s', [user_id])[0]}
    )

def profile(request, user_id):
    spotifyAuth.userAuth()
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
            user = Users.objects.raw('SELECT * FROM main_users WHERE ID = %s', [user_id])[0]
            if request.POST.get('prev_password') == user.Password:
                nickname = request.POST.get('nickname')
                if nickname == "":
                    nickname = user.Nickname
                new_password = request.POST.get('new_password')
                if new_password == "":
                    new_password = user.Password
                gender = request.POST.get('gender')

                cursor = connection.cursor()
                cursor.execute("UPDATE main_users SET Nickname = %s, Password = %s, Gender = %s WHERE ID = %s", [nickname, new_password, gender, user_id])
                # cursor.execute("DELETE main_users WHERE ID = %s", )
                # Users.objects.filter(ID=user_id).update(Nickname=nickname, Password=new_password, Gender=gender)
                return redirect('profile', user_id=user_id)
            else:
                messages.error(request,'Password is incorrect.')
    else:
        form = update_form()
    return render(
        request,
        'update.html', {'form':form, 'id': user_id}
    )


def yourRooms(request, user_id):
    # cur = connection.cursor()
    # cur.execute('SELECT * FROM main_users WHERE ID = %s', [user_id])
    # user = cur.fetchone()
    # print("test", user[3])

    user = Users.objects.raw('SELECT * FROM main_users WHERE ID = %s', [user_id])[0]
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


                user = Users.objects.raw('SELECT * FROM main_users WHERE ID = %s', [user_id])[0]
                room = Rooms(idRoomNumber = Rooms.room_counter, RoomName = room_name, Access = access, Host = user.Nickname)
                room.save()
                return redirect('user_home2', user_id=user_id)
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
    # room = Rooms.objects.get(idRoomNumber=room_id)
    # user = Users.objects.get(ID=user_id)
    cursor = connection.cursor()
     # cursor.execute("UPDATE main_users SET Phone = 1 WHERE ID = %s", [user_id])
    cursor.execute("DELETE FROM main_guest WHERE Room_id = %s AND User_id = %s", [room_id, user_id])
    # Guest.objects.filter(Room=room, User=user).delete()
    return redirect('user_home2', user_id=user_id)


def party(request, room_id, user_id):
    room = Rooms.objects.get(idRoomNumber = room_id)
    #print(Guest.objects.raw('SELECT count(*) FROM main_guest WHERE Room = %s', [room_id]))
    rec = request.COOKIES.get(REC_COOKIE, None)
    if rec == None:
        pass
    else:
        print("-----rec songs-----")
        rec = rec.split(",")
        rec[0] = rec[0][1:]
        rec[9] = rec[9][:-1]
        print("-----rec songs-----")

    d = {
        'user': Users.objects.get(ID=user_id),
        'room': room,
        'guests': Guest.objects.filter(Room = room),
        'rec': rec,
        'count': Guest.objects.filter(Room = room).count(),
    }
    return render(request, 'party.html', d)


def public_rooms(request):
    rooms = Rooms.objects.filter(Access='public').order_by('RoomName')
    return render(request,
                'public_rooms.html',
                {'rooms': rooms}
    )

# def create(request):
#     form = room_form(request.POST or None)
#     if request.method == 'POST':
#         if form.is_valid():
#             if not Rooms.room_counter:
#                 Rooms.room_counter = 1
#             else:
#                 Rooms.room_counter += 1
#             room_name = request.POST.get('room_name')
#             private = request.POST.get('private')
#             host = request.POST.get('host')
#             #duration = request.POST.get('duration')
#             room = Rooms(idRoomNumber = Rooms.room_counter, RoomName = room_name, Access = private, Host = host)
#             room.save()
#             return JsonResponse(form.data, status=201)
#     else:
#         form = room_form()
#     return render(
#         request,
#         'create.html', {'form': form}
#     )

# def delete(request):
#     form = delete_form(request.POST or None)
#     if request.method == 'POST':
#         if form.is_valid():
#             email = request.POST.get('email')
#             password = request.POST.get('password')
#             room_name = request.POST.get('room_name')
#             res = Users.objects.filter(Email = email).filter(Password = password)
#             if res:
#                 pending_rooms = Rooms.objects.filter(RoomName = room_name)
#                 if pending_rooms.first() and pending_rooms.first().Host == res.first().Nickname:
#                     pending_rooms.first().delete()
#             return HttpResponse("You successfully deleted your room.")
#     else:
#         form = delete_form()
#     return render(
#         request,
#         'delete.html', {'form': form}
#     )
#
# def public_rooms(request):
#     rooms = Rooms.objects.filter(Access='public').order_by('RoomName')
#     return render(request,
#                 'public_rooms.html',
#                 {'rooms': rooms}
#     )
#
# def update(request):
#     form = update_form(request.POST or None)
#     if request.method == 'POST':
#         if form.is_valid():
#             email = request.POST.get('email')
#             password = request.POST.get('password')
#             room_name = request.POST.get('room_name')
#             new_room_name = request.POST.get('new_room_name')
#             res = Users.objects.filter(Email = email).filter(Password = password)
#             if res:
#                 pending_rooms = Rooms.objects.filter(RoomName = room_name)
#                 if pending_rooms.first() and pending_rooms.first().Host == res.first().Nickname:
#                     pending_rooms.update(RoomName=new_room_name)
#                     return HttpResponse("Done")
#                 else:
#                     return HttpResponse("Something went wrong!")
#     else:
#         form = update_form()
#     return render(
#         request,
#         'update.html', {'form': form}
#     )
#
# def join(request):
#     form = room_search_form(request.POST or None)
#     if request.method == 'POST':
#         if form.is_valid():
#             room_name = request.POST.get('search')
#             print(room_name)
#             res = Rooms.objects.filter(RoomName = room_name)
#             return render(
#                 request,
#                     'res.html', {'res':res}
#             )
#     else:
#         form = room_search_form()
#     return render(
#         request,
#         'join.html', {'form':form }
#     )

def test(request):
    auth_header = spotifyAuth.ajay(request)
    user_data = spotifyAuth.getUserData(auth_header)
    return render(request,'hello/test.html',{'user_data':user_data})

def test2(request):
    spotifyAuth.playlistsAuth()
    return render(request, 'hello/test2.html')

def playlists(request):
    auth_header = spotifyAuth.getListofPlaylistsAuthToken(request)
    user_data = spotifyAuth.getUserData(auth_header)
    user_id = user_data['id']
    playlist_data = spotifyAuth.getListofPlayLists(auth_header,user_id)
    return render(request,'hello/playlists.html',{'playlist_data':playlist_data})

def test4(request):
    return render(request,'hello/test4.html')

def album(request):
    return render(request, 'hello/album.html')

def test3(request):
    #spotifyAuth.tracksAuth()
    return spotifyAuth.tracksAuth()


def tracks(request):
        auth_header = spotifyAuth.getTracksAuthToken(request)
        user_data = spotifyAuth.getUserData(auth_header)
        user_id = user_data['id']
        playlist_data = spotifyAuth.getListofPlayLists(auth_header,user_id)
        listOfPlaylists = playlist_data['items']
        listOfPlaylistId = []

        for playlist in listOfPlaylists:
            if playlist['name'] == 'Test':
                listOfPlaylistId.append(playlist['id'])

        listOfTracks = [[] for id in listOfPlaylistId]

        for id in listOfPlaylistId:
            temp = spotifyAuth.getTracksfromPlaylist(auth_header,id)
            temp2 = temp['items']
            for song in temp2:
                listOfTracks[listOfPlaylistId.index(id)].append(song['track'])

        song_dict = [dict() for id in listOfPlaylistId]
        for k in range(len(listOfTracks)):
            for song in listOfTracks[k]:
                if song['is_local']==False:
                    name = song['name']
                    popularity = song['popularity']
                    listOfartists = song['artists']
                    temp = list()
                    for artist in listOfartists:
                        artist_name = artist['name']
                        temp.append(artist_name)

                    song_dict[k][name] = (popularity,temp)
                #full_album = spotifyAuth.getAlbum(auth_header,albumId)
                # Make a get album method because get request is not working because its asking for authtoken.
                # LOOK AT THE COMMENT ABOVE IN THE MORNING ONCE YOU HAVE SLEPT!!!!!!!!!!!!!
        r1, r2 = recommendation.do_recommendation(song_dict)
        t1 = [0] * 5
        for i in r1:
            t1[i] += 1
        temp = r2[r1.index(t1.index(max(t1)))]
        print("-----temp-----")
        print(temp)
        # res = " \n".join(temp)
        response = redirect('user_home2', user_id = request.COOKIES.get(UID_COOKIE, None))
        response.set_cookie(REC_COOKIE, temp)
        return response
