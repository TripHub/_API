from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from common.models.utils import TimeStampedModel


class Trip(TimeStampedModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='members')
    title = models.CharField(blank=True, max_length=255)

    def transfer_ownership(self, user):
        try:
            # check the new owner is an active user
            new_owner = get_user_model().objects.filter(is_active=True)\
                .get(pk=user.pk)
            self.owner = new_owner
        except get_user_model().DoesNotExist:
            pass

    def __str__(self):
        return self.title
