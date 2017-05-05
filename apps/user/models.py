from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def raise_no_identifier_error(self):
        raise ValueError('users must have an identifier')

    def create_user(self, identifier):
        if not identifier:
            self.raise_no_identifier_error()
        user = User.objects.create(
            identifier=identifier)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, identifier, password, email=''):
        user = User.objects.create(
            identifier=identifier, email=email)
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    identifier = models.CharField(max_length=128, primary_key=True)
    email = models.EmailField(blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'identifier'

    def get_full_name(self):
        return self.email or self.identifier

    def get_short_name(self):
        return self.email or self.identifier

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email or self.identifier
