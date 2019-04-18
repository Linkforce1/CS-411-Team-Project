from rest_framework import serializers
from django.db import models
from main.models import Users, Rooms, Guest

class UsersSerializer(serializers.Serializer):
    Email = serializers.EmailField(required=True,allow_blank=False)
    Phone = serializers.CharField(max_length=14, allow_blank = True)
    Nickname = serializers.CharField(max_length=45,allow_blank = True)
    Gender = serializers.CharField(max_length=6,allow_blank = True)
    Password = serializers.CharField(max_length=255, allow_blank=False)
    class Meta:
        model = Users
        fields = (
            'Email',
            'Phone',
            'Nickname',
            'Gender',
            'Password'
        )

    def create(self, validated_data):
        return Users.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.Email = validated_data.get('Email',instance.Email)
        instance.Phone = validated_data.get('Phone',instance.Phone)
        instance.Nickname = validated_data.get('Nickname',instance.Nickname)
        instance.Gender = validated_data.get('Gender',instance.Gender)
        instance.Password = validated_data('Password',instance.Password)


class RoomsSerializer(serializers.Serializer):
    idRoomNumber = serializers.IntegerField(required = True)
    RoomName = serializers.CharField(max_length = 45, allow_blank = False)
    Access = serializers.CharField(max_length=7, allow_blank = False)
    Host = serializers.CharField(max_length=45, allow_blank = False)
    class Meta:
        model = Rooms
        fields = (
            'idRoomNumber',
            'RoomName',
            'Access',
            'Host'
        )
    
    def create(self, validated_data):
        return Rooms.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.idRoomNumber = validated_data.get('idRoomNumber',instance.idRoomNumber)
        instance.RoomName = validated_data.get('RoomName',instance.RoomName)
        instance.Access = validated_data.get('Access',instance.Access)
        instance.Host = validated_data.get('Host',instance.Host)

class GuestsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = (
            'UserEmail',
            'RoomNumber'
        )







