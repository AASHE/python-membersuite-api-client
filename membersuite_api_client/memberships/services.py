"""
    The service for connecting to MemberSuite for MembershipService

    http://api.docs.membersuite.com/#References/Objects/Membership.htm

"""

from .models import Membership
from ..utils import convert_ms_object


class MembershipService(object):

    def __init__(self, client):
        """
        Accepts a ConciergeClient to connect with MemberSuite
        """
        self.client = client

    def get_memberships_for_org(self, org):
        """
        Retrieve all memberships associated with an organization
        """
        if not self.client.session_id:
            self.client.request_session()

        query = "SELECT Objects() FROM Membership WHERE Owner == {}".format(
            org.account_num
        )
        result = self.client.client.runSQL(query)
        msql_result = result['body']['ExecuteMSQLResult']

        if not msql_result['Errors']:
            return self.package_memberships(msql_result)
        else:
            return None

    def get_all_memberships(self):
        """
        Retrieve all memberships
        """
        if not self.client.session_id:
            self.client.request_session()

        query = "SELECT Objects() FROM Membership"
        result = self.client.client.runSQL(query)
        msql_result = result['body']['ExecuteMSQLResult']

        if not msql_result['Errors']:
            return self.package_memberships(msql_result)
        else:
            return None

    def package_memberships(self, msql_result):
        """
        Loops through MS objects returned from queries to turn them into
        Membership objects and pack them into a list for later use.
        """

        obj_result = msql_result['ResultValue']['ObjectSearchResult']
        objects = obj_result['Objects']['MemberSuiteObject']

        membership_list = []
        for obj in objects:
            sane_obj = convert_ms_object(
                obj['Fields']['KeyValueOfstringanyType'])
            membership = Membership(sane_obj)
            membership_list.append(membership)

        return membership_list
