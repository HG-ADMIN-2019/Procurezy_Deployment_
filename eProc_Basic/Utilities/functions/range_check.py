def range_check(data,from_range,to_range):
    """

    :param data:
    :param from_range:
    :param to_range:
    :return:
    """
    if int(data) in range(int(from_range), int(to_range)+1):
        return True

    return False
