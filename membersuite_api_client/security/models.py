from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.utils import python_2_unicode_compatible

from ..exceptions import ExecuteMSQLError
from ..models import MemberSuiteObject
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
            return Individual(membersuite_object_data=membersuite_object_data,
                              portal_user=self)
        else:
            raise ExecuteMSQLError(result=result)


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

        self.portal_user = portal_user

    def __str__(self):
        return ("<Individual: ID: {id}, email_address: {email_address}, "
                "first_name: {first_name}, last_name: {last_name}>".format(
                    id=self.id,
                    email_address=self.email_address,
                    first_name=self.first_name,
                    last_name=self.last_name))
