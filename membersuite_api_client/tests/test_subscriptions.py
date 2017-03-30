import unittest

from .base import BaseTestCase
from ..subscriptions.services import SubscriptionService
from ..subscriptions.models import Subscription

# @todo - these should go in the env to be portable across associations
TEST_SUBSCRIPTION_OWNER = '6faf90e4-0006-cd5b-0ec7-0b3ca00fae56'
TEST_PUBLICATION_ID = '6faf90e4-009e-cb9b-7c9e-0b3bcd6dff6a'


class SubscriptionTestCase(BaseTestCase):

    def setUp(self):
        super(SubscriptionTestCase, self).setUp()
        self.service = SubscriptionService(self.client)

    def test_get_org_subscriptions(self):
        """
        Get the all subscriptions for an organization
        """
        subscription_list = self.service.get_subscriptions(
            org_id=TEST_SUBSCRIPTION_OWNER, verbose=True)
        self.assertGreaterEqual(len(subscription_list), 2)
        self.assertEqual(type(subscription_list[0]), Subscription)

        # with publication_id
        subscription_list = self.service.get_subscriptions(
            org_id=TEST_SUBSCRIPTION_OWNER,
            publication_id=TEST_PUBLICATION_ID,
            verbose=True)
        self.assertGreaterEqual(len(subscription_list), 2)
        self.assertEqual(type(subscription_list[0]), Subscription)

        # now for a "long query" - querying ALL subscriptions
        subscription_list = self.service.get_subscriptions(
            limit_to=3, max_calls=3, verbose=True)
        self.assertEqual(len(subscription_list), 9)
        self.assertEqual(type(subscription_list[0]), Subscription)

        # test a long query that's longer than the number we have
        # to ensure that edge case stops the queries
        # ~1500 subscriptions at the time of these tests
        subscription_list = self.service.get_subscriptions(
            limit_to=100, start_record=1300, verbose=True)
        self.assertGreater(len(subscription_list), 0)
        self.assertEqual(type(subscription_list[0]), Subscription)

        # @todo: test the modified date


if __name__ == '__main__':
    unittest.main()
