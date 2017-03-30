import unittest

from .base import BaseTestCase
from ..memberships.services import MembershipService
from ..memberships.models import Membership, MembershipProduct

# This should come from the env...
# in fact, we should consistently define these somewhere
# fixtures would be ideal
TEST_ORG_ID_WITH_MEM = "6faf90e4-0007-c316-3054-0b3ca00fb259"
TEST_ORG_ID_WITHOUT_MEM = "6faf90e4-0007-c77c-326a-0b3ca00fb259"


class MembershipServiceTestCase(BaseTestCase):

    def setUp(self):
        super(MembershipServiceTestCase, self).setUp()
        self.service = MembershipService(self.client)

    @unittest.skip("Need an Organization ID for a non-member org")
    def test_get_membership_for_org(self):
        """
        Get membership info for a test org
        """
        # Test org with a membership
        membership_list = self.service.get_memberships_for_org(
            TEST_ORG_ID_WITH_MEM, verbose=True)
        self.assertEqual(type(membership_list[0]), Membership)

        # Test org without a membership
        membership_list = self.service.get_memberships_for_org(
            TEST_ORG_ID_WITHOUT_MEM, verbose=True)
        self.assertFalse(membership_list)

    def test_get_all_memberships(self):
        """
        Does the get_all_memberships() method work?
        """
        membership_list = self.service.get_all_memberships(
            limit_to=1, max_calls=2, verbose=True
        )
        self.assertEqual(len(membership_list), 2)
        self.assertEqual(type(membership_list[0]), Membership)

    def test_get_all_membership_products(self):
        """
        Test if we can retrieve all MembershipProduct objects
        103 at the time of testing
        """
        membership_product_list = self.service.get_all_membership_products()
        self.assertTrue(len(membership_product_list) > 0)
        self.assertEqual(type(membership_product_list[0]),
                         MembershipProduct)


if __name__ == '__main__':
    unittest.main()
