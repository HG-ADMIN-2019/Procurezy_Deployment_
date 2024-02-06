"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    context_processors.py
Usage:
    globalize context for all html pages in project


Author:
    Deepika K
"""
from eProc_Notification.models import Notifications
from eProc_Basic.Utilities.functions.get_db_query import *
from eProc_Catalog.Utilities.catalog_generic import CatalogGenericMethods
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import AuthorizationLevel
from eProc_System_Settings.Utilities.system_settings_generic import sys_attributes
from eProc_User_Settings.Utilities import user_settings_generic


def globalise_context(request):
    """
    Globalizing context
    :param request:
    :return:
    """
    msg_display_time_value = '1'
    attachment_size_val = ''
    encrypt_value = ''
    if request.user.is_authenticated:
        update_user_info(request)
        # get updated submenu and slide menu

        client = global_variables.GLOBAL_CLIENT
        login_user_obj_id = get_login_obj_id(request)
        auth_level = AuthorizationLevel(client, login_user_obj_id)
        global_variables.GLOBAL_SLIDE_MENU = auth_level.get_main_menu(CONST_FEATURE)
        global_variables.GLOBAL_SUB_MENU = auth_level.get_sub_menu(CONST_FORM)

        # Centralize cart count
        global_variables.GLOBAL_CART_COUNTER = display_cart_counter(global_variables.GLOBAL_LOGIN_USERNAME)
        global_variables.GLOBAL_NOTIFICATION_COUNTER = Notifications.objects.filter(
            username=global_variables.GLOBAL_LOGIN_USERNAME,
            client=global_variables.GLOBAL_CLIENT,
            read_status=False).count()

        # Get assigned catalogs
        if global_variables.GLOBAL_REQUESTER_OBJECT_ID:
            user_object_id = global_variables.GLOBAL_REQUESTER_OBJECT_ID
        else:
            user_object_id = global_variables.GLOBAL_LOGIN_USER_OBJ_ID
        obj_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT, user_object_id)
        global_variables.CATALOGS_ASSIGNED = CatalogGenericMethods.get_logged_in_user_catalogs(obj_id_list)

        # encrypt_value = encrypt(global_variables.CATALOGS_ASSIGNED)
        sys_attributes_instance = sys_attributes(client)
        msg_display_time_value = sys_attributes_instance.get_msg_display_time()
        if msg_display_time_value is None:
            msg_display_time_value = "5"
    else:
        msg_display_time_value = "1"
    kwargs = {
        'sub_menu': global_variables.GLOBAL_SUB_MENU,
        'shop_purchaser_flag': global_variables.GLOBAL_PURCHASER_FLAG,
        'cart_counter': int(global_variables.GLOBAL_CART_COUNTER),
        'slide_menu': global_variables.GLOBAL_SLIDE_MENU,
        'assigned_catalogs': global_variables.CATALOGS_ASSIGNED,
        # 'encrypt_value':encrypt_value,
        'notification_count': global_variables.GLOBAL_NOTIFICATION_COUNTER,
        'msg_display_time_value': msg_display_time_value,
        'attachment_size_val': attachment_size_val,
    }
    return kwargs


def update_user_info(request):
    """

    :param request:
    :return:
    """
    global_variables.GLOBAL_CLIENT = getClients(request)
    global_variables.GLOBAL_LOGIN_USERNAME = getUsername(request)
    global_variables.GLOBAL_LOGIN_USER_OBJ_ID = get_login_obj_id(request)
    global_variables.GLOBAL_LOGIN_USER_EMAIL_ID = getUserEmailId(request)
    global_variables.GLOBAL_USER_CURRENCY = get_user_currency(request)
    global_variables.GLOBAL_USER_LANGUAGE = get_user_language(request)
    global_variables.GLOBAL_USER_TIMEZONE = get_user_timezone(request)


def clear_user_info():
    """

    :param request:
    :return:
    """
    global_variables.GLOBAL_CLIENT = None
    global_variables.GLOBAL_LOGIN_USERNAME = None
    global_variables.GLOBAL_LOGIN_USER_OBJ_ID = None
    global_variables.GLOBAL_LOGIN_USER_EMAIL_ID = None
    global_variables.GLOBAL_USER_CURRENCY = None
    global_variables.GLOBAL_USER_LANGUAGE = None


def update_user_info_from_db(query_dic):
    """

    """
    if DjangoQueries().django_existence_check(UserData, query_dic):
        user_data = DjangoQueries().django_get_query(UserData, query_dic)
        global_variables.GLOBAL_CLIENT = user_data.client
        global_variables.GLOBAL_LOGIN_USERNAME = user_data.username
        global_variables.GLOBAL_LOGIN_USER_OBJ_ID = user_data.object_id_id
        global_variables.GLOBAL_LOGIN_USER_EMAIL_ID = user_data.email
        global_variables.GLOBAL_USER_CURRENCY = user_data.currency_id_id
        global_variables.GLOBAL_USER_LANGUAGE = user_data.language_id_id


def update_user_obj_id_list_info():
    global_variables.USER_OBJ_ID_LIST = user_settings_generic.get_object_id_list_user(global_variables.GLOBAL_CLIENT,
                                                                                      global_variables.GLOBAL_LOGIN_USER_OBJ_ID)
