from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from .serializers import *
from .models import *


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'List-Users': 'users/list',
        'Detail-Users': 'users/detail',
        'Create-Users': 'users/create',
        'Update-Users': 'users/update/<int:id_user>',
        'Delete-Users': 'users/delete<int:id_user>',
    }

    return Response(api_urls)


# ENDPOINTS USERS
@api_view(['GET'])
def user_list(request):
    try:
        users = Users.objects.filter(status=True)
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def user_detail(request, id_user=None):
    user = Users.objects.get(id_user=id_user)
    serializer = UsersSerializer(user, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def user_create(request):
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        serializer_dict = serializer.data
        serializer_dict['message'] = 'Usuario creado correctamente'
        return Response(serializer_dict, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def user_update(request, id_user):
    user = Users.objects.get(id_user=id_user)
    serializer = UsersSerializer(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        serializer_dict = serializer.data
        serializer_dict['message'] = 'Usuario modificado correctamente'
        return Response(serializer_dict, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def user_delete(request, id_user):
    user = Users.objects.get(id_user=id_user)
    request.data['status'] = False
    serializer = UsersSerializer(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        serializer_dict = serializer.data
        serializer_dict['message'] = 'Usuario eliminado correctamente'
        return Response(serializer_dict, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def user_activate(request, id_user=None):
    user = Users.objects.get(id_user=id_user)
    request.data['status'] = True
    serializer = UsersSerializer(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        serializer_dict = serializer.data
        serializer_dict['message'] = 'Usuario activado correctamente'
        return Response(serializer_dict, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ENDPOINTS PAPERS_USER
@api_view(['POST'])
def papersuser_create(request):
    serializer = PapersUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        serializer_dict = serializer.data
        serializer_dict['message'] = 'Papers_User creado correctamente'
        return Response(serializer_dict, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def papersuser_list(request):
    try:
        history = PapersUser.objects.all()
        serializer = PapersUserSerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def papersuser_detail(request, id_user=None):
    try:
        history = PapersUser.objects.get(id_user=id_user)
        serializer = PapersUserSerializer(history, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response('Objeto no encontrado', status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def papersuser_update(request, id_user=None):
    history = PapersUser.objects.get(id_user=id_user)
    serializer = PapersUserSerializer(instance=history, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        serializer_dict = serializer.data
        serializer_dict['message'] = 'Historial modificado correctamente'
        return Response(serializer_dict, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
