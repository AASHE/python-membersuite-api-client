import os
import unittest

from ..client import ConciergeClient
from ..subscriptions import STARSSubscriptionService
import datetime

MS_ACCESS_KEY = os.environ["MS_ACCESS_KEY"]
MS_SECRET_KEY = os.environ["MS_SECRET_KEY"]
MS_ASSOCIATION_ID = os.environ["MS_ASSOCIATION_ID"]


class SubscriptionTestCase(unittest.TestCase):

    def test_get_subscriptions(self):
        """
        Get the all subscriptions for an organization
        """
        client = ConciergeClient(
            access_key=MS_ACCESS_KEY,
            secret_key=MS_SECRET_KEY,
            association_id=MS_ASSOCIATION_ID)

        ss = STARSSubscriptionService(client)
        org_id = "6faf90e4-0007-c91c-7dc8-0b3c53985743"
        subscription_list = ss.get_subscriptions(org_id)
        self.assertNotEqual(subscription_list, None)


if __name__ == '__main__':
    unittest.main()
