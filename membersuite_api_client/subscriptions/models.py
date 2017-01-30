"""
    Models the Subscription object in MemberSuite

    http://api.docs.membersuite.com/#References/Objects/Subscription.htm
"""


class Subscription(object):

    def __init__(self, id, org, start, end, extra_data={}):
        self.id = id
        self.org = org
        self.start = start
        self.end = end
        self.extra_data = extra_data  # all other fields, for reference
