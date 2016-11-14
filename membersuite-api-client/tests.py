from django.test import Client, TestCase
from .client import ConciergeClient


class ConciergeClientTestCase(TestCase):

    def test_create_client(self):
        """
        Tests that we can instantiate the SOAP client using PySimpleSOAP
        """
        test_client = ConciergeClient()
        self.assertTrue(test_client)
        self.assertEqual(test_client.hashed_signature, "2zsMYdHb/MJUeTjv5cQl5pBuIqU=")
