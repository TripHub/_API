from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from common.models.abstract import TimeStampedModel, PublicIdModel


class Trip(TimeStampedModel, PublicIdModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='members', blank=True)
    title = models.CharField(blank=True, max_length=255)

    def transfer_ownership(self, user):
        try:
            # check the new owner is an active user
            new_owner = get_user_model().objects.filter(is_active=True)\
                .get(pk=user.pk)
            self.owner = new_owner
        except get_user_model().DoesNotExist:
            return False

    def __str__(self):
        return self.title


class Destination(TimeStampedModel, PublicIdModel):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)
    arrival_time = models.DateTimeField(null=True, blank=True)
    depart_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        # gives us get_next_in_order() and get_previous_in_order() methods
        order_with_respect_to = 'trip'

    def __str__(self):
        return self.title
