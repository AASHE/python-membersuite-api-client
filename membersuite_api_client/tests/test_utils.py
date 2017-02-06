import os
import unittest

from ..client import ConciergeClient
from ..utils import convert_ms_object


MS_ACCESS_KEY = os.environ["MS_ACCESS_KEY"]
MS_SECRET_KEY = os.environ["MS_SECRET_KEY"]
MS_ASSOCIATION_ID = os.environ["MS_ASSOCIATION_ID"]


class UtilsTestCase(unittest.TestCase):

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
        converted_dict = convert_ms_object(
            response[0]["Fields"]["KeyValueOfstringanyType"])

        self.assertEqual(converted_dict["Name"], "AASHE Test Campus")


if __name__ == '__main__':
    unittest.main()
