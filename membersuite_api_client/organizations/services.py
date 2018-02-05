"""
    The service for connecting to MemberSuite for OrganizationService

    http://api.docs.membersuite.com/#References/Objects/Organization.htm

"""
import datetime

from ..exceptions import ExecuteMSQLError
from ..mixins import ChunkQueryMixin
from ..security.models import Individual
from ..utils import convert_ms_object, get_new_client
from .models import Organization, OrganizationType


class OrganizationService(ChunkQueryMixin, object):

    def __init__(self, client=None):
        """
        Accepts a ConciergeClient to connect with MemberSuite
        """
        self.client = client or get_new_client(request_session=True)

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

        query = "SELECT Objects() FROM Organization"

        # collect all where parameters into a list of
        # (key, operator, value) tuples
        where_params = []

        if parameters:
            for k, v in parameters.items():
                where_params.append((k, "=", v))

        if since_when:
            d = datetime.date.today() - datetime.timedelta(days=since_when)
            where_params.append(
                ('LastModifiedDate', ">", "'%s 00:00:00'" % d))

        if where_params:
            query += " WHERE "
            query += " AND ".join(
                ["%s %s %s" % (p[0], p[1], p[2]) for p in where_params])

        if verbose:
            print("Fetching Organizations...")

        # note, get_long_query is overkill when just looking at
        # one org, but it still only executes once
        # `get_long_query` uses `ms_object_to_model` to return Organizations
        org_list = self.get_long_query(
            query, limit_to=limit_to, max_calls=max_calls,
            start_record=start_record, verbose=verbose)

        return org_list

    def ms_object_to_model(self, ms_obj):
        " Converts an individual result to an Organization Model "
        sane_obj = convert_ms_object(
            ms_obj['Fields']['KeyValueOfstringanyType'])
        return Organization(sane_obj)

    def get_org_types(self):
        """
        Retrieves all current OrganizationType objects
        """
        if not self.client.session_id:
            self.client.request_session()

        object_query = "SELECT Objects() FROM OrganizationType"
        result = self.client.execute_object_query(object_query=object_query)
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

    def get_individuals_for_primary_organization(self,
                                                 organization):
        """
        Returns all Individuals that have `organization` as a primary org.

        """
        if not self.client.session_id:
            self.client.request_session()

        object_query = ("SELECT Objects() FROM Individual WHERE "
                        "PrimaryOrganization = '{}'".format(
                            organization.membersuite_account_num))

        result = self.client.execute_object_query(object_query)

        msql_result = result["body"]["ExecuteMSQLResult"]

        if msql_result["Success"]:
            membersuite_objects = (msql_result["ResultValue"]
                                   ["ObjectSearchResult"]
                                   ["Objects"])
        else:
            raise ExecuteMSQLError(result=result)

        individuals = []

        if membersuite_objects is not None:
            for membersuite_object in membersuite_objects["MemberSuiteObject"]:
                individuals.append(
                    Individual(membersuite_object_data=membersuite_object))

        return individuals

    # get_stars_liaison_for_organization doesn't belong here.  It should
    # live in some AASHE-specific place, not in OrganizationService.
    def get_stars_liaison_for_organization(self, organization):

        candidates = self.get_individuals_for_primary_organization(
            organization=organization)

        # Check for a STARS Primary Contact first:
        for candidate in candidates:
            if "StarsPrimaryContact__rt" in candidate.fields:
                return candidate

        # No STARS Primary Contact? Try the account's primary contact:
        for candidate in candidates:
            if "Primary_Contact__rt" in candidate.fields:
                return candidate

        # No primary contact? Try billing contact:
        for candidate in candidates:
            if "Billing_Contact__rt" in candidate.fields:
                return candidate

        return None
