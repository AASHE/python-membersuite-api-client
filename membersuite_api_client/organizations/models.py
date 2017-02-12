class Organization(object):

    def __init__(self, org):
        """Create an Organization model from MemberSuite Organization object
        """
        self.account_num = org["ID"]
        self.id = self.account_num
        self.membersuite_id = org["LocalID"]
        self.local_id = self.membersuite_id
        self.org_name = org["Name"]
        self.name = self.org_name
        self.picklist_name = org["SortName"] or ''

        address = org["Mailing_Address"]
        if address:
            self.street1 = address["Line1"] or ''
            self.street2 = address["Line2"] or ''
            self.city = address["City"] or ''
            self.state = address["State"] or ''
            self.country = address["Country"]
            self.postal_code = address["PostalCode"] or ''
            self.latitude = address["GeocodeLat"] or ''
            self.longitude = address["GeocodeLong"] or ''

        self.website = org["WebSite"] or ''
        self.exclude_from_website = False
        self.is_defunct = (org["Status"] == 'Defunct')

        self.org_type = org["Type"]

        self.stars_participant_status = (
            'STARS participant' if org["STARSCharterParticipant__c"] else ''
        )

        self.primary_email = org['EmailAddress'] or ''


class OrganizationType(object):

    def __init__(self, org_type):
        """Create an OrganizationType model
        from MemberSuite OrganizationType object
        """
        self.id = org_type["ID"]
        self.Name = org_type["Name"]

STATUSES = {
    '6faf90e4-01f3-c54c-f01a-0b3bc87640ab': 'Active',
    '6faf90e4-01f3-c0f1-4593-0b3c3ca7ff6c': 'Deceased',
    '6faf90e4-01f3-c7ad-174c-0b3c52b7f497': 'Defunct',
    '6faf90e4-01f3-cd50-ffed-0b3c3ca7f4fd': 'Retired',
}
