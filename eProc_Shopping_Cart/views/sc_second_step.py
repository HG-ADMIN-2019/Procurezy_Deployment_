"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    sc_second_step.py
Usage:
      review_page: 1) Functionality to generate default shopping cart name and make it editable returning the values to sc_second_step.html page.
                   2) Functionality to display shopping cart items in sc_second_step.html page.
                   3) Functionality to display receivers name in sc_second_step.html page.
                   4) Functionality to retrieve and edit default shipping address of the user in sc_second_step.html page.
                   5) Functionality to change and edit shipping address from an available list in drop-down of the user in sc_second_step.html page.
Author:
    Sanjay, Deepika, Siddarth Menon
"""
import json

from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from eProc_Account_Assignment.Utilities.account_assignment_generic import AccountAssignmentCategoryDetails, \
    get_default_gl_acc, get_acc_details, get_prod_cat_value_guid
from eProc_Basic.Utilities.functions.get_system_setting_attributes import *
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.messages.messages import MSG109, MSG134
from eProc_Doc_Search_and_Display.Utilities.search_display_specific import get_order_status
from eProc_Emails.Utilities.email_notif_generic import appr_notify, send_po_attachment_email
from eProc_Price_Calculator.Utilities.price_calculator_generic import calculate_item_total_value
from eProc_Purchase_Order.Utilities.purchase_order_generic import *
from eProc_Purchase_Order.Utilities.purchase_order_generic import CreatePurchaseOrder
# from eProc_Purchase_Order.Utilities.purchase_order_generic import CreatePurchaseOrder
# from eProc_Purchase_Order.Utilities.purchase_order_generic import CreatePurchaseOrder
from eProc_Registration.models.registration_model import UserData
from eProc_Ship_To_Bill_To_Address.Utilites.ship_to_bill_to_generic import ShipToBillToAddress, \
    get_shipping_address_detail
from eProc_Shopping_Cart.Shopping_Cart_Forms.call_off_forms.limit_form import UpdateLimitItem
from eProc_Shopping_Cart.Utilities.save_order_edit_sc import SaveShoppingCart, CheckForScErrors, \
    check_sc_second_step_shopping_cart
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import *
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import get_prod_cat_dropdown, get_manger_detail, \
    get_completion_work_flow, get_users_first_name, unpack_accounting_data, update_supplier_uom, \
    update_supplier_uom_for_prod, get_cart_default_name_and_user_first_name, update_suppliers_uom_details
from eProc_Configuration.models import UnitOfMeasures, Currency
from eProc_Basic.Utilities.functions.get_db_query import getUsername, getClients, get_login_obj_id
from eProc_Basic.Utilities.functions.str_concatenate import concatenate_str_with_space
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import check_for_eform
from eProc_Notes_Attachments.Notes_Attachments.Attachment_Form import CreateAttachForm, CreateAttachlistForm
from eProc_Notes_Attachments.Notes_Attachments.Notes_Form import NotesForm
from eProc_Shopping_Cart.context_processors import update_user_info, update_user_obj_id_list_info
from eProc_Shopping_Cart.models import CartItemDetails
from eProc_System_Settings.Utilities.system_settings_generic import sys_attributes, get_system_settings_data
from eProc_User_Settings.Utilities.user_settings_generic import get_object_id_list_user, get_attr_value
from eProc_User_Settings.Utilities.user_settings_specific import UserSettings
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import empty_shopping_cart_data
from eProc_Calendar_Settings.Utilities.calender_settings_generic import *
from eProc_Basic.Utilities.functions.get_db_query import get_user_currency
from eProc_Exchange_Rates.Utilities.exchange_rates_generic import convert_currency
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Workflow.Utilities.work_flow_specific import update_appr_status

django_query_instance = DjangoQueries()


@login_required
def review_page(request):
    """
    :param request: Get shopping cart and user details in second step of shopping cart
    :return: sc_second_step.html
    """
    update_user_info(request)
    org_attr_value_instance = OrgAttributeValues()
    user_currency = get_user_currency(request)
    username = getUsername(request)
    requester_user_name = username
    update_requester_info(requester_user_name)
    requester_currency = global_variables.GLOBAL_REQUESTER_CURRENCY
    client = getClients(request)
    username = getUsername(request)
    prod_desc = ''
    total_item_value = []
    actual_price_list = []
    discount_value_list = []
    tax_value_list = []
    catalog_qty = None
    manager_details = []
    holiday_list = []
    approver_id = []
    prod_cat_list = []
    completion_work_flow = []
    requester_user_id = ''
    call_off_list = []
    cart_items_guid_list = []
    sc_completion_flag = False
    login_username = getUsername(request)
    login_user_obj_id = get_login_obj_id(request)
    update_user_obj_id_list_info()
    object_id_list = get_object_id_list_user(client, login_user_obj_id)
    edit_flag = False
    attr_low_value_list, company_code = OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(object_id_list,
                                                                                                       CONST_CO_CODE)
    default_calendar_id = org_attr_value_instance.get_user_default_attr_value_list_by_attr_id(object_id_list,
                                                                                              CONST_CALENDAR_ID)[1]
    if default_calendar_id is not None or default_calendar_id != '':
        holiday_list = get_list_of_holidays(default_calendar_id, client)

    request.session['company_code'] = company_code
    item_detail_list = []
    requester_first_name = requester_field_info(username, 'first_name')
    sc_check_instance = CheckForScErrors(client, username)
    sc_check_instance.document_sc_transaction_check(object_id_list)
    sc_check_instance.po_transaction_check(object_id_list)

    sc_check_instance.calender_id_check(default_calendar_id)

    # Get default shopping cart name
    date_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    cart_name = concatenate_str_with_space(requester_first_name, date_time)

    # Display shopping cart items in 2nd step of wizard

    cart_items = list(
        django_query_instance.django_filter_query(CartItemDetails, {
            'username': login_username, 'client': client
        }, ['item_num'], None)
    )

    cart_items_count = django_query_instance.django_filter_count_query(CartItemDetails, {
        'username': login_username, 'client': client
    })

    if cart_items_count == 0:
        return redirect('eProc_Shop_Home:shopping_cart_home')
    i = 0
    for items in cart_items:
        cart_items_guid_list.append(items['guid'])
        item_currency = items['currency']
        if not item_currency:
            item_currency = requester_currency
        item_details = {}
        item_number = i + 1
        requester_user_id = items['username']
        product_category = items['prod_cat_id']
        lead_time = items['lead_time']
        supplier_id = items['supplier_id']
        call_off = items['call_off']

        sc_check_instance.check_for_prod_cat(product_category, company_code, item_number)
        if call_off != CONST_PR_CALLOFF:
            sc_check_instance.check_for_supplier(supplier_id, product_category, company_code, item_number)

        if call_off == CONST_CATALOG_CALLOFF:
            product_id = items['int_product_id']
            sc_check_instance.catalog_item_check(product_id, items['price'], lead_time, item_number, items['guid'],
                                                 items['quantity'])
        if item_currency != user_currency:
            actual_price_list.append(
                convert_currency(float(items['actual_price']) * items['quantity'], str(item_currency),
                                 str(user_currency)))
            discount_value_list.append(
                convert_currency(items['discount_value'], str(item_currency), str(user_currency)))
            tax_value_list.append(convert_currency(items['tax_value'], str(item_currency), str(user_currency)))
            # gross_price_list.append(convert_currency(float(items['gross_price'])*items['quantity'], str(item_currency), str(user_currency)))
        else:
            actual_price_list.append(float(items['actual_price']) * items['quantity'])
            discount_value_list.append(items['discount_value'])
            tax_value_list.append(items['tax_value'])
            # gross_price_list.append(float(items['gross_price'])*items['quantity'])
        if call_off not in [CONST_FREETEXT_CALLOFF, CONST_LIMIT_ORDER_CALLOFF]:
            if len(holiday_list) == 0:
                item_delivery_date = None
            else:
                item_delivery_date = calculate_delivery_date(items['guid'],
                                                             lead_time,
                                                             supplier_id,
                                                             default_calendar_id,
                                                             client,
                                                             CartItemDetails)
        elif call_off == CONST_FREETEXT_CALLOFF:
            item_delivery_date = calculate_delivery_date_base_on_lead_time(
                lead_time,
                supplier_id,
                default_calendar_id)
            if items['item_del_date'] < item_delivery_date:
                django_query_instance.django_update_query(CartItemDetails,
                                                          {'guid': items['guid'],
                                                           'client': global_variables.GLOBAL_CLIENT},
                                                          {'item_del_date': item_delivery_date})
            else:
                item_delivery_date = items['item_del_date']

        else:
            if items['start_date'] is None:
                item_delivery_date = items['item_del_date']

            else:
                item_delivery_date = items['start_date']

        sc_check_instance.delivery_date_check(item_delivery_date, item_number, holiday_list, default_calendar_id)

        prod_cat_list.append(product_category)
        call_off_list.append(call_off)
        call_off = call_off
        if call_off == CONST_LIMIT_ORDER_CALLOFF:
            overall_limit = items['overall_limit']
            quantity = None
            price_unit = None
            prod_id = product_category
            price = None
            prod_desc = get_prod_by_id(prod_id=prod_id)
            value = calculate_item_total_value(call_off, quantity, catalog_qty, price_unit, price, overall_limit)
            value = convert_currency(value, str(item_currency), str(user_currency))
            sc_check_instance.check_for_currency(item_number, value, str(item_currency))
            if value:
                total_item_value.append(float(format(value, '2f')))
            else:
                value = 0
                total_item_value.append(0)

            total_value = round(sum(total_item_value), 2)
            request.session['total_value'] = total_value

        else:

            prod_cat_list.append(product_category)
            call_off_list.append(call_off)
            call_off = call_off
            if call_off == CONST_LIMIT_ORDER_CALLOFF:
                overall_limit = items['overall_limit']
                quantity = None
                price_unit = None
                prod_id = product_category
                price = None
                prod_desc = get_prod_by_id(prod_id=prod_id)
                value = calculate_item_total_value(call_off, quantity, catalog_qty, price_unit, price, overall_limit)
                value = convert_currency(value, str(item_currency), str(user_currency))
                sc_check_instance.check_for_currency(item_number, value, str(item_currency))
                if value:
                    total_item_value.append(float(format(value, '2f')))
                else:
                    value = 0
                    total_item_value.append(value)

                total_value = round(sum(total_item_value), 2)
                request.session['total_value'] = total_value

            else:
                overall_limit = None
                quantity = items['quantity']
                price = items['price']
                price_unit = items['price_unit']
                value = calculate_item_total_value(call_off, quantity, catalog_qty, price_unit, price, overall_limit)
                value = convert_currency(value, str(item_currency), str(user_currency))
                sc_check_instance.check_for_currency(item_number, value, str(item_currency))
                if value:
                    total_item_value.append(float(format(value, '2f')))
                else:
                    value = 0
                    total_item_value.append(value)

                total_value = round(sum(total_item_value), 2)
                i += 1
                request.session['total_value'] = total_value

        item_details['prod_cat'] = product_category
        item_details['value'] = value
        item_details['guid'] = items['guid']
        item_detail_list.append(item_details)
    global_variables.GLOBAL_REQUESTER_CURRENCY = requester_field_info(requester_user_id, 'currency_id')
    global_variables.GLOBAL_REQUESTER_LANGUAGE = requester_field_info(requester_user_id, 'language_id')
    highest_item_value = max(total_item_value)
    highest_item_number = total_item_value.index(highest_item_value)
    # Display receivers name
    receiver_name = concatenate_str_with_space(request.user.first_name, request.user.last_name)

    user_object_id = global_variables.USER_OBJ_ID_LIST
    user_setting = UserSettings()
    ship_to_bill_to_address_instance = ShipToBillToAddress(global_variables.GLOBAL_LOGIN_USER_OBJ_ID)
    address_number_list, default_address_number = ship_to_bill_to_address_instance.get_default_address_number_and_list()

    delivery_addr_list, addr_default, addr_val_desc = ship_to_bill_to_address_instance. \
        get_default_address_and_available_address_with_description(address_number_list, default_address_number)

    delivery_addr_desc = ship_to_bill_to_address_instance.get_all_addresses_with_descriptions(address_number_list)

    acc_obj = AccountAssignmentCategoryDetails(object_id_list, company_code, item_detail_list)
    accounting_data = acc_obj.get_acc_list_and_default()

    # Get notes and attachment form
    upload_attach_form = CreateAttachForm()
    attach_list_form = CreateAttachlistForm()
    add_note_form = NotesForm()

    product_category = get_prod_cat_dropdown(request)
    supplier = check_for_eform(request)

    # to get manager detail
    default_cmp_code = user_setting.get_attr_default(user_object_id, CONST_CO_CODE)
    purchase_control_call_off_list = get_order_status(default_cmp_code, prod_cat_list, global_variables.GLOBAL_CLIENT)
    if default_cmp_code:
        manager_detail, msg_info = get_manger_detail(client, username, accounting_data['default_acc_ass_cat'],
                                                     total_value,
                                                     default_cmp_code, accounting_data['default_acc'],
                                                     global_variables.GLOBAL_USER_CURRENCY)
        if manager_detail:
            manager_details, approver_id = get_users_first_name(manager_detail)
        default_cmp_code = [default_cmp_code]
        for purchase_control_call_off in purchase_control_call_off_list:
            if purchase_control_call_off in call_off_list:
                completion_work_flow = get_completion_work_flow(client, prod_cat_list, default_cmp_code)
                sc_completion_flag = True
    else:
        error_msg = get_message_desc(MSG109)[1]
        # msgid = 'MSG109'
        # error_msg = get_msg_desc(msgid)
        # msg = error_msg['message_desc'][0]
        # error_msg = msg
        msg_info = error_msg
    formatted_value = format(total_value, '2f')

    default_account_assignment_category, default_account_assignment_value = unpack_accounting_data(accounting_data,
                                                                                                   sc_check_instance)

    sc_check_instance.delivery_address_check(default_address_number, '0')
    sc_check_instance.approval_check(default_account_assignment_category, default_account_assignment_value, total_value,
                                     company_code)

    cart_items = list(
        django_query_instance.django_filter_query(CartItemDetails, {
            'username': login_username, 'client': client
        }, ['item_num'], None)
    )
    for items in cart_items:
        if items['call_off'] == CONST_CATALOG_CALLOFF:
            items['image_url'] = get_image_url(items['int_product_id'])
        else:
            items['image_url'] = ''
        items = update_supplier_uom_for_prod(items)
    cart_items = update_eform_details_scitem(cart_items)
    cart_items = zip(cart_items, total_item_value)
    sys_attributes_instance = sys_attributes(client)
    shopping_cart_errors = sc_check_instance.get_shopping_cart_errors()

    # total price detail
    actual_price = round(sum(actual_price_list), 2)
    discount_value = round(sum(discount_value_list), 2)
    tax_value = round(sum(tax_value_list), 2)

    context = {
        'shopping_cart_errors': shopping_cart_errors,
        'highest_item_number': highest_item_number + 1,
        'sc_completion_flag': sc_completion_flag,
        'requester_user_name': requester_user_id,
        'item_detail_list': item_detail_list,
        'cart_items_guid_list': cart_items_guid_list,
        'supplier': supplier,
        'requester_first_name': requester_first_name,
        'manager_details': manager_details,
        'approver_id': approver_id,
        'msg_info': msg_info,
        'default_company_code': company_code,
        'header_level_gl_acc': accounting_data['header_level_gl_acc'],
        'completion_work_flow': completion_work_flow,
        'limit_form': UpdateLimitItem(),
        'cart_name': cart_name,
        'inc_nav': True,
        'cart_items': cart_items,
        'actual_price': format(actual_price, '.2f'),
        'discount_value': format(discount_value, '.2f'),
        'tax_value': format(tax_value, '.2f'),
        'requester_currency': global_variables.GLOBAL_REQUESTER_CURRENCY,
        'gl_acc_item_level_default': accounting_data['gl_acc_item_level_default'],
        'receiver_name': receiver_name,
        'rest_shipping_addr': delivery_addr_list,
        'upload_attach_form': upload_attach_form,
        'attach_list_form': attach_list_form,
        'add_note_form': add_note_form,
        'select_flag': True,
        'acc_default': accounting_data['acc_default'],
        'acc_value': accounting_data['acc_value'],
        'currency': django_query_instance.django_filter_only_query(Currency, {'del_ind': False}),
        'unit': django_query_instance.django_filter_only_query(UnitOfMeasures, {'del_ind': False}),
        'product_category': product_category,
        'supplier_details': get_supplier_first_second_name(client),
        'date_today': datetime.datetime.today(),
        'total_item_value': total_item_value,
        'total_value': round(float(formatted_value), 2),
        'prod_desc': prod_desc,
        'acc_list': accounting_data['acc_list'],
        'acc_value_list': accounting_data['acc_value_list'],
        'addr_val_desc': addr_val_desc,
        'display_update_delete': False,
        'delivery_addr_desc': delivery_addr_desc,
        'acc_cat_default_value': accounting_data['default_acc_ass_cat'],
        'country_list': get_country_data(),
        'is_second_step': True,
        'is_document_detail': False,
        'acct_assignment_category': sys_attributes_instance.get_acct_assignment_category(),
        'purchase_group': sys_attributes_instance.get_purchase_group(),
        'edit_address_flag': sys_attributes_instance.get_edit_address(),
        'shipping_address_flag': sys_attributes_instance.get_shipping_address(),
        'attachment_size': sys_attributes_instance.get_attachment_size(),
        'attachment_extension': sys_attributes_instance.get_attachment_extension(),
        'currency_list': get_currency_list(),

    }

    return render(request, 'Shopping_Cart/sc_second_step/sc_second_step.html', context)


def sc_second_step(request):
    """
    :param request: Get shopping cart and user details in second step of shopping cart
    :return: sc_second_step.html
    """
    prod_desc = ''
    update_user_info(request)

    sc_check_instance = CheckForScErrors(global_variables.GLOBAL_CLIENT, global_variables.GLOBAL_LOGIN_USERNAME)

    update_requester_info(global_variables.GLOBAL_LOGIN_USERNAME)

    # get default calender id and company code from org model
    attr_low_value_list, company_code, default_calendar_id, object_id_list = get_company_calendar_from_org_model()

    org_attr_value_instance = OrgAttributeValues()
    default_invoice_adr = org_attr_value_instance.get_user_default_attr_value_list_by_attr_id(object_id_list,
                                                                                              CONST_INV_ADDR)[1]
    # get cart default name, first name
    requester_first_name, cart_name, receiver_name = get_cart_default_name_and_user_first_name(request.user.first_name,
                                                                                               request.user.last_name)
    request.session['company_code'] = company_code
    # Display shopping cart items in 2nd step of wizard

    cart_items, cart_items_count = get_cart_items_detail()

    if cart_items_count == 0:
        return redirect('eProc_Shop_Home:shopping_cart_home')

    actual_price, discount_value, \
    tax_value, total_value, cart_items = validate_get_currency_converted_price_data(cart_items,
                                                                                    global_variables.GLOBAL_USER_CURRENCY,
                                                                                    sc_check_instance,
                                                                                    True)
    cart_items_guid_list, prod_cat_list, call_off_list, total_item_value = get_required_field_into_list(cart_items)
    request.session['total_value'] = total_item_value

    update_request_default_detail()

    highest_item_value = max(total_item_value)
    highest_item_number = total_item_value.index(highest_item_value)

    # get shipping data
    address_number_list, \
    default_address_number, \
    delivery_addr_list, \
    addr_default, \
    addr_val_desc, \
    delivery_addr_desc = get_shipping_address_detail(object_id_list)

    # cart_items = add_new_key_value(cart_items)
    item_detail_list = get_prod_cat_value_guid(cart_items)
    # get Accounting data
    accounting_data = get_acc_details(object_id_list, company_code, item_detail_list)

    supplier = check_for_eform(request)

    # updates suppliers and UOM details into cart items
    cart_items = update_suppliers_uom_details(cart_items)

    # updates delivery data
    cart_items = update_delivery_date_to_item_table(cart_items)

    # to get manager detail
    msg_info, sc_completion_flag, \
    completion_work_flow, manager_details, \
    approver_id = get_manger_and_purchasing_details(
        company_code,
        accounting_data['default_acc_ass_cat'],
        total_value,
        accounting_data['default_acc'],
        call_off_list,
        prod_cat_list)

    cart_items, shopping_cart_errors = check_sc_second_step_shopping_cart(sc_check_instance, object_id_list,
                                                                          default_calendar_id, default_invoice_adr,
                                                                          company_code, default_address_number,
                                                                          address_number_list,
                                                                          accounting_data, manager_details,
                                                                          approver_id, total_value, msg_info,
                                                                          cart_items)

    # update images
    cart_items = update_image_for_catalog(cart_items)

    cart_items = update_eform_details_scitem(cart_items)

    currency, uom, currency_list, product_category, country_list = get_currency_uom_prod_cat_country()

    sys_attributes_instance = sys_attributes(global_variables.GLOBAL_CLIENT)
    request.session['total_value'] = total_item_value
    request.session['company_code'] = company_code
    system_settings_data = get_system_settings_data()
    print("completion_work_flow ", completion_work_flow)

    context = {
        'shopping_cart_errors': shopping_cart_errors,
        'cart_items_count': cart_items_count,
        'highest_item_number': highest_item_number + 1,
        'sc_completion_flag': sc_completion_flag,
        'requester_user_name': global_variables.GLOBAL_LOGIN_USERNAME,
        'item_detail_list': item_detail_list,
        'cart_items_guid_list': cart_items_guid_list,
        'supplier': supplier,
        'requester_first_name': requester_first_name,
        'manager_details': manager_details,
        'approver_id': approver_id,
        'msg_info': msg_info,
        'default_company_code': company_code,
        'header_level_gl_acc': accounting_data['header_level_gl_acc'],
        'completion_work_flow': completion_work_flow,
        'limit_form': UpdateLimitItem(),
        'cart_name': cart_name,
        'inc_nav': True,
        'cart_items': cart_items,
        'total_value': format(total_value, '.2f'),
        'actual_price': format(actual_price, '.2f'),
        'discount_value': format(discount_value, '.2f'),
        'tax_value': format(tax_value, '.2f'),
        'requester_currency': global_variables.GLOBAL_REQUESTER_CURRENCY,
        'gl_acc_item_level_default': accounting_data['gl_acc_item_level_default'],
        'receiver_name': receiver_name,
        'select_flag': True,
        'acc_default': accounting_data['acc_default'],
        'acc_value': accounting_data['acc_value'],
        'account_assign_cat_list': accounting_data['account_assign_cat_list'],
        'acc_desc_append_list': accounting_data['acc_desc_append_list'],
        'currency': currency,
        'unit': uom,
        'product_category': product_category,
        'supplier_details': get_supplier_first_second_name(global_variables.GLOBAL_CLIENT),
        'date_today': datetime.datetime.today(),
        'total_item_value': total_item_value,
        'prod_desc': prod_desc,
        'acc_list': accounting_data['acc_list'],
        'acc_value_list': accounting_data['acc_value_list'],
        'display_update_delete': False,
        'rest_shipping_addr': delivery_addr_list,
        'addr_val_desc': addr_val_desc,
        'delivery_addr_desc': delivery_addr_desc,
        'default_address_number': default_address_number,
        'acc_cat_default_value': accounting_data['default_acc_ass_cat'],
        'country_list': get_country_data(),
        'is_second_step': True,
        'is_document_detail': False,
        'acct_assignment_category': system_settings_data['acct_assignment_category'],
        'purchase_group': system_settings_data['purchase_group'],
        'edit_address_flag': system_settings_data['edit_address_flag'],
        'shipping_address_flag': system_settings_data['shipping_address_flag'],
        'attachment_size': system_settings_data['attachment_size'],
        'attachment_extension': system_settings_data['attachment_extension'],
        'currency_list': currency_list,

    }

    return render(request, 'Shopping_Cart/sc_second_step/shopping_cart_second_step.html', context)


# Function to call save shopping cart through ajax call (login required decorator is not required)
@transaction.atomic
def save_shopping_cart(request):
    """
    :param request:
    :return:
    """
    manager_details = []
    update_user_info(request)
    if request.method == 'POST':
        attachments_data = request.FILES
        sc_ui_data = request.POST
        manager_detail = request.POST.get('manger_detail')
        manager_detail = json.dumps(manager_detail)
        manager_detail = eval(json.loads(manager_detail))
        sc_completion_flag = request.POST.get('sc_completion_flag')
        if manager_detail:
            manager_details = manager_detail
        header_guid = guid_generator()
        save_sc_data = SaveShoppingCart(request, sc_ui_data, attachments_data, header_guid, 'Save')

        sc_details = save_sc_data.save_header_details(CONST_SC_HEADER_SAVED)
        if not sc_details[0]:
            return JsonResponse({'error_ms': sc_details[1]}, status=201)

        save_sc_data.save_approval_data(manager_details, CONST_SC_HEADER_SAVED, sc_completion_flag)

        if sc_details[0]:
            save_sc_data.save_item_details(request)
            save_sc_data.eform_item_guid.clear()
            save_sc_data.cart_guid.clear()

        # empty_shopping_cart_data(username, client)
        return JsonResponse({'sc_details': sc_details})

    else:
        msgid = 'MSG131'
        error_msg = get_msg_desc(msgid)[1]

        return JsonResponse({'error_ms': error_msg}, status=201)


# Display the selected shipping from drop-down in the shipping details section
def change_ship_adr(request):
    change_ship_add = request.POST.get('ship_adr')
    del_ad = change_ship_add.split('-')
    addr = del_ad[1]
    new_ship_add = addr.split('/')

    return JsonResponse({'new_ship_add': new_ship_add, 'address_num': del_ad[0]})


def order_shopping_cart(request):
    username = getUsername(request)
    client = getClients(request)
    if request.method == 'POST':
        attachments_data = request.FILES
        sc_ui_data = request.POST
        manager_detail = request.POST.get('manger_detail')
        sc_completion_flag = request.POST.get('sc_completion_flag')
        manager_detail = json.dumps(manager_detail)
        manager_detail = eval(json.loads(manager_detail))
        header_guid = guid_generator()
        save_sc_data = SaveShoppingCart(request, sc_ui_data, attachments_data, header_guid, 'Order')
        if sc_completion_flag == 'True':
            status = CONST_SC_HEADER_INCOMPLETE
        else:
            if manager_detail[0]['app_id_value'] == CONST_AUTO:
                status = CONST_SC_HEADER_APPROVED
            else:
                status = CONST_SC_HEADER_AWAITING_APPROVAL
                # temp = {'status': status+'-'+header_guid+'-'+'01'}
                # header_status, sc_header_instance = update_appr_status(temp)

        sc_details = save_sc_data.save_header_details(status)
        update_user_info(request)
        save_sc_data.save_approval_data(manager_detail, CONST_SC_HEADER_ORDERED, sc_completion_flag)

        if sc_details[0]:
            save_sc_data.save_item_details(request)
            # print(save_sc_data.cart_item_guid)
            django_query_instance.django_filter_delete_query(CartItemDetails,
                                                             {'guid__in': save_sc_data.cart_item_guid,
                                                              'client': global_variables.GLOBAL_CLIENT})
            save_sc_data.eform_item_guid.clear()
            save_sc_data.cart_guid.clear()

            if status == CONST_SC_HEADER_APPROVED:
                sc_header_instance = django_query_instance.django_get_query(ScHeader,
                                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                                             'doc_number': sc_details[0]})
                ScApproval.objects.update_or_create(header_guid=sc_header_instance.guid,
                                                    defaults={'proc_lvl_sts': CONST_COMPLETED,
                                                              'app_sts': CONST_SC_APPR_APPROVED})
                create_purchase_order = CreatePurchaseOrder(sc_header_instance)
                status, error_message, output, po_doc_list = create_purchase_order.create_po()
                # Send purchase order email to supplier

                for po_document_number in po_doc_list:
                    email_supp_monitoring_guid = ''
                    send_po_attachment_email(output, po_document_number, email_supp_monitoring_guid)
            # function to send SC Approval email
            #  check for sc_completion_flag == true  , if not send mail
            if sc_completion_flag == 'False':
                auto_app_flag = 0
                for app_type in manager_detail:
                    if app_type['app_id_value'] == 'Auto':
                        auto_app_flag = 1
                if auto_app_flag == 0:
                    context = get_SC_details_email(header_guid)
                    context['manager_details'] = manager_detail
                    context['step_num_inc'] = 1
                    context['email_document_monitoring_guid'] = ''
                    appr_notify(context, 'SC_APPROVAL', client)
        else:
            return JsonResponse({'error_ms': sc_details[1]}, status=400)

        # empty_shopping_cart_data(username, client)
        return JsonResponse({'sc_details': sc_details})


def auto_complete_goods_receiver(request):
    client = getClients(request)
    if 'term' in request.GET:
        qs = UserData.objects.filter(Q(client=client, first_name__icontains=request.GET.get('term')) |
                                     Q(client=client, last_name__icontains=request.GET.get('term')) |
                                     Q(client=client, email__icontains=request.GET.get('term')))

        receiver_names = list()
        for names in qs:
            receiver_names.append(names.first_name + ' ' + names.last_name + ' - ' + names.email)
        return JsonResponse(receiver_names, safe=False)


def update_user_name(request):
    user_detail = {}
    email_id = request.POST.get('email_id')
    user_detail['user_name'] = get_user_id_by_email_id(email_id)

    return JsonResponse(user_detail, safe=False)


def ajax_trigger_wf(request):
    """
    """
    wf_data_dictionary = {}
    gl_acc_list = []
    update_user_info(request)
    trigger_wf_input_data = JsonParser().get_json_from_req(request)
    requester_user_name = trigger_wf_input_data['requester_user_name']
    acc_default = trigger_wf_input_data['acc_default']
    total_val = trigger_wf_input_data['total_value']
    company_code = trigger_wf_input_data['default_company_code']
    acc_default_val = trigger_wf_input_data['acc_default_val']
    item_details = trigger_wf_input_data['item_details']
    update_requester_info(requester_user_name)
    if total_val:
        total_val = float(total_val)
    else:
        total_val = 0
    manager_detail, error_message = get_manger_detail(global_variables.GLOBAL_CLIENT, requester_user_name, acc_default,
                                                      total_val,
                                                      company_code, acc_default_val,
                                                      global_variables.GLOBAL_REQUESTER_CURRENCY)
    manager_details, approver_id = get_users_first_name(manager_detail)
    if item_details:
        for item_detail in item_details:
            item_value = float(item_detail['item_value'])
            gl_acc_list.append(get_default_gl_acc(company_code, acc_default,
                                                  item_detail['prod_cat'], item_value,
                                                  global_variables.GLOBAL_REQUESTER_CURRENCY,
                                                  global_variables.GLOBAL_REQUESTER_LANGUAGE))
    wf_data_dictionary['manager_detail'] = manager_details
    wf_data_dictionary['error_message'] = error_message
    wf_data_dictionary['gl_acc_list'] = gl_acc_list
    wf_data_dictionary['approver_id'] = approver_id
    return JsonResponse(wf_data_dictionary)
