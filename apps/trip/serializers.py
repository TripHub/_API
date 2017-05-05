from rest_framework import serializers

from .models import Trip


class TripSerializerSimple(serializers.ModelSerializer):
    """Provides list, detail, create, update and delete endpoints."""
    class Meta:
        model = Trip
        fields = ('id', 'title', 'owner',)
