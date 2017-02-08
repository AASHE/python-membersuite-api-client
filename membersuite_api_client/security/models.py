from membersuite_api_client.utils import convert_ms_object
from membersuite_api_client.exceptions import ExecuteMSQLError


class PortalUser(object):

    def __init__(self, portal_user, session_id=None):
        """Create a PortalUser object from a the Zeep'ed XML representation of
        a Membersuite PortalUser.

        """
        fields = convert_ms_object(portal_user["Fields"]
                                   ["KeyValueOfstringanyType"])

        self.id = fields["ID"]
        self.email_address = fields["EmailAddress"]
        self.first_name = fields["FirstName"]
        self.last_name = fields["LastName"]

        self.owner = fields["Owner"]

        self.session_id = session_id

        self.extra_data = portal_user

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
            individual = msql_result["ResultValue"]["SingleObject"]
            return Individual(individual=individual, portal_user=self)
        else:
            raise ExecuteMSQLError(result=result)


class Individual(object):

    def __init__(self, individual, portal_user=None):
        """Create an Individual object from the Zeep'ed XML representation of
        a MemberSuite Individual.

        """
        fields = convert_ms_object(individual["Fields"]
                                   ["KeyValueOfstringanyType"])

        self.id = fields["ID"]
        self.email_address = fields["EmailAddress"]
        self.first_name = fields["FirstName"]
        self.last_name = fields["LastName"]

        self.extra_data = individual

        self.portal_user = portal_user
