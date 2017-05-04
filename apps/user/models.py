from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    identifier = models.CharField(max_length=128, primary_key=True)

    USERNAME_FIELD = 'identifier'
    REQUIRED_FIELDS = ['email']
