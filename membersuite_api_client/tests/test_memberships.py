import unittest

from .base import BaseTestCase
from ..memberships.services import MembershipService


class MembershipServiceTestCase(BaseTestCase):

    def setUp(self):
        super(MembershipServiceTestCase, self).setUp()
        self.service = MembershipService(self.client)
