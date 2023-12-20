def dictionary_key_to_list(dictionary_list,key):
    """

    :param dictionary_list:
    :param key:
    :return:
    """
    value_list = [dictionary[key] for dictionary in dictionary_list]
    return value_list