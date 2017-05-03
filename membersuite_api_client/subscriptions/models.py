# -*- coding: utf-8 -*-
"""
    Models the Subscription object in MemberSuite

    http://api.docs.membersuite.com/#References/Objects/Subscription.htm
"""
from __future__ import unicode_literals

from ..models import MemberSuiteObject
from ..orders import services as orders_services


class Subscription(MemberSuiteObject):

    def __init__(self, membersuite_object_data):
        super(Subscription, self).__init__(
            membersuite_object_data=membersuite_object_data)
        self.owner_id = self.fields["Owner"]
        self.start_date = self.fields["StartDate"]
        self.expiration_date = self.fields["ExpirationDate"]
        self.name = self.fields["Name"]
        self.created_date = self.fields["CreatedDate"]
        self.order_id = self.fields["OriginalOrder"]

    def get_order(self, client=None):
        order = orders_services.get_order(membersuite_id=self.order_id,
                                          client=client)
        return order
