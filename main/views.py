import re
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django import forms
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect, Http404
from main.serializers import UsersSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from main.models import Users, Rooms
import json
import requests
from . import spotifyAuth
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
    room_name = forms.CharField(label='Room Name', max_length=100)
    private = forms.CharField(label= 'Access Type', max_length=10)
    duration = forms.IntegerField()
    host = forms.CharField(label="Username of Host", max_length=100)

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
            host = request.POST.get('host')
            #duration = request.POST.get('duration')
            room = Rooms(idRoomNumber = Rooms.room_counter, RoomName = room_name, Access = private, Host = host)
            room.save()
            return JsonResponse(form.data, status=201)
    else:
        form = room_form()
    return render(
        request,
        'create.html', {'form': form}
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
            return HttpResponse("You successfully deleted your room.")
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
                    return HttpResponse("Something went wrong!")
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
            return HttpResponseRedirect('/user_home')
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


def party(request):
    return render(request, 'party.html')


def profile(request):
    spotifyAuth.userAuth()
    return render(request, 'profile.html')

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
    spotifyAuth.getTracksAuth()
    return render(request, 'hello/test3.html')

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

    listOfTracks = []
    
    for id in listOfPlaylistId:
        temp = spotifyAuth.getTracksfromPlaylist(auth_header,id)
        temp2 = temp['items']
        for song in temp2:
            listOfTracks.append(song['track'])

    song_dict = dict()

    for song in listOfTracks:
        if song['is_local']==False:
            name = song['name']
            popularity = song['popularity']
            listOfartists = song['artists']
            temp = list()
            for artist in listOfartists:
                artist_name = artist['name']
                temp.append(artist_name)
            
            song_dict[name] = (popularity,temp)
            #full_album = spotifyAuth.getAlbum(auth_header,albumId)
            # Make a get album method because get request is not working because its asking for authtoken. 
            # LOOK AT THE COMMENT ABOVE IN THE MORNING ONCE YOU HAVE SLEPT!!!!!!!!!!!!!
            #print(response_data)

    return render(request, 'hello/tracks.html',{'song_dict':song_dict})

    