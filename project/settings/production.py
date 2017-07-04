import dj_database_url

from .common import *


INSTALLED_APPS += ['gunicorn', 'raven.contrib.django.raven_compat']


# This ensures that Django will be able to detect a secure connection
# properly on Heroku.

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Update from DATABASE_URL environment variable

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)


# Anymail
# This configures the app for email via Django's built-in email functions.

ANYMAIL = {
    'MAILGUN_API_KEY': os.environ.get('MAILGUN_API_KEY'),
    'MAILGUN_SENDER_DOMAIN': os.environ.get('MAILGUN_DOMAIN')
}
EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
DEFAULT_FROM_EMAIL = 'invite@triphub.com'
