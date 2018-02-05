import unittest

from ..exceptions import ExecuteMSQLError
from ..utils import (get_new_client,
                     submit_msql_object_query)


client = get_new_client()


class MemberSuiteAPIErrorTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        client.request_session()
        try:
            submit_msql_object_query(
                object_query="SELECT OBJECT() FROM BOB",
                client=client)
        except ExecuteMSQLError as exc:
            cls.exc = exc

    def test_get_concierge_error(self):
        concierge_error = self.exc.get_concierge_error()
        self.assertTrue(concierge_error is not None)

    def test___str__(self):
        self.assertTrue(str(self.exc) > '')


if __name__ == '__main__':
    unittest.main()
