from django.http import JsonResponse
from django.shortcuts import render
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import encrypt
from eProc_Basic.Utilities.functions.get_db_query import get_country_id, getClients
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.messages_config import get_message_desc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import SupplierMaster, SupplierMasterHistory
from eProc_Registration.models import UserData
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Shopping_Cart.models import ScItem, CartItemDetails
from eProc_Suppliers.Utilities.supplier_generic import supplier_detail_search
from eProc_Suppliers.Utilities.supplier_specific import update_block_status, get_supplier_data
from eProc_Suppliers.models import OrgSuppliers, OrgSuppliersHistory

JsonParser_obj = JsonParser()
django_query_instance = DjangoQueries()


def delete_supplier(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    supplier_data = JsonParser_obj.get_json_from_req(request)
    success_message = ''
    for supplier_id in supplier_data['data']:
        if django_query_instance.django_existence_check(SupplierMaster,
                                                        {'supplier_id': supplier_id,
                                                         'client': global_variables.GLOBAL_CLIENT,
                                                         'del_ind': False}) and not \
                django_query_instance.django_existence_check(OrgSuppliers,
                                                             {'supplier_id': supplier_id,
                                                              'client': global_variables.GLOBAL_CLIENT,
                                                              'del_ind': False}):
            create_supplier_history_data(supplier_id)
            django_query_instance.django_filter_delete_query(SupplierMaster,
                                                             {'supplier_id': supplier_id,
                                                              'client': global_variables.GLOBAL_CLIENT,
                                                              'del_ind': False})
            success_message = get_message_desc('MSG206')[1]
        if django_query_instance.django_existence_check(SupplierMaster,
                                                        {'supplier_id': supplier_id,
                                                         'client': global_variables.GLOBAL_CLIENT,
                                                         'del_ind': False}):
            if django_query_instance.django_existence_check(OrgSuppliers,
                                                            {'supplier_id': supplier_id,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'del_ind': False}):
                # create_Orgsupplier_history_data(supplier_id)
                django_query_instance.django_filter_delete_query(OrgSuppliers,
                                                                 {'supplier_id': supplier_id,
                                                                  'client': global_variables.GLOBAL_CLIENT,
                                                                  'del_ind': False})
                create_supplier_history_data(supplier_id)
                django_query_instance.django_filter_delete_query(SupplierMaster,
                                                                 {'supplier_id': supplier_id,
                                                                  'client': global_variables.GLOBAL_CLIENT,
                                                                  'del_ind': False})
                success_message = get_message_desc('MSG206')[1]

    supplier_results = get_supplier_data()
    response = {'supplier_results': supplier_results, 'success_message': success_message}
    return JsonResponse(response, safe=False)


def supplier_blocking(request):
    """

    """
    update_user_info(request)
    supplier_block_data = JsonParser_obj.get_json_from_req(request)
    update_block_status(supplier_block_data)
    response = {'success_message': "Changed Successfully"}

    return JsonResponse(response, safe=False)


def create_supplier_history_data(supplier_id):
    supplier_info = django_query_instance.django_filter_query(SupplierMaster,
                                                              {'supplier_id': supplier_id,
                                                               'del_ind': False}, None, None)
    # supplier_db_dictionary = {'supp_guid': '706BCF6B3053410CA78A555C1CB6D5B7', 'supplier_id': '186678',
    # 'supp_type': 'one_time ', 'name1': 'test', 'name2': 'test', 'supplier_username': None, 'city': 'Bangalore',
    # 'postal_code': '560041', 'street': '24th main 38th cross, jayanagar 4th T block', 'landline': '07406661881',
    # 'mobile_num': '9844067292', 'fax': '', 'email': 'chaitrakiran04@gmail.com', 'email1': None, 'email2': None,
    # 'email3': None, 'email4': None, 'email5': None, 'output_medium': 'email', 'search_term1': 'demo',
    # 'search_term2': 'demo', 'duns_number': '', 'block_date': None, 'block': False, 'delivery_days': '5,6',
    # 'is_active': True, 'registration_number': 'hu77789', 'company_id': '', 'supplier_master_created_by': None,
    # 'supplier_master_created_at': None, 'supplier_master_changed_by': None, 'supplier_master_changed_at': None,
    # 'supplier_master_source_system': '', 'pref_routing': None, 'lock_date': None, 'global_duns': None,
    # 'domestic_duns': None, 'ics_code': None, 'internal_ind': False, 'sba_code': None, 'ethnicity': None,
    # 'hubzone': None, 'no_vend_text': False, 'agr_reg_no': None, 'no_mult_addr': False, 'del_ind': False,
    # 'client_id': '100', 'country_code_id': 'IN', 'currency_id_id': 'INR', 'language_id_id': 'EN'} }
    client_val = supplier_info[0]['client_id']
    country_val = supplier_info[0]['country_code_id']
    currency_val = supplier_info[0]['currency_id_id']
    language_val = supplier_info[0]['language_id_id']
    if 'client_id'  in supplier_info[0]:
        del supplier_info[0]['client_id']
    if 'country_code_id' in supplier_info[0]:
        del supplier_info[0]['country_code_id']
    if 'currency_id_id' in supplier_info[0]:
        del supplier_info[0]['currency_id_id']
    if 'language_id_id' in supplier_info[0]:
        del supplier_info[0]['language_id_id']
    supplier_info.append({'client': client_val, 'country_code': country_val, 'currency_id': currency_val, 'language_id': language_val})

    django_query_instance.django_create_query(SupplierMasterHistory, supplier_info[0])


def create_Orgsupplier_history_data(supplier_id):
    supplier_info = django_query_instance.django_filter_query(OrgSuppliers,
                                                              {'supplier_id': supplier_id,
                                                               'del_ind': False}, None, None)
    for supplier in supplier_info:
        django_query_instance.django_create_query(OrgSuppliersHistory, supplier)
