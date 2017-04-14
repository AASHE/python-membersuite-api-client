import unittest
import os

from .base import BaseTestCase
from ..subscriptions.services import SubscriptionService
from ..subscriptions.models import Subscription

# @todo - these should go in the env to be portable across associations
TEST_MS_SUBSCRIPTION_ORG_ID = os.environ['TEST_MS_SUBSCRIBER_ORG_ID']
TEST_MS_PUBLICATION_ID = os.environ['TEST_MS_PUBLICATION_ID']


class SubscriptionTestCase(BaseTestCase):

    def setUp(self):
        super(SubscriptionTestCase, self).setUp()
        self.service = SubscriptionService(self.client)

    # def test_get_org_subscriptions_all_for_org(self):
    #     """
    #     Get the all subscriptions for an organization
    #     """
    #     subscription_list = self.service.get_subscriptions(
    #         org_id=TEST_MS_SUBSCRIPTION_ORG_ID)
    #     self.assertGreaterEqual(len(subscription_list), 2)
    #     self.assertEqual(type(subscription_list[0]), Subscription)

    # def test_get_org_subscriptions_by_publication_id(self):
    #     # with publication_id
    #     subscription_list = self.service.get_subscriptions(
    #         org_id=TEST_MS_SUBSCRIPTION_ORG_ID,
    #         publication_id=TEST_MS_PUBLICATION_ID)
    #     self.assertGreaterEqual(len(subscription_list), 2)
    #     self.assertEqual(type(subscription_list[0]), Subscription)

    # def test_get_org_subscriptions_long_query(self):
    #     # now for a "long query" - querying ALL subscriptions
    #     subscription_list = self.service.get_subscriptions(
    #         limit_to=3, max_calls=3)
    #     self.assertEqual(len(subscription_list), 3)
    #     self.assertEqual(type(subscription_list[0]), Subscription)

    # def test_get_org_subscriptions_long_query_edge_case(self):
    #     # test a long query that's longer than the number we have
    #     # to ensure that edge case stops the queries
    #     #
    #     # This test sort of sucks, in that the start_record value
    #     # below is hard-coded and must be within 99 Subscriptions
    #     # of the total number of Subscriptions.  Make it better.
    #     # SELECT COUNT() FROM Subscription (sic).
    #     subscription_list = self.service.get_subscriptions(
    #         limit_to=100, start_record=1100)
    #     self.assertGreater(len(subscription_list), 0)
    #     self.assertEqual(type(subscription_list[0]), Subscription)


if __name__ == '__main__':
    unittest.main()
