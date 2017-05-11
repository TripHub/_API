from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Trip
from .serializers import TripSerializer, TripSerializerSimple


class TripViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, creating, updating and deleting trips.
    """
    serializer_class = TripSerializerSimple
    lookup_field = 'uid'

    def get_queryset(self):
        return Trip.objects.filter(owner=self.request.user)

    def retrieve(self, request, uid=None, *args, **kwargs):
        trip = get_object_or_404(self.get_queryset(), uid=uid)
        serializer = TripSerializer(trip)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Creates a trip, setting the owner as the requester."""
        title = request.data.get('title')
        if not title:
            title = 'Unnamed trip'
        trip = Trip.objects.create(owner=self.request.user, title=title)
        serializer = TripSerializerSimple(trip)
        return Response(serializer.data, status=201)
