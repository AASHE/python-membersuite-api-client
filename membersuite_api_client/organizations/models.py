class Organization(object):

    def __init__(self, org):
        """Create an Organization model from MemberSuite Organization object
        """
        self.account_num = org["ID"]
