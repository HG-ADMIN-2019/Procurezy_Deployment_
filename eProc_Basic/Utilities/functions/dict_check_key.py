def checkKey(dict, key):
    for dict_value in dict:
        if key in dict_value:
            return True
    return False


def list_value_count(array):
    """

    :param array:
    :return:
    """
    array_count = {i: array.count(i) for i in array}
    return array_count
