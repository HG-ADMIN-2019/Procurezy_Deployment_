import json

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db import transaction
from django.http import JsonResponse

from Majjaka_eProcure import settings
from eProc_Basic.Utilities.constants.constants import CONST_SC_APPR_APPROVED, CONST_SC_HEADER_APPROVED, CONST_COMPLETED, \
    CONST_SC_HEADER_REJECTED, CONST_VALIDATION_ERROR
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG184
from eProc_Doc_Search.views import generate_sc_details_pdf
from eProc_Emails.Utilities.email_notif_generic import appr_notify, email_notify, send_po_attachment_email
from eProc_Generate_PDF.Utilities.generate_pdf_generic import save_pdf
from eProc_Purchase_Order.Utilities.purchase_order_generic import CreatePurchaseOrder, create_po_pdf, \
    update_po_error_status
from eProc_Registration.models import UserData
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Shopping_Cart.models import ScHeader, ScItem
from eProc_Workflow.Utilities.work_flow_specific import update_appr_status
import time

JsonParser_obj = JsonParser()
django_query_instance = DjangoQueries()


def save_appr_status(request):
    """
    save approval status
    :param request:
    :return:
    """
    data = {}
    appr_status = JsonParser_obj.get_json_from_req(request)
    client = global_variables.GLOBAL_CLIENT
    email_data = ''
    variant_name = ''
    update_user_info(request)
    header_status, sc_header_instance = update_appr_status(appr_status)
    user_details = django_query_instance.django_get_query(UserData, {
        'username': sc_header_instance.requester,
        'client': global_variables.GLOBAL_CLIENT
    })
    email_data = {
        'username': user_details.username,
        'email': user_details.email,
        'first_name': user_details.first_name,
        'doc_number': sc_header_instance.doc_number,
        'sc_description': sc_header_instance.description,
        'email_user_monitoring_guid': ''
    }
    po_doc_list = ''
    status = ''
    if header_status == CONST_SC_HEADER_APPROVED:
        sc_item_details = django_query_instance.django_filter_only_query(ScItem, {
            'header_guid': sc_header_instance.guid, 'client': client, 'del_ind': False
        })
        for sc_item in sc_item_details:
            if not sc_item.source_relevant_ind == 1:
                create_purchase_order = CreatePurchaseOrder(sc_header_instance)
                status, error_message, data['output'], po_doc_list = create_purchase_order.create_po()
        # Send purchase order email to supplier
        for po_document_number in po_doc_list:
            email_supp_monitoring_guid = ''
            send_po_attachment_email(data['output'], po_document_number, email_supp_monitoring_guid)

            if not status:
                update_po_error_status(sc_header_instance.guid, CONST_VALIDATION_ERROR)
            variant_name = 'APPROVED_SC'
            # email_notify(email_data, variant_name, client)
    if header_status == CONST_SC_HEADER_REJECTED:
        variant_name = 'SC_REJECTED'
        email_notify(email_data, variant_name, client)

    # approval_detail = appr_status['status'].split('-')
    # header_guid = approval_detail[1]
    # sc_header_instance = django_query_instance.django_get_query(ScHeader, {'guid': header_guid})
    # generate_sc_details_pdf(request, doc_number)
    # -------------------------------------------------------------
    # context = create_po_pdf(sc_header_instance.doc_number)
    # file_name,status,output = save_pdf(context)
    # if not status:
    #     return JsonResponse({'status': 400})
    # mail = EmailMultiAlternatives('subject', 'text_content', settings.EMAIL_HOST_USER, ['deepika@hiranya-garbha.com'])
    # file = open(output, "r+")
    # attachment = file.read()
    # file.close()
    # mail.attach("my.pdf", attachment, "application/pdf")
    # mail.send()
    # return JsonResponse({'status':200,'path':f'/media/{sc_header_instance.doc_number}.pdf'})

    msgid = 'MSG184'
    error_msg = get_message_desc(msgid)[1]
    data['message'] = error_msg
    data['approver_status'] = header_status
    data['status'] = header_status
    return JsonResponse(data)
