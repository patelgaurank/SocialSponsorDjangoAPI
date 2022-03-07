# from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import UserData, url
from django.conf import settings
from users.models import NewUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['url', 'name']


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = '__all__'


class AllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['email', 'user_name', 'first_name']


class AllUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = url
        fields = '__all__'