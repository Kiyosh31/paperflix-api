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

# ============================================================================== #
# ============================================================================== #
# ============================================================================== #
# ENDPOINTS USERS

@api_view(['GET'])
def user_list(request):
    try:
        users = Users.objects.all()
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

# ============================================================================== #
# ============================================================================== #
# ============================================================================== #
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
        return Response('Historial no encontrado', status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def papersuser_detail(request, id_user=None):
    try:
        history = PapersUser.objects.get(id_user=id_user)
        serializer = PapersUserSerializer(history, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response('Historial no encontrado', status=status.HTTP_404_NOT_FOUND)


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


# ============================================================================== #
# ============================================================================== #
# ============================================================================== #
# ENDPOINTS PAPERS

@api_view(['POST'])
def paper_create(request):
    serializer = PapersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        serializer_dict = serializer.data
        serializer_dict['message'] = 'Paper creado correctamente'
        return Response(serializer_dict, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def paper_list(request):
    try:
        paper = Papers.objects.all()
        serializer = PapersSerializer(paper, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response('Paper no encontrado', status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def paper_detail(request, id_paper=None):
    try:
        paper = Papers.objects.get(id_paper=id_paper)
        serializer = PapersSerializer(paper, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response('Paper no encontrado', status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def paper_update(request, id_paper=None):
    paper = Papers.objects.get(id_paper=id_paper)
    serializer = PapersSerializer(instance=paper, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        serializer_dict = serializer.data
        serializer_dict['message'] = 'Paper modificado correctamente'
        return Response(serializer_dict, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ============================================================================== #
# ============================================================================== #
# ============================================================================== #
# ENDPOINTS CATEGORIES

@api_view(['POST'])
def category_create(request):
    serializer = CategoriesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        serializer_dict = serializer.data
        serializer_dict['message'] = 'Categoria creado correctamente'
        return Response(serializer_dict, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def category_list(request):
    try:
        category = Categories.objects.filter(status=True)
        serializer = CategoriesSerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response('Categoria no encontrada', status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def category_detail(request, id_category=None):
    try:
        category = Categories.objects.get(id_category=id_category)
        serializer = CategoriesSerializer(category, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response('Categoria no encontrada', status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def category_update(request, id_category=None):
    category = Categories.objects.get(id_category=id_category)
    serializer = CategoriesSerializer(instance=category, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        serializer_dict = serializer.data
        serializer_dict['message'] = 'Categoria modificada correctamente'
        return Response(serializer_dict, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def category_delete(request, id_category=None):
    category = Categories.objects.get(id_category=id_category)
    request.data['status'] = False
    serializer = CategoriesSerializer(instance=category, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        serializer_dict = serializer.data
        serializer_dict['message'] = 'Categoria eliminada correctamente'
        return Response(serializer_dict, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def category_activate(request, id_category=None):
    category = Categories.objects.get(id_category=id_category)
    request.data['status'] = True
    serializer = CategoriesSerializer(instance=category, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        serializer_dict = serializer.data
        serializer_dict['message'] = 'Categoria activada correctamente'
        return Response(serializer_dict, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
