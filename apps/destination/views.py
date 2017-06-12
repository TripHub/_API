import json

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import list_route

from apps.trip.models import Trip
from apps.trip.serializers import TripSerializer

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

    @list_route(methods=['POST'])
    def order(self, request):
        trip_uid = request.data.get('trip')
        dest_order = request.data.get('order')
        try:
            trip = Trip.objects.get(uid=trip_uid)
            if trip.owner != request.user:
                raise PermissionError()
            if len(trip.get_destinations()) != len(dest_order):
                raise ValueError()
            order = list(map(
                lambda uid: Destination.objects.get(uid=uid).id, dest_order))
            trip.set_destination_order(order)
            serializer = TripSerializer(trip)
            return Response(serializer.data, status=200)
        except Trip.DoesNotExist:
            return Response({
                'detail': 'Trip {0} does not exist.'.format(
                    request.data.get('trip'))
            }, status=status.HTTP_404_NOT_FOUND)
        except Destination.DoesNotExist:
            return Response({
                'detail': 'Destination does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        except PermissionError:
            return Response({
                'detail': 'Only the trip owner can add destinations.'
            }, status=status.HTTP_403_FORBIDDEN)
        except ValueError:
            return Response({
                'detail': 'All destination ID\'s must be included in the '
                          '\'order\' parameter.'
            }, status.HTTP_400_BAD_REQUEST)
