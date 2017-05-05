from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Trip(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(blank=True, max_length=255)

    def transfer_ownership(self, user):
        try:
            new_owner = get_user_model().objects.get(pk=user.pk)
            self.owner = new_owner
        except get_user_model().DoesNotExist:
            pass

    def __str__(self):
        return self.title
