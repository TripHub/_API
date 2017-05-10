from rest_framework import viewsets
from rest_framework.response import Response

from .models import Trip
from .serializers import TripSerializerSimple


class TripViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, creating, updating and deleting trips.
    """
    serializer_class = TripSerializerSimple
    lookup_field = 'uid'

    def get_queryset(self):
        return Trip.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """Creates a trip, setting the owner as the requester."""
        title = request.data.get('title')
        if not title:
            title = 'Unnamed trip'
        trip = Trip.objects.create(owner=self.request.user, title=title)
        serializer = TripSerializerSimple(trip)
        return Response(serializer.data, status=201)
