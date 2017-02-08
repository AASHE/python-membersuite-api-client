import os
import unittest

from ..client import ConciergeClient
from ..security import models
from ..security.services import (login_to_portal,
                                 LoginToPortalError)


class SecurityServicesTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = ConciergeClient(
            access_key=os.environ["MS_ACCESS_KEY"],
            secret_key=os.environ["MS_SECRET_KEY"],
            association_id=os.environ["MS_ASSOCIATION_ID"])

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

    def test_get_individual(self):
        """Does get_individual() work?"""
        client = ConciergeClient(
            access_key=os.environ["MS_ACCESS_KEY"],
            secret_key=os.environ["MS_SECRET_KEY"],
            association_id=os.environ["MS_ASSOCIATION_ID"])
        portal_user = login_to_portal(
            username=os.environ["TEST_MS_PORTAL_USER_ID"],
            password=os.environ["TEST_MS_PORTAL_USER_PASS"],
            client=client)
        individual = portal_user.get_individual(client=client)
        self.assertEqual(portal_user.first_name, individual.first_name)
        self.assertEqual(portal_user.last_name, individual.last_name)
        self.assertEqual(portal_user.owner, individual.id)
