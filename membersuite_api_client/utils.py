def convert_ms_object(ms_object):
    """
    Converts the list of dictionaries with keys "key" and "value" into
    more logical value-key pairs in a plain dictionary.
    """
    out_dict = {}
    for item in ms_object:
        out_dict[item["Key"]] = item["Value"]
    return out_dict
