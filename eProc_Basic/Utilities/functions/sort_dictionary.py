def sort_list_dictionary_key_values(sort_list, dictionary_list, dictionary_key):
    """

    """
    sorted_list = []
    for sort_value in sort_list:
        for dictionary_value in dictionary_list:
            if dictionary_value[dictionary_key] == sort_value:
                sorted_list.append(dictionary_value)
    return sorted_list


def sort_dic_list_by_value(dic_list, key):
    """

    """
    return sorted(dic_list, key=lambda d: d[key])
