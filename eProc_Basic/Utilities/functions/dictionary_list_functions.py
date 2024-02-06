from eProc_Basic.Utilities.global_defination import global_variables


def rename_dictionary_list_key(old_key, new_key, dictionary_list):
    for dictionary in dictionary_list:
        dictionary[new_key] = dictionary.pop(old_key)
        dictionary['client'] = global_variables.GLOBAL_CLIENT
        dictionary['del_ind'] = False
    return dictionary_list


def update_key_value_with_new_key_dictionary_list(dictionary_list,old_key, new_key):
    for dictionary in dictionary_list:
        dictionary[new_key] = dictionary[old_key]
    return dictionary_list
