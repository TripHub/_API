from rest_framework import serializers
from rest_framework.response import Response

from common.rest_framework.serializers.abstract import PublicIdBaseSerializer
from apps.trip.models import Trip

from .models import Destination


class DestinationSerializer(PublicIdBaseSerializer):
    trip = serializers.SlugRelatedField(
        slug_field='uid',
        queryset=Trip.objects.all())

    class Meta:
        model = Destination
        exclude = ('uid',)


class DestinationSerializerSimple(PublicIdBaseSerializer):
    class Meta:
        model = Destination
        fields = ('id', 'title', 'latitude', 'longitude', '_order',)
