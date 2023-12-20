"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    upload_specific.py
Usage:
get_date_value - get str and convert into datetime
str_decimal - get str and convert into decimal

Author:
    Deepika K/Shreyas
"""

# convert string to datetime format
from datetime import datetime
from decimal import Decimal
from decimal import Decimal


def get_date_value(str_value):
    """
    get str and convert into datetime
    :param str_value: str date
    :return: datetime
    """

    input_formats = [
        '%d.%m.%Y %H:%M:%S',
        '%m/%d/%Y %H:%M:%S',
        '%m-%d-%Y %H:%M:%S',
        '%Y.%m.%d %H:%M:%S',
        '%Y/%m/%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S',
        '%m/%d/%Y %H:%M',
        '%Y%m%d',
        '%d/%m/%Y',
        '%m/%d/%Y'
    ]

    for format in input_formats:
        try:
            return datetime.strptime(str_value, format)
        except (ValueError, TypeError):
            continue


def str_decimal(stringvalue):
    """
    get str and convert into decimal
    :param stringvalue: str data
    :return: decimal value
    """
    if (stringvalue):
        return Decimal(stringvalue)
    else:
        return 0


def convert_query_set_list(query_set_value):
    """
    Convert Query set into list
    :return:
    """
    query_set_list = [entry for entry in query_set_value]

    return query_set_list


def type_cast_array_str_to_int(str_array):
    """

    :param str_array:
    :return:
    """
    return [int(str_data) for str_data in str_array]


def type_cast_array_str_to_float(str_array):
    """

    :param str_array:
    :return:
    """
    return [float(str_data) for str_data in str_array]

def type_cast_array_str_to_decimal(str_array):
    """

    :param str_array:
    :return:
    """
    return [Decimal(str_data) for str_data in str_array]


def type_cast_array_float_to_str(str_array):
    """

    :param str_array:
    :return:
    """
    return [str(str_data) for str_data in str_array]


def date_to_diff_days(created_date):
    """

    :param created_date:
    :return:
    """
    weeks = 0
    today_date = datetime.datetime.now()
    days, hours, minutes, seconds = dhms_from_seconds(date_diff_in_seconds(today_date, created_date))
    diff_days = str(days) + 'D ' + str(hours) + 'H ' + str(minutes) + 'M ' + str(seconds) + 'S '
    if int(days) == 0 and int(hours) == 0 and int(minutes) == 0:
        diff_days = str(seconds) + 'S '
    elif int(days) == 0 and int(hours) == 0 and int(minutes) in range(1, 60):
        diff_days = str(minutes) + 'M '
    elif int(days) == 0 and int(hours) in range(1, 24):
        diff_days = str(hours) + 'H '
    elif int(days) in range(1, 7):
        diff_days = str(days) + 'D '
    elif int(days) >= 7:
        weeks, days = divmod(days, 7)
        diff_days = str(weeks) + 'W '

    return diff_days


def date_diff_in_seconds(dt2, dt1):
    """

    :param dt2:
    :param dt1:
    :return:
    """
    timedelta = dt2 - dt1
    return timedelta.days * 24 * 3600 + timedelta.seconds


def dhms_from_seconds(seconds):
    """

    :param seconds:
    :return:
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return days, hours, minutes, seconds


def integer_type_caste(value):
    if value:
        value = int(value)
    else:
        value = 0
    return value


def decimal_type_caste(value):
    if value:
        value = Decimal(value)
    else:
        value = Decimal(0)
    return value