"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    purchaser_cockpit.py
Usage:
    Purchase assist role user data
Author:
    Deepika K
"""
from django.http import JsonResponse
from django.shortcuts import render

from eProc_Basic.Utilities.constants.constants import CONST_SC_HEADER_APPROVED, CONST_PO_SPLIT_SUPPLIER, \
    CONST_PO_SPLIT_CURRENCY, CONST_PO_GROUP_COMPANY_CODE, CONST_PO_GROUP_CURRENCY, CONST_PO_DELIVERY_DATE
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.remove_element_from_list import remove_element_from_list
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic_Settings.views import JsonParser_obj
from eProc_Configuration.models import OrgCompanies, PoGroupCriteria
from eProc_Doc_Search_and_Display.Utilities.search_display_generic import get_hdr_data
from eProc_Emails.Utilities.email_notif_generic import send_po_attachment_email
from eProc_Purchase_Order.Utilities.purchase_order_generic import CreatePurchaseOrder, check_for_po_creation, check_po
from eProc_Purchaser_Cockpit.Utilities.purchaser_cockpit_specific import filter_based_on_sc_item_field, item_search, \
    get_sourcing_data, filter_rfq

# purchaser_cockpit_search
from eProc_Reports.Utilities.reports_generic import get_companylist, get_companyDetails
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Shopping_Cart.models import ScItem, ScHeader

django_query_instance = DjangoQueries()


def incomplete_form(request, guid=None):
    """

    :param request:
    :param guid:
    :return:
    """
    context = {
        'inc_nav': True,
        'shopping': True,
    }

    return render(request, 'Purchaser_Cockpit/incomplete_form.html', context)


def sc_item_field_filter(request):
    supplier_id = False
    comp_code = False
    prod_cat = False
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    order_list = []
    search_fields = {}
    # sc_header_item_details = ''
    sc_header_item = []
    comp_list = get_companyDetails(request)
    sc_header_item_details = filter_based_on_sc_item_field(client, order_list)
    count = len(sc_header_item_details)
    if request.method == 'POST':
        search_fields = {}
        inp_comp_code = request.POST.get('company_code')
        inp_doc_type = 'SC'
        inp_doc_num = request.POST.get('sc_number')
        inp_from_date = request.POST.get('from_date')
        inp_to_date = request.POST.get('to_date')
        inp_supl = None
        inp_created_by = None
        inp_requester = None
        prod_cat = request.POST.get('product_desc')
        # results
        search_fields['doc_number'] = request.POST.get('sc_number')
        search_fields['prod_cat_id'] = request.POST.get('product_desc')
        if request.POST.get('company_code') == '':
            search_fields['comp_code'] = '*'
        else:
            search_fields['comp_code'] = request.POST.get('company_code')
        sc_item_inst = ScItem()
        sc_header_item_details = item_search(inp_from_date, inp_to_date, **search_fields)
        count = len(sc_header_item_details)

    context = {
        'sc_header_item_details': sc_header_item_details,
        'count': count,
        'prod_cat': prod_cat,
        'supplier_id': supplier_id,
        'comp_code': comp_code,
        'comp_list': comp_list,
        'inc_nav': True,
        'shopping': True,
        'is_slide_menu': True,
        'is_sourcing_active': True
    }

    return render(request, 'Purchaser_Cockpit/sourcing_cockpit.html', context)


def generate_po(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    response = {}
    sc_header_list = []
    sc_header_instance = ''
    doc_num = []
    guid_arr = []
    requester = []
    po_split_list = []
    status = ''
    po_data = JsonParser_obj.get_json_from_req(request)
    for doc in po_data:
        sc_header_list.append(django_query_instance.django_filter_value_list_query(ScHeader,
                                                                                   {
                                                                                       'client': global_variables.GLOBAL_CLIENT,
                                                                                       'doc_number': doc['doc_number']},
                                                                                   'guid'))
        doc_num.append(doc['doc_number'])
        sc_header_instance = django_query_instance.django_get_query(ScHeader,
                                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                                     'doc_number': doc['doc_number']})
        guid_arr.append(sc_header_instance.guid)
        requester.append(sc_header_instance.requester)
        po_split_list1 = get_po_split_group_type(sc_header_instance.co_code)
        if po_split_list1:
            po_split_list.append(po_split_list1)

    sc_item_details = django_query_instance.django_filter_query(ScItem, {
        'header_guid__in': guid_arr, 'client': client, 'del_ind': False
    }, None, None)

    create_purchase_order = CreatePurchaseOrder(sc_header_instance)
    po_creation_flag = ''
    qty = ''
    # po_split_list = get_po_split_group_type(sc_header_instance.co_code)

    # check whether the items are same
    desc = sc_item_details[0]['description']
    supp_id = sc_item_details[0]['supplier_id']
    del_date = sc_item_details[0]['item_del_date']
    company_id = sc_item_details[0]['comp_code']
    if len(sc_item_details) > 1:
        if len(requester) != len(set(requester)):
            for i in range(1, len(sc_item_details)):
                qty = sc_item_details[0]['quantity']
                if desc == sc_item_details[i]['description'] and company_id == sc_item_details[i]['comp_code'] \
                        and supp_id == sc_item_details[i]['supplier_id'] and del_date == sc_item_details[i]['item_del_date']:
                    po_creation_flag = 1
                    qty = qty + sc_item_details[i]['quantity']
            if po_creation_flag == 1:
                sc_item_details1 = django_query_instance.django_filter_query(ScItem, {
                    'header_guid': guid_arr[0], 'client': client, 'del_ind': False
                }, None, None)
                sc_item_details1[0]['quantity'] = qty
                status = create_purchase_order.create_purchaser_order(sc_item_details1, sc_item_details[0]['supplier_id'])
            else:
                status = create_purchase_order.create_purchaser_order(sc_item_details,
                                                                      sc_item_details[0]['supplier_id'])
        elif po_split_list:
            if CONST_PO_GROUP_COMPANY_CODE in po_split_list[0]:
                company_id = sc_item_details[0]['comp_code']
                for i in range(1, len(sc_item_details)):
                    if company_id == sc_item_details[i]['comp_code']:
                        status = create_purchase_order.create_purchaser_order(sc_item_details, sc_item_details[0]['supplier_id'])
                    else:
                        response['grping_error'] = "The PO cannot be grouped as Company Codes are different"
            if CONST_PO_GROUP_CURRENCY in po_split_list[0]:
                currency_id = sc_item_details[0]['currency']
                for i in range(1, len(sc_item_details)):
                    if currency_id == sc_item_details[i]['currency']:
                        status = create_purchase_order.create_purchaser_order(sc_item_details,
                                                                              sc_item_details[0]['supplier_id'])
                    else:
                        response['grping_error'] = "The PO cannot be grouped as Currencies are different"
            if CONST_PO_DELIVERY_DATE in po_split_list[0]:
                currency_id = sc_item_details[0]['currency']
                for i in range(1, len(sc_item_details)):
                    if currency_id == sc_item_details[i]['currency']:
                        status = create_purchase_order.create_purchaser_order(sc_item_details,
                                                                              sc_item_details[0]['supplier_id'])
                    else:
                        response['grping_error'] = "The PO cannot be grouped as Delivery Dates are different"
    else:
        status = create_purchase_order.create_purchaser_order(sc_item_details, sc_item_details[0]['supplier_id'])
    if not status:
        return False, create_purchase_order.error_message, create_purchase_order.output, create_purchase_order.po_doc_list

    # status, error_message, output, po_doc_list = create_purchase_order.create_po()
    for po_document_number in create_purchase_order.po_doc_list:
        email_supp_monitoring_guid = ''
        send_po_attachment_email(create_purchase_order.output, po_document_number, email_supp_monitoring_guid)

    for data in sc_item_details:
        django_query_instance.django_update_query(ScItem,
                                                  {'client': global_variables.GLOBAL_CLIENT,
                                                   'guid': data['guid'],
                                                   'del_ind': False},
                                                  {'po_doc_num': create_purchase_order.po_doc_list[0],
                                                   })

    if create_purchase_order.error_message:
        response['message'] = "error"
    else:
        response['message'] = "PO generated"

    order_list = []
    response['sourcing_data'] = filter_based_on_sc_item_field(client, order_list)

    return JsonResponse(response, safe=False)


def PO_grouping(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    response = ''
    supplier_id = []
    po_flag = False
    po_data = JsonParser_obj.get_json_from_req(request)
    for doc in po_data:
        if doc['supplier_id'] not in supplier_id:
            supplier_id.append(doc['supplier_id'])

    temp = supplier_id[0]
    for supp in supplier_id:
        if supp == temp:
            po_flag = True
        else:
            po_flag = False

    response = po_flag

    return JsonResponse(response, safe=False)


def rfq_details(request):
    supplier_id = False
    comp_code = False
    prod_cat = False
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    order_list = []
    search_fields = {}
    # sc_header_item_details = ''
    sc_header_item = []
    sc_header_item_details = filter_rfq(client, order_list)
    count = len(sc_header_item_details)
    if request.method == 'POST':
        search_fields = {}
        inp_comp_code = request.POST.get('company_code')
        inp_doc_type = 'SC'
        inp_doc_num = request.POST.get('sc_number')
        inp_from_date = request.POST.get('from_date')
        inp_to_date = request.POST.get('to_date')
        inp_supl = None
        inp_created_by = None
        inp_requester = None
        prod_cat = request.POST.get('product_desc')
        # results
        search_fields['doc_number'] = request.POST.get('sc_number')
        # search_fields['from_date'] = request.POST.get('from_date')
        # search_fields['to_date'] = request.POST.get('to_date')
        search_fields['prod_cat_id'] = request.POST.get('product_desc')
        search_fields['comp_code'] = request.POST.get('company_code')
        sc_item_inst = ScItem()
        sc_header_item_details = item_search(inp_from_date, inp_to_date, **search_fields)
        count = len(sc_header_item_details)

    context = {
        'sc_header_item_details': sc_header_item_details,
        'count': count,
        'prod_cat': prod_cat,
        'supplier_id': supplier_id,
        'comp_code': comp_code,
        'inc_nav': True,
        'shopping': True,
        'is_slide_menu': True
    }

    return render(request, 'Purchaser_Cockpit/display_rfq.html', context)


def get_po_split_group_type(company_code):
    """

    """
    po_split_active_list_cocode = []
    po_split_list = django_query_instance.django_filter_value_list_query(PoGroupCriteria,
                                                                         {'client': global_variables.GLOBAL_CLIENT,
                                                                          'del_ind': False,
                                                                          'company_code_id': '*',
                                                                          'activate': True}, 'po_split_group_type_id')

    if django_query_instance.django_existence_check(PoGroupCriteria,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'del_ind': False,
                                                     'company_code_id': company_code,
                                                     'activate': False}):
        po_split_inactive_list_cocode = django_query_instance.django_filter_value_list_query(PoGroupCriteria,
                                                                                             {
                                                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                                                 'del_ind': False,
                                                                                                 'company_code_id': company_code,
                                                                                                 'activate': False},
                                                                                             'po_split_group_type_id')
        po_split_list = remove_element_from_list(po_split_list, po_split_inactive_list_cocode)
    if django_query_instance.django_existence_check(PoGroupCriteria,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'del_ind': False,
                                                     'company_code_id': company_code,
                                                     'activate': True}):
        po_split_active_list_cocode = django_query_instance.django_filter_value_list_query(PoGroupCriteria,
                                                                                           {
                                                                                               'client': global_variables.GLOBAL_CLIENT,
                                                                                               'del_ind': False,
                                                                                               'company_code_id': company_code,
                                                                                               'activate': True},
                                                                                           'po_split_group_type_id')
    po_split_list = list(set(po_split_list + po_split_active_list_cocode))
    return po_split_list
