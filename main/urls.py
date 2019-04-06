from django.urls import path,include
from main import views

urlpatterns = [
    path("", views.home, name="home"),
    path("welcome", views.welcome, name="welcome"),
    path("user_home/<int:user_id>", views.user_home, name="user_home"),
    path("login", views.login, name="login"),
    path("create/<int:user_id>", views.create, name="create"),
    path("signup", views.signup, name="signup"),
    path("party", views.party, name="party"),
    path("profile/<int:user_id>",views.profile,name="profile"),
    # path('accounts/', include('django.contrib.auth.urls')),
]
