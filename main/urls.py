from django.urls import path
from main import views

urlpatterns = [
    path("", views.home, name="home"),
    path("welcome", views.welcome, name="welcome"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("main/<name>", views.hello_there, name="hello_there"),
    path("", views.hello_world, name = "hello_world"),
]
