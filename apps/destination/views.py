from rest_framework import viewsets

from apps.trip.models import Trip

from .models import Destination
from .serializers import DestinationSerializer


class DestinationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, creating, updating and deleting
    destinations for a given trip.
    """
    serializer_class = DestinationSerializer
    lookup_field = 'uid'

    def get_queryset(self):
        user_trips = Trip.objects.filter(owner=self.request.user)
        print(user_trips, Destination.objects.filter(trip__in=user_trips))
        return Destination.objects.filter(trip__in=user_trips)
