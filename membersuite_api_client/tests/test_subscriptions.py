import unittest

from .base import BaseTestCase
from ..subscriptions.services import SubscriptionService


class SubscriptionTestCase(BaseTestCase):

    def setUp(self):
        super(SubscriptionTestCase, self).setUp()
        self.service = SubscriptionService(self.client)

    def test_get_org_subscriptions(self):
        """
        Get the all subscriptions for an organization
        """

        test_org_id = "6faf90e4-0007-cbaa-6232-0b3c7fa70db7"
        subscription_list = self.service.get_subscriptions(org_id=test_org_id)
        self.assertGreaterEqual(len(subscription_list), 2)

        # with publication_id
        STARS_PUBLICATION_ID = '6faf90e4-009e-cb9b-7c9e-0b3bcd6dff6a'
        subscription_list = self.service.get_subscriptions(
            org_id=test_org_id, publication_id=STARS_PUBLICATION_ID)
        self.assertGreaterEqual(len(subscription_list), 2)

        # now for a "long query" - querying ALL subscriptions
        subscription_list = self.service.get_subscriptions(
            retry_attempts=2, limit_to=3, max_calls=3)
        self.assertEqual(len(subscription_list), 9)

        # test a long query that's longer than the number we have
        # to ensure that edge case stops the queries
        subscription_list = self.service.get_subscriptions(
            retry_attempts=5, limit_to=200, max_calls=6)
        self.assertLess(len(subscription_list), 1500)

        # @todo: test the modified date


if __name__ == '__main__':
    unittest.main()
