from rest_framework import serializers

from .models import Trip


class TripSerializer(serializers.ModelSerializer):
    """Provides list, detail, create, update and delete endpoints."""
    class Meta:
        model = Trip
        fields = '__all__'
