from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import SupplierMaster, OrgPorg
from eProc_Basic.Utilities.functions.django_q_query import django_q_query
from eProc_Supplier_Order_Management.models.supplier_order_management_models import SOMPoHeader, \
    get_som_po_details_by_fields
from eProc_Suppliers.models import OrgSuppliers

django_query_instance = DjangoQueries()


class Supplier:
    def __init__(self):
        self.client = global_variables.GLOBAL_CLIENT

    def get_supplier_detail_by_id(self, supplier_id):
        try:
            return django_query_instance.django_get_query(SupplierMaster, {
                'client': self.client, 'del_ind': False, 'supplier_id': supplier_id
            })

        except ObjectDoesNotExist:
            return None

    def filter_supplier_query(self, filter_dictionary):
        filter_dictionary['del_ind'] = False
        filter_dictionary['client'] = self.client

        return django_query_instance.django_filter_only_query(SupplierMaster, filter_dictionary)

    def supplier_get_query(self, get_based_on):
        try:
            get_based_on['del_ind'] = False
            get_based_on['client'] = self.client

            return django_query_instance.django_get_query(SupplierMaster, get_based_on)

        except ObjectDoesNotExist:
            return None


def supplier_detail_search(**kwargs):
    """

    """
    search_query = {}
    block = False
    client = global_variables.GLOBAL_CLIENT
    name1_query = Q()
    name2_query = Q()
    supplier_id_query = Q()
    email_query = Q()
    supp_type_query = Q()
    country_code_query = Q()
    org_supplier_query = Q()
    city_query = Q()
    instance = SupplierMaster()
    purch_org_list = django_query_instance.django_filter_value_list_query(OrgPorg, {
        'client': global_variables.GLOBAL_CLIENT,
        'del_ind': False, }, 'porg_id')
    porg_array = []
    for porg in purch_org_list:
        if porg != '*':
            porg_array.append(porg)

    for key, value in kwargs.items():
        value_list = []
        if value:
            if key == 'purchasing_org':
                if '*' not in value:
                    value_list = [value]
                if value == '*':
                    value_list = porg_array
                org_supplier_query = django_q_query(value, value_list, 'porg_id')
                supplier_id_query = django_query_instance.django_queue_query_value_list(OrgSuppliers, {
                    'client': global_variables.GLOBAL_CLIENT,
                    'del_ind': False}, org_supplier_query, 'supplier_id')
                supplier_id_query = django_q_query(None, supplier_id_query, 'supplier_id')
            if key == 'name1':
                if '*' not in value:
                    value_list = [value]
                name1_query = django_q_query(value, value_list, 'name1')
            if key == 'name2':
                if '*' not in value:
                    value_list = [value]
                name2_query = django_q_query(value, value_list, 'name2')
            if key == 'supplier_id':
                if '*' not in value:
                    value_list = [value]
                supplier_id_query = django_q_query(value, value_list, 'supplier_id')
            if key == 'email':
                if '*' not in value:
                    value_list = [value]
                email_query = django_q_query(value, value_list, 'email')
            if key == 'supplier_type':
                if '*' not in value:
                    value_list = [value]
                supp_type_query = django_q_query(value, value_list, 'supp_type')
            if key == 'country_code':
                if '*' not in value:
                    value_list = [value]
                country_code_query = django_q_query(value, value_list, 'country_code')
            if key == 'city':
                if '*' not in value:
                    value_list = [value]
                city_query = django_q_query(value, value_list, 'city')

            if key == 'block':
                if value == 'on':
                    block = True
                else:
                    block = False

    supplier_details_query = list(instance.get_supplier_details_by_fields(client,
                                                                          block,
                                                                          instance,
                                                                          name1_query,
                                                                          name2_query,
                                                                          supplier_id_query,
                                                                          email_query,
                                                                          supp_type_query,
                                                                          country_code_query,
                                                                          city_query
                                                                          ))

    return supplier_details_query


def get_supplier_email(supplier_id):
    """

    """
    supplier_email_addr = ''
    if django_query_instance.django_existence_check(SupplierMaster,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'supplier_id': supplier_id,
                                                     'del_ind': False}):
        supplier_detail = django_query_instance.django_get_query(SupplierMaster,
                                                                 {'client': global_variables.GLOBAL_CLIENT,
                                                                  'supplier_id': supplier_id,
                                                                  'del_ind': False})
        supplier_email_addr = supplier_detail.email

    return supplier_email_addr


def som_po_search(**kwargs):
    """

    """
    search_query = {}
    block = False
    client = global_variables.GLOBAL_CLIENT
    doc_number = Q()
    name2_query = Q()
    supplier_id_query = Q()
    search_term1_query = Q()
    search_term2_query = Q()
    country_code_query = Q()
    org_supplier_query = Q()
    city_query = Q()

    for key, value in kwargs.items():
        value_list = []
        if value:
            if key == 'po_number':
                if '*' not in value:
                    value_list = [value]
                doc_number = django_q_query(value, value_list, 'doc_number')
            if key == 'company_name':
                if '*' not in value:
                    value_list = [value]
                doc_number = django_q_query(value, value_list, 'requester_company_name')
            if key == 'received_date':
                if '*' not in value:
                    value_list = [value]
                doc_number = django_q_query(value, value_list, 'ordered_at')
            if key == 'buyer_phone_num':
                if '*' not in value:
                    value_list = [value]
                doc_number = django_q_query(value, value_list, 'requester_mobile_num')
            if key == 'buyer_name':
                if '*' not in value:
                    value_list = [value]
                doc_number = django_q_query(value, value_list, 'requester')
            if key == 'buyer_email_id':
                if '*' not in value:
                    value_list = [value]
                doc_number = django_q_query(value, value_list, 'requester_email')
    som_po_data = get_som_po_details_by_fields(doc_number)
    return som_po_data
