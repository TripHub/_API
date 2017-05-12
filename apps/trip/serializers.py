from rest_framework import serializers

from common.rest_framework.serializers.abstract import PublicIdBaseSerializer
from apps.destination.serializers import DestinationSerializerSimple

from .models import Trip


class TripSerializer(PublicIdBaseSerializer):
    owner = serializers.CharField(source='owner.uid')
    destinations = DestinationSerializerSimple(
        source='get_destinations', many=True)

    class Meta:
        model = Trip
        exclude = ('uid',)


class TripSerializerSimple(PublicIdBaseSerializer):
    owner = serializers.CharField(source='owner.uid')

    class Meta:
        model = Trip
        fields = ('id', 'title', 'owner',)
