import os

from .exceptions import ExecuteMSQLError


def convert_ms_object(ms_object):
    """
    Converts the list of dictionaries with keys "key" and "value" into
    more logical value-key pairs in a plain dictionary.
    """
    out_dict = {}
    for item in ms_object:
        out_dict[item["Key"]] = item["Value"]
    return out_dict


def get_session_id(result):
    """Returns the Session ID for an API result.

    When there's no Session ID, returns None.
    """
    try:
        return result["header"]["header"]["SessionId"]
    except TypeError:
        return None


def membersuite_object_factory(membersuite_object_data):
    from .models import MemberSuiteObject
    import membersuite_api_client.security.models as security_models

    klasses = {"Individual": security_models.Individual,
               "PortalUser": security_models.PortalUser}

    try:
        klass = klasses[membersuite_object_data["ClassType"]]
    except KeyError:
        return MemberSuiteObject(
            membersuite_object_data=membersuite_object_data)
    else:
        return klass(membersuite_object_data=membersuite_object_data)


def get_new_client():
    """Return a new ConciergeClient, pulling secrets from the environment.

    """
    from .client import ConciergeClient
    return ConciergeClient(access_key=os.environ["MS_ACCESS_KEY"],
                           secret_key=os.environ["MS_SECRET_KEY"],
                           association_id=os.environ["MS_ASSOCIATION_ID"])


def submit_msql_query(query, client=None):
    """Submit `query` to MemberSuite, returning .models.MemberSuiteObjects.

    So this is a converter from MSQL to .models.MemberSuiteObjects.

    Returns query results as a list of MemberSuiteObjects.

    """
    if client is None:
        client = get_new_client()
    if not client.session_id:
        client.request_session()

    result = client.runSQL(query)
    execute_msql_result = result["body"]["ExecuteMSQLResult"]

    membersuite_object_list = []

    if execute_msql_result["Success"]:
        result_value = execute_msql_result["ResultValue"]
        if result_value["ObjectSearchResult"]["Objects"]:
            # Multiple results.
            membersuite_object_list = []
            for obj in (result_value["ObjectSearchResult"]["Objects"]
                        ["MemberSuiteObject"]):
                membersuite_object = membersuite_object_factory(obj)
                membersuite_object_list.append(membersuite_object)
        elif result_value["SingleObject"]["ClassType"]:
            # Only one result.
            membersuite_object = membersuite_object_factory(
                execute_msql_result["ResultValue"]["SingleObject"])
            membersuite_object_list.append(membersuite_object)
        elif (result_value["ObjectSearchResult"]["Objects"] is None and
              result_value["SingleObject"]["ClassType"] is None):
            # No results, I guess.
            pass
        return membersuite_object_list
    else:
        # @TODO Fix - exposing only the first of possibly many errors here.
        raise ExecuteMSQLError(result=execute_msql_result)
