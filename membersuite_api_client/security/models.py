from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.utils import python_2_unicode_compatible

from ..exceptions import ExecuteMSQLError
from ..models import MemberSuiteObject
from ..memberships import services as membership_services
from ..organizations.models import Organization
from ..utils import convert_ms_object


@python_2_unicode_compatible
class PortalUser(MemberSuiteObject):

    def __init__(self, membersuite_object_data, session_id=None):
        """Create a PortalUser object from a the Zeep'ed XML representation of
        a Membersuite PortalUser.

        """
        super(PortalUser, self).__init__(
            membersuite_object_data=membersuite_object_data)

        self.email_address = self.fields["EmailAddress"]
        self.first_name = self.fields["FirstName"]
        self.last_name = self.fields["LastName"]
        self.owner = self.fields["Owner"]
        self.session_id = session_id

    def __str__(self):
        return ("<PortalUser: ID: {id}, email_address: {email_address}, "
                "first_name: {first_name}, last_name: {last_name}, "
                "owner: {owner}, session_id: {session_id}>".format(
                    id=self.id,
                    email_address=self.email_address,
                    first_name=self.first_name,
                    last_name=self.last_name,
                    owner=self.owner,
                    session_id=self.session_id))

    def get_username(self):
        """Return a username suitable for storing in auth.User.username.

        """
        return "_membersuite_id_{}".format(self.id)

    def get_individual(self, client):
        """Return the Individual that owns this PortalUser.

        """
        if not client.session_id:
            client.request_session()

        query = "SELECT OBJECT() FROM INDIVIDUAL WHERE ID = '{}'".format(
            self.owner)

        result = client.runSQL(query)

        msql_result = result["body"]["ExecuteMSQLResult"]

        if msql_result["Success"]:
            membersuite_object_data = (msql_result["ResultValue"]
                                       ["SingleObject"])
        else:
            raise ExecuteMSQLError(result=result)

        return Individual(membersuite_object_data=membersuite_object_data,
                          portal_user=self)


@python_2_unicode_compatible
class Individual(MemberSuiteObject):

    def __init__(self, membersuite_object_data, portal_user=None):
        """Create an Individual object from the Zeep'ed XML representation of
        a MemberSuite Individual.

        """
        super(Individual, self).__init__(
            membersuite_object_data=membersuite_object_data)

        self.email_address = self.fields["EmailAddress"]
        self.first_name = self.fields["FirstName"]
        self.last_name = self.fields["LastName"]

        self.primary_organization__rtg = (
            self.fields["PrimaryOrganization__rtg"])

        self.portal_user = portal_user

    def __str__(self):
        return ("<Individual: ID: {id}, email_address: {email_address}, "
                "first_name: {first_name}, last_name: {last_name}>".format(
                    id=self.id,
                    email_address=self.email_address,
                    first_name=self.first_name,
                    last_name=self.last_name))

    def is_member(self, client):
        """Is this Individual a member?

        """
        if not client.session_id:
            client.request_session()

        primary_organization = self.get_primary_organization(client=client)

        membership = membership_services.get_primary_membership(
            organization_id=primary_organization.id,
            entity_id=self.id,
            client=client)

        return membership.receives_member_benefits

    def get_primary_organization(self, client):
        """Return the primary Organization for this Individual.

        Makes 1 or 2 MemberSuite API calls.
        """
        if not client.session_id:
            client.request_session()

        query = "SELECT OBJECT() FROM ORGANIZATION WHERE ID = '{}'".format(
            self.primary_organization__rtg)

        result = client.runSQL(query)

        msql_result = result["body"]["ExecuteMSQLResult"]

        if msql_result["Success"]:
            membersuite_object_data = (msql_result["ResultValue"]
                                       ["SingleObject"])
        else:
            raise ExecuteMSQLError(result=result)

        # Could omit this step if Organization inherits from MemberSuiteObject.
        organization = convert_ms_object(
            membersuite_object_data["Fields"]["KeyValueOfstringanyType"])

        return Organization(org=organization)
