from rest_framework import serializers

from apps.user.serializers import UserSerializer

from .models import Trip


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'


class TripSerializerSimple(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.uid')

    class Meta:
        model = Trip
        fields = ('uid', 'title', 'owner',)
