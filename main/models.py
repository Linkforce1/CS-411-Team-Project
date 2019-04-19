from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Rooms(models.Model):
    room_counter = 0
    idRoomNumber = models.IntegerField(primary_key=True)
    RoomName = models.CharField(max_length = 45, default = "my-room")
    Access = models.CharField(max_length = 10, default = "public")
    Host = models.CharField(max_length=45)
    objects = models.Manager()

class Users(models.Model):
    user_counter = 0
    ID = models.IntegerField(primary_key=True)
    Email = models.EmailField(max_length=45,unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    Phone = models.CharField(max_length=14, validators=[phone_regex], blank = True)
    Nickname = models.CharField(max_length=45, blank = True, unique = True)
    Gender = models.CharField(max_length=6, blank = True)
    Password = models.CharField(max_length=255, blank = False)
    objects = models.Manager()

class Guest(models.Model):
    User = models.ForeignKey(Users, on_delete=models.CASCADE)
    Room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    objects = models.Manager()
