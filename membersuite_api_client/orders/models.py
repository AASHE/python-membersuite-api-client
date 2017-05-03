from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.utils import python_2_unicode_compatible

from ..models import MemberSuiteObject
from ..utils import get_new_client, value_for_key
from ..financial import services as financial_services


@python_2_unicode_compatible
class OrderLineItem(MemberSuiteObject):

    def __init__(self, membersuite_object_data, session_id=None):
        """Create an OrderLineItem object from a the Zeep'ed XML
        representation of a Membersuite OrderLineItem.

        """
        membersuite_id = value_for_key(
            membersuite_object_data=membersuite_object_data,
            key="OrderLineItemID")
        super(OrderLineItem, self).__init__(
            membersuite_object_data=membersuite_object_data,
            membersuite_id=membersuite_id)
        self.product_id = self.fields["Product"]
        self.session_id = session_id

    def __str__(self):
        return ("<Order: ID: {id}, product: {product} "
                " session_id: {session_id}>".format(
                    id=self.membersuite_id,
                    product=self.product,
                    session_id=self.session_id))

    def get_product(self, client=None):
        """Return a Product object for this line item.
        """
        client = client or get_new_client(request_session=True)
        if not client.session_id:
            client.request_session()

        product = financial_services.get_product(
            membersuite_id=self.product_id,
            client=client)

        return product


@python_2_unicode_compatible
class Order(MemberSuiteObject):

    def __init__(self, membersuite_object_data, session_id=None):
        """Create an Order object from a the Zeep'ed XML representation of
        a Membersuite Order.

        """
        super(Order, self).__init__(
            membersuite_object_data=membersuite_object_data)
        self.session_id = session_id

    def __str__(self):
        return ("<Order: ID: {id}, Line Items: {line_items} "
                " session_id: {session_id}>".format(
                    id=self.membersuite_id,
                    line_items=self.line_items,
                    session_id=self.session_id))

    @property
    def line_items(self):
        """Returns the OrderLineItem objects for line items
        in this order.
        """
        membersuite_object_data = (
            self.fields["LineItems"]["MemberSuiteObject"])
        line_items = []
        for datum in membersuite_object_data:
            line_items.append(OrderLineItem(membersuite_object_data=datum))
        return line_items

    def get_products(self, client=None):
        """A list of Product objects in this Order.
        """
        client = client or get_new_client(request_session=True)
        if not client.session_id:
            client.request_session()
        products = []
        for line_item in self.line_items:
            products.append(line_item.get_product(client=client))
        return products
