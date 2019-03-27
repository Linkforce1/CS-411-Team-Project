from django.db import models

# Create your models here.

class Rooms(models.Model):
    idRoomNumber = models.IntegerField(primary_key=True)
    Access = models.CharField(max_length=7)
    Host = models.CharField(max_length=45)
    
class Users(models.Model):
    Email = models.CharField(max_length=45, primary_key = True)
    Phone = models.CharField(max_length=14)
    Nickname = models.CharField(max_length=45)
    Gender = models.CharField(max_length=7)
    Password = models.CharField(max_length=255)

    def __init__(self, Email, Phone, Nickname, Gender, Password):
        self.Email = Email
        self.Phone = Phone
        self.Nickname = Nickname
        self.Gender = Gender
        self.Password = Password

        
class Guest(models.Model):
    UserEmail = models.ForeignKey(Users,on_delete=models.CASCADE)
    RoomNumber = models.ForeignKey(Rooms, on_delete=models.CASCADE)

