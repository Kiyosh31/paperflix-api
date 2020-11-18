from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from .models import Cookies, Papers
from .serializers import PapersSerializer
import json
import copy

#=========================================
#============== Constants ================
#=========================================

RESPONSE_NO_PRIVILEGES = {'Message': 'Sin privilegios.'}
RESPONSE_ACCESS_DENIED = {'Message': 'Acceso Denegado.'}
RESPONSE_HEADERS_ERROR = {'Message': 'Error en los Headers: \'authorization\' es necesario.'}

#=========================================
#=============== Lambdas =================
#=========================================

convert_to_lowercase = lambda object_x: [x.lower() for x in object_x] if type(object_x) == list else object_x.lower()

#=========================================
#============== Functions ================
#=========================================

def read_json(fname):
    try:
        file_ = open(fname, 'r', encoding='utf-8')
        load  = json.load(file_)
        return load
    except FileNotFoundError:
        return None


# COOKIES ============================================

def delete_cookie(id_user, type_user):
    try:
        cookie = Cookies.objects.get(id_user=id_user, type_user=type_user)
        cookie.delete()
        return True
    except ObjectDoesNotExist:
        return False


def is_user_logged_in(cookie):
    try:
        cookie = Cookies.objects.get(cookie=cookie)
        return cookie
    except ObjectDoesNotExist:
        return False


def user_rules(func, current_user_id, add_id, args, kwargs):
    if add_id:
        kwargs['id_user'] = current_user_id
        return func(*args, **kwargs)
    if kwargs.get('id_user'):
        if current_user_id == kwargs.get('id_user'):
            return func(*args, **kwargs)
        else:
            return Response(RESPONSE_NO_PRIVILEGES, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return func(*args, **kwargs)


def admin_rules(func, current_user_id, admin_endpoint, args, kwargs):
    if admin_endpoint:
        if kwargs.get('id_user'):
            if current_user_id == kwargs.get('id_user'):
                return func(*args, **kwargs)
            else:
                return Response(RESPONSE_NO_PRIVILEGES, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return func(*args, **kwargs)
    else:
        return func(*args, **kwargs)


def is_authenticated(type_user=['user','admin'], add_id=False, admin_endpoint=False):
    def inner(func):
        def user_restrictions(*args, **kwargs):
            request = args[0]
            auth = request.headers.get('authorization')
            if auth:
                cookie = is_user_logged_in(auth)
                if cookie:
                    current_user = cookie.type_user
                    if   current_user.lower() == 'user'  and 'user'  in convert_to_lowercase(type_user): return user_rules(func, cookie.id_user, add_id, args, kwargs)
                    elif current_user.lower() == 'admin' and 'admin' in convert_to_lowercase(type_user): return admin_rules(func, cookie.id_user, admin_endpoint, args, kwargs)
                    else:
                        return Response(RESPONSE_ACCESS_DENIED, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response(RESPONSE_ACCESS_DENIED, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(RESPONSE_HEADERS_ERROR, status=status.HTTP_401_UNAUTHORIZED)
        return user_restrictions
    return inner


#=========================================
#=========================================
#=========================================

cache_papers = []

def api_cache(func):
    def cache(*args, **kwargs):
        global cache_papers
        if not cache_papers:
            print(1)
            resp = func(*args, **kwargs)
            cache_papers = copy.deepcopy(resp)
        return cache_papers
    return cache


@api_cache
def get_all_papers():
    papers = Papers.objects.all()
    serializer = PapersSerializer(papers, many=True)
    return serializer

