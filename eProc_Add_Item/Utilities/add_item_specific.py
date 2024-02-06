import decimal
from decimal import Decimal

from django.db.models import Q

from eProc_Add_Item.Utilities.add_item_generic import exists_update_sc_item
from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.dict_check_key import checkKey
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries, bulk_create_entry_db
from eProc_Basic.Utilities.functions.encryption_util import decrypt
from eProc_Basic.Utilities.functions.get_db_query import getUsername, getClients, display_cart_counter
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.insert_remove import dictionary_remove_insert_first, remove_dictionary_from_list
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG125, MSG016, MSG0199
from eProc_Configuration.models import *
from eProc_Configuration.models import ProductsDetail, FreeTextForm, Currency, UnitOfMeasures, ProductEformPricing
from eProc_Configuration.models.development_data import *
from eProc_Exchange_Rates.Utilities.exchange_rates_generic import convert_currency
from eProc_Form_Builder.models import EformFieldData
from eProc_Price_Calculator.Utilities.price_calculator_generic import calculate_item_total_value, validate_price, \
    calculate_item_price, check_discount_update_base_price
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import get_prod_by_id, get_price_discount_tax
from eProc_Shopping_Cart.Utilities.save_order_edit_sc import EditShoppingCart
from eProc_Shopping_Cart.models import CartItemDetails, ScHeader, ScItem
import datetime

django_query_instance = DjangoQueries()


# Function to create or update freetext item
def update_create_free_text(free_text_fields, request):
    """
    :param request:
    :param free_text_fields:
    :return:
    """
    client = getClients(request)
    eform = free_text_fields[0]
    guid = free_text_fields[1]
    item_name = free_text_fields[2]
    prod_desc = free_text_fields[3]
    price = free_text_fields[4]
    uom = free_text_fields[5]
    del_date = free_text_fields[6]
    quantity = free_text_fields[7]
    supp_id = free_text_fields[8]
    header_guid = ''
    document_number = request.POST.get('document_number')
    if document_number != 'create' and document_number is not None:
        document_number = decrypt(document_number)

        if django_query_instance.django_existence_check(ScHeader, {'doc_number': document_number, 'client': client}):
            header_guid = django_query_instance.django_get_query(ScHeader, {'doc_number': document_number,
                                                                            'client': client}).guid

    product_category_id = request.POST.get('product_category_id')
    print(product_category_id)
    prod_id = django_query_instance.django_get_query(FreeTextForm, {'supp_id': supp_id,
                                                                    'prod_cat_id': product_category_id,
                                                                    'client': client})

    free_text_data = {
        'guid': guid,
        'description': item_name,
        'prod_cat_desc': prod_desc,
        'unit': uom,
        'price': price,
        'item_del_date': del_date,
        'quantity': quantity,
        'call_off': CONST_FREETEXT_CALLOFF,
        'supplier_id': supp_id,
        'price_unit': 1,
        'username': global_variables.GLOBAL_LOGIN_USERNAME,
        'prod_cat': prod_id.prod_cat_id,
        'client_id': client,
        'lead_time': prod_id.lead_time,
        'form_id': free_text_fields[19]
    }
    if eform == 'true' or eform == True:
        field_value1 = free_text_fields[9]
        field_value2 = free_text_fields[10]
        field_value3 = free_text_fields[11]
        field_value4 = free_text_fields[12]
        field_value5 = free_text_fields[13]
        field_value6 = free_text_fields[14]
        field_value7 = free_text_fields[15]
        field_value8 = free_text_fields[16]
        field_value9 = free_text_fields[17]
        field_value10 = free_text_fields[18]
        form_id = free_text_fields[19]

        # django_query_instance.django_update_or_create_query(EformData, {'cart_guid': guid}, {
        #     'cart_guid': guid,
        #     'form_field1': field_value1,
        #     'form_field2': field_value2,
        #     'form_field3': field_value3,
        #     'form_field4': field_value4,
        #     'form_field5': field_value5,
        #     'form_field6': field_value6,
        #     'form_field7': field_value7,
        #     'form_field8': field_value8,
        #     'form_field9': field_value9,
        #     'form_field10': field_value10,
        #     'form_id': form_id,
        #     'client_id': client
        # })

    if header_guid != '':
        del free_text_data['username']
        del free_text_data['prod_cat_desc']
        del free_text_data['supplier_id']
        free_text_data['header_guid'] = django_query_instance.django_get_query(ScHeader, {'guid': header_guid,
                                                                                          'client': client,
                                                                                          'del_ind': False})
        free_text_data['prod_cat'] = prod_id.prod_cat_id
        free_text_data['unspsc'] = prod_id.prod_cat_id
        free_text_data['supplier_id'] = supp_id
        free_text_data['process_flow'] = 'Green'
        free_text_data['prod_type'] = '01'
        free_text_data['catalog_id'] = 'Majjaka_Catalog'
        free_text_data['price'] = price
        free_text_data['price_unit'] = 1
        free_text_data['unit'] = uom
        free_text_data['supp_prod_num'] = CONST_FREETEXT_CALLOFF
        free_text_data['call_off'] = CONST_FREETEXT_CALLOFF
        free_text_data['del_ind'] = False
        free_text_data['created_at'] = datetime.datetime.now()
        free_text_data['object_type'] = CONST_DOC_TYPE_SC
        free_text_data['quantity'] = quantity
        free_text_data['value'] = calculate_item_total_value(CONST_FREETEXT_CALLOFF, quantity, quantity, 1, price,
                                                             overall_limit=None)
        free_text_data['eform'] = eform
        free_text_data['client'] = django_query_instance.django_get_query(OrgClients, {'client': client,
                                                                                       'del_ind': False})
        free_text_data['description'] = item_name
        edit_object = EditShoppingCart(request)
        is_saved = edit_object.add_item_to_saved_cart(header_guid, free_text_data)
        if not is_saved[0]:
            return False, is_saved[1]
        else:
            return True, ''
    else:
        django_query_instance.django_update_or_create_query(CartItemDetails, {'guid': guid}, free_text_data)
        return True, ''


def update_create_free_text_item(freetext_ui_data):
    """

    """
    client = global_variables.GLOBAL_CLIENT
    cart_guid = None
    item_guid = None
    freetext_detail = []
    header_guid = ''
    document_number = freetext_ui_data['document_number']
    if document_number != 'create' and document_number is not None:
        document_number = decrypt(document_number)

        if django_query_instance.django_existence_check(ScHeader, {'doc_number': document_number, 'client': client}):
            header_guid = django_query_instance.django_get_query(ScHeader, {'doc_number': document_number,
                                                                            'client': client}).guid

    if django_query_instance.django_existence_check(FreeTextDetails,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'freetext_id': freetext_ui_data['freetext_id'],
                                                     'del_ind': False}):
        freetext_detail = django_query_instance.django_get_query(FreeTextDetails,
                                                                 {'client': global_variables.GLOBAL_CLIENT,
                                                                  'freetext_id': freetext_ui_data['freetext_id'],
                                                                  'del_ind': False})
    guid = guid_generator()
    value = calculate_item_total_value(CONST_FREETEXT_CALLOFF, freetext_ui_data['quantity'],
                                       freetext_ui_data['quantity'], 1,
                                       freetext_ui_data['price'], None)
    free_text_data = {
        'guid': guid,
        'item_num': get_cart_item_max_num(),
        'description': freetext_ui_data['item_name'],
        'long_desc': freetext_ui_data['prod_desc'],
        'unit': freetext_ui_data['uom'],
        'price': freetext_ui_data['price'],
        'gross_price': freetext_ui_data['price'],
        'actual_price': freetext_ui_data['price'],
        'base_price': freetext_ui_data['price'],
        'additional_price': 0,
        'discount_percentage': 0,
        'discount_value': 0,
        'tax_value': 0,
        'sgst': 0,
        'cgst': 0,
        'vat': 0,
        'value': value,
        'item_del_date': freetext_ui_data['item_del_date'],
        'quantity': freetext_ui_data['quantity'],
        'call_off': CONST_FREETEXT_CALLOFF,
        'supplier_id': freetext_detail.supplier_id,
        'pref_supplier': freetext_detail.supplier_id,
        'price_unit': freetext_ui_data['price_unit'],
        'username': global_variables.GLOBAL_LOGIN_USERNAME,
        'prod_cat_id': freetext_detail.prod_cat_id,
        'client_id': client,
        'lead_time': freetext_detail.lead_time,
        'eform_id': freetext_detail.eform_id,
        'currency': freetext_detail.currency_id,
        'int_product_id': freetext_detail.freetext_id,
        'supp_product_id': freetext_detail.supp_product_id,
        'prod_cat_desc': get_prod_by_id(freetext_detail.prod_cat_id)

    }
    free_text_data = update_supplier_detail(free_text_data, freetext_detail.supplier_id)
    if header_guid == '':
        django_query_instance.django_update_or_create_query(CartItemDetails, {'guid': guid}, free_text_data)
        cart_guid = guid
    if freetext_ui_data['freetext_id']:
        create_free_text_eform(freetext_detail, freetext_ui_data, cart_guid, item_guid)
    return True, ''


def create_free_text_eform(freetext_detail, freetext_ui_data, cart_guid, item_guid):
    """

    """
    dictionary_list = []
    if freetext_detail.eform_id:
        if item_guid:
            item_guid = django_query_instance.django_get_query(ScItem,
                                                               {'guid': item_guid,
                                                                'client': global_variables.GLOBAL_CLIENT})
        for item_detail in freetext_ui_data['eform_data']:
            eform_dictionary = {'eform_field_data_guid': guid_generator(),
                                'eform_id': freetext_detail.eform_id,
                                'cart_guid': cart_guid,
                                'item_guid': item_guid,
                                'eform_type': CONST_FT_ITEM_EFORM,
                                'eform_field_count': int(item_detail['eform_field_count']),
                                'eform_field_name': item_detail['eform_field_name'],
                                'client': global_variables.GLOBAL_CLIENT,
                                'eform_field_data': item_detail['eform_field_data']}
            dictionary_list.append(eform_dictionary)
        bulk_create_entry_db(EformFieldData, dictionary_list)


class CartItem:
    def __init__(self, requester, user_currency, selected_currency):
        self.requester = requester
        self.client = global_variables.GLOBAL_CLIENT
        self.user_currency = user_currency
        self.selected_currency = selected_currency

    @staticmethod
    def add_or_update_item(guid, item_details):
        django_query_instance.django_update_or_create_query(CartItemDetails, {'guid': guid}, item_details)

    def check_for_cart_update_or_create(self, user_cart_item_dic_list, eform_detail):
        eform_data_existence_flag = True
        user_cart_item_detail = []
        cart_item_detail = None
        for user_cart_item in user_cart_item_dic_list:
            eform_data_existence_flag = True
            if django_query_instance.django_existence_check(EformFieldData,
                                                            {'client': self.client,
                                                             'cart_guid': user_cart_item['guid']}):
                for eform_data in eform_detail:
                    eform_field_name, eform_field_data = self.get_eform_field_data(eform_data)
                    if not django_query_instance.django_existence_check(EformFieldData,
                                                                        {'client': self.client,
                                                                         'cart_guid': user_cart_item['guid'],
                                                                         'eform_field_name': eform_field_name,
                                                                         'eform_field_data': eform_field_data}):
                        eform_data_existence_flag = False
                        # user_cart_item_dic_list = remove_dictionary_from_list(user_cart_item_dic_list,
                        #                                                          'guid',user_cart_item['guid'])
                if eform_data_existence_flag:
                    user_cart_item_detail.append(user_cart_item)

        if len(user_cart_item_detail) == 1:
            cart_item_detail = user_cart_item_detail[0]
            eform_data_existence_flag = True

        return eform_data_existence_flag, cart_item_detail

    @staticmethod
    def get_eform_field_data(eform_data):
        """

        """
        eform_field_name = django_query_instance.django_filter_value_list_query(VariantConfig,
                                                                                {
                                                                                    'client': global_variables.GLOBAL_CLIENT,
                                                                                    'variant_config_guid':
                                                                                        eform_data[
                                                                                            'variant_config_guid']},
                                                                                'variant_name')[0]
        if eform_data['pricing_type'] != CONST_VARIANT_WITHOUT_PRICING:
            eform_field_data = django_query_instance.django_filter_value_list_query(ProductEformPricing,
                                                                                    {
                                                                                        'client': global_variables.GLOBAL_CLIENT,
                                                                                        'product_eform_pricing_guid':
                                                                                            eform_data[
                                                                                                'product_eform_pricing_guid']},
                                                                                    'pricing_data')[0]

        else:
            eform_field_data = eform_data['data']
        return eform_field_name, eform_field_data

    def limit_order_validation(self, call_off):
        if call_off == CONST_LIMIT_ORDER_CALLOFF:
            cart_item = django_query_instance.django_existence_check(CartItemDetails, {'username': self.requester,
                                                                                       'client': self.client})
        else:
            cart_item = False

        return cart_item

    def update_item_details_for_limit(self, item_details):
        if 'guid' in item_details:
            guid = item_details['guid']
        else:
            guid = guid_generator()

        item_details['guid'] = guid
        if item_details['call_off'] == CONST_LIMIT_ORDER_CALLOFF:
            follow_up_action = item_details['follow_up_action']
            required = item_details['required']

            if follow_up_action == 'Invoice & Confirmation Only':
                item_details['ir_gr_ind_limi'] = True
                item_details['gr_ind_limi'] = False
            else:
                item_details['gr_ind_limi'] = True
                item_details['ir_gr_ind_limi'] = False

            if required == 'On':
                item_details['start_date'] = None
                item_details['end_date'] = None

            if required == 'From':
                item_details['item_del_date'] = None
                item_details['end_date'] = None

            if required == 'Between':
                item_details['item_del_date'] = None

        del item_details['required']
        del item_details['follow_up_action']
        item_details['price'] = 0
        item_details['price_unit'] = 1
        item_details['quantity'] = 0
        item_details['username'] = self.requester
        item_details['client'] = self.client
        item_details['prod_cat_desc'] = get_prod_by_id(item_details['prod_cat'])
        item_details['value'] = calculate_item_total_value(CONST_LIMIT_ORDER_CALLOFF, item_details['quantity'],
                                                           item_details['quantity'], 1, item_details['price'],
                                                           overall_limit=None)

        return guid, item_details

    def update_item_details_for_pr(self, item_details, document_number, edit_object):
        if 'guid' in item_details:
            guid = item_details['guid']
        else:
            guid = guid_generator()

        header_guid = ''
        client = self.client
        if document_number != 'create':
            document_number = decrypt(document_number)
            if django_query_instance.django_existence_check(ScHeader,
                                                            {'doc_number': document_number, 'client': client}):
                header_guid = django_query_instance.django_get_query(ScHeader, {'doc_number': document_number,
                                                                                'client': client}).guid

        item_details['prod_cat_desc'] = get_prod_by_id(item_details['prod_cat_id'])
        item_value = calculate_item_total_value(CONST_PR_CALLOFF, item_details['quantity'],
                                                item_details['quantity'], 1, item_details['price'],
                                                overall_limit=None)
        if item_details['currency'] != global_variables.GLOBAL_USER_CURRENCY:
            item_details['value'] = convert_currency(item_value, str(item_details['currency']),
                                                     str(global_variables.GLOBAL_USER_CURRENCY))
        else:
            item_details['value'] = item_value
        item_details['price_unit'] = 1
        item_details['username'] = self.requester
        item_details['client'] = self.client
        item_details['item_num'] = get_cart_item_max_num()
        item_details['gross_price'] = item_details['price']
        item_details['actual_price'] = item_details['price']
        item_details['base_price'] = item_details['price']
        item_details['additional_price'] = 0
        item_details['discount_percentage'] = 0
        item_details['discount_value'] = 0
        item_details['tax_value'] = 0
        item_details['sgst'] = 0
        item_details['cgst'] = 0
        item_details['vat'] = 0

        item_value = calculate_item_total_value(item_details['call_off'], item_details['quantity'], None,
                                                item_details['quantity'], item_details['price'], overall_limit=None)

        item_value = convert_currency(item_value, str(self.selected_currency), str(self.user_currency))
        if item_value:
            item_value = round(item_value, 2)
        if header_guid == '':
            return guid, item_details, item_value
        else:
            del item_details['username']
            del item_details['prod_cat_desc']
            item_details['header_guid'] = django_query_instance.django_get_query(ScHeader, {
                'guid': header_guid, 'client': client, 'del_ind': False
            })
            item_details['process_flow'] = 'Red'
            item_details['prod_type'] = '01'
            item_details['catalog_id'] = 'Majjaka_Catalog'
            item_details['item_del_date'] = datetime.datetime.now()
            item_details['price_unit'] = 1
            item_details['call_off'] = CONST_PR_CALLOFF
            item_details['del_ind'] = False
            item_details['created_at'] = datetime.datetime.now()
            item_details['document_type'] = CONST_DOC_TYPE_SC
            item_details['lead_time'] = item_details['lead_time']
            item_details['quantity'] = item_details['quantity']
            item_details['gross_price'] = item_details['price']
            item_details['client'] = django_query_instance.django_get_query(OrgClients, {'client': client,
                                                                                         'del_ind': False})

            is_saved = edit_object.add_item_to_saved_cart(header_guid, item_details)

            return is_saved[0], is_saved[1], ''

    def update_item_details_for_freetext(self, item_details, document_number, edit_object):
        header_guid = ''
        quantity = item_details['quantity']
        freetext_detail = []
        cart_guid = None
        item_guid = None
        if document_number != 'create':

            document_number = decrypt(document_number)
            if django_query_instance.django_existence_check(ScHeader, {
                'doc_number': document_number, 'client': self.client
            }):
                header_guid = django_query_instance.django_get_query(ScHeader, {
                    'doc_number': document_number, 'client': self.client
                })

        guid = guid_generator()

        if header_guid != '':
            if django_query_instance.django_existence_check(FreeTextDetails,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'freetext_id': item_details['freetext_id'],
                                                             'del_ind': False}):
                freetext_detail = django_query_instance.django_get_query(FreeTextDetails,
                                                                         {'client': global_variables.GLOBAL_CLIENT,
                                                                          'freetext_id': item_details[
                                                                              'freetext_id'],
                                                                          'del_ind': False})
            value = calculate_item_total_value(CONST_FREETEXT_CALLOFF, quantity, quantity, 1,
                                               item_details['price'], overall_limit=None)
            free_text_data = {
                'guid': guid,
                'item_num': get_cart_item_max_num(),
                'description': item_details['item_name'],
                'long_desc': item_details['prod_desc'],
                'unit': item_details['uom'],
                'price': item_details['price'],
                'gross_price': item_details['price'],
                'actual_price': item_details['price'],
                'base_price': item_details['price'],
                'additional_price': 0,
                'discount_percentage': 0,
                'discount_value': 0,
                'tax_value': 0,
                'sgst': 0,
                'cgst': 0,
                'vat': 0,
                'currency': freetext_detail.currency_id,
                'value': decimal.Decimal(value),
                'item_del_date': item_details['item_del_date'],
                'quantity': item_details['quantity'],
                'call_off': CONST_FREETEXT_CALLOFF,
                'supplier_id': freetext_detail.supplier_id,
                'pref_supplier': freetext_detail.supplier_id,
                'price_unit': item_details['price_unit'],
                'prod_cat_id': freetext_detail.prod_cat_id,
                'client_id': global_variables.GLOBAL_CLIENT,
                'lead_time': freetext_detail.lead_time,
                'eform_id': freetext_detail.eform_id,
                'currency': freetext_detail.currency_id,
                'int_product_id': freetext_detail.freetext_id,
                'supp_product_id': freetext_detail.supp_product_id,
                'prod_cat_desc': get_prod_by_id(freetext_detail.prod_cat_id),
                'header_guid': header_guid
            }
            free_text_data = update_supplier_detail(free_text_data, freetext_detail.supplier_id)

            flag, item_guid = edit_object.add_item_to_saved_cart(header_guid, free_text_data)
            if item_details['freetext_id']:
                create_free_text_eform(freetext_detail, item_details, cart_guid, item_guid)

    def update_eform_details(self, cart_guid, eform_details, form_id):
        list_keys = list(eform_details.keys())
        for key in list_keys:
            if not key.startswith('form_field'):
                del eform_details[key]

        eform_details['form_id'] = django_query_instance.django_get_query(FreeTextForm, {'form_id': form_id})
        eform_details['client_id'] = self.client
        eform_details['cart_guid'] = cart_guid

        # django_query_instance.django_update_or_create_query(EformData, {'cart_guid': cart_guid}, eform_details)

    def add_catalog_item(self, product_id, edit_object, document_number, username, quantity, item_details):
        header_instance = ''
        header_guid = ''
        catalog_id = ''
        eform_check_flag = False
        user_cart_item_guid = []
        user_cart_item = None
        eform_data_existence_flag = False
        user_cart_item_dic_list = []
        user_cart_item_quantity = 0
        additional_price = 0
        discount_percentage = 0
        if document_number != 'create':
            document_number = decrypt(document_number)
            if django_query_instance.django_existence_check(ScHeader, {
                'doc_number': document_number, 'client': self.client
            }):
                header_instance = django_query_instance.django_get_query(ScHeader, {
                    'doc_number': document_number,
                    'client': self.client
                })
                header_guid = header_instance.guid

        get_prd_ref = django_query_instance.django_get_query(ProductsDetail,
                                                             {'product_id': product_id, 'client': self.client})
        if get_prd_ref:
            tax = {'sgst': get_prd_ref.sgst, 'cgst': get_prd_ref.cgst, 'vat': get_prd_ref.vat}
            if document_number == 'create':
                eform_existence_flag = False
                if django_query_instance.django_filter_count_query(CartItemDetails,
                                                                   {'client': self.client,
                                                                    'username': global_variables.GLOBAL_LOGIN_USERNAME,
                                                                    'int_product_id': get_prd_ref.product_id}) == 1:
                    user_cart_item = django_query_instance.django_get_query(CartItemDetails, {
                        'client': self.client,
                        'username': global_variables.GLOBAL_LOGIN_USERNAME,
                        'int_product_id': get_prd_ref.product_id})
                    user_cart_item_dic_list = [{'guid': user_cart_item.guid, 'quantity': user_cart_item.quantity}]
                    # check if eform with pricing not exist then update quantity,value from product detail and save
                    if not django_query_instance.django_existence_check(EformFieldData,
                                                                        {'client': self.client,
                                                                         'cart_guid': user_cart_item.guid}):
                        total_quantity = int(user_cart_item.quantity) + int(quantity)
                        user_cart_item.quantity = total_quantity
                        # if eform without impact on price then calculate discount from product details value
                        if get_prd_ref.variant_id:
                            queue_query = Q()
                            queue_query = ~Q(
                                dropdown_pricetype__in=[CONST_VARIANT_BASE_PRICING, CONST_VARIANT_ADDITIONAL_PRICING])
                            if django_query_instance.django_queue_existence_check(VariantConfig,
                                                                                  {
                                                                                      'client': global_variables.GLOBAL_CLIENT,
                                                                                      'del_ind': False,
                                                                                      'variant_id': get_prd_ref.variant_id},
                                                                                  queue_query):
                                user_cart_item.price, discount_percentage = check_discount_update_base_price(
                                    get_prd_ref.price, total_quantity,
                                    get_prd_ref.discount_id)
                                actual_price, discount_value, tax_value, gross_price = get_price_discount_tax(
                                    get_prd_ref.price,
                                    user_cart_item.base_price,
                                    user_cart_item.additional_price,
                                    tax,
                                    discount_percentage,
                                    quantity)
                                user_cart_item.discount_percentage = discount_percentage
                                user_cart_item.discount_value = discount_value
                                user_cart_item.tax_value = tax_value
                                user_cart_item.gross_price = gross_price
                                user_cart_item.value = calculate_item_total_value(CONST_CATALOG_CALLOFF, quantity,
                                                                                  quantity, 1,
                                                                                  user_cart_item.price,
                                                                                  overall_limit=None)

                        user_cart_item.save()
                        cart_count = display_cart_counter(global_variables.GLOBAL_LOGIN_USERNAME)
                        return True, 'Item added to cart successfully', cart_count
                    else:
                        eform_check_flag = True
                elif django_query_instance.django_filter_count_query(CartItemDetails,
                                                                     {'client': self.client,
                                                                      'username': global_variables.GLOBAL_LOGIN_USERNAME,
                                                                      'int_product_id': get_prd_ref.product_id}) > 1:
                    user_cart_item_dic_list = django_query_instance.django_filter_query(CartItemDetails,
                                                                                        {'client': self.client,
                                                                                         'username': global_variables.GLOBAL_LOGIN_USERNAME,
                                                                                         'int_product_id': get_prd_ref.product_id},
                                                                                        None, ['guid', 'quantity'])
                    # check eform data exists then set eform check flag
                    for user_cart_item_dic in user_cart_item_dic_list:
                        if django_query_instance.django_existence_check(EformFieldData,
                                                                        {'client': self.client,
                                                                         'cart_guid': user_cart_item_dic['guid']}):
                            eform_check_flag = True
                            break

            base_price = float(get_prd_ref.price)
            actual_price, discount_value, tax_value, gross_price = get_price_discount_tax(get_prd_ref.price, base_price,
                                                                                          additional_price, tax,
                                                                                          discount_percentage, quantity)

            if django_query_instance.django_existence_check(CatalogMapping,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'call_off': CONST_CATALOG_CALLOFF,
                                                             'item_id': get_prd_ref.product_id}):
                catalog_id = django_query_instance.django_filter_value_list_query(CatalogMapping,
                                                                                  {
                                                                                      'client': global_variables.GLOBAL_CLIENT,
                                                                                      'call_off': CONST_CATALOG_CALLOFF,
                                                                                      'item_id': get_prd_ref.product_id},
                                                                                  'catalog_id')[0]
                catalog_desc = django_query_instance.django_filter_value_list_query(Catalogs,
                                                                                    {
                                                                                        'client': global_variables.GLOBAL_CLIENT,
                                                                                        'catalog_id': catalog_id},
                                                                                    'description')
            catalog_content = {
                'description': get_prd_ref.short_desc,
                'item_num': get_cart_item_max_num(),
                'prod_type': get_prd_ref.prod_type,
                # 'guid': guid_generator(),
                'username': username,
                'client': self.client,
                'call_off': CONST_CATALOG_CALLOFF,
                'quantity': int(quantity),
                'prod_cat_desc': get_prod_by_id(get_prd_ref.prod_cat_id.prod_cat_id),
                'price': float(get_prd_ref.price),
                'discount_id': get_prd_ref.discount_id,
                'base_price': base_price,
                'additional_price': additional_price,
                'actual_price': actual_price,
                'gross_price': gross_price,
                'discount_percentage': discount_percentage,
                'discount_value': float(discount_value),
                'sgst': tax['sgst'],
                'cgst': tax['cgst'],
                'vat': tax['vat'],
                'tax_value': float(tax_value),
                'unit': get_prd_ref.unit_id,
                'currency': get_prd_ref.currency_id,
                'lead_time': get_prd_ref.lead_time,
                'price_unit': 1,
                'prod_cat_id': get_prd_ref.prod_cat_id.prod_cat_id,
                'product_info_id': get_prd_ref.product_info_id,
                'supplier_id': get_prd_ref.supplier_id,
                'pref_supplier': get_prd_ref.supplier_id,
                'int_product_id': get_prd_ref.product_id,
                'supp_product_id': get_prd_ref.supp_product_id,
                'long_desc': get_prd_ref.long_desc,
                'manufacturer': get_prd_ref.manufacturer,
                'manu_part_num': get_prd_ref.manu_part_num,
                'manu_code_num': get_prd_ref.manu_code_num,
                'quantity_min': get_prd_ref.quantity_min,
                'quantity_max': get_prd_ref.quantity_max,
                'tiered_flag': get_prd_ref.tiered_flag,
                'ctr_num': get_prd_ref.ctr_num,
                'ctr_item_num': get_prd_ref.ctr_item_num,
                'ctr_name': get_prd_ref.ctr_name,
                'bundle_flag': get_prd_ref.bundle_flag,

            }
            update_supplier_detail(catalog_content, get_prd_ref.supplier_id)

            if header_guid != '':
                is_success = []
                product_id_exists = False
                eform_existence_flag = False
                del catalog_content['username']
                del catalog_content['int_product_id']
                catalog_content['int_product_id'] = get_prd_ref.product_id
                catalog_content["header_guid"] = django_query_instance.django_get_query(ScHeader,
                                                                                        {'guid': header_instance.guid})
                catalog_content['prod_cat_id'] = get_prd_ref.prod_cat_id.prod_cat_id
                catalog_content['product_info_id'] = get_prd_ref.product_info_id
                catalog_content['process_flow'] = 'Green'
                catalog_content['prod_type'] = '01'
                catalog_content['catalog_id'] = 'Majjaka_Catalog'
                catalog_content['item_del_date'] = datetime.datetime.now()
                catalog_content['del_ind'] = False
                catalog_content['created_at'] = datetime.datetime.now()
                catalog_content['document_type'] = CONST_DOC_TYPE_SC
                catalog_content['catalog_qty'] = quantity
                catalog_content['quantity'] = quantity
                catalog_content['variant_id'] = None
                catalog_content['item_num'] = get_sc_item_max_num(header_instance.guid)
                # if catalog  with eform exists
                if get_prd_ref.variant_id:
                    # check product already exist in ScItem table and EformFieldData
                    eform_existence_flag, item_detail, item_quantity = self.check_if_exist_update_sc_item(
                        get_prd_ref.product_id, header_instance.guid,
                        item_details['eform_detail'], quantity)
                    if eform_existence_flag:
                        is_success.append(True)
                        is_success.append('')
                    else:
                        # item_price = calculate_item_price(item_detail['guid'], quantity)
                        price, item_price, validation_error, base_price, discount_percentage, additional_price = validate_price(
                            item_details['item_total_value'],
                            item_details['eform_detail'], quantity, get_prd_ref.discount_id)
                        if not validation_error:
                            if catalog_content['currency'] != global_variables.GLOBAL_USER_CURRENCY:
                                catalog_content['value'] = convert_currency(item_price,
                                                                            str(catalog_content['currency']),
                                                                            str(global_variables.GLOBAL_USER_CURRENCY))
                            else:
                                catalog_content['value'] = item_price
                            catalog_content['price'] = price
                            actual_price, discount_value, tax_value, gross_price = get_price_discount_tax(price,
                                                                                                          base_price,
                                                                                                          additional_price,
                                                                                                          tax,
                                                                                                          discount_percentage,
                                                                                                          quantity)
                            catalog_content['actual_price'] = actual_price
                            catalog_content['discount_value'] = discount_value
                            catalog_content['tax_value'] = tax_value
                            catalog_content['gross_price'] = gross_price
                            catalog_content['discount_percentage'] = discount_percentage
                            catalog_content['base_price'] = base_price
                            catalog_content['additional_price'] = additional_price
                            catalog_content['variant_id'] = item_details['eform_id']
                    pricing_list = [CONST_VARIANT_BASE_PRICING, CONST_VARIANT_ADDITIONAL_PRICING,
                                    CONST_QUANTITY_BASED_DISCOUNT]
                    if not django_query_instance.django_existence_check(VariantConfig,
                                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                                         'del_ind': False,
                                                                         'variant_id': item_details['eform_id'],
                                                                         'dropdown_pricetype__in': pricing_list}):
                        item_price = get_prd_ref.price
                        catalog_content['value'] = calculate_item_total_value(CONST_CATALOG_CALLOFF, quantity,
                                                                              quantity, 1,
                                                                              item_price, overall_limit=None)
                        if get_prd_ref.currency != header_instance.currency:
                            catalog_content['value'] = convert_currency(catalog_content['value'],
                                                                        str(get_prd_ref.currency),
                                                                        str(header_instance.currency))
                else:
                    item_price = get_prd_ref.price
                    if django_query_instance.django_existence_check(ScItem,
                                                                    {'header_guid': header_instance.guid,
                                                                     'client': global_variables.GLOBAL_CLIENT,
                                                                     'int_product_id': get_prd_ref.product_id
                                                                     }):
                        cart_item_detail = django_query_instance.django_filter_query(ScItem,
                                                                                     {
                                                                                         'header_guid': header_instance.guid,
                                                                                         'client': global_variables.GLOBAL_CLIENT,
                                                                                         'int_product_id': get_prd_ref.product_id
                                                                                     }, None, None)[0]
                        product_id_exists = exists_update_sc_item(header_instance.guid, cart_item_detail, quantity)
                        is_success.append(True)
                        is_success.append('')
                        return True, 'Item added to sc tables'
                if not get_prd_ref.variant_id:
                    catalog_content['value'] = calculate_item_total_value(CONST_CATALOG_CALLOFF, quantity,
                                                                          quantity, 1,
                                                                          item_price, overall_limit=None)
                    if header_instance.currency != get_prd_ref.currency:
                        catalog_content['value'] = convert_currency(catalog_content['value'],
                                                                    str(get_prd_ref.currency),
                                                                    str(header_instance.currency))
                        # catalog_content['eform'] = None
                catalog_content['client'] = django_query_instance.django_get_query(OrgClients, {
                    'client': global_variables.GLOBAL_CLIENT,
                    'del_ind': False})
                catalog_content['supp_product_id'] = get_prd_ref.supp_product_id
                catalog_content['item_del_date'] = datetime.datetime.now()
                if not product_id_exists:
                    if not eform_existence_flag:
                        if checkKey(item_details, 'eform_id'):
                            catalog_content['variant_id'] = item_details['eform_id']
                        is_success = edit_object.add_item_to_saved_cart(header_instance.guid, catalog_content)

                    if get_prd_ref.variant_id and catalog_content['call_off'] == CONST_CATALOG_CALLOFF:
                        sc_item_guid = django_query_instance.django_filter_value_list_ordered_by_distinct_query(ScItem,
                                                                                                                {
                                                                                                                    'header_guid': header_instance.guid,
                                                                                                                    'client': global_variables.GLOBAL_CLIENT,
                                                                                                                    'del_ind': False},
                                                                                                                'guid',
                                                                                                                [
                                                                                                                    '-item_num'])[
                            0]

                        update_product_detail_eform(item_details, None, sc_item_guid)

                if is_success[0]:
                    msgid = 'MSG125'
                    error_msg = get_message_desc(msgid)[1]
                    # msg = error_msg['message_desc'][0]
                    # error_msg = msg
                    return True, error_msg
                else:
                    return False, is_success[1]

            else:
                cart_item_guid = guid_generator()
                if checkKey(item_details, 'eform_id'):

                    catalog_content['variant_id'] = get_prd_ref.variant_id

                    catalog_content['product_info_id'] = get_prd_ref.product_info_id

                    if eform_check_flag:
                        if cart_item_guid:
                            eform_data_existence_flag, user_cart_item_detail = self.check_for_cart_update_or_create(
                                user_cart_item_dic_list,
                                item_details['eform_detail'])
                            if eform_data_existence_flag:
                                quantity = int(user_cart_item_detail['quantity']) + int(quantity)
                    price, item_price, validation_error, base_price, discount_percentage, additional_price = validate_price(
                        item_details['item_total_value'],
                        item_details['eform_detail'], quantity,
                        get_prd_ref.discount_id)
                    if not validation_error:
                        catalog_content['price'] = price
                        actual_price, discount_value, tax_value, gross_price = get_price_discount_tax(price,
                                                                                                      base_price,
                                                                                                      additional_price,
                                                                                                      tax,
                                                                                                      discount_percentage,
                                                                                                      quantity)
                        catalog_content['actual_price'] = actual_price
                        catalog_content['discount_value'] = discount_value
                        catalog_content['tax_value'] = tax_value
                        catalog_content['gross_price'] = gross_price
                        catalog_content['discount_percentage'] = discount_percentage
                        catalog_content['base_price'] = base_price
                        catalog_content['additional_price'] = additional_price

                    # update cart item table with quantity and price
                    if eform_data_existence_flag:
                        actual_price, discount_value, tax_value, gross_price = get_price_discount_tax(price,
                                                                                                      base_price,
                                                                                                      additional_price,
                                                                                                      tax,
                                                                                                      discount_percentage,
                                                                                                      quantity)

                        catalog_content = {'quantity': quantity,
                                           'price': price,
                                           'discount_percentage': discount_percentage,
                                           'discount_value': discount_value,
                                           'gross_price': gross_price}
                        self.add_or_update_item(user_cart_item_detail['guid'], catalog_content)
                    else:
                        print(cart_item_guid)
                        catalog_content['guid'] = cart_item_guid
                        queue_query = Q()
                        queue_query = ~Q(
                            dropdown_pricetype__in=[CONST_VARIANT_BASE_PRICING, CONST_VARIANT_ADDITIONAL_PRICING])
                        if django_query_instance.django_queue_existence_check(VariantConfig,
                                                                              {'client': global_variables.GLOBAL_CLIENT,
                                                                               'del_ind': False,
                                                                               'variant_id': get_prd_ref.variant_id},
                                                                              queue_query):
                            # catalog_content['price'] = check_discount_update_base_price(catalog_content['price'], quantity,
                            #                                                              get_prd_ref.variant_id)
                            catalog_content['value'] = calculate_item_total_value(CONST_CATALOG_CALLOFF, quantity,
                                                                                  quantity, 1,
                                                                                  catalog_content['price'],
                                                                                  overall_limit=None)
                            if catalog_content['currency'] != global_variables.GLOBAL_USER_CURRENCY:
                                catalog_content['value'] = convert_currency(catalog_content['value'],
                                                                            str(catalog_content['currency']),
                                                                            str(global_variables.GLOBAL_USER_CURRENCY))
                        self.add_or_update_item(user_cart_item_guid, catalog_content)

                    if not eform_data_existence_flag:
                        update_product_detail_eform(item_details, cart_item_guid, None)
                    if not user_cart_item_guid:
                        print("unused")
                        catalog_content['guid'] = cart_item_guid
                        catalog_content['client'] = global_variables.GLOBAL_CLIENT
                        self.add_or_update_item(cart_item_guid, catalog_content)
                elif not eform_check_flag:
                    print("without eform")
                    catalog_content['guid'] = guid_generator()
                    self.add_or_update_item(cart_item_guid, catalog_content)
                cart_count = display_cart_counter(global_variables.GLOBAL_LOGIN_USERNAME)
                error_msg = get_message_desc(MSG016)[1]
                # msgid = 'MSG016'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg
                return True, error_msg, cart_count
                # return True, MSG016, cart_count
        else:
            cart_count = display_cart_counter(global_variables.GLOBAL_LOGIN_USERNAME)
            msgid = 'MSG199'
            error_msg = get_message_desc(msgid)[0]
            return False, error_msg, cart_count

    def check_if_exist_update_sc_item(self, product_id, header_guid, eform_detail, ui_quantity):
        """"
        """
        existence_flag = False
        cart_item_detail = {}
        quantity = 1
        # get scitem list for added item
        if django_query_instance.django_existence_check(ScItem,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'header_guid': header_guid, 'int_product_id': product_id}):
            item_details = django_query_instance.django_filter_query(ScItem,
                                                                     {'client': global_variables.GLOBAL_CLIENT,
                                                                      'header_guid': header_guid,
                                                                      'int_product_id': product_id}, None, None)

            existence_flag, cart_item_detail = self.check_catalog_item_exists(item_details, eform_detail)
            # if eform data for login user exist then increment the quantity in cart detail table
            if existence_flag:
                updated = exists_update_sc_item(header_guid, cart_item_detail, ui_quantity)

        return existence_flag, cart_item_detail, quantity

    def check_catalog_item_exists(self, user_cart_item_dic_list, eform_detail):
        eform_data_existence_flag = True
        user_cart_item_detail = []
        cart_item_detail = None
        for user_cart_item in user_cart_item_dic_list:
            eform_data_existence_flag = True
            queue_query = Q()
            queue_query = Q(item_guid=user_cart_item['guid']) | Q(cart_guid=user_cart_item['guid'])
            if django_query_instance.django_queue_existence_check(EformFieldData,
                                                                  {'client': global_variables.GLOBAL_CLIENT},
                                                                  queue_query):
                # check if already eform data exist by cart guid
                for eform_data in eform_detail:
                    if django_query_instance.django_existence_check(ProductEformPricing,
                                                                    {'product_eform_pricing_guid': eform_data[
                                                                        'product_eform_pricing_guid'],
                                                                     'client': global_variables.GLOBAL_CLIENT}):
                        eform_field_name, eform_field_data = self.get_eform_field_data(eform_data)
                        if not django_query_instance.django_existence_check(EformFieldData,
                                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                                             'item_guid': user_cart_item['guid'],
                                                                             'eform_field_name': eform_field_name,
                                                                             'eform_field_data': eform_field_data}):
                            eform_data_existence_flag = False
                if eform_data_existence_flag:
                    user_cart_item_detail.append(user_cart_item)

        if len(user_cart_item_detail) == 1:
            cart_item_detail = user_cart_item_detail[0]
            eform_data_existence_flag = True

        return eform_data_existence_flag, cart_item_detail


def update_product_detail_eform(item_details, cart_guid, item_guid):
    """
    """
    dictionary_list = []
    product_eform_pricing_guid = None
    item_guid_obj = None
    if item_guid:
        item_guid_obj = django_query_instance.django_get_query(ScItem,
                                                               {'guid': item_guid,
                                                                'client': global_variables.GLOBAL_CLIENT})
    for item_detail in item_details['eform_detail']:
        if item_detail['pricing_type'] != CONST_VARIANT_WITHOUT_PRICING:
            # product_eform_pricing_guid = get_pricing_guid(item_detail['eform_field_config_guid'],
            #                                               item_detail['eform_field_data'])
            product_eform_pricing_guid = item_detail['product_eform_pricing_guid']
        eform_detail = django_query_instance.django_filter_query(VariantConfig,
                                                                 {'variant_config_guid': item_detail[
                                                                     'variant_config_guid']},
                                                                 None, None)[0]
        if item_detail['pricing_type'] != CONST_VARIANT_WITHOUT_PRICING:
            eform_field_data = django_query_instance.django_filter_value_list_query(ProductEformPricing,
                                                                                    {
                                                                                        'client': global_variables.GLOBAL_CLIENT,
                                                                                        'product_eform_pricing_guid':
                                                                                            item_detail[
                                                                                                'product_eform_pricing_guid']},
                                                                                    'pricing_data')[0]
        else:
            eform_field_data = item_detail['data']
        eform_dictionary = {'eform_field_data_guid': guid_generator(),
                            'eform_id': item_details['eform_id'],
                            'cart_guid': cart_guid,
                            'item_guid': item_guid_obj,
                            'product_eform_pricing_guid': django_query_instance.django_get_query(ProductEformPricing,
                                                                                                 {
                                                                                                     'product_eform_pricing_guid': product_eform_pricing_guid}),
                            'eform_type': CONST_CATALOG_ITEM_VARIANT,
                            'eform_field_count': int(eform_detail['variant_count']),
                            'eform_field_name': eform_detail['variant_name'],
                            'client': global_variables.GLOBAL_CLIENT,
                            'eform_field_data': eform_field_data}
        dictionary_list.append(eform_dictionary)
    bulk_create_entry_db(EformFieldData, dictionary_list)


def get_pricing_guid(eform_field_config_guid, pricing_data):
    """
    """
    product_eform_pricing_guid = None
    if django_query_instance.django_existence_check(ProductEformPricing,
                                                    {'eform_field_config_guid': eform_field_config_guid,
                                                     'pricing_data': pricing_data,
                                                     'client': global_variables.GLOBAL_CLIENT,
                                                     'del_ind': False}):
        product_eform_pricing_guid = django_query_instance.django_filter_value_list_ordered_by_distinct_query(
            ProductEformPricing,
            {'eform_field_config_guid': eform_field_config_guid,
             'pricing_data': pricing_data,
             'client': global_variables.GLOBAL_CLIENT,
             'del_ind': False},
            'product_eform_pricing_guid', None)[0]
    return product_eform_pricing_guid


def get_cart_item_max_num():
    """

    """
    if django_query_instance.django_existence_check(CartItemDetails,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'username': global_variables.GLOBAL_LOGIN_USERNAME}
                                                    ):
        max_item_num = django_query_instance.django_max_filter(CartItemDetails,
                                                               {'client': global_variables.GLOBAL_CLIENT,
                                                                'username': global_variables.GLOBAL_LOGIN_USERNAME},
                                                               'item_num')
        max_item_num = int(max_item_num) + 1
    else:
        max_item_num = 1
    return max_item_num


def get_sc_item_max_num(header_guid):
    """

    """
    if django_query_instance.django_existence_check(ScItem,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'header_guid': header_guid}
                                                    ):
        max_item_num = django_query_instance.django_max_filter(ScItem,
                                                               {'client': global_variables.GLOBAL_CLIENT,
                                                                'header_guid': header_guid}, 'item_num')
        max_item_num = int(max_item_num) + 1
    else:
        max_item_num = 1
    return max_item_num


def update_supplier_detail(catalog_content, supplier_id):
    """

    """
    if django_query_instance.django_existence_check(SupplierMaster,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'supplier_id': supplier_id}):
        supplier_detail = django_query_instance.django_get_query(SupplierMaster,
                                                                 {'client': global_variables.GLOBAL_CLIENT,
                                                                  'supplier_id': supplier_id})
        catalog_content['supplier_mobile_num'] = supplier_detail.mobile_num
        catalog_content['supplier_username'] = supplier_detail.supplier_username
        catalog_content['supplier_fax_no'] = supplier_detail.fax
        catalog_content['supplier_email'] = supplier_detail.email
    return catalog_content
