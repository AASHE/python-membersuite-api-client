import unittest
from client import ConciergeClient


class ConciergeClientTestCase(unittest.TestCase):

    def test_signature_hashing(self):
        """
        Tests that we are properly hashing the signature data
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

    def test_create_session(self):
        """
        Tests that with your credentials saved to proper env vars the client
        can send a login request and receive a session ID.
        """
        # Instantiate Client and check that it was successful.
        test_client = ConciergeClient()
        self.assertTrue(test_client)

        # Send a login request to receive a session id
        session_id = test_client.request_session()
        self.assertTrue(session_id)

        # Invoke the ListAllReports method to test usage of the received session ID
        test_client.url = "http://membersuite.com/contracts/IConciergeAPIService/ListAllReports"
        test_client.hashed_signature = test_client.get_hashed_signature()
        concierge_request_header = test_client.construct_concierge_header()
        response = test_client.client.service.ListAllReports(_soapheaders=[concierge_request_header])

        # Check that the session ID in the response headers matches the
        # previously obtained session, so the user was not re-authenticated
        # but properly used the established session.
        self.assertEqual(response['header']['header']['SessionId'], test_client.session_id)

if __name__ == '__main__':
    unittest.main()
