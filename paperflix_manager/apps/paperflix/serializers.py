from rest_framework import serializers
from .models import *


class AdminUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUsers
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class CookiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cookies
        fields = '__all__'


class PapersUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PapersUser
        fields = '__all__'


class PapersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Papers
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'
