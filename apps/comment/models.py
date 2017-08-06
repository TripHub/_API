"""
A Comment models a single comment left by a user. Each comment stores to which
entity it relates to (e.g. a Destination instance).
"""

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from common.models.abstract import PublicIdModel, TimeStampedModel


class Comment(PublicIdModel, TimeStampedModel):
    """
    Target refers to the entity the comment was made in relation to. Since this
    element could have a variety of types, we link the ForeignKey to
    ContentType, and set content_object to a GenericForeignKey instance.

    https://docs.djangoproject.com/en/1.11/ref/contrib/contenttypes/#generic-relations
    """
    target = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    in_reply_to = models.ForeignKey(
        'self', models.CASCADE, null=True, blank=True)
