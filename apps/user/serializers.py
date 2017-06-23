from common.rest_framework.serializers.abstract import PublicIdBaseSerializer

from .models import User


class UserSerializer(PublicIdBaseSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'auth0_id',
            'email',
            'last_login',
        )


class UserSerializerSimple(PublicIdBaseSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'auth0_id',
        )
