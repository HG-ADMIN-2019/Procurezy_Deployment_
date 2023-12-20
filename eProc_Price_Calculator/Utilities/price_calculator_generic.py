from decimal import Decimal

from django.db.models import Q

from eProc_Basic.Utilities.constants.constants import CONST_CATALOG_CALLOFF, CONST_LIMIT_ORDER_CALLOFF, \
    CONST_VARIANT_BASE_PRICING, \
    CONST_VARIANT_ADDITIONAL_PRICING, CONST_QUANTITY_BASED_DISCOUNT
from eProc_Basic.Utilities.functions.dictionary_list_functions import rename_dictionary_list_key
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.sort_dictionary import sort_dic_list_by_value
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import EformFieldConfig, ProductEformPricing, ProductsDetail, VariantConfig, \
    DiscountData
from eProc_Exchange_Rates.Utilities.exchange_rates_generic import convert_currency
from eProc_Form_Builder.models import EformFieldData
from eProc_Shopping_Cart.models import CartItemDetails, ScItem

django_query_instance = DjangoQueries()


def calculate_item_total_value(call_off, quantity, catalog_qty, price_unit, price, overall_limit):
    """
    :param overall_limit:
    :param call_off:
    :param quantity:
    :param catalog_qty:
    :param price_unit:
    :param price:
    :return:
    """

    if call_off == CONST_CATALOG_CALLOFF:
        if catalog_qty is None:
            catalog_qty = quantity
        value = (float(catalog_qty) * float(price)) / int(price_unit)
        return round(value, 2)

    elif call_off == CONST_LIMIT_ORDER_CALLOFF:
        value = overall_limit
        return round(value, 2)

    else:
        value = (float(quantity) * float(price)) / int(price_unit)
        return round(value, 2)


def calculate_total_value(username):
    """
    :param username:
    :return:
    """
    total_value_sc = 0
    total_item_value = []
    cart_items = django_query_instance.django_filter_only_query(CartItemDetails, {
        'username': username, 'client': global_variables.GLOBAL_CLIENT
    })

    for items in cart_items:
        call_off = items.call_off
        if call_off == CONST_LIMIT_ORDER_CALLOFF:
            total_value = items.overall_limit
            return total_value
        else:
            quantity = items.quantity
            price = items.price
            price_unit = items.price_unit
            value = (float(quantity) * float(price)) / int(price_unit)
            if global_variables.GLOBAL_USER_CURRENCY != items.currency:
                value = convert_currency(value, str(items.currency),
                                         str(global_variables.GLOBAL_USER_CURRENCY))
            total_item_value.append(value)
            total_value_sc = round(sum(total_item_value), 2)
            total_value_sc = format(total_value_sc, '.2f')
    return total_value_sc


def calculate_pricing(username):
    """

    """
    total_item_value = []
    actual_price_list = []
    discount_value_list = []
    tax_value_list = []
    cart_items = django_query_instance.django_filter_only_query(CartItemDetails, {
        'username': username, 'client': global_variables.GLOBAL_CLIENT
    })

    for items in cart_items:
        call_off = items.call_off
        if call_off == CONST_LIMIT_ORDER_CALLOFF:
            total_value = items.overall_limit
            return total_value
        else:
            quantity = items.quantity
            price = items.price
            price_unit = items.price_unit
            value = (float(quantity) * float(price)) / int(price_unit)
            if global_variables.GLOBAL_USER_CURRENCY != items.currency:
                value = convert_currency(value, str(items.currency),
                                         str(global_variables.GLOBAL_USER_CURRENCY))
                actual_price_list.append(
                    convert_currency(float(items.actual_price) * items.quantity, str(items.currency),
                                     str(global_variables.GLOBAL_USER_CURRENCY)))
                discount_value_list.append(
                    convert_currency(items.discount_value, str(items.currency),
                                     str(global_variables.GLOBAL_USER_CURRENCY)))
                tax_value_list.append(
                    convert_currency(items.tax_value, str(items.currency), str(global_variables.GLOBAL_USER_CURRENCY)))
                # gross_price_list.append(convert_currency(float(items['gross_price'])*items['quantity'], str(item_currency), str(user_currency)))
            else:
                actual_price_list.append(float(items.actual_price) * items.quantity)
                discount_value_list.append(items.discount_value)
                tax_value_list.append(items.tax_value)
                # gross_price_list.append(float(items['gross_price'])*items['quantity'])
            total_item_value.append(value)
    # total price detail
    actual_price = round(sum(actual_price_list), 2)
    discount_value = round(sum(discount_value_list), 2)
    tax_value = round(sum(tax_value_list), 2)
    gross_price = round(sum(total_item_value), 2)
    pricing_data = {'gross_price': gross_price,
                    'actual_price': actual_price,
                    'discount_value': discount_value,
                    'tax_value': tax_value}
    return pricing_data


def get_product_price_from_eform(form_id):
    """
    gets default price by efrom id
    """
    item_price = get_base_price(form_id)
    if item_price != 0:
        additional_pricing_details = get_additional_default_price_details(form_id)
        item_price = get_item_price(item_price, additional_pricing_details)
    return item_price


def get_base_price(variant_id):
    """

    """
    base_price_value = 0
    base_price_eform_details = django_query_instance.django_get_query(VariantConfig,
                                                                      {'variant_id': variant_id,
                                                                       'client': global_variables.GLOBAL_CLIENT,
                                                                       'del_ind': False,
                                                                       'dropdown_pricetype': CONST_VARIANT_BASE_PRICING},
                                                                      )
    if base_price_eform_details:
        base_price_value = django_query_instance.django_filter_value_list_ordered_by_distinct_query(
            ProductEformPricing,
            {'variant_config_guid': base_price_eform_details.variant_config_guid,
             'pricing_data_default': True,
             'client': global_variables.GLOBAL_CLIENT}, 'price', None)[0]

    return float(base_price_value)


def get_additional_default_price_details(variant_id):
    """

    """
    additional_price_list = []
    additional_price_eform_details = django_query_instance.django_filter_query(VariantConfig,
                                                                               {'variant_id': variant_id,
                                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                                'del_ind': False,
                                                                                'dropdown_pricetype': CONST_VARIANT_ADDITIONAL_PRICING},
                                                                               None, ['default_variant_data',
                                                                                      'variant_config_guid'])
    # chage dictionary key from default_eform_field_data to price_data
    additional_price_eform_detail_list = rename_dictionary_list_key('default_variant_data', 'pricing_data',
                                                                    additional_price_eform_details)
    # query_list = form_q_query_from_list(additional_price_eform_detail_list)
    for additional_price_eform_detail in additional_price_eform_detail_list:
        additional_price_list.append(django_query_instance.django_filter_query(ProductEformPricing,
                                                                               additional_price_eform_detail,
                                                                               None,
                                                                               ['price', 'operator'])[0])
    return additional_price_list


def get_item_price(base_price, additional_pricing_details):
    """

    """
    item_price = base_price
    for additional_pricing in additional_pricing_details:
        if additional_pricing['operator'] == "PLUS":
            item_price = float(item_price) + float(additional_pricing['price'])

    return item_price


# def validate_price1(item_total_value, eform_detail, quantity, eform_id):
#     """
#
#     """
#     base_price = 0
#     validation_error = False
#     item_db_total_value = 0
#     for eform_data in eform_detail:
#         if eform_data['pricing_type'] == CONST_VARIANT_BASE_PRICING:
#             if django_query_instance.django_existence_check(ProductEformPricing, {
#                 'eform_field_config_guid': eform_data['eform_field_config_guid'],
#                 'pricing_data': eform_data['eform_field_data']}):
#                 base_price = \
#                     django_query_instance.django_filter_value_list_ordered_by_distinct_query(ProductEformPricing,
#                                                                                              {'eform_field_config_guid':
#                                                                                                   eform_data[
#                                                                                                       'eform_field_config_guid'],
#                                                                                               'pricing_data':
#                                                                                                   eform_data[
#                                                                                                       'eform_field_data']},
#                                                                                              'price',
#                                                                                              None)[0]
#                 break
#     if base_price:
#         base_price = check_discount_update_base_price(base_price, quantity, eform_id)
#         item_db_total_value = float(base_price)
#     for eform_data in eform_detail:
#         if eform_data['pricing_type'] == CONST_VARIANT_ADDITIONAL_PRICING:
#             if django_query_instance.django_existence_check(ProductEformPricing, {
#                 'eform_field_config_guid': eform_data['eform_field_config_guid'],
#                 'pricing_data': eform_data['eform_field_data']}):
#                 additional_price = django_query_instance.django_filter_value_list_ordered_by_distinct_query(
#                     ProductEformPricing,
#                     {'eform_field_config_guid': eform_data['eform_field_config_guid'],
#                      'pricing_data':
#                          eform_data[
#                              'eform_field_data']},
#                     'price',
#                     None)[0]
#                 item_db_total_value += float(additional_price)
#     price = item_db_total_value
#     item_db_total_value = float(item_db_total_value) * int(quantity)
#     if float(item_db_total_value) != float(item_total_value):
#         validation_error = True
#     return price, item_db_total_value, validation_error


def validate_price(item_total_value, eform_detail, quantity, discount_id):
    """

    """
    base_price = 0
    discount_percentage = 0
    validation_error = False
    item_db_total_value = 0
    additional_prices = 0
    additional_pricing_list = []
    for eform_data in eform_detail:
        if eform_data['pricing_type'] == CONST_VARIANT_BASE_PRICING:
            if django_query_instance.django_existence_check(ProductEformPricing,
                                                            {'variant_config_guid': eform_data[
                                                                'variant_config_guid'],
                                                             'product_eform_pricing_guid': eform_data[
                                                                 'product_eform_pricing_guid']}):
                base_price = \
                    django_query_instance.django_filter_value_list_ordered_by_distinct_query(ProductEformPricing,
                                                                                             {'variant_config_guid':
                                                                                                  eform_data[
                                                                                                      'variant_config_guid'],
                                                                                              'product_eform_pricing_guid':
                                                                                                  eform_data[
                                                                                                      'product_eform_pricing_guid']},
                                                                                             'price',
                                                                                             None)[0]
                break
    if base_price:
        base_price_with_discount, discount_percentage = check_discount_update_base_price(base_price, quantity, discount_id)
        item_db_total_value = float(base_price_with_discount)
    for eform_data in eform_detail:
        if eform_data['pricing_type'] == CONST_VARIANT_ADDITIONAL_PRICING:
            if django_query_instance.django_existence_check(ProductEformPricing, {
                'variant_config_guid': eform_data['variant_config_guid'],
                'product_eform_pricing_guid': eform_data['product_eform_pricing_guid']}):
                additional_price = django_query_instance.django_filter_value_list_ordered_by_distinct_query(
                    ProductEformPricing,
                    {'variant_config_guid': eform_data['variant_config_guid'],
                     'product_eform_pricing_guid':
                         eform_data[
                             'product_eform_pricing_guid']},
                    'price',
                    None)[0]
                additional_pricing_list.append(float(additional_price))
                item_db_total_value += float(additional_price)
    if additional_pricing_list:
        additional_prices = sum(additional_pricing_list)
    price = item_db_total_value
    item_db_total_value = float(item_db_total_value) * int(quantity)
    if float(item_db_total_value) != float(item_total_value):
        validation_error = True
    return price, item_db_total_value, validation_error, base_price, discount_percentage, additional_prices


def check_discount_update_base_price(base_price, quantity, discount_id):
    """

    """
    range_value_percentage = 0
    if django_query_instance.django_existence_check(DiscountData,
                                                    {'discount_id': discount_id,
                                                     'client': global_variables.GLOBAL_CLIENT,
                                                     'del_ind': False}):
        base_price, range_value_percentage = calculate_quantity_based_discount(discount_id, quantity, base_price)
    return base_price, range_value_percentage


def calculate_quantity_based_discount(discount_id, quantity, base_price):
    """

    """
    percentage = 0
    quantity_price_detail = django_query_instance.django_filter_query(DiscountData,
                                                                      {'discount_id': discount_id,
                                                                       'client': global_variables.GLOBAL_CLIENT,
                                                                       'del_ind': False},
                                                                      ['quantity'], ['quantity', 'discount_percentage'])
    for quantity_price in quantity_price_detail:
        quantity_price['quantity'] = int(quantity_price['quantity'])

    quantity_price_detail = sort_dic_list_by_value(quantity_price_detail, 'quantity')
    range_value_percentage = find_range(quantity_price_detail, quantity)
    if range_value_percentage:
        percentage = 100 - int(range_value_percentage['discount_percentage'])
        base_price = float(base_price) * percentage / 100
        percentage = range_value_percentage['discount_percentage']
    return base_price, percentage


def find_range(quantity_price_details, quantity):
    """

    """
    min_quantity = 0
    range_detail = 0
    quantity = int(quantity)

    if len(quantity_price_details) == 1:
        if quantity >= quantity_price_details[0]['quantity']:
            range_detail = quantity_price_details[0]
    else:
        for index, quantity_price_detail in enumerate(quantity_price_details):
            if quantity in range(min_quantity, int(quantity_price_detail['quantity']) - 1):
                if index != 0:
                    range_detail = quantity_price_details[index - 1]
                break
            if len(quantity_price_detail) - 1 == index:
                if quantity > int(quantity_price_detail['quantity']):
                    range_detail = quantity_price_detail
            min_quantity = int(quantity_price_detail['quantity'])

    return range_detail


def add_additional_price_to_base_price(base_price, product_eform_pricing_guid_list):
    """

    """
    additional_pricing = []
    if django_query_instance.django_existence_check(ProductEformPricing,
                                                    {'product_eform_pricing_guid__in': product_eform_pricing_guid_list,
                                                     'client': global_variables.GLOBAL_CLIENT,
                                                     'pricing_type': CONST_VARIANT_ADDITIONAL_PRICING,
                                                     'del_ind': False}):
        additional_price = django_query_instance.django_filter_value_list_ordered_by_distinct_query(ProductEformPricing,
                                                                                                    {
                                                                                                        'product_eform_pricing_guid__in': product_eform_pricing_guid_list,
                                                                                                        'client': global_variables.GLOBAL_CLIENT,
                                                                                                        'pricing_type': CONST_VARIANT_ADDITIONAL_PRICING,
                                                                                                        'del_ind': False},
                                                                                                    'price', None)

        additional_price = [float(item) for item in additional_price]
        if additional_price:
            additional_pricing = sum(additional_price)
        base_price += additional_pricing

    return base_price, additional_pricing


def calculate_item_price(guid, quantity):
    """

    """
    item_price = 0
    variant_id = None
    discount_percentage = 0
    additional_pricing = 0
    base_price_value = 0
    discount_id = None
    if CartItemDetails.objects.filter(Q(guid=guid), ~Q(variant_id=None)).exists():
        variant_id = django_query_instance.django_filter_value_list_ordered_by_distinct_query(CartItemDetails,
                                                                                            {'guid': guid},
                                                                                            'variant_id', None)[0]
        discount_id = django_query_instance.django_filter_value_list_ordered_by_distinct_query(CartItemDetails,
                                                                                              {'guid': guid},
                                                                                              'discount_id', None)[0]
    elif ScItem.objects.filter(Q(guid=guid), ~Q(variant_id=None)).exists():
        variant_id = django_query_instance.django_filter_value_list_ordered_by_distinct_query(ScItem,
                                                                                            {'guid': guid},
                                                                                            'variant_id', None)[0]
        discount_id = django_query_instance.django_filter_value_list_ordered_by_distinct_query(ScItem,
                                                                                               {'guid': guid},
                                                                                               'discount_id', None)[0]

    if variant_id:
        pricing_list = [CONST_VARIANT_BASE_PRICING, CONST_VARIANT_ADDITIONAL_PRICING, CONST_QUANTITY_BASED_DISCOUNT]
        if django_query_instance.django_existence_check(VariantConfig,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'del_ind': False,
                                                         'variant_id': variant_id,
                                                         'dropdown_pricetype__in': pricing_list}):
            product_eform_pricing_guid_list = EformFieldData.objects.filter((Q(cart_guid=guid) | Q(item_guid=guid)) &
                                                                            ~Q(product_eform_pricing_guid=None)).values_list(
                'product_eform_pricing_guid',
                flat=True)
            for pricing_guid in product_eform_pricing_guid_list:
                if django_query_instance.django_existence_check(ProductEformPricing,
                                                                {'product_eform_pricing_guid': pricing_guid,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'pricing_type': CONST_VARIANT_BASE_PRICING,
                                                                 'del_ind': False}):
                    base_price_value = \
                        django_query_instance.django_filter_value_list_ordered_by_distinct_query(ProductEformPricing,
                                                                                                 {
                                                                                                     'product_eform_pricing_guid': pricing_guid,
                                                                                                     'client': global_variables.GLOBAL_CLIENT,
                                                                                                     'pricing_type': CONST_VARIANT_BASE_PRICING,
                                                                                                     'del_ind': False},
                                                                                                 'price', None)[0]

            base_price, discount_percentage = check_discount_update_base_price(base_price_value, quantity, discount_id)
            print(base_price)
            item_price, additional_pricing = add_additional_price_to_base_price(float(base_price),
                                                                                product_eform_pricing_guid_list)
        else:
            if CartItemDetails.objects.filter(Q(guid=guid), ~Q(variant_id=None)).exists():
                item_price = django_query_instance.django_filter_value_list_ordered_by_distinct_query(CartItemDetails,
                                                                                                      {'guid': guid},
                                                                                                      'price', None)[0]
            elif ScItem.objects.filter(Q(guid=guid), ~Q(variant_id=None)).exists():
                item_price = django_query_instance.django_filter_value_list_ordered_by_distinct_query(ScItem,
                                                                                                      {'guid': guid},
                                                                                                      'price', None)[0]
    else:
        if CartItemDetails.objects.filter(Q(guid=guid)).exists():
            item_price = django_query_instance.django_filter_value_list_ordered_by_distinct_query(CartItemDetails,
                                                                                                  {'guid': guid},
                                                                                                  'price', None)[0]
        elif ScItem.objects.filter(Q(guid=guid)).exists():
            item_price = django_query_instance.django_filter_value_list_ordered_by_distinct_query(ScItem,
                                                                                                  {'guid': guid},
                                                                                                  'price', None)[0]
    print(item_price)
    return item_price, discount_percentage, base_price_value, additional_pricing


#
# def calculate_dynamic_price(eform_id, item_guid):
#     """
#
#     """
#     filter_queue = ~Q(product_eform_pricing_guid=None) & (Q(cart_guid=item_guid) | Q(cart_guid=item_guid))
#     django_query_instance.django_queue_query_value_list(EformFieldData,
#                                                         {'eform_id': eform_id},
#                                                         filter_queue,
#                                                         'product_eform_pricing_guid')
#     calculate_item_price()

def currency_convert_update(item_details):
    """

    """
    value = calculate_item_total_value(item_details.call_off, item_details.quantity, item_details.catalog_qty,
                                       item_details.price_unit, item_details.price, None)
    item_value = convert_currency(value, str(item_details.currency), str(global_variables.GLOBAL_USER_CURRENCY))
    if item_details.value != item_value:
        item_details.value = item_value
    item_details.save()
    return item_value
