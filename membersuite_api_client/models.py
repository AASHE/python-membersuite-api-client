from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.utils import python_2_unicode_compatible

from .utils import convert_ms_object


@python_2_unicode_compatible
class MemberSuiteObject(object):

    def __init__(self, membersuite_object_data):
        """Takes the Zeep'ed XML Representation of a MemberSuiteObject as
        input.

        """
        self.fields = convert_ms_object(
            membersuite_object_data["Fields"]["KeyValueOfstringanyType"])

        self.id = self.fields["ID"]
        self.extra_data = membersuite_object_data

    def __str__(self):
        return ("<MemberSuiteObject: ID: {id}>".format(id=self.id))
