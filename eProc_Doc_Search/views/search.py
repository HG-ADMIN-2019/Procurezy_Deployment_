"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    search.py
Usage:
     m_search_meth - This function is used to get header details of shopping cart and purchase order.
Author:
    Shankar / Sanjay / Soni(MEP:19) / Deepika(MEP:84)
"""

from django.http import HttpResponse
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import OrgAddress
# from eProc_Generate_PDF.views import render_pdf_view
# from eProc_Generate_PDF.views.sc_details_pdf import render_pdf_view
from eProc_Generate_PDF.views.sc_details_pdf import render_pdf_view
from eProc_Registration.models import UserData
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Shopping_Cart.models import *

JsonParser_obj = JsonParser()
django_query_instance = DjangoQueries()


def get_sc_app_data(request):
    """

    :param request:
    :return:
    """
    update_user_info(request)
    sc_app_guid_data = JsonParser_obj.get_json_from_req(request)
    # sc_app_guid_data = request.POST.get('sc_app_guid_data')
    client = global_variables.GLOBAL_CLIENT
    sc_app = django_query_instance.django_filter_only_query(ScPotentialApproval, {'sc_approval_guid': sc_app_guid_data['guid'], 'client': client})
    return JsonParser_obj.get_json_from_obj(sc_app)


def generate_sc_details_pdf(request, doc_number):
    client = getClients(request)
    sc_details = django_query_instance.django_get_query(ScHeader, {'doc_number': doc_number, 'del_ind': False})
    guid = sc_details.guid
    address_details = django_query_instance.django_get_query(ScAddresses, {'header_guid': guid,
                                                                           'del_ind': False,
                                                                           'address_type':'D'})
    inv_add_number = sc_details.inv_addr_num

    invoice_address = django_query_instance.django_filter_only_query(OrgAddress, {
        'address_number': inv_add_number, 'client': client, 'del_ind': False
    })

    item_details = django_query_instance.django_filter_only_query(ScItem, {
        'header_guid': guid, 'del_ind': False
    })

    accounting_data = django_query_instance.django_filter_only_query(ScAccounting, {
        'header_guid': guid, 'del_ind': False, 'client': client
    })

    requester_details = django_query_instance.django_filter_only_query(UserData, {'username': sc_details.requester,
                                                                                  'client': client})

    context = {
        'sc_details': sc_details,
        'address_details': address_details,
        'invoice_address': invoice_address,
        'item_details': item_details,
        'accounting_data': accounting_data,
        'requester_details': requester_details,
    }
    pdf = render_pdf_view('sc_pdf.html', context)

    return HttpResponse(pdf, content_type='application/pdf')
