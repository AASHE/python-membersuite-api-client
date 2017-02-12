import unittest

from .base import BaseTestCase
from ..memberships.services import MembershipService
from ..memberships.models import Membership, MembershipProduct


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
        test_org_id = "6faf90e4-0007-c578-8310-0b3c53985743"
        membership_list = self.service.get_memberships_for_org(test_org_id)
        self.assertEqual(type(membership_list[0]), Membership)
        self.assertEqual(membership_list[0].id,
                         '6faf90e4-0074-cbb5-c1d2-0b3c539859ef')

        # Test org without a membership

        # Need an Organization ID for a non-member org. The one here
        # is the same used above for testing with a member org.
        #
        #            HERE!
        #              |
        #              |
        #              V
        test_org_id = "6faf90e4-0007-c9dc-98b7-0b3c53985743"
        membership_list = self.service.get_memberships_for_org(test_org_id)
        self.assertFalse(membership_list)

    def test_get_all_memberships(self):
        """
        Does the get_all_memberships() method work?
        """
        membership_list = self.service.get_all_memberships(
            limit_to=1, max_depth=2
        )
        self.assertEqual(len(membership_list), 2)
        self.assertEqual(type(membership_list[0]), Membership)

    def test_get_all_membership_products(self):
        """
        Test if we can retrieve all 103 MembershipProduct objects
        """
        membership_product_list = self.service.get_all_membership_products()
        self.assertTrue(len(membership_product_list) == 103)
        self.assertEqual(type(membership_product_list[0]),
                         MembershipProduct)
