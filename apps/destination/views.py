from rest_framework import viewsets, status
from rest_framework.response import Response

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

    def create(self, request, *args, **kwargs):
        """Check the trip is owned by requesting user, then pass to super."""
        trip_uid = request.data.get('trip')
        try:
            # Check that the trip exists
            trip = Trip.objects.get(uid=trip_uid)
            # Check the requesting user owns the trip
            if trip.owner != request.user:
                raise PermissionError()
            return super().create(request, *args, **kwargs)
        except Trip.DoesNotExist:
            return Response({
                'detail': 'Trip {0} does not exist.'.format(
                    request.data.get('trip'))
            }, status=status.HTTP_404_NOT_FOUND)
        except PermissionError:
            return Response({
                'detail': 'Only the trip owner can add destinations.'
            }, status=status.HTTP_403_FORBIDDEN)
