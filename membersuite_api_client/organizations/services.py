"""
    The service for connecting to MemberSuite for OrganizationService

    http://api.docs.membersuite.com/#References/Objects/Organization.htm

"""

from ..mixins import ChunkQueryMixin
from .models import Organization, OrganizationType
from ..utils import convert_ms_object
from zeep.exceptions import TransportError
import datetime


class OrganizationService(ChunkQueryMixin, object):

    def __init__(self, client):
        """
        Accepts a ConciergeClient to connect with MemberSuite
        """
        self.client = client

    def get_orgs(
            self, limit_to=100, max_calls=None, parameters=None,
            since_when=None, start_record=0, verbose=False):
        """
        Constructs request to MemberSuite to query organization objects.

        :param int limit_to: number of records to fetch with each chunk
        :param int max_calls: the maximum number of calls (chunks) to request
        :param str parameters: additional query parameter dictionary
        :param date since_when: fetch records modified after this date
        :param int start_record: the first record to return from the query
        :param bool verbose: print progress to stdout
        :return: a list of Organization objects
        """

        if not self.client.session_id:
            self.client.request_session()

        query = "SELECT Objects() FROM Organization "
        if parameters:
            query += "WHERE"
            for key, value in parameters.items():
                query += " %s = '%s' AND" % (key, value)
            query = query[:-4]

        if since_when:
            query += " AND LastModifiedDate > '{since_when} 00:00:00'" \
                .format(since_when=datetime.date.today() -
                        datetime.timedelta(days=since_when))

        if verbose:
            print "Fetching Organizations..."

        # note, get_long_query is overkill when just looking at
        # one org, but it still only executes once
        # `get_long_query` uses `ms_object_to_model` to return Subscriptions
        org_list = self.get_long_query(
            query, limit_to=limit_to, max_calls=max_calls,
            start_record=start_record, verbose=verbose)

        return org_list

    def ms_object_to_model(self, ms_obj):
        " Converts an individual result to a Subscription Model "
        sane_obj = convert_ms_object(
            ms_obj['Fields']['KeyValueOfstringanyType'])
        return Organization(sane_obj)

    def get_org_types(self):
        """
        Retrieves all current OrganizationType objects
        """
        if not self.client.session_id:
            self.client.request_session()

        query = "SELECT Objects() FROM OrganizationType"
        result = self.client.runSQL(query=query)
        msql_result = result['body']["ExecuteMSQLResult"]
        return self.package_org_types(msql_result["ResultValue"]
                                      ["ObjectSearchResult"]
                                      ["Objects"]["MemberSuiteObject"]
                                      )

    def package_org_types(self, obj_list):
        """
        Loops through MS objects returned from queries to turn them into
        OrganizationType objects and pack them into a list for later use.
        """
        org_type_list = []
        for obj in obj_list:
            sane_obj = convert_ms_object(
                obj['Fields']['KeyValueOfstringanyType']
            )
            org = OrganizationType(sane_obj)
            org_type_list.append(org)
        return org_type_list
