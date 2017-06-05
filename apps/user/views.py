from rest_framework import viewsets

from .models import User
from .serializers import UserSerializerSimple


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving users.
    """
    serializer_class = UserSerializerSimple
    lookup_field = 'uid'

    def get_queryset(self):
        return User.objects.filter(is_active=True)
