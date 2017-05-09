from rest_framework import serializers

from .models import Trip


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'


class TripSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ('uid', 'title', 'owner',)
