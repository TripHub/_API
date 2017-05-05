from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import authentication
from rest_framework import exceptions
from jose import jwt

from utils.authentication.jwt import validate_access_token


class Auth0Authentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        access_token = request.META.get('HTTP_AUTHORIZATION')
        # if there's no Authorization header then give up
        if not access_token:
            return None
        try:
            # decode the access_token
            issuer = 'https://' + settings.AUTH0_DOMAIN + '/'
            web_key_url = "https://" + settings.AUTH0_DOMAIN + "/.well-known/jwks.json"
            payload = validate_access_token(
                token=access_token, web_key_url=web_key_url, audience=settings.AUTH0_API_AUDIENCE, issuer=issuer)
            # get the user identifier from the token and get the associated user object.
            sub = payload.get('sub')
            user = get_user_model().objects.get(identifier=sub)
        except jwt.JWTError as e:
            raise exceptions.AuthenticationFailed(e.__str__())
        except get_user_model().DoesNotExist:
            raise exceptions.AuthenticationFailed('User does not exist')

        return user, None
