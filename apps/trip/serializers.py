from rest_framework import serializers

from common.rest_framework.serializers.abstract import PublicIdBaseSerializer
from apps.destination.serializers import DestinationSerializerSimple
from apps.user.serializers import UserSerializerSimple

from .models import Trip


class TripSerializer(PublicIdBaseSerializer):
    owner = serializers.CharField(source='owner.uid')
    members = UserSerializerSimple(many=True)
    destinations = DestinationSerializerSimple(
        source='get_destinations', many=True)

    class Meta:
        model = Trip
        exclude = ('uid',)


class TripSerializerSimple(PublicIdBaseSerializer):
    owner = serializers.CharField(source='owner.uid')
    member_count = serializers.SerializerMethodField()

    def get_member_count(self, obj):
        return len(obj.members.all())

    class Meta:
        model = Trip
        fields = (
            'id', 'title', 'owner', 'member_count', 'created', 'modified',)
