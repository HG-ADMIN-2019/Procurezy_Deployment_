import datetime

from django.core.exceptions import ObjectDoesNotExist

from eProc_Basic.Utilities.functions.append_delimiter import append_delimiter
from eProc_Basic.Utilities.functions.dict_check_key import checkKey
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries, bulk_create_entry_db
import re
from django.db.models import Max
from eProc_Basic.Utilities.constants.constants import CONST_SF01, CONST_CATALOG_ITEM_VARIANT, \
    CONST_VARIANT_BASE_PRICING, \
    CONST_DROPDOWN_DATA_TYPE, CONST_VARIANT_WITHOUT_PRICING, CONST_VARIANT_BASE_PRICING, \
    CONST_VARIANT_ADDITIONAL_PRICING, CONST_QUANTITY_BASED_DISCOUNT, CONST_OPERATOR_PLUS, CONST_OPERATOR_PERCENTAGE, \
    CONST_FT_ITEM_EFORM, CONST_FREETEXT_CALLOFF, CONST_CATALOG_CALLOFF
from eProc_Basic.Utilities.functions.encryption_util import decrypt, encrypt
from eProc_Basic.Utilities.functions.guid_generator import random_int, guid_generator
from eProc_Basic.Utilities.functions.insert_remove import remove_dictionary_from_list, get_uncommon_elements_from_lists
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG131, MSG132
from eProc_Calendar_Settings.Utilities.calender_settings_generic import calculate_delivery_date, \
    calculate_delivery_date_base_on_lead_time
from eProc_Configuration.models import SupplierMaster, FreeTextForm, Currency, UnitOfMeasures, EformFieldConfig, \
    ProductEformPricing, ProductInfo, FreeTextDetails, CatalogMapping, ProductsDetail, VariantConfig
from eProc_Form_Builder.models import *
from eProc_Manage_Content.Utilities.manage_content_generic import get_discount_data
from eProc_Manage_Content.Utilities.manage_content_specific import get_product_detail_config
from eProc_Price_Calculator.Utilities.price_calculator_generic import get_product_price_from_eform
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import get_supp_name_by_id, get_prod_by_id
from eProc_Shopping_Cart.models import CartItemDetails, ScItem

django_query_instance = DjangoQueries()


# This class contains every operation related to form builder and freetext(except adding item to cart)
class FormBuilder:
    @staticmethod
    def save_freetext_form(data_dictionary):
        """

        """
        error_msg = ''
        eform_id = FormBuilder.freetext_eform_create(data_dictionary['eform_configured'], data_dictionary['eform_id'],
                                                     data_dictionary['type'])
        if django_query_instance.django_existence_check(FreeTextDetails,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'freetext_id': data_dictionary['freetext_id']}
                                                        ):
            django_query_instance.django_update_query(FreeTextDetails,
                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                       'freetext_id': data_dictionary['freetext_id']},
                                                      {'freetext_details_guid': guid_generator(),
                                                       'supplier_id': data_dictionary['supplier_id'],
                                                       'supp_product_id': data_dictionary['supplier_article_number'],
                                                       'lead_time': data_dictionary['lead_time'],
                                                       'currency_id': django_query_instance.django_get_query(Currency,
                                                                                                             {
                                                                                                                 'currency_id':
                                                                                                                     data_dictionary[
                                                                                                                         'currency_id']}),
                                                       'prod_cat_id': data_dictionary['product_category'],
                                                       'description': data_dictionary['supplier_description'],
                                                       'eform_id': eform_id,
                                                       'freetext_details_changed_at': datetime.datetime.now(),
                                                       'freetext_details_changed_by': global_variables.GLOBAL_LOGIN_USERNAME, })
        else:
            django_query_instance.django_create_query(FreeTextDetails,
                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                       'freetext_details_guid': guid_generator(),
                                                       'freetext_id': data_dictionary['freetext_id'],
                                                       'supplier_id': data_dictionary['supplier_id'],
                                                       'supp_product_id': data_dictionary['supplier_article_number'],
                                                       'lead_time': data_dictionary['lead_time'],
                                                       'prod_cat_id': data_dictionary['product_category'],
                                                       'description': data_dictionary['supplier_description'],
                                                       'eform_id': eform_id,
                                                       'currency_id': django_query_instance.django_get_query(Currency,
                                                                                                             {
                                                                                                                 'currency_id':
                                                                                                                     data_dictionary[
                                                                                                                         'currency_id']}),

                                                       'freetext_details_created_at': datetime.datetime.now(),
                                                       'freetext_details_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                       })
            msgid = 'MSG131'
            error_msg = get_message_desc(msgid)[1]

        return True, error_msg

    @staticmethod
    def freetext_eform_create(eform_configured, eform_id, action):
        """

        """
        eform_dictionary_list = []
        if eform_id:
            django_query_instance.django_filter_delete_query(EformFieldConfig,
                                                             {'client': global_variables.GLOBAL_CLIENT,
                                                              'eform_type': CONST_FT_ITEM_EFORM,
                                                              'eform_id': eform_id})
        else:
            eform_id = random_int(8)
        for count, eform_config in enumerate(eform_configured):

            eform_dictionary = {'eform_field_config_guid': guid_generator(),
                                'eform_id': eform_id,
                                'eform_type': CONST_FT_ITEM_EFORM,
                                'eform_field_count': count,
                                'eform_field_name': eform_config['field_name'],
                                'eform_field_datatype': eform_config['field_data_type'],
                                'required_flag': eform_config['required'],
                                'specialchar_flag': eform_config['allow_special_char'],
                                'client': global_variables.GLOBAL_CLIENT,
                                'del_ind': False
                                }
            if eform_config['field_data_type'] == 'dropdown':
                if eform_config['field_name'] not in ['Country', 'Currency']:
                    dropdown_options = None
                    eform_dictionary['eform_field_data'] = '|~#'.join(str(e) for e in eform_config['dropdown_options'])
            eform_dictionary_list.append(eform_dictionary)
        bulk_create_entry_db(EformFieldConfig, eform_dictionary_list)
        return eform_id

    # @staticmethod
    # def create_freetext_form(data_dictionary, client):
    #     """
    #     :param data_dictionary:
    #     :param client:
    #     :return:
    #     This method is used to create freetext form based on the user entered values
    #     """
    #     eform_configured = data_dictionary['eform_configured']
    #     supplier_id = data_dictionary['supplier_id']
    #     product_category = data_dictionary['product_category']
    #     form_id = data_dictionary['form_id']
    #     save_type = data_dictionary['type']
    #     if save_type == 'edit_mode':
    #         message = MSG131
    #
    #     else:
    #         message = MSG132
    #     if form_id == '':
    #         form_id = FormBuilder().generate_form_id(client)
    #         check_for_supplier = django_query_instance.django_existence_check(FreeTextForm, {
    #             'supp_id': supplier_id,
    #             'prod_cat_id': product_category,
    #             'client': client,
    #             'del_ind': False
    #         })
    #
    #         if check_for_supplier:
    #             return False, f'Freetext from with Supplier ID {supplier_id} and product category {product_category} ' \
    #                           f'already exists'
    #
    #     is_exists = FormBuilder().check_if_form_exists_in_eform(form_id, client)
    #     if is_exists:
    #         return False, f'You are not allowed to update the form: {form_id}'
    #
    #     converted_model_fields = FormBuilder().generate_model_based_keys(eform_configured)
    #     converted_model_fields['form_id'] = form_id
    #     converted_model_fields['supp_id'] = supplier_id
    #     converted_model_fields['description'] = data_dictionary['supplier_description']
    #     converted_model_fields['prod_cat_id'] = product_category
    #     converted_model_fields['supp_art_no'] = data_dictionary['supplier_article_number']
    #     converted_model_fields['lead_time'] = data_dictionary['lead_time']
    #     converted_model_fields['catalog_id'] = data_dictionary['catalog_id']
    #     converted_model_fields['client'] = client
    #     django_query_instance.django_filter_delete_query(FreeTextForm, {'form_id': form_id})
    #     django_query_instance.django_update_or_create_query(FreeTextForm, {'form_id': form_id}, converted_model_fields)
    #     return True, f'{message}: {form_id}'

    @staticmethod
    def get_freetext_form(freetext_id):
        """
        :param supplier_id:
        :param product_category_id:
        :param client:
        :return:
        This method is used to get freetext form based on supplier_id and product category Id
        """
        configured_freetext_form = {}
        eform_configured = []
        eform_flag = 0
        try:
            freetext_form = django_query_instance.django_filter_only_query(FreeTextDetails, {
                'freetext_id': freetext_id, 'del_ind': False, 'client': global_variables.GLOBAL_CLIENT
            }).values()[0]

            supplier_info = django_query_instance.django_get_query(SupplierMaster, {
                'supplier_id': freetext_form['supplier_id'], 'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
            })

            supplier_name = get_supp_name_by_id(global_variables.GLOBAL_CLIENT, freetext_form['supplier_id'])
            supplier_name = supplier_name.split('          ')
            first_name = supplier_name[0]
            last_name = supplier_name[1]
            configured_freetext_form['supplier_id'] = freetext_form['supplier_id']
            configured_freetext_form['supplier_name'] = get_supp_name_by_id(global_variables.GLOBAL_CLIENT,
                                                                            freetext_form['supplier_id'])
            configured_freetext_form['supplier_firstname'] = first_name
            configured_freetext_form['supplier_lastname'] = last_name
            configured_freetext_form['supplier_article_number'] = freetext_form['supp_product_id']
            configured_freetext_form['supplier_email'] = supplier_info.email
            configured_freetext_form['lead_time'] = freetext_form['lead_time']
            # configured_freetext_form['catalog_id'] = freetext_form['catalog_id']
            configured_freetext_form['product_category_id'] = freetext_form['prod_cat_id']
            configured_freetext_form['form_id'] = freetext_form['eform_id']
            configured_freetext_form['description'] = freetext_form['description']
            configured_freetext_form['freetext_id'] = freetext_form['freetext_id']
            configured_freetext_form['currency_id'] = freetext_form['currency_id_id']
            configured_freetext_form['prod_cat_desc'] = get_prod_by_id(freetext_form['prod_cat_id'])
            configured_freetext_form['delivery_date'] = calculate_delivery_date_base_on_lead_time(
                freetext_form['lead_time'],
                freetext_form['supplier_id'], None)
            eform_configured = get_freetext_eform_detail(freetext_form['eform_id'])
            if eform_configured:
                eform_flag = 1
            configured_freetext_form['eform_flag'] = eform_flag
            return configured_freetext_form, eform_configured

        except ObjectDoesNotExist:
            return None

    @staticmethod
    def generate_model_based_keys(eform_configured):
        """
        :param eform_configured:
        :return:
        This methods returns back an dictionary containing keys as in model fields and used in create method
        """
        converted_model_fields = {}
        for i in range(0, len(eform_configured)):
            index = str(i + 1)
            get_each_field = eform_configured[i]
            input_type = get_each_field['input_type']
            converted_model_fields['form_field' + index] = get_each_field['input_label']
            if input_type == 'dropdown':
                if get_each_field['dropdown_type'] == 'custom_options':
                    dropdown_options = get_each_field['dropdown_options']
                    string_value = ','.join(str(e) for e in dropdown_options)
                    converted_model_fields['input_type' + index] = get_each_field['input_type'] + '-' + string_value
                else:
                    converted_model_fields['input_type' + index] = get_each_field['input_type'] + \
                                                                   '-' + get_each_field['dropdown_pricetype']

            else:
                converted_model_fields['input_type' + index] = get_each_field['input_type']

            converted_model_fields['check_box' + index] = get_each_field['required']
            converted_model_fields['is_special_char' + index] = get_each_field['allow_special_char']
        return converted_model_fields

    # @staticmethod
    # def generate_form_id(client):
    #     """
    #     :param client:
    #     :return:
    #     """
    #     initial = (str(1).zfill(4))  # To set the initial value to '0001' for the form id
    #     client_des = django_query_instance.django_get_query(OrgClients, {'client': client, 'del_ind': False})
    #     form_id = CONST_SF01 + initial + '_' + client_des.description
    #     check_form_id = django_query_instance.django_existence_check(FreeTextForm, {'form_id': form_id,
    #                                                                                 'client': client})
    #
    #     if check_form_id:
    #         max_form_id = django_query_instance.django_filter_only_query(FreeTextForm,
    #                                                                      {'client': client}).values('form_id')
    #         max_form_id = max_form_id.aggregate(Max('form_id'))
    #         value = list(max_form_id.values())[0]
    #         get_id = re.split('(\d+)', str(value))
    #         increment_id = (int(get_id[1]) + 1)
    #         final_id = (str(increment_id).zfill(4))
    #         form_id = CONST_SF01 + final_id + '_' + client_des.description
    #
    #     return form_id

    @staticmethod
    def check_if_form_exists_in_eform(freetext_id):
        existence_flag = False
        eform_id = None
        if django_query_instance.django_existence_check(FreeTextDetails,
                                                        {'freetext_id': freetext_id,
                                                         'client': global_variables.GLOBAL_CLIENT,
                                                         'del_ind': False}):
            eform_id = django_query_instance.django_filter_value_list_query(FreeTextDetails,
                                                                            {'freetext_id': freetext_id},
                                                                            'eform_id')[0]
            if eform_id:
                if django_query_instance.django_existence_check(EformFieldData,
                                                                {'eform_id': eform_id,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'eform_type': CONST_FT_ITEM_EFORM}):
                    existence_flag = True
        return existence_flag, eform_id

    @staticmethod
    def delete_freetext(freetext_id_list):
        """

        :param freetext_id_list:
        :return:
        """
        freetext_details = django_query_instance.django_filter_query(FreeTextDetails,
                                                                     {'freetext_id__in': freetext_id_list,
                                                                      'client': global_variables.GLOBAL_CLIENT},
                                                                     None,
                                                                     None)
        for freetext_detail in freetext_details:
            # if freetext exists in CartItemDetails or sc item then perform soft delete by setting del_ind = True
            if django_query_instance.django_existence_check(CartItemDetails,
                                                            {'int_product_id': freetext_detail['freetext_id'],
                                                             'call_off': CONST_FREETEXT_CALLOFF,
                                                             'client': global_variables.GLOBAL_CLIENT}
                                                            ) or django_query_instance.django_existence_check(ScItem,
                                                                                                              {
                                                                                                                  'int_product_id':
                                                                                                                      freetext_detail[
                                                                                                                          'freetext_id'],
                                                                                                                  'call_off': CONST_FREETEXT_CALLOFF,
                                                                                                                  'client': global_variables.GLOBAL_CLIENT}
                                                                                                              ):
                if not django_query_instance.django_existence_check(CatalogMapping,
                                                                    {'item_id': freetext_detail['freetext_id'],
                                                                     'client': global_variables.GLOBAL_CLIENT,
                                                                     'call_off': CONST_FREETEXT_CALLOFF,
                                                                     'del_ind': False}):
                    django_query_instance.django_update_query(FreeTextDetails,
                                                              {'freetext_id': freetext_detail['freetext_id'],
                                                               'client': global_variables.GLOBAL_CLIENT},
                                                              {'del_ind': True})
                    django_query_instance.django_update_query(EformFieldConfig,
                                                              {'eform_id': freetext_detail['eform_id'],
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'eform_type': CONST_FT_ITEM_EFORM},
                                                              {'del_ind': True})
            else:
                django_query_instance.django_filter_delete_query(EformFieldConfig,
                                                                 {'eform_id': freetext_detail['eform_id'],
                                                                  'client': global_variables.GLOBAL_CLIENT,
                                                                  'eform_type': CONST_FT_ITEM_EFORM})
                django_query_instance.django_filter_delete_query(FreeTextDetails,
                                                                 {'freetext_id': freetext_detail['freetext_id'],
                                                                  'client': global_variables.GLOBAL_CLIENT})
                django_query_instance.django_filter_delete_query(CatalogMapping,
                                                                 {'item_id': freetext_detail['freetext_id'],
                                                                  'client': global_variables.GLOBAL_CLIENT,
                                                                  'call_off': CONST_FREETEXT_CALLOFF,
                                                                  'del_ind': False})
        freetext_info = get_ft_data()
        return freetext_info

    @staticmethod
    def delete_product_item(product_id_list):
        """

        :param product_id_list:
        :return:
        """
        product_details = django_query_instance.django_filter_query(ProductsDetail,
                                                                    {'product_id__in': product_id_list,
                                                                     'client': global_variables.GLOBAL_CLIENT},
                                                                    None,
                                                                    None)
        for product_detail in product_details:
            # if product exists in CartItemDetails or sc item then perform soft delete by setting del_ind = True
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
                if not django_query_instance.django_existence_check(CatalogMapping,
                                                                    {'item_id': product_detail['product_id'],
                                                                     'client': global_variables.GLOBAL_CLIENT,
                                                                     'call_off': CONST_CATALOG_CALLOFF,
                                                                     'del_ind': False}):
                    django_query_instance.django_update_query(ProductsDetail,
                                                              {'product_id': product_detail['product_id'],
                                                               'client': global_variables.GLOBAL_CLIENT},
                                                              {'del_ind': True})
                    django_query_instance.django_update_query(VariantConfig,
                                                              {'variant_id': product_detail['variant_id'],
                                                               'client': global_variables.GLOBAL_CLIENT},
                                                              {'del_ind': True})
            else:
                django_query_instance.django_filter_delete_query(VariantConfig,
                                                                 {'variant_id': product_detail['variant_id'],
                                                                  'client': global_variables.GLOBAL_CLIENT})
                django_query_instance.django_filter_delete_query(ProductsDetail,
                                                                 {'product_id': product_detail['product_id'],
                                                                  'client': global_variables.GLOBAL_CLIENT})
                django_query_instance.django_filter_delete_query(CatalogMapping,
                                                                 {'item_id': product_detail['product_id'],
                                                                  'client': global_variables.GLOBAL_CLIENT,
                                                                  'call_off': CONST_CATALOG_CALLOFF,
                                                                  'del_ind': False})
        product_info = get_product_detail_config()
        return product_info


def product_eform_into_query_dictionary_list(eform_configured, eform_field_config_guid_list, eform_id):
    """
    :param eform_configured:
    :return:
    This methods returns back an dictionary containing keys as in model fields and used in create method
    """
    converted_model_fields_list = []
    pricing_list = []
    eform_configured_guid = []
    eform_configured_data = []
    # check and remove which is already saved in db table
    if eform_field_config_guid_list:
        for eform_config in eform_configured:
            if not checkKey(eform_config, 'eform_field_config_guid'):
                eform_configured_data.append(eform_config)
            else:
                eform_configured_guid.append(eform_config['eform_field_config_guid'])
    else:
        eform_configured_data = eform_configured
    # uncommon_guid = get_uncommon_elements_from_lists(eform_configured_guid, eform_field_config_guid_list)
    # # delete pricing and eform config db table
    # if uncommon_guid:
    #     delete_eform_data(uncommon_guid)
    # if eformid exists UPDATE max eform_field_count or reset it to 0
    if eform_id:
        form_id = eform_id
        eform_config_detail = django_query_instance.django_filter_only_query(EformFieldConfig,
                                                                             {'eform_id': eform_id,
                                                                              'client': global_variables.GLOBAL_CLIENT,
                                                                              'del_ind': False})
        max_count = eform_config_detail.aggregate(Max('eform_field_count'))
        eform_field_count = max_count['eform_field_count__max']
    else:
        eform_field_count = 0
        form_id = random_int(8)

    # loop the ui entered data
    for eform_configured in eform_configured_data:
        eform_guid = guid_generator()
        converted_model_fields = {'pk': eform_guid, 'eform_type': CONST_CATALOG_ITEM_VARIANT, 'price_flag': False}
        get_each_field = eform_configured
        if get_each_field['dropdown_pricetype'] == "QUANTITY":
            eform_field_count = "0"
        else:
            eform_field_count = str(int(eform_field_count) + 1)
        short_desc = get_each_field['product_desc']
        converted_model_fields['eform_field_count'] = eform_field_count
        eform_field_datatype = get_each_field['eform_field_datatype']
        converted_model_fields['eform_field_name'] = get_each_field['eform_field_name']
        converted_model_fields['eform_id'] = form_id
        if eform_field_datatype == 'dropdown':
            # if get_each_field['dropdown_pricetype'] == 'custom_options':
            dropdown_options = get_each_field['eform_field_data']
            price_option = get_each_field['eform_price']
            converted_model_fields['default_eform_field_data'] = get_each_field['default_eform_field_data']

            if price_option:
                converted_model_fields['price_flag'] = True
                for count, (price, price_data) in enumerate(zip(price_option, dropdown_options)):
                    # set default dropdown in pricing table
                    pricing_data_default = False
                    if price_data == get_each_field['default_eform_field_data']:
                        pricing_data_default = True

                    differential_pricing_flag = False
                    if get_each_field['dropdown_pricetype'] in ['DIFFERENTIAL', 'QUANTITY']:
                        differential_pricing_flag = True
                    if get_each_field['dropdown_pricetype'] == CONST_VARIANT_BASE_PRICING:
                        short_description = short_desc[count]
                    else:
                        short_description = None
                    pricing = {'product_eform_pricing_guid': guid_generator(),
                               'eform_id': form_id,
                               'price': price,
                               'pricing_data': price_data,
                               'operator': get_each_field['operator'],
                               'product_description': short_description,
                               'client': global_variables.GLOBAL_CLIENT,
                               'pricing_type': get_each_field['dropdown_pricetype'],
                               'pricing_data_default': pricing_data_default,
                               'eform_field_config_guid': eform_guid
                               }
                    pricing_list.append(pricing)
            converted_model_fields['eform_field_data'] = '|'.join(str(e) for e in dropdown_options)
            converted_model_fields['eform_field_datatype'] = get_each_field['eform_field_datatype']
            converted_model_fields['dropdown_pricetype'] = get_each_field['dropdown_pricetype']
        else:
            converted_model_fields['eform_field_datatype'] = get_each_field['eform_field_datatype']

        converted_model_fields['required_flag'] = get_each_field['required_flag']
        converted_model_fields['specialchar_flag'] = get_each_field['specialchar_flag']
        converted_model_fields['client'] = global_variables.GLOBAL_CLIENT
        converted_model_fields_list.append(converted_model_fields)

    return converted_model_fields_list, form_id, pricing_list


def get_eform_update_price(prod_detail_get_query):

    """

    """
    price = None
    quantity_index = None
    quantity_dictionary = []
    eform_details = django_query_instance.django_filter_query(VariantConfig,
                                                              {'variant_id': prod_detail_get_query.variant_id,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'del_ind': False},
                                                              None,
                                                              ['variant_id', 'variant_count', 'variant_name',
                                                               'required_flag', 'variant_datatype',
                                                               'specialchar_flag',
                                                               'variant_data', 'display_flag',
                                                               'variant_config_guid', 'variant_flag',
                                                               'dropdown_pricetype'])
    for index, eform_detail in enumerate(eform_details):
        ordered_by = ['-pricing_data_default']
        if eform_detail['dropdown_pricetype'] == CONST_QUANTITY_BASED_DISCOUNT:
            quantity_index = index
            ordered_by = ['pricing_data']
        if eform_detail['variant_flag']:
            eform_product_pricing = django_query_instance.django_filter_query(ProductEformPricing,
                                                                              {'client': global_variables.GLOBAL_CLIENT,
                                                                               'del_ind': False,
                                                                               'variant_config_guid': eform_detail[
                                                                                   'variant_config_guid']},
                                                                              ordered_by, None)

            eform_detail['pricing'] = eform_product_pricing
    # if quantity_index is not None:
    #     if quantity_index >= 0:
    #         quantity_dictionary = eform_details.pop(quantity_index)
    item_price_value = get_product_price_from_eform(prod_detail_get_query.variant_id)
    quantity_dictionary = get_discount_data(prod_detail_get_query.discount_id)
    return eform_details, item_price_value, quantity_dictionary


def get_product_specification_details(product_id, product_info_id):
    """

    """
    product_spec_detail = django_query_instance.django_filter_query(ProductInfo,
                                                                    {'product_info_id': product_info_id,
                                                                     'product_id': product_id,
                                                                     'client': global_variables.GLOBAL_CLIENT,
                                                                     'del_ind': False},
                                                                    None, None)
    return product_spec_detail


def get_freetext_eform_detail(eform_id):
    """

    """
    efrom_details = []
    if django_query_instance.django_existence_check(EformFieldConfig,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'eform_id': eform_id,
                                                     'eform_type': CONST_FT_ITEM_EFORM}):
        efrom_details = django_query_instance.django_filter_query(EformFieldConfig,
                                                                  {'client': global_variables.GLOBAL_CLIENT,
                                                                   'eform_id': eform_id,
                                                                   'eform_type': CONST_FT_ITEM_EFORM},
                                                                  ['eform_field_count'],
                                                                  None)
    eform_configured = []
    for efrom_detail in efrom_details:
        dropdown_options = ''
        required_flag = ''
        if efrom_detail['required_flag']:
            required_flag = 1
        allow_special_char = ''
        if efrom_detail['specialchar_flag']:
            allow_special_char = 1
        if efrom_detail['eform_field_data']:
            dropdown_options = efrom_detail['eform_field_data'].split('|~#')
        eform_dictionary = {'eform_field_config_guid': efrom_detail['eform_field_config_guid'],
                            'eform_id': efrom_detail['eform_id'],
                            'eform_type': efrom_detail['eform_type'],
                            'eform_field_count': efrom_detail['eform_field_count'],
                            'field_data_type': efrom_detail['eform_field_datatype'],
                            'field_name': efrom_detail['eform_field_name'],
                            'required': required_flag,
                            'allow_special_char': allow_special_char,
                            'dropdown_options': dropdown_options}

        if efrom_detail['eform_field_datatype'] == 'dropdown':
            if efrom_detail['eform_field_name'] == 'Country':
                eform_dictionary['dropdown_type'] = 'Country'
            elif efrom_detail['eform_field_name'] == 'Currency':
                eform_dictionary['dropdown_type'] = 'Currency'
            else:
                eform_dictionary['dropdown_type'] = 'dropdown_custom_options'
        eform_configured.append(eform_dictionary)
    return eform_configured


def get_freetext_detail_by_catalog(catalog_id_list, filter_query):
    """

    """
    catalog_mapping_freetext_id_list = django_query_instance.django_filter_value_list_query(CatalogMapping,
                                                                                            {
                                                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                                                'catalog_id__in': catalog_id_list,
                                                                                                'call_off': CONST_FREETEXT_CALLOFF,
                                                                                                'del_ind': False},
                                                                                            'item_id')
    filter_query['freetext_id__in'] = catalog_mapping_freetext_id_list
    free_texts_list = django_query_instance.django_filter_only_query(FreeTextDetails, filter_query).values()
    return free_texts_list


def get_ft_data():
    """

    :return:
    """
    freetext_details = django_query_instance.django_filter_query_with_entry_count(FreeTextDetails,
                                                                                  {
                                                                                      'client': global_variables.GLOBAL_CLIENT,
                                                                                      'del_ind': False},
                                                                                  None,
                                                                                  None, 10)
    freetext_details = update_ft(freetext_details)
    return freetext_details


def update_ft(freetext_details):
    """

    :param freetext_details:
    :return:
    """
    for freetext_detail in freetext_details:
        freetext_detail['ft_transaction'] = False
        if django_query_instance.django_existence_check(CartItemDetails,
                                                        {'int_product_id': freetext_detail['freetext_id'],
                                                         'call_off': CONST_FREETEXT_CALLOFF,
                                                         'client': global_variables.GLOBAL_CLIENT}
                                                        ) or django_query_instance.django_existence_check(ScItem,
                                                                                                          {
                                                                                                              'int_product_id':
                                                                                                                  freetext_detail[
                                                                                                                      'freetext_id'],
                                                                                                              'call_off': CONST_FREETEXT_CALLOFF,
                                                                                                              'client': global_variables.GLOBAL_CLIENT}
                                                                                                          ):
            if django_query_instance.django_existence_check(CatalogMapping,
                                                            {'item_id': freetext_detail['freetext_id'],
                                                             'client': global_variables.GLOBAL_CLIENT}):
                freetext_detail['ft_transaction'] = True
        freetext_detail['encrypted_freetext_id'] = encrypt(freetext_detail['freetext_id'])

    return freetext_details
