from django.urls import reverse
from django.db.models import signals

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from apps.user.models import User
from apps.trip.models import Trip
from apps.destination.models import Destination


class DestinationTest(APITestCase):
    def setUp(self):
        # prevent attempting to get test users from Auth0
        signals.pre_save.disconnect(sender=User)
        self.client = APIClient()
        self.user_1 = User.objects.create(
            auth0_id='test0|testtesttesttesttesttest', email='1@t.com')
        self.user_1_trip = Trip.objects.create(
            address='user1 trip', owner=self.user_1)
        self.user_2 = User.objects.create(
            auth0_id='test1|testtesttesttesttesttest', email='2@t.com')
        self.user_2_trip = Trip.objects.create(
            address='user2 trip', owner=self.user_2)

    def test_get_destinations_returns_ok(self):
        """We should get HTTP 200."""
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(reverse('destination-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owned_destinations_returned(self):
        """Only dest_1 should be returned."""
        dest_1 = Destination.objects.create(
            address='', trip=self.user_1_trip)
        dest_2 = Destination.objects.create(
            address='', trip=self.user_2_trip)
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(reverse('destination-list'))
        count = response.data.get('count')
        results = response.data.get('results')
        # one result should be returned
        self.assertEqual(count, 1)
        self.assertEqual(len(results), 1)
        # dest_1 should be in results
        self.assertEqual(results[0].get('id'), dest_1.uid)

    def test_member_destinations_returned(self):
        """
        Check destinations of trips the user is a member of are returned.
        """
        dest_1 = Destination.objects.create(
            address='', trip=self.user_2_trip)
        self.user_2_trip.members.add(self.user_1)
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(reverse('destination-list'))
        results = response.data.get('results')
        self.assertEqual(results[0].get('id'), dest_1.uid)
