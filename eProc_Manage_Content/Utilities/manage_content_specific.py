import datetime
import os
import shutil
from decimal import Decimal

from django.db.models import Q
from django.http import HttpResponseRedirect

from Majjaka_eProcure import settings
from eProc_Basic.Utilities.constants.constants import CONST_PRODUCT_SPECIFICATION, CONST_CATALOG_CALLOFF, \
    CONST_FREETEXT_CALLOFF, \
    CONST_SEARCH_COUNT, CONST_VARIANT_WITHOUT_PRICING, CONST_CATALOG_ITEM_VARIANT, CONST_DROPDOWN_DATA_TYPE, \
    CONST_QUANTITY_BASED_DISCOUNT, CONST_VARIANT_BASE_PRICING, CONST_VARIANT_ADDITIONAL_PRICING, CONST_OPERATOR_PLUS, \
    CONST_OPERATOR_PERCENTAGE, CONST_CATALOG_IMAGE_TYPE
from eProc_Basic.Utilities.functions.append_delimiter import append_delimiter
from eProc_Basic.Utilities.functions.dictionary_check_value_based_for_key import dictionary_check_value_based_for_key
from eProc_Basic.Utilities.functions.dictionary_key_to_list import dictionary_key_to_list
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries, bulk_create_entry_db
from eProc_Basic.Utilities.functions.encryption_util import encrypt
from eProc_Basic.Utilities.functions.guid_generator import guid_generator, random_int
from eProc_Basic.Utilities.functions.type_casting import integer_type_caste, decimal_type_caste
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import EformFieldConfig, ProductEformPricing, ProductInfo, ProductsDetail, Catalogs, \
    OrgClients, CatalogMapping, FreeTextDetails, ImagesUpload, VariantConfig, DiscountData
from eProc_Content_Search.Utilities.content_search_generic import get_product_detail_filter_list
from eProc_Shopping_Cart.models import CartItemDetails, ScItem

django_query_instance = DjangoQueries()


# def save_product_details_eform(eform_configured, product_id,create_flag,edit_variant_flag):
#     """
#
#     """
#     form_id = None
#     eform_id = None
#     eform_field_config_guid_list = []
#     eform_id = None
#     if eform_configured:
#         if ProductsDetail.objects.filter(Q(product_id=product_id) & Q(client=global_variables.GLOBAL_CLIENT) &
#                                          ~Q(eform_id=None)).exists():
#             eform_id = django_query_instance.django_filter_value_list_ordered_by_distinct_query(ProductsDetail,
#                                                                                                 {
#                                                                                                     'product_id': product_id,
#                                                                                                     'client': global_variables.GLOBAL_CLIENT},
#                                                                                                 'eform_id', None)[0]
#             django_query_instance.django_filter_delete_query(ProductEformPricing,
#                                                              {'eform_id': eform_id,
#                                                               'client': global_variables.GLOBAL_CLIENT,
#                                                               'del_ind': False})
#             django_query_instance.django_filter_delete_query(EformFieldConfig,
#                                                              {'eform_id': eform_id,
#                                                               'client': global_variables.GLOBAL_CLIENT,
#                                                               'del_ind': False})
#         eform_configured_list, form_id, pricing_list = product_eform_price_query_dictionary_list(eform_configured,
#                                                                                                  eform_id)
#         print(form_id)
#         create_status = bulk_create_entry_db(EformFieldConfig, eform_configured_list)
#         for pricing in pricing_list:
#             pricing['eform_field_config_guid'] = DjangoQueries().django_get_query(EformFieldConfig,
#                                                                                   {'eform_field_config_guid': pricing[
#                                                                                       'eform_field_config_guid']})
#         create_status = bulk_create_entry_db(ProductEformPricing, pricing_list)
#     return form_id


def save_product_details_eform(eform_configured):
    """

    """
    form_id = None
    eform_id = None
    if eform_configured:
        eform_configured_list, form_id, pricing_list = product_eform_price_query_dictionary_list(eform_configured,
                                                                                                 eform_id)
        print(form_id)
        create_status = bulk_create_entry_db(VariantConfig, eform_configured_list)
        for pricing in pricing_list:
            pricing['variant_config_guid'] = DjangoQueries().django_get_query(VariantConfig,
                                                                              {'variant_config_guid': pricing[
                                                                                  'variant_config_guid']})
        create_status = bulk_create_entry_db(ProductEformPricing, pricing_list)
    return form_id


def save_discount_data(discount_dic_list):
    """

    """
    form_id = None
    eform_id = None
    discount_price = []
    discount_id = None
    if discount_dic_list:

        discount_id = random_int(8)
        for discount_dic in discount_dic_list:
            for discount in discount_dic['variant_data']:
                discount_list = {'discount_data_guid': guid_generator(),
                                 'discount_id': discount_id,
                                 'discount_name': discount_dic['field_name'],
                                 'quantity': discount['discount_min_quantity'],
                                 'discount_percentage': discount['discount_percentage_value'],
                                 'client': global_variables.GLOBAL_CLIENT}
                discount_price.append(discount_list)
        create_status = bulk_create_entry_db(DiscountData, discount_price)
    return discount_id


def save_product_specification(product_specification_data, product_id):
    """

    """

    product_info_id = random_int(8)
    for product_specification in product_specification_data:
        product_specification['product_info_guid'] = guid_generator()
        product_specification['product_info_id'] = product_info_id
        product_specification['product_id'] = product_id
        product_specification['product_info_type'] = CONST_PRODUCT_SPECIFICATION
        product_specification['product_info_created_at'] = datetime.date.today()
        product_specification['product_info_created_by'] = global_variables.GLOBAL_LOGIN_USERNAME
        product_specification['client'] = global_variables.GLOBAL_CLIENT
    create_status = bulk_create_entry_db(ProductInfo, product_specification_data)
    return product_info_id


def get_catalog_filter_list(filter, query_count):
    """

    """
    catalog_details = django_query_instance.django_filter_query_with_entry_count(Catalogs, filter, ['catalog_id'], None,
                                                                                 int(query_count))

    return catalog_details


def save_catalog_to_db(catalog_data):
    """

    """
    catalog_id = []
    catalog_data_response = []
    if catalog_data['catalog_action'] == 'UPDATE':
        for data in catalog_data['catalog_data']:
            django_query_instance.django_update_query(Catalogs,
                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                       'catalog_id': data['catalog_id']},
                                                      {'name': data['name'],
                                                       'description': data['description'],
                                                       'prod_type': data['product_type']})
            catalog_id.append(data['catalog_id'])
        catalog_data_response = django_query_instance.django_filter_query(Catalogs,
                                                                          {'client': global_variables.GLOBAL_CLIENT,
                                                                           'catalog_id__in': catalog_id},
                                                                          None,
                                                                          None)
    else:
        for data in catalog_data['catalog_data']:
            catalog_dictionary = {'catalog_guid': guid_generator(),
                                  'client': global_variables.GLOBAL_CLIENT,
                                  'catalog_id': data['catalog_id'],
                                  'name': data['name'],
                                  'description': data['description'],
                                  'prod_type': data['product_type']}
            django_query_instance.django_create_query(Catalogs, catalog_dictionary)

    return catalog_data_response


class CatalogMappingAction:
    def __init__(self, catalog_id):
        self.catalog_id = catalog_id

    def get_assigned_unssigned_product_id_list(self, assign_unassign_data):
        """

        """
        filter_queue = Q()
        product_id_detail_list = []
        freetext_id_detail_list = []
        if assign_unassign_data['action'] == "ASSIGN":
            product_id_detail_list = self.get_unassigned_catalog_item_list()
            freetext_id_detail_list = self.get_unassigned_freetext_item_list()

        elif assign_unassign_data['action'] == "UNASSIGN" or "VIEW":
            product_id_detail_list = self.get_assigned_catalog_item_list()
            freetext_id_detail_list = self.get_assigned_freetext_item_list()

        return product_id_detail_list, freetext_id_detail_list

    def get_unassigned_catalog_item_list(self):
        """
        """
        assign_product_id_list = django_query_instance.django_filter_value_list_ordered_by_distinct_query(
            CatalogMapping,
            {'catalog_id': self.catalog_id,
             'client': global_variables.GLOBAL_CLIENT,
             'del_ind': False,
             'call_off': CONST_CATALOG_CALLOFF},
            'item_id', None)
        filter_queue = ~Q(product_id__in=assign_product_id_list)
        product_id_detail_list = django_query_instance.django_queue_query(ProductsDetail,
                                                                          {'client': global_variables.GLOBAL_CLIENT,
                                                                           'del_ind': False}, filter_queue, None, None)
        return product_id_detail_list

    def get_unassigned_freetext_item_list(self):
        """
        """
        assign_product_id_list = django_query_instance.django_filter_value_list_ordered_by_distinct_query(
            CatalogMapping,
            {'catalog_id': self.catalog_id,
             'client': global_variables.GLOBAL_CLIENT,
             'del_ind': False,
             'call_off': CONST_FREETEXT_CALLOFF},
            'item_id', None)
        filter_queue = ~Q(freetext_id__in=assign_product_id_list)
        freetext_id_detail_list = django_query_instance.django_queue_query(FreeTextDetails,
                                                                           {'client': global_variables.GLOBAL_CLIENT,
                                                                            'del_ind': False}, filter_queue, None, None)
        return freetext_id_detail_list

    def get_assigned_catalog_item_list(self):
        """
        """
        unassign_product_id_list = django_query_instance.django_filter_value_list_ordered_by_distinct_query(
            CatalogMapping,
            {'catalog_id': self.catalog_id,
             'client': global_variables.GLOBAL_CLIENT,
             'del_ind': False,
             'call_off': CONST_CATALOG_CALLOFF},
            'item_id',
            ['item_id'])
        product_id_detail_list = django_query_instance.django_filter_query(ProductsDetail,
                                                                           {'client': global_variables.GLOBAL_CLIENT,
                                                                            'del_ind': False,
                                                                            'product_id__in': unassign_product_id_list},
                                                                           None, None)
        return product_id_detail_list

    def get_assigned_freetext_item_list(self):
        """
        """
        unassign_freetext_id_list = django_query_instance.django_filter_value_list_ordered_by_distinct_query(
            CatalogMapping,
            {'catalog_id': self.catalog_id,
             'client': global_variables.GLOBAL_CLIENT,
             'del_ind': False,
             'call_off': CONST_FREETEXT_CALLOFF},
            'item_id',
            ['item_id'])
        freetext_id_detail_list = django_query_instance.django_filter_query(FreeTextDetails,
                                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                                             'del_ind': False,
                                                                             'freetext_id__in': unassign_freetext_id_list},
                                                                            None, None)
        return freetext_id_detail_list

    def save_catalog_mapping(self, catalog_mapping_info):
        """

        """
        create_list = []
        if catalog_mapping_info['action'] == "ASSIGN":
            self.assign_catalog_item_to_catalog_mapping(catalog_mapping_info['product_id_list'], CONST_CATALOG_CALLOFF)
            self.assign_catalog_item_to_catalog_mapping(catalog_mapping_info['freetext_id_list'],
                                                        CONST_FREETEXT_CALLOFF)

        elif catalog_mapping_info['action'] == "UNASSIGN":
            item_list = catalog_mapping_info['product_id_list'] + catalog_mapping_info['freetext_id_list']
            django_query_instance.django_filter_delete_query(CatalogMapping,
                                                             {'client': global_variables.GLOBAL_CLIENT,
                                                              'item_id__in': item_list,
                                                              })

    def assign_catalog_item_to_catalog_mapping(self, item_list, call_off):
        """

        """
        create_list = []
        for item in item_list:
            create_dictionary = {'catalog_mapping_guid': guid_generator(),
                                 'catalog_id': self.catalog_id,
                                 'item_id': item,
                                 'call_off': call_off,
                                 'catalogs_mapping_source_system': 'ERP1',
                                 'client': global_variables.GLOBAL_CLIENT}
            create_list.append(create_dictionary)
        bulk_create_entry_db(CatalogMapping, create_list)


def get_assigned_unssigned_product_id_list():
    return None


def save_catalog_mapping():
    return None


def get_product_detail_config():
    """

    :return:
    """
    product_details_query = get_product_detail_filter_list({'client': global_variables.GLOBAL_CLIENT, 'del_ind': False},
                                                           CONST_SEARCH_COUNT)
    product_details_query = update_prod_detail(product_details_query)
    return product_details_query


def update_prod_detail(product_details_query):
    """

    :param product_details_query:
    :return:
    """
    for product_detail in product_details_query:
        product_detail['product_transaction'] = False
        if django_query_instance.django_existence_check(CartItemDetails,
                                                        {'int_product_id': product_detail['product_id'],
                                                         'call_off': CONST_CATALOG_CALLOFF,
                                                         'client': global_variables.GLOBAL_CLIENT}
                                                        ) or django_query_instance.django_existence_check(ScItem,
                                                                                                          {
                                                                                                              'int_product_id':
                                                                                                                  product_detail[
                                                                                                                      'product_id'],
                                                                                                              'call_off': CONST_CATALOG_CALLOFF,
                                                                                                              'client': global_variables.GLOBAL_CLIENT}
                                                                                                          ):
            if django_query_instance.django_existence_check(CatalogMapping,
                                                            {'item_id': product_detail['product_id'],
                                                             'call_off': CONST_CATALOG_CALLOFF,
                                                             'client': global_variables.GLOBAL_CLIENT}):
                product_detail['product_transaction'] = True
        product_detail['encrypted_product_id'] = encrypt(product_detail['product_id'])

    return product_details_query


def product_eform_price_query_dictionary_list(eform_configured, eform_id):
    """

    """
    if not eform_id:
        eform_id = random_int(8)
    eform_field_count = 0
    eform_field_list = []
    eform_pricing_list = []
    for eform_data in eform_configured:
        eform_field_data = ''
        price_flag = True
        eform_guid = guid_generator()
        eform_field_count = eform_field_count + 1
        if eform_data['field_type'] == CONST_VARIANT_WITHOUT_PRICING:
            price_flag = False
        eform_field_dictionary = {'pk': eform_guid,
                                  'dropdown_pricetype': eform_data['field_type'],
                                  'variant_name': eform_data['field_name'],
                                  'variant_datatype': CONST_DROPDOWN_DATA_TYPE,
                                  'variant_id': eform_id,
                                  'variant_count': eform_field_count,
                                  'variant_flag': price_flag,
                                  'client': global_variables.GLOBAL_CLIENT}
        # pricing will not have impact on VARIANT_WITHOUT_PRICING

        for variant_data in eform_data['variant_data']:
            if eform_data['field_type'] != CONST_VARIANT_WITHOUT_PRICING:
                if eform_data['field_type'] != CONST_QUANTITY_BASED_DISCOUNT:
                    if variant_data['default_option']:
                        eform_field_dictionary['default_variant_data'] = variant_data['option_value']
                    # eform_field_data = eform_field_data + variant_data['option_value'] + '|~#'
                    eform_field_data = append_delimiter(eform_field_data, variant_data['option_value'], '|~#')
                    pricing_data = variant_data['option_value']
                    pricing_data_default = variant_data['default_option']
                    price = variant_data['option_price']
                else:
                    # eform_field_data = eform_field_data + variant_data['discount_min_quantity'] + '|~#'
                    eform_field_data = append_delimiter(eform_field_data, variant_data['discount_min_quantity'], '|~#')
                    pricing_data = variant_data['discount_min_quantity']
                    pricing_data_default = False
                    price = variant_data['discount_percentage_value']
                if eform_data['field_type'] != CONST_VARIANT_WITHOUT_PRICING:
                    eform_pricing_dictionary = {'product_eform_pricing_guid': guid_generator(),
                                                'pricing_type': eform_data['field_type'],
                                                'pricing_data': pricing_data,
                                                'pricing_data_default': pricing_data_default,
                                                'price': price,
                                                'eform_id': eform_id,
                                                'variant_config_guid': eform_guid,
                                                'client': global_variables.GLOBAL_CLIENT}
                    if eform_data['field_type'] == CONST_VARIANT_BASE_PRICING:
                        eform_pricing_dictionary['product_description'] = variant_data['option_description']
                    if eform_data['field_type'] == CONST_VARIANT_ADDITIONAL_PRICING:
                        eform_pricing_dictionary['operator'] = CONST_OPERATOR_PLUS
                    if eform_data['field_type'] == CONST_QUANTITY_BASED_DISCOUNT:
                        eform_pricing_dictionary['operator'] = CONST_OPERATOR_PERCENTAGE
                    eform_pricing_list.append(eform_pricing_dictionary)
            else:
                # eform_field_data = eform_field_data + variant_data['option_value'] + '|~#'
                eform_field_data = append_delimiter(eform_field_data, variant_data['option_value'], '|~#')
        print(eform_field_data)
        eform_field_dictionary['variant_data'] = eform_field_data
        eform_field_list.append(eform_field_dictionary)
    return eform_field_list, eform_id, eform_pricing_list


def save_product_detail_images(path, product_id):
    """

    """
    source_folder = path
    destination_folder = str(settings.BASE_DIR) + f'/media/catalog/{global_variables.GLOBAL_CLIENT}/{product_id}'
    image_url_path = f'/catalog/{global_variables.GLOBAL_CLIENT}/{product_id}'
    # delete existing images
    if django_query_instance.django_existence_check(ImagesUpload,
                                                    {'image_id': product_id,
                                                     'image_type': CONST_CATALOG_IMAGE_TYPE,
                                                     'client': global_variables.GLOBAL_CLIENT}):
        shutil.rmtree(destination_folder)
        django_query_instance.django_filter_delete_query(ImagesUpload,
                                                         {'image_id': product_id,
                                                          'image_type': CONST_CATALOG_IMAGE_TYPE,
                                                          'client': global_variables.GLOBAL_CLIENT})

    # fetch all files
    image_count = 0
    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)
    for file_name in os.listdir(source_folder):
        image_url_path = f'/catalog/{global_variables.GLOBAL_CLIENT}/{product_id}'
        # construct full file path
        source = os.path.join(source_folder, file_name)
        destination = os.path.join(destination_folder, file_name)
        image_url_path = os.path.join(image_url_path, file_name)
        # copy only files
        if os.path.isfile(source):
            shutil.copy(source, destination)
            print('copied', file_name)

        django_query_instance.django_create_query(ImagesUpload, {
            'images_upload_guid': guid_generator(),
            'client': global_variables.GLOBAL_CLIENT,
            'image_id': product_id,
            'image_url': image_url_path,
            'image_number': image_count,
            'image_name': file_name,
            'image_default': 0,
            'image_type': CONST_CATALOG_IMAGE_TYPE,
            'created_at': datetime.datetime.now(),
            'created_by': global_variables.GLOBAL_LOGIN_USERNAME,
            'del_ind': False
        })
        image_count = image_count + 1


def update_boolean(val):
    """

    """
    for key, value in val.items():
        if value == 'TRUE':
            val[key] = 1
        elif value == 'FALSE':
            val[key] = 0
    return val


def value_type_caste(val):
    """

    """
    val['lead_time'] = integer_type_caste(val['lead_time'])
    val['quantity_avail'] = integer_type_caste(val['quantity_avail'])
    val['quantity_min'] = integer_type_caste(val['quantity_min'])
    val['value_min'] = integer_type_caste(val['value_min'])
    val['quantity_max'] = integer_type_caste(val['quantity_max'])
    val['quantity_1'] = integer_type_caste(val['quantity_1'])
    val['quantity_2'] = integer_type_caste(val['quantity_2'])
    val['quantity_3'] = integer_type_caste(val['quantity_3'])
    val['quantity_max'] = integer_type_caste(val['quantity_max'])
    val['price'] = decimal_type_caste(val['price'])
    val['sgst'] = decimal_type_caste(val['sgst'])
    val['cgst'] = decimal_type_caste(val['cgst'])
    val['vat'] = decimal_type_caste(val['vat'])
    val['price_1'] = decimal_type_caste(val['price_1'])
    val['price_2'] = decimal_type_caste(val['price_2'])
    val['price_3'] = decimal_type_caste(val['price_3'])
    return val


def save_products_specifications(product_specification_data):
    """

    """
    prod_id_list = []
    for prod_spec in product_specification_data:
        prod_id_list.append(prod_spec[0])
    prod_id_list = list(set(prod_id_list))
    product_spec_list = []
    for prod_id in prod_id_list:
        product_spec_list.append({'product_id': prod_id, 'product_info_id': random_int(8)})
    product_info_id = None
    # create product specification
    product_specifications_list = []
    product_info_id = random_int(8)
    for product_specification in product_specification_data:
        product_specifications = {}
        # product_info_id = get_product_info_id(product_spec_list,product_specification[0])
        product_specifications['product_info_guid'] = guid_generator()
        product_specifications['product_id'] = product_specification[0]
        product_specifications['product_info_id'] = product_info_id
        product_specifications['product_info_key'] = product_specification[1]
        product_specifications['product_info_value'] = product_specification[2]
        product_specifications['product_info_type'] = CONST_PRODUCT_SPECIFICATION
        product_specifications['product_info_created_at'] = datetime.date.today()
        product_specifications['product_info_created_by'] = global_variables.GLOBAL_LOGIN_USERNAME
        product_specifications['client'] = global_variables.GLOBAL_CLIENT
        product_specifications_list.append(product_specifications)
    create_status = bulk_create_entry_db(ProductInfo, product_specifications_list)
    return product_info_id


def get_product_info_id(product_spec_list,product_id):
    """

    """
    product_info_id = [product_spec['product_info_id'] for product_spec in product_spec_list if product_spec['product_id'] == product_id]
    if product_info_id:
        product_info_id = product_info_id[0]
    else:
        product_info_id = None
    return  product_info_id

