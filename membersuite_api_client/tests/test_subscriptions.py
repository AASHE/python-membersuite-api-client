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

        test_org_id = "6faf90e4-0007-c91c-7dc8-0b3c53985743"
        subscription_list = self.service.get_org_subscriptions(test_org_id)
        self.assertNotEqual(subscription_list, None)

        # with publication_id
        STARS_PUBLICATION_ID = '6faf90e4-009e-cb9b-7c9e-0b3bcd6dff6a'
        subscription_list = self.service.get_org_subscriptions(
            test_org_id, publication_id=STARS_PUBLICATION_ID)
        self.assertNotEqual(subscription_list, None)


if __name__ == '__main__':
    unittest.main()
