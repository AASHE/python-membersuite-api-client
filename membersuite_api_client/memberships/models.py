from membersuite_api_client.utils import convert_ms_object
from membersuite_api_client.exceptions import ExecuteMSQLError


class Membership(object):

    def __init__(self, membership):
        """Create a Membership model from MemberSuite Member object
        """
        self.id = membership["ID"]
        self.owner = membership["Owner"]
