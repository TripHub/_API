from rest_framework import serializers

from apps.destination.serializers import DestinationSerializerSimple

from .models import Trip


class TripSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.uid')
    destinations = DestinationSerializerSimple(
        source='get_destinations', many=True)

    class Meta:
        model = Trip
        exclude = ('id',)


class TripSerializerSimple(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.uid')

    class Meta:
        model = Trip
        fields = ('uid', 'title', 'owner',)
