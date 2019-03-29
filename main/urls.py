from django.urls import path,include
from main import views

urlpatterns = [
    path("", views.home, name="home"),
    path("welcome", views.welcome, name="welcome"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("party", views.party, name="party"),
    path("profile",views.profile,name="profile"),
    path('accounts/', include('django.contrib.auth.urls')),
]
