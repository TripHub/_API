from django.db import models

from common.models.abstract import TimeStampedModel, PublicIdModel
from apps.trip.models import Trip

from .constants import TYPE_CHOICES, MAIN


class Destination(TimeStampedModel, PublicIdModel):
    """
    Destinations are the building blocks of trips. They represent a distinct
    place of interest (e.g. airport, local attraction, etc...).
    """
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    google_place_id = models.CharField(max_length=255, blank=True)

    # the address and lat/lng are stored in the DB to avoid making
    # further requests for common info
    address = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(
        max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(
        max_digits=12, decimal_places=9, blank=True, null=True)

    arrival_time = models.DateTimeField(null=True, blank=True)
    depart_time = models.DateTimeField(null=True, blank=True)

    type = models.CharField(max_length=4, choices=TYPE_CHOICES, default=MAIN)
    related = models.ForeignKey('self', blank=True, null=True)

    class Meta:
        # gives us get_next_in_order() and get_previous_in_order() methods
        order_with_respect_to = 'trip'

    def __str__(self):
        return self.address
