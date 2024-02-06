from collections import deque


def list_remove_insert_first(array_list, insert_remove_element):
    """

    """
    if insert_remove_element:
        array_list.remove(str(insert_remove_element))
        array_list.insert(0, insert_remove_element)
    return array_list


def dictionary_remove_insert_first(dictionary_list, key, insert_remove_element):
    """

    """
    insert_dictionary = {}
    default_exist_flag = default_existance_check(dictionary_list, key, insert_remove_element)
    result = dictionary_list
    if default_exist_flag:
        for i in range(len(dictionary_list)):
            if dictionary_list[i][key] == insert_remove_element:
                insert_dictionary = dictionary_list[i]
                del dictionary_list[i]
                break
        remove_add_list = deque(dictionary_list)
        remove_add_list.appendleft(insert_dictionary)
        result = list(remove_add_list)
    return result


def default_existance_check(dictionary_list, key, value):
    """

    """
    for dictionary in dictionary_list:
        if dictionary[key] == value:
            return dictionary
    return None


def remove_dictionary_from_list(dictionary_list, key, remove_element):
    for i in range(len(dictionary_list)):
        if dictionary_list[i][key] == remove_element:
            insert_dictionary = dictionary_list[i]
            del dictionary_list[i]
            break
    return dictionary_list


def get_uncommon_elements_from_lists(list1,list2):
    return list(set(list1).symmetric_difference(set(list2)))
