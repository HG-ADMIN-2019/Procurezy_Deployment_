"""Copyright (c) 2020 Hiranya Garbha, Inc. Name: email_notification.py Usage: On click of E-mails tab in Application
Settings email_notification_form - This function handles the display, modifying and saving the email notification
format and renders email_settings.html Author: Shilpa """
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

from Majjaka_eProcure import settings
from eProc_Add_Item.views import JsonParser_obj
from eProc_Basic.Utilities.constants.constants import CONST_USER_REG, CONST_ACTIVE, CONST_COFIG_UI_MESSAGE_LIST
from eProc_Basic.Utilities.functions.django_q_query import django_q_query
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import *
from eProc_Configuration.Utilities.application_settings_generic import get_configuration_data, get_ui_messages
from eProc_Configuration.models import NotifSettings, NotifKeywordsDesc, NotifSettingsDesc, EmailObjectTypes, \
    EmailKeywords, EmailContents, Languages
from eProc_Emails.Utilities.email_notif_generic import email_notify, appr_notify, send_po_attachment_email
from eProc_Emails.models import EmailUserMonitoring, EmailDocumentMonitoring, EmailSupplierMonitoring
from eProc_Registration.models import UserData
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import get_SC_details_email
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Shopping_Cart.models import ScHeader, ScPotentialApproval, ScApproval

django_query_instance = DjangoQueries()


@login_required
def email_notification_form(req):
    """
    handles email notification data for displaying, edit and saving
    :param req: request data from UI
    :return: renders emailnotif.html
    """
    update_user_info(req)
    client = global_variables.GLOBAL_CLIENT
    variant_list = []
    keyword_list = []

    # django_query_instance.django_filter_only_query(EmailObjectTypes, {'client': client, 'del_ind': False})
    object_type_data = django_query_instance.django_filter_only_query(EmailObjectTypes,
                                                                      {'client': client,
                                                                       'del_ind': False}).values('object_type')

    for variant_names in object_type_data:
        variant_list.append(variant_names['object_type'])
    try:
        keyword_data = django_query_instance.django_filter_only_query(EmailKeywords, {
            'client': client,
            'del_ind': False
        }).values('keyword')
        for dt in keyword_data:
            keyword_list.append(dt['keyword'])

        email_data = get_configuration_data(EmailContents, {'del_ind': False},
                                            ['email_contents_guid', 'object_type', 'subject', 'header', 'body',
                                             'footer', 'language_id'])
        language_list = list(django_query_instance.django_filter_only_query(Languages, {'del_ind': False}).values('language_id', 'description'))
        for data in email_data:
            for lang in language_list:
                if data['language_id'] == lang['language_id']:
                    data['lang_description'] = lang['description']

    except ObjectDoesNotExist:
        msg = messages.error(req, 'please maintain data')
        return render(req, 'emailnotif.html', msg)

    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)

    context = {
        'variant_list': variant_list,
        'keyword_list': keyword_list,
        'email_data': email_data,
        'messages_list': messages_list,
        'language_list': language_list,
        'inc_nav': True,
    }

    return render(req, 'Application_Settings/email_settings.html', context)


@transaction.atomic
def edit_email_notif_form(req):
    """
    Function to retrieve selected email notification type data.
    :param req:
    :return:
    """
    client = getClients(req)

    if req.is_ajax():
        keyword_list = []
        selected_variant = req.POST.get('variant_data')

        form_data1 = django_query_instance.django_get_query(EmailContents,
                                                            {'object_type': selected_variant, 'client': client,
                                                             'del_ind': False})

        keyword_data1 = django_query_instance.django_filter_only_query(EmailKeywords,
                                                                       {'object_type': selected_variant,
                                                                        'client': client, 'del_ind': False}).values(
            'keyword')

        for keywords in keyword_data1:
            keyword_list.append(keywords['keyword'])

        ajax_context = {
            'keyword_list': keyword_list,
            'email_contents_guid': form_data1.email_contents_guid,
            'subject': form_data1.subject,
            'body': form_data1.body,
            'header': form_data1.header,
            'footer': form_data1.footer
        }

        return JsonResponse(ajax_context)


@transaction.atomic
def update_email_notif_form(request):
    """
    This function is to update the edited email content data.
    :param request:
    :return:
    """
    if request.method == 'POST':
        update_email_guid = request.POST.get('email_guid')
        update_email_subject = request.POST.get('email_subject')
        update_email_header = request.POST.get('email_header')
        update_email_body = request.POST.get('email_body')
        update_email_footer = request.POST.get('email_footer')

        if update_email_guid is None:
            update_email_guid = guid_generator()
        update_email_notif_data = django_query_instance.django_filter_only_query(EmailContents,
                                                                                 {
                                                                                     'email_contents_guid': update_email_guid,
                                                                                     'del_ind': False})

        update_email_notif_data.update(subject=update_email_subject, header=update_email_header, body=update_email_body,
                                       footer=update_email_footer)
        error_msg = get_message_desc(MSG037)[1]
        # msgid = 'MSG037'
        # error_msg = get_msg_desc(msgid)
        # msg = error_msg['message_desc'][0]
        # error_msg = msg
        return JsonResponse({'message': error_msg})
        # return JsonResponse({'message': MSG037})


@transaction.atomic
def resend_user_mail(request):
    """
    This function is to update the edited email content data.
    :param request:
    :return:
    """
    global message, email_list, status
    variant_name = ''
    client = getClients(request)
    mgr_details = {}
    approver = []
    appr_flag = 0
    status = 0
    basic_data = JsonParser_obj.get_json_from_req(request)
    sc_email_data = []

    # for user in user_details:
    #     first_name = user['first_name']
    #     last_name = user['last_name']

    if request.is_ajax():
        for val in basic_data:
            username = val['username']
            email = val['email']
            email_user_monitoring_guid = val['email_user_monitoring_guid']
            variant_name = val['email_type']
            if variant_name == 'SC Approval' or variant_name == 'SC_APPROVAL':
                variant_name = 'SC_APPROVAL'
            elif variant_name == 'Supplier Order':
                variant_name = 'PO_SUPPLIER'
            user_details = django_query_instance.django_get_query(UserData, {'email': val['email'],
                                                                             'del_ind': False,
                                                                             'client': client})
            if variant_name == 'SC_APPROVAL':
                result = {}
                sc_email_details = django_query_instance.django_get_query(EmailDocumentMonitoring,
                                                                          {
                                                                              'email_document_monitoring_guid': email_user_monitoring_guid,
                                                                              'client': client,
                                                                              'object_type': variant_name,
                                                                              'del_ind': False})
                appr_flag = check_sc_approval_email(sc_email_details.doc_number)
                if appr_flag != 1:
                    sc_header_instance = django_query_instance.django_get_query(ScHeader,
                                                                                {'client': client,
                                                                                 'doc_number': sc_email_details.doc_number,
                                                                                 'del_ind': False,
                                                                                 })
                    app_step_number = django_query_instance.django_filter_value_list_query(ScPotentialApproval,
                                                                                           {
                                                                                               'sc_header_guid': sc_header_instance.guid,
                                                                                               'app_id': user_details.username,
                                                                                               'client': client,
                                                                                           },
                                                                                           'step_num')[0]
                    next_level_approver = django_query_instance.django_filter_value_list_query(ScPotentialApproval,
                                                                                               {
                                                                                                   'sc_header_guid': sc_header_instance.guid,
                                                                                                   'step_num': app_step_number,
                                                                                                   'client': client,
                                                                                                   'proc_lvl_sts': CONST_ACTIVE},
                                                                                               'app_id')
                    for appr in next_level_approver:
                        if appr == user_details.username:
                            approver.append(appr)
                    if len(next_level_approver) > 1:
                        mgr_details['app_id_detail'] = approver
                    else:
                        mgr_details['app_id_detail'] = approver[0]
                    mgr_details['app_id_value'] = next_level_approver[0]
                    context = get_SC_details_email(sc_header_instance.guid)
                    context['manager_details'] = [mgr_details]
                    context['step_num_inc'] = int(app_step_number)
                    context['email_document_monitoring_guid'] = email_user_monitoring_guid
                    status = appr_notify(context, 'SC_APPROVAL', client)
                    email_list = django_query_instance.django_filter_query(EmailDocumentMonitoring,
                                                                           {'client': client,
                                                                            'object_type': variant_name,
                                                                            'email_status': 2,
                                                                            'del_ind': False}, None, None)
                else:
                    email_list = django_query_instance.django_filter_query(EmailDocumentMonitoring,
                                                                           {'client': client,
                                                                            'object_type': variant_name,
                                                                            'email_status': 2,
                                                                            'del_ind': False}, None, None)
                result['doc_num'] = username
                if status == 1:
                    result['message'] = "Email Re-Sent Successfully"
                else:
                    result['message'] = "Email Not-Sent"
                sc_email_data.append(result)
            elif variant_name == 'PO_SUPPLIER':
                file_name = str(username)
                path = str(settings.BASE_DIR) + f'/media/po_pdf/{client}/{file_name}.pdf'
                status = send_po_attachment_email(path, username, email_user_monitoring_guid)
                email_list = django_query_instance.django_filter_query(EmailSupplierMonitoring,
                                                                       {'client': client,
                                                                        'object_type': variant_name,
                                                                        'email_status': 2,
                                                                        'del_ind': False}, None, None)
            else:
                email_data = {
                    'username': username,
                    'email': email,
                    'email_user_monitoring_guid': email_user_monitoring_guid,
                    'first_name': user_details.first_name,
                    'doc_number': username
                }
                status = email_notify(email_data, variant_name, client)
                email_list = django_query_instance.django_filter_query(EmailUserMonitoring,
                                                                       {'client': client,
                                                                        'object_type': variant_name,
                                                                        'email_status': 2,
                                                                        'del_ind': False}, None, None)

            if status == 1:
                message = "Email Re-Sent Successfully"
            else:
                message = "Email Not-Sent"

    return JsonResponse({'result': sc_email_data, 'email_list': email_list, 'appr_flag': appr_flag, 'message': message})


def check_sc_approval_email(doc_num):
    approved_flag = 0
    guid_list = []
    sc_header_details = django_query_instance.django_filter_query(ScHeader,
                                                                  {'doc_number': doc_num,
                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                   'del_ind': False},
                                                                  None,
                                                                  None)
    for sc_data in sc_header_details:
        guid_list.append(sc_data['guid'])
    approval_data = django_query_instance.django_filter_query(ScApproval,
                                                              {
                                                                  'header_guid__in': guid_list,
                                                                  'client': global_variables.GLOBAL_CLIENT,
                                                              }, None, None)
    for data in approval_data:
        if data['proc_lvl_sts'] == 'COMPLETED' and data['app_sts'] == 'APPROVER_APPROVED':
            sc_guid = data['header_guid_id']
            approved_docs = django_query_instance.django_filter_value_list_query(ScHeader,
                                                                                 {
                                                                                     'guid': sc_guid,
                                                                                     'client': global_variables.GLOBAL_CLIENT,
                                                                                 },
                                                                                 'doc_number')
            approved_flag = 1
    return approved_flag
