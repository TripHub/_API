from common.rest_framework.serializers.abstract import PublicIdBaseSerializer

from .models import User


class UserSerializer(PublicIdBaseSerializer):
    class Meta:
        model = User
        exclude = ('uid',)
