"""
    The service for connecting to MemberSuite for MembershipService

    http://api.docs.membersuite.com/#References/Objects/Membership.htm

"""
import datetime

from ..mixins import ChunkQueryMixin
from ..utils import convert_ms_object
from .models import Membership, MembershipProduct


class MembershipService(ChunkQueryMixin, object):

    def __init__(self, client):
        """
        Requires a ConciergeClient to connect with MemberSuite
        """
        self.client = client

    def get_current_membership_for_org(self, account_num, verbose=False):
        """Return a current membership for this org, or, None if
        there is none.
        """
        all_memberships = self.get_memberships_for_org(
            account_num=account_num,
            verbose=verbose)
        # Look for first membership that hasn't expired yet.
        for membership in all_memberships:
            if (membership.expiration_date and
                membership.expiration_date > datetime.datetime.now()):  # noqa
                return membership  # noqa
        return None

    def get_memberships_for_org(self, account_num, verbose=False):
        """
        Retrieve all memberships associated with an organization,
        ordered by expiration date.
        """
        if not self.client.session_id:
            self.client.request_session()

        query = "SELECT Objects() FROM Membership " \
                "WHERE Owner = '%s' ORDER BY ExpirationDate" % account_num

        membership_list = self.get_long_query(query, verbose=verbose)
        return membership_list or []

    def get_all_memberships(
            self, limit_to=100, max_calls=None, parameters=None,
            since_when=None, start_record=0, verbose=False):
        """
        Retrieve all memberships updated since "since_when"

        Loop over queries of size limit_to until either a non-full queryset
        is returned, or max_depth is reached (used in tests). Then the
        recursion collapses to return a single concatenated list.
        """
        if not self.client.session_id:
            self.client.request_session()

        query = "SELECT Objects() FROM Membership"

        # collect all where parameters into a list of
        # (key, operator, value) tuples
        where_params = []

        if parameters:
            for k, v in parameters.items():
                where_params.append((k, "=", v))

        if since_when:
            d = datetime.date.today() - datetime.timedelta(days=since_when)
            where_params.append(
                ('LastModifiedDate', ">", "'%s 00:00:00'" % d))

        if where_params:
            query += " WHERE "
            query += " AND ".join(
                ["%s %s %s" % (p[0], p[1], p[2]) for p in where_params])

        query += " ORDER BY LocalID"

        # note, get_long_query is overkill when just looking at
        # one org, but it still only executes once
        # `get_long_query` uses `ms_object_to_model` to return Organizations
        membership_list = self.get_long_query(
            query, limit_to=limit_to, max_calls=max_calls,
            start_record=start_record, verbose=verbose)

        return membership_list or []

    def ms_object_to_model(self, ms_obj):
        " Converts an individual result to a Subscription Model "
        sane_obj = convert_ms_object(
            ms_obj['Fields']['KeyValueOfstringanyType'])
        return Membership(sane_obj)


class MembershipProductService(ChunkQueryMixin, object):

    def __init__(self, client):
        """
        Accepts a ConciergeClient to connect with MemberSuite
        """
        self.client = client

    def get_all_membership_products(self, verbose=False):
        """
        Retrieves membership product objects
        """
        if not self.client.session_id:
            self.client.request_session()

        query = "SELECT Objects() FROM MembershipDuesProduct"

        membership_product_list = self.get_long_query(query, verbose=verbose)
        return membership_product_list or []

    def ms_object_to_model(self, ms_obj):
        " Converts an individual result to a Subscription Model "
        sane_obj = convert_ms_object(
            ms_obj['Fields']['KeyValueOfstringanyType'])
        return MembershipProduct(sane_obj)
