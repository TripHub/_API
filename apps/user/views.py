from rest_framework import viewsets, mixins

from .serializers import UserSerializer


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for creating users.
    """
    serializer_class = UserSerializer
