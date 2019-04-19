import requests
# import spotipy
# import spotipy.oauth2 as oauth2
import urllib
import base64
import json
from django.http import HttpResponseRedirect

REDIRECT_URI = 'http://127.0.0.1:8000/test'
SCOPE = 'user-read-private user-read-email user-read-birthdate'
CLIENT_ID = '0955f539ece74b6aac739cdb549252ec'
CLIENT_SECRET = '4706273ab20144909ab3549c3ae67a29'

SPOTIFY_ENDPOINT  = 'https://api.spotify.com'
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

def appAuth():
    auth_query_params = {
        'client_id' : CLIENT_ID,
        "response_type" : 'code',
        "redirect_uri": REDIRECT_URI,
        "scope" : 'user-read-private user-read-email user-read-birthdate'
    }

    url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key,val in auth_query_params.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    print(auth_url)
    return auth_url

def getListofPlaylistsAuth():
    auth_query_params = {
        'client_id' : CLIENT_ID,
        "response_type" : 'code',
        "redirect_uri": 'http://127.0.0.1:8000/playlists',
        "scope" : 'playlist-read-private playlist-read-collaborative'
    }

    url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key,val in auth_query_params.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    print(auth_url)
    return auth_url


def getTracksAuth():
    auth_query_params = {
        'client_id' : CLIENT_ID,
        "response_type" : 'code',
        "redirect_uri": 'http://127.0.0.1:8000/tracks',
        "scope" : ''
    }

    url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key,val in auth_query_params.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    print(auth_url)
    return auth_url


def userAuth():
    auth_header = appAuth()
    HttpResponseRedirect(auth_header)
    #requests.get(auth_header)


def playlistsAuth():
    auth_header = getListofPlaylistsAuth()
    requests.get(auth_header)

def tracksAuth():
    auth_header = getTracksAuth()
    return HttpResponseRedirect(auth_header)
    #requests.get(auth_header)


def ajay(request):
    auth_token = request.GET.get('code')
    #print('my auth token')
    #print(auth_token)
    #print(' done printing token')
    #print(auth_token['code'])
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    #base64encoded = base64.b64encode(b"0955f539ece74b6aac739cdb549252ec:4706273ab20144909ab3549c3ae67a29")
    hard_code = "MDk1NWY1MzllY2U3NGI2YWFjNzM5Y2RiNTQ5MjUyZWM6NDcwNjI3M2FiMjAxNDQ5MDlhYjM1NDljM2FlNjdhMjk="
    headers = {"Authorization": "Basic {}".format(hard_code)}

    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    response_data = json.loads(post_request.text)
    print(response_data)
    access_token = response_data["access_token"]
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}
    print(authorization_header)
    return authorization_header

def getListofPlaylistsAuthToken(request):
    auth_token = request.GET.get('code')
    #print('my auth token')
    #print(auth_token)
    #print(' done printing token')
    #print(auth_token['code'])
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": 'http://127.0.0.1:8000/playlists'
    }
    #base64encoded = base64.b64encode(b"0955f539ece74b6aac739cdb549252ec:4706273ab20144909ab3549c3ae67a29")
    hard_code = "MDk1NWY1MzllY2U3NGI2YWFjNzM5Y2RiNTQ5MjUyZWM6NDcwNjI3M2FiMjAxNDQ5MDlhYjM1NDljM2FlNjdhMjk="
    headers = {"Authorization": "Basic {}".format(hard_code)}

    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    response_data = json.loads(post_request.text)
    print(response_data)
    access_token = response_data["access_token"]
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}
    print(authorization_header)
    return authorization_header

def getTracksAuthToken(request):
    auth_token = request.GET.get('code')
    #print('my auth token')
    #print(auth_token)
    #print(' done printing token')
    #print(auth_token['code'])
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": 'http://127.0.0.1:8000/tracks'
    }
    #base64encoded = base64.b64encode(b"0955f539ece74b6aac739cdb549252ec:4706273ab20144909ab3549c3ae67a29")
    hard_code = "MDk1NWY1MzllY2U3NGI2YWFjNzM5Y2RiNTQ5MjUyZWM6NDcwNjI3M2FiMjAxNDQ5MDlhYjM1NDljM2FlNjdhMjk="
    headers = {"Authorization": "Basic {}".format(hard_code)}

    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    response_data = json.loads(post_request.text)
    print(response_data)
    access_token = response_data["access_token"]
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}
    print(authorization_header)
    return authorization_header


def getUserData(header):
    spotify_user_endpoint = SPOTIFY_ENDPOINT+'/v1/me'
    profile_response = requests.get(spotify_user_endpoint, headers=header)
    profile_data = json.loads(profile_response.text)
    return profile_data


def getListofPlayLists(header,spotifyUserid):
    id = str(spotifyUserid)
    spotify_getListofPlaylists_endpoint = SPOTIFY_ENDPOINT+ '/v1/users/'+id+'/playlists'
    playlists_response = requests.get(spotify_getListofPlaylists_endpoint,headers = header)
    playlists_data = json.loads(playlists_response.text)
    return playlists_data


def getTracksfromPlaylist(header,playlistId):
    id = str(playlistId)
    spotify_getTracks_endpoints = SPOTIFY_ENDPOINT+'/v1/playlists/'+id+'/tracks'
    tracks = requests.get(spotify_getTracks_endpoints, headers = header)
    tracks_data = json.loads(tracks.text)
    return tracks_data
