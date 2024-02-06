def dictionary_check_value_based_for_key(dictionary_list, key, value):
    for dictionary in dictionary_list:
        if dictionary[key] == value:
            return True
    return False


def dictionary_check_get_value_based_for_key(dictionary_list, key, value):
    result = None
    for dictionary in dictionary_list:
        if dictionary[key] == value:
            result = dictionary
    return result
