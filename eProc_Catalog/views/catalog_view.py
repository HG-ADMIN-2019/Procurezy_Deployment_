"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    catalog_view.py
Usage:


Author:
   Deepika
"""
import datetime

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from eProc_Basic.Utilities.constants.constants import CONST_CATALOG, CONST_CATALOG_IMAGE_TYPE, \
    CONST_USER_RECENTLY_VIEWED, CONST_CATALOG_CALLOFF
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import decrypt, encrypt
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.global_defination import global_variables
from django.http import JsonResponse
from itertools import chain
from eProc_Basic.decorators import authorize_view
from eProc_Catalog.Utilities import catalog_global_variables
from eProc_Catalog.Utilities.catalog_generic import CatalogGenericMethods, append_image_into_catalog_list, \
    get_supplier_info, get_prod_cat_info, update_requester_object_id, get_item_detail
from eProc_Catalog.Utilities.catalog_specific import *
from eProc_Configuration.models import UnspscCategoriesCustDesc, ImagesUpload, Catalogs, ProductsDetail, SupplierMaster, \
    CatalogMapping
from eProc_Form_Builder.Utilities.form_builder_generic import get_eform_update_price, get_product_specification_details
from eProc_Manage_Content.Utilities.manage_content_generic import get_catalog_mapping_product_id_list
from eProc_Form_Builder.models import EformFieldData
from eProc_Registration.models import UserData
from eProc_Shop_Home.models import RecentlyViewedProducts
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import update_supplier_uom, update_unspsc, update_country
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Shopping_Cart.models import ScHeader, CartItemDetails, ScItem

json_obj = JsonParser()
django_query_instance = DjangoQueries()


@login_required
@authorize_view(CONST_CATALOG)
def get_catalog_list(req, catalog_id, document_number=None):
    """
    Get the list of static catalog items
    :param catalog_id:
    :param document_number:
    :param req: POST
    :return: list of static catalog items(get_cat)
    """
    update_user_info(req)
    encrypt_doc_num = 'create'
    if document_number != 'create':
        encrypt_doc_num = document_number.split('doc_number-')[1]
    # catalog_id = decrypt(catalog_id)
    if 'hg_cat_search_txt' in req.POST:
        context = get_search_result_list(req.POST.get('hg_cat_search_txt'), catalog_id, None, None)
        context['encrypt_doc_num'] = encrypt_doc_num
        return render(req, 'Catalog/products_services_catalog.html', context)
    global_variables.GLOBAL_CATALOG_ID = catalog_id
    global_variables.GLOBAL_PRODUCT_SEARCH_FLAG = False
    if document_number == 'create':
        global_variables.GLOBAL_DOCUMENT_NUM = 'create'
        user_object_id = global_variables.GLOBAL_LOGIN_USER_OBJ_ID
        global_variables.GLOBAL_REQUESTER_OBJECT_ID = None
    else:

        document_number = decrypt(document_number.split('doc_number-')[1])
        global_variables.GLOBAL_DOCUMENT_NUM = document_number
        user_object_id = update_requester_object_id(document_number)
    result = CatalogGenericMethods.get_supplier_prod_cat_info(catalog_id, user_object_id)
    catalog_global_variables.CATALOG_PAGE_REQUIERED_DATA = result
    result['is_slide_menu'] = True
    result['document_number'] = document_number
    result['is_shop_active'] = True
    result['encrypt_doc_num'] = global_variables.GLOBAL_ENCRYPTED_DOC_NUM
    result['search_type'] = ''
    result['search_id'] = ''
    result['search_type'] = global_variables.GLOBAL_PROD_SEARCH_TYPE
    print("search type", result['search_type'])

    return render(req, 'Catalog/products_services_catalog.html', result)


@transaction.atomic
def create_catalog(request):
    """
    saving the catalog which is newly created
    :param request: POST
    :return: Success or failure response
    """
    input = json_obj.get_json_from_req(request)
    res = CatalogManagement.save_catalog(input)
    return json_obj.get_json_from_obj(res)


def get_app_catalogs(request):
    """
    Get list of catalogs to show in application setting
    :param request: post
    :return: list of catalogs
    """
    res = django_query_instance.django_filter_only_query(Catalogs, {'client': global_variables.GLOBAL_CLIENT,
                                                                    'del_ind': False,
                                                                    'is_active_flag': True})
    return json_obj.get_json_from_obj(res)


def get_catalogs_not_used(request):
    """
    Get the catalogs which are not assigned any where
    :param request: post
    :return: list of catalogs not Used
    """
    return CatalogManagement.get_catalogs_not_used()


@transaction.atomic
def delete_catalogs(request):
    """
    Catalogs to be deleted
    :param request: POST
    :return: result
    """
    get_item = request.POST.get('delete_item')
    django_query_instance.django_filter_delete_query(Catalogs, {'client': global_variables.GLOBAL_CLIENT,
                                                                'pk': get_item, 'del_ind': False,
                                                                'is_active_flag': True})

    res = django_query_instance.django_filter_only_query(Catalogs,
                                                         {'client': global_variables.GLOBAL_CLIENT,
                                                          'del_ind': False,
                                                          'is_active_flag': True})

    return json_obj.get_json_from_obj(res)


def product_form_required_data(request):
    """
    Get the data which to used to create a product/service for catalog
    :param request:
    :return:
    """
    result = ProductServicesFunctionalities.product_form_required_data()
    return JsonResponse(result)


@transaction.atomic
def add_product_or_service(request):
    """
    Creating a product from application settings
    :param request: POST
    :return: A newly created product
    """
    input = json_obj.get_json_from_req(request)
    res = ProductServicesFunctionalities.save_product(input)
    return json_obj.get_json_from_obj(res)


@authorize_view(CONST_CATALOG)
def get_products_services_on_select(request, selected_catalog, search_type, search_id, document_number=None):
    update_user_info(request)
    encrypt_doc_num = 'create'
    if 'hg_cat_search_txt' in request.POST:
        result = get_search_result_list(request.POST.get('hg_cat_search_txt'), selected_catalog, None, None)
    else:
        if not global_variables.GLOBAL_PRODUCT_SEARCH_FLAG:
            result = CatalogSearch.get_selected_prds_data(selected_catalog, search_type, search_id)
        else:
            result = get_searched_prod_detail(selected_catalog, search_type, search_id)
    if document_number != 'create':
        encrypt_doc_num = document_number.split('doc_number-')[1]
        document_number = decrypt(encrypt_doc_num)
        result['document_number'] = document_number
    if result['Free_Texts_list']:
        result['Free_Texts_list'] = encrypt_freetext(result['Free_Texts_list'])
    # for catalogs_list in result['catalogs_list']:
    #     catalogs_list = update_supplier_uom(catalogs_list)
    result['encrypt_doc_num'] = encrypt_doc_num
    result['document_number'] = document_number
    result['search_type'] = search_type
    result['search_id'] = search_id
    result['is_slide_menu'] = True
    result['is_shop_active'] = True
    return render(request, 'Catalog/products_services_catalog.html', result)


def get_all_catalogs(request):
    return django_query_instance.django_filter_only_query(Catalogs, {'client': global_variables.GLOBAL_CLIENT,
                                                                     'del_ind': False,
                                                                     'is_active_flag': True})


# Render Product detail pop up
# def get_product_service_prod_details(request):
#     """
#     :param request:
#     :return:
#     """
#     update_user_info(request)
#     eform_detail = []
#     product_specification = []
#     quantity_dictionary = []
#     item_price = None
#     username = global_variables.GLOBAL_LOGIN_USERNAME
#     client = global_variables.GLOBAL_CLIENT
#     product_details = {}
#
#     prod_id = json_obj.get_json_from_req(request)
#     product_id = prod_id['prod_id']
#     # catalog_id = catalog_id
#     prod_detail = {}
#
#     if django_query_instance.django_existence_check(ProductsDetail, {'client': global_variables.GLOBAL_CLIENT,
#                                                                      'product_id': product_id}):
#         prod_detail = django_query_instance.django_filter_query(ProductsDetail,
#                                                                 {'client': global_variables.GLOBAL_CLIENT,
#                                                                  'product_id': product_id}, None, None)[0]
#         prod_detail_get_query = django_query_instance.django_get_query(ProductsDetail,
#                                                                        {'client': global_variables.GLOBAL_CLIENT,
#                                                                         'product_id': product_id})
#         if prod_detail:
#             prod_detail = update_supplier_uom(prod_detail)
#             prod_detail = update_unspsc(prod_detail,'prod_cat_id_id')
#             prod_detail = update_country(prod_detail)
#
#         if prod_detail_get_query.eform_id:
#             eform_detail, item_price, quantity_dictionary = get_eform_update_price(prod_detail_get_query.eform_id)
#
#             for data in eform_detail:
#                 data['eform_field_data'] = data['eform_field_data'].split('|~#')
#
#         if prod_detail_get_query.product_info_id:
#             product_specification = get_product_specification_details(prod_detail_get_query.product_info_id)
#         if item_price:
#             prod_detail['price'] = item_price
#
#     product_details['prod_detail'] = prod_detail
#
#     prod_img_detail = django_query_instance.django_filter_query(ImagesUpload,
#                                                                 {'client': global_variables.GLOBAL_CLIENT,
#                                                                  'image_id': product_id,
#                                                                  'image_type': CONST_CATALOG_IMAGE_TYPE
#                                                                  }, None, None)
#
#     # Add to recently viewed products
#     existing_product_query = django_query_instance.django_filter_only_query(RecentlyViewedProducts, {
#         'product_id': product_id,
#         'username': username,
#         'client': client,
#         'del_ind': False
#     })
#     if not existing_product_query.exists():
#         django_query_instance.django_create_query(RecentlyViewedProducts, {
#             'recently_viewed_prod_guid': guid_generator(),
#             'client': global_variables.GLOBAL_CLIENT,
#             'username': global_variables.GLOBAL_LOGIN_USERNAME,
#             'product_id': prod_detail['product_id'],
#             'catalog_id': prod_detail['prod_cat_id_id'],
#             'recently_viewed_prod_created_at': datetime.datetime.now(),
#             'recently_viewed_prod_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
#             'del_ind': False
#         })
#
#     recently_viewed_products_query = django_query_instance.django_filter_only_query(RecentlyViewedProducts, {
#         'username': username,
#         'client': client,
#         'del_ind': False
#     })
#
#     product_details['prod_img_detail'] = prod_img_detail
#     product_details['eform_detail'] = eform_detail
#     product_details['quantity_dictionary'] = quantity_dictionary
#     product_details['product_specification'] = product_specification
#     if existing_product_query.exists():
#         existing_product_query.update(recently_viewed_prod_changed_at=datetime.datetime.now(),
#                                       recently_viewed_prod_changed_by=username)
#         print(product_details)
#         return JsonResponse(product_details)
#
#     if recently_viewed_products_query.count() == CONST_USER_RECENTLY_VIEWED:
#         django_query_instance.django_filter_only_query(RecentlyViewedProducts, {
#             'username': username,
#             'client': client,
#             'del_ind': False
#         }).earliest('recently_viewed_prod_created_at').delete()
#
#     guid = guid_generator()
#     # django_query_instance.django_update_or_create_query(RecentlyViewedProducts, {'recently_viewed_prod_guid': guid}, {
#     #     'username': username,
#     #     'product_id': product_id,
#     #     'catalog_id': catalog_id,
#     #     'recently_viewed_prod_created_at': datetime.datetime.now(),
#     #     'recently_viewed_prod_created_by': username,
#     #     'recently_viewed_prod_changed_at': datetime.datetime.now(),
#     #     'recently_viewed_prod_changed_by': username,
#     #     'client_id': client,
#     # })
#     print(product_details)
#
#     return JsonResponse(product_details)

def get_product_service_prod_details(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    eform_detail = []
    product_specification = []
    quantity_dictionary = []
    item_price = None
    username = global_variables.GLOBAL_LOGIN_USERNAME
    client = global_variables.GLOBAL_CLIENT
    product_details = {}
    prod_id = json_obj.get_json_from_req(request)
    prod_detail = django_query_instance.django_filter_query(ProductsDetail,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'product_id': prod_id['prod_id']
                                                             },
                                                            None,
                                                            None)
    prod_detail_get_query = django_query_instance.django_get_query(ProductsDetail,
                                                                   {'client': global_variables.GLOBAL_CLIENT,
                                                                    'product_id': prod_id['prod_id']})
    for product in prod_detail:
        if django_query_instance.django_existence_check(SupplierMaster,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'supplier_id': product['supplier_id'],
                                                         'del_ind': False}):
            product['supplier_id'] = django_query_instance.django_filter_value_list_query(SupplierMaster,
                                                                                          {
                                                                                              'client': global_variables.GLOBAL_CLIENT,
                                                                                              'supplier_id': product[
                                                                                                  'supplier_id'],
                                                                                              'del_ind': False},
                                                                                          'name1')[0]
        if django_query_instance.django_existence_check(UnitOfMeasures,
                                                        {'uom_id': product['unit_id']}):
            product['unit'] = django_query_instance.django_filter_value_list_query(UnitOfMeasures,
                                                                                   {'uom_id': product['unit_id']},
                                                                                   'uom_description')[0]

    if prod_detail_get_query.variant_id:
        eform_detail, item_price, quantity_dictionary = get_eform_update_price(prod_detail_get_query)
    if prod_detail_get_query.product_info_id:
        product_specification = get_product_specification_details(prod_detail_get_query.product_id,
                                                                  prod_detail_get_query.product_info_id)
    if item_price:
        for product in prod_detail:
            product['price'] = item_price

    prod_img_detail = django_query_instance.django_filter_query(ImagesUpload,
                                                                {'client': global_variables.GLOBAL_CLIENT,
                                                                 'image_id': prod_id['prod_id'],
                                                                 'image_type': CONST_CATALOG_IMAGE_TYPE
                                                                 },
                                                                None,
                                                                None)

    product_details['prod_detail'] = prod_detail,
    product_details['prod_img_detail'] = prod_img_detail
    product_details['eform_detail'] = eform_detail
    product_details['quantity_dictionary'] = quantity_dictionary
    product_details['product_specification'] = product_specification

    # Add to recently viewed products
    recently_viewed_products_query = django_query_instance.django_filter_only_query(RecentlyViewedProducts, {
        'username': username,
        'client': client,
        'del_ind': False
    })

    existing_product_query = django_query_instance.django_filter_only_query(RecentlyViewedProducts, {
        'product_id': prod_id['prod_id'],
        'username': username,
        'client': client,
        'del_ind': False
    })

    if existing_product_query.exists():
        existing_product_query.update(recently_viewed_prod_changed_at=datetime.datetime.now(),
                                      recently_viewed_prod_changed_by=username)
        print(product_details)
        return JsonResponse(product_details)

    if recently_viewed_products_query.count() == CONST_USER_RECENTLY_VIEWED:
        django_query_instance.django_filter_only_query(RecentlyViewedProducts, {
            'username': username,
            'client': client,
            'del_ind': False
        }).earliest('recently_viewed_prod_created_at').delete()

    guid = guid_generator()
    django_query_instance.django_update_or_create_query(RecentlyViewedProducts, {'recently_viewed_prod_guid': guid}, {
        'username': username,
        'product_id': prod_id['prod_id'],
        'catalog_id': prod_id['catalog_id'],
        'recently_viewed_prod_created_at': datetime.datetime.now(),
        'recently_viewed_prod_created_by': username,
        'recently_viewed_prod_changed_at': datetime.datetime.now(),
        'recently_viewed_prod_changed_by': username,
        'client_id': client,
    })
    print(product_details)
    return JsonResponse(product_details)


def get_prod_details(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    username = global_variables.GLOBAL_LOGIN_USERNAME
    client = global_variables.GLOBAL_CLIENT
    product_specification = []
    product_detail = {}
    prod_id = json_obj.get_json_from_req(request)
    item_detail = get_item_detail(prod_id['prod_item_guid'])
    if django_query_instance.django_existence_check(ProductsDetail,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'product_id': prod_id['prod_id']}):
        product_detail['prod_detail'] = django_query_instance.django_filter_query(ProductsDetail, {
            'client': global_variables.GLOBAL_CLIENT,
            'product_id': prod_id['prod_id']
        }, None, None)
        product_detail['prod_detail'] = [update_unspsc(product_detail['prod_detail'][0], 'prod_cat_id_id')]
        product_detail['prod_detail'] = [update_country(product_detail['prod_detail'][0])]
        product_detail['prod_detail'] = [update_supplier_uom(product_detail['prod_detail'][0])]
        # product_detail['prod_detail'] = update_product_pricing(product_detail['prod_detail'])
        product_detail['prod_detail'][0]['price'] = item_detail.price
    prod_detail_get_query = django_query_instance.django_get_query(ProductsDetail,
                                                                   {'client': global_variables.GLOBAL_CLIENT,
                                                                    'product_id': prod_id['prod_id']})
    if item_detail.product_info_id:
        product_detail['product_specification'] = get_product_specification_details(item_detail.int_product_id,
                                                                                    item_detail.product_info_id)
    product_detail['prod_img_detail'] = django_query_instance.django_filter_query(ImagesUpload, {
        'client': global_variables.GLOBAL_CLIENT,
        'image_id': prod_id['prod_id'],
        'image_type': CONST_CATALOG_IMAGE_TYPE
    }, None, None)

    if item_detail:
        if item_detail.variant_id:
            filter_queue = Q(cart_guid=prod_id['prod_item_guid']) | Q(item_guid=prod_id['prod_item_guid']) | Q(
                po_item_guid=prod_id['prod_item_guid'])
            product_detail['variant_data'] = django_query_instance.django_queue_query(EformFieldData,
                                                                                      {
                                                                                          'client': global_variables.GLOBAL_CLIENT},
                                                                                      filter_queue,
                                                                                      None, None)

    # prod_cat_details = list(chain(prod_detail, product_specification, prod_img_detail))
    # Add to recently viewed products
    recently_viewed_products_query = django_query_instance.django_filter_only_query(RecentlyViewedProducts, {
        'username': username,
        'client': client,
        'del_ind': False
    })

    existing_product_query = django_query_instance.django_filter_only_query(RecentlyViewedProducts, {
        'product_id': prod_id['prod_id'],
        'username': username,
        'client': client,
        'del_ind': False
    })

    if existing_product_query.exists():
        existing_product_query.update(recently_viewed_prod_changed_at=datetime.datetime.now(),
                                      recently_viewed_prod_changed_by=username)
        return JsonResponse(product_detail, safe=False)

    if recently_viewed_products_query.count() == CONST_USER_RECENTLY_VIEWED:
        django_query_instance.django_filter_only_query(RecentlyViewedProducts, {
            'username': username,
            'client': client,
            'del_ind': False
        }).earliest('recently_viewed_prod_created_at').delete()

    guid = guid_generator()
    # django_query_instance.django_update_or_create_query(RecentlyViewedProducts, {'recently_viewed_prod_guid': guid}, {
    #     'username': username,
    #     'product_id': prod_id['prod_id'],
    #     'catalog_id': None,
    #     'recently_viewed_prod_created_at': datetime.datetime.now(),
    #     'recently_viewed_prod_created_by': username,
    #     'recently_viewed_prod_changed_at': datetime.datetime.now(),
    #     'recently_viewed_prod_changed_by': username,
    #     'client_id': client,
    # })
    print(product_detail)
    return JsonResponse(product_detail, safe=False)


def get_image_detail(request):
    """

    :param request:
    :return:
    """
    update_user_info(request)
    prod_id = json_obj.get_json_from_req(request)
    prod_img_detail = django_query_instance.django_filter_only_query(ImagesUpload, {
        'client': global_variables.GLOBAL_CLIENT,
        'image_id': str(prod_id),
        'image_type': CONST_CATALOG_IMAGE_TYPE
    })

    return json_obj.get_json_from_obj(prod_img_detail)


def auto_completion_search(request):
    """

    :param request:
    :return:
    """
    titles = list()
    if 'term' in request.GET:
        update_user_info(request)
        search_value = request.GET.get('term')
        global_variables.GLOBAL_PROD_SEARCH_TYPE = request.GET.get('prod_search_type')
        search_type = request.GET.get('search_type')
        search_id = request.GET.get('search_id')
        selected_catalog = request.GET.get('selected_catalog')
        login_user_catalog_id_list = get_catalog_id_list(selected_catalog)
        product_id_list = get_catalog_mapping_product_id_list(login_user_catalog_id_list)
        if global_variables.GLOBAL_PROD_SEARCH_TYPE in ['PRODUCTS', 'ALL']:
            prod_detail_search = get_product_based_product_details_search_type(login_user_catalog_id_list, search_value,
                                                                               search_type, search_id)
            for product in prod_detail_search:
                titles.append(product['short_desc'])
            if global_variables.GLOBAL_PROD_SEARCH_TYPE == 'ALL':
                prod_detail_search = get_freetext_detail(login_user_catalog_id_list, search_value, search_type,
                                                         search_id)
                for product in prod_detail_search:
                    titles.append(product['description'])
        if global_variables.GLOBAL_PROD_SEARCH_TYPE == 'CATEGORIES':
            prod_cat_list = list(ProductsDetail.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                                               product_id__in=product_id_list).values_list(
                'prod_cat_id', flat=True).distinct())
            prod_detail_search = UnspscCategoriesCustDesc.objects.filter(Q(client=global_variables.GLOBAL_CLIENT) &
                                                                         Q(category_desc__icontains=search_value) &
                                                                         Q(prod_cat_id__in=prod_cat_list))
            for product in prod_detail_search:
                titles.append(product.category_desc)
        if global_variables.GLOBAL_PROD_SEARCH_TYPE == 'SUPPLIERS':
            supplier_list = list(ProductsDetail.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                                               product_id__in=product_id_list).values_list(
                'supplier_id', flat=True).distinct())

            prod_detail_search = SupplierMaster.objects.filter((Q(client=global_variables.GLOBAL_CLIENT) &
                                                                Q(supplier_id__in=supplier_list)) &
                                                               Q(name1__icontains=search_value))
            for product in prod_detail_search:
                titles.append(product.name1)
        if global_variables.GLOBAL_PROD_SEARCH_TYPE == 'FREETEXT':
            prod_detail_search = get_freetext_detail(login_user_catalog_id_list, search_value, search_type, search_id)
            for product in prod_detail_search:
                titles.append(product['description'])
        # titles = [product.title for product in prod_detail_search]
        return JsonResponse(titles, safe=False)
    return render(request, 'Catalog/products_services_catalog.html', {'is_slide_menu': True})

# def get_search_result(request, selected_catalog,document_number=None):
#     """
#
#     :param request:
#     :return:
#     """
#     update_user_info(request)
#     context = get_search_result_list (request.POST.get('hg_cat_search_txt'),selected_catalog)
#
#     return render(request, 'Catalog/products_services_catalog.html', context)
