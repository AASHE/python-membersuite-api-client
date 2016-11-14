from django.test import Client, TestCase
from .client import ConciergeClient


class ConciergeClientTestCase(TestCase):

    def test_create_client(self):
        """
        Tests that we can instantiate the SOAP client using PySimpleSOAP
        """
        # Instantiate Client and check that it was successful.
        test_client = ConciergeClient()
        self.assertTrue(test_client)

        # Modify attributes to use sample data from API docs
        # to test that signature is hashed properly.
        test_client.url = "http://membersuite.com/contracts/IConciergeAPIService/WhoAmI"
        test_client.secret_key = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=="
        test_client.association_id = "00000000-0000-0000-0000-000000000000"
        test_client.session_id = "11111111-1111-1111-1111-111111111111"
        signature = test_client.get_hashed_signature()
        self.assertEqual(signature, "2zsMYdHb/MJUeTjv5cQl5pBuIqU=")
