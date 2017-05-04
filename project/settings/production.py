import dj_database_url

from .common import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ('DJANGO_SECRET_KEY')


# This ensures that Django will be able to detect a secure connection
# properly on Heroku.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES['default'].update(dj_database_url.config(conn_max_age=500))
