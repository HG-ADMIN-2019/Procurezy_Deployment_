from django.http import JsonResponse
from django.shortcuts import render

from eProc_Basic.Utilities.constants.constants import CONST_UNSPSC_IMAGE_TYPE, CONST_SEARCH_COUNT, CONST_FREETEXT_CALLOFF, \
    CONST_CATALOG_CALLOFF
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import encrypt
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Catalog.Utilities.catalog_generic import CatalogGenericMethods
from eProc_Catalog.Utilities.catalog_specific import CatalogManagement
from eProc_Configuration.models import UnitOfMeasures, Currency, Country, Languages, UnspscCategoriesCustDesc, \
    UnspscCategoriesCust, ProductsDetail, Catalogs, SupplierMaster, UnspscCategories, ImagesUpload, CatalogMapping
from eProc_Content_Search.Utilities.content_search_generic import product_detail_search, get_product_detail_filter_list, \
    catalog_search
from eProc_Manage_Content.Utilities.manage_content_specific import get_catalog_filter_list, get_product_detail_config, \
    update_prod_detail
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Shopping_Cart.models import CartItemDetails, ScItem

django_query_instance = DjangoQueries()


def upload_catalog(request):
    client = getClients(request)
    my_list = CatalogManagement.get_catalogs_not_used()
    upload_catalog = django_query_instance.django_filter_query(Catalogs, {'client': client, 'del_ind': False},
                                                               None, ['catalog_guid', 'catalog_id', 'name',
                                                                      'description', 'product_type'])
    content_managment_settings = 'content_managment_settings'

    return render(request, 'ManageContent/upload_catalog.html',
                  {'upload_catalog': upload_catalog, 'my_list': my_list,
                   'content_managment_settings': content_managment_settings})


def product_and_service_config(request):
    """

    """
    product_id = ''
    client = getClients(request)
    update_user_info(request)
    product_details_query = []
    if request.method == 'GET':
        product_details_query = get_product_detail_config()

    elif request.is_ajax():
        item_details = JsonParser().get_json_from_req(request)
        product_details_query = product_detail_search(**item_details)
        update_prod_detail(product_details_query)
        return JsonResponse(product_details_query, safe=False)

    supp_data = django_query_instance.django_filter_query(SupplierMaster, {'client': client, 'del_ind': False},
                                                          None, ['supplier_id', 'name1'])

    get_units = django_query_instance.django_filter_query(UnitOfMeasures,
                                                          {'del_ind': False}, None, ['uom_id', 'uom_description'])

    currency_list = django_query_instance.django_filter_query(Currency,
                                                              {'del_ind': False}, None, ['currency_id', 'description'])

    country_list = django_query_instance.django_filter_query(Country,
                                                             {'del_ind': False}, None, ['country_code', 'country_name'])

    language_list = django_query_instance.django_filter_query(Languages,
                                                              {'del_ind': False}, None, ['language_id', 'description'])
    catalogs_list = list(CatalogGenericMethods.catalog_list())
    unspsc_list = django_query_instance.django_filter_query(UnspscCategoriesCustDesc,
                                                            {'del_ind': False}, None, ['prod_cat_id', 'category_desc'])

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_content_mgmnt_active': True,
        'product_details_query': product_details_query,
        'supp_data': supp_data,
        'get_units': get_units,
        'currency_list': currency_list,
        'country_list': country_list,
        'language_list': language_list,
        'catalogs_list': catalogs_list,
        'unspsc_list': unspsc_list,
    }
    return render(request,
                  'ManageContent/product_details_config.html', context)


def catalog_config(request):
    """

    """
    update_user_info(request)
    catalog_query = []
    if request.method == 'GET':
        filter_query = {'client': global_variables.GLOBAL_CLIENT, 'del_ind': False}
        catalog_query = get_catalog_filter_list(filter_query, 10)
    elif request.is_ajax():
        catalog_details = JsonParser().get_json_from_req(request)
        product_details_query = catalog_search(**catalog_details)
        return JsonResponse(product_details_query, safe=False)

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_content_mgmnt_active': True,
        'catalog_query': catalog_query
    }
    return render(request,
                  'ManageContent/catalog_config.html', context)




