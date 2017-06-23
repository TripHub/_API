from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from common.models.abstract import TimeStampedModel, PublicIdModel

from .signals import get_user_email, delete_auth0_user


class UserManager(BaseUserManager):
    def create_user(self, auth0_id):
        if not auth0_id:
            raise ValueError('Users must have an auth0_id')
        user = User.objects.create(
            auth0_id=auth0_id)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, auth0_id, password, email=''):
        if not auth0_id:
            raise ValueError('Users must have an auth0_id')
        if User.objects.filter(email=email).exists():
            raise ValidationError('User with email already exists')
        user = User.objects.create(
            auth0_id=auth0_id, email=email)
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, TimeStampedModel, PublicIdModel):
    auth0_id = models.CharField(max_length=128, unique=True, editable=False)
    email = models.EmailField(unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'auth0_id'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.email or self.auth0_id

    def get_short_name(self):
        return self.email or self.auth0_id

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        # normalise the email (if provided)
        self.email = self.email.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email or self.auth0_id

# match Django user's with Auth0 users
pre_save.connect(get_user_email, sender=User)
post_delete.connect(delete_auth0_user, sender=User)
