from django.urls import path,include
from main import views

urlpatterns = [
    path("", views.home, name="home"),
    path("welcome", views.welcome, name="welcome"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("user_home/<int:user_id>", views.user_home, name="user_home"),
    path("profile/<int:user_id>",views.profile,name="profile"),
    path("yourRooms/<int:user_id>", views.yourRooms, name="yourRooms"),
    path("create/<int:user_id>", views.create, name="create"),
    path("join/<int:user_id>", views.join, name="join"),
    path("addGuest/<int:room_id>/<int:user_id>", views.addGuest, name="addGuest"),
    path("party/<int:room_id>/<int:user_id>", views.party, name="party"),
    #path("party", views.party, name="party"),

    path("public_rooms",views.public_rooms,name="public_rooms"),
]
