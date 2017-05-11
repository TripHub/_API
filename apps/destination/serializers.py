from rest_framework import serializers

from .models import Destination


class DestinationSerializer(serializers.ModelSerializer):
    trip = serializers.CharField(source='trip.uid')

    class Meta:
        model = Destination
        exclude = ('id',)


class DestinationSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ('uid', 'title', 'latitude', 'longitude', '_order',)
