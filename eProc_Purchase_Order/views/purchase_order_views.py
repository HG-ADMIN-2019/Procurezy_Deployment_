from django.http import HttpResponse
from django.shortcuts import render

from eProc_Basic.Utilities.functions.encryption_util import decrypt
from eProc_Basic.Utilities.functions.get_db_query import getClients, django_query_instance
from eProc_Generate_PDF.views.sc_details_pdf import render_pdf_view
from eProc_Purchase_Order.Utilities.purchase_order_generic import get_po_details
from eProc_Purchase_Order.models import PoHeader, PoAddresses
from eProc_Shopping_Cart.context_processors import update_user_info


def po_doc_details(request, encrypted_guid):
    update_user_info(request)
    po_header_guid = decrypt(encrypted_guid)
    context = get_po_details(po_header_guid)
    context['inc_nav'] = True

    return render(request, 'purchase_order/purchase_order.html', context)


def generate_po_details_pdf(request, doc_number):
    client = getClients(request)
    po_header_data = django_query_instance.django_get_query(PoHeader, {'doc_number': doc_number, 'client': client,
                                                                       'del_ind': False})
    po_header_guid = po_header_data.po_header_guid
    context = get_po_details(po_header_guid)
    context['po_header_delivery_address'] = django_query_instance.django_get_query(PoAddresses, {'po_header_guid': po_header_guid,
                                                                                                 'address_type': 'D',
                                                                                                 'del_ind': False})
    context['po_header_invoice_address'] = django_query_instance.django_get_query(PoAddresses, {'po_header_guid': po_header_guid,
                                                                                                'address_type': 'I',
                                                                                                'del_ind': False})

    pdf = render_pdf_view('po_pdf_mockup.html', context)

    return HttpResponse(pdf, content_type='application/pdf')
