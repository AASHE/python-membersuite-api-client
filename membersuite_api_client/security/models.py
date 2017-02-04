from ..utils import convert_ms_object


class PortalUser(object):

    def __init__(self, portal_user, session_id=None):
        """Create a PortalUser object from a the Zeep'ed XML representation of
        a Membersuite PortalUser object.

        """
        fields = convert_ms_object(portal_user["Fields"]
                                   ["KeyValueOfstringanyType"])

        self.id = fields["ID"]
        self.email_address = fields["EmailAddress"]
        self.first_name = fields["FirstName"]
        self.last_name = fields["LastName"]

        self.session_id = session_id

        self.extra_data = portal_user

    def get_username(self):
        return "_membersuite_id_{}".format(self.id)
