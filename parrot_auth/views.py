from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import (
    status,
    viewsets,
    permissions
)

from django.contrib.auth.models import User

from parrot_auth.serializers import (
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    User._meta.get_field('email')._unique = True

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
