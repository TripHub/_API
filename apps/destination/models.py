from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import pre_save

from common.models.abstract import TimeStampedModel, PublicIdModel
from apps.trip.models import Trip

from .constants import TYPE_CHOICES, MAIN
from .signals import get_place_details_from_google


class Destination(TimeStampedModel, PublicIdModel):
    """
    Destinations are the building blocks of trips. They represent a distinct
    place of interest (e.g. airport, local attraction, etc...).
    """
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    """
    Store a copy of Google place data for the location. this avoids redundant
    requests to Google's API.
    
    This is the preferred way to store Destination information.
    """
    google_place_id = models.CharField(max_length=255, blank=True)
    google_place_data = JSONField(blank=True, null=True)

    """
    We will also store location and address information for custom
    destinations that do not have Google place data.
    """
    address = models.CharField(max_length=255, blank=True)
    lat = models.DecimalField(
        verbose_name='Latitude',
        max_digits=13,
        decimal_places=10,
        blank=True,
        null=True,
    )
    lng = models.DecimalField(
        verbose_name='Longitude',
        max_digits=13,
        decimal_places=10,
        blank=True,
        null=True,
    )

    """
    Arrival/departure information.
    """
    arrival_time = models.DateTimeField(null=True, blank=True)
    depart_time = models.DateTimeField(null=True, blank=True)

    """
    Extra Destination category info.
    """
    type = models.CharField(max_length=4, choices=TYPE_CHOICES, default=MAIN)
    related = models.ForeignKey('self', blank=True, null=True)

    class Meta:
        # gives get_next_in_order() and get_previous_in_order() methods
        order_with_respect_to = 'trip'

    def __str__(self):
        return self.trip.__str__()


pre_save.connect(receiver=get_place_details_from_google, sender=Destination)
