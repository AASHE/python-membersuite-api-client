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

    def __init__(self, client):
        self.client = client

    def get_current_subscription(self, org_id):
        query = "SELECT Objects() FROM Subscription"
        query += " WHERE owner = '%s'" % org_id

        result = self.client.runSQL(query)

        if result["body"]["ExecuteMSQLResult"]["ResultValue"]["ObjectSearchResult"]["Objects"]:
            return(result["body"]["ExecuteMSQLResult"]["ResultValue"]
                   ["ObjectSearchResult"]["Objects"]["MemberSuiteObject"])
        else:
            return None
