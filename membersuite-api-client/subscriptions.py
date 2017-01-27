"""
    get_subscriptions_for_org
    get_current_subscription_for_org
"""


class STARSSubscription(object):

    def __init__(self, subscription_id, org, start, end):
        self.id = subscription_id
        self.org = org
        self.start = start
        self.end = end


class STARSSubscriptionService(object):
    """

    """

    STARS_PUBLICATION_ID = '6faf90e4-009e-cb9b-7c9e-0b3bcd6dff6a'

    def __init__(self, client):
        self.client = client

    def get_subscriptions(self, org_id):
        query = "SELECT Objects() FROM Subscription"
        query += " WHERE owner = '%s' AND publication = '%s'" % (
            org_id, self.STARS_PUBLICATION_ID)

        result = self.client.runSQL(query)

        mysql_result = result['body']['ExecuteMSQLResult']
        if !mysql_result['Errors']:
            obj_result = mysql_result['ResultValue']['ObjectSearchResult']
            objects = obj_result['Objects']['MemberSuiteObject']
            # todo - convert to Subscription objects
            return objects
        else:
            return None
