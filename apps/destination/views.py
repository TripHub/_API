from rest_framework import mixins, viewsets
from rest_framework.response import Response

from apps.trip.models import Trip

from .models import Destination
from .serializers import DestinationSerializer


class DestinationViewSet(mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    """
    ViewSet for retrieving, creating, updating and deleting destinations for a
    given trip.
    """
    serializer_class = DestinationSerializer
    lookup_field = 'uid'

    def get_queryset(self):
        user_trips = Trip.objects.filter(owner=self.request.user)
        return Destination.objects.filter(trip__in=user_trips)
