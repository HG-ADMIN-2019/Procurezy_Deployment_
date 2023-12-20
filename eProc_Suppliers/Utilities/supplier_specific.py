from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import encrypt
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import SupplierMaster, Country
from eProc_Suppliers.Utilities.supplier_generic import Supplier
from eProc_Suppliers.models import OrgSuppliers

django_query_instance = DjangoQueries()


def get_sup_list_by_input(request):
    supplier_instance = Supplier()
    inp_supp_id = request.POST.get('supplier_id')
    inp_srch1 = request.POST.get('search_term1')
    inp_srch2 = request.POST.get('search_term2')
    inp_first_name = request.POST.get('first_name')
    inp_last_name = request.POST.get('last_name')
    inp_country = request.POST.get('country')
    inp_city = request.POST.get('city')

    args_list = {}

    if inp_supp_id is not None and inp_supp_id != '':
        args_list['supplier_id'] = inp_supp_id

    if inp_srch1 is not None and inp_srch1 != '':
        args_list['search_term1'] = inp_srch1

    if inp_srch2 is not None and inp_srch2 != '':
        args_list['search_term2'] = inp_srch2

    if inp_first_name is not None and inp_first_name != '':
        args_list['name1'] = inp_first_name

    if inp_last_name is not None and inp_last_name != '':
        args_list['name2'] = inp_last_name

    if inp_country is not None and inp_country != '':
        args_list['country_code'] = inp_country

    if inp_city is not None and inp_city != '':
        args_list['city'] = inp_city

    result = supplier_instance.filter_supplier_query(args_list)

    return result


def update_block_status(supplier_block_data):
    """

    """
    if django_query_instance.django_existence_check(OrgSuppliers,
                                                    {'supplier_id': supplier_block_data['supplier_id'],
                                                     'client': global_variables.GLOBAL_CLIENT,
                                                     'del_ind': False}):
        django_query_instance.django_update_query(OrgSuppliers,
                                                  {'supplier_id': supplier_block_data['supplier_id'],
                                                   'client': global_variables.GLOBAL_CLIENT,
                                                   'del_ind': False},
                                                  {'purch_block': supplier_block_data['flag']})
    django_query_instance.django_update_query(SupplierMaster,
                                              {'supplier_id': supplier_block_data['supplier_id'],
                                               'client': global_variables.GLOBAL_CLIENT,
                                               'del_ind': False},
                                              {'block': supplier_block_data['flag']})


def get_supplier_data():
    """

    """
    supplier_results = django_query_instance.django_filter_query(SupplierMaster,
                                                                 {'client': global_variables.GLOBAL_CLIENT,
                                                                  'del_ind': False,
                                                                  'block': False}, ['supplier_id'], None)
    supplier_results = update_country_encrypt(supplier_results)
    return supplier_results


def update_country_encrypt(supplier_results):
    """

    """
    country_dictionary_list = django_query_instance.django_filter_query(Country,
                                                                        None, None, ['country_code', 'country_name'])
    for supplier in supplier_results:
        for country_dictionary in country_dictionary_list:
            if supplier['country_code_id'] == country_dictionary['country_code']:
                supplier['country_code_id'] = country_dictionary['country_name']
        supplier['supplier_id_encrypted'] = encrypt(supplier['supplier_id'])
    return supplier_results
