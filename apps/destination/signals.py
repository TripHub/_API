import requests

from django.conf import settings

from rest_framework import status


def get_place_details_from_google(sender, instance=None, **kwargs):
    """
    This calls the Google API and supplements the passed Destination instance
    with the data returned from Google.
    """
    if instance.pk:
        return

    url_to_call = 'https://maps.googleapis.com/maps/api/place/details/json'
    response = requests.get(url_to_call, {
        'key': getattr(settings, 'GOOGLE_API_KEY'),
        'placeid': instance.google_place_id,
    })

    if response.status_code != status.HTTP_200_OK:
        raise Exception('Could not get place data from Google.')

    result = response.json().get('result')
    instance.google_place_data = result

    # Set the optional address and lat/lng fields using the result
    instance.address = result.get('formatted_address')
    instance.lat = result.get('geometry').get('location').get('lat')
    instance.lng = result.get('geometry').get('location').get('lng')
