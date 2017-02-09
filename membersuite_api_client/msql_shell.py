#!/usr/bin/env python
"""A REPL for MSQL.

"""
import atexit
import os
import readline

import cmd2

from membersuite_api_client.client import ConciergeClient
from membersuite_api_client.utils import membersuite_object_factory


class NewStyleCmd2(object, cmd2.Cmd):
    """A cmd2.Cmd class that supports super().

    cmd2.Cmd is an "old style class", and that causes super() to throw
    a fit.  Turns out we really do need the logic in
    cmd22.Cmd.__init__(), so for our app we inherit from this
    NewStyleCmd2.

    """

    def __init__(self):
        super(object, self).__init__()


class MSQLShell(NewStyleCmd2):

    intro = "Welcome to the MSQL Shell.  Burp."
    prompt = "(MSQL) "
    history_file = os.path.expanduser("~/.msql_shell_history")

    def __init__(self):
        super(MSQLShell, self).__init__()
        self._client = None
        self.load_history()

    @property
    def client(self):
        if not self._client:
            self._client = ConciergeClient(
                access_key=os.environ["MS_ACCESS_KEY"],
                secret_key=os.environ["MS_SECRET_KEY"],
                association_id=os.environ["MS_ASSOCIATION_ID"])
        return self._client

    def load_history(self):
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                f.write('')
        readline.read_history_file(self.history_file)
        atexit.register(readline.write_history_file, self.history_file)

    def do_query(self, line):
        if not self.client.session_id:
            self.client.request_session()
        result = self.client.runSQL(line)
        msql_result = result["body"]["ExecuteMSQLResult"]
        if msql_result["Success"]:
            if msql_result["ResultValue"]["ObjectSearchResult"]["Objects"]:
                for obj in (msql_result["ResultValue"]["ObjectSearchResult"]
                            ["Objects"]["MemberSuiteObject"]):
                    membersuite_object = membersuite_object_factory(obj)
                    print(str(membersuite_object))
            else:
                membersuite_object = membersuite_object_factory(
                    msql_result["ResultValue"]["SingleObject"])
                print(str(membersuite_object))
        else:
            # @TODO Fix - showing only the first of possibly many errors here.
            print(self.colorize(str(msql_result["Errors"]["ConciergeError"]),
                                "red"))

    def default(self, line):
        self.do_query(line)


if __name__ == "__main__":
    app = MSQLShell()
    app.cmdloop()
