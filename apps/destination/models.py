from django.db import models

from common.models.abstract import TimeStampedModel, PublicIdModel
from apps.trip.models import Trip


class Destination(TimeStampedModel, PublicIdModel):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    google_place_id = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(
        max_digits=12, decimal_places=9, blank=True, null=True)
    longitude = models.DecimalField(
        max_digits=12, decimal_places=9, blank=True, null=True)
    arrival_time = models.DateTimeField(null=True, blank=True)
    depart_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        # gives us get_next_in_order() and get_previous_in_order() methods
        order_with_respect_to = 'trip'

    def __str__(self):
        return self.title
