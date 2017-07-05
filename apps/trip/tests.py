from django.urls import reverse
from django.db.models import signals

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from apps.user.models import User
from apps.trip.models import Trip


class TripTest(APITestCase):
    def setUp(self):
        # prevent attempting to retrieve test users from Auth0
        signals.pre_save.disconnect(sender=User)
        self.client = APIClient()
        self.user_1 = User.objects.create(
            auth0_id='test0|testtesttesttesttesttest', email='1@t.com')
        self.user_1_trip = Trip.objects.create(
            title='user1 trip', owner=self.user_1)
        self.user_2 = User.objects.create(
            auth0_id='test1|testtesttesttesttesttest', email='2@t.com')
        self.user_2_trip = Trip.objects.create(
            title='user2 trip', owner=self.user_2)

    def test_list_trips_endpoint_returns_ok(self):
        """
        We should get HTTP 200.
        """
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(reverse('trip-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owned_trips_returned(self):
        """
        Only dest_1 should be returned.
        """
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(reverse('trip-list'))

        count = response.data.get('count')
        results = response.data.get('results')

        # only user_1_trip should be returned
        self.assertEqual(count, 1)
        self.assertEqual(len(results), 1)

        # dest_1 should be in results
        self.assertEqual(results[0].get('id'), self.user_1_trip.uid)

    def test_member_trips_returned(self):
        """
        Check destinations of trips the user is a member of are returned.
        """
        self.user_2_trip.members.add(self.user_1)
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(reverse('trip-list'))

        count = response.data.get('count')
        results = response.data.get('results')

        # we expect two results now, user_1_trip and user_2_trip
        self.assertEqual(count, 2)
        self.assertEqual(len(results), 2)
