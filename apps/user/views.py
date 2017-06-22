from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for creating users.
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
