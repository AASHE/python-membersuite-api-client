from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.utils import python_2_unicode_compatible

from ..models import MemberSuiteObject


@python_2_unicode_compatible
class Product(MemberSuiteObject):

    def __init__(self, membersuite_object_data, session_id=None):
        """Create an Product object from a the Zeep'ed XML
        representation of a Membersuite Product.

        """
        super(Product, self).__init__(
            membersuite_object_data=membersuite_object_data)
        self.name = self.fields['Name']
