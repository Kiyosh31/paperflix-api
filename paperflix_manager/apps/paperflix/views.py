from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password

from .serializers import *
from .models import *

from .files import files_db


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Users-List': 'user-list/',
        'Users-Detail': 'user-detail/<int:id_user>/',
        'Users-Login': 'user-login/',
        'Users-Create': 'user-Create/',
        'Users-Update': 'user-update/<int:id_user>/',
        'Users-Delete': 'user-delete/<int:id_user>/',
        'PapersUsers-List': 'papersuser-list/',
        'PapersUsers-Detail': 'papersuser-detail/',
        'PapersUsers-Create': 'papersuser-create/',
        'PapersUsers-Update': 'papersuser-update/<int:id_user>/',
        'PapersUsers-Delete': 'papersuser-delete/<int:id_user>/',
        'Papers-List': 'paper-list/',
        'Papers-Detail': 'paper-detail/<int:id_paper>/',
        'Papers-Create': 'paper-create/',
        'Papers-Update': 'paper-update/<int:id_paper>/',
        'Papers-Delete': 'paper-delete/<int:id_paper>/',
        'Categories-List': 'category-list/',
        'Categories-Detail': 'category-detail/',
        'Categories-Create': 'category-create/',
        'Categories-Update': 'category-update/<int:id_category>/',
        'Categories-Delete': 'category-delete/<int:id_category>/',
        'CategoryPapers-List': 'categorypaper-list/',
        'CategoryPapers-Detail': 'categorypaper-detail/',
        'CategoryPapers-Create': 'categorypaper-create/',
        'CategoryPapers-Update': 'categorypaper-update/<int:id_categorypaper>/',
        'CategoryPapers-Delete': 'categorypaper-delete/<int:id_categorypaper>/',
    }

    return Response(api_urls)


@api_view(['POST'])
def showb64file(request):
    b64file = files_db.getFileb64(request.data.get('id_paper'))
    return Response(b64file, status=status.HTTP_200_OK)

# ============================================================================== #
# ============================================================================== #
# ============================================================================== #
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
    try:
        user = Users.objects.get(id_user=id_user)
        serializer = UsersSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def user_login(request):
    try:
        user = Users.objects.filter(email=request.data['email'])[0]
        if check_password(request.data['password'], user.password):
            serializer = UsersSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def user_create(request):
    request.data['password'] = make_password(request.data['password'])
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
    data = request.data.pop('selectedFile')
    serializer = PapersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        serializer_dict = serializer.data
        serializer_dict['message'] = 'Paper creado correctamente'
        files_db.setFile(serializer_dict['id_paper'], data)
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


# ============================================================================== #
# ============================================================================== #
# ============================================================================== #
# ENDPOINTS CATEGORIE_PAPERS

@api_view(['POST'])
def categorypaper_create(request):
    serializer = CategoryPapersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        serializer_dict = serializer.data
        serializer_dict['message'] = 'Pivote creado correctamente'
        return Response(serializer_dict, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def categorypaper_list(request):
    try:
        categorypaper = CategoryPaper.objects.all()
        serializer = CategoryPapersSerializer(categorypaper, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response('Pivote no encontrado', status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def categorypaper_detail(request, id_categorypaper=None):
    try:
        categorypaper = CategoryPaper.objects.get(id_categorypaper=id_categorypaper)
        serializer = CategoriesSerializer(categorypaper, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response('Pivote no encontrado', status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def categorypaper_update(request, id_categorypaper=None):
    categorypaper = CategoryPaper.objects.get(id_categorypaper=id_categorypaper)
    serializer = CategoryPapersSerializer(instance=categorypaper, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        serializer_dict = serializer.data
        serializer_dict['message'] = 'Pivote modificado correctamente'
        return Response(serializer_dict, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
