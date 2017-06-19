from django.db import models

from common.models.abstract import PublicIdModel, TimeStampedModel
from apps.trip.models import Trip


class Invite(PublicIdModel, TimeStampedModel):
    trip = models.ForeignKey(Trip)
    email = models.EmailField(max_length=255)
