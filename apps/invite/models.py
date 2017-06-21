from django.db import models
from django.db.models.signals import post_save

from common.models.abstract import PublicIdModel, TimeStampedModel
from apps.trip.models import Trip

from .constants import STATUS_CHOICES, PENDING, CANCELLED, ACCEPTED, REJECTED
from .signals import send_invitation


class InviteManager(models.Manager):
    def pending(self):
        """Returns a queryset containing pending invitations only."""
        return self.get_queryset().filter(status=PENDING)


class Invite(PublicIdModel, TimeStampedModel):
    class Meta:
        unique_together = ('trip', 'email',)

    trip = models.ForeignKey(Trip)
    email = models.EmailField(max_length=255)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=PENDING)

    objects = InviteManager()

    def cancel(self):
        """Invalidates the invite. Throws error if status is not pending."""
        if self.status == PENDING:
            self.status = CANCELLED
            self.save()
        else:
            raise PermissionError()

    def accept(self):
        """Accepts the invitation. Throws error if status is not pending."""
        if self.status == PENDING:
            self.status = ACCEPTED
            self.save()
        else:
            raise PermissionError()

    def reject(self):
        """Rejects the invitation.  Throws error if status is not pending."""
        if self.status == PENDING:
            self.status = REJECTED
            self.save()
        else:
            raise PermissionError()

    def save(self, *args, **kwargs):
        # normalise email
        self.email = self.email.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return '<{0}> {1}'.format(self.email, self.trip)


# send invitation email on save.
post_save.connect(send_invitation, sender=Invite)
