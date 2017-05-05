from rest_framework import viewsets
from rest_framework.response import Response

from .models import Trip
from .serializers import TripSerializer


class TripViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing trips.
    """
    serializer_class = TripSerializer

    def get_queryset(self):
        print('user', self.request.user)
        return Trip.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        title = request.data.get('title')
        if not title:
            title = 'Unnamed trip'
        trip = Trip.objects.create(owner=self.request.user, title=title)
        serializer = TripSerializer(trip)
        return Response(serializer.data, status=201)
