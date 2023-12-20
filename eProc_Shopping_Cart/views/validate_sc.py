import datetime
from eProc_Attributes.Utilities.attributes_generic import OrgAttributeValues
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Calendar_Settings.Utilities.calender_settings_generic import get_list_of_holidays
from eProc_Shopping_Cart.context_processors import update_user_info
from django.http import JsonResponse
from eProc_Shopping_Cart.Utilities.save_order_edit_sc import CheckForScErrors, check_sc_second_step_shopping_cart
from eProc_Basic.Utilities.functions.get_db_query import getClients, get_object_id_from_username
from eProc_Basic.Utilities.constants.constants import CONST_CO_CODE, CONST_CALENDAR_ID, CONST_INV_ADDR
from eProc_User_Settings.Utilities.user_settings_generic import get_attr_value
from eProc_User_Settings.Utilities.user_settings_generic import get_object_id_list_user
from eProc_Shopping_Cart.models import ScHeader

django_query_instance = DjangoQueries()


def check_shopping_cart(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    header_level_acc ={}
    header_level_addr = {}
    client = global_variables.GLOBAL_CLIENT
    holiday_list = []
    sc_check_data = JsonParser().get_json_from_req(request)
    username = sc_check_data['requester']
    if 'sc_header_guid' in sc_check_data:
        sc_header_guid = sc_check_data['sc_header_guid']
        username = django_query_instance.django_get_query(ScHeader, {'guid': sc_header_guid}).requester

    sc_check_instance = CheckForScErrors(client, username)
    org_attr_value_instance = OrgAttributeValues()
    user_object_id = get_object_id_from_username(username)
    object_id_list = get_object_id_list_user(client, user_object_id)
    default_calendar_id = org_attr_value_instance.get_user_default_attr_value_list_by_attr_id(object_id_list,
                                                                                              CONST_CALENDAR_ID)[1]
    default_invoice_adr = org_attr_value_instance.get_user_default_attr_value_list_by_attr_id(object_id_list,
                                                                                              CONST_INV_ADDR)[1]

    if default_calendar_id is not None or default_calendar_id != '':
        holiday_list = get_list_of_holidays(default_calendar_id, client)

    if 'sc_header_guid' in sc_check_data:
        sc_header_guid = sc_check_data['sc_header_guid']
        company_code = django_query_instance.django_get_query(ScHeader, {'guid': sc_header_guid}).co_code
    else:
        company_code = get_attr_value(client, CONST_CO_CODE, object_id_list, False)
        sc_check_instance.document_sc_transaction_check(object_id_list)
        sc_check_instance.po_transaction_check(object_id_list)
    acc_default = sc_check_data['acc_default']
    acc_default_val = sc_check_data['acc_default_val']
    total_val = sc_check_data['total_val']
    check_sc_data = sc_check_data['check_sc_data']
    check_type = sc_check_data['type']

    if check_type == 'approval_workflow':
        sc_check_instance.approval_check(acc_default, acc_default_val, total_val, company_code)
        data = sc_check_instance.get_shopping_cart_errors()
        return JsonResponse(data)

    else:
        check_status = sc_check_data['check_type']
        if check_status == 'sc_second_step':
            header_level_data = sc_check_data['header_level_data']
            header_level_addr = header_level_data['header_level_addr']
            header_level_acc = header_level_data['header_level_acc']
        for data in check_sc_data:
            address_number = data['address_number']
            if 'delivery_date' in data:
                delivery_date = data['delivery_date']
                try:
                    delivery_date = datetime.datetime.strptime(delivery_date, '%Y-%m-%d').date()
                except ValueError:
                    delivery_date = None
                sc_check_instance.delivery_date_check(delivery_date, data['item_num'], holiday_list,
                                                      default_calendar_id)
            if check_status == 'sc_second_step':
                sc_check_instance.item_level_acc_check(data['acc_acc_cat'],
                                                       data['acc_acc_val'],
                                                       header_level_acc['acc_desc_list'],
                                                       data['gl_acc_num'], company_code,
                                                       data['item_num'])
                sc_check_instance.header_level_delivery_address_check(header_level_addr['adr_num'], company_code, None,
                                                                      False)
                sc_check_instance.header_acc_check(header_level_acc['acc_asg_cat'],
                                                   header_level_acc['acc_asg_cat_value'],
                                                   header_level_acc['acc_desc_list'],
                                                   company_code)
            else:
                sc_check_instance.account_assignment_check(data['acc_acc_cat'], data['acc_acc_val'], data['gl_acc_num'],
                                                           data['item_num'])
            sc_check_instance.item_level_delivery_address_check(address_number, data['item_num'])

            sc_check_instance.check_for_prod_cat(data['prod_cat'], company_code, data['item_num'])
            sc_check_instance.check_for_supplier(data['supplier_name'], data['prod_cat'], company_code,
                                                 data['item_num'])

            if 'product_id' in data:
                sc_check_instance.catalog_item_check(data['product_id'], data['item_price'], data['lead_time'],
                                                     data['item_num'], data['item_guid'],data['quantity'])

        sc_check_instance.approval_check(acc_default, acc_default_val, total_val, company_code)

        sc_check_instance.invoice_address_check(default_invoice_adr, company_code)

        sc_check_instance.calender_id_check(default_calendar_id)
        data = sc_check_instance.get_shopping_cart_errors()
        return JsonResponse(data)


def check_shopping_cart1(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    holiday_list = []
    sc_check_data = JsonParser().get_json_from_req(request)
    username = sc_check_data['requester']
    if 'sc_header_guid' in sc_check_data:
        sc_header_guid = sc_check_data['sc_header_guid']
        username = django_query_instance.django_get_query(ScHeader, {'guid': sc_header_guid}).requester

    sc_check_instance = CheckForScErrors(client, username)
    org_attr_value_instance = OrgAttributeValues()
    user_object_id = get_object_id_from_username(username)
    object_id_list = get_object_id_list_user(client, user_object_id)
    default_calendar_id = org_attr_value_instance.get_user_default_attr_value_list_by_attr_id(object_id_list,
                                                                                              CONST_CALENDAR_ID)[1]

    if default_calendar_id is not None or default_calendar_id != '':
        holiday_list = get_list_of_holidays(default_calendar_id, client)

    if 'sc_header_guid' in sc_check_data:
        sc_header_guid = sc_check_data['sc_header_guid']
        company_code = django_query_instance.django_get_query(ScHeader, {'guid': sc_header_guid}).co_code
    else:
        company_code = get_attr_value(client, CONST_CO_CODE, object_id_list, False)
        sc_check_instance.document_sc_transaction_check(object_id_list)
        sc_check_instance.po_transaction_check(object_id_list)
    acc_default = sc_check_data['acc_default']
    acc_default_val = sc_check_data['acc_default_val']
    total_val = sc_check_data['total_val']
    check_sc_data = sc_check_data['check_sc_data']
    check_type = sc_check_data['type']

    if check_type == 'approval_workflow':
        sc_check_instance.approval_check(acc_default, acc_default_val, total_val, company_code)
        data = sc_check_instance.get_shopping_cart_errors()
        return JsonResponse(data)

    else:
        for data in check_sc_data:
            address_number = data['address_number']
            if 'delivery_date' in data:
                delivery_date = data['delivery_date']
                try:
                    delivery_date = datetime.datetime.strptime(delivery_date, '%Y-%m-%d').date()
                except ValueError:
                    delivery_date = None
                sc_check_instance.delivery_date_check(delivery_date, data['item_num'], holiday_list,
                                                      default_calendar_id)

            if address_number != '':
                sc_check_instance.delivery_address_check(address_number, data['item_num'])
            sc_check_instance.account_assignment_check(data['acc_acc_cat'], data['acc_acc_val'], data['gl_acc_num'],
                                                       data['item_num'])
            sc_check_instance.check_for_prod_cat(data['prod_cat'], company_code, data['item_num'])
            sc_check_instance.check_for_supplier(data['supplier_name'], data['prod_cat'], company_code,
                                                 data['item_num'])

            if 'product_id' in data:
                sc_check_instance.catalog_item_check(data['product_id'], data['item_price'], data['lead_time'],
                                                     data['item_num'], data['item_guid'],data['quantity'])

        sc_check_instance.approval_check(acc_default, acc_default_val, total_val, company_code)

        sc_check_instance.calender_id_check(default_calendar_id)
        data = sc_check_instance.get_shopping_cart_errors()
        return JsonResponse(data)
