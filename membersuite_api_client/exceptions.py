from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.utils import python_2_unicode_compatible


@python_2_unicode_compatible
class MemberSuiteAPIError(Exception):

    def __init__(self, result):
        self.result = result
        self.exception_type = self.__class__.__name__

    def __str__(self):
        concierge_error = self.get_concierge_error()
        return "<{exception_type} ConciergeError: {concierge_error}>".format(
            exception_type=self.exception_type,
            concierge_error=concierge_error)

    def get_concierge_error(self):
        try:
            return (self.result["body"][self.result_type]
                    ["Errors"]["ConciergeError"])
        except KeyError:
            return (self.result["Errors"])


class LoginToPortalError(MemberSuiteAPIError):
    pass


class LogoutError(MemberSuiteAPIError):
    pass


class ExecuteMSQLError(MemberSuiteAPIError):
    pass


class NoResultsError(MemberSuiteAPIError):
    pass


class NotAnObjectQuery(MemberSuiteAPIError):
    pass
