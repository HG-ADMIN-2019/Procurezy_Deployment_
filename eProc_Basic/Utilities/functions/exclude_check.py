def check_for_exclude(exclude_list, field_name):
    """
    check field contain in exclude string
    :param exclude_list:
    :param field_name:
    :return:
    """
    exclude_field_flag = False
    for exclude in exclude_list:
        if not field_name.find(exclude) == -1:
            exclude_field_flag = True
            break
    return exclude_field_flag
