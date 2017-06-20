from django.db import models

from common.models.abstract import PublicIdModel, TimeStampedModel
from apps.trip.models import Trip

from .constants import STATUS_CHOICES, PENDING, CANCELLED


class Invite(PublicIdModel, TimeStampedModel):
    class Meta:
        unique_together = ('trip', 'email',)

    trip = models.ForeignKey(Trip)
    email = models.EmailField(max_length=255)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=PENDING)

    def cancel_request(self):
        self.status = CANCELLED
        self.save()

    def save(self, *args, **kwargs):
        # normalise email
        self.email = self.email.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return '<{0}> {1}'.format(self.email, self.trip)
