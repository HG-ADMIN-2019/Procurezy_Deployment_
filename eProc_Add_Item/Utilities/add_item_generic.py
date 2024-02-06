from eProc_Add_Item.Utilities.add_item_specific import *
from eProc_Basic.Utilities.constants.constants import CONST_CATALOG_CALLOFF
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Price_Calculator.Utilities.price_calculator_generic import calculate_item_price, calculate_item_total_value
from eProc_Shopping_Cart.models import ScItem, ScHeader
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import get_price_discount_tax

django_query_instance = DjangoQueries()
from eProc_Exchange_Rates.Utilities.exchange_rates_generic import convert_currency


def exists_update_sc_item(header_guid, cart_item_detail, ui_quantity):
    """

    """
    db_quantity = cart_item_detail['quantity']
    quantity = int(cart_item_detail['quantity']) + int(ui_quantity)
    item_price, discount_percentage, base_price, additional_pricing = calculate_item_price(cart_item_detail['guid'],
                                                                                           quantity)
    actual_price, discount_value, tax_value, gross_price = get_price_discount_tax(item_price,
                                                                                  base_price,
                                                                                  additional_pricing,
                                                                                  None,
                                                                                  discount_percentage,
                                                                                  quantity)
    price_total_value = calculate_item_total_value(CONST_CATALOG_CALLOFF, quantity,
                                                   quantity, 1,
                                                   item_price, overall_limit=None)
    if cart_item_detail['currency'] != global_variables.GLOBAL_USER_CURRENCY:
        price_total_value = convert_currency(float(price_total_value), str(cart_item_detail['currency']),
                                             str(global_variables.GLOBAL_USER_CURRENCY))
    django_query_instance.django_update_query(ScItem,
                                              {'guid': cart_item_detail['guid'],
                                               'client': global_variables.GLOBAL_CLIENT,
                                               'del_ind': False},
                                              {'catalog_qty': quantity,
                                               'quantity': quantity,
                                               'value': price_total_value,
                                               'price': item_price,
                                               'discount_percentage': discount_percentage,
                                               'discount_value': discount_value,
                                               'gross_price': gross_price})
    sc_item_value_list = django_query_instance.django_filter_value_list_ordered_by_distinct_query(ScItem,
                                                                                                  {
                                                                                                      'client': global_variables.GLOBAL_CLIENT,
                                                                                                      'header_guid': header_guid},
                                                                                                  'value', None)
    total_value = sum(sc_item_value_list)
    django_query_instance.django_update_query(ScHeader,
                                              {'client': global_variables.GLOBAL_CLIENT,
                                               'guid': header_guid}, {'total_value': total_value})
    return True
