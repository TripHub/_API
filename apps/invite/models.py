from django.db import models

from common.models.abstract import PublicIdModel, TimeStampedModel
from apps.trip.models import Trip


class Invite(PublicIdModel, TimeStampedModel):
    class Meta:
        unique_together = ('trip', 'email',)

    trip = models.ForeignKey(Trip)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return '<{0}> {1}'.format(self.email, self.trip)
