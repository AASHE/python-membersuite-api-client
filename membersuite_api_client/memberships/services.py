"""
    The service for connecting to MemberSuite for MembershipService

    http://api.docs.membersuite.com/#References/Objects/Membership.htm

"""

from .models import Membership, MembershipProduct
from ..utils import convert_ms_object
from zeep.exceptions import TransportError


class MembershipService(object):

    def __init__(self, client):
        """
        Accepts a ConciergeClient to connect with MemberSuite
        """
        self.client = client

    def get_memberships_for_org(self, account_num):
        """
        Retrieve all memberships associated with an organization
        """
        if not self.client.session_id:
            self.client.request_session()

        query = "SELECT Objects() FROM Membership " \
                "WHERE Owner = '%s'" % account_num
        result = self.client.runSQL(query)
        msql_result = result["body"]["ExecuteMSQLResult"]
        obj_result = msql_result["ResultValue"]["ObjectSearchResult"]
        if obj_result['Objects']:
            objects = obj_result['Objects']['MemberSuiteObject']
            if not msql_result["Errors"] and len(objects):
                return self.package_memberships(objects)
        return None

    def get_all_memberships(self, since_when=None, results=None,
                            start_record=0, limit_to=200,
                            depth=1, max_depth=None):
        """
        Retrieve all memberships updated since "since_when"

        Loop over queries of size limit_to until either a non-full queryset
        is returned, or max_depth is reached (used in tests). Then the
        recursion collapses to return a single concatenated list.
        """
        if not self.client.session_id:
            self.client.request_session()

        query = "SELECT Objects() FROM Membership"
        if since_when:
            query += " WHERE LastModifiedDate > '{since_when} 00:00:00'" \
                     " ORDER BY LocalID"\
                .format(since_when=since_when.isoformat())
        else:
            query += " ORDER BY LocalID"

        try:
            result = self.client.runSQL(
                query=query,
                start_record=start_record,
                limit_to=limit_to,
            )

        except TransportError:
            # API Intermittently fails and kicks a 504,
            # this is a way to retry if that happens.
            result = self.get_all_memberships(
                since_when=since_when,
                results=results,
                start_record=start_record,
                limit_to=limit_to,
                depth=depth,
                max_depth=max_depth,
            )

        msql_result = result['body']["ExecuteMSQLResult"]
        if (not msql_result['Errors'] and msql_result["ResultValue"]
                ["ObjectSearchResult"]["Objects"]):
            new_results = self.package_memberships(msql_result
                                                   ["ResultValue"]
                                                   ["ObjectSearchResult"]
                                                   ["Objects"]
                                                   ["MemberSuiteObject"]
                                                   ) + (results or [])

            # Check if the queryset was completely full. If so, there may be
            # More results we need to query
            if len(new_results) >= limit_to and depth < max_depth:
                new_results = self.get_all_memberships(
                    since_when=since_when,
                    results=new_results,
                    start_record=start_record + limit_to,
                    limit_to=limit_to,
                    depth=depth+1,
                    max_depth=max_depth
                )
            return new_results
        else:
            return results

    def get_all_membership_products(self):
        """
        Retrieves membership product objects
        """
        if not self.client.session_id:
            self.client.request_session()

        query = "SELECT Objects() FROM MembershipDuesProduct"
        result = self.client.runSQL(query)
        msql_result = result['body']['ExecuteMSQLResult']
        if not msql_result['Errors']:
            return self.package_membership_products(msql_result)
        else:
            return None

    def package_memberships(self, object_list):
        """
        Loops through MS objects returned from queries to turn them into
        Membership objects and pack them into a list for later use.
        """
        membership_list = []
        for obj in object_list:
            if type(obj) != str:
                sane_obj = convert_ms_object(
                    obj['Fields']['KeyValueOfstringanyType'])
                membership = Membership(sane_obj)
                membership_list.append(membership)

        return membership_list

    def package_membership_products(self, msql_result):
        """
        Loops through MS objects returned from queries to turn them into
        MembershipProduct objects and pack them into a list for later use.
        """
        obj_result = msql_result['ResultValue']['ObjectSearchResult']
        objects = obj_result['Objects']['MemberSuiteObject']
        product_list = []
        for obj in objects:
            sane_obj = convert_ms_object(
                obj['Fields']['KeyValueOfstringanyType']
            )
            product = MembershipProduct(sane_obj)
            product_list.append(product)
        return product_list
