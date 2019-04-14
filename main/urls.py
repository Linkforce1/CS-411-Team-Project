from django.urls import path,include
from main import views
from django.conf.urls import url

urlpatterns = [
    path("", views.home, name="home"),
    path("welcome", views.welcome, name="welcome"),
    path("user_home", views.user_home, name="user_home"),
    path("login", views.login, name="login"),
    path("join", views.join, name="join"),
    path("delete", views.delete, name="delete"),
    path("update", views.update, name="update"),
    path("create", views.create, name="create"),
    path("signup", views.signup, name="signup"),
    path("party", views.party, name="party"),
    path("profile",views.profile,name="profile"),
    path("public_rooms",views.public_rooms,name="public_rooms"),
    path("test",views.test,name="test"),
    path('test2',views.test2,name='test2'),
    path('playlists',views.playlists,name='playlists'),
    path('test3',views.test3,name='test3'),
    path('tracks',views.tracks,name='test3'),
    path('test4',views.test4,name='test4'),
    path('album',views.album,name='album'),
    path('', include('django.contrib.auth.urls')),
    path('social/', include('social_django.urls')),
]
