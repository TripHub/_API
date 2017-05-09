"""
Model utils, intended for inheritance.
"""

from django.db import models

from .utils import generate_model_uid


class TimeStampedModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class PublicIdModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # since we need `self` we can't use the default param, so we add the
        # uid on save instead
        self.uid = generate_model_uid(self, length=42)
        return super().save(*args, **kwargs)

    uid = models.CharField(
        unique=True, editable=False, max_length=42)
