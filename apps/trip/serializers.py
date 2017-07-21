from common.rest_framework.serializers.abstract import PublicIdBaseSerializer
from apps.destination.serializers import DestinationSerializer
from apps.user.serializers import UserSerializer

from .models import Trip


class TripSerializer(PublicIdBaseSerializer):
    owner = UserSerializer()
    members = UserSerializer(many=True)
    destinations = DestinationSerializer(
        source='get_destinations', many=True)

    class Meta:
        model = Trip
        exclude = ('uid',)


class TripSerializerSimple(PublicIdBaseSerializer):
    owner = UserSerializer()
    members = UserSerializer(many=True)

    class Meta:
        model = Trip
        fields = (
            'id',
            'title',
            'tag_line',
            'owner',
            'members',
            'created',
            'modified',
        )
