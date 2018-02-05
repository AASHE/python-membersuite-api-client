from ..exceptions import ExecuteMSQLError
from ..utils import get_new_client
from .models import Order


def get_order(membersuite_id, client=None):
    """Get an Order by ID.
    """
    if not membersuite_id:
        return None

    client = client or get_new_client(request_session=True)
    if not client.session_id:
        client.request_session()

    object_query = "SELECT Object() FROM ORDER WHERE ID = '{}'".format(
        membersuite_id)

    result = client.execute_object_query(object_query)

    msql_result = result["body"]["ExecuteMSQLResult"]

    if msql_result["Success"]:
        membersuite_object_data = (msql_result["ResultValue"]
                                   ["SingleObject"])
    else:
        raise ExecuteMSQLError(result=result)

    return Order(membersuite_object_data=membersuite_object_data)
