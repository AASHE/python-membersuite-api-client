"""
    The service for accessing STARS Subscriptions from MemberSuite

    @todo
        let's define an Organization object, like this Subscription,
        for this interface
    @todo
        confirm owner field is actually the orgnization
    @todo
        confirm STARS_PUBLICATION_ID
    @todo
        set up fixtures in MemberSuite for integration testing
    @todo
        add date modified param for performance
    @todo
        additional method for getting all subscriptions for syncing purposes
"""


class STARSSubscription(object):

    def __init__(self, id, org, start, end, extra_data={}):
        self.id = id
        self.org = org
        self.start = start
        self.end = end
        self.extra_data = extra_data  # all other fields, for reference


class STARSSubscriptionService(object):

    STARS_PUBLICATION_ID = '6faf90e4-009e-cb9b-7c9e-0b3bcd6dff6a'

    def __init__(self, client):
        self.client = client

    def get_subscriptions(self, org_id):
        """
        Get all the subscriptions for a given organization

        Returns a list of subscription objects
        """
        query = "SELECT Objects() FROM Subscription"
        query += " WHERE owner = '%s' AND publication = '%s'" % (
            org_id, self.STARS_PUBLICATION_ID)

        result = self.client.runSQL(query)
        mysql_result = result['body']['ExecuteMSQLResult']

        if not mysql_result['Errors']:
            obj_result = mysql_result['ResultValue']['ObjectSearchResult']
            objects = obj_result['Objects']['MemberSuiteObject']

            subscription_list = []
            for obj in objects:
                sane_obj = self.client.convert_ms_object(
                    obj['Fields']['KeyValueOfstringanyType'])
                subscription = STARSSubscription(
                    id=sane_obj['ID'],
                    org=org_id,
                    start=sane_obj['StartDate'],
                    end=sane_obj['TerminationDate'],
                    extra_data=sane_obj)
                subscription_list.append(subscription)

            return subscription_list

        else:
            return None
