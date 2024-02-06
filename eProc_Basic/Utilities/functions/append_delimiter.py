def append_delimiter(data,value,delimiter):
    """

    """
    if not data:
        data = value
    else:
        data += delimiter + value
    return data