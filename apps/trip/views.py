from rest_framework import viewsets

from .models import Trip
from .serializers import TripSerializer


class TripViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing trips.
    """
    serializer_class = TripSerializer
    queryset = Trip.objects.all()