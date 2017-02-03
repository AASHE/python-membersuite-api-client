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
