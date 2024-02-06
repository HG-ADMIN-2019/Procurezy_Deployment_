def remove_duplicates_in_dic_list(dic_list):
    """

    :param dic_list:
    :return:
    """
    unique_list = [i for n, i in enumerate(dic_list) if i not in dic_list[n + 1:]]
    return unique_list


def remove_duplicate_element_array(array):
    """

    """
    result = []
    [result.append(x) for x in array if x not in result]
    return result
