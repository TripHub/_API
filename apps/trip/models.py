from django.db import models


class Trip(models.Model):
    title = models.CharField(blank=True, max_length=255)
