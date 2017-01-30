import os
import unittest

from ..client import ConciergeClient


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.MS_ACCESS_KEY = os.environ["MS_ACCESS_KEY"]
        self.MS_SECRET_KEY = os.environ["MS_SECRET_KEY"]
        self.MS_ASSOCIATION_ID = os.environ["MS_ASSOCIATION_ID"]

        self.client = ConciergeClient(
            access_key=self.MS_ACCESS_KEY,
            secret_key=self.MS_SECRET_KEY,
            association_id=self.MS_ASSOCIATION_ID)
