from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from rest_framework import status


# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# def user_crud(request, id_user):
#     user = Users.objects.get(id_user=id_user)
#     serializer = UsersSerializer(data=request.data)
#
#     if request.method == 'GET':
#         serializer = UsersSerializer(user, many=True)
#         return Response(serializer.data)
#     elif request.method in ['POST', 'PUT']:
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         serializer.status = False
#         return Response(serializer.data, status=status.HTTP_200_OK)
