"""
    The service for connecting to MemberSuite for SubscriptionService

    http://api.docs.membersuite.com/#References/Objects/Subscription.htm

    @todo
        set up fixtures in MemberSuite sandbox for integration testing
    @todo
        add date modified param for performance
"""
from ..mixins import ChunkQueryMixin
from ..utils import get_new_client
from .models import Subscription

import datetime


class SubscriptionService(ChunkQueryMixin, object):

    def __init__(self, client=None):
        """
        Accepts a ConciergeClient to connect with MemberSuite
        """
        super(SubscriptionService, self).__init__()
        self.client = client or get_new_client()

    def get_subscriptions(self, publication_id=None, owner_id=None,
                          since_when=None, limit_to=200, max_calls=None,
                          start_record=0, verbose=False):
        """
        Fetches all subscriptions from Membersuite of a particular
        `publication_id` if set.
        """
        query = "SELECT Objects() FROM Subscription"

        # collect all where parameters into a list of
        # (key, operator, value) tuples
        where_params = []

        if owner_id:
            where_params.append(('owner', '=', "'%s'" % owner_id))
        if publication_id:
            where_params.append(('publication', '=', "'%s'" % publication_id))
        if since_when:
            d = datetime.date.today() - datetime.timedelta(days=since_when)
            where_params.append(
                ('LastModifiedDate', ">", "'%s 00:00:00'" % d))

        if where_params:
            query += " WHERE "
            query += " AND ".join(
                ["%s %s %s" % (p[0], p[1], p[2]) for p in where_params])

        subscription_list = self.get_long_query(
            query, limit_to=limit_to, max_calls=max_calls,
            start_record=start_record, verbose=verbose)

        return subscription_list

    def ms_object_to_model(self, ms_obj):
        " Converts an individual result to a Subscription Model "
        return Subscription(membersuite_object_data=ms_obj)
