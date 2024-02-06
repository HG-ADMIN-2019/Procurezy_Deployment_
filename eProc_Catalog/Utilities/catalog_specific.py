"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    catalog_specific.py
Usage:

Author:
   Deepika
"""

from django.db.models import Q
from django.http import JsonResponse
from eProc_Basic.Utilities.constants.constants import CONST_CATALOG_IMAGE_TYPE, CONST_UNSPSC_IMAGE_TYPE, CONST_FREETEXT_CALLOFF
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import encrypt
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.image_type_funtions import get_image_type
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG128
from eProc_Catalog.Utilities import catalog_global_variables
from eProc_Catalog.Utilities.catalog_generic import CatalogGenericMethods, append_image_into_catalog_list, \
    get_supplier_info, get_prod_cat_info
from eProc_Configuration.models import *
from eProc_Form_Builder.Utilities.form_builder_generic import get_freetext_detail_by_catalog
from eProc_Manage_Content.Utilities.manage_content_generic import get_catalog_mapping_product_id_list
import datetime

from eProc_Price_Calculator.Utilities.price_calculator_generic import get_product_price_from_eform

django_query_instance = DjangoQueries()


class CatalogManagement:

    @staticmethod
    def save_catalog(input):
        """
           saving the catalog which is newly created
           :return: Success or failure response
        """
        catalog_id = int(input['id'])
        get_client = global_variables.GLOBAL_CLIENT
        check_exists = django_query_instance.django_existence_check(Catalogs,
                                                                    {'del_ind': False, 'client': get_client,
                                                                     'catalog_id': catalog_id,
                                                                     'is_active_flag': True})

        if not check_exists:

            """Save the newly added details"""
            inst = Catalogs()
            inst.catalog_guid = guid_generator()
            inst.client = django_query_instance.django_get_query(OrgClients, {'client': get_client})
            inst.del_ind = False
            inst.catalog_id = catalog_id
            inst.name = input['name']
            inst.description = input['description']
            inst.product_type = input['product_type']
            inst.save()
        else:
            """ save the edited details"""
            update_row = django_query_instance.django_get_query(Catalogs,
                                                                {'catalog_id': catalog_id, 'client': get_client,
                                                                 'is_active_flag': True,

                                                                 'del_ind': False})
            update_row.name = input['name']
            update_row.description = input['description']
            update_row.product_type = input['product_type']
            update_row.save()

        res = django_query_instance.django_filter_only_query(Catalogs, {'catalog_id': catalog_id, 'client': get_client,
                                                                        'is_active_flag': True,
                                                                        'del_ind': False})
        return res

    @staticmethod
    def get_catalogs_not_used():
        """
        Get the list of unused catalogs
        :return: list of unused catalogs
        """
        pro_cat_list = list(
            django_query_instance.django_filter_only_query(ProductsDetail,
                                                           {'client': global_variables.GLOBAL_CLIENT}
                                                           ).values_list('catalog_id',
                                                                         flat=True).distinct())
        catalogs_not_assigned = list(
            django_query_instance.django_filter_only_query(Catalogs, {'client': global_variables.GLOBAL_CLIENT,
                                                                      'is_active_flag': True,
                                                                      'del_ind': False
                                                                      })
                .exclude(pk__in=pro_cat_list).values_list('catalog_id', flat=True))

        return JsonResponse(catalogs_not_assigned, safe=False)


class CatalogSearch:

    @staticmethod
    def get_selected_prds_data(selected_catalog, search_type, search_id):
        if selected_catalog == "All":
            catalog_search = catalog_global_variables.USER_ASSIGNED_CATALOGS_LIST
        else:
            catalog_search = [selected_catalog]
        product_id_list = get_catalog_mapping_product_id_list(catalog_search)
        if search_type == 'prod_category':
            get_prds = django_query_instance.django_filter_only_query(ProductsDetail, {
                'client': global_variables.GLOBAL_CLIENT, 'prod_cat_id': search_id, 'product_id__in': product_id_list
            }).values()
            filter_values = {
                'client': global_variables.GLOBAL_CLIENT,
                'prod_cat_id__in': [search_id],
                'del_ind': False
            }
            get_free_texts = get_freetext_detail_by_catalog(catalog_search, filter_values)

            # get_free_texts = django_query_instance.django_filter_only_query(FreeTextForm, {
            #     'client': global_variables.GLOBAL_CLIENT,
            #     'form_id__in': catalog_global_variables.USER_ASSIGNED_FREE_TEXTS_LIST,
            #     'prod_cat_id': search_id
            # })

        elif search_type == 'supplier':
            get_prds = django_query_instance.django_filter_only_query(ProductsDetail, {
                'client': global_variables.GLOBAL_CLIENT, 'product_id__in': product_id_list, 'supplier_id': search_id
            }).values()

            # get_free_texts = django_query_instance.django_filter_only_query(FreeTextForm, {
            #     'client': global_variables.GLOBAL_CLIENT,
            #     'form_id__in': catalog_global_variables.USER_ASSIGNED_FREE_TEXTS_LIST,
            #     'supp_id': search_id
            # })
            filter_values = {
                'client': global_variables.GLOBAL_CLIENT,
                'supplier_id__in': [search_id],
                'del_ind': False
            }
            get_free_texts = get_freetext_detail_by_catalog(catalog_search, filter_values)
        prod_id_list = list(get_prds.values_list('product_id', flat=True))

        image_info = django_query_instance.django_filter_query(ImagesUpload, {
            'client': global_variables.GLOBAL_CLIENT, 'image_default': True, 'image_type': CONST_CATALOG_IMAGE_TYPE,
            'image_id__in': prod_id_list, 'del_ind': False
        }, None, ['image_id', 'image_url'])
        get_prds = update_product_pricing(get_prds)
        catalog_array = append_image_into_catalog_list(get_prds, image_info)
        total_result_count = int(get_prds.count()) + int(get_free_texts.count())

        get_result = CatalogGenericMethods.get_supplier_prod_cat_info(selected_catalog,
                                                                      global_variables.GLOBAL_LOGIN_USER_OBJ_ID)
        for product in catalog_array:
            product['encrypted_product_id'] = encrypt(product['product_id'])

        get_result["catalogs_list"] = get_prds
        get_result["catalog_array"] = catalog_array
        get_result["display_products_result"] = True
        get_result["Free_Texts_list"] = get_free_texts
        get_result['total_result_count'] = total_result_count
        return get_result


class ProductServicesFunctionalities:

    @staticmethod
    def product_form_required_data():
        """
        Get the details which are required to add a product
        :return: Json Data
        """
        supp_data = list(django_query_instance.django_filter_only_query(SupplierMaster, {
            'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
        }).values_list('supplier_id', 'name1'))

        catalogs_list = list(CatalogGenericMethods.catalog_list())
        get_products = list(
            django_query_instance.django_filter_only_query(ProductsDetail, {'client': global_variables.GLOBAL_CLIENT}
                                                           ).values_list('product_id',
                                                                         'short_desc',
                                                                         'supplier_id',
                                                                         'lead_time', 'unit',
                                                                         'price', 'currency'))
        django_query_instance.django_filter_only_query(UnitOfMeasures, {'del_ind': False})
        get_units = list(
            django_query_instance.django_filter_only_query(UnitOfMeasures, {'del_ind': False}).values_list('uom_id',
                                                                                                           'uom_description'))
        currency_list = list(
            django_query_instance.django_filter_only_query(Currency, {'del_ind': False}).values_list('currency_id',
                                                                                                     'description'))
        country_list = list(
            django_query_instance.django_filter_only_query(Country, {'del_ind': False}).values_list('country_code',
                                                                                                    'country_name'))
        language_list = list(
            django_query_instance.django_filter_only_query(Languages, {'del_ind': False}).values_list('language_id',
                                                                                                      'description'))
        # unspsc_list = list(UnspscCategories.objects.filter(del_ind=False).values_list('prod_cat_id'))
        unspsc_list = list(
            django_query_instance.django_filter_only_query(UnspscCategoriesCust, {'del_ind': False}).values_list(
                'prod_cat_id', 'category_desc'))

        context = {
            'supp_list': supp_data,
            'catalog_list': catalogs_list,
            'get_products': get_products,
            'units_of_measure': get_units,
            'currencies': currency_list,
            'country_list': country_list,
            'lang_list': language_list,
            'unspsc_list': unspsc_list
        }

        return context

    @staticmethod
    def save_product(input):
        """
        Saving the newly added product to the catalog
        :return: Queryset of newly added product
        """
        new_prd_inp = ProductsDetail()
        new_prd_inp.client = django_query_instance.django_get_query(OrgClients,
                                                                    {'client': global_variables.GLOBAL_CLIENT})
        new_prd_inp.catalog_item = guid_generator()
        new_prd_inp.product_id = input['product_id']
        new_prd_inp.description = input['description']
        new_prd_inp.supp_txt = input['long_text']
        new_prd_inp.supplier_id = input['supplier_id']
        new_prd_inp.prod_cat_id = input['prod_cat_id']
        new_prd_inp.catalog_id = input['catalog_id']
        new_prd_inp.product_type = input['product_type']
        new_prd_inp.price_on_request = input['price_on_request']
        new_prd_inp.unit = django_query_instance.django_get_query(UnitOfMeasures, {'uom_id': input['unit']})
        new_prd_inp.price_unit = input['price_unit']
        new_prd_inp.currency = django_query_instance.django_get_query(Currency, {'currency_id': input['currency']})
        new_prd_inp.price = float(input['price'])
        new_prd_inp.manufacturer = input['manufacturer']
        new_prd_inp.manu_part_num = input['manu_prod']
        new_prd_inp.unspsc = django_query_instance.django_get_query(UnspscCategories, {'prod_cat_id': input['unspsc']})
        new_prd_inp.brand = input['brand']
        new_prd_inp.lead_time = int(input['lead_time'])
        new_prd_inp.quantity = input['quantity']
        new_prd_inp.quantity_min = int(input['quantity_min'])
        new_prd_inp.offer_key = input['offer_key']
        new_prd_inp.country_of_origin = django_query_instance.django_get_query(Country, {
            'country_code': input['country_of_origin']})
        new_prd_inp.language = django_query_instance.django_get_query(Languages, {'language_id': input['language']})
        new_prd_inp.search_term1 = input['search_term1']
        new_prd_inp.search_term2 = input['search_term2']
        new_prd_inp.created_at = datetime.date.today()
        new_prd_inp.created_by = global_variables.GLOBAL_LOGIN_USERNAME
        new_prd_inp.changed_at = datetime.date.today()
        new_prd_inp.changed_by = global_variables.GLOBAL_LOGIN_USERNAME
        new_prd_inp.ctr_num = ""
        new_prd_inp.ctr_item_num = ""
        new_prd_inp.save()

        return django_query_instance.django_filter_only_query(ProductsDetail, {
            'product_id': input['product_id'],
            'client': global_variables.GLOBAL_CLIENT
        })


def save_image_to_db(prod_cat, file_name, attached_file, default_image):
    prod_id_list = []
    image_type = ''
    for file_path, name, image_flag in zip(prod_cat, file_name, default_image):
        # get product id from file path
        prod_id = file_path.split('-')[0]
        image_type = get_image_type(CONST_CATALOG_IMAGE_TYPE)

        # Delete images if product id already exist in ImagesUpload table for image type catalog
        if image_type:
            if (prod_id in prod_id_list) == False:
                if django_query_instance.django_existence_check(ImagesUpload,
                                                                {'image_id': prod_id, 'image_type': image_type}):
                    product_image_guid = django_query_instance.django_filter_value_list_query(ImagesUpload, {
                        'image_id': prod_id, 'image_type': image_type, 'client': global_variables.GLOBAL_CLIENT
                    }, 'images_upload_guid')

                    for image_guid in product_image_guid:
                        django_query_instance.django_get_query(ImagesUpload,
                                                               {'images_upload_guid': image_guid}).image_url.delete(
                            save=True)
                        django_query_instance.django_get_query(ImagesUpload,
                                                               {'images_upload_guid': image_guid}).delete()
                    prod_id_list.append(prod_id)
        if image_type:
            django_query_instance.django_create_query(ImagesUpload, {
                'images_upload_guid': guid_generator(),
                'client': global_variables.GLOBAL_CLIENT,
                'image_id': prod_id,
                'image_url': attached_file[file_path],
                'image_name': name,
                'image_default': image_flag,
                'image_type': image_type,
                'created_at': datetime.datetime.now(),
                'created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                'del_ind': False
            })
        else:
            msgid = 'MSG128'
            error_msg = get_message_desc(msgid)[1]

            print(error_msg)


def save_prod_cat_cust_image_to_db(prod_cat, file_name, attached_file, default_image):
    prod_id_list = []
    image_type = get_image_type(CONST_UNSPSC_IMAGE_TYPE)
    for file_path, name, image_flag in zip(prod_cat, file_name, default_image):
        prod_id = file_path.split('-')[0]
        if image_type:
            if (prod_id in prod_id_list) == False:
                if django_query_instance.django_existence_check(ImagesUpload, {
                    'image_id': prod_id,
                    'image_type': image_type,
                    'client': global_variables.GLOBAL_CLIENT
                }):
                    product_image_guid = django_query_instance.django_filter_value_list_query(ImagesUpload, {
                        'image_id': prod_id,
                        'image_type': image_type,
                        'client': global_variables.GLOBAL_CLIENT
                    }, 'images_upload_guid')

                    for image_guid in product_image_guid:
                        django_query_instance.django_get_query(ImagesUpload,
                                                               {'images_upload_guid': image_guid}).image_url.delete(
                            save=True)
                        django_query_instance.django_get_query(ImagesUpload,
                                                               {'images_upload_guid': image_guid}).delete()
                    prod_id_list.append(prod_id)
        if image_type:
            django_query_instance.django_create_query(ImagesUpload, {
                'images_upload_guid': guid_generator(),
                'client': global_variables.GLOBAL_CLIENT,
                'image_id': prod_id,
                'image_url': attached_file[file_path],
                'image_name': name,
                'image_default': image_flag,
                'image_type': image_type,
                'created_at': datetime.date.today(),
                'created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                'del_ind': False
            })


def get_searched_prod_detail(selected_catalog, search_type, search_id):
    """

    :param selected_catalog:
    :param search_type:
    :param search_id:
    :return:
    """
    Free_Texts_list = {}
    prod_detail_prodcat_supp = []
    catalog_array = []
    if search_type == 'prod_category':
        prod_detail_prodcat_supp = django_query_instance.django_filter_only_query(ProductsDetail, {
            'client': global_variables.GLOBAL_CLIENT, 'prod_cat_id': search_id,
            'product_id__in': global_variables.GLOBAL_PRODUCT_ID_LIST
        }).values()
        filter_values = {
            'client': global_variables.GLOBAL_CLIENT,
            'prod_cat_id__in': search_id,
            'del_ind': False
        }
        Free_Texts_list = get_freetext_detail_by_catalog(selected_catalog, filter_values)
        # Free_Texts_list = django_query_instance.django_filter_only_query(FreeTextForm, {
        #     'client': global_variables.GLOBAL_CLIENT,
        #     'prod_cat_id': search_id,
        #     'form_id__in': global_variables.GLOBAL_FORM_ID_LIST
        # })
    elif search_type == 'supplier':
        prod_detail_prodcat_supp = django_query_instance.django_filter_only_query(ProductsDetail, {
            'client': global_variables.GLOBAL_CLIENT,
            'product_id__in': global_variables.GLOBAL_PRODUCT_ID_LIST,
            'supplier_id': search_id
        }).values()
        filter_values = {
            'client': global_variables.GLOBAL_CLIENT,
            'supplier_id__in': search_id,
            'del_ind': False
        }
        Free_Texts_list = get_freetext_detail_by_catalog(selected_catalog, filter_values)
        # Free_Texts_list = django_query_instance.django_filter_only_query(FreeTextForm, {
        #     'client': global_variables.GLOBAL_CLIENT,
        #     'supp_id': search_id,
        #     'form_id__in': global_variables.GLOBAL_FORM_ID_LIST
        # }).values()

    total_result_count = int(prod_detail_prodcat_supp.count()) + int(Free_Texts_list.count())
    if prod_detail_prodcat_supp:
        prod_id_list = list(prod_detail_prodcat_supp.values_list('product_id', flat=True))

        image_info = django_query_instance.django_filter_query(ImagesUpload, {
            'client': global_variables.GLOBAL_CLIENT,
            'image_default': True,
            'image_type': CONST_CATALOG_IMAGE_TYPE, 'image_id__in': prod_id_list, 'del_ind': False
        }, None, ['image_id', 'image_url'])
        prod_detail_prodcat_supp = update_product_pricing(prod_detail_prodcat_supp)
        catalog_array = append_image_into_catalog_list(prod_detail_prodcat_supp, image_info)

    prod_detail_search = django_query_instance.django_filter_only_query(ProductsDetail, {
        'client': global_variables.GLOBAL_CLIENT, 'product_id__in': global_variables.GLOBAL_PRODUCT_ID_LIST
    }).values()

    form_detail = django_query_instance.django_filter_only_query(FreeTextDetails, {
        'client': global_variables.GLOBAL_CLIENT, 'eform_id__in': global_variables.GLOBAL_FORM_ID_LIST
    }).values()

    get_unique_suppliers, supp_info, total_supp = CatalogGenericMethods.get_supp_list_count(prod_detail_search,
                                                                                            form_detail)
    get_unique_prods, prod_cat_info, total_prod_count = CatalogGenericMethods.get_prod_cat_list_count(
        prod_detail_search, form_detail)
    for product_detail in  catalog_array:
        product_detail['encrypted_product_id'] = encrypt(product_detail['product_id'])
    context = {
        'is_slide_menu': True,
        'inc_nav': True,
        'selected_catalog': selected_catalog,
        'total_supp': total_supp,
        'cart_counter': global_variables.GLOBAL_CART_COUNTER,
        'supp_info': supp_info,
        'total_prod_count': total_prod_count,
        'prod_cat_info': prod_cat_info,
        'catalog_array': catalog_array,
        'total_result_count': total_result_count,
        'display_products_result': True,
        'Free_Texts_list': Free_Texts_list,
    }
    return context


def encrypt_freetext(free_texts_list):
    """

    """
    freetext_detail_list = []
    for freetext in free_texts_list:
        freetext_dictionary = freetext
        freetext_dictionary['encrypted_freetext_id'] = encrypt(freetext['freetext_id'])
        freetext_detail_list.append(freetext_dictionary)
    return freetext_detail_list


def get_catalog_id_list(selected_catalog):
    """

    :param selected_catalog:
    :return:
    """
    if selected_catalog == "All":
        catalog_search = catalog_global_variables.USER_ASSIGNED_CATALOGS_LIST
    else:
        catalog_search = []
        catalog_search.append(selected_catalog)
    return catalog_search


def get_product_based_product_details_search_type(login_user_catalog_id_list, search_value, search_type, search_id):
    product_id_list = get_catalog_mapping_product_id_list(login_user_catalog_id_list)
    product_detail_query = Q()
    product_detail_query = Q(short_desc__icontains=search_value) | Q(long_desc__icontains=search_value) | Q(
        search_term1__icontains=search_value) | Q(search_term2__icontains=search_value)
    filter_dictionary = {'client': global_variables.GLOBAL_CLIENT,
                         'product_id__in': product_id_list,
                         'del_ind': False}
    if search_type:
        if search_type == 'prod_category':
            filter_dictionary['prod_cat_id__in'] = [search_id]
        elif search_type == 'supplier':
            filter_dictionary['supplier_id__in'] = [search_id]
    prod_detail_search = ProductsDetail.objects.filter(product_detail_query, **filter_dictionary).values()

    return prod_detail_search


def get_category_based_product_details_ft(login_user_catalog_id_list, search_value):
    """

    :param login_user_catalog_id_list:
    :param search_value:
    :return:
    """
    product_id_list = get_catalog_mapping_product_id_list(login_user_catalog_id_list)
    prod_cat_list = list(django_query_instance.django_filter_only_query(ProductsDetail, {
        'client': global_variables.GLOBAL_CLIENT, 'product_id__in': product_id_list
    }).values_list('prod_cat_id', flat=True).distinct())

    unspsc_list = django_query_instance.django_filter_value_list_query(UnspscCategoriesCustDesc, {
        'client': global_variables.GLOBAL_CLIENT,
        'category_desc__icontains': search_value,
        'prod_cat_id__in': prod_cat_list
    }, 'prod_cat_id')

    prod_detail_search = django_query_instance.django_filter_only_query(ProductsDetail, {
        'client': global_variables.GLOBAL_CLIENT,
        'product_id__in': product_id_list,
        'prod_cat_id__in': unspsc_list
    }).values()
    filter_values = {
        'client': global_variables.GLOBAL_CLIENT,
        'prod_cat_id__in': unspsc_list,
        'del_ind': False
    }
    free_texts_list = get_freetext_detail_by_catalog(login_user_catalog_id_list, filter_values)
    # Free_Texts_list = django_query_instance.django_filter_only_query(FreeTextDetails, {
    #     'client': global_variables.GLOBAL_CLIENT,
    #     'catalog_id__in': login_user_catalog_id_list,
    #     'prod_cat_id__in': unspsc_list
    # }).values()

    return prod_detail_search, free_texts_list


def get_supplier_based_product_details_ft(login_user_catalog_id_list, search_value):
    prod_detail_search = []
    free_texts_list = []
    product_id_list = get_catalog_mapping_product_id_list(login_user_catalog_id_list)
    supplier_list = list(django_query_instance.django_filter_only_query(ProductsDetail, {
        'client': global_variables.GLOBAL_CLIENT,
        'product_id__in': product_id_list
    }).values_list('supplier_id', flat=True).distinct())

    if search_value:
        supp_detail = django_query_instance.django_filter_value_list_query(SupplierMaster, {
            'client': global_variables.GLOBAL_CLIENT,
            'supplier_id__in': supplier_list,
            'name1__icontains': search_value
        }, 'supplier_id')

        prod_detail_search = django_query_instance.django_filter_only_query(ProductsDetail, {
            'client': global_variables.GLOBAL_CLIENT,
            'product_id__in': product_id_list,
            'supplier_id__in': supp_detail
        }).values()
        # Free_Texts_list = django_query_instance.django_filter_only_query(FreeTextDetails, {
        #     'client': global_variables.GLOBAL_CLIENT,
        #     'catalog_id__in': login_user_catalog_id_list,
        #     'supplier_id__in': supp_detail
        # }).values()
        filter_values = {
            'client': global_variables.GLOBAL_CLIENT,
            'supplier_id__in': supp_detail,
            'del_ind': False
        }
        free_texts_list = get_freetext_detail_by_catalog(login_user_catalog_id_list, filter_values)

    return prod_detail_search, free_texts_list


def get_product_id_free_text_id_list(prod_detail_search, free_texts_detail):
    free_text_id_list = []
    prod_id_list = []
    if prod_detail_search:
        prod_id_list = list(prod_detail_search.values_list('product_id', flat=True))
    if free_texts_detail:
        free_text_id_list = list(free_texts_detail.values_list('freetext_id', flat=True))

    return prod_id_list, free_text_id_list


def save_product_images(attached_file, product_id):
    """

    """
    # delete if image exists for specified product id
    # if django_query_instance.django_existence_check(ImagesUpload, {
    #     'image_id': product_id,
    #     'image_type': CONST_CATALOG_IMAGE_TYPE,
    #     'client': global_variables.GLOBAL_CLIENT
    # }):
    #     product_image_guid = django_query_instance.django_filter_value_list_query(ImagesUpload, {
    #         'image_id': product_id,
    #         'image_type': CONST_CATALOG_IMAGE_TYPE,
    #         'client': global_variables.GLOBAL_CLIENT
    #     }, 'images_upload_guid')
    #
    #     for image_guid in product_image_guid:
    #         django_query_instance.django_get_query(ImagesUpload,
    #                                                {'images_upload_guid': image_guid}).image_url.delete(
    #             save=True)
    #         django_query_instance.django_get_query(ImagesUpload,
    #                                                {'images_upload_guid': image_guid}).delete()
    for key, value in attached_file.items():
        image_key = key.split('-')
        if image_key[1] == '1':
            image_default = True
            image_no = int(image_key[1])
        else:
            image_default = False
        if django_query_instance.django_existence_check(ImagesUpload,
                                                        {'image_id': product_id,
                                                         'image_type': CONST_CATALOG_IMAGE_TYPE,
                                                         'image_number': int(image_key[1]),
                                                         'client': global_variables.GLOBAL_CLIENT}):
            django_query_instance.django_get_query(ImagesUpload,
                                                   {'image_id': product_id,
                                                    'image_type': CONST_CATALOG_IMAGE_TYPE,
                                                    'image_number': int(image_key[1]),
                                                    'client': global_variables.GLOBAL_CLIENT}).image_url.delete(
                save=True)
            django_query_instance.django_get_query(ImagesUpload,
                                                   {'image_id': product_id,
                                                    'image_type': CONST_CATALOG_IMAGE_TYPE,
                                                    'image_number': int(image_key[1]),
                                                    'client': global_variables.GLOBAL_CLIENT}).delete()
        django_query_instance.django_create_query(ImagesUpload, {
            'images_upload_guid': guid_generator(),
            'client': global_variables.GLOBAL_CLIENT,
            'image_id': image_key[0],
            'image_url': value,
            'image_number': int(image_key[1]),
            'image_name': value.name,
            'image_default': image_default,
            'image_type': CONST_CATALOG_IMAGE_TYPE,
            'created_at': datetime.datetime.now(),
            'created_by': global_variables.GLOBAL_LOGIN_USERNAME,
            'del_ind': False
        })


def get_search_result_list(search_value, selected_catalog, search_type, search_id):
    """

    """
    login_user_catalog_id_list = get_catalog_id_list(selected_catalog)
    free_texts_detail = {}
    prod_detail_search = {}
    free_text_id_list = []
    product_count = 0
    freetext_count = 0
    total_result_count = 0
    global_variables.GLOBAL_PRODUCT_SEARCH_FLAG = True
    """ Start of get Free Text and Product Details """
    if global_variables.GLOBAL_PROD_SEARCH_TYPE in ['PRODUCTS','ALL']:
        prod_detail_search = get_product_based_product_details_search_type(login_user_catalog_id_list, search_value,
                                                                           search_type, search_id)
        if global_variables.GLOBAL_PROD_SEARCH_TYPE == 'ALL':
            free_texts_detail = get_freetext_detail(login_user_catalog_id_list, search_value, search_type, search_id)
    if global_variables.GLOBAL_PROD_SEARCH_TYPE == 'CATEGORIES':
        prod_detail_search, free_texts_detail = get_category_based_product_details_ft(login_user_catalog_id_list,
                                                                                      search_value)

    if global_variables.GLOBAL_PROD_SEARCH_TYPE == 'SUPPLIERS':
        prod_detail_search, free_texts_detail = get_supplier_based_product_details_ft(login_user_catalog_id_list,
                                                                                      search_value)
    if global_variables.GLOBAL_PROD_SEARCH_TYPE == 'FREETEXT':
        free_texts_detail = get_freetext_detail(login_user_catalog_id_list, search_value, search_type, search_id)

    """ End of get Free Text and Product Details """

    """ Globally store Product id and form id of user entered search text"""
    global_variables.GLOBAL_PRODUCT_ID_LIST, global_variables.GLOBAL_FORM_ID_LIST = get_product_id_free_text_id_list(
        prod_detail_search, free_texts_detail)

    image_info = django_query_instance.django_filter_query(ImagesUpload, {
        'client': global_variables.GLOBAL_CLIENT,
        'image_default': True,
        'image_type': CONST_CATALOG_IMAGE_TYPE,
        'image_id__in': global_variables.GLOBAL_PRODUCT_ID_LIST,
        'del_ind': False
    }, None, ['image_id', 'image_url'])
    prod_detail_search = update_product_pricing(prod_detail_search)
    catalog_array = append_image_into_catalog_list(prod_detail_search, image_info)

    if global_variables.GLOBAL_PROD_SEARCH_TYPE == 'PRODUCT':
        get_unique_suppliers, supp_info, total_supp = get_supplier_info(prod_detail_search)
        get_unique_prods, prod_cat_info, total_prod_count = get_prod_cat_info(prod_detail_search)

    else:
        get_unique_suppliers, supp_info, total_supp = CatalogGenericMethods.get_supp_list_count(prod_detail_search,
                                                                                                free_texts_detail)
        get_unique_prods, prod_cat_info, total_prod_count = CatalogGenericMethods.get_prod_cat_list_count(
            prod_detail_search, free_texts_detail)

        if free_texts_detail:
            freetext_count = int(free_texts_detail.count())
        if prod_detail_search:
            product_count = int(prod_detail_search.count())
        total_result_count = product_count + freetext_count
    if free_texts_detail:
        free_texts_detail = encrypt_freetext(free_texts_detail)
    for product_detail in  catalog_array:
        product_detail['encrypted_product_id'] = encrypt(product_detail['product_id'])
    context = {
        'is_slide_menu': True,
        'inc_nav': True,
        'selected_catalog': global_variables.GLOBAL_CATALOG_ID,
        'total_supp': total_supp,
        'cart_counter': global_variables.GLOBAL_CART_COUNTER,
        'supp_info': supp_info,
        'total_prod_count': total_prod_count,
        'prod_cat_info': prod_cat_info,
        'catalog_array': catalog_array,
        'total_result_count': total_result_count,
        'display_products_result': True,
        'Free_Texts_list': free_texts_detail,
        'is_shop_active': True,
        'document_number': global_variables.GLOBAL_DOCUMENT_NUM,
        'encrypt_doc_num': global_variables.GLOBAL_ENCRYPTED_DOC_NUM
    }
    return context


def update_product_pricing(prod_details):
    """

    """
    for product_detail in prod_details:
        if product_detail['variant_id']:
            product_detail['price'] = get_product_price_from_eform(product_detail['variant_id'])
            print("price ", product_detail['price'])
    return prod_details


def get_freetext_detail(login_user_catalog_id_list, search_value, search_type, search_id):
    """

    :param login_user_catalog_id_list:
    :param search_value:
    :return:
    """
    filter_query = {}
    catalog_mapping_freetext_id_list = django_query_instance.django_filter_value_list_query(CatalogMapping,
                                                                                            {
                                                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                                                'catalog_id__in': login_user_catalog_id_list,
                                                                                                'call_off': CONST_FREETEXT_CALLOFF,
                                                                                                'del_ind': False},
                                                                                            'item_id')
    freetext_detail_query = Q()
    freetext_detail_query = Q(freetext_id__icontains=search_value) | Q(description__icontains=search_value)
    filter_dictionary = {'client': global_variables.GLOBAL_CLIENT,
                         'freetext_id__in': catalog_mapping_freetext_id_list,
                         'del_ind': False}
    if search_type:
        if search_type == 'prod_category':
            filter_dictionary['prod_cat_id__in'] = [search_id]
        elif search_type == 'supplier':
            filter_dictionary['supplier_id__in'] = [search_id]
    free_texts_list = FreeTextDetails.objects.filter(freetext_detail_query, **filter_dictionary).values()
    return free_texts_list
