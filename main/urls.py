from django.urls import path,include
from main import views
from django.conf.urls import url

urlpatterns = [
    path("", views.home, name="home"),
    path("welcome", views.welcome, name="welcome"),
    # path("user_home", views.user_home, name="user_home"),
    path("login", views.login, name="login"),
    # path("join", views.join, name="join"),
    #path("delete", views.delete, name="delete"),
    # path("update", views.update, name="update"),
    # path("create", views.create, name="create"),
    path("signup", views.signup, name="signup"),
    path("user_home/<int:user_id>", views.user_home, name="user_home"),
    path("profile/<int:user_id>",views.profile,name="profile"),
    path("update/<int:user_id>",views.update,name="update"),
    path("yourRooms/<int:user_id>", views.yourRooms, name="yourRooms"),
    path("create/<int:user_id>", views.create, name="create"),
    path("join/<int:user_id>", views.join, name="join"),
    path("addGuest/<int:room_id>/<int:user_id>", views.addGuest, name="addGuest"),
    path("leaveRoom/<int:room_id>/<int:user_id>", views.leaveRoom, name="leaveRoom"),
    path("party/<int:room_id>/<int:user_id>", views.party, name="party"),
    #path("party", views.party, name="party"),

    path("public_rooms",views.public_rooms,name="public_rooms"),

    # path("party", views.party, name="party"),
    # path("profile",views.profile,name="profile"),
    # path("public_rooms",views.public_rooms,name="public_rooms"),
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
