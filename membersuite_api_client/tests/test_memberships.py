import unittest

from .base import BaseTestCase
from ..memberships.services import MembershipService


class MembershipServiceTestCase(BaseTestCase):

    def setUp(self):
        super(MembershipServiceTestCase, self).setUp()
        self.service = MembershipService(self.client)

    def test_get_membership_for_org(self):
        """
        Get membership info for a test org
        """
        # Test org with a membership
        test_org_id = "6faf90e4-0007-c578-8310-0b3c53985743"
        membership_list = self.service.get_memberships_for_org(test_org_id)
        self.assertEqual(membership_list[0].id,
                         '6faf90e4-0074-cbb5-c1d2-0b3c539859ef')

        # Test org without a membership
        test_org_id = "6faf90e4-0007-c9dc-98b7-0b3c53985743"
        membership_list = self.service.get_memberships_for_org(test_org_id)
        self.assertFalse(membership_list)

    def test_get_all_memberships(self):
        """
        Get all memberships beginning with index 700, which should ensure
        we run two API calls, one for 200, and one for under 200,
        and are able to test the recursion without having to query all
        942+ records (which takes about 10 minutes)
        """
        membership_list = self.service.get_all_memberships(start_record=700)
        self.assertTrue(len(membership_list) > 200)

    def test_get_all_membership_products(self):
        """
        Test if we can retrieve all 103 MembershipProduct objects
        """
        membership_product_list = self.service.get_all_membership_products()
        self.assertTrue(len(membership_product_list) == 103)
