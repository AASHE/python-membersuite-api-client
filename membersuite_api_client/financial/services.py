from ..exceptions import ExecuteMSQLError
from ..utils import get_new_client
from .models import Product


def get_product(membersuite_id, client=None):
    """Return a Product object by ID.
    """
    if not membersuite_id:
        return None

    client = client or get_new_client(request_session=True)

    object_query = "SELECT Object() FROM PRODUCT WHERE ID = '{}'".format(
        membersuite_id)

    result = client.execute_object_query(object_query)

    msql_result = result["body"]["ExecuteMSQLResult"]

    if msql_result["Success"]:
        membersuite_object_data = (msql_result["ResultValue"]
                                   ["SingleObject"])
    else:
        raise ExecuteMSQLError(result=result)

    return Product(membersuite_object_data=membersuite_object_data)
