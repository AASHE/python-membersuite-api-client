class MemberSuiteAPIError(Exception):
    def __init__(self, result):
        self.result = result


class LoginToPortalError(MemberSuiteAPIError):
    pass


class ExecuteMSQLError(MemberSuiteAPIError):
    pass
