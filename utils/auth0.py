import requests
import time

from django.conf import settings


class Auth0Auth(requests.auth.AuthBase):
    """
    Pass an instance of this class to the auth parameter of a request to
    authenticate it.
    Singleton so tokens are retained.

    http://docs.python-requests.org/en/master/user/advanced/#custom-authentication
    """
    instance = None

    def __init__(self):
        if Auth0Auth.instance is None:
            Auth0Auth.instance = Auth0Auth.Auth0Auth()

    class Auth0Auth:
        def __init__(self):
            self.auth0_domain = getattr(
                settings, 'AUTH0_DOMAIN')
            self.auth0_api_client_id = getattr(
                settings, 'AUTH0_API_CLIENT_ID')
            self.auth0_api_client_secret = getattr(
                settings, 'AUTH0_API_CLIENT_SECRET')
            self.access_token = None
            self.access_token_expiry_time = None  # expressed in seconds

        def _update_auth0_management_access_token(self):
            response = requests.post(
                'https://{0}/oauth/token'.format(self.auth0_domain),
                {
                    'grant_type': 'client_credentials',
                    'client_id': self.auth0_api_client_id,
                    'client_secret': self.auth0_api_client_secret,
                    'audience': 'https://{0}/api/v2/'.format(self.auth0_domain)
                }
            )
            access_token = response.json().get('access_token')
            expires_in = response.json().get('expires_in')  # usually 86400s (24hr)
            current_time_in_seconds = int(time.time())
            self.access_token = access_token
            self.access_token_expiry_time = current_time_in_seconds + expires_in

        def check_access_token(self):
            """Updates the access_token if it does not exist or has expired."""
            current_time = int(time.time())
            has_access_token = self.access_token is not None
            within_expiry_time = self.access_token_expiry_time and \
                current_time < self.access_token_expiry_time
            if not has_access_token or not within_expiry_time:
                self._update_auth0_management_access_token()

    def __call__(self, r):
        """Attach the access_token to the authorization header."""
        self.instance.check_access_token()
        r.headers['authorization'] = 'Bearer {}'.format(
            self.instance.access_token)
        return r
