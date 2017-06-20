from rest_framework import serializers

from common.rest_framework.serializers.abstract import PublicIdBaseSerializer
from apps.trip.serializers import TripSerializerSimple

from .models import Invite


class InviteSerializerSimple(PublicIdBaseSerializer):
    class Meta:
        model = Invite
        fields = ('uid',)


class InviteSerializer(PublicIdBaseSerializer):
    trip = TripSerializerSimple()
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Invite
        exclude = ('uid',)
