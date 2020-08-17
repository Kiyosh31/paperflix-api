from rest_framework import serializers
from .models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class PapersUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PapersUser
        fields = '__all__'
