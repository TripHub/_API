from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model

from common.models.abstract import TimeStampedModel, PublicIdModel


class Trip(TimeStampedModel, PublicIdModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='members', blank=True)
    title = models.CharField(blank=True, max_length=255)
    tag_line = models.CharField(blank=True, max_length=255)

    def get_destinations(self):
        return self.destination_set.all()

    def transfer_ownership(self, user):
        """
        Updates the owner. Throws User.DoesNotExist if the specified user does
        not exist or is not active.
        """
        new_owner = get_user_model().objects.filter(is_active=True) \
            .get(pk=user.pk)
        self.owner = new_owner

    def add_member(self, user):
        """Adds a new member. Throws if the user is also the owner."""
        if user is self.owner:
            raise ValidationError('A trip owner cannot also be a member.')
        if user in self.members.all():
            return
        self.members.add(user)

    def __str__(self):
        return self.title
