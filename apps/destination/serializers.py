from rest_framework import serializers

from common.rest_framework.serializers.abstract import PublicIdBaseSerializer

from .models import Destination


class DestinationSerializer(PublicIdBaseSerializer):
    trip = serializers.CharField(source='trip.uid')

    class Meta:
        model = Destination
        exclude = ('uid',)


class DestinationSerializerSimple(PublicIdBaseSerializer):
    class Meta:
        model = Destination
        fields = ('id', 'title', 'latitude', 'longitude', '_order',)
