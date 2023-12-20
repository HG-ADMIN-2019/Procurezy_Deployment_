"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    email_notif_generic.py
Usage:
   Generic functions to send email based on variant names.
   email_notify:function to send to email for user registration and returns the boolean value
   appr_notify:function to send email for approval registration and returns the boolean value
Author:
Soni Vydyula
"""
import re
import smtplib
from email.mime.image import MIMEImage
from functools import lru_cache

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.http import BadHeaderError
from django.template.loader import render_to_string

from Majjaka_eProcure import settings
from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import EmailContents, AccountAssignmentCategory, UnitOfMeasures, \
    OrgClients, SupplierMaster
from eProc_Emails.models import EmailUserMonitoring, EmailDocumentMonitoring, EmailSupplierMonitoring
from eProc_Notes_Attachments.models import Notes
from eProc_Purchase_Order.models import PoHeader, PoItem
from eProc_Registration.models import UserData
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import get_acc_detail
from eProc_Shopping_Cart.models import ScPotentialApproval, ScItem
from eProc_Suppliers.Utilities.supplier_generic import Supplier

django_query_instance = DjangoQueries()


def email_notify(emaildata, variant_name, client):
    """
    function to send an email for user registration
    :param client:
    :param request: request data from UI
    :param variant_name: takes the variant name for user registration
    :return: returns Boolean value
    """
    global email_status, error_type
    username = emaildata['username']
    email = emaildata['email']
    guid = emaildata['email_user_monitoring_guid']
    # doc_num = emaildata['doc_number']
    subject = ''
    body = ''
    header = ''
    footer = ''
    first_name = ''
    # gets the email content based on the variant name
    emailDetail = list(django_query_instance.django_filter_only_query(EmailContents, {
        'object_type': variant_name, 'client': client
    }).values())

    # loop to separate the subject and body from query set
    for subValue in emailDetail:
        subject = subValue['subject']

    for bodyValue in emailDetail:
        body = bodyValue['body']
    for headerValue in emailDetail:
        header = headerValue['header']
    for footerValue in emailDetail:
        footer = footerValue['footer']

    #  this function separates the keywords from the content.
    subjectKeys = re.findall('\@.*?\@', subject)
    bodyKeys = re.findall('\@.*?\@', body)
    headerKeys = re.findall('\@.*?\@', header)
    footerKeys = re.findall('\@.*?\@', footer)
    keys = subjectKeys + bodyKeys + headerKeys + footerKeys
    # site = Si.filter(id=1)
    # domain = site[0].domain

    # loop to assign the respective values based on the keywords from the email content
    for data in keys:
        if data == CONST_CLIENT:
            client = client
            subject = subject.replace(data, client)
            body = body.replace(data, client)
            header = header.replace(data, client)
            footer = footer.replace(data, client)
        if data == CONST_USER_NAME:
            username = username
            subject = subject.replace(data, username)
            body = body.replace(data, username)
            header = header.replace(data, username)
            footer = footer.replace(data, username)
        if data == CONST_PASSWORD:
            password = emaildata['password']
            body = body.replace(data, password)
            header = header.replace(data, password)
            footer = footer.replace(data, password)
        if data == CONST_FIRST_NAME:
            first_name = emaildata['first_name']
            subject = subject.replace(data, first_name)
            body = body.replace(data, first_name)
            header = header.replace(data, first_name)
            footer = footer.replace(data, first_name)
        if data == CONST_EMAIL:
            email = email
            subject = subject.replace(data, email)
            body = body.replace(data, email)
            header = header.replace(data, email)
            footer = footer.replace(data, email)
        if data == CONST_LOGIN_BUTTON:
            link = ' <div style="padding: 20px; text-align: center;"> ' \
                   '<a href="www.majjaka.com">' \
                   '<button class="button-37" role="button" style="  background-color: #13aa52; border: 1px solid #13aa52; border-radius: 4px; box-shadow: rgba(0, 0, 0, .1) 0 2px 4px 0; box-sizing: border-box; color: #fff; cursor: pointer; font-size: 16px; font-weight: 400; outline: none; outline: 0; padding: 10px 25px; text-align: center; transform: translateY(0); user-select: none; -webkit-user-select: none; width: 50%;"> Login </button>' \
                   '</a> ' \
                   '</div>'
            body = body.replace(data, link)
        if data == CONST_MAJJAKA_LOGO:
            link = '<img src="cid:logo" width="100px" height="40px"> '
            body = body.replace(data, link)
            header = header.replace(data, link)
            footer = footer.replace(data, link)
        if data == CONST_RESET_LINK:
            link = '<a  href="http://127.0.0.1:8000/reset/c2hpbHBhLmlsa2FsQGhpcmFueWEtZ2FyYmhhLmNvbQ/set-password/"> ' \
                   'Reset Password </a> '
            body = body.replace(data, link)
        if data == CONST_SC_DESCRIPTION:
            sc_desc = emaildata['sc_description']
            subject = subject.replace(data, sc_desc)
            body = body.replace(data, sc_desc)
            header = header.replace(data, sc_desc)
            footer = footer.replace(data, sc_desc)
        if data == CONST_DOC_NUMBER:
            doc_num = emaildata['doc_number']
            subject = subject.replace(data, doc_num)
            body = body.replace(data, doc_num)
            header = header.replace(data, doc_num)
            footer = footer.replace(data, doc_num)

    # assigns to and from email
    to_mail = email

    context = {
        'username': username,
        'body': body,
        'header': header,
        'footer': footer,
    }
    # send_mail(subject, message.as_string(), From_Email, To_Email, fail_silently=True)
    FROM = "support@hiranya-garbha.com"
    TO = to_mail
    html_template = 'user_registration_email.html'
    html_message = render_to_string(html_template, {'context': context})

    message = EmailMessage(subject, html_message, FROM, [TO])
    message.content_subtype = 'html'  # this is required because there is no plain text email message
    # message.attach_file(path="D:/mystuff/table_list.txt", mimetype=DEFAULT_ATTACHMENT_MIME_TYPE)
    # message.send()

    with open(finders.find('img/HG.jpg'), 'rb') as f:
        logo_data1 = f.read()
    logo = MIMEImage(logo_data1)
    logo.add_header('Content-ID', '<logo>')
    logo.add_header('Content-ID', '<{}>'.format('img/HG.jpg'))
    message.mixed_subtype = 'related'
    # message.attach_alternative(html_message, "text/html")
    message.attach(logo)
    email_data = {}
    for details in emailDetail:
        email_data['email_contents_guid'] = details['email_contents_guid']
        email_data['object_type'] = details['object_type']
        email_data['username'] = username
        email_data['receiver_email'] = email
        email_data['sender_email'] = FROM
        email_data['email_user_monitoring_guid'] = guid
        email_data['client'] = client
    # Function to update the status to PROCESSING
    update_mail_status(email_data)

    email_status, error_type = error_handle(message)
    # if email_status == 1:
    #     error_type = 'NA'
    # elif email_status == 2:
    #     error_type = 'DATA ERROR'

    save_email_details(email_data, email_status, error_type)
    print("Email sent")

    return email_status


@lru_cache()
def logo_data():
    with open(finders.find('img/HG.jpg'), 'rb') as f:
        logo_data1 = f.read()
    logo = MIMEImage(logo_data1)
    logo.add_header('Content-ID', '<logo>')
    logo.add_header("Content-Disposition", "inline", filename="img/HG.jpg")
    return logo


def error_handle(message):
    status = 2
    try:
        status = message.send()
        error_type = 'NA'
        return status, error_type
    except BadHeaderError:
        status = 2
        error_type = 'Data Error'
        return status, error_type
    except smtplib.SMTPException as e:
        status = 2
        error_type = 'Data Error'
        return status, error_type
        # save_email_details(email_data, email_status, error_type)
        # print('There was an error sending an email.' + e)
    except:
        status = 2
        error_type = 'Network'
        return status, error_type


# def send_mail():
#     # date = datetime.now()
#     # print(date)
#     tmp = UserData.objects.filter(client='700', username='soni').values('email')
#     subject = 'test mail'
#     body = 'test'
#     email = tmp['email']
#     From_Email = settings.EMAIL_HOST_USER
#     To_Email = [email]
#     send_mail(subject, body, From_Email, To_Email, fail_silently=True)
# schedule.every(5).minutes.do(send_mail)
# while 1:
#     schedule.run_pending()
#     time.sleep(1)


def appr_notify(sc_header_instance, variant_name, client):
    """
    :return: return the Boolean value
    """
    # gets the email content based on the variant name emailDetail = django_query_instance.django_filter_only_query(
    # NotifSettings, {'variant_name': 'sc_approval'}).values('notif_subject' , 'notif_body')
    global user_details, item_qty, item_list, guid_note, approver_array, approver_name, app_name_val
    subject = ''
    body = ''
    header = ''
    footer = ''
    approver = ''
    decision_status = ''
    cost_object_val = ''
    doc_type = ''
    doc_num = ''
    currency = ''
    acc_val = ''
    doc_guid = sc_header_instance['email_document_monitoring_guid']

    print("sc_header_instance = ", sc_header_instance)
    emailDetail = list(django_query_instance.django_filter_only_query(EmailContents, {
        'object_type': variant_name, 'client': client
    }).values())

    user_res = django_query_instance.django_get_query(UserData, {
        'username': sc_header_instance['requester_username'], 'client': client, 'del_ind': False
    })
    header_res = sc_header_instance['po_header_details']
    appr_res = sc_header_instance['po_approver_details']
    for header in header_res:
        val = header['guid']
        doc_type = header['document_type']
        doc_num = header['doc_number']
    stp_no = sc_header_instance['step_num_inc']

    # po_header_details, po_approver_details, sc_completion, requester_first_name = get_sc_header_app(header_res,
    #                                                                                                 global_variables.GLOBAL_CLIENT)
    appr_res1 = django_query_instance.django_filter_query(ScPotentialApproval,
                                                          {'sc_header_guid': val,
                                                           'client': client}, ['step_num'], None)
    # appr_res1 = JsonParser_obj.get_json_from_obj(appr_res1)
    res_name = {}
    names = []
    lc = 1
    for sc in appr_res:
        # num = int(sc['step_num'])
        appr_step = django_query_instance.django_filter_query(ScPotentialApproval,
                                                              {'sc_header_guid': val,
                                                               'step_num': lc,
                                                               'client': client}, None, None)
        for step in appr_step:
            first_name = django_query_instance.django_filter_value_list_query(UserData, {
                'client': client, 'username': step['app_id']
            }, 'first_name')[0]
            names.append(first_name)
            sc['mgr_name'] = names
        names = []
        lc = lc + 1

        # print(sc.app_id, sc.step_num)
    req_name = sc_header_instance['requester_first_name']
    item_details = sc_header_instance['sc_item_details']
    acct_details = sc_header_instance['sc_accounting_details']
    mgr_details = sc_header_instance['manager_details']
    username_array = []
    mgr_names = []
    guid_val = ''
    for guid in header_res:
        guid_val = guid['guid']
        co_code = guid['co_code']
        total_val = guid['total_value']
        currency = guid['currency']
    for acc in acct_details:
        acc_val = acc['acc_cat']
        acct_desc = get_acct_description(acc['acc_cat'])
        cost_object = acc['acc_cat']
        cost_object_val = get_acc_detail(acc['guid'])

    appr_email = []

    if stp_no == 1:
        for res, mgr in zip(appr_res, mgr_details):
            mgr_array = (mgr['app_id_detail']).split(',')
            # username_array = mgr['app_id_detail']
            for m in set(mgr_array):
                first_name = django_query_instance.django_filter_value_list_query(UserData, {
                    'client': client, 'username': m
                }, 'first_name')[0]
                mgr_names.append(first_name)
                res['mgr_name'] = mgr_names
            mgr_names = []

        app_name_val = ''
        for app in appr_res:
            if app['step_num'] == '1':
                app_name_val = app['mgr_name']

        for name in app_name_val:
            appr_email.append(django_query_instance.django_filter_value_list_query(UserData, {
                'client': client, 'first_name': name
            }, 'email')[0])
    elif stp_no > 1:
        app_name_val = []
        appr_len = mgr_details['app_id_detail']

        if (len(sc_header_instance['manager_details'])) > 1:
            for app in mgr_details['app_id_detail']:
                app_name_val = app
                email_id = django_query_instance.django_filter_value_list_query(UserData, {
                    'client': client, 'username': app_name_val
                }, 'email')[0]
                appr_email.append(email_id)
        else:
            app_name_val = mgr_details['app_id_detail']
            email_id = django_query_instance.django_filter_value_list_query(UserData, {
                'client': client, 'username': mgr_details['app_id_detail']
            }, 'email')[0]
            appr_email.append(email_id)

        # manager_data, msg = get_manger_detail(client, req_name, acc_val, total_val, co_code, cost_object_val,
        #                                       currency)

        # mgr_names1 = []
        # for res, mgr in zip(appr_res, appr_res1):
        #     # mgr_array = (mgr['app_id_detail']).split(',')
        #     # username_array = mgr['app_id_detail']
        #     first_name = django_query_instance.django_filter_value_list_query(UserData, {
        #         'client': client, 'username': mgr['app_id']
        #     }, 'first_name')[0]
        #     mgr_names1.append(first_name)
        #     res['mgr_name'] = mgr_names1
        #     mgr_names1 = []

    # loop to separate the subject and body from query set
    for subValue in emailDetail:
        subject = subValue['subject']

    for bodyValue in emailDetail:
        body = bodyValue['body']
    for headerValue in emailDetail:
        header = headerValue['header']
    for footerValue in emailDetail:
        footer = footerValue['footer']

        #  this function separates the keywords from the content.
    subjectKeys = re.findall('\@.*?\@', subject)
    bodyKeys = re.findall('\@.*?\@', body)
    headerKeys = re.findall('\@.*?\@', header)
    footerKeys = re.findall('\@.*?\@', footer)
    keys = subjectKeys + bodyKeys + headerKeys + footerKeys

    # loop to assign the respective values based on the keywords from the email content
    for data in keys:
        if data == CONST_LOGIN_BUTTON:
            link = ' <div style="padding: 20px; text-align: center;"> ' \
                   '<a href="www.majjaka.com">' \
                   '<button class="button-37" role="button" style="  background-color: #13aa52; border: 1px solid #13aa52; border-radius: 4px; box-shadow: rgba(0, 0, 0, .1) 0 2px 4px 0; box-sizing: border-box; color: #fff; cursor: pointer; font-size: 16px; font-weight: 400; outline: none; outline: 0; padding: 10px 25px; text-align: center; transform: translateY(0); user-select: none; -webkit-user-select: none; width: 50%;"> Login </button>' \
                   '</a> ' \
                   '</div>'
            body = body.replace(data, link)

    From_Email = settings.EMAIL_HOST_USER
    # for mails in req_res:
    #     to_email = mails['email']
    item_list = {}

    if decision_status == 'AWAITING_APPROVAL':
        decision_status = 'AWAITING APPROVAL'
    approver_note = django_query_instance.django_filter_value_list_query(Notes, {'header_guid': guid_val,
                                                                                 'note_type': 'Approver Note'},
                                                                         'note_text')
    for val in acct_details:
        acct_desc = get_acct_description(val['acc_cat'])
        val['acct_desc'] = acct_desc

    for val in item_details:
        unit_desc = get_unit_description(val['unit'])
        val['unit_desc'] = unit_desc
    for keyWord in acct_details:
        cost_object = keyWord['acc_cat']
        cost_object_val = get_acc_detail(keyWord['guid'])

    context = {
        'body': body,
        'header': header,
        'footer': footer,
        'cost_object_val': cost_object_val,
        'item_list': item_list,
        'header_res': header_res,
        'appr_res': appr_res,
        'appr_res1': appr_res1,
        'req_name': req_name,
        'item_details': item_details,
        'acct_details': acct_details,
        'manager_details': mgr_details,
        'approver_note': approver_note,
        'user_lastname': user_res.last_name,
        'user_email': user_res.email
        # 'approver_array': approver_array
    }

    if approver != 'Multiple':
        user_details = django_query_instance.django_get_query(UserData, {
            'username': approver, 'client': client, 'del_ind': False
        })
    to_email = appr_email

    for mail in to_email:
        FROM = "support@hiranya-garbha.com"
        TO = mail
        html_template = 'sc_approval_html_email.html'
        html_message = render_to_string(html_template, {'context': context})

        message = EmailMessage(subject, html_message, FROM, [TO])
        message.content_subtype = 'html'  # this is required because there is no plain text email message

        with open(finders.find('img/HG.jpg'), 'rb') as f:
            logo_data1 = f.read()
        logo = MIMEImage(logo_data1)
        logo.add_header('Content-ID', '<logo>')
        logo.add_header('Content-ID', '<{}>'.format('img/HG.jpg'))
        message.mixed_subtype = 'related'
        # message.attach_alternative(html_message, "text/html")
        message.attach(logo)
        # main function to send an email.
        # sc_email_status, sc_email_error_type = error_handle(message)
        email_data = {}
        guid = guid_generator()
        for details in emailDetail:
            email_data['email_contents_guid'] = details['email_contents_guid']
            email_data['doc_type'] = 'DOC01'
            email_data['doc_num'] = doc_num
            email_data['object_type'] = details['object_type']
            email_data['username'] = req_name
            email_data['receiver_email'] = TO
            email_data['sender_email'] = FROM
            email_data['email_document_monitoring_guid'] = doc_guid
            email_data['client'] = client
        # Function to update the status to PROCESSING
        update_sc_mail_status(email_data)

        email_status, error_type = error_handle(message)
        # if email_status == 1:
        #     error_type = 'NA'
        # elif email_status == 2:
        #     error_type = 'DATA ERROR'

        save_sc_email_details(email_data, email_status, error_type)

    return True


def send_po_attachment_email(output, po_document_number, email_supp_monitoring_guid):
    """

    """
    global client_name, supp_name
    client = global_variables.GLOBAL_CLIENT
    po_supp_guid = email_supp_monitoring_guid
    supplier_id = ''
    po_details = django_query_instance.django_get_query(PoHeader, {
        'doc_number': po_document_number, 'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
    })
    sc_item_details = django_query_instance.django_filter_value_list_query(PoItem, {
            'po_header_guid': po_details.po_header_guid, 'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
        }, 'sc_item_guid')

    for supp in sc_item_details:
        supplier_id = django_query_instance.django_filter_value_list_query(ScItem, {
            'guid': supp, 'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
        }, 'supplier_id')

    supp_email = django_query_instance.django_filter_value_list_query(SupplierMaster, {
            'supplier_id': supplier_id[0], 'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
        }, 'email')

    client_data = django_query_instance.django_get_query(OrgClients, {
        'client': client, 'del_ind': False
    })
    emailDetail = list(django_query_instance.django_filter_only_query(EmailContents, {
        'object_type': 'PO_SUPPLIER', 'client': client,
    }).values())
    username = po_details.requester
    # loop to separate the subject and body from query set
    for subValue in emailDetail:
        subject = subValue['subject']

    for bodyValue in emailDetail:
        body = bodyValue['body']
    for headerValue in emailDetail:
        header = headerValue['header']
    for footerValue in emailDetail:
        footer = footerValue['footer']

    #  this function separates the keywords from the content.
    subjectKeys = re.findall('\@.*?\@', subject)
    bodyKeys = re.findall('\@.*?\@', body)
    headerKeys = re.findall('\@.*?\@', header)
    footerKeys = re.findall('\@.*?\@', footer)
    keys = subjectKeys + bodyKeys + headerKeys + footerKeys

    # loop to assign the respective values based on the keywords from the email content
    for data in keys:
        if data == CONST_DOC_NUMBER:
            doc_num = str(po_document_number)
            subject = subject.replace(data, doc_num)
            body = body.replace(data, doc_num)
            header = header.replace(data, doc_num)
            footer = footer.replace(data, doc_num)
        if data == CONST_USER_NAME:
            username = username
            subject = subject.replace(data, username)
            body = body.replace(data, username)
            header = header.replace(data, username)
            footer = footer.replace(data, username)
        if data == CONST_SUPPLIER_USERNAME:
            supp_name = po_details.supplier_id
            body = body.replace(data, supp_name)
            header = header.replace(data, supp_name)
            footer = footer.replace(data, supp_name)
        if data == CONST_CLIENT_NAME:
            client_name = client_data.description
            subject = subject.replace(data, client_name)
            body = body.replace(data, client_name)
            header = header.replace(data, client_name)
            footer = footer.replace(data, client_name)

    context = {
        'username': username,
        'client_name': client_name,
        'supp_name': supp_name,
        'body': body,
        'header': header,
        'footer': footer,
    }

    html_template = 'po_supplier_email.html'
    html_message = render_to_string(html_template, {'context': context})

    # message = EmailMessage(subject, html_message, FROM, [TO])
    TO = [po_details.supplier_email]
    #
    mail = EmailMultiAlternatives(subject, html_message, settings.EMAIL_HOST_USER, TO)
    mail.content_subtype = 'html'
    with open(str(output), 'rb') as file:
        attachment = file.read()
    file.close()
    print("send email", output)
    mail.attach(str(po_document_number), attachment, "application/pdf")
    mail.mixed_subtype = 'related'
    mail.send()

    email_data = {}
    for details in emailDetail:
        email_data['email_contents_guid'] = details['email_contents_guid']
        email_data['doc_type'] = po_details.document_type
        email_data['doc_num'] = po_document_number
        email_data['object_type'] = details['object_type']
        email_data['username'] = po_details.requester
        email_data['receiver_email'] = supp_email[0]
        email_data['sender_email'] = settings.EMAIL_HOST_USER
        email_data['email_supplier_monitoring_guid'] = po_supp_guid
        email_data['client'] = po_details.client_id

    email_status, error_type = error_handle(mail)
    save_supplier_email_details(email_data, email_status, error_type)
    return True


def save_email_details(emailDetail, email_status, error_type):
    if emailDetail['email_user_monitoring_guid']:
        django_query_instance.django_update_query(EmailUserMonitoring, {
            'email_user_monitoring_guid': emailDetail[
                'email_user_monitoring_guid']},
                                                  {'client': django_query_instance.django_get_query(OrgClients,
                                                                                                    {'client':
                                                                                                         emailDetail[
                                                                                                             'client']}),
                                                   'object_type': emailDetail['object_type'],
                                                   'username': emailDetail['username'],
                                                   'sender_email': emailDetail['sender_email'],
                                                   'receiver_email': emailDetail['receiver_email'],
                                                   'email_status': email_status,
                                                   'error_type': error_type,
                                                   'email_contents_guid': EmailContents.objects.get(
                                                       email_contents_guid=emailDetail['email_contents_guid'])
                                                   })
    else:
        guid = guid_generator()
        django_query_instance.django_create_query(EmailUserMonitoring, {'email_user_monitoring_guid': guid,
                                                                        'client': django_query_instance.django_get_query(
                                                                            OrgClients,
                                                                            {'client':
                                                                                 emailDetail[
                                                                                     'client']}),
                                                                        'object_type': emailDetail['object_type'],
                                                                        'username': emailDetail['username'],
                                                                        'sender_email': emailDetail['sender_email'],
                                                                        'receiver_email': emailDetail['receiver_email'],
                                                                        'email_status': email_status,
                                                                        'error_type': error_type,
                                                                        'email_contents_guid': EmailContents.objects.get(
                                                                            email_contents_guid=emailDetail[
                                                                                'email_contents_guid'])
                                                                        })
    return True


def update_mail_status(emailDetail):
    django_query_instance.django_update_query(EmailUserMonitoring,
                                              {'email_user_monitoring_guid': emailDetail['email_user_monitoring_guid']
                                               }, {'client': global_variables.GLOBAL_CLIENT,
                                                   'email_status': 3,
                                                   'email_contents_guid': EmailContents.objects.get(
                                                       email_contents_guid=emailDetail[
                                                           'email_contents_guid'])
                                                   })
    return True


def get_acct_description(acct_cat):
    acct_cat_desc = django_query_instance.django_get_query(AccountAssignmentCategory, {
        'account_assign_cat': acct_cat
    })
    return acct_cat_desc.description


def get_unit_description(unit):
    unit_desc = django_query_instance.django_get_query(UnitOfMeasures, {
        'uom_id': unit
    })
    return unit_desc.uom_description


def save_sc_email_details(emailDetail, email_status, error_type):
    if emailDetail['email_document_monitoring_guid']:
        django_query_instance.django_update_query(EmailDocumentMonitoring, {
            'email_document_monitoring_guid': emailDetail[
                'email_document_monitoring_guid']},
                                                  {'client': django_query_instance.django_get_query(OrgClients,
                                                                                                    {'client':
                                                                                                         emailDetail[
                                                                                                             'client']}),
                                                   'object_type': emailDetail['object_type'],
                                                   'doc_type': emailDetail['doc_type'],
                                                   'doc_number': emailDetail['doc_num'],
                                                   'sender_email': emailDetail['sender_email'],
                                                   'receiver_email': emailDetail['receiver_email'],
                                                   'email_status': email_status,
                                                   'error_type': error_type,
                                                   'email_contents_guid': EmailContents.objects.get(
                                                       email_contents_guid=emailDetail['email_contents_guid'])
                                                   })
    else:
        guid = guid_generator()
        django_query_instance.django_create_query(EmailDocumentMonitoring, {'email_document_monitoring_guid': guid,
                                                                            'client': global_variables.GLOBAL_CLIENT,
                                                                            'object_type': emailDetail['object_type'],
                                                                            'doc_type': emailDetail['doc_type'],
                                                                            'doc_number': emailDetail['doc_num'],
                                                                            'sender_email': emailDetail['sender_email'],
                                                                            'receiver_email': emailDetail[
                                                                                'receiver_email'],
                                                                            'email_status': email_status,
                                                                            'error_type': error_type,
                                                                            'email_contents_guid': EmailContents.objects.get(
                                                                                email_contents_guid=emailDetail[
                                                                                    'email_contents_guid'])
                                                                            })
    return True


def update_sc_mail_status(emailDetail):
    django_query_instance.django_update_query(EmailDocumentMonitoring,
                                              {'email_document_monitoring_guid': emailDetail[
                                                  'email_document_monitoring_guid']
                                               }, {'client': global_variables.GLOBAL_CLIENT,
                                                   'email_status': 3,
                                                   'email_contents_guid': EmailContents.objects.get(
                                                       email_contents_guid=emailDetail[
                                                           'email_contents_guid'])
                                                   })
    return True


def save_supplier_email_details(emailDetail, email_status, error_type):
    if emailDetail['email_supplier_monitoring_guid']:
        django_query_instance.django_update_query(EmailSupplierMonitoring, {
            'email_supplier_monitoring_guid': emailDetail[
                'email_supplier_monitoring_guid']},
                                                  {'client': django_query_instance.django_get_query(OrgClients,
                                                                                                    {'client':
                                                                                                         emailDetail[
                                                                                                             'client']}),
                                                   'object_type': emailDetail['object_type'],
                                                   'doc_type': emailDetail['doc_type'],
                                                   'doc_number': emailDetail['doc_num'],
                                                   'sender_email': emailDetail['sender_email'],
                                                   'receiver_email': emailDetail['receiver_email'],
                                                   'email_status': email_status,
                                                   'error_type': error_type,
                                                   'email_contents_guid': EmailContents.objects.get(
                                                       email_contents_guid=emailDetail['email_contents_guid'])
                                                   })
    else:
        guid = guid_generator()
        django_query_instance.django_create_query(EmailSupplierMonitoring, {'email_supplier_monitoring_guid': guid,
                                                                            'client': global_variables.GLOBAL_CLIENT,
                                                                            'object_type': emailDetail['object_type'],
                                                                            'doc_type': emailDetail['doc_type'],
                                                                            'doc_number': emailDetail['doc_num'],
                                                                            'sender_email': emailDetail['sender_email'],
                                                                            'receiver_email': emailDetail[
                                                                                'receiver_email'],
                                                                            'email_status': email_status,
                                                                            'error_type': error_type,
                                                                            'email_contents_guid': EmailContents.objects.get(
                                                                                email_contents_guid=emailDetail[
                                                                                    'email_contents_guid'])
                                                                            })
    return True
