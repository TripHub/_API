from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from common.models.abstract import TimeStampedModel, PublicIdModel

from .signals import create_auth0_user, delete_auth0_user


class UserManager(BaseUserManager):
    def create_user(self, identifier):
        if not identifier:
            raise ValueError('Users must have an identifier')
        user = User.objects.create(
            identifier=identifier)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, identifier, password, email=''):
        if not identifier:
            raise ValueError('Users must have an identifier')
        if User.objects.filter(email=email).exists():
            raise ValidationError('User with email already exists')
        user = User.objects.create(
            identifier=identifier, email=email)
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, TimeStampedModel, PublicIdModel):
    identifier = models.CharField(max_length=128, unique=True, editable=False)
    email = models.EmailField(unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'identifier'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.email or self.identifier

    def get_short_name(self):
        return self.email or self.identifier

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        # normalise the email (if provided)
        self.email = self.email.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email or self.identifier

# match Django user's with Auth0 users
pre_save.connect(create_auth0_user, sender=User)
post_delete.connect(delete_auth0_user, sender=User)
