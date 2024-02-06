import calendar
from datetime import date
import datetime

from eProc_Attributes.Utilities.attributes_generic import OrgAttributeValues
from eProc_Basic.Utilities.constants.constants import CONST_CALENDAR_ID, CONST_CO_CODE, CONST_PR_CALLOFF, \
    CONST_CATALOG_CALLOFF, CONST_FREETEXT_CALLOFF, CONST_LIMIT_ORDER_CALLOFF
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import requester_field_info
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import SupplierMaster, CalenderConfig, CalenderHolidays

from eProc_User_Settings.Utilities.user_settings_generic import get_object_id_list_user

django_query_instance = DjangoQueries()


# Function to determine week day based on day number
def determine_day_by_day_number(day):
    """
    :param day:
    :return:
    """
    if day == 1:
        return 'Monday'
    elif day == 2:
        return 'Tuesday'
    elif day == 3:
        return 'Wednesday'
    elif day == 4:
        return 'Thursday'
    elif day == 5:
        return 'Friday'
    elif day == 6:
        return 'Saturday'
    else:
        return 'Sunday'


# Function to get list of holidays based on calender ID
def get_list_of_holidays(calender_id, client):
    """
    :param calender_id:
    :param client:
    :return:
    """
    get_holidays = django_query_instance.django_filter_only_query(CalenderHolidays, {
        'calender_id': calender_id, 'client': client, 'del_ind': False
    })

    from_date = list(get_holidays.values_list('from_date', flat=True))
    to_date = list(get_holidays.values_list('to_date', flat=True))
    holiday_list = list(set(from_date + to_date))

    return holiday_list


# Function to get weekdays and weekends based on working days which will be in the format (1,2,3,4,5,6,7)
def determine_working_days(working_days):
    week_days = []
    holidays = []
    working_days = working_days.split(',')
    for day in range(1, 8):
        if str(day) in working_days:
            week_day = determine_day_by_day_number(day)
            week_days.append(week_day)
        else:
            holidays.append(determine_day_by_day_number(day))
    return week_days, holidays


# Function to determine how many times each day appears between two given dates. Returns a dictionary
def weekday_count(start, end):
    """
    :param start:
    :param end:
    :return:
    """
    week = {}
    for i in range((end - start).days):
        day = calendar.day_name[(start + datetime.timedelta(days=i + 1)).weekday()]
        week[day] = week[day] + 1 if day in week else 1
    return week


# Function to calculate delivery date based on the parameters provided
def calculate_delivery_date(guid, lead_time, supplier_id, calender_id, client, model):
    """
    :param guid:
    :param lead_time:
    :param supplier_id:
    :param calender_id:
    :param client:
    :param model:
    :return:
    """
    is_supplier_holiday = True
    get_requester_working_days = django_query_instance.django_get_query(CalenderConfig, {'calender_id': calender_id,
                                                                                         'client': client})
    if get_requester_working_days is not None:
        requester_working_days = get_requester_working_days.working_days
        requester_week_days = (determine_working_days(requester_working_days))[0]
        requester_weekends = (determine_working_days(requester_working_days))[1]
        current_date = date.today()
        current_day = calendar.day_name[current_date.weekday()]
        requester_holiday_list = get_list_of_holidays(calender_id, client)
        valid_date = current_date
        valid_day = current_day

        if supplier_id is not None and supplier_id != 'None':
            get_supplier_working_days = django_query_instance.django_get_query(SupplierMaster,
                                                                               {'supplier_id': supplier_id,
                                                                                'client': client})
            supplier_working_days = get_supplier_working_days.delivery_days
            if supplier_working_days == '' or supplier_working_days is None:
                return None

            supplier_week_days = (determine_working_days(supplier_working_days))[0]
            while is_supplier_holiday:
                if valid_day in supplier_week_days:
                    # Add lead time to the valid date and update the valid date
                    valid_date = valid_date + datetime.timedelta(days=lead_time)
                    # Check number of holidays between date before adding lead time and date after adding leadtime
                    validated_dates = get_date_after_lead_time(supplier_working_days, current_date, valid_date)
                    valid_date = validated_dates[0]
                    valid_day = validated_dates[1]
                    break
                else:
                    # Add one day until the day is valid
                    valid_date = valid_date + datetime.timedelta(days=1)
                    valid_day = calendar.day_name[valid_date.weekday()]

            delivery_date = update_delivery_date(requester_working_days, requester_week_days, valid_date,
                                                 requester_holiday_list, model, guid)
            return delivery_date

        else:
            valid_date = current_date + datetime.timedelta(days=lead_time)
            valid_day = calendar.day_name[valid_date.weekday()]
            delivery_date = update_delivery_date(requester_working_days, requester_week_days, valid_date,
                                                 requester_holiday_list, model, guid)
            return delivery_date

    return None


# def calculate_delivery_date_base_on_lead_time(lead_time,supplier_id):
#     """
#
#     """
#     requester_working_days = ''
#     is_supplier_holiday = True
#     requester_week_days = ''
#     org_attr_value_instance = OrgAttributeValues()
#     current_date = date.today()
#     object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT, global_variables.GLOBAL_LOGIN_USER_OBJ_ID)
#
#     default_calendar_id = org_attr_value_instance.get_user_default_attr_value_list_by_attr_id(object_id_list,
#                                                                                               CONST_CALENDAR_ID)[
#         1]
#     get_requester_working_days = django_query_instance.django_get_query(CalenderConfig,
#                                                                         {'calender_id': default_calendar_id,
#                                                                          'client': global_variables.GLOBAL_CLIENT})
#     if get_requester_working_days is not None:
#         requester_working_days = get_requester_working_days.working_days
#         requester_week_days = (determine_working_days(requester_working_days))[0]
#         requester_holiday_list = get_list_of_holidays(default_calendar_id, global_variables.GLOBAL_CLIENT)
#         valid_date = current_date + datetime.timedelta(days=int(lead_time))
#     if supplier_id is not None and supplier_id != 'None':
#         get_supplier_working_days = django_query_instance.django_get_query(SupplierMaster,
#                                                                            {'supplier_id': supplier_id,
#                                                                             'client': global_variables.GLOBAL_CLIENT})
#         supplier_working_days = get_supplier_working_days.delivery_days
#         if supplier_working_days == '' or supplier_working_days is None:
#             return None
#
#         supplier_week_days = (determine_working_days(supplier_working_days))[0]
#         while is_supplier_holiday:
#             if valid_day in supplier_week_days:
#                 # Add lead time to the valid date and update the valid date
#                 valid_date = valid_date + datetime.timedelta(days=lead_time)
#                 # Check number of holidays between date before adding lead time and date after adding leadtime
#                 validated_dates = get_date_after_lead_time(supplier_working_days, current_date, valid_date)
#                 valid_date = validated_dates[0]
#                 valid_day = validated_dates[1]
#                 break
#             else:
#                 # Add one day until the day is valid
#                 valid_date = valid_date + datetime.timedelta(days=1)
#                 valid_day = calendar.day_name[valid_date.weekday()]
#
#         delivery_date = update_delivery_date(requester_working_days, requester_week_days, valid_date,
#                                              requester_holiday_list, model, guid)
#         return delivery_date
#
#
#     delivery_date = get_delivery_date(requester_working_days, requester_week_days, valid_date,
#                                          requester_holiday_list)
#     return delivery_date

def calculate_delivery_date_base_on_lead_time(lead_time, supplier_id, default_calendar_id):
    """

    """
    if not default_calendar_id:
        object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT,
                                                 global_variables.GLOBAL_LOGIN_USER_OBJ_ID)
        org_attr_value_instance = OrgAttributeValues()
        default_calendar_id = org_attr_value_instance.get_user_default_attr_value_list_by_attr_id(object_id_list,
                                                                                                  CONST_CALENDAR_ID)[1]
    is_supplier_holiday = True
    get_requester_working_days = django_query_instance.django_get_query(CalenderConfig,
                                                                        {'calender_id': default_calendar_id,
                                                                         'client': global_variables.GLOBAL_CLIENT})
    if get_requester_working_days is not None:
        requester_working_days = get_requester_working_days.working_days
        requester_week_days = (determine_working_days(requester_working_days))[0]
        # requester_weekends = (determine_working_days(requester_working_days))[1]
        current_date = date.today()
        current_day = calendar.day_name[current_date.weekday()]
        requester_holiday_list = get_list_of_holidays(default_calendar_id, global_variables.GLOBAL_CLIENT)
        valid_date = current_date
        valid_day = current_day

        if supplier_id is not None and supplier_id != 'None':
            get_supplier_working_days = django_query_instance.django_get_query(SupplierMaster,
                                                                               {'supplier_id': supplier_id,
                                                                                'client': global_variables.GLOBAL_CLIENT})
            supplier_working_days = get_supplier_working_days.delivery_days
            if supplier_working_days == '' or supplier_working_days is None:
                return None

            supplier_week_days = (determine_working_days(supplier_working_days))[0]
            while is_supplier_holiday:
                if valid_day in supplier_week_days:
                    # Add lead time to the valid date and update the valid date
                    valid_date = valid_date + datetime.timedelta(days=int(lead_time))
                    # Check number of holidays between date before adding lead time and date after adding leadtime
                    validated_dates = get_date_after_lead_time(supplier_working_days, current_date, valid_date)
                    valid_date = validated_dates[0]
                    # valid_day = validated_dates[1]
                    break
                else:
                    # Add one day until the day is valid
                    valid_date = valid_date + datetime.timedelta(days=1)
                    valid_day = calendar.day_name[valid_date.weekday()]

            delivery_date = get_delivery_date(requester_working_days, requester_week_days, valid_date,
                                              requester_holiday_list)
            return delivery_date

        else:
            valid_date = current_date + datetime.timedelta(days=int(lead_time))
            # valid_day = calendar.day_name[valid_date.weekday()]
            delivery_date = get_delivery_date(requester_working_days, requester_week_days, valid_date,
                                              requester_holiday_list)
            return delivery_date

    return None


# Function to get valid date and valid day after adding leadtime
def get_date_after_lead_time(working_days, current_date, valid_date):
    """
    :param working_days:
    :param current_date:
    :param valid_date:
    :returns two outputs 1) valid date 2) valid day

    After adding leadtime to the date, this function checks if there are any holidays between today's date and
    date after adding leadtime and adds number of holidays between the two dates.
    """
    number_of_holidays_added = []
    get_holidays_list = (determine_working_days(working_days))[1]
    get_number_weekdays = weekday_count(current_date, valid_date)

    for data in get_holidays_list:
        if data in get_number_weekdays:
            number_of_holidays_added.append(get_number_weekdays[data])
    sum_of = sum(number_of_holidays_added)
    valid_date = valid_date + datetime.timedelta(days=sum_of + 1)
    valid_day = calendar.day_name[valid_date.weekday()]
    return valid_date, valid_day


# Function to determine delivery date and update to DB after supplier date validation
def update_delivery_date(requester_working_days, requester_week_days, valid_date, requester_holiday_list, model, guid):
    """
    :param requester_working_days:
    :param requester_week_days:
    :param valid_date:
    :param requester_holiday_list:
    :param model:
    :param guid:
    :return:
    """
    current_date = date.today()
    is_requester_holiday = True
    # Get date after adding leadtime and check for number of holidays between current date and date after adding
    # leadtime for requester
    validated_dates = get_date_after_lead_time(requester_working_days, current_date, valid_date)
    valid_date = validated_dates[0]
    valid_day = validated_dates[1]

    while is_requester_holiday:
        # Check if day is working day for requester
        if valid_day in requester_week_days:
            # If valid date is holiday then add 1 day until its working day for requester
            if valid_date in requester_holiday_list:
                valid_date = valid_date + datetime.timedelta(days=1)
                valid_day = calendar.day_name[valid_date.weekday()]
            else:
                # Update the delivery date to the respective item and model
                django_query_instance.django_filter_only_query(model, {'guid': guid}).update(item_del_date=valid_date)
                return valid_date
        else:
            valid_date = valid_date + datetime.timedelta(days=1)
            valid_day = calendar.day_name[valid_date.weekday()]


# Function to determine delivery date and update to DB after supplier date validation
def get_delivery_date(requester_working_days, requester_week_days, valid_date, requester_holiday_list):
    """
    :param requester_working_days:
    :param requester_week_days:
    :param valid_date:
    :param requester_holiday_list:
    :param model:
    :param guid:
    :return:
    """
    current_date = date.today()
    is_requester_holiday = True
    # Get date after adding leadtime and check for number of holidays between current date and date after adding
    # leadtime for requester
    validated_dates = get_date_after_lead_time(requester_working_days, current_date, valid_date)
    valid_date = validated_dates[0]
    valid_day = validated_dates[1]

    while is_requester_holiday:
        # Check if day is working day for requester
        if valid_day in requester_week_days:
            # If valid date is holiday then add 1 day until its working day for requester
            if valid_date in requester_holiday_list:
                valid_date = valid_date + datetime.timedelta(days=1)
                valid_day = calendar.day_name[valid_date.weekday()]
            else:
                # Update the delivery date to the respective item and model
                return valid_date
        else:
            valid_date = valid_date + datetime.timedelta(days=1)
            valid_day = calendar.day_name[valid_date.weekday()]


def get_company_calendar_from_org_model():
    """

    """
    org_attr_value_instance = OrgAttributeValues()
    object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT, global_variables.GLOBAL_LOGIN_USER_OBJ_ID)
    attr_low_value_list, company_code = OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(object_id_list,
                                                                                                       CONST_CO_CODE)
    default_calendar_id = org_attr_value_instance.get_user_default_attr_value_list_by_attr_id(object_id_list,
                                                                                              CONST_CALENDAR_ID)[1]
    return attr_low_value_list, company_code, default_calendar_id, object_id_list

