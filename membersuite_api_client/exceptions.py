from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.utils import python_2_unicode_compatible


@python_2_unicode_compatible
class MemberSuiteAPIError(Exception):

    def __init__(self, result):
        self.result = result

    def __str__(self):
        concierge_error = self.get_concierge_error()
        return "<{classname} ConciergeError: {concierge_error}>".format(
            classname=self.__class__.__name__,
            concierge_error=concierge_error)

    def get_concierge_error(self):
        try:
            return (self.result["body"][self.result_type]
                    ["Errors"]["ConciergeError"])
        except KeyError:
            return (self.result["Errors"])


class LoginToPortalError(MemberSuiteAPIError):

    result_type = "LoginToPortalResult"


class LogoutError(MemberSuiteAPIError):

    result_type = "LogoutResult"


class ExecuteMSQLError(MemberSuiteAPIError):

    result_type = "ExecuteMSQLResult"
