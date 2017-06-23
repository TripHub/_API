import requests

from django.conf import settings

from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, \
    HTTP_204_NO_CONTENT
from utils.auth0 import Auth0Auth


BASE_URL = url = 'https://{0}/api/v2'.format(getattr(settings, 'AUTH0_DOMAIN'))


def create_auth0_user(sender, instance=None, **kwargs):
    """
    Registers a new user on Auth0.
    """
    url = '{0}/users'.format(BASE_URL)
    response = requests.post(url=url, auth=Auth0Auth(), json={
            'connection': 'Username-Password-Authentication',
            'email': instance.email,
            'password': instance.password
        })
    if response.status_code != HTTP_201_CREATED:
        raise Exception('Error creating user on Auth0.')

    user_id = response.json().get('user_id')
    instance.identifier = user_id


def get_user_email(sender, instance=None, **kwargs):
    """
    Supplements the instance with email from Auth0.
    """
    url = '{0}/users/{1}'.format(BASE_URL, instance.identifier)
    response = requests.get(url=url, auth=Auth0Auth())
    if response.status_code != HTTP_200_OK:
        raise Exception('Error finding user on Auth0.')

    email = response.json().get('email')
    instance.email = email


def delete_auth0_user(sender, instance=None, **kwargs):
    """
    Deletes an existing user on Auth0.
    """
    url = '{0}/users/{1}'.format(BASE_URL, instance.identifier)
    response = requests.delete(url=url, auth=Auth0Auth())

    if response.status_code != HTTP_204_NO_CONTENT:
        # silently fail
        pass
