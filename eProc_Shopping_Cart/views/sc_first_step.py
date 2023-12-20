"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    sc_first_step.py
Usage:
     cart_details       - Used to display cart items in UI
     display_eform_data - Used to display eform data for free text items in UI

Author:
    Sanjay
"""
import datetime
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from eProc_Attributes.Utilities.attributes_generic import OrgAttributeValues
from eProc_Basic.Utilities.constants.constants import CONST_LIMIT_ORDER_CALLOFF, CONST_CATALOG_CALLOFF, \
    CONST_CALENDAR_ID, CONST_FREETEXT_CALLOFF, CONST_PR_CALLOFF
from eProc_Basic.Utilities.functions.dictionary_key_to_list import dictionary_key_to_list
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import get_currency_list, get_country_data, get_requester_currency, \
    get_login_obj_id
from django.contrib.auth.decorators import login_required
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Calendar_Settings.Utilities.calender_settings_generic import get_list_of_holidays, calculate_delivery_date, \
    calculate_delivery_date_base_on_lead_time
from eProc_Configuration.models import UnitOfMeasures, Currency
from eProc_Form_Builder.models import EformFieldData
from eProc_Price_Calculator.Utilities.price_calculator_generic import calculate_item_total_value, calculate_total_value
from eProc_Shopping_Cart.Shopping_Cart_Forms.call_off_forms.limit_form import UpdateLimitItem
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import get_prod_by_id, get_supplier_first_second_name, \
    get_image_url, get_prod_cat, update_eform_details_scitem, get_currency_converted_price_data, \
    update_image_for_catalog, get_currency_uom_prod_cat_country, get_cart_items_detail, update_delivery_date_to_item_table
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import check_for_eform, get_prod_cat_dropdown, \
    get_free_text_content, get_limit_item_details, update_supplier_uom, update_supplier_uom_for_prod, \
    update_suppliers_uom_details, get_limit_order_item_details
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Shopping_Cart.models import *
from eProc_Basic.Utilities.functions.get_db_query import get_user_currency
from eProc_Exchange_Rates.Utilities.exchange_rates_generic import convert_currency
from eProc_Shopping_Cart.models.add_to_cart import CartItemDetails
from eProc_System_Settings.Utilities.system_settings_generic import sys_attributes
from eProc_User_Settings.Utilities.user_settings_generic import get_object_id_list_user

django_query_instance = DjangoQueries()


@login_required
# Function to display shopping cart first step data
def sc_first_step(request):
    """
    :param request: Gets the items from the database w.r.t the user and display all items in the cart
    :return: sc_first_step.html
    """
    is_limit_item = False
    update_user_info(request)
    org_attr_value_instance = OrgAttributeValues()
    user_currency = get_user_currency(request)
    client = global_variables.GLOBAL_CLIENT
    login_user_obj_id = get_login_obj_id(request)
    total_value = 0
    supplier_id = None
    actual_price_list = []
    discount_value_list = []
    tax_value_list = []
    gross_price_list = []
    catalog_qty = None
    total_item_value = []
    holiday_list = []
    limit_item_details = {}
    prod_desc = ''
    form_id = ''
    requester_user_id = ''
    cart_items = list(
        django_query_instance.django_filter_query(CartItemDetails, {
            'username': global_variables.GLOBAL_LOGIN_USERNAME,
            'client': client
        }, ['item_num'], None)
    )

    if len(cart_items) == 0:
        return HttpResponseRedirect('/shop/products_services/All/create')

    object_id_list = get_object_id_list_user(client, login_user_obj_id)
    default_calendar_id = org_attr_value_instance.get_user_default_attr_value_list_by_attr_id(object_id_list,
                                                                                              CONST_CALENDAR_ID)[1]

    supplier = check_for_eform(request)
    i = 0
    cart_items_guid_list = []
    for items in cart_items:
        cart_items_guid_list.append(items['guid'])
        item_currency = items['currency']
        if not item_currency:
            item_currency = get_requester_currency(items['username'])

        call_off = items['call_off']
        lead_time = items['lead_time']

        if call_off in [CONST_CATALOG_CALLOFF, CONST_FREETEXT_CALLOFF]:
            supplier_id = items['supplier_id']

        requester_user_id = items['username']
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
            delivery_date = calculate_delivery_date(items['guid'],
                                                    lead_time,
                                                    supplier_id,
                                                    default_calendar_id,
                                                    client,
                                                    CartItemDetails)
        elif call_off == CONST_FREETEXT_CALLOFF:
            # if user entered delivery is less than calculated delivery date than
            # update delivery date alculated delivery date
            delivery_date = calculate_delivery_date_base_on_lead_time(
                lead_time,
                supplier_id,
                default_calendar_id)
            if items['item_del_date'] < delivery_date:
                django_query_instance.django_update_query(CartItemDetails,
                                                          {'guid': items['guid'],
                                                           'client': global_variables.GLOBAL_CLIENT},
                                                          {'item_del_date': delivery_date})

        if call_off == CONST_LIMIT_ORDER_CALLOFF:
            is_limit_item = True
            limit_item_details = get_limit_item_details(items['guid'])
            overall_limit = items['overall_limit']
            quantity = 0
            price_unit = 1
            prod_id = items['prod_cat']
            price = 0
            prod_desc = get_prod_by_id(prod_id=prod_id)
            value = calculate_item_total_value(call_off, quantity, catalog_qty, price_unit, price, overall_limit)
            if item_currency != user_currency:
                value = convert_currency(value, str(item_currency), str(user_currency))
            if value:
                total_item_value.append(float(format(value, '2f')))
            else:
                total_item_value.append(0)
            items['item_value'] = value

            total_value = round(sum(total_item_value), 2)

        else:
            overall_limit = None
            quantity = items['quantity']
            price = items['price']
            price_unit = items['price_unit']
            value = calculate_item_total_value(call_off, quantity, catalog_qty, price_unit, price, overall_limit)
            value = convert_currency(value, str(item_currency), str(user_currency))
            if value:
                total_item_value.append(float(format(value, '2f')))
            else:
                total_item_value.append(0)

            total_value = round(sum(total_item_value), 2)
            i += 1

    cart_length = django_query_instance.django_filter_count_query(CartItemDetails, {
        'username': global_variables.GLOBAL_LOGIN_USERNAME,
        'client': client
    })
    # total price detail
    actual_price = round(sum(actual_price_list), 2)
    discount_value = round(sum(discount_value_list), 2)
    tax_value = round(sum(tax_value_list), 2)
    # gross_price = round(sum(gross_price_list), 2)

    product_category = get_prod_cat()
    requester_currency = get_requester_currency(requester_user_id)

    cart_items = list(django_query_instance.django_filter_query(CartItemDetails,
                                                                {'username': global_variables.GLOBAL_LOGIN_USERNAME,
                                                                 'client': client},
                                                                ['item_num'], None))
    for items in cart_items:
        if items['call_off'] == CONST_CATALOG_CALLOFF:
            items['image_url'] = get_image_url(items['int_product_id'])
        else:
            items['image_url'] = ''
        items = update_supplier_uom_for_prod(items)
    cart_items = update_eform_details_scitem(cart_items)

    cart_items = zip(cart_items, total_item_value)

    sys_attributes_instance = sys_attributes(client)

    context = {
        'product_category': product_category,
        'limit_form': UpdateLimitItem(),
        'cart_items': cart_items,
        'cart_length': cart_length,
        'cart_items_guid_list': cart_items_guid_list,
        'requester_currency': requester_currency,
        'inc_nav': True,
        'shopping': True,
        'prod_desc': prod_desc,
        'form_id': form_id,
        'supplier': supplier,
        'currency': django_query_instance.django_filter_only_query(Currency, {'del_ind': False}),
        'unit': django_query_instance.django_filter_only_query(UnitOfMeasures, {'del_ind': False}),
        'total_item_value': total_item_value,
        # total price detail
        'total_value': format(total_value, '.2f'),
        'actual_price': format(actual_price, '.2f'),
        'discount_value': format(discount_value, '.2f'),
        'tax_value': format(tax_value, '.2f'),
        # 'gross_price': gross_price,
        'supplier_details': get_supplier_first_second_name(global_variables.GLOBAL_CLIENT),
        'date_today': datetime.datetime.today(),
        'display_update_delete': True,
        'currency_list': get_currency_list(),
        'country_list': get_country_data(),
        'is_first_step': True,
        'add_favourites_flag': sys_attributes_instance.get_add_favourites(),
    }

    if is_limit_item:
        context['limit_item_details'] = limit_item_details

    return render(request, 'Shopping_Cart/sc_first_step/sc_first_step.html', context)


def shopping_cart_first_step(request):
    """
    :param request: Gets the items from the database w.r.t the user and display all items in the cart
    :return: sc_first_step.html
    """
    update_user_info(request)

    cart_items,cart_length = get_cart_items_detail()

    if cart_length == 0:
        return HttpResponseRedirect('/shop/products_services/All/create')

    cart_items_guid_list = dictionary_key_to_list(cart_items, 'guid')

    cart_items = update_delivery_date_to_item_table(cart_items)

    # get LO details if exists
    # limit_item_details, is_limit_item = get_limit_order_item_details(cart_items)

    # updates suppliers and UOM details into cart items
    cart_items = update_suppliers_uom_details(cart_items)

    # calculate and convert currency
    actual_price, discount_value, tax_value, total_item_value,cart_items = get_currency_converted_price_data(cart_items)

    cart_items = update_image_for_catalog(cart_items)

    cart_items = update_eform_details_scitem(cart_items)

    sys_attributes_instance = sys_attributes(global_variables.GLOBAL_CLIENT)
    currency, uom, currency_list,product_category,country_list = get_currency_uom_prod_cat_country()
    context = {
        'product_category': product_category,
        'limit_form': UpdateLimitItem(),
        'cart_items': cart_items,
        'cart_length': cart_length,
        'cart_items_guid_list': cart_items_guid_list,
        'requester_currency': global_variables.GLOBAL_USER_CURRENCY,
        'currency': currency,
        'unit': uom,
        'inc_nav': True,
        'shopping': True,
        # total price detail
        'total_value': format(total_item_value, '.2f'),
        'actual_price': format(actual_price, '.2f'),
        'discount_value': format(discount_value, '.2f'),
        'tax_value': format(tax_value, '.2f'),
        # 'gross_price': gross_price,
        'date_today': datetime.datetime.today(),
        'display_update_delete': True,
        'currency_list': currency_list,
        'country_list': country_list,
        'is_first_step': True,
        'add_favourites_flag': sys_attributes_instance.get_add_favourites(),
    }

    # if is_limit_item:
    #     context['limit_item_details'] = limit_item_details

    return render(request, 'Shopping_Cart/sc_first_step/sc_first_step.html', context)


# Function display eform data in first step of shopping cart wizard
def display_eform_data(request):
    """
    :param request: Takes request from the user and displays eform data w.r.t item.
    :return: returns eform data details
    """
    guid = request.POST.get('guid')
    eform_context = get_free_text_content(guid)
    return JsonResponse(eform_context)


def update_quantity(request):
    """

    :return:
    """
    cart_resp = {}
    item_guid = request.POST.get('item_guid')
    quantity = request.POST.get('quantity')
    cart_item = django_query_instance.django_get_query(CartItemDetails, {'guid': item_guid})
    cart_item.quantity = int(quantity)
    cart_item.save()
    cart_resp['total'] = calculate_total_value(request)
    cart_resp['quantity'] = quantity
    return JsonResponse(cart_resp)
