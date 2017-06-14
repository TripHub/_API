from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework.exceptions import PermissionDenied, NotFound, \
    ValidationError

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
                raise PermissionDenied(
                    'Only the trip owner can add destinations.')
            return super().create(request, *args, **kwargs)
        except Trip.DoesNotExist:
            raise NotFound(
                'Trip {0} does not exist.'.format(request.data.get('trip')))

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
            raise NotFound('Trip {0} does not exist.'.format(
                request.data.get('trip')))
        except Destination.DoesNotExist:
            raise NotFound('Destination does not exist.')
        except PermissionError:
            raise PermissionDenied(
                'Only the trip owner can add destinations.')
        except ValueError:
            raise ValidationError(
                'All destination ID\'s must be included in the \'order\' '
                'parameter.')
