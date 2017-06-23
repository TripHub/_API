from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, \
    APIClient

from apps.user.models import User
from apps.trip.models import Trip
from apps.invite.models import Invite

from .constants import PENDING, ACCEPTED, REJECTED


class InviteTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_1 = User.objects.create(
            auth0_id='test0|testtesttesttesttesttest', email='foo@test.com')
        self.user_1_trip = Trip.objects.create(
            title='user1 trip', owner=self.user_1)
        self.user_2 = User.objects.create(
            auth0_id='test1|testtesttesttesttesttest', email='bar@test.com')
        self.user_3 = User.objects.create(
            auth0_id='test2|testtesttesttesttesttest', email='baz@test.com')

    def test_invite_status_defaults_to_pending(self):
        invite = Invite.objects.create(
            trip=self.user_1_trip, email='foo@test.com')
        self.assertEqual(invite.status, PENDING)

    def test_user_can_accept_invite(self):
        """We should get HTTP_204 and the invite should be set to accepted."""
        self.client.force_authenticate(user=self.user_2)
        # create an invitation
        created = Invite.objects.create(
            trip=self.user_1_trip, email='bar@test.com')
        # accept the invite
        response = self.client.get(
            reverse('invite-accept', kwargs={'uid': created.uid}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        invite = Invite.objects.get(email='bar@test.com')
        self.assertEqual(invite.status, ACCEPTED)

    def test_user_can_reject_invite(self):
        """We should get HTTP_204 and the invite should be set to rejected."""
        self.client.force_authenticate(user=self.user_2)
        # create an invitation
        created = Invite.objects.create(
            trip=self.user_1_trip, email='bar@test.com')
        # reject the invite
        response = self.client.get(
            reverse('invite-reject', kwargs={'uid': created.uid}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        invite = Invite.objects.get(email='bar@test.com')
        self.assertEqual(invite.status, REJECTED)

    def test_user_cant_accept_invites_that_are_not_theirs(self):
        """We should get HTTP 404 and the status should not change."""
        # request as user_3
        self.client.force_authenticate(user=self.user_3)
        # create an invitation for user_2
        created = Invite.objects.create(
            trip=self.user_1_trip, email='bar@test.com')
        # attempt accept user_2's invite
        response = self.client.get(
            reverse('invite-accept', kwargs={'uid': created.uid}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        invite = Invite.objects.get(email='bar@test.com')
        self.assertEqual(created.status, invite.status)
