"""
Utils for handling JWTs.
"""

import json
import requests

from jose import jwt


def validate_access_token(token, web_key_url, audience, issuer):
    """
    This validates a RS256 JWT. Returns token contents if valid, else an error.
    """
    json_web_key_url = requests.get(web_key_url).text
    json_web_key = json.loads(json_web_key_url)
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    for key in json_web_key["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
        if rsa_key:
            return jwt.decode(
                token,
                rsa_key,
                algorithms=unverified_header["alg"],
                audience=audience,
                issuer=issuer
            )
