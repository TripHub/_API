"""
Utils for access the Auth0 API
"""
import requests

from django.conf import settings


class Auth0:
    def __init__(self):
        self.auth0_domain = getattr(
            settings, 'AUTH0_DOMAIN')
        self.auth0_api_client_id = getattr(
            settings, 'AUTH0_API_CLIENT_ID')
        self.auth0_api_client_secret = getattr(
            settings, 'AUTH0_API_CLIENT_SECRET')
        self.api_token = None

    def _get_auth0_management_api_token(self):
        response = requests.post('https://{0}/oauth/token'.format(self.auth0_domain), {
            'grant_type': 'client_credentials',
            'client_id': self.auth0_api_client_id,
            'client_secret': self.auth0_api_client_secret,
            'audience': 'https://{0}/api/v2/'.format(self.auth0_domain)
        })
