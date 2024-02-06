"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    str_concatenate.py
Usage:
concatenate_str - concatenate string1 and string2 with " - "
Author:
    Deepika K
"""


def concatenate_str(string1, string2):
    """
    concatenate string1 and string2 with " - "
    :param string1:first element of str
    :param string2:second element of str
    :return: returns value(string1) - value(string1)
    """
    apend_value = string1 + ' - ' + string2
    return apend_value


def concatenate_array_str(string1, string2):
    """
    concatenate string1 and string2 with " - "
    :param string1:first element of str
    :param string2:second element of str
    :return: returns value(string1) - value(string1)
    """
    append_value_desc = []
    for (str_val1, str_val2) in zip(string1, string2):
        append_value_desc.append(str_val1 + ' - ' + str_val2)
    return append_value_desc


def split_str(value, delimiter):
    """

    :param value:
    :param delimiter:
    :return:
    """
    split_value = value.split(delimiter)
    return split_value[0]


def concatenate_str_with_space(string1, string2):
    """
    concatenate string1 and string2 with "  " empty space
    :param string1:first element of str
    :param string2:second element of str
    :return: returns value(string1) - value(string1)
    """
    apend_value = string1 + ' ' + string2
    return apend_value
