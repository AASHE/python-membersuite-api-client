import unittest

from ..exceptions import ExecuteMSQLError
from ..models import MemberSuiteObject
from ..security.models import Individual
from ..utils import (get_new_client,
                     submit_msql_query)


client = get_new_client()


class SubmitMSQLQueryTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        client.request_session()

    def test_class_familiar_to_factory(self):
        individual = submit_msql_query(
            query="SELECT OBJECT() FROM INDIVIDUAL",
            client=client)[0]
        self.assertIsInstance(individual, Individual)

    # test_class_not_familiar_to_factory below needs a MemberSuite
    # object for which at least one instance is available, and which
    # is not modeled in membersuite_api_client. Don't know of one
    # of those that's reliably (or even now and then-ly) available,
    # that's why this test gets skipped.
    @unittest.skip("Needs data fixture")
    def test_class_not_familiar_to_factory(self):
        """Is a base MemberSuiteObject returned when the class is unfamiliar?

        Test will fail when MemberSuite Task is modeled (and added to
        membersuite_object_factory.klasses).
        """
        results = submit_msql_query(query="SELECT OBJECT() FROM ???",
                                    client=client)
        self.assertEqual(type(results[0]), MemberSuiteObject)

    def test_unpermitted_query(self):
        with self.assertRaises(ExecuteMSQLError):
            submit_msql_query(query="SELECT OBJECT() FROM TermsOfService",
                              client=client)

    def test_well_formed_but_invalid_msql(self):
        with self.assertRaises(ExecuteMSQLError):
            submit_msql_query(query="SELECT OBJECT() FROM BOB",
                              client=client)

    def test_query_with_no_results(self):
        results = submit_msql_query(
            query=("SELECT OBJECT() FROM INDIVIDUAL "
                   "WHERE LASTNAME = 'bo-o-o-ogus'"),
            client=client)
        self.assertEqual(0, len(results))

    def test_query_with_multiple_results(self):
        """Does submit_msql_query work with multiple results?

        NOTE: This test depends on multiple Individuals with LastName
        of 'User' being available.

        """
        results = submit_msql_query(
            query=("SELECT OBJECTS() FROM INDIVIDUAL "
                   "WHERE LASTNAME = 'User'"),
            client=client)
        self.assertTrue(len(results))


class MemberSuiteAPIErrorTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        client.request_session()

    def test___str__(self):
        try:
            submit_msql_query(query="SELECT OBJECT() FROM BOB",
                              client=client)
        except ExecuteMSQLError as exc:
            pass

        self.assertTrue(str(exc))
