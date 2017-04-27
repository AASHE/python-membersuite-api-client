"""
    Models the Subscription object in MemberSuite

    http://api.docs.membersuite.com/#References/Objects/Subscription.htm
"""


class Subscription(object):

    def __init__(self, id, org_id, name, start, end, extra_data={}):
        self.id = id
        self.org_id = org_id
        self.name = name
        self.start = start
        self.end = end
        self.extra_data = extra_data  # all other fields, for reference
