from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
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
        # filter trips to those that the user owns or is a member of
        return Trip.objects.filter(
            Q(owner=self.request.user) | Q(members__in=[self.request.user])
        )

    def retrieve(self, request, uid=None, *args, **kwargs):
        trip = get_object_or_404(self.get_queryset(), uid=uid)
        serializer = TripSerializer(trip)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Creates a trip, setting the owner as the requester."""
        title = request.data.get('title')
        if not title:
            title = 'Untitled Trip'
        trip = Trip.objects.create(owner=self.request.user, title=title)
        serializer = TripSerializerSimple(trip)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            # check trip exists
            trip_to_delete = self.get_queryset().get(uid=kwargs.get('uid'))
            # check user owns trip
            if trip_to_delete.owner == self.request.user:
                return super().destroy(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Trip.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
