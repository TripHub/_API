"""
Model utils, intended for inheritance.
"""

from django.db import models

from utils.models.id import generate_model_prefixed_id


class TimeStampedModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class PublicIdModel(models.Model):
    """
    The UID field is a candidate field, but not a primary key field (for db 
    performance reasons). It's purpose is to enable external users to identify
    a specific entity without publicly exposing an the numerical ID (which can
    be easily iterated/looped over in an attempt to access sequential
    resources).
    """
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # since we need `self` we can't use the default param, so we add the
        # uid on save instead
        self.uid = generate_model_prefixed_id(self, length=32)
        return super().save(*args, **kwargs)

    uid = models.CharField(
        unique=True, editable=False, max_length=32)
