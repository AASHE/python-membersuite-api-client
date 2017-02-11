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
