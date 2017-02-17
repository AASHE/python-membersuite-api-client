class Membership(object):

    def __init__(self, membership):
        """ Create a Membership model from MemberSuite Membership object
        """
        self.id = membership["ID"]
        self.owner = membership["Owner"]
        self.membership_directory_opt_out = \
            membership["MembershipDirectoryOptOut"]
        self.receives_member_benefits = membership["ReceivesMemberBenefits"]
        self.current_dues_amount = membership["CurrentDuesAmount"]
        self.expiration_date = membership["ExpirationDate"]
        self.type = membership["Type"]
        self.product = membership["Product"]
        self.last_modified_date = membership["LastModifiedDate"]

        self.status = membership["Status"]
        self.join_date = membership["JoinDate"]
        self.termination_date = membership["TerminationDate"]
        self.renewal_date = membership["RenewalDate"]


class MembershipProduct(object):

    def __init__(self, membership_type):
        """ Create a MembershipType model from MembershipDuesProduct object
        """
        self.id = membership_type["ID"]
        self.name = membership_type["Name"]

STATUSES = {
    '6faf90e4-0069-cf2c-650f-0b3c15a7d3aa': 'Expired',
    '6faf90e4-0069-cd19-6a43-0b3c15a7c287': 'New Member',
    '6faf90e4-0069-c450-a9c8-0b3c6a781755': 'Pending',
    '6faf90e4-0069-c7d5-2e88-0b3c15a7cf8a': 'Reinstated',
    '6faf90e4-0069-c2ef-6d51-0b3c15a7cb7f': 'Renewed',
    '6faf90e4-0069-cebb-b501-0b3c15a7d742': 'Terminated',
}

TYPES = {
    '6faf90e4-006a-c1e7-1ac8-0b3c2f7cb3bc': 'Business',
    '6faf90e4-006a-c2ae-40f5-0b3c5c99549d': 'International Institution',
    '6faf90e4-006a-c242-d6ab-0b3c5c994f57': 'North American Institution',
    '6faf90e4-006a-c6b0-10c0-0b3c2f7cc1c5': 'Other',
    '6faf90e4-006a-c71f-2f32-0b3c2f7cbbee': 'Campus',
    '6faf90e4-006a-c85d-2efa-0b3c2f7ca9cc': 'HEASC Membership',
    '6faf90e4-006a-c9c7-5aa2-0b3bc8775e74': 'New Member',
    '6faf90e4-006a-c904-255d-0b3bc8774c95': 'Regained Membership',
}
