import os
import unittest

from ..client import ConciergeClient
from ..exceptions import LoginToPortalError, MemberSuiteAPIError
from ..security import models
from ..security.services import login_to_portal, logout


def get_new_client():
    return ConciergeClient(access_key=os.environ["MS_ACCESS_KEY"],
                           secret_key=os.environ["MS_SECRET_KEY"],
                           association_id=os.environ["MS_ASSOCIATION_ID"])


def get_portal_user(client, member=True):
    if client.session_id is None:
        client.request_session()
    if member:
        return login_to_portal(
            username=os.environ["TEST_MS_PORTAL_USER_ID"],
            password=os.environ["TEST_MS_PORTAL_USER_PASS"],
            client=client)
    else:
        return login_to_portal(
            username=os.environ["TEST_NON_MEMBER_MS_PORTAL_USER_ID"],
            password=os.environ["TEST_NON_MEMBER_MS_PORTAL_USER_PASS"],
            client=client)


class SecurityServicesTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = get_new_client()

    def test_login_to_portal(self):
        """Can we log in to the portal?"""
        portal_user = login_to_portal(
            username=os.environ["TEST_MS_PORTAL_USER_ID"],
            password=os.environ["TEST_MS_PORTAL_USER_PASS"],
            client=self.client)
        self.assertIsInstance(portal_user, models.PortalUser)

    def test_login_to_portal_failure(self):
        """What happens when we can't log in to the portal?"""
        with self.assertRaises(LoginToPortalError):
            login_to_portal(username="bo-o-o-gus user ID",
                            password="wrong password",
                            client=self.client)


class PortalUserTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = get_new_client()

    def setUp(self):
        self.portal_user = get_portal_user(client=self.client)

    def test_get_username(self):
        """Does get_username() work?

        """
        self.portal_user.id = "fake-membersuite-id"
        self.assertEqual("_membersuite_id_fake-membersuite-id",
                         self.portal_user.get_username())

    def test_get_individual(self):
        """Does get_individual() work?

        """
        individual = self.portal_user.get_individual(client=self.client)
        self.assertEqual(self.portal_user.first_name, individual.first_name)
        self.assertEqual(self.portal_user.last_name, individual.last_name)
        self.assertEqual(self.portal_user.owner, individual.id)


class IndividualTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = get_new_client()

    def setUp(self):
        self.client.request_session()
        member_portal_user = get_portal_user(client=self.client)
        self.individual_member = member_portal_user.get_individual(
            client=self.client)

    def test_is_member_for_member(self):
        """Does is_member() work for members?

        """
        is_member = self.individual_member.is_member(client=self.client)
        self.assertTrue(is_member)

    def test_is_member_for_nonmember(self):
        """Does is_member() work for non-members?

        """
        # logout(client=self.client)
        client = get_new_client()
        client.request_session()
        non_member_portal_user = get_portal_user(client=client,
                                                 member=False)
        individual_non_member = non_member_portal_user.get_individual(
            client=client)
        is_member = individual_non_member.is_member(client=client)
        self.assertFalse(is_member)

    def test_get_primary_organization(self):
        """Does get_primary_organization() work?

        """
        organization = self.individual_member.get_primary_organization(
            client=self.client)
        self.assertIsInstance(organization, models.Organization)

    def test_get_primary_organization_fails(self):
        """What happens when get_primary_organization() fails?

        """
        with self.assertRaises(MemberSuiteAPIError):
            self.individual_member.primary_organization__rtg = "bogus ID"
            self.individual_member.get_primary_organization(
                client=self.client)
