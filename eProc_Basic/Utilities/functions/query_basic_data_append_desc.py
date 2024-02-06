from eProc_Attributes.Utilities.attributes_specific import append_description_atrr_value_exists
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.insert_remove import dictionary_remove_insert_first
from eProc_Basic.Utilities.functions.query_append_id_desc import AppendIdDesc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import *

django_query_instance = DjangoQueries()


def get_supplier_append_desc_data(default_supplier_id):
    supplier_desc = AppendIdDesc().query_append_id_desc_language(SupplierMaster,
                                                                 {'del_ind': False,
                                                                  'client': global_variables.GLOBAL_CLIENT},
                                                                 {'del_ind': False,
                                                                  'language_id': global_variables.GLOBAL_USER_LANGUAGE},
                                                                 'supplier_id', 'name1',
                                                                 default_supplier_id)
    return supplier_desc


def get_uom_append_desc_data(default_uom):
    unit_desc = AppendIdDesc().query_append_id_desc(UnitOfMeasures,
                                                    {'del_ind': False}, 'uom_id', 'uom_description',
                                                    default_uom)
    return unit_desc


def get_currency_append_desc_data(default_currency):
    currency_desc = AppendIdDesc().query_append_id_desc(Currency,
                                                        {'del_ind': False}, 'currency_id', 'description',
                                                        default_currency)
    return currency_desc


def get_country_append_desc_data(default_country_id):
    country_desc = AppendIdDesc().query_append_id_desc(Country,
                                                       {'del_ind': False}, 'country_code', 'country_name',
                                                       default_country_id)
    return country_desc


def get_language_append_desc_data(default_language):
    language_desc = AppendIdDesc().query_append_id_desc(Languages,
                                                        {'del_ind': False}, 'language_id', 'description',
                                                        default_language)
    return language_desc


def get_unspsc_append_desc_data(language, default_unspsc):
    """

    """
    prod_cat_cust = django_query_instance.django_filter_value_list_query(UnspscCategoriesCust, {
        'client': global_variables.GLOBAL_CLIENT
    }, 'prod_cat_id')
    prod_cat_cust_desc = django_query_instance.django_filter_query(UnspscCategoriesCustDesc, {
        'prod_cat_id__in': prod_cat_cust,
        'language_id': language,
        'client': global_variables.GLOBAL_CLIENT
    }, None, ['prod_cat_id', 'category_desc'])
    django_query_set_result = dictionary_remove_insert_first(prod_cat_cust_desc, 'prod_cat_id', default_unspsc)
    append_value_desc = append_description_atrr_value_exists(django_query_set_result,
                                                             prod_cat_cust,
                                                             'prod_cat_id',
                                                             'category_desc')[0]
    return append_value_desc


def catalog_append_desc_data(default_catalog_id):
    catalog_desc = AppendIdDesc().query_append_id_desc(Catalogs,
                                                       {'del_ind': False,
                                                        'is_active_flag': True,
                                                        'client': global_variables.GLOBAL_CLIENT},
                                                       'catalog_id', 'description',
                                                       default_catalog_id)
    return catalog_desc


def get_basic_data(country_of_origin_id, currency_id, unit_id, language_id, supplier_id, unspsc, requester_language):
    country_desc = get_country_append_desc_data(country_of_origin_id)
    currency_desc = get_currency_append_desc_data(currency_id)
    unit_desc = get_uom_append_desc_data(unit_id)
    language_desc = get_language_append_desc_data(language_id)
    supplier_desc = get_supplier_append_desc_data(supplier_id)
    # catalog_desc = catalog_append_desc_data(catalog_id)
    unspsc_desc = get_unspsc_append_desc_data(requester_language, unspsc)
    return country_desc, currency_desc, unit_desc, language_desc, supplier_desc, unspsc_desc
