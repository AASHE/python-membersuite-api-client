from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.utils import python_2_unicode_compatible

from .utils import convert_ms_object


@python_2_unicode_compatible
class MemberSuiteObject(object):

    def __init__(self, membersuite_object_data, membersuite_id=None):
        """Takes the Zeep'ed XML Representation of a MemberSuiteObject as
        input.

        """
        self.fields = convert_ms_object(
            membersuite_object_data["Fields"]["KeyValueOfstringanyType"])
        self.extra_data = membersuite_object_data
        self.membersuite_id = (self.fields["ID"]
                               if membersuite_id is None
                               else membersuite_id)

    def __str__(self):
        return ("<MemberSuiteObject: MemberSuite ID: {id}>".format(
            id=self.membersuite_id))
