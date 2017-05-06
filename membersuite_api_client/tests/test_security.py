import os
import unittest

from ..exceptions import LoginToPortalError, MemberSuiteAPIError
from ..security import models
from ..security.services import login_to_portal, logout
from ..utils import get_new_client


LOGIN_TO_PORTAL_RETRIES = 5
LOGIN_TO_PORTAL_DELAY = 1

MEMBER_ID = os.environ['TEST_MS_MEMBER_PORTAL_USER_ID']
MEMBER_PASSWORD = os.environ['TEST_MS_MEMBER_PORTAL_USER_PASSWORD']

NONMEMBER_ID = os.environ['TEST_MS_NON_MEMBER_PORTAL_USER_ID']
NONMEMBER_PASSWORD = os.environ['TEST_MS_NON_MEMBER_PORTAL_USER_PASSWORD']

MEMBER_ORG_NAME = os.environ['TEST_MS_MEMBER_ORG_NAME']


def _login(client, member=True):
    if client.session_id is None:
        client.request_session()
    if member:
        return login_to_portal(
            username=MEMBER_ID,
            password=MEMBER_PASSWORD,
            client=client,
            retries=LOGIN_TO_PORTAL_RETRIES,
            delay=LOGIN_TO_PORTAL_DELAY)
    else:
        return login_to_portal(
            username=NONMEMBER_ID,
            password=NONMEMBER_PASSWORD,
            client=client,
            retries=LOGIN_TO_PORTAL_RETRIES,
            delay=LOGIN_TO_PORTAL_DELAY)


class SecurityServicesTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = get_new_client()

    def test_login_to_portal(self):
        """Can we log in to the portal?"""
        portal_user = _login(client=self.client)
        self.assertIsInstance(portal_user, models.PortalUser)

    def test_login_to_portal_failure(self):
        """What happens when we can't log in to the portal?"""
        with self.assertRaises(LoginToPortalError):
            login_to_portal(username="bo-o-o-gus user ID",
                            password="wrong password",
                            client=self.client,
                            retries=LOGIN_TO_PORTAL_RETRIES,
                            delay=LOGIN_TO_PORTAL_DELAY)

    def test_logout(self):
        """Can we logout?

        This logs out from the API client session, not the MemberSuite
        Portal.

        """
        self.client.session_id = None

        self.client.request_session()  # A fresh session. Yum!
        self.assertTrue(self.client.session_id)

        logout(self.client)

        self.assertIsNone(self.client.session_id)


class PortalUserTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = get_new_client()

    def setUp(self):
        self.portal_user = _login(client=self.client)

    def test_generate_username(self):
        """Does generate_username() work?

        """
        self.portal_user.membersuite_id = "6faf90e4-fake-membersuite-id"
        self.assertEqual("ms-fake-membersuite-id",
                         models.generate_username())

    def test_get_individual(self):
        """Does get_individual() work?

        """
        individual = self.portal_user.get_individual(client=self.client)
        self.assertEqual(self.portal_user.first_name, individual.first_name)
        self.assertEqual(self.portal_user.last_name, individual.last_name)
        self.assertEqual(self.portal_user.owner, individual.membersuite_id)


class IndividualTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = get_new_client()

    def setUp(self):
        self.client.request_session()
        member_portal_user = _login(client=self.client)
        self.individual_member = member_portal_user.get_individual(
            client=self.client)

    def test_is_member_for_member(self):
        """Does is_member() work for members?

        """
        is_member = self.individual_member.is_member(client=self.client)
        self.assertTrue(is_member)

    # test_is_member_for_nonmember() below can't succeed, because it
    # doesn't know about any non-member to use. Once non-member data
    # (at least a non-member Organization and a connected Individudal
    # with Portal Access) is available, push it into the env in
    # TEST_NON_MEMBER_MS_PORTAL_USER_ID and
    # TEST_NON_MEMBER_MS_PORTAL_USER_PASS and unskip this test.
    @unittest.skip("Because it can't succeed")
    def test_is_member_for_nonmember(self):
        """Does is_member() work for non-members?

        """
        client = get_new_client()
        client.request_session()
        non_member_portal_user = _login(client=client,
                                        member=False)
        individual_non_member = non_member_portal_user.get_individual(
            client=client)
        is_member = individual_non_member.is_member(client=client)
        self.assertFalse(is_member)

    def test_get_primary_organization(self):
        """Does get_primary_organization() work?

        Assumptions:

        - self.individual_member has as its primary organization, one
          named MEMBER_ORG_NAME

        """
        organization = self.individual_member.get_primary_organization(
            client=self.client)
        self.assertEqual(MEMBER_ORG_NAME, organization.name)

    def test_get_primary_organization_fails(self):
        """What happens when get_primary_organization() fails?

        """
        with self.assertRaises(MemberSuiteAPIError):
            self.individual_member.primary_organization__rtg = "bogus ID"
            self.individual_member.get_primary_organization(
                client=self.client)


if __name__ == '__main__':
    unittest.main()
