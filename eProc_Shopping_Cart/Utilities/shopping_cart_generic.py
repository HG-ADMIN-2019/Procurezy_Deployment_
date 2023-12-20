import datetime

from django.db.models import Q

from eProc_Basic.Utilities.functions.dictionary_key_to_list import dictionary_key_to_list
from eProc_Basic.Utilities.functions.dictionary_list_functions import update_key_value_with_new_key_dictionary_list
from eProc_Basic.Utilities.functions.get_db_query import *
from eProc_Basic.Utilities.functions.messages_config import get_message_desc
from eProc_Basic.Utilities.functions.remove_element_from_list import remove_element_from_list
from eProc_Basic.Utilities.functions.str_concatenate import concatenate_str_with_space
from eProc_Calendar_Settings.Utilities.calender_settings_generic import calculate_delivery_date, \
    calculate_delivery_date_base_on_lead_time
from eProc_Configuration.models import UnspscCategories, UnspscCategoriesCustDesc
from eProc_Configuration.models.basic_data import Currency, UnitOfMeasures
from eProc_Configuration.models.master_data import SupplierMaster
from eProc_Doc_Search_and_Display.Utilities.search_display_specific import get_po_header_app, get_sc_header_app_wf, \
    get_sc_header_app, get_order_status
from eProc_Exchange_Rates.Utilities.exchange_rates_generic import convert_currency
from eProc_Form_Builder.models import EformFieldData
from eProc_Price_Calculator.Utilities.price_calculator_generic import calculate_item_total_value, calculate_item_price
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import get_completion_work_flow, get_manger_detail, \
    get_users_first_name
from eProc_Shopping_Cart.models import ScItem, ScHeader, ScAccounting, ScPotentialApproval, ScApproval
from eProc_Shopping_Cart.models.add_to_cart import CartItemDetails

django_query_instance = DjangoQueries()


# Function to get product category description based on product category Id and display it in drop down
def get_prod_cat():
    """
    The variable prod_det is used to store product Id  of an item while updating an item in 1st step of shopping cart wizard
    This function is mainly used to display product category in drop down in limit_order, form_builder,
    """
    prod_cat_cust = django_query_instance.django_filter_value_list_query(UnspscCategoriesCust, {
        'client': global_variables.GLOBAL_CLIENT
    }, 'prod_cat_id')
    if django_query_instance.django_existence_check(UnspscCategoriesCustDesc,
                                                    {'prod_cat_id__in': prod_cat_cust,
                                                     'language_id': global_variables.GLOBAL_USER_LANGUAGE,
                                                     'client': global_variables.GLOBAL_CLIENT}):
        prod_cat_cust_desc = django_query_instance.django_filter_query(UnspscCategoriesCustDesc, {
            'prod_cat_id__in': prod_cat_cust,
            'language_id': global_variables.GLOBAL_USER_LANGUAGE,
            'client': global_variables.GLOBAL_CLIENT
        }, None, ['prod_cat_id', 'category_desc'])
    else:
        prod_cat_cust_desc = django_query_instance.django_filter_query(UnspscCategoriesCustDesc, {
            'prod_cat_id__in': prod_cat_cust,
            'language_id': CONST_DEFAULT_LANGUAGE,
            'client': global_variables.GLOBAL_CLIENT
        }, None, ['prod_cat_id', 'category_desc'])
    return prod_cat_cust_desc


# Function to get supplier details based on client and display it in drop down
def get_supplier_details(client, supp_id_up):
    """
    The variable supp_id_up is used to store supplier Id  of an item while updating an item in 1st step of shopping cart wizard
    This function is mainly used to display supplier info in drop down in limit_order, form_builder,
    """
    supp_id = []
    supp_name1 = []
    supp_name2 = []
    suppliers = SupplierMaster.objects.filter(client=client, del_ind=False).values('supplier_id', 'name1', 'name2')

    for supplier_details in suppliers:
        supplier_id = supplier_details['supplier_id']
        supplier_name1 = supplier_details['name1']
        supplier_name2 = supplier_details['name2']
        supp_id.append(supplier_id)
        supp_name1.append(supplier_name1)
        supp_name2.append(supplier_name2)

    # Pop an element from a list to avoid duplicate values in drop down in update functionality
    if supp_id_up is not None:
        for supp_id_item in supp_id:
            if supp_id_item == supp_id_up:
                supp_id_index = supp_id.index(supp_id_up)
                del supp_id[supp_id_index]
                del supp_name1[supp_id_index]
                del supp_name2[supp_id_index]

    supplier_info = zip(supp_id, supp_name1, supp_name2)
    return supplier_info


# Function to get supplier first name and last name based on supplier Id
def get_supp_name_by_id(client, supp_id):
    """
    This function is used to supplier details based on supplier id using in select_supplier.py and html
    """
    supplier = django_query_instance.django_get_query(SupplierMaster, {
        'supplier_id': supp_id, 'client': client, 'del_ind': False
    })
    name1 = supplier.name1
    name2 = supplier.name2
    supp_name = name1 + '          ' + name2
    return supp_name


# Function to get product category details by Id
def get_prod_by_id(prod_id):
    """
    This function is used to get product category description from product Id in update functionality
    """
    description = None
    if prod_id is not None:
        if django_query_instance.django_existence_check(UnspscCategories,
                                                        {'prod_cat_id': prod_id,
                                                         'del_ind': False}):
            if django_query_instance.django_existence_check(UnspscCategoriesCust,
                                                            {'prod_cat_id': prod_id,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'del_ind': False}):
                if django_query_instance.django_existence_check(UnspscCategoriesCustDesc,
                                                                {'client': global_variables.GLOBAL_CLIENT,
                                                                 'del_ind': False,
                                                                 'prod_cat_id': prod_id,
                                                                 'language_id': global_variables.GLOBAL_USER_LANGUAGE}):
                    prod_det = django_query_instance.django_get_query(UnspscCategoriesCustDesc,
                                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                                       'del_ind': False,
                                                                       'prod_cat_id': prod_id,
                                                                       'language_id': global_variables.GLOBAL_USER_LANGUAGE})
                    description = prod_det.category_desc
                elif django_query_instance.django_existence_check(UnspscCategoriesCustDesc,
                                                                  {'client': global_variables.GLOBAL_CLIENT,
                                                                   'del_ind': False,
                                                                   'prod_cat_id': prod_id,
                                                                   'language_id': 'EN'}):
                    prod_det = django_query_instance.django_get_query(UnspscCategoriesCustDesc,
                                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                                       'del_ind': False,
                                                                       'prod_cat_id': prod_id,
                                                                       'language_id': 'EN'})
                    description = prod_det.category_desc
                else:
                    prod_det = django_query_instance.django_get_query(UnspscCategories,
                                                                      {'del_ind': False,
                                                                       'prod_cat_id': prod_id})
                    description = prod_det.prod_cat_desc
    return description


def get_supplier_first_second_name(client):
    supplier_list = get_registered_org_suppliers(client)
    supp_id = []
    supp_name1 = []
    supp_name2 = []
    for supplier in supplier_list:
        suppliers = django_query_instance.django_get_query(SupplierMaster, {
            'supplier_id': supplier, 'client': client, 'del_ind': False
        })
        supp_id.append(suppliers.supplier_id)
        supp_name1.append(suppliers.name1)
        supp_name2.append(suppliers.name2)

    supplier_info = zip(supp_id, supp_name1, supp_name2)
    return supplier_info


def get_image_url(int_product_id):
    """

    """
    image_url = ''
    if django_query_instance.django_existence_check(ImagesUpload, {
        'client': global_variables.GLOBAL_CLIENT, 'image_id': int_product_id,
        'image_type': CONST_CATALOG_IMAGE_TYPE, 'image_default': True
    }):
        image_url = django_query_instance.django_filter_value_list_query(ImagesUpload, {
            'client': global_variables.GLOBAL_CLIENT, 'image_id': int_product_id,
            'image_type': CONST_CATALOG_IMAGE_TYPE, 'image_default': True
        }, 'image_url')[0]

    return image_url


def update_eform_details_scitem(cart_items):
    """

    """
    filter_queue = Q()
    for cart_item in cart_items:
        if cart_item['call_off'] in [CONST_CATALOG_CALLOFF, CONST_FREETEXT_CALLOFF]:
            if cart_item['eform_id']:
                filter_queue = Q(cart_guid=cart_item['guid']) | Q(item_guid=cart_item['guid'])
                if django_query_instance.django_queue_existence_check(EformFieldData,
                                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                                       'del_ind': False},
                                                                      filter_queue):
                    cart_item['eform_data'] = django_query_instance.django_queue_query(EformFieldData,
                                                                                       {
                                                                                           'client': global_variables.GLOBAL_CLIENT,
                                                                                           'del_ind': False},
                                                                                       filter_queue,
                                                                                       None,
                                                                                       None)
    return cart_items


def get_price_discount_tax(price, base_price, additional_price, tax, discount_percentage, quantity):
    """

    """
    if additional_price:
        actual_price = float(base_price) + float(additional_price)
    else:
        actual_price = float(base_price)
    discount_value = float(base_price) * float(discount_percentage / 100) * int(quantity)
    if tax:
        if not tax['sgst']:
            tax['sgst'] = 0
        if not tax['cgst']:
            tax['cgst'] = 0
        if not tax['vat']:
            tax['vat'] = 0
        sgst = float(price) * (float(tax['sgst']) / 100) * int(quantity)
        cgst = float(price) * (float(tax['cgst']) / 100) * int(quantity)
        vat = float(price) * (float(tax['vat']) / 100) * int(quantity)
        tax_value = sgst + cgst + vat
        gross_price = float(price) + float(
            (float(price) * (float(tax['sgst']) / 100)) + (float(price) * (float(tax['cgst']) / 100)) + (
                    float(price) * (float(tax['vat']) / 100)))
    else:
        tax_value = 0
        gross_price = price
    return actual_price, discount_value, tax_value, gross_price


def get_total_price_details(item_details, user_currency):
    """

    """
    actual_price_list = []
    discount_value_list = []
    tax_value_list = []
    price_details = {}
    for items in item_details:
        if items['currency'] != user_currency:
            actual_price_list.append(
                convert_currency(float(items['actual_price']) * items['quantity'], str(items['currency']),
                                 str(user_currency)))
            discount_value_list.append(
                convert_currency(items['discount_value'], str(items['currency']), str(user_currency)))
            tax_value_list.append(convert_currency(items['tax_value'], str(items['currency']), str(user_currency)))
            # gross_price_list.append(convert_currency(float(items['gross_price'])*items['quantity'], str(items['currency']), str(user_currency)))
        else:
            actual_price_list.append(float(items['actual_price']) * items['quantity'])
            discount_value_list.append(float(items['discount_value']))
            tax_value_list.append(float(items['tax_value']))
            # gross_price_list.append(float(items['gross_price'])*items['quantity'])
    actual_price = round(sum(actual_price_list), 2)
    discount_value = round(sum(discount_value_list), 2)
    tax_value = round(sum(tax_value_list), 2)
    price_details = {'actual_price': format(actual_price, '.2f'),
                     'discount_value': format(discount_value, '.2f'),
                     'tax_value': format(tax_value, '.2f')}
    return price_details


def get_total_value(sc_item_details, requester_currency):
    """

    """
    value = []
    for sc_item_detail in sc_item_details:
        total_item_value = calculate_item_total_value(sc_item_detail['call_off'], sc_item_detail['quantity'],
                                                      sc_item_detail['quantity'], sc_item_detail['price_unit'],
                                                      sc_item_detail['price'], sc_item_detail['overall_limit'])
        value.append(convert_currency(total_item_value, str(sc_item_detail['currency']), str(requester_currency)))
    if value:
        sc_total_value = round(sum(value), 2)
    else:
        sc_total_value = 0
    return sc_total_value


def get_SC_details_email(sc_header_guid):
    """

    """
    po_header_details = django_query_instance.django_filter_query(ScHeader,
                                                                  {'guid': sc_header_guid,
                                                                   'client': global_variables.GLOBAL_CLIENT},
                                                                  None,
                                                                  None)

    sc_item_details = django_query_instance.django_filter_query(ScItem,
                                                                {'header_guid': sc_header_guid,
                                                                 'client': global_variables.GLOBAL_CLIENT},
                                                                None,
                                                                None)
    for po_header_detail in sc_item_details:
        po_header_detail['supplier_description'] = django_query_instance.django_filter_value_list_query(SupplierMaster,
                                                                                                        {
                                                                                                            'client': global_variables.GLOBAL_CLIENT,
                                                                                                            'supplier_id':
                                                                                                                po_header_detail[
                                                                                                                    'supplier_id']},
                                                                                                        'name1')[0]
    po_item_guid_list = dictionary_key_to_list(po_header_details, 'guid')

    sc_accounting_details = django_query_instance.django_filter_query(ScAccounting,
                                                                      {'header_guid__in': po_item_guid_list,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      None,
                                                                      None)

    po_header_details, po_approver_details, sc_completion, requester_first_name = get_sc_header_app(po_header_details,
                                                                                                    global_variables.GLOBAL_CLIENT)

    context = {'po_header_details': po_header_details,
               'sc_item_details': sc_item_details,
               'sc_accounting_details': sc_accounting_details,
               'po_approver_details': po_approver_details,
               'sc_completion': sc_completion,
               'requester_first_name': requester_first_name,
               'requester_username': po_header_details[0]['requester']

               }
    return context


def get_acc_detail(header_guid):
    """

    """
    item_accounting_data = django_query_instance.django_get_query(ScAccounting, {
        'guid': header_guid
    })

    account_assignment_category = item_accounting_data.acc_cat
    if account_assignment_category == 'CC':
        account_assignment_value = item_accounting_data.cost_center

    elif account_assignment_category == 'AS':
        account_assignment_value = item_accounting_data.asset_number

    elif account_assignment_category == 'OR':
        account_assignment_value = item_accounting_data.internal_order

    else:
        account_assignment_value = item_accounting_data.wbs_ele
    return account_assignment_value


def update_pricing_data(item_details):
    """

    """
    discount_value_list = []
    item_value_list = []
    for item_detail in item_details:
        if item_detail['call_off'] == CONST_CATALOG_CALLOFF:
            price, discount_percentage, base_price, additional_pricing = calculate_item_price(
                item_detail['guid'], item_detail['quantity'])
            actual_price, discount_value, tax_value, gross_price = get_price_discount_tax(price,
                                                                                          base_price,
                                                                                          additional_pricing,
                                                                                          None,
                                                                                          discount_percentage,
                                                                                          item_detail['quantity'])
            if not additional_pricing:
                additional_pricing = 0
            update_dictionary = {'actual_price': actual_price,
                                 'discount_value': discount_value,
                                 'tax_value': tax_value,
                                 'gross_price': gross_price,
                                 'price': price,
                                 'discount_percentage': discount_percentage,
                                 'base_price': base_price,
                                 'additional_price': additional_pricing}
            django_query_instance.django_update_query(ScItem,
                                                      {'guid': item_detail['guid'],
                                                       'client': global_variables.GLOBAL_CLIENT},
                                                      update_dictionary)
            discount_value = discount_value
        else:

            discount_value = 0
        discount_value_list.append(discount_value)
        item_value_list.append(item_detail['value'])

    total_sc_value = round(sum(item_value_list), 2)
    return total_sc_value


def get_currency_converted_price_data(cart_items):
    """

    """
    total_actual_price = 0
    total_discount_value = 0
    total_tax_value = 0
    total_value = 0
    for items in cart_items:
        item_currency = items['currency']
        if not item_currency:
            item_currency = global_variables.GLOBAL_USER_CURRENCY
        if items['call_off'] == CONST_LIMIT_ORDER_CALLOFF:
            overall_limit = items['overall_limit']
            price_unit = 1
        else:
            overall_limit = None
            price_unit = items['price_unit']
        value = calculate_item_total_value(items['call_off'], items['quantity'], None, price_unit, items['price'],
                                           overall_limit)
        if item_currency != global_variables.GLOBAL_USER_CURRENCY:
            actual_price = convert_currency(float(items['actual_price']) * items['quantity'], str(item_currency),
                                            str(global_variables.GLOBAL_USER_CURRENCY))
            discount_value = convert_currency(float(items['discount_value']) * items['quantity'],
                                              str(item_currency),
                                              str(global_variables.GLOBAL_USER_CURRENCY))
            tax_value = convert_currency(float(items['tax_value']) * items['quantity'],
                                         str(item_currency),
                                         str(global_variables.GLOBAL_USER_CURRENCY))
            value = convert_currency(value, str(item_currency), str(global_variables.GLOBAL_USER_CURRENCY))
            # gross_price_list.append(convert_currency(float(items['gross_price'])*items['quantity'], str(item_currency), str(user_currency)))
        else:
            actual_price = float(items['actual_price']) * items['quantity']
            discount_value = items['discount_value']
            tax_value = items['tax_value']
            # gross_price_list.append(float(items['gross_price'])*items['quantity'])
        if value:
            item_total_value = round(value, 2)
            # item_total_value = round(item_total_value, 2)
            items['item_total_value'] = format(item_total_value, '.2f')
        else:
            items['item_total_value'] = round(0, 2)
        total_actual_price = total_actual_price + actual_price
        total_discount_value = total_discount_value + discount_value
        total_tax_value = total_tax_value + tax_value
        total_value = total_value + value
    total_actual_price = round(total_actual_price, 2)
    total_discount_value = round(total_discount_value, 2)
    total_tax_value = round(total_tax_value, 2)
    total_value = round(total_value, 2)
    return total_actual_price, total_discount_value, total_tax_value, total_value, cart_items


def validate_get_currency_converted_price_data(cart_items, currency, sc_check_instance, check_flag):
    """

    """
    total_actual_price = 0
    total_discount_value = 0
    total_tax_value = 0
    total_value = 0
    for loop_count, items in enumerate(cart_items):
        item_number = loop_count + 1
        item_currency = items['currency']
        if not item_currency:
            item_currency = currency
        if items['call_off'] == CONST_LIMIT_ORDER_CALLOFF:
            overall_limit = items['overall_limit']
            price_unit = 1
        else:
            overall_limit = None
            price_unit = items['price_unit']
        value = calculate_item_total_value(items['call_off'], items['quantity'], None, price_unit, items['price'],
                                           overall_limit)
        if item_currency != currency:
            actual_price = convert_currency(float(items['actual_price']) * items['quantity'], str(item_currency),
                                            str(currency))
            discount_value = convert_currency(float(items['discount_value']) * items['quantity'],
                                              str(item_currency),
                                              str(currency))
            tax_value = convert_currency(float(items['tax_value']) * items['quantity'],
                                         str(item_currency),
                                         str(currency))
            value = convert_currency(value, str(item_currency), str(currency))
            if check_flag:
                sc_check_instance.check_for_currency(item_number, value, str(item_currency))
            # gross_price_list.append(convert_currency(float(items['gross_price'])*items['quantity'], str(item_currency), str(user_currency)))
        else:
            actual_price = float(items['actual_price']) * items['quantity']
            discount_value = items['discount_value']
            tax_value = items['tax_value']
            # gross_price_list.append(float(items['gross_price'])*items['quantity'])
        if value:
            item_total_value = round(value, 2)
            item_total_value = format(item_total_value, '.2f')
            items['item_total_value'] = item_total_value
            items['value'] = item_total_value
        else:
            items['item_total_value'] = 0.00
            items['value'] = 0.00
        total_actual_price = total_actual_price + actual_price
        total_discount_value = total_discount_value + discount_value
        total_tax_value = total_tax_value + tax_value
        total_value = total_value + value
    total_actual_price = round(total_actual_price, 2)
    total_discount_value = round(total_discount_value, 2)
    total_tax_value = round(total_tax_value, 2)
    total_value = round(total_value, 2)
    return total_actual_price, total_discount_value, total_tax_value, total_value, cart_items


def update_image_for_catalog(cart_items):
    """

    """
    for items in cart_items:
        if items['call_off'] == CONST_CATALOG_CALLOFF:
            items['image_url'] = get_image_url(items['int_product_id'])
        else:
            items['image_url'] = ''
    return cart_items


def get_currency_uom_prod_cat_country():
    """

    """
    currency = django_query_instance.django_filter_query(Currency, {'del_ind': False}, None,
                                                         ['currency_id', 'description'])
    uom = django_query_instance.django_filter_query(UnitOfMeasures, {'del_ind': False}, None, None)
    currency_list = dictionary_key_to_list(currency, 'currency_id')
    product_category = get_prod_cat()
    country_list = get_country_data()
    return currency, uom, currency_list, product_category, country_list


def get_cart_items_detail():
    """

    """
    cart_items = django_query_instance.django_filter_query(CartItemDetails,
                                                           {'username': global_variables.GLOBAL_LOGIN_USERNAME,
                                                            'client': global_variables.GLOBAL_CLIENT},
                                                           ['item_num'],
                                                           None)
    cart_items_count = len(cart_items)
    return cart_items, cart_items_count


def update_delivery_date_to_item_table(cart_items):
    """

    """
    org_attr_value_instance = OrgAttributeValues()
    object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT, global_variables.GLOBAL_LOGIN_USER_OBJ_ID)
    default_calendar_id = org_attr_value_instance.get_user_default_attr_value_list_by_attr_id(object_id_list,
                                                                                              CONST_CALENDAR_ID)[1]
    for items in cart_items:
        if items['call_off'] not in [CONST_FREETEXT_CALLOFF, CONST_LIMIT_ORDER_CALLOFF]:
            items['item_del_date'] = calculate_delivery_date(items['guid'],
                                                             items['lead_time'],
                                                             items['supplier_id'],
                                                             default_calendar_id,
                                                             global_variables.GLOBAL_CLIENT,
                                                             CartItemDetails)
        elif items['call_off'] == CONST_FREETEXT_CALLOFF:
            # if user entered delivery is less than calculated delivery date than
            # update delivery date alculated delivery date
            delivery_date = calculate_delivery_date_base_on_lead_time(
                items['lead_time'],
                items['supplier_id'],
                default_calendar_id)
            if items['item_del_date'] < delivery_date:
                django_query_instance.django_update_query(CartItemDetails,
                                                          {'guid': items['guid'],
                                                           'client': global_variables.GLOBAL_CLIENT},
                                                          {'item_del_date': delivery_date})
                items['item_del_date'] = delivery_date
    return cart_items


def get_manger_and_purchasing_details(company_code, default_acc_ass_cat, total_value, default_acc, call_off_list,
                                      prod_cat_list):
    """

    """
    error_msg = ''
    completion_work_flow = []
    manager_details = []
    sc_completion_flag = False
    approver_id = []
    company_code = [company_code]
    purchase_control_call_off_list = get_order_status(company_code, prod_cat_list, global_variables.GLOBAL_CLIENT)
    if company_code:
        manager_detail, error_msg = get_manger_detail(global_variables.GLOBAL_CLIENT,
                                                      global_variables.GLOBAL_LOGIN_USERNAME,
                                                      default_acc_ass_cat,
                                                      total_value,
                                                      company_code[0], default_acc,
                                                      global_variables.GLOBAL_USER_CURRENCY)
        if manager_detail:
            manager_details, approver_id = get_users_first_name(manager_detail)

        for purchase_control_call_off in purchase_control_call_off_list:
            if purchase_control_call_off in call_off_list:
                completion_work_flow = get_completion_work_flow(global_variables.GLOBAL_CLIENT, prod_cat_list,
                                                                company_code)
                sc_completion_flag = True
    else:
        error_msg = get_message_desc('MSG109')[1]
    return error_msg, sc_completion_flag, completion_work_flow, manager_details, approver_id


def get_required_field_into_list(cart_items):
    """

    """
    cart_items_guid_list = dictionary_key_to_list(cart_items, 'guid')
    prod_cat_list = dictionary_key_to_list(cart_items, 'prod_cat_id')
    call_off_list = dictionary_key_to_list(cart_items, 'call_off')
    total_item_value = dictionary_key_to_list(cart_items, 'item_total_value')

    return cart_items_guid_list, prod_cat_list, call_off_list, total_item_value


def add_new_key_value(cart_items):
    """

    """
    cart_items = update_key_value_with_new_key_dictionary_list(cart_items, 'prod_cat_id', 'prod_cat')
    return cart_items


def update_request_default_detail():
    """

    """
    global_variables.GLOBAL_REQUESTER_CURRENCY = requester_field_info(global_variables.GLOBAL_LOGIN_USERNAME,
                                                                      'currency_id')
    global_variables.GLOBAL_REQUESTER_LANGUAGE = requester_field_info(global_variables.GLOBAL_LOGIN_USERNAME,
                                                                      'language_id')
