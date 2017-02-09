from .base import BaseTestCase
from ..organizations.services import OrganizationService
from ..organizations.models import Organization


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
