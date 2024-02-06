def update_del_ind(dic_list):
    """

    """
    update_dictionary_list = []
    for dictionary in list(dic_list):
        if dictionary['del_ind']:
            dictionary['del_ind'] = 1
        else:
            dictionary['del_ind'] = 0
        values = dictionary.values()
        update_dictionary_list.append(list(values))
    return update_dictionary_list


def query_update_del_ind(dic_list):
    """

    """
    for dictionary in dic_list:
        if not dictionary['del_ind']:
            dictionary['del_ind'] = 0
    return dic_list
