from django.db.models import Q

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
    search_fields = 'trip__uid'

    def get_trip_queryset(self):
        return Trip.objects.filter(
            # is the user the owner
            Q(owner=self.request.user) |
            # is the user a member of the trip
            Q(members__in=[self.request.user])
        )

    def get_queryset(self):
        trips = self.get_trip_queryset()
        return Destination.objects.filter(trip__in=trips)

    def create(self, request, *args, **kwargs):
        """Check the trip is owned by requesting user, then pass to super."""
        trip_uid = request.data.get('trip')
        if not trip_uid:
            raise ValidationError({'trip': 'No trip provided.'})
        try:
            # check that the trip is in user's scope
            trip = self.get_trip_queryset().get(uid=trip_uid)
            # check the user owns the trip
            if trip.owner != request.user:
                raise PermissionDenied(
                    'Only the trip owner can add destinations.')
            return super().create(request, *args, **kwargs)

        except Trip.DoesNotExist:
            # if trip not in user's scope, return 404
            raise NotFound(
                'Trip {0} does not exist.'.format(request.data.get('trip')))

    @list_route(methods=['POST'])
    def order(self, request):
        trip_uid = request.data.get('trip')
        dest_uid_order = request.data.get('order')
        try:
            # check that the trip is in the user's scope
            trip = self.get_queryset().get(uid=trip_uid)
            # check that the user owns the trip
            if trip.owner != request.user:
                raise PermissionError()
            # check correct number of destinations have been given
            if len(trip.get_destinations()) != len(dest_uid_order):
                raise ValueError()
            # convert the list of UIDs to IDs
            dest_id_order = list(map(
                lambda uid: Destination.objects.get(uid=uid).id, dest_uid_order))
            # set the new order of destination objects
            trip.set_destination_order(dest_id_order)
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
            raise ValidationError({
                'order': 'All destination ID\'s must be included.'})
