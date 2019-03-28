from rest_framework import serializers
from django.db import models
from main.models import Users

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

        





