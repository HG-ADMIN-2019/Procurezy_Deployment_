# Utility functions for search functionality
# Utils is a collection of small functions and classes which make common patterns shorter and easier.

import os

from django.db.models.query_utils import Q
from django.http import Http404
from Majjaka_eProcure import settings
from eProc_Attributes.Utilities.attributes_generic import OrgAttributeValues
from eProc_Basic.Utilities.constants.constants import CONST_SC_HEADER_APPROVED, CONST_COMPLETED, CONST_SC_APPR_APPROVED, \
    CONST_SC_HEADER_AWAITING_APPROVAL, CONST_ACTIVE, CONST_AUTO, CONST_INITIATED, CONST_SC_APPR_OPEN, CONST_PR_CALLOFF, \
    CONST_CALENDAR_ID, CONST_CATALOG_CALLOFF, CONST_SUPPLIER_NOTE, CONST_INTERNAL_NOTE, CONST_APPROVER_NOTE, \
    CONST_DEFAULT_LANGUAGE, CONST_GLACC, CONST_SC_HEADER_DELETED, CONST_DOC_TYPE_SC
from eProc_Basic.Utilities.functions.dict_check_key import checkKey
from eProc_Basic.Utilities.functions.dictionary_key_to_list import dictionary_key_to_list
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients, get_object_id_from_username, update_requester_info
from eProc_Basic.Utilities.functions.type_casting import type_cast_array_str_to_decimal
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Calendar_Settings.Utilities.calender_settings_generic import calculate_delivery_date
from eProc_Configuration.models import ImagesUpload
from eProc_Configuration.models.development_data import AccountAssignmentCategory
from eProc_Configuration.models.master_data import AccountingDataDesc
from eProc_Doc_Details.Utilities.details_specific import get_notes
from eProc_Doc_Search_and_Display.Utilities.search_display_specific import get_shopping_cart_approval
from eProc_Emails.Utilities.email_notif_generic import get_unit_description
from eProc_Exchange_Rates.Utilities.exchange_rates_generic import convert_currency
from eProc_Notes_Attachments.models import Attachments, Notes
from eProc_Price_Calculator.Utilities.price_calculator_generic import calculate_item_total_value
from eProc_Purchase_Order.models.purchase_order import *

# Importing  the models from m_database app
from eProc_Registration.models.registration_model import UserData
from eProc_Related_Documents.Utilities.related_documents_generic import get_item_level_related_documents
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import update_eform_details_scitem, get_image_url, \
    get_currency_converted_price_data
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import get_login_user_spend_limit, update_supplier_desc

from eProc_Shopping_Cart.models import *
import datetime

from eProc_Shopping_Cart.models.shopping_cart import ScHeader, ScItem, ScAccounting, ScAddresses, ScApproval, \
    ScPotentialApproval

django_query_instance = DjangoQueries()
from eProc_User_Settings.Utilities.user_settings_generic import get_object_id_list_user


# Get Item, Accounting and Approval details from header guid
def get_doc_details(type, hdr_guid):
    if type == 'SC':
        hdr_obj = ScHeader()
        itm_obj = ScItem()
        acc_obj = ScAccounting()
        appr_obj = ScApproval()
        addr_obj = ScAddresses()
    elif type == 'PO':
        hdr_obj = PoHeader()
        itm_obj = PoItem()
        acc_obj = PoAccounting()
        appr_obj = PoApproval()
    else:
        raise Http404
    hdr_data = hdr_obj.get_hdr_data_by_guid(hdr_guid)
    itm_data = itm_obj.get_itms_by_guid(hdr_guid)
    itm_guids = []
    for item in itm_data:
        itm_guids.append(getattr(item, 'guid'))
    acc_data = acc_obj.get_acc_data_by_guid(itm_guids)
    appr_data = appr_obj.get_apprs_by_guid(hdr_guid)
    addr_data = addr_obj.get_addr_by_guid(itm_guids)
    return {'hdr_data': hdr_data, 'itm_data': itm_data, 'acc_data': acc_data, 'appr_data': appr_data,
            'addr_data': addr_data}


def get_shopping_cart_details(hdr_guid):
    """

    """
    sc_header_details = []
    sc_item_details = []
    sc_account_details = []
    sc_address_details = []
    sc_approval_details = []
    sc_potential_approval_details = []
    if django_query_instance.django_existence_check(ScHeader,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'guid': hdr_guid,
                                                     'del_ind': False}):
        sc_header_details = django_query_instance.django_filter_query(ScHeader,
                                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                                       'guid': hdr_guid,
                                                                       'del_ind': False},
                                                                      None,
                                                                      None)
        sc_item_details = django_query_instance.django_filter_query(ScItem,
                                                                    {'header_guid': hdr_guid,
                                                                     'client': global_variables.GLOBAL_CLIENT,
                                                                     'del_ind': False},
                                                                    ['item_num'],
                                                                    None)
        sc_item_guid = dictionary_key_to_list(sc_item_details, 'guid')
        sc_account_details = django_query_instance.django_filter_query(ScAccounting,
                                                                       {'client': global_variables.GLOBAL_CLIENT,
                                                                        'item_guid__in': sc_item_guid,
                                                                        'del_ind': False},
                                                                       ['acc_item_num'],
                                                                       None)
        sc_address_details = django_query_instance.django_filter_query(ScAddresses,
                                                                       {'client': global_variables.GLOBAL_CLIENT,
                                                                        'item_guid__in': sc_item_guid,
                                                                        'del_ind': False},
                                                                       ['item_guid'],
                                                                       None)
        sc_approval_details = django_query_instance.django_filter_query(ScApproval,
                                                                        {'header_guid': hdr_guid,
                                                                         'client': global_variables.GLOBAL_CLIENT,
                                                                         'del_ind': False},
                                                                        ['step_num'],
                                                                        None)
        sc_approval_guid = dictionary_key_to_list(sc_approval_details, 'guid')
        sc_potential_approval_details = django_query_instance.django_filter_query(ScPotentialApproval,
                                                                                  {
                                                                                      'sc_approval_guid__in': sc_approval_guid},
                                                                                  ['step_num'],
                                                                                  None)
    data = {'sc_header_details': sc_header_details,
            'sc_item_details': sc_item_details,
            'sc_account_details': sc_account_details,
            'sc_address_details': sc_address_details,
            'sc_approval_details': sc_approval_details,
            'sc_potential_approval_details': sc_potential_approval_details}
    return data


def get_sc_supplier_internal_approver_note(header_guid, sc_item_guid_list):
    """

    """
    supp_notes = get_notes(header_guid, sc_item_guid_list, CONST_SUPPLIER_NOTE, True)
    int_notes = get_notes(header_guid, sc_item_guid_list, CONST_INTERNAL_NOTE, True)
    appr_notes = get_notes(header_guid, sc_item_guid_list, CONST_APPROVER_NOTE, False)
    return supp_notes, int_notes, appr_notes


# Get attachments by path
class GetAttachments:
    po_attachments = []

    @staticmethod
    def get_sc_attachments(guid):
        attachment_data = []
        if Attachments.objects.filter(header_guid=guid).exists():
            attachment_file_path = Attachments.objects.filter(header_guid=guid).order_by('item_num')
            for attachments in attachment_file_path:
                item_guid = attachments.item_guid
                file_path = str(attachments.doc_file)
                split_file_path = file_path.split('/')
                file_path = '/'.join(split_file_path[:-1])
                file_path = 'media/' + file_path
                GetAttachments.get_all_files(file_path, item_guid)
                file_name = split_file_path[6]
                attachment_dict = {
                    'attachment_guid': attachments.guid,
                    'item_guid': attachments.item_guid,
                    'file_name': file_name,
                    'file_path': file_path + '/' + file_name,
                    'attachment_name': attachments.title,
                    'type': attachments.attach_type_flag,
                    'item_num': attachments.item_num,
                }
                attachment_data.append(attachment_dict)
        return attachment_data

    @staticmethod
    def get_attachments_by_item_number(document_number, item_guid):
        available_attachments = Attachments.objects.filter(doc_num=document_number, item_guid=item_guid,
                                                           del_ind=False).order_by('item_num')
        attachment_data = []
        if available_attachments:
            attachment_file_path = available_attachments
            for attachments in attachment_file_path:
                item_guid = attachments.item_guid
                file_path = str(attachments.doc_file)
                split_file_path = file_path.split('/')
                file_path = '/'.join(split_file_path[:-1])
                file_path = 'media/' + file_path
                GetAttachments.get_all_files(file_path, item_guid)
                file_name = split_file_path[6]
                attachment_dict = {
                    'attachment_guid': attachments.guid,
                    'item_guid': attachments.item_guid,
                    'file_name': file_name,
                    'file_path': file_path + '/' + file_name,
                    'attachment_name': attachments.title,
                    'type': attachments.attach_type_flag,
                    'item_num': attachments.item_num,
                }
                attachment_data.append(attachment_dict)
        return attachment_data

    def get_attachments(self, req, hdr_guid):  # Get attachments by PO header guid
        client = getClients(req)  # To get logged in users client
        self.po_attachments = []
        hdr_obj = PoHeader()
        objid = hdr_obj.get_objid_by_guid(hdr_guid)
        item_guid = ''
        attach_dir = settings.ATTACH_PATH + '/' + client + '/Attachments'  # Get attachments path by settings.py file
        attach_file_path = None
        if os.path.exists(attach_dir):
            dir_list = os.listdir(attach_dir)
            for dir in dir_list:
                if attach_file_path is None:
                    tmp_file = attach_dir + '/' + dir
                    if os.path.exists(tmp_file):
                        sub_list = os.listdir(tmp_file)
                        for subfile in sub_list:
                            sub_path = tmp_file + '/' + subfile
                            if os.path.exists(sub_path) and subfile == objid:
                                attach_file_path = sub_path
                                break
                else:
                    break
        if attach_file_path is not None:
            self.get_all_files(attach_file_path, item_guid)
        return self.po_attachments

    # To get all files inside the attachments and popdf's
    @staticmethod
    def get_all_files(path, item_guid):
        if os.path.exists(path):
            if os.path.isfile(path):
                path = path.replace('&', '%26')
                return GetAttachments.po_attachments.append((path, os.path.basename(path), item_guid))
            elif os.path.isdir(path):
                for subfile in os.listdir(path):
                    GetAttachments.get_all_files(path + '/' + subfile, item_guid)

    # Get POPDF files by Header guid
    def get_popdf(self, req, hdr_guid):
        file_list = []
        objid = PoHeader.get_objid_by_guid(hdr_guid)
        client = getClients(req)  # To get logged in users client
        # POPODF path based on user client
        pdf_path = settings.ATTACH_PATH + '/' + client + '/POPDF/PO_' + objid  # Get POPDF path by settings.py
        if os.path.exists(pdf_path):
            directory = os.listdir(pdf_path)
            for files in directory:
                fname = pdf_path + '/' + files
                fname = fname.replace('&', '%26')
                pdf = (fname, files)
                file_list.append(pdf)
                return file_list


def update_sc_data(sc_data, scheader_guid):
    """

    :param sc_data:
    :param scheader_guid:
    :return:
    """
    # update ScHeader change
    hdr_obj = ScHeader
    save_update_sc(sc_data, hdr_obj, 'ScHeader', 'guid', scheader_guid)

    # update ScAccounting change
    hdr_obj = ScAccounting
    save_update_sc(sc_data, hdr_obj, 'ScAccounting', 'guid', scheader_guid)

    # update ScAddresses change
    hdr_obj = ScAddresses
    save_update_sc(sc_data, hdr_obj, 'ScAddresses', 'guid', scheader_guid)

    # update Notes change
    hdr_obj = Notes
    save_update_sc(sc_data, hdr_obj, 'Notes', 'guid', scheader_guid)

    # update ScItem change
    hdr_obj = ScItem
    save_update_sc(sc_data, hdr_obj, 'ScItem', 'guid', scheader_guid)


def save_update_sc(sc_data, db_table_name, db_name, pk_value, header_guid):
    scitem_dictionary = []
    org_attr_value_instance = OrgAttributeValues()
    sc_header_instance = ScHeader.objects.get(guid=header_guid)
    sc_requester = sc_header_instance.requester
    user_object_id = get_object_id_from_username(sc_requester)
    object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT, user_object_id)
    default_calendar_id = org_attr_value_instance.get_user_default_attr_value_list_by_attr_id(object_id_list,
                                                                                              CONST_CALENDAR_ID)[1]
    for field, field_value in sc_data.items():
        update_dict = {}
        flag = 0
        match = re.search('(\w+)-(\w+)-(\w+)', field)
        if match is not None:
            if db_name == match.group(1):
                if not hasattr(update_dict, pk_value):
                    update_dict[pk_value] = match.group(3)
                    update_dict[match.group(2)] = field_value
                for val in scitem_dictionary:
                    if val[pk_value] == update_dict[pk_value]:
                        val.update(update_dict)
                        flag = 1
                if not scitem_dictionary or not flag:
                    scitem_dictionary.append(update_dict)

    item_guid = {}

    for scitem in scitem_dictionary:
        item_guid[pk_value] = str(list(scitem.values())[0])
        if db_name == 'ScItem':
            item_instance = ScItem.objects.get(guid=item_guid[pk_value])
            # if item_instance.call_off == CONST_PR_CALLOFF:
            #     calculate_delivery_date(item_guid[pk_value], int(item_instance.lead_time), scitem['supplier_id'],
            #                             default_calendar_id, global_variables.GLOBAL_CLIENT, ScItem)

            quantity, catalog_qty, price_unit, price, overall_limit = check_key_exist(scitem, item_instance)
            item_total_value = calculate_item_total_value(item_instance.call_off, quantity, catalog_qty, price_unit,
                                                          price, overall_limit)
            if sc_header_instance.currency != item_instance.currency:
                item_total_value = convert_currency(item_total_value, str(item_instance.currency),
                                                    str(sc_header_instance.currency))

            scitem['value'] = item_total_value
            if item_instance.call_off == CONST_CATALOG_CALLOFF:
                scitem['quantity'] = catalog_qty
        if db_name == 'ScAddresses':
            item_guid['address_type'] = 'D'
        save_sc_item_details_to_db(db_table_name, scitem, **item_guid)


def update_approval_status(scheader_guid):
    """

    :param scheader_guid:
    :return:
    """
    app_id = ''
    sc_approval = ScApproval.objects.filter(header_guid=scheader_guid).order_by('-step_num').first()
    received_time, proc_time = get_received_proc_time(sc_approval)
    proc_lvl_sts, app_sts = get_proc_appr_level_status(sc_approval)
    if django_query_instance.django_existence_check(ScPotentialApproval,
                                                    {'sc_header_guid': scheader_guid,
                                                     'client': global_variables.GLOBAL_CLIENT,
                                                     'del_ind': False}):
        app_id = django_query_instance.django_filter_value_list_query(ScPotentialApproval,
                                                                      {'sc_header_guid': scheader_guid,
                                                                       'client': global_variables.GLOBAL_CLIENT,
                                                                       'del_ind': False},
                                                                      'app_id')[0]
    django_query_instance.django_update_query(ScApproval,
                                              {'header_guid': scheader_guid,
                                               'client': global_variables.GLOBAL_CLIENT,
                                               'del_ind': False},
                                              {'received_time': received_time,
                                               'proc_time': proc_time,
                                               'proc_lvl_sts': proc_lvl_sts,
                                               'app_sts': app_sts})
    return app_id

    # sc_approval.received_time = received_time
    # sc_approval.proc_time = proc_time
    # sc_approval.proc_lvl_sts = proc_lvl_sts
    # sc_approval.app_sts = app_sts
    # sc_approval.save()


def get_received_proc_time(sc_approval):
    """

    :param sc_approval:
    :return:
    """
    received_time = None
    proc_time = None
    if sc_approval.app_id == CONST_AUTO:
        received_time = datetime.datetime.now()
        proc_time = datetime.datetime.now()
    elif int(sc_approval.step_num) == 1:
        received_time = datetime.datetime.now()
    return received_time, proc_time


def get_proc_appr_level_status(sc_approval):
    """

    :param sc_approval:
    :return:
    """
    proc_lvl_sts = CONST_INITIATED
    app_sts = CONST_SC_APPR_OPEN
    if int(sc_approval.step_num) == 1:
        proc_lvl_sts = CONST_ACTIVE
    if sc_approval.app_id == CONST_AUTO:
        proc_lvl_sts = CONST_COMPLETED
        app_sts = CONST_SC_APPR_APPROVED
    return proc_lvl_sts, app_sts


def check_key_exist(scitem, item_instance):
    """

    :param scitem:
    :param item_instance:
    :return:
    """
    catalog_qty = None
    if checkKey(scitem, 'quantity'):
        quantity = scitem['quantity']
    else:
        quantity = item_instance.quantity

    if checkKey(scitem, 'catalog_qty'):
        catalog_qty = scitem['catalog_qty']
        quantity = catalog_qty
    elif item_instance == CONST_CATALOG_CALLOFF:
        catalog_qty = item_instance.catalog_qty
        quantity = catalog_qty

    if checkKey(scitem, 'price_unit'):
        price_unit = scitem['price_unit']
    else:
        price_unit = item_instance.price_unit

    if checkKey(scitem, 'price'):
        price = scitem['price']
    else:
        price = item_instance.price

    if checkKey(scitem, 'overall_limit'):
        overall_limit = scitem['overall_limit']
    else:
        overall_limit = item_instance.overall_limit

    return quantity, catalog_qty, price_unit, price, overall_limit


def save_sc_item_details_to_db(db_table_name, sc_item_details, **kwargs):
    db_table_name.objects.update_or_create(**kwargs, defaults=sc_item_details)


def update_scheader_approval_status(scheader_guid):
    """

    :param scheader_guid:
    :return:
    """
    sc_header_instant = ScHeader.objects.get(guid=scheader_guid)
    login_user_spend_limit, sl_code_id = get_login_user_spend_limit(sc_header_instant.co_code,
                                                                    global_variables.GLOBAL_CLIENT,
                                                                    sc_header_instant.requester)
    if float(sc_header_instant.total_value) < float(login_user_spend_limit):
        ScHeader.objects.filter(guid=scheader_guid).update(status=CONST_SC_HEADER_APPROVED)
        ScApproval.objects.filter(header_guid=scheader_guid).update(proc_lvl_sts=CONST_COMPLETED,
                                                                    app_sts=CONST_SC_APPR_APPROVED,
                                                                    received_time=datetime.datetime.now(),
                                                                    proc_time=datetime.datetime.now())
    else:
        ScHeader.objects.filter(guid=scheader_guid).update(status=CONST_SC_HEADER_AWAITING_APPROVAL)
        ScApproval.objects.filter(header_guid=scheader_guid).update(proc_lvl_sts=CONST_ACTIVE,
                                                                    received_time=datetime.datetime.now())


def update_eform_scitem(header_guid):
    """

    """
    item_dictionary_list = django_query_instance.django_filter_query(ScItem,
                                                                     {'header_guid': header_guid,
                                                                      'client': global_variables.GLOBAL_CLIENT,
                                                                      'del_ind': False},
                                                                     ['item_num'], None)
    item_dictionary_list = update_eform_details_scitem(item_dictionary_list)
    for item_dictionary in item_dictionary_list:
        if item_dictionary['call_off'] == CONST_CATALOG_CALLOFF:
            item_dictionary['image_url'] = get_image_url(item_dictionary['int_product_id'])
        else:
            item_dictionary['image_url'] = ''
    return item_dictionary_list


def get_sc_detail(header_guid):
    """

    """
    sc_header_detail = {}
    sc_item_level_address = []
    sc_item_details = []
    sc_accounting_details = []
    sc_header_level_address = {}
    sc_approval_details = []
    requester_first_name = ''
    sc_completion = []
    sc_header = []
    sc_header_level_acc = []
    sc_item_level_acc = []
    supp_notes = []
    int_notes = []
    appr_notes = []
    total_item_value = []
    actual_price = []
    discount_value = []
    tax_value = []
    sc_attachments = []
    highest_item_guid = ''
    org_attr_value_instance = OrgAttributeValues()
    object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT, global_variables.GLOBAL_LOGIN_USER_OBJ_ID)
    default_calendar_id = org_attr_value_instance.get_user_default_attr_value_list_by_attr_id(object_id_list,
                                                                                              CONST_CALENDAR_ID)[1]
    if django_query_instance.django_existence_check(ScHeader,
                                                    {'guid': header_guid,
                                                     'client': global_variables.GLOBAL_CLIENT,
                                                     'del_ind': False}):
        sc_header_details = django_query_instance.django_filter_query(ScHeader,
                                                                      {'guid': header_guid,
                                                                       'client': global_variables.GLOBAL_CLIENT,
                                                                       'del_ind': False},
                                                                      None,
                                                                      None)
        sc_header_detail = sc_header_details[0]
        update_requester_info(sc_header_detail['requester'])
        sc_item_details = django_query_instance.django_filter_query(ScItem,
                                                                    {'header_guid': header_guid,
                                                                     'client': global_variables.GLOBAL_CLIENT,
                                                                     },
                                                                    ['item_num'],
                                                                    None)
        highest_item_guid = get_highest_item_guid_detail(sc_item_details)
        for sc_item_detail in sc_item_details:
            sc_item_detail['related_documents'] = get_item_level_related_documents(sc_item_detail,
                                                                                   CONST_DOC_TYPE_SC,
                                                                                   sc_item_detail['po_doc_num'])
            sc_item_detail['unit_desc'] = get_unit_description(sc_item_detail['unit'])
            sc_item_detail ['item_del_date'] = calculate_delivery_date(sc_item_detail['guid'],
                                                                       int(sc_item_detail['lead_time']), sc_item_detail['supplier_id'],
                                                    default_calendar_id, global_variables.GLOBAL_CLIENT,
                                                    ScItem)
            update_supplier_desc(sc_item_detail)
        actual_price, discount_value, tax_value, total_item_value, sc_item_details = get_currency_converted_price_data(
            sc_item_details)
        sc_item_guid_list = dictionary_key_to_list(sc_item_details, 'guid')
        filter_queue = Q(header_guid=header_guid) | Q(item_guid__in=sc_item_guid_list)
        sc_accounting_details = django_query_instance.django_queue_query(ScAccounting,
                                                                         {'client': global_variables.GLOBAL_CLIENT},
                                                                         filter_queue,
                                                                         ['acc_item_num'],
                                                                         None)
        sc_address_details = django_query_instance.django_queue_query(ScAddresses,
                                                                      {'address_type': 'D',
                                                                       'client': global_variables.GLOBAL_CLIENT,
                                                                      },
                                                                      filter_queue,
                                                                      ['item_num'],
                                                                      None)
        for sc_address_detail in sc_address_details:
            if sc_address_detail['header_guid_id'] == header_guid:
                sc_header_level_address = sc_address_detail
            else:
                sc_item_level_address.append(sc_address_detail)
        acc_cat = dictionary_key_to_list(sc_accounting_details, 'acc_cat')
        acc_cat_detail = get_acc_description(acc_cat)
        for sc_accounting_detail in sc_accounting_details:
            if sc_accounting_detail['acc_cat']:
                sc_accounting_detail['acc_desc'] = get_acc_detail_desc(acc_cat_detail, sc_accounting_detail['acc_cat'])
                sc_accounting_detail['acc_value_desc'] = get_acc_value_description(sc_accounting_detail,
                                                                                   sc_header_detail['co_code'])
                sc_accounting_detail['gl_account_value_desc'] = get_gl_acc_desc(sc_accounting_detail,
                                                                                sc_header_detail['co_code'])
            if sc_accounting_detail['header_guid_id'] == header_guid:
                sc_header_level_acc.append(sc_accounting_detail)
            else:
                sc_item_level_acc.append(sc_accounting_detail)
        sc_approval_details = django_query_instance.django_filter_query(ScApproval,
                                                                        {'header_guid': header_guid,
                                                                         'client': global_variables.GLOBAL_CLIENT,
                                                                         },
                                                                        ['step_num'],
                                                                        None)
        sc_potential_approval_details = django_query_instance.django_filter_query(ScPotentialApproval,
                                                                                  {'sc_header_guid': header_guid,
                                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                                   },
                                                                                  ['step_num'],
                                                                                  None)
        supp_notes, int_notes, appr_notes = get_sc_supplier_internal_approver_note(header_guid, sc_item_guid_list)
        data = {'sc_item_details': sc_item_details,
                'sc_approval_details': sc_approval_details,
                'sc_potential_approval_details': sc_potential_approval_details,
                'sc_header_details': sc_header_details}

        sc_header, sc_appr, sc_completion, requester_first_name = get_shopping_cart_approval(data)
        GetAttachments.po_attachments = []
        sc_attachments = GetAttachments.get_sc_attachments(header_guid)

    requester_full_name = django_query_instance.django_get_query(UserData,
                                                                 {'username': sc_header_detail['requester'],
                                                                  'client': global_variables.GLOBAL_CLIENT})
    shopping_cart_detail = {'hdr_det': sc_header_detail,
                            'item_dictionary_list': sc_item_details,
                            'header_acc_detail': sc_header_level_acc,
                            'acc_det': sc_item_level_acc,
                            'header_level_addr': sc_header_level_address,
                            'addr_det': sc_item_level_address,
                            'sc_appr': sc_approval_details,
                            'sc_head': sc_header_detail,
                            'requester_first_name': requester_first_name,
                            'sc_completion': sc_completion,
                            'sc_header': sc_header,
                            'is_document_detail': True,
                            'supp_notes': supp_notes,
                            'int_notes': int_notes,
                            'appr_notes': appr_notes,
                            'edit_address_flag': '0',
                            'acct_assignment_category': '0',
                            'button_status': False,
                            'requester_full_name': requester_full_name,
                            'total_value': format(total_item_value, '.2f'),
                            'actual_price': format(actual_price, '.2f'),
                            'discount_value': format(discount_value, '.2f'),
                            'tax_value': format(tax_value, '.2f'),
                            'highest_item_guid': highest_item_guid,
                            'sc_attachements':sc_attachments
                            }
    return shopping_cart_detail


def get_acc_description(acc):
    """

    """
    acc_value_desc = django_query_instance.django_filter_query(AccountAssignmentCategory,
                                                               {'account_assign_cat__in': acc,
                                                                'del_ind': False},
                                                               None,
                                                               ['account_assign_cat', 'description'])
    return acc_value_desc


def get_acc_value_description(sc_accounting_detail, company_code):
    """

    """
    acc_desc_detail = None
    acc_desc = ''
    acc_value = get_account_asg_value(sc_accounting_detail)
    if django_query_instance.django_existence_check(AccountingDataDesc,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'del_ind': False,
                                                     'account_assign_cat': sc_accounting_detail['acc_cat'],
                                                     'account_assign_value': acc_value,
                                                     'company_id': company_code,
                                                     'language_id': global_variables.GLOBAL_USER_LANGUAGE}):
        acc_desc_detail = django_query_instance.django_filter_query(AccountingDataDesc,
                                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                                     'del_ind': False,
                                                                     'account_assign_cat': sc_accounting_detail[
                                                                         'acc_cat'],
                                                                     'account_assign_value': acc_value,
                                                                     'company_id': company_code,
                                                                     'language_id': global_variables.GLOBAL_USER_LANGUAGE},
                                                                    None,
                                                                    None)[0]
    elif django_query_instance.django_existence_check(AccountingDataDesc,
                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                       'del_ind': False,
                                                       'account_assign_cat': sc_accounting_detail['acc_cat'],
                                                       'account_assign_value': acc_value,
                                                       'company_id': company_code,
                                                       'language_id': CONST_DEFAULT_LANGUAGE}):
        acc_desc_detail = django_query_instance.django_filter_query(AccountingDataDesc,
                                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                                     'del_ind': False,
                                                                     'account_assign_cat': sc_accounting_detail[
                                                                         'acc_cat'],
                                                                     'account_assign_value': acc_value,
                                                                     'company_id': company_code,
                                                                     'language_id': CONST_DEFAULT_LANGUAGE},
                                                                    None,
                                                                    None)[0]
    if acc_desc_detail:
        acc_desc = acc_desc_detail['account_assign_value'] + ' - ' + acc_desc_detail['description']
    return acc_desc


def get_account_asg_value(sc_accounting_detail):
    """

    """
    account_assignment_category = sc_accounting_detail['acc_cat']
    if account_assignment_category == 'CC':
        account_assignment_value = sc_accounting_detail['cost_center']

    elif account_assignment_category == 'AS':
        account_assignment_value = sc_accounting_detail['asset_number']

    elif account_assignment_category == 'OR':
        account_assignment_value = sc_accounting_detail['internal_order']

    else:
        account_assignment_value = sc_accounting_detail['wbs_ele']
    return account_assignment_value


def get_acc_detail_desc(acc_cat_details, acc_cat):
    """

    """
    for acc_cat_detail in acc_cat_details:
        if acc_cat_detail['account_assign_cat'] == acc_cat:
            return acc_cat + ' - ' + acc_cat_detail['description']
    return acc_cat


def get_gl_acc_desc(sc_accounting_detail, company_code):
    """

    """
    acc_desc_detail = None
    acc_desc = ''
    if django_query_instance.django_existence_check(AccountingDataDesc,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'del_ind': False,
                                                     'account_assign_cat': CONST_GLACC,
                                                     'account_assign_value': sc_accounting_detail['gl_acc_num'],
                                                     'company_id': company_code,
                                                     'language_id': global_variables.GLOBAL_USER_LANGUAGE}):
        acc_desc_detail = django_query_instance.django_filter_query(AccountingDataDesc,
                                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                                     'del_ind': False,
                                                                     'account_assign_cat': CONST_GLACC,
                                                                     'account_assign_value': sc_accounting_detail[
                                                                         'gl_acc_num'],
                                                                     'company_id': company_code,
                                                                     'language_id': global_variables.GLOBAL_USER_LANGUAGE},
                                                                    None,
                                                                    None)[0]
    elif django_query_instance.django_existence_check(AccountingDataDesc,
                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                       'del_ind': False,
                                                       'account_assign_cat': CONST_GLACC,
                                                       'account_assign_value': sc_accounting_detail['gl_acc_num'],
                                                       'company_id': company_code,
                                                       'language_id': CONST_DEFAULT_LANGUAGE}):
        acc_desc_detail = django_query_instance.django_filter_query(AccountingDataDesc,
                                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                                     'del_ind': False,
                                                                     'account_assign_cat': CONST_GLACC,
                                                                     'account_assign_value': sc_accounting_detail[
                                                                         'gl_acc_num'],
                                                                     'company_id': company_code,
                                                                     'language_id': CONST_DEFAULT_LANGUAGE},
                                                                    None,
                                                                    None)[0]
    if acc_desc_detail:
        acc_desc = acc_desc_detail['account_assign_value'] + ' - ' + acc_desc_detail['description']
    return acc_desc


def get_highest_item_guid_detail(item_details):
    max_item_guid = 0
    price_array = []
    item_guid = []
    if item_details:
        for item_price in item_details:
            price_array.append(item_price['value'])
            item_guid.append(item_price['guid'])
        item_value_list = type_cast_array_str_to_decimal(price_array)
        max_item_price = max(item_value_list)
        if max_item_price in price_array:
            max_item_price_index = price_array.index(max_item_price)
            max_item_guid = item_guid[max_item_price_index]
    return max_item_guid


def update_sc_delete_status(sc_guid):
    """

    """
    django_query_instance.django_update_query(ScHeader,
                                              {'guid': sc_guid,
                                               'client': global_variables.GLOBAL_CLIENT},
                                              {'status': CONST_SC_HEADER_DELETED})
    django_query_instance.django_update_query(ScItem,
                                              {'header_guid': sc_guid,
                                               'client': global_variables.GLOBAL_CLIENT},
                                              {'del_ind': True})
    sc_item_list = django_query_instance.django_filter_value_list_query(ScItem,
                                                                        {'header_guid': sc_guid,
                                                                         'client': global_variables.GLOBAL_CLIENT},
                                                                        'guid')
    django_query_instance.django_update_query(ScAccounting,
                                              {'item_guid__in': sc_item_list,
                                               'client': global_variables.GLOBAL_CLIENT},
                                              {'del_ind': True})
    django_query_instance.django_update_query(ScAccounting,
                                              {'header_guid': sc_guid,
                                               'client': global_variables.GLOBAL_CLIENT},
                                              {'del_ind': True})
    django_query_instance.django_update_query(ScAddresses,
                                              {'item_guid__in': sc_item_list,
                                               'client': global_variables.GLOBAL_CLIENT},
                                              {'del_ind': True})
    django_query_instance.django_update_query(ScAddresses,
                                              {'header_guid': sc_guid,
                                               'client': global_variables.GLOBAL_CLIENT},
                                              {'del_ind': True})
    django_query_instance.django_update_query(Notes,
                                              {'header_guid': sc_guid,
                                               'client': global_variables.GLOBAL_CLIENT},
                                              {'del_ind': True})
    django_query_instance.django_update_query(Notes,
                                              {'item_guid__in': sc_item_list,
                                               'client': global_variables.GLOBAL_CLIENT},
                                              {'del_ind': True})
    django_query_instance.django_update_query(ScApproval,
                                              {'header_guid': sc_guid,
                                               'client': global_variables.GLOBAL_CLIENT},
                                              {'del_ind': True})
    django_query_instance.django_update_query(ScPotentialApproval,
                                              {'sc_header_guid':sc_guid,
                                               'client':global_variables.GLOBAL_CLIENT},
                                              {'del_ind': True})

