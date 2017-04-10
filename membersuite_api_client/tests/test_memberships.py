import unittest
import os

from .base import BaseTestCase
from ..memberships.services import MembershipService, MembershipProductService
from ..memberships.models import Membership, MembershipProduct

# might eventually have to come from fixtures
MEMBER_ORG_ID = os.environ.get('TEST_MS_MEMBER_ORG_ID')
NONMEMBER_ORG_ID = os.environ.get('TEST_MS_NON_MEMBER_ORG_ID')


class MembershipServiceTestCase(BaseTestCase):

    def setUp(self):
        super(MembershipServiceTestCase, self).setUp()
        self.service = MembershipService(self.client)
        self.product_service = MembershipProductService(self.client)

    @unittest.skip("Need an Organization ID for a non-member org")
    def test_get_membership_for_org(self):
        """
        Get membership info for a test org
        """
        # Test org with a membership
        membership_list = self.service.get_memberships_for_org(
            MEMBER_ORG_ID, verbose=False)
        self.assertEqual(type(membership_list[0]), Membership)

        # Test org without a membership
        membership_list = self.service.get_memberships_for_org(
            NONMEMBER_ORG_ID, verbose=False)
        self.assertFalse(membership_list)

    def test_get_all_memberships(self):
        """
        Does the get_all_memberships() method work?
        """
        membership_list = self.service.get_all_memberships(
            limit_to=1, max_calls=2, verbose=False
        )
        self.assertEqual(len(membership_list), 2)
        self.assertEqual(type(membership_list[0]), Membership)

    def test_get_all_membership_products(self):
        """
        Test if we can retrieve all MembershipProduct objects
        103 at the time of testing
        """
        service = self.product_service
        membership_product_list = service.get_all_membership_products()
        self.assertTrue(len(membership_product_list) > 0)
        self.assertEqual(type(membership_product_list[0]),
                         MembershipProduct)


if __name__ == '__main__':
    unittest.main()
