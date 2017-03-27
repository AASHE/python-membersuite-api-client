import unittest

from .base import BaseTestCase
from ..organizations.services import OrganizationService
from ..organizations.models import Organization, OrganizationType


class OrganizationServiceTestCase(BaseTestCase):

    def setUp(self):
        super(OrganizationServiceTestCase, self).setUp()
        self.service = OrganizationService(self.client)

    def test_get_orgs(self):
        """
        Can we call the get_orgs method and receive an org object back?
        """
        # Fetch just one org by name
        parameters = {
            'Name': 'AASHE Test Campus',
        }
        org_list = self.service.get_orgs(parameters)
        self.assertEqual(len(org_list), 1)
        self.assertEqual(type(org_list[0]), Organization)

        # Fetch all orgs using get_all=True
        # But limit to 1 result per iteration, 2 iterations
        org_list = self.service.get_orgs(get_all=True,
                                         limit_to=1,
                                         max_depth=2)
        self.assertEqual(len(org_list), 2)
        self.assertEqual(type(org_list[0]), Organization)

        # How does recursion handle the end?
        # 8055 records at the time of this test
        org_list = self.service.get_orgs(
            get_all=True, start_record=8000, limit_to=10)
        self.assertGreater(len(org_list), 50)
        self.assertEqual(type(org_list[0]), Organization)

    def test_get_org_types(self):
        """
        Test fetching all org type objects
        """
        org_type_list = self.service.get_org_types()
        self.assertTrue(len(org_type_list))
        self.assertTrue(type(org_type_list[0]), OrganizationType)


if __name__ == '__main__':
    unittest.main()
