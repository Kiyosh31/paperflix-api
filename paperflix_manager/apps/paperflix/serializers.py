from rest_framework import serializers
from .models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        # fields = ('id_user', 'name', 'mail', 'password', 'status')
        fields = '__all__'


class PapersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PapersUser
        # fields = ('id_user', 'id_paper', 'rated')
        fields = '__all__'
