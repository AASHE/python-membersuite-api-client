"""
    The service for connecting to MemberSuite for SubscriptionService

    http://api.docs.membersuite.com/#References/Objects/Subscription.htm

    @todo
        set up fixtures in MemberSuite sandbox for integration testing
    @todo
        add date modified param for performance
"""

from .models import Subscription
from ..exceptions import ExecuteMSQLError
from ..mixins import ChunkQueryMixin
from ..utils import convert_ms_object

import datetime


class SubscriptionService(ChunkQueryMixin, object):

    def __init__(self, client):
        """
        Accepts a ConciergeClient to connect with MemberSuite
        """
        self.client = client

    def get_subscriptions(
            self, publication_id=None, org_id=None, since_when=None,
            retry_attempts=2, limit_to=200, max_calls=None):
        """
        Fetches all subscriptions from Membersuite of a particular
        `publication_id` if set.
        """
        query = "SELECT Objects() FROM Subscription"
        if org_id:
            query += " WHERE owner = '%s'" % org_id
        if publication_id:
            query += " AND publication = '%s'" % publication_id
        if since_when:
            query += " AND LastModifiedDate > '{since_when} 00:00:00'" \
                .format(since_when=datetime.date.today() -
                        datetime.timedelta(days=since_when))

        # note, get_long_query is overkill when just looking at
        # one org, but it still only executes once
        # `get_long_query` uses `ms_object_to_model` to return Subscriptions
        subscription_list = self.get_long_query(
            query, retry_attempts=retry_attempts, limit_to=limit_to,
            max_calls=max_calls)

        return subscription_list

    def ms_object_to_model(self, ms_obj):
        " Converts an individual result to a Subscription Model "
        sane_obj = convert_ms_object(
            ms_obj['Fields']['KeyValueOfstringanyType'])
        subscription = Subscription(
            id=sane_obj['ID'],
            org_id=sane_obj['Owner'],
            start=sane_obj['StartDate'],
            end=sane_obj['TerminationDate'],
            extra_data=sane_obj)
        return subscription
