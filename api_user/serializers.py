from rest_framework import serializers
from .models import UserTinder
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  

    class Meta:
        model = UserTinder 
        fields = ['email', 'name', 'password'] 

    def create(self, validated_data):

        user = UserTinder.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

class UserTinderSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTinder
        fields = ['id', 'email', 'name', 'is_active', 'is_staff', 'created']
        read_only_fields = ['id', 'created']