import re
from gettext import Catalog

from django.db.models import Q

from eProc_Basic.Utilities.constants.constants import CONST_CATALOG_IMAGE_TYPE, CONST_SEARCH_COUNT, CONST_CATALOG_CALLOFF
from eProc_Basic.Utilities.functions.django_q_query import django_q_query
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import SupplierMaster, UnspscCategoriesCustDesc, ProductsDetail, Catalogs, ImagesUpload, \
    FreeTextDetails, CatalogMapping
from eProc_Shopping_Cart.models import ScItem

django_query_instance = DjangoQueries()


def get_product_detail_filter_list(filter_query, query_count):
    """

    """
    product_details_query = django_query_instance.django_filter_query_with_entry_count(ProductsDetail,
                                                                                       filter_query,
                                                                                       ['product_id'],
                                                                                       ['product_id', 'short_desc',
                                                                                        'supplier_id',
                                                                                        'lead_time', 'unit', 'price',
                                                                                        'currency',
                                                                                        'long_desc', 'catalog_item',
                                                                                        'prod_type',
                                                                                        'price_on_request',
                                                                                        'price_unit', 'manufacturer',
                                                                                        'manu_part_num',
                                                                                        'brand', 'quantity_avail',
                                                                                        'quantity_min',
                                                                                        'offer_key',
                                                                                        'country_of_origin', 'language',
                                                                                        'cust_prod_cat_id', 'search_term1',
                                                                                        'search_term2',
                                                                                        'prod_cat_id'], query_count)

    for product_id in product_details_query:

        if django_query_instance.django_existence_check(ImagesUpload, {'client': global_variables.GLOBAL_CLIENT, 'image_default': True, 'image_id': product_id['product_id'], 'image_type': CONST_CATALOG_IMAGE_TYPE, 'del_ind': False}):
            product_id['image_url'] = django_query_instance.django_filter_value_list_ordered_by_distinct_query(ImagesUpload, {
                'client': global_variables.GLOBAL_CLIENT, 'image_default': True, 'image_id': product_id['product_id'],
                'image_type': CONST_CATALOG_IMAGE_TYPE, 'del_ind': False
            }, 'image_url', None)[0]

        else:
            product_id['image_url'] = ""

        # Check if product is mapped in catalog
        check_product_mapped_in_catalog(product_id)
        # Check if product exists in catalog
        check_product_exist_in_transaction_table(product_id)

    return product_details_query


def product_detail_search(**kwargs):
    """

    """
    supp_query = Q()
    product_id_query = Q()
    product_category_query = Q()
    short_desc_query = Q()
    search_term1_query = Q()
    search_term2_query = Q()
    products_detail_source_system_query = Q()
    instance = ProductsDetail()
    search_count = 10
    for key, value in kwargs.items():
        value_list = []
        if value:
            if key == 'supplier_name':
                supp_query = get_supplier_id(value)
            if key == 'product_category':
                product_category_query = get_product_category_id(value)
            if key == 'product_id':
                if '*' not in value:
                    value_list = [value]
                product_id_query = django_q_query(value, value_list, 'product_id')
            if key == 'product_desc':
                if '*' not in value:
                    value_list = [value]
                short_desc_query = django_q_query(value, value_list, 'short_desc')
            if key == 'search_term1':
                if '*' not in value:
                    value_list = [value]
                search_term1_query = django_q_query(value, value_list, 'search_term1')
            if key == 'search_term2':
                if '*' not in value:
                    value_list = [value]
                search_term2_query = django_q_query(value, value_list, 'search_term2')
            if key == 'source_system':
                if '*' not in value:
                    value_list = [value]
                products_detail_source_system_query = django_q_query(value, value_list, 'products_detail_source_system')
            if key == 'search_count':
                search_count = int(value)

    product_details_query = list(instance.get_product_details_by_fields(global_variables.GLOBAL_CLIENT,
                                                                        instance,
                                                                        supp_query,
                                                                        product_category_query,
                                                                        product_id_query,
                                                                        short_desc_query,
                                                                        search_term1_query,
                                                                        search_term2_query,
                                                                        products_detail_source_system_query,
                                                                        search_count))

    for product_id in product_details_query:

        if django_query_instance.django_existence_check(ImagesUpload, {'client': global_variables.GLOBAL_CLIENT, 'image_default': True, 'image_id': product_id['product_id'], 'image_type': CONST_CATALOG_IMAGE_TYPE, 'del_ind': False}):
            product_id['image_url'] = django_query_instance.django_filter_value_list_ordered_by_distinct_query(ImagesUpload, {
                'client': global_variables.GLOBAL_CLIENT, 'image_default': True, 'image_id': product_id['product_id'],
                'image_type': CONST_CATALOG_IMAGE_TYPE, 'del_ind': False
            }, 'image_url', None)[0]

        else:
            product_id['image_url'] = ""

        # Check if product is mapped in catalog
        check_product_mapped_in_catalog(product_id)
        # Check if product exists in catalog
        check_product_exist_in_transaction_table(product_id)

    print(product_details_query)
    return product_details_query


def get_supplier_id(value):
    """"
    """

    supp_list = SupplierMaster.get_suppid_by_first_name(value)
    if '*' not in value:
        supp_list.append(value)
    supp_query = django_q_query(value, supp_list, 'supplier_id')
    return supp_query


def get_product_category_id(filter_value):
    """

    """
    prod_cat_id_query = {}
    prod_cat_id_list = get_prod_cat_search_query(filter_value)
    prod_cat_id_query = django_q_query(filter_value, prod_cat_id_list, 'prod_cat_id__prod_cat_id')

    return prod_cat_id_query


def get_prod_cat_search_query(filter_value):
    """

    """
    prod_cat_id_query = {}
    prod_cat_id_list = UnspscCategoriesCustDesc.get_prod_cat_by_desc(filter_value)
    if '*' not in filter_value:
        prod_cat_id_list.append(filter_value)
    return prod_cat_id_list


def get_product_id_list(filter_value):
    """

    """
    product_id_query = django_q_query(filter_value, [filter_value], 'product_id')

    return product_id_query


def catalog_search(**kwargs):
    """

    """
    catalog_id_query = Q()
    catalog_desc_query = Q()
    catalog_name_query = Q()
    product_type_query = Q()
    instance = Catalogs()
    search_count = 10
    for key, value in kwargs.items():
        value_list = []
        if value:
            if '*' not in value:
                value_list = [value]
            if key == 'catalog_id':
                catalog_id_query = django_q_query(value, value_list, 'catalog_id')
            if key == 'catalog_desc':
                catalog_desc_query = django_q_query(value, value_list, 'description')
            if key == 'catalog_name':
                catalog_name_query = django_q_query(value, value_list, 'name')
            if key == 'product_type':
                product_type_query = django_q_query(value, value_list, 'prod_type')
            if key == 'search_count':
                search_count = int(value)

    product_details_query = list(instance.get_catalog_fields(global_variables.GLOBAL_CLIENT,
                                                             catalog_id_query,
                                                             catalog_desc_query,
                                                             catalog_name_query,
                                                             product_type_query,
                                                             search_count))
    return product_details_query


def freetext_search(**kwargs):
    """

    """
    supp_query = Q()
    freetext_id_query = Q()
    product_category_query = Q()
    short_desc_query = Q()
    search_count = CONST_SEARCH_COUNT
    for key, value in kwargs.items():
        value_list = []
        if value:
            if key == 'supplier_id':
                supp_query = get_supplier_id(value)
            if key == 'prod_cat_id':
                product_category_query = get_prod_cat_search_query(value)
                product_category_query = django_q_query(value, product_category_query, 'prod_cat_id')
                # product_category_query = get_product_category_id(value)
            if key == 'form_id':
                if '*' not in value:
                    value_list = [value]
                freetext_id_query = django_q_query(value, value_list, 'freetext_id')
            if key == 'description':
                if '*' not in value:
                    value_list = [value]
                short_desc_query = django_q_query(value, value_list, 'description')
            if key == 'search_count':
                search_count = int(value)

    freetext_details_query = list(FreeTextDetails.objects.filter(supp_query, product_category_query,
                                                  freetext_id_query,
                                                  short_desc_query, client=global_variables.GLOBAL_CLIENT,
                                                  del_ind=False).values('freetext_id', 'supp_product_id', 'supplier_id',
                                                                        'lead_time', 'description',
                                                                        'prod_cat_id').order_by('freetext_id')[:int(search_count)])
    return freetext_details_query


def check_product_mapped_in_catalog(product_id):
    if django_query_instance.django_existence_check(CatalogMapping, {'client': global_variables.GLOBAL_CLIENT,
                                                                     'call_off': CONST_CATALOG_CALLOFF,
                                                                     'item_id': product_id['product_id'],
                                                                     'del_ind': False}):
        product_id['mapped_in_catlog'] = True

    else:
        product_id['mapped_in_catlog'] = False
    return


def check_product_exist_in_transaction_table(product_id):
    if django_query_instance.django_existence_check(ScItem, {'client': global_variables.GLOBAL_CLIENT,
                                                             'call_off': CONST_CATALOG_CALLOFF,
                                                             'int_product_id': product_id['product_id'],
                                                             'del_ind': False}):
        product_id['exist_in_transaction_table'] = True

    else:
        product_id['exist_in_transaction_table'] = False
