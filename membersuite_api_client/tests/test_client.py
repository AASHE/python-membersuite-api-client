import os
import unittest

from ..client import ConciergeClient
import datetime


MS_USER_ID = os.environ.get("MS_USER_ID", None)
MS_USER_PASS = os.environ.get("MS_USER_PASS", None)
MS_ACCESS_KEY = os.environ["MS_ACCESS_KEY"]
MS_SECRET_KEY = os.environ["MS_SECRET_KEY"]
MS_ASSOCIATION_ID = os.environ["MS_ASSOCIATION_ID"]


class ConciergeClientTestCase(unittest.TestCase):

    def test_signature_hashing(self):
        """
        Tests that we are properly hashing the signature data
        """
        client = ConciergeClient(
            access_key=MS_ACCESS_KEY,
            secret_key=("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=="),
            association_id="00000000-0000-0000-0000-000000000000")

        # Modify attributes to use sample data from API docs
        # to test that signature is hashed properly.
        client.session_id = "11111111-1111-1111-1111-111111111111"
        signature = client.get_hashed_signature(
            url="http://membersuite.com/contracts/IConciergeAPIService/WhoAmI")
        self.assertEqual(signature, "2zsMYdHb/MJUeTjv5cQl5pBuIqU=")

    def test_request_session(self):
        """
        Can we send a login request and receive a session ID?
        """
        client = ConciergeClient(access_key=MS_ACCESS_KEY,
                                 secret_key=MS_SECRET_KEY,
                                 association_id=MS_ASSOCIATION_ID)

        # Send a login request to receive a session id
        session_id = client.request_session()
        self.assertTrue(session_id)

        # Invoke the ListAllReports method to test usage of the
        # received session ID
        url = ("http://membersuite.com/contracts/"
               "IConciergeAPIService/ListAllReports")
        client.hashed_signature = client.get_hashed_signature(url=url)
        concierge_request_header = client.construct_concierge_header(url=url)
        response = client.client.service.ListAllReports(
            _soapheaders=[concierge_request_header])

        # Check that the session ID in the response headers matches the
        # previously obtained session, so the user was not re-authenticated
        # but properly used the established session.
        self.assertEqual(
            client.get_session_id_from_login_result(login_result=response),
            client.session_id)

    def test_query_orgs(self):
        """
        Can we call the search method and receive an org object back?
        """
        client = ConciergeClient(access_key=MS_ACCESS_KEY,
                                 secret_key=MS_SECRET_KEY,
                                 association_id=MS_ASSOCIATION_ID)

        # Send a login request to receive a session id
        session_id = client.request_session()
        self.assertTrue(session_id)
        parameters = {
            'Name': 'AASHE Test Campus',
        }
        response = client.query_orgs(parameters)
        self.assertEqual(response[0]["Fields"]["KeyValueOfstringanyType"]
                         [28]["Value"],
                         'AASHE Test Campus')

        # Test querying orgs modified in the last day
        # (there should be zero in our sandbox)
        since_when = datetime.date.today() - datetime.timedelta(1)
        response = client.query_orgs(parameters, since_when)
        self.assertFalse(response)

    def test_convert_ms_object(self):
        """
        Can we parse the list of dicts for org attributes into a dict?
        """
        client = ConciergeClient(access_key=MS_ACCESS_KEY,
                                 secret_key=MS_SECRET_KEY,
                                 association_id=MS_ASSOCIATION_ID)

        # Send a login request to receive a session id
        session_id = client.request_session()
        self.assertTrue(session_id)
        parameters = {
            'Name': 'AASHE Test Campus',
        }
        response = client.query_orgs(parameters)
        self.assertEqual(response[0]["Fields"]["KeyValueOfstringanyType"]
                         [28]["Value"],
                         'AASHE Test Campus')
        converted_dict = client.convert_ms_object(
            response[0]["Fields"]["KeyValueOfstringanyType"])

        self.assertEqual(converted_dict["Name"], "AASHE Test Campus")


if __name__ == '__main__':
    unittest.main()