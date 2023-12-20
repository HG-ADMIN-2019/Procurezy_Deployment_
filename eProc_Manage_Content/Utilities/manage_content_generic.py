from eProc_Basic.Utilities.constants.constants import CONST_CATALOG_IMAGE_TYPE, CONST_CATALOG_ITEM_VARIANT, \
    CONST_VARIANT_ADDITIONAL_PRICING, CONST_QUANTITY_BASED_DISCOUNT, CONST_VARIANT_BASE_PRICING, \
    CONST_VARIANT_WITHOUT_PRICING, CONST_CATALOG_CALLOFF
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import ImagesUpload, ProductsDetail, EformFieldConfig, ProductEformPricing, ProductInfo, \
    CatalogMapping, VariantConfig, DiscountData
from eProc_Form_Builder.models import EformFieldData

django_query_instance = DjangoQueries()


def get_product_details_image_eform(product_id):
    prod_img_detail = []
    product_details = []
    product_eform_data = []
    product_specification = []
    eform_edit_flag = 0
    if DjangoQueries().django_existence_check(ProductsDetail, {'product_id': product_id,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'del_ind': False}):
        product_details = DjangoQueries().django_get_query(ProductsDetail,
                                                           {'product_id': product_id,
                                                            'client': global_variables.GLOBAL_CLIENT,
                                                            'del_ind': False})
        prod_img_detail = DjangoQueries().django_filter_query(ImagesUpload,
                                                              {'client': global_variables.GLOBAL_CLIENT,
                                                               'image_id': str(product_id),
                                                               'image_type': CONST_CATALOG_IMAGE_TYPE},
                                                              ['image_number'],
                                                              None)
        product_eform_data, eform_edit_flag = get_eform_details(product_details.variant_id)
        discount_data = get_discount_data(product_details.discount_id)
        if discount_data:
            product_eform_data.append(discount_data)
        product_specification = get_product_specification(product_details.product_info_id)

    return product_details, prod_img_detail, product_eform_data, product_specification, eform_edit_flag


def get_eform_details(variant_id):
    """

    """
    eform_data = []
    eform_edit_flag = 0
    product_eform_data = DjangoQueries().django_filter_query(VariantConfig,
                                                             {'client': global_variables.GLOBAL_CLIENT,
                                                              'variant_id': variant_id},
                                                             None,
                                                             ['variant_id', 'variant_count', 'variant_name',
                                                              'required_flag', 'variant_datatype',
                                                              'default_variant_data',
                                                              'specialchar_flag',
                                                              'variant_data', 'display_flag',
                                                              'variant_config_guid', 'variant_flag',
                                                              'dropdown_pricetype'])
    for product_eform in product_eform_data:
        eform_dictionary = {'field_name': product_eform['variant_name'],
                            'field_type': product_eform['dropdown_pricetype']}
        if product_eform['dropdown_pricetype'] == CONST_VARIANT_WITHOUT_PRICING:
            eform_field_data = product_eform['variant_data'].split('|~#')
            eform_pricing_list = []
            for eform_field_list in eform_field_data:
                eform_pricing_dictionary = {'default_option': False, 'option_value': eform_field_list}
                eform_pricing_list.append(eform_pricing_dictionary)
            eform_dictionary['variant_data'] = eform_pricing_list
        if product_eform['dropdown_pricetype'] == CONST_VARIANT_BASE_PRICING or \
                CONST_VARIANT_ADDITIONAL_PRICING or CONST_QUANTITY_BASED_DISCOUNT:
            eform_price = django_query_instance.django_filter_query(ProductEformPricing,
                                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                                     'del_ind': False,
                                                                     'variant_config_guid':
                                                                         product_eform['variant_config_guid']},
                                                                    None, None)
            eform_pricing_list = []
            for eform_pricing in eform_price:
                if product_eform['dropdown_pricetype'] != CONST_QUANTITY_BASED_DISCOUNT:
                    eform_pricing_dictionary = {'default_option': eform_pricing['pricing_data_default'],
                                                'option_value': eform_pricing['pricing_data'],
                                                'option_price': eform_pricing['price'],
                                                'option_description': eform_pricing['product_description']}
                else:
                    eform_pricing_dictionary = {'discount_min_quantity': eform_pricing['pricing_data'],
                                                'discount_percentage_value': eform_pricing['price']}
                eform_pricing_list.append(eform_pricing_dictionary)
            if product_eform['dropdown_pricetype'] != CONST_VARIANT_WITHOUT_PRICING:
                eform_dictionary['variant_data'] = eform_pricing_list
        eform_data.append(eform_dictionary)
    print(eform_data)
    eform_edit_flag = 0
    if django_query_instance.django_existence_check(EformFieldData,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'del_ind': False,
                                                     'eform_id': variant_id}):
        eform_edit_flag = 1

    return eform_data, eform_edit_flag


def get_discount_data(discount_id):
    """

    """
    discount_dictionary = {}
    variant_array = []
    if django_query_instance.django_existence_check(DiscountData,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'discount_id': discount_id}):
        discount_details = django_query_instance.django_filter_query(DiscountData,
                                                                     {'client': global_variables.GLOBAL_CLIENT,
                                                                      'discount_id': discount_id},
                                                                     None,
                                                                     None)
        discount_dictionary = {'field_name': discount_details[0]['discount_name'],
                               'field_type': CONST_QUANTITY_BASED_DISCOUNT}
        for discount_detail in discount_details:
            variant_array.append({'discount_min_quantity': discount_detail['quantity'],
                                  'discount_percentage_value': discount_detail['discount_percentage'],
                                  'discount_data_guid':discount_detail['discount_data_guid']
                                  })
        discount_dictionary['variant_data'] = variant_array
    return discount_dictionary


def product_eform_ui_dictionary_list(eform_id):
    """

    """
    eform_data = []
    product_eform_data = DjangoQueries().django_filter_query(EformFieldConfig,
                                                             {'client': global_variables.GLOBAL_CLIENT,
                                                              'eform_id': eform_id,
                                                              'eform_type': CONST_CATALOG_ITEM_VARIANT},
                                                             None,
                                                             ['eform_id', 'eform_field_count', 'eform_field_name',
                                                              'required_flag', 'eform_field_datatype',
                                                              'default_eform_field_data',
                                                              'specialchar_flag',
                                                              'eform_field_data', 'display_flag',
                                                              'eform_field_config_guid', 'price_flag',
                                                              'dropdown_pricetype'])
    for product_eform in product_eform_data:
        eform_dictionary = {'field_name': product_eform['eform_field_name'],
                            'field_type': product_eform['dropdown_pricetype']}
        if product_eform['dropdown_pricetype'] == CONST_VARIANT_WITHOUT_PRICING:
            eform_field_data = product_eform['eform_field_data'].split('|~#')
            eform_pricing_list = []
            for eform_field_list in eform_field_data:
                eform_pricing_dictionary = {'default_option': False, 'option_value': eform_field_list}
                eform_pricing_list.append(eform_pricing_dictionary)
            eform_dictionary['variant_data'] = eform_pricing_list
        if product_eform['dropdown_pricetype'] == CONST_VARIANT_BASE_PRICING or \
                CONST_VARIANT_ADDITIONAL_PRICING or CONST_QUANTITY_BASED_DISCOUNT:
            eform_price = django_query_instance.django_filter_query(ProductEformPricing,
                                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                                     'del_ind': False,
                                                                     'eform_field_config_guid':
                                                                         product_eform['eform_field_config_guid']},
                                                                    None, None)
            eform_pricing_list = []
            for eform_pricing in eform_price:
                if product_eform['dropdown_pricetype'] != CONST_QUANTITY_BASED_DISCOUNT:
                    eform_pricing_dictionary = {'default_option': eform_pricing['pricing_data_default'],
                                                'option_value': eform_pricing['pricing_data'],
                                                'option_price': eform_pricing['price'],
                                                'option_description': eform_pricing['product_description']}
                else:
                    eform_pricing_dictionary = {'discount_min_quantity': eform_pricing['pricing_data'],
                                                'discount_percentage_value': eform_pricing['price']}
                eform_pricing_list.append(eform_pricing_dictionary)
            if product_eform['dropdown_pricetype'] != CONST_VARIANT_WITHOUT_PRICING:
                eform_dictionary['variant_data'] = eform_pricing_list
        eform_data.append(eform_dictionary)
    print(eform_data)

    return eform_data


def get_product_specification(product_info_id):
    """

    """
    product_info_details = django_query_instance.django_filter_query(ProductInfo,
                                                                     {'product_info_id': product_info_id,
                                                                      'client': global_variables.GLOBAL_CLIENT},
                                                                     None,
                                                                     ['product_info_key', 'product_info_value'])
    return product_info_details


def get_catalog_mapping_product_id_list(catalog_id):
    """

    """
    product_id_list = django_query_instance.django_filter_value_list_ordered_by_distinct_query(CatalogMapping,
                                                                                               {
                                                                                                   'catalog_id__in': catalog_id,
                                                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                                                   'call_off': CONST_CATALOG_CALLOFF, },
                                                                                               'item_id',
                                                                                               None)
    return product_id_list
