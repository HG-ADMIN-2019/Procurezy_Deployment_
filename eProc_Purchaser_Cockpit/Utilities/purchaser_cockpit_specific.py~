from datetime import datetime
import re

# from asn1crypto.core import Null
from django.db.models import Q

from eProc_Basic.Utilities.constants.constants import CONST_SC_HEADER_ORDERED, CONST_SC_HEADER_APPROVED
from eProc_Basic.Utilities.functions.django_q_query import django_q_query
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import OrgCompanies
from eProc_Doc_Search_and_Display.Utilities.search_display_generic import get_hdr_data
from eProc_Purchase_Order.models import PoHeader
from eProc_Shopping_Cart.models import ScItem, ScHeader
from eProc_Supplier_Order_Management.models import get_som_po_details_by_fields

django_query_instance = DjangoQueries()


def filter_based_on_sc_item_field(client, order_list):
    """

    :param client:
    :param order_list:
    :return:
    """
    sc_header_item_details = []
    sc_header_list = django_query_instance.django_filter_value_list_query(ScHeader,
                                                                          {'client': global_variables.GLOBAL_CLIENT,
                                                                           'status': CONST_SC_HEADER_ORDERED,
                                                                           'ordered_at': datetime.today()},
                                                                          'guid')
    sc_item_details = django_query_instance.django_filter_only_query(ScItem,
                                                                     {'client': client, 'source_relevant_ind': True,
                                                                      'po_doc_num': None,
                                                                      'call_off__in': ['01', '02']
                                                                      }).order_by(
        *order_list)
    for sc_item in sc_item_details:
        guid = sc_item.header_guid_id
        scheader_details = django_query_instance.django_filter_only_query(ScHeader,
                                                                          {'guid': guid,
                                                                           'client': client,
                                                                           'status': CONST_SC_HEADER_APPROVED,
                                                                           }).values('doc_number')
        for scheader_detail in scheader_details:
            sc_header_item_detail = [scheader_detail['doc_number'], sc_item.description, sc_item.supplier_id,
                                     sc_item.comp_code, sc_item.item_del_date, sc_item.unit, sc_item.quantity,
                                     sc_item.prod_cat_id]

            sc_header_item_details.append(sc_header_item_detail)
    return sc_header_item_details


def item_search(inp_from_date, inp_to_date, **kwargs):
    client = global_variables.GLOBAL_CLIENT
    PO_cat_query = Q()
    company_query = Q()
    sc_obj = ScItem
    sc_item_inst = ScItem()
    hdr_obj = ScHeader
    sc_hdr_inst = ScHeader()
    args_list = {}
    order_list = []
    doc_num_query = Q()
    sc_header_item_details = []
    from_date_val = ''
    for key, value in kwargs.items():
        value_list = []
        if value:
            if key == 'doc_number':
                if '*' in value:
                    doc_num_match = re.search(r'[a-zA-Z0-9]+', value)
                    if value[0] == '*' and value[-1] == '*':
                        doc_num_query = Q(doc_number__in=value) | Q(doc_number__icontains=doc_num_match.group(0))
                    elif value[0] == '*':
                        doc_num_query = Q(doc_number__in=value) | Q(doc_number__iendswith=doc_num_match.group(0))
                    else:
                        doc_num_query = Q(doc_number__in=value) | Q(doc_number__istartswith=doc_num_match.group(0))
                else:
                    # doc_list = sc_hdr_inst.get_hdr_data_by_fields(hdr_obj, value, client)
                    # args_list['doc_number__in'] = doc_list
                    args_list['doc_number'] = value
                result = sc_hdr_inst.get_hdr_data_for_docnum(client, hdr_obj,
                                                             doc_num_query,
                                                             **args_list)
                sc_item_details = django_query_instance.django_filter_only_query(ScItem,
                                                                                 {'client': client,
                                                                                  'source_relevant_ind': True,
                                                                                  'item_del_date__gte': inp_from_date,
                                                                                  'item_del_date__lte': inp_to_date,
                                                                                  'call_off__in': ['01', '02']}).order_by(
                    *order_list)
                for sc_item in sc_item_details:
                    guid = sc_item.header_guid_id
                    for guid_val in result:
                        if guid_val['guid'] == guid:
                            sc_header_item_detail = [guid_val['doc_number'], sc_item.description,
                                                     sc_item.supplier_id,
                                                     sc_item.comp_code, sc_item.item_del_date, sc_item.unit,
                                                     sc_item.quantity,
                                                     sc_item.prod_cat_id]
                            sc_header_item_details.append(sc_header_item_detail)
                return sc_header_item_details
            else:
                if key == 'prod_cat_id':
                    if '*' in value:
                        prod_cat_list = ScItem.get_prod_cat_id(value)
                        # supp_list = SupplierMaster.get_suppid_by_first_name(prod_cat)
                        prod_cat_match = re.search(r'[a-zA-Z0-9]+', value)
                        if value[0] == '*' and value[-1] == '*':
                            PO_cat_query = Q(description__in=prod_cat_list) | Q(
                                description__icontains=prod_cat_match.group(0))
                        elif value[0] == '*':
                            PO_cat_query = Q(description__in=prod_cat_list) | Q(
                                description__iendswith=prod_cat_match.group(0))
                        else:
                            PO_cat_query = Q(description__in=prod_cat_list) | Q(
                                description__istartswith=prod_cat_match.group(0))
                    else:
                        prod_cat_list = ScItem.get_prod_cat_id(value)
                        prod_cat_list.append(value)
                        args_list['description__in'] = prod_cat_list
                    # if '*' not in value:
                    #     value_list = [value]
                    # prod_cat_query = django_q_query(value, value_list, 'description')
                if inp_from_date or inp_to_date:
                    args_list['item_del_date__gte'] = inp_from_date
                    args_list['item_del_date__lte'] = inp_to_date
                if key == 'comp_code':
                    if '*' not in value:
                        value_list = [value]
                        company_query = django_q_query(value, value_list, 'comp_code')
                    if value == '*':
                        args_list['comp_code__in'] = django_query_instance.django_filter_value_list_query(OrgCompanies,
                                                                                                          {
                                                                                                              'client': global_variables.GLOBAL_CLIENT,
                                                                                                              'del_ind': False},
                                                                                                          'company_id')
                    else:
                        args_list['comp_code'] = value
                args_list['call_off__in'] = ['01', '02']
                sc_header_item_details = []
                sc_details_query = list(sc_item_inst.get_item_data_by_fields_src(client,
                                                                                 sc_obj,
                                                                                 PO_cat_query,
                                                                                 company_query,
                                                                                 **args_list
                                                                                 ))
                for sc_item in sc_details_query:
                    guid = sc_item['header_guid_id']
                    scheader_details = django_query_instance.django_filter_only_query(ScHeader,
                                                                                      {'guid': guid,
                                                                                       'client': global_variables.GLOBAL_CLIENT,
                                                                                       'status': CONST_SC_HEADER_APPROVED,
                                                                                       }).values('doc_number')
                    for scheader_detail in scheader_details:
                        sc_header_item_detail = [scheader_detail['doc_number'], sc_item['description'],
                                                 sc_item['supplier_id'],
                                                 sc_item['comp_code'], sc_item['item_del_date'], sc_item['unit'],
                                                 sc_item['quantity'],
                                                 sc_item['prod_cat_id']]

                        sc_header_item_details.append(sc_header_item_detail)

            return sc_header_item_details


def get_sourcing_data(doc_num, from_date, to_date, prod_cat, comp_code):
    global hdr_obj_sc
    username = global_variables.GLOBAL_LOGIN_USERNAME
    client = global_variables.GLOBAL_CLIENT
    hdr_obj = ScHeader
    hdr_inst = ScHeader()
    hdr_obj_sc = ScItem
    sc_inst = ScItem()
    result = None
    PO_cat_query = Q()
    creator_query = Q()
    requester_query = Q()
    doc_num_query = Q()
    company_query = Q()
    sc_header_item_details = []
    args_list = {}
    if doc_num is not None and doc_num != '':
        result = hdr_inst.get_hdr_data_by_objid(hdr_obj, doc_num, client)
        if '*' in doc_num:
            doc_num_match = re.search(r'[0-9]+', doc_num)
            if doc_num[0] == '*' and doc_num[-1] == '*':
                doc_num_query = Q(doc_number__in=result) | Q(doc_number__icontains=doc_num_match.group(0))
            elif doc_num[0] == '*':
                doc_num_query = Q(doc_number__in=result) | Q(doc_number__iendswith=doc_num_match.group(0))
            else:
                doc_num_query = Q(doc_number__in=result) | Q(doc_number__istartswith=doc_num_match.group(0))
        else:
            doc_list = sc_inst.get_item_data_by_objid(hdr_obj_sc, doc_num, client)
            # doc_list = hdr_inst.get_hdr_data_by_objid(hdr_obj, doc_num, client)
            # doc_list['prod_cat'] = prod_cat
            print(doc_list[0]['guid'])

            # args_list['header_guid__in'] = doc_list[0]['guid']
            doc_list = hdr_inst.get_hdr_data_by_fields(hdr_obj, doc_num, client)
            args_list['doc_number__in'] = doc_list
        result1 = hdr_inst.get_hdr_data_for_docnum(client, hdr_obj,
                                                   doc_num_query,
                                                   **args_list)
        sc_item_details = django_query_instance.django_filter_only_query(ScItem,
                                                                         {'client': client,
                                                                          'grouping_ind': True}).order_by(
            *args_list)
        for sc_item in sc_item_details:
            guid = sc_item.header_guid_id
            for guid_val in result1:
                if guid_val['guid'] == guid:
                    sc_header_item_detail = [guid_val['doc_number'], sc_item.description,
                                             sc_item.supplier_id,
                                             sc_item.comp_code, sc_item.item_del_date, sc_item.unit,
                                             sc_item.quantity,
                                             sc_item.prod_cat_id]
                    sc_header_item_details.append(sc_header_item_detail)
    else:
        if from_date is not None and to_date is not None and from_date != '' and to_date != '':
            args_list['item_del_date__gte'] = from_date
            args_list['item_del_date__lte'] = to_date
        if prod_cat is not None and prod_cat != '':
            if '*' in prod_cat:
                prod_cat_list = ScItem.get_prod_cat_id(prod_cat)
                # supp_list = SupplierMaster.get_suppid_by_first_name(prod_cat)
                prod_cat_match = re.search(r'[a-zA-Z0-9]+', prod_cat)
                if prod_cat[0] == '*' and prod_cat[-1] == '*':
                    PO_cat_query = Q(description__in=prod_cat_list) | Q(description__icontains=prod_cat_match.group(0))
                elif prod_cat[0] == '*':
                    PO_cat_query = Q(description__in=prod_cat_list) | Q(description__iendswith=prod_cat_match.group(0))
                else:
                    PO_cat_query = Q(description__in=prod_cat_list) | Q(
                        description__istartswith=prod_cat_match.group(0))
            else:
                prod_cat_list = ScItem.get_prod_cat_id(prod_cat)
                prod_cat_list.append(prod_cat)
                args_list['description__in'] = prod_cat_list
        if '*' not in comp_code:
            value_list = [comp_code]
            company_query = django_q_query(comp_code, value_list, 'comp_code')
        if comp_code == '*':
            args_list['comp_code__in'] = django_query_instance.django_filter_value_list_query(OrgCompanies,
                                                                                              {
                                                                                                  'client': global_variables.GLOBAL_CLIENT,
                                                                                                  'del_ind': False},
                                                                                              'company_id')
        else:
            args_list['comp_code'] = comp_code

    result = sc_inst.get_item_data_by_fields_src(client, hdr_obj_sc, PO_cat_query, company_query, doc_num_query,
                                                 **args_list)
    return result


def filter_rfq(client, order_list):
    """

    :param client:
    :param order_list:
    :return:
    """
    sc_header_item_details = []
    sc_item_details = django_query_instance.django_filter_only_query(ScItem,
                                                                     {'client': client, 'source_relevant_ind': True,
                                                                      'po_doc_num': None,
                                                                      'call_off': '03'
                                                                      }).order_by(
        *order_list)
    for sc_item in sc_item_details:
        guid = sc_item.header_guid_id
        scheader_details = django_query_instance.django_filter_only_query(ScHeader,
                                                                          {'guid': guid,
                                                                           'client': client,
                                                                           'status': CONST_SC_HEADER_APPROVED,
                                                                           }).values('doc_number')
        for scheader_detail in scheader_details:
            sc_header_item_detail = [scheader_detail['doc_number'], sc_item.description, sc_item.supplier_id,
                                     sc_item.comp_code, sc_item.item_del_date, sc_item.unit, sc_item.quantity,
                                     sc_item.prod_cat_id]

            sc_header_item_details.append(sc_header_item_detail)
    return sc_header_item_details
