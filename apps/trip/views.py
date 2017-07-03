from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError, NotFound
from apps.invite.models import Invite

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
            Q(owner=self.request.user) |
            Q(members__in=[self.request.user])
        ).order_by('-modified', 'title')

    def retrieve(self, request, uid=None, *args, **kwargs):
        trip = get_object_or_404(self.get_queryset(), uid=uid)
        serializer = TripSerializer(trip)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Creates a trip, setting the owner as the requester."""
        title = request.data.get('title')
        tag_line = request.data.get('tag_line')
        if not title:
            title = 'Untitled Trip'
            
        trip = Trip.objects.create(
            owner=self.request.user,
            title=title,
            tag_line=tag_line,
        )

        serializer = self.get_serializer(trip)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        trip_to_delete = get_object_or_404(
            self.get_queryset(), uid=kwargs.get('uid'))
        # only delete if the user is the owner
        if trip_to_delete.owner == self.request.user:
            # is owner: delete
            return super().destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

    @detail_route(methods=['POST'])
    def invite(self, request, uid=None):
        # from user input so be cautious
        email = request.data.get('email').lower().strip()
        if not email:
            raise ValidationError({'email': 'No email provided.'})

        trip = get_object_or_404(self.get_queryset(), uid=uid)
        user_previously_invited = Invite.objects.filter(
            trip=trip, email=email).exists()
        if user_previously_invited:
            raise ValidationError(
                '{0} has already been invited to {1}.'.format(
                    email, trip.title))

        _ = Invite.objects.create(trip=trip, email=email)
        return Response(status=status.HTTP_204_NO_CONTENT)
