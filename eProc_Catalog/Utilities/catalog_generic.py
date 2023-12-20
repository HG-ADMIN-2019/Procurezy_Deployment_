"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    catalog_generic.py
Usage:
    append_image_into_catalog_list
    append_supp_image_into_supp_list
    get_supplier_info
    get_prod_cat_info

Author:
   Deepika
"""
from django.db.models import Q

from eProc_Attributes.Utilities.attributes_generic import OrgAttributeValues
from eProc_Attributes.Utilities.attributes_specific import CONST_CAT_ID, CONST_FREE_TEXT_ID
from eProc_Attributes.models.org_attribute_models import OrgAttributesLevel
from eProc_Basic.Utilities.constants.constants import CONST_SUPPLIER_IMAGE_TYPE, CONST_UNSPSC_IMAGE_TYPE, \
    CONST_VARIANT_BASE_PRICING, CONST_VARIANT_ADDITIONAL_PRICING, CONST_CATALOG_ITEM_VARIANT
from eProc_Basic.Utilities.functions.dict_check_key import list_value_count
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import encrypt, decrypt
from eProc_Basic.Utilities.functions.get_db_query import display_cart_counter
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Catalog.Utilities import catalog_global_variables
from eProc_Configuration.models import ImagesUpload, Catalogs, ProductsDetail, FreeTextForm, EformFieldConfig
from eProc_Form_Builder.Utilities.form_builder_generic import get_freetext_detail_by_catalog
from eProc_Manage_Content.Utilities.manage_content_generic import get_catalog_mapping_product_id_list
from eProc_Price_Calculator.Utilities.price_calculator_generic import get_product_price_from_eform
from eProc_Registration.models import UserData
from eProc_Shopping_Cart.models import ScHeader, ScItem, CartItemDetails
from eProc_User_Settings.Utilities.user_settings_generic import get_supp_desc_count, get_prod_cat_desc_count, \
    get_object_id_list_user

django_query_instance = DjangoQueries()


def append_image_into_catalog_list(catalog_list, image_info):
    """

    :param catalog_list:
    :return:
    """
    catalog_array = []
    for catalog_item in catalog_list:
        catalog_dic = catalog_item
        for product_image_info in image_info:
            if catalog_item['product_id'] == product_image_info['image_id']:
                catalog_dic['image_url'] = product_image_info['image_url']
                break
            else:
                catalog_item['image_url'] = ''
        if catalog_item['eform_id']:
            queue_query = Q()
            queue_query = ~Q(dropdown_pricetype__in=[CONST_VARIANT_BASE_PRICING, CONST_VARIANT_ADDITIONAL_PRICING])
            if not django_query_instance.django_queue_existence_check(EformFieldConfig,
                                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                                       'del_ind': False,
                                                                       'eform_id': catalog_item['eform_id'],
                                                                       'eform_type': CONST_CATALOG_ITEM_VARIANT},
                                                                      queue_query):
                catalog_dic['price'] = get_product_price_from_eform(catalog_item['eform_id'])

        catalog_array.append(catalog_dic)
    return catalog_array


def append_supp_image_into_supp_list(catalog_list, image_info):
    """

    :param catalog_list:
    :return:
    """
    catalog_array = []
    for catalog_item in catalog_list:
        catalog_dic = {}
        for product_image_info in image_info:
            catalog_dic = catalog_item
            if catalog_item['product_id'] == product_image_info['product_id']:
                catalog_dic['image_url'] = product_image_info['image_url']
                break
            else:
                catalog_item['image_url'] = ''

        catalog_array.append(catalog_dic)
    return catalog_array


class CatalogGenericMethods:

    @staticmethod
    def catalog_list():

        get_list = django_query_instance.django_filter_query(Catalogs,
                                                             {'client': global_variables.GLOBAL_CLIENT,
                                                              'is_active_flag': True,
                                                              'del_ind': False},
                                                             None,
                                                             ['catalog_id', 'name'])
        return get_list

    @staticmethod
    def get_supp_list_count(get_cat, assigned_free_texts_querry_set):
        """

        :param get_cat:
        :param assigned_free_texts_querry_set:
        :return:
        """
        unique_supp_list = []
        supp_id_desc_count = []
        total_supp = []

        if get_cat:
            if assigned_free_texts_querry_set:
                catalog_supp_list = list(get_cat.values_list('supplier_id', flat=True)) + list(
                    assigned_free_texts_querry_set.values_list('supplier_id', flat=True))
                uncommon_supp_id = set(list(get_cat.values_list('supplier_id', flat=True).distinct())) - set(
                    list(assigned_free_texts_querry_set.values_list('supplier_id', flat=True).distinct()))
                unique_supp_list = list(
                    assigned_free_texts_querry_set.values_list('supplier_id', flat=True).distinct()) + list(
                    uncommon_supp_id)
            else:
                catalog_supp_list = list(get_cat.values_list('supplier_id', flat=True))
                unique_supp_list = set(list(get_cat.values_list('supplier_id', flat=True).distinct()))
        else:
            if assigned_free_texts_querry_set:
                catalog_supp_list = list(assigned_free_texts_querry_set.values_list('supplier_id', flat=True))
                unique_supp_list = set(
                    list(assigned_free_texts_querry_set.values_list('supplier_id', flat=True).distinct()))
            else:
                catalog_supp_list = []
                unique_supp_list = set()
        supp_id_count = list_value_count(catalog_supp_list)
        supp_id_desc_count = get_supp_desc_count(supp_id_count)
        total_supp = len(list(dict.fromkeys(unique_supp_list)))
        supp_image_info = django_query_instance.django_filter_query(ImagesUpload,
                                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                                     'image_id__in': unique_supp_list,
                                                                     'image_type': CONST_SUPPLIER_IMAGE_TYPE,
                                                                     'del_ind': False}, None,
                                                                    ['image_id', 'image_url'])
        for supp_dic in supp_id_desc_count:
            for supp_image in supp_image_info:
                if supp_dic['supplier_id'] == supp_image['image_id']:
                    supp_dic['image_url'] = supp_image['image_url']
                    break
                else:
                    supp_dic['image_url'] = ''

        return unique_supp_list, supp_id_desc_count, total_supp

    @staticmethod
    def get_prod_cat_list_count(get_cat, assigned_free_texts_querry_set):
        """

        :param get_cat:
        :param assigned_free_texts_querry_set:
        :return:
        """
        unique_prod_cat_list = []
        prod_cat_info = []
        total_prod_count = []
        if get_cat:
            if assigned_free_texts_querry_set:
                catalog_prod_cat_list = list(get_cat.values_list('prod_cat_id', flat=True)) + list(
                    assigned_free_texts_querry_set.values_list('prod_cat_id', flat=True))
                uncommon_prod_cat = set(list(get_cat.values_list('prod_cat_id', flat=True).distinct())) - set(
                    list(assigned_free_texts_querry_set.values_list('prod_cat_id', flat=True).distinct()))
                unique_prod_cat_list = list(
                    assigned_free_texts_querry_set.values_list('prod_cat_id', flat=True).distinct()) + list(
                    uncommon_prod_cat)
            else:
                catalog_prod_cat_list = list(get_cat.values_list('prod_cat_id', flat=True))
                unique_prod_cat_list = list(get_cat.values_list('prod_cat_id', flat=True).distinct())
        else:
            if assigned_free_texts_querry_set:
                catalog_prod_cat_list = list(assigned_free_texts_querry_set.values_list('prod_cat_id', flat=True))
                unique_prod_cat_list = set(
                    list(assigned_free_texts_querry_set.values_list('prod_cat_id', flat=True).distinct()))
            else:
                catalog_prod_cat_list = []
                unique_prod_cat_list = set()
        prod_cat_count = list_value_count(catalog_prod_cat_list)
        prod_cat_info = get_prod_cat_desc_count(prod_cat_count)
        total_prod_count = len(list(dict.fromkeys(unique_prod_cat_list)))
        prod_cat_image_info = django_query_instance.django_filter_query(ImagesUpload,
                                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                                         'image_id__in': unique_prod_cat_list,
                                                                         'image_type': CONST_UNSPSC_IMAGE_TYPE,
                                                                         'del_ind': False}, None,
                                                                        ['image_id', 'image_url'])

        for prod_cat_dic in prod_cat_info:
            for prod_cat_image in prod_cat_image_info:
                if prod_cat_dic['prod_cat_id'] == prod_cat_image['image_id']:
                    prod_cat_dic['image_url'] = prod_cat_image['image_url']
                    break
                else:
                    prod_cat_dic['image_url'] = ''
        return unique_prod_cat_list, prod_cat_info, total_prod_count

    @staticmethod
    def get_supplier_prod_cat_info(catalog_id, user_object_id):
        """

        :return:
        """
        obj_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT, user_object_id)
        CatalogGenericMethods.get_logged_in_user_catalogs(obj_id_list)

        if catalog_id == 'All':
            get_list_of_assigned_catalogs = catalog_global_variables.USER_ASSIGNED_CATALOGS_LIST
            product_id_list = get_catalog_mapping_product_id_list(get_list_of_assigned_catalogs)
            get_cat = django_query_instance.django_filter_only_query(ProductsDetail,
                                                                     {'client': global_variables.GLOBAL_CLIENT,
                                                                      'product_id__in': product_id_list,
                                                                      'del_ind': False})
        else:
            get_list_of_assigned_catalogs = [catalog_id]
            product_id_list = get_catalog_mapping_product_id_list([catalog_id])
            get_cat = django_query_instance.django_filter_only_query(ProductsDetail,
                                                                     {'client': global_variables.GLOBAL_CLIENT,
                                                                      'product_id__in': product_id_list,
                                                                      'del_ind': False})
        filter_values = {
            'client': global_variables.GLOBAL_CLIENT,
            'del_ind': False
        }
        assigned_free_texts_querry_set = get_freetext_detail_by_catalog(get_list_of_assigned_catalogs, filter_values)
        # assigned_free_texts_querry_set = CatalogGenericMethods.get_logged_in_user_Free_texts(obj_id_list)

        """Get the suppliers and its count for catalog products data"""
        get_unique_suppliers, supp_info, total_supp = CatalogGenericMethods.get_supp_list_count(get_cat,
                                                                                                assigned_free_texts_querry_set)
        """Get the product Categories and its count from the catalog products """
        get_unique_prods, prod_cat_info, total_prod_count = CatalogGenericMethods.get_prod_cat_list_count(get_cat,
                                                                                                          assigned_free_texts_querry_set)

        data = {'inc_nav': True,
                'total_supp': total_supp,
                'cart_counter': display_cart_counter(global_variables.GLOBAL_LOGIN_USERNAME),
                'supp_info': supp_info,
                'total_prod_count': total_prod_count,
                'prod_cat_info': prod_cat_info,
                'selected_catalog': catalog_id,
                }
        return data

    @staticmethod
    def get_logged_in_user_catalogs(obj_id_list):
        """
        Get the list of catalogs assigned to the logged in user
        :return: The list of assigned catalogs
        """
        catalog_id_list = OrgAttributeValues.get_user_attr_value_list_by_attr_id(
            obj_id_list, CONST_CAT_ID)
        catalog_global_variables.USER_ASSIGNED_CATALOGS_LIST = django_query_instance.django_filter_value_list_query(
            Catalogs,
            {'client': global_variables.GLOBAL_CLIENT,
             'del_ind': False,
             'catalog_id__in': catalog_id_list,
             'is_active_flag': True}
            , 'catalog_id')
        assigned_catalogs = django_query_instance.django_filter_only_query(Catalogs, {
            'client': str(global_variables.GLOBAL_CLIENT),
            'catalog_id__in': catalog_global_variables.USER_ASSIGNED_CATALOGS_LIST,
            'is_active_flag': True
        })
        return assigned_catalogs

    @staticmethod
    def get_logged_in_user_Free_texts(obj_id_list):
        """
        Get the list of free texts assigned to the logged in user
        :return: The list of Free texts
        """
        catalog_global_variables.USER_ASSIGNED_FREE_TEXTS_LIST = django_query_instance.django_filter_value_list_query(
            OrgAttributesLevel, {
                'client': str(global_variables.GLOBAL_CLIENT), 'object_id__in': obj_id_list,
                'attribute_id': CONST_FREE_TEXT_ID, 'del_ind': False
            }, 'low')

        assigned_free_texts = django_query_instance.django_filter_only_query(FreeTextForm, {
            'client': str(global_variables.GLOBAL_CLIENT),
            'form_id__in': catalog_global_variables.USER_ASSIGNED_FREE_TEXTS_LIST
        })

        return assigned_free_texts


def get_supplier_info(prod_detail):
    unique_supp_list = []
    supp_id_desc_count = []
    total_supp = []
    if prod_detail:
        catalog_supp_list = list(prod_detail.values_list('supplier_id', flat=True))
        unique_supp_list = set(list(prod_detail.values_list('supplier_id', flat=True).distinct()))
        supp_id_count = list_value_count(catalog_supp_list)
        supp_id_desc_count = get_supp_desc_count(supp_id_count)
        total_supp = len(list(dict.fromkeys(unique_supp_list)))

    return unique_supp_list, supp_id_desc_count, total_supp


def get_prod_cat_info(prod_detail):
    """

    :param prod_detail:
    :return:
    """
    unique_prod_cat_list = []
    prod_cat_info = []
    total_prod_count = 0
    if prod_detail:
        catalog_prod_cat_list = list(prod_detail.values_list('unspsc', flat=True))
        unique_prod_cat_list = set(list(prod_detail.values_list('unspsc', flat=True).distinct()))
        prod_cat_count = list_value_count(catalog_prod_cat_list)
        prod_cat_info = get_prod_cat_desc_count(prod_cat_count)
        total_prod_count = len(list(dict.fromkeys(unique_prod_cat_list)))
    return unique_prod_cat_list, prod_cat_info, total_prod_count


def update_requester_object_id(document_number):
    """

    """
    print(global_variables.GLOBAL_REQUESTER_OBJECT_ID)
    if django_query_instance.django_existence_check(ScHeader, {'doc_number': document_number,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'del_ind': False}):
        document_requester = django_query_instance.django_get_query(ScHeader, {'doc_number': document_number,
                                                                               'client': global_variables.GLOBAL_CLIENT,
                                                                               'del_ind': False}).requester

        user_object_id = django_query_instance.django_get_query(UserData, {'username': document_requester,
                                                                           'client': global_variables.GLOBAL_CLIENT}).object_id_id
        global_variables.GLOBAL_REQUESTER_OBJECT_ID = user_object_id

    return user_object_id


def get_item_detail(item_guid):
    """
    """
    item_detail  = None
    if django_query_instance.django_existence_check(CartItemDetails,
                                                    {'guid':item_guid,
                                                     'client':global_variables.GLOBAL_CLIENT}):
        item_detail = django_query_instance.django_get_query(CartItemDetails,
                                                    {'guid':item_guid,
                                                     'client':global_variables.GLOBAL_CLIENT})
    elif django_query_instance.django_existence_check(ScItem,
                                                      {'guid':item_guid,
                                                       'client': global_variables.GLOBAL_CLIENT}):
        item_detail = django_query_instance.django_get_query(ScItem,
                                                             {'guid': item_guid,
                                                              'client': global_variables.GLOBAL_CLIENT})
    return item_detail
