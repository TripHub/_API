"""
Model utils, intended for inheritance.
"""

from django.db import models

from .utils import generate_uid


class TimeStampedModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class PublicIdModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.uid = generate_uid(self)
        return super().save(*args, **kwargs)

    uid = models.CharField(
        unique=True, editable=False, max_length=42)
