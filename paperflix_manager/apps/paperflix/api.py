from .models import Users
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


# Lead Viewset
class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def delete_user(self, request, id_user=None):
        user = self.get_object()
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            user.status = False
            user.save()
            return Response({'Deletes': 'Usuario eliminaro correctamente'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
