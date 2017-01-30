"""
    The service for connecting to MemberSuite for SubscriptionService

    http://api.docs.membersuite.com/#References/Objects/Subscription.htm

    @todo
        let's define an Organization object, like this Subscription,
        for this interface
    @todo
        confirm owner field is actually the orgnization
    @todo
        set up fixtures in MemberSuite for integration testing
    @todo
        add date modified param for performance
    @todo
        additional method for getting all subscriptions for syncing purposes
"""

from .models import Subscription


class SubscriptionService(object):

    def __init__(self, client):
        """
        Accepts a ConciergeClient to connect with MemberSuite
        """
        self.client = client

    def get_org_subscriptions(self, org_id, publication_id=None):
        """
        Get all the subscriptions for a given organization

        Returns a list of subscription objects
        """
        query = "SELECT Objects() FROM Subscription"
        query += " WHERE owner = '%s'" % org_id

        if publication_id:
            query += "AND publication = '%s'" % publication_id

        result = self.client.runSQL(query)
        mysql_result = result['body']['ExecuteMSQLResult']

        if not mysql_result['Errors']:
            obj_result = mysql_result['ResultValue']['ObjectSearchResult']
            objects = obj_result['Objects']['MemberSuiteObject']

            subscription_list = []
            for obj in objects:
                sane_obj = self.client.convert_ms_object(
                    obj['Fields']['KeyValueOfstringanyType'])
                subscription = Subscription(
                    id=sane_obj['ID'],
                    org=org_id,
                    start=sane_obj['StartDate'],
                    end=sane_obj['TerminationDate'],
                    extra_data=sane_obj)
                subscription_list.append(subscription)

            return subscription_list

        else:
            return None
