"""
    The service for connecting to MemberSuite for OrganizationService

    http://api.docs.membersuite.com/#References/Objects/Organization.htm

"""

from .models import Organization, OrganizationType
from ..utils import convert_ms_object
from zeep.exceptions import TransportError
import datetime


class OrganizationService(object):

    def __init__(self, client):
        """
        Accepts a ConciergeClient to connect with MemberSuite
        """
        self.client = client

    def get_orgs(self, parameters=None, get_all=False, since_when=None,
                 results=None, start_record=0, limit_to=200, depth=1,
                 max_depth=None):
        """
        Constructs request to MemberSuite to query organization objects
        based on parameters provided.

        Loop over queries of size limit_to until either a non-full queryset
        is returned, or max_depth is reached (used in tests). Then the
        recursion collapses to return a single concatenated list.
        """
        if not self.client.session_id:
            self.client.request_session()

        query = "SELECT Objects() FROM Organization "
        if parameters and not get_all:
            query += "WHERE"
            for key in parameters:
                query += " %s = '%s' AND" % (key, parameters[key])
            query = query[:-4]

            if since_when:
                query += " AND LastModifiedDate > '{since_when} 00:00:00'" \
                    .format(since_when=datetime.date.today() -
                            datetime.timedelta(days=since_when))
        elif since_when and not get_all:
            query += "WHERE LastModifiedDate > '{since_when} 00:00:00'".format(
                since_when=datetime.date.today() -
                datetime.timedelta(days=since_when))
        try:
            result = self.client.runSQL(
                query=query,
                start_record=start_record,
                limit_to=limit_to,
            )

        except TransportError:
            # API Intermittently fails and kicks a 504,
            # this is a way to retry if that happens.
            result = self.get_orgs(
                parameters=parameters,
                get_all=get_all,
                since_when=since_when,
                results=results,
                start_record=start_record,
                limit_to=limit_to,
                depth=depth,
                max_depth=max_depth,
            )

        msql_result = result['body']["ExecuteMSQLResult"]
        if not msql_result['Errors'] and \
                msql_result["ResultValue"]["ObjectSearchResult"]["Objects"]:
            new_results = self.package_organizations(msql_result["ResultValue"]
                                                     ["ObjectSearchResult"]
                                                     ["Objects"]
                                                     ["MemberSuiteObject"]
                                                     ) + (results or [])
            # Check if the queryset was completely full. If so, there may be
            # More results we need to query
            if len(new_results) >= limit_to and not depth == max_depth:
                new_results = self.get_orgs(
                    parameters=parameters,
                    get_all=get_all,
                    since_when=since_when,
                    results=new_results,
                    start_record=start_record + limit_to,
                    limit_to=limit_to,
                    depth=depth + 1,
                    max_depth=max_depth
                )
            return new_results
        else:
            return results

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

    def package_organizations(self, obj_list):
        """
        Loops through MS objects returned from queries to turn them into
        Organization objects and pack them into a list for later use.
        """
        org_list = []
        for obj in obj_list:
            sane_obj = convert_ms_object(
                obj['Fields']['KeyValueOfstringanyType']
            )
            org = Organization(sane_obj)
            org_list.append(org)
        return org_list

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
