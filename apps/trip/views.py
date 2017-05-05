from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Trip
from .serializers import TripSerializer


class TripViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing trips.
    """
    serializer_class = TripSerializer
    queryset = Trip.objects.all()