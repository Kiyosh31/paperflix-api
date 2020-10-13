from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password

from .serializers import *
from .models import *
from .utils import *
from random import choice


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


# ============================================================================== #
# ============================================================================== #
# ============================================================================== #
# COOKIES

def is_user_logged_in(cookie):
    try:
        cookie = Cookies.objects.filter(cookie=cookie)
        if cookie:
            return True
    except (ObjectDoesNotExist, IndexError):
        return False


def delete_cookie(id_user=None):
    try:
        cookie = Cookies.objects.get(id_user=id_user)
        cookie.delete()
        return True
    except (ObjectDoesNotExist, IndexError):
        return False


def is_authenticated(func):
    def function_call(*args, **kwargs):
        request = args[0]
        auth = request.headers.get('authorization')
        if auth:
            if is_user_logged_in(auth):
                return func(*args, **kwargs)
            else:
                return Response({'Message': 'Acceso Denegado'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'Message': 'Error en los Headers: \'authorization\' es necesario.'}, status=status.HTTP_401_UNAUTHORIZED)
    return function_call



# ============================================================================== #
# ============================================================================== #
# ============================================================================== #
# ENDPOINTS ADMIN USERS


@api_view(['POST'])
def admin_create(request):
    request.data['password'] = make_password(request.data['password'])
    serializer = AdminUsersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        serializer_dict = serializer.data
        serializer_dict['message'] = 'Usuario creado correctamente'
        return Response(serializer_dict, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@is_authenticated
def admin_login(request):
    try:
        user = AdminUsers.objects.filter(email=request.data['email'])[0]
        if check_password(request.data['password'], user.password):
            serializer = UsersSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except IndexError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# ============================================================================== #
# ============================================================================== #
# ============================================================================== #
# ENDPOINTS USERS


# @api_view(['GET'])
# def user_list(request):
#     try:
#         users = Users.objects.filter(status=True)
#         serializer = UsersSerializer(users, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except ObjectDoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@is_authenticated
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
        user = Users.objects.filter(email=request.data['email'], status=True)[0]
        if check_password(request.data['password'], user.password):
            try:
                cookie = Cookies.objects.get(id_user=user.id_user)
                serialized_cookie = CookiesSerializer(instance=cookie, many=False)
                return Response(serialized_cookie.data, status=status.HTTP_200_OK)
            except (ObjectDoesNotExist, IndexError):
                hashed_cookie = make_password(user.name + request.data['password'])
                data = {'id_user': user.id_user, 'cookie': hashed_cookie}
                serialized_new_cookie = CookiesSerializer(data=data)
                if serialized_new_cookie.is_valid():
                    serialized_new_cookie.save()
                    return Response(serialized_new_cookie.data, status=status.HTTP_201_CREATED)
                else:
                    return Response("error", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Contraseña incorecta'}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({'message': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
    except IndexError:
        return Response({'message': 'IndexError'}, status=status.HTTP_400_BAD_REQUEST)



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
@is_authenticated
def user_update(request, id_user=None):
    if 'password' in request.data:
        request.data['password'] = make_password(request.data['password'])

    user = Users.objects.get(id_user=id_user)
    serializer = UsersSerializer(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        serializer_dict = serializer.data
        serializer_dict['message'] = 'Usuario modificado correctamente'
        return Response(serializer_dict, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@is_authenticated
def user_delete(request, id_user=None):
    user = Users.objects.get(id_user=id_user)
    request.data['status'] = False
    serializer = UsersSerializer(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        serializer_dict = serializer.data
        serializer_dict['message'] = 'Usuario eliminado correctamente'
        if delete_cookie(id_user):
            return Response(serializer_dict, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PATCH'])
def user_activate(request):
    try:
        user = Users.objects.filter(email=request.data['email'])[0]
        if check_password(request.data['password'], user.password):
            request.data['status'] = True
            request.data['password'] = make_password(request.data['password'])
            serializer = UsersSerializer(instance=user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                serializer_dict = serializer.data
                serializer_dict['message'] = 'Usuario activado correctamente'
                return Response(serializer_dict, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'message': 'El objeto no existe'}, status=status.HTTP_404_NOT_FOUND)
    except IndexError:
        return Response({'message': 'No se encontro la cuenta'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@is_authenticated
def user_logout(request, id_user=None):
    if delete_cookie(id_user):
        return Response({'Message': 'Logout Exitoso'}, status=status.HTTP_200_OK)
    else:
        return Response({'Message': 'Cookie no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

# ============================================================================== #
# ============================================================================== #
# ============================================================================== #
# ENDPOINTS PAPERS_USER


@api_view(['POST'])
@is_authenticated
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
@is_authenticated
def papersuser_list(request):
    try:
        history = PapersUser.objects.all()
        serializer = PapersUserSerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response('Historial no encontrado', status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@is_authenticated
def papersuser_detail(request, id_user=None, id_paper=None):
    try:
        history = PapersUser.objects.filter(id_user=id_user, id_paper=id_paper)[0]
        serializer = PapersUserSerializer(history, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response('Historial no encontrado', status=status.HTTP_404_NOT_FOUND)
    except IndexError:
        return Response('La calificacion no existe', status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
@is_authenticated
def papersuser_update(request, id_user=None, id_paper=None):
    try:
        history = PapersUser.objects.filter(id_user=id_user, id_paper=id_paper)[0]
        serializer = PapersUserSerializer(instance=history, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            serializer_dict = serializer.data
            serializer_dict['message'] = 'Historial modificado correctamente'
            return Response(serializer_dict, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except IndexError:
        return Response("No encontrado", status=status.HTTP_204_NO_CONTENT)



# ============================================================================== #
# ============================================================================== #
# ============================================================================== #
# ENDPOINTS PAPERS

@api_view(['POST'])
def paper_multiple_create(request):
    # if is_admin_logged_in(request.headers['authorization']):
        serializers = []
        resultados = []
        if request.data: papers = request.data
        else: papers = read_json('papers.json')
        if not papers: return Response('No hay papers para cargar.', status=status.HTTP_400_BAD_REQUEST)
        total = len(papers)
        all_papers = Papers.objects.all()
        for paper in papers:
            xD = all_papers.filter(title=paper['title'], publication_year=paper['publication_year'])
            if xD:
                total-=1
                continue
            try:
                serializers.append(PapersSerializer(data=paper))
            except:
                return Response(resultados, status=status.HTTP_400_BAD_REQUEST)
            if not serializers[-1].is_valid():
                resultados.append('Error en: ' + paper['title'])
                resultados.append(serializers[-1].errors)
        if resultados:
            return Response(resultados, status=status.HTTP_400_BAD_REQUEST)
        else:
            if total:
                for i, serializer in enumerate(serializers):
                    serializer.save()
                    print('[*] Paper: '+str(i + 1) + '/' + str(total) + '         ')
                context = 'Total: ' + str(total) + '. Todos los Datos Fueron Cargados Correctamente.'
                return Response(context, status=status.HTTP_201_CREATED)
            else:
                return Response('Total: 0. La Base de Datos esta Actualizada.', status=status.HTTP_200_OK)
    # else:
    #     return Response({'Message': 'Acceso Denegado'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def paper_create(request):
    # if is_admin_logged_in(request.headers['authorization']):
        serializer = PapersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer_dict = serializer.data
            serializer_dict['message'] = 'Paper creado correctamente'
            return Response(serializer_dict, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # else:
    #     return Response({'Message': 'Acceso Denegado'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@is_authenticated
def paper_list(request):
    try:
        papers = Papers.objects.all()
        serializer = PapersSerializer(papers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response('Paper no encontrado', status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@is_authenticated
def paper_latest(request):
    try:
        papers = Papers.objects.order_by('-publication_year')
        serializer = PapersSerializer(papers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response('Paper no encontrado', status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@is_authenticated
def paper_random(request):
    try:
        papers = Papers.objects.all()
        random_item = choice(papers)
        serialized_paper = PapersSerializer(instance=random_item, many=False)
        return Response(serialized_paper.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response('Paper no encontrado', status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@is_authenticated
def paper_detail(request, id_paper=None):
    try:
        paper = Papers.objects.get(id_paper=id_paper)
        serializer = PapersSerializer(instance=paper, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response('Paper no encontrado', status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@is_authenticated
def paper_search(request):
    try:
        papers = Papers.objects.filter(title__icontains=request.data['search'])
        papers |= Papers.objects.filter(author__icontains=request.data['search'])
        serializer = PapersSerializer(instance=papers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response("Papers no encontrados", status=status.HTTP_404_NOT_FOUND)



@api_view(['PUT'])
@is_authenticated
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



@api_view(['DELETE'])
@is_authenticated
def paper_delete(request, id_paper=None):
    try:
        paper = Papers.objects.get(id_paper=id_paper)
        paper.delete()
        return Response('Paper eliminado correctamente', status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response('Paper no encontrado', status=status.HTTP_404_NOT_FOUND)



# @api_view(['GET'])
# def paper_pagination(request, id_category=None, last_paper=None):
#     try:
#         papers = Papers.objects.filter(id_category=id_category)[last_paper: last_paper + 20]
#         serializer = PapersSerializer(papers, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except ObjectDoesNotExist:
#         return Response('Papers no encontrados', status=status.HTTP_404_NOT_FOUND)
#     except IndexError:
#         return Response('IndexError', status=status.HTTP_404_NOT_FOUND)


# ============================================================================== #
# ============================================================================== #
# ============================================================================== #
# ENDPOINTS CATEGORIES

@api_view(['POST'])
def category_multiple_create(request):
    # if is_admin_logged_in(request.headers['authorization']):
        serializers = []
        resultados = []
        if request.data:
            categories = request.data
        else:
            categories = read_json('categories.json')
        if not categories:
            return Response('No hay categoias para cargar.', status=status.HTTP_400_BAD_REQUEST)
        total = len(categories)
        all_categories = Categories.objects.all()
        for category in categories:
            if all_categories.filter(category=category['category']):
                total -= 1
                continue
            try:
                serializers.append(CategoriesSerializer(data=category))
            except:
                return Response(resultados, status=status.HTTP_400_BAD_REQUEST)
            if not serializers[-1].is_valid():
                resultados.append('Error en: ' + category['category'])
                resultados.append(serializers[-1].errors)
        if resultados:
            return Response(resultados, status=status.HTTP_400_BAD_REQUEST)
        else:
            if total:
                for i, serializer in enumerate(serializers):
                    serializer.save()
                    print('[*] Category: ' + str(i + 1) + '/' + str(total) + '         ')
                context = 'Total: ' + str(total) + '. Todos los Datos Fueron Cargados Correctamente.'
                return Response(context, status=status.HTTP_201_CREATED)
            else:
                return Response('Total: 0. La Base de Datos esta Actualizada.', status=status.HTTP_200_OK)
    # else:
    #     return Response({'Message': 'Acceso Denegado'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def category_create(request):
    # if is_admin_logged_in(request.headers['authorization']):
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer_dict = serializer.data
            serializer_dict['message'] = 'Categoria creado correctamente'
            return Response(serializer_dict, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # else:
    #     return Response({'Message': 'Acceso Denegado'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@is_authenticated
def category_list(request):
    try:
        category = Categories.objects.filter(status=True)
        serializer = CategoriesSerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response('Categoria no encontrada', status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@is_authenticated
def category_detail(request, id_category=None):
    try:
        category = Categories.objects.get(id_category=id_category, status=True)
        serializer = CategoriesSerializer(category, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response('Categoria no encontrada', status=status.HTTP_404_NOT_FOUND)



@api_view(['PATCH'])
@is_authenticated
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
@is_authenticated
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
@is_authenticated
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


