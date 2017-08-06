import requests

from django.conf import settings

from rest_framework import status


def get_place_details_from_google(sender, instance=None, **kwargs):
    """
    This calls the Google API and supplements the passed Destination instance
    with the data returned from Google.
    """
    if instance.pk:  # do nothing if already saved to DB
        return

    if instance.google_place_id is None:  # do nothing if no Google Place ID
        return

    url_to_call = 'https://maps.googleapis.com/maps/api/place/details/json'
    response = requests.get(url_to_call, {
        'key': getattr(settings, 'GOOGLE_API_KEY'),
        'placeid': instance.google_place_id,
    })

    if response.status_code != status.HTTP_200_OK:
        raise Exception('Could not get place data from Google.')

    result = response.json().get('result')

    # We can not store the full result as is because it violates Google's T&Cs.
    # Instead store a few core pieces of data and make additional requests to
    # Google's API in the future if we need additional data.
    instance.address = result.get('formatted_address')
    instance.lat = result.get('geometry').get('location').get('lat')
    instance.lng = result.get('geometry').get('location').get('lng')
