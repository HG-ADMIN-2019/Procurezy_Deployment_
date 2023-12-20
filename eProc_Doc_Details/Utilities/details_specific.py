"""Copyright (c) 2020 Hiranya Garbha, Inc.
    Name:
        details_specific.py
    Usage:

     Author:
        Deepika,Shilpa Ellur
"""
from datetime import datetime

from django.db.models import Q

from eProc_Attributes.models.org_attribute_models import OrgAttributesLevel
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Account_Assignment.Utilities.account_assignment_generic import *

from eProc_Account_Assignment.Utilities.account_assignment_specific import ACCValueDesc, ACC_CAT, get_gl_account_value
from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.get_db_query import get_user_id_by_email_id, update_user_roles_to_session
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.str_concatenate import concatenate_array_str, concatenate_str
from eProc_Basic.Utilities.functions.type_casting import type_cast_array_str_to_int, type_cast_array_str_to_float, \
    type_cast_array_str_to_decimal
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import AccountingDataDesc, OrgCompanies, \
    OrgPorg, OrgPGroup, SupplierMaster
from eProc_Configuration.models.development_data import *
from eProc_Notes_Attachments.models import Notes
from eProc_Org_Model.models import OrgModel
from eProc_Registration.models import UserData
from eProc_Ship_To_Bill_To_Address.Utilites.ship_to_bill_to_generic import ShipToBillToAddress
from eProc_Ship_To_Bill_To_Address.Utilites.ship_to_bill_to_specific import get_shipping_drop_down
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import get_free_text_content, get_manger_detail
from eProc_Shopping_Cart.models import ScItem, ScAddresses, ScHeader, PurchasingData, ScAccounting, ScApproval, \
    PurchasingUser
from eProc_Suppliers.models.suppliers_model import OrgSuppliers
from eProc_User_Settings.Utilities import user_settings_generic
from eProc_User_Settings.Utilities.user_settings_generic import get_object_id_list_user
from eProc_User_Settings.Utilities.user_settings_specific import UserSettings

django_query_instance = DjangoQueries()


def get_item_notes(guid, note_type, item_flag):
    """
    :param guid:
    :param note_type:
    :return:
    """
    item_note = ''
    if item_flag:
        scitem_guid = ScItem.objects.filter(header_guid=guid, del_ind=False).values_list('guid', flat=True)

        if Notes.objects.filter(item_guid__in=scitem_guid, note_type=note_type, del_ind=False).exists():
            item_note = Notes.objects.filter(item_guid__in=scitem_guid, note_type=note_type, del_ind=False).order_by(
                'item_num')
    else:
        if Notes.objects.filter(header_guid=guid, note_type=note_type, del_ind=False).exists():
            item_note = Notes.objects.get(header_guid=guid, note_type=note_type, del_ind=False)
    return item_note


def get_notes(header_guid,sc_item_guid_list,note_type, item_flag):
    if item_flag:
        item_note = django_query_instance.django_filter_query(Notes,
                                                              {'item_guid__in':sc_item_guid_list,
                                                               'note_type':note_type,
                                                               'client':global_variables.GLOBAL_CLIENT},
                                                              ['item_num'],
                                                              None)
    else:
        item_note = django_query_instance.django_filter_query(Notes,
                                                              {'header_guid': header_guid,
                                                               'note_type': note_type,
                                                               'client': global_variables.GLOBAL_CLIENT},
                                                              None,
                                                              None)
    return item_note

def get_del_addr(guid):
    """

    :param guid:
    :return:
    """
    sc_addr = ''
    scitem_guid = ScItem.objects.filter(header_guid=guid).values_list('guid', flat=True)
    if ScAddresses.objects.filter(item_guid__in=scitem_guid).exists():
        sc_addr = ScAddresses.objects.filter(item_guid__in=scitem_guid).order_by('item_num')
    return sc_addr


def get_pgrp_item(guid):
    """

    :param guid:
    :return:
    """
    purchase_grp = PurchasingData.objects.filter(sc_header_guid=guid).values('purch_grp', 'item_num').order_by(
        'purch_grp')
    return purchase_grp


def get_acc_value_list(guid, sc_flag):
    """

    :param guid:
    :return:
    """
    sc_co_code = ScHeader.objects.filter(guid=guid, client=global_variables.GLOBAL_CLIENT).values_list('co_code',
                                                                                                       flat=True)
    sc_header_detail = ScHeader.objects.get(guid=guid, client=global_variables.GLOBAL_CLIENT)
    # for SC completion doc detail ACC
    if sc_flag == 'True':
        acc_value_list = AccountingDataDesc.objects.filter(~Q(account_assign_cat='GLACC'), company_id__in=sc_co_code,
                                                           client=global_variables.GLOBAL_CLIENT).values()
        acc_list = AccountAssignmentCategory.objects.filter(~Q(account_assign_cat='GLACC')).values_list(
            'account_assign_cat', flat=True)
        acc_description = AccountAssignmentCategory.objects.filter(~Q(account_assign_cat='GLACC')).values()
    # for Myorder doc detail ACC
    else:
        acc_value_list, acc_list = get_orgattr_acc_list()
        acc_description = AccountAssignmentCategory.objects.filter(Q(account_assign_cat__in=acc_list)).values()

    gl_acc_value_list = AccountingDataDesc.objects.filter(account_assign_cat='GLACC', company_id__in=sc_co_code,
                                                          client=global_variables.GLOBAL_CLIENT).values()
    gl_acc_value_append = ACCValueDesc.append_acc_desc(gl_acc_value_list)
    acc_append_desc = ACC_CAT.append_acc_ass_desc(acc_description)
    acc_value_append = ACCValueDesc.append_acc_desc(acc_value_list)
    if sc_header_detail.total_value:
        total_value = sc_header_detail.total_value
    else:
        total_value = 0
    default_gl_acc_detail, gl_acc_detail = get_gl_account_value(global_variables.GLOBAL_CLIENT,
                                                                round(float(total_value)), sc_co_code,
                                                                acc_list)

    return acc_value_list, acc_list, acc_value_append, acc_append_desc, default_gl_acc_detail, gl_acc_detail, gl_acc_value_append


def get_orgattr_acc_list():
    """
    :return:
    """
    user_obj_id_list = user_settings_generic.get_object_id_list_user(global_variables.GLOBAL_CLIENT,
                                                                     global_variables.GLOBAL_LOGIN_USER_OBJ_ID)
    user_setting_obj = UserSettings()
    acc_list = user_setting_obj.get_attr_list(user_obj_id_list, CONST_ACC_CAT)
    attr_id_list = [CONST_CT_CTR, CONST_WBS_ELEM, CONST_INT_ORD, CONST_AS_SET]
    acc_values = user_setting_obj.get_attrs_list(user_obj_id_list, attr_id_list)
    acc_value_list = ACCValueDesc.get_acc_value_description(global_variables.GLOBAL_CLIENT, acc_values)
    return acc_value_list, acc_list


def get_sc_comp_my_order(requester_object_id):
    ship_to_bill_to_address_instance = ShipToBillToAddress(requester_object_id)
    addr_value, addr_default_value = ship_to_bill_to_address_instance.get_default_address_number_and_list()
    delivery_addr_list, addr_default, addr_val_desc = get_shipping_drop_down(addr_value, addr_default_value)

    return delivery_addr_list, addr_default, addr_val_desc


def get_supplier_dropdown():
    """

    :return:
    """
    supplier_list = []
    supplier = SupplierMaster.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('supplier_id',
                                                                                                          'name1')

    for supp_id in supplier:
        supplier_dict = {}
        supplier_dict['supp_id'] = supp_id['supplier_id']
        supplier_dict['supp_desc'] = concatenate_str(supp_id['supplier_id'], supp_id['name1'])
        supplier_list.append(supplier_dict)

    return supplier_list


def get_sc_requester_user_name(guid):
    """

    :param guid:
    :return:
    """
    sc_header_data = django_query_instance.django_filter_query(ScHeader,
                                                               {'guid':guid,
                                                                'client':global_variables.GLOBAL_CLIENT,
                                                                'del_ind':False},None,None)[0]
    requester_user_name = sc_header_data['requester']
    sc_header_data['total_value'] = format(float(sc_header_data['total_value']), '.2f')
    return sc_header_data, requester_user_name


def get_requester_object_id(requester_user_name):
    """

    :param requester_user_name:
    :return:
    """

    requester_obj_id = UserData.objects.get(username=requester_user_name, client=global_variables.GLOBAL_CLIENT)

    return requester_obj_id.object_id_id


def get_eform_data(guid):
    """

    :param guid:
    :return:
    """
    eform_list = []
    # sc_item_guid_eform = ScItem.objects.filter(header_guid=guid, client=global_variables.GLOBAL_CLIENT,
    #                                            eform=True).values_list('guid', flat=True)
    filter_queue = ~Q(eform_id=None)
    sc_item_guid_eform = django_query_instance.django_queue_query_value_list(ScItem,
                                                                   {'header_guid':guid,
                                                                    'client':global_variables.GLOBAL_CLIENT},
                                                                  filter_queue,
                                                                  'guid')
    for item_guid in sc_item_guid_eform:
        eform_data = get_free_text_content(item_guid)
        if eform_data:
            eform_list.append(eform_data)
    return eform_list


def get_acc_desc_append(acc_cat):
    acc_and_description = ACC_CAT.get_acc_cat_description(acc_cat)
    acc_desc_append = ACC_CAT.append_acc_ass_desc(acc_and_description)
    return acc_desc_append


def get_acc_value(acc_detail, acc_data):
    """

    :param header_level_acc:
    :return:
    """
    acc_val = ''
    if acc_data in CONST_CC:
        acc_val = acc_detail.cost_center
    if acc_data in CONST_WBS:
        acc_val = acc_detail.wbs_ele
    if acc_data in CONST_OR:
        acc_val = acc_detail.internal_order
    if acc_data in CONST_AS:
        acc_val = acc_detail.asset_number
    return acc_val


def get_acc_value_acc_level(acc_detail, acc_data):
    """

    :param header_level_acc:
    :return:
    """
    acc_val = ''
    if acc_data in CONST_CC:
        acc_val = acc_detail['cost_center']
    if acc_data in CONST_WBS:
        acc_val = acc_detail['wbs_ele']
    if acc_data in CONST_OR:
        acc_val = acc_detail['internal_order']
    if acc_data in CONST_AS:
        acc_val = acc_detail['asset_number']
    return acc_val


def get_header_level_acc(header_guid):
    """

    :param header_guid:
    :return:
    """
    header_level_acc = ''
    acc_val = ''
    acc_desc = ''
    acc_value_description = ''
    gl_value_description = ''
    if ScAccounting.objects.filter(header_guid=header_guid, client=global_variables.GLOBAL_CLIENT,
                                   del_ind=False).exists():
        header_level_acc = ScAccounting.objects.get(header_guid=header_guid)

        # Account assignment category and its description appended
        acc_desc = get_acc_desc_append([header_level_acc.acc_cat])

        # get acc value from ScAccounting query set
        acc_val = get_acc_value(header_level_acc, header_level_acc.acc_cat)

        acc_value_and_description = ACCValueDesc.get_acc_value_description(global_variables.GLOBAL_CLIENT, [acc_val])
        acc_value_description = ACCValueDesc.append_acc_desc(acc_value_and_description)
        gl_value_and_description = ACCValueDesc.get_acc_value_description(global_variables.GLOBAL_CLIENT,
                                                                          [header_level_acc.gl_acc_num])
        gl_value_description = ACCValueDesc.append_acc_desc(gl_value_and_description)

    return header_level_acc, acc_desc, acc_value_description, gl_value_description


def get_header_acc_detail(header_guid):
    """
    """
    header_level_acc_guid = ''
    sc_accounting_data = ScAccounting.objects.filter(header_guid=header_guid,
                                                     del_ind=False,
                                                     client=global_variables.GLOBAL_CLIENT).order_by(
        'acc_item_num').values()
    for acc_detail in sc_accounting_data:
        header_level_acc_guid = acc_detail['guid']
        acc_desc_append = get_acc_desc_append([acc_detail['acc_cat']])
        if acc_desc_append:
            acc_detail['acc_desc'] = acc_desc_append[0]['append_val']
        else:
            acc_detail['acc_desc'] = acc_detail['acc_cat']

        acc_value_desc = get_acc_value_and_description_append_based_on_acc_query(acc_detail,
                                                                                 acc_detail['acc_cat'],
                                                                                 global_variables.GLOBAL_REQUESTER_COMPANY_CODE,
                                                                                 global_variables.GLOBAL_REQUESTER_LANGUAGE)
        acc_detail['acc_value_desc'] = acc_value_desc['attribute_values_description']
    return sc_accounting_data, header_level_acc_guid


def get_acc_value_and_description_append_based_on_acc_query(acc_detail, acc_asg_cat, default_company_code, language_id):
    """

    """
    acc_asg_cat_value = get_acc_value_acc_level(acc_detail, acc_asg_cat)
    acc_asg_cat_value_desc = ACCValueDesc.get_acc_asg_cat_value_desc(acc_asg_cat_value, default_company_code,
                                                                     acc_asg_cat, language_id)
    if acc_asg_cat_value_desc:
        acc_value_desc_append_list = append_attribute_value_description(acc_asg_cat_value_desc, 'account_assign_value',
                                                                        'description')[0]
        acc_value_desc_append = acc_value_desc_append_list[0]
    else:
        acc_value_desc_append = {'attribute_values': acc_asg_cat_value,
                                 'attribute_values_description': acc_asg_cat_value}
    return acc_value_desc_append


def get_header_level_addr(header_guid):
    """

    :param header_guid:
    :return:
    """
    header_level_addr = ''
    if ScAddresses.objects.filter(header_guid=header_guid, address_type='D').exists():
        if ScAddresses.objects.filter(header_guid=header_guid, address_type='D').count() == 1:
            header_level_addr = ScAddresses.objects.get(header_guid=header_guid, address_type='D')
    return header_level_addr


def get_highest_item_guid(guid):
    """
    :param guid:
    :return:
    """
    price_array = []
    item_guid = []
    max_item_guid = 0
    sc_item_price = ScItem.objects.filter(header_guid=guid).order_by('item_num')
    if sc_item_price:
        for item_price in sc_item_price:
            price_array.append(item_price.value)
            item_guid.append(item_price.guid)
        item_value_list = type_cast_array_str_to_decimal(price_array)
        max_item_price = max(item_value_list)
        if max_item_price in price_array:
            max_item_price_index = price_array.index(max_item_price)
            max_item_guid = item_guid[max_item_price_index]
    return max_item_guid


def get_approver_list(item_detail):
    """

    :param item_detail:
    :return:
    """
    manager_detail = ''
    msg_info = ''
    if item_detail['cmp_code']:
        manager_detail, msg_info = get_manger_detail(global_variables.GLOBAL_CLIENT,
                                                     global_variables.GLOBAL_LOGIN_USERNAME, item_detail['acc_type'],
                                                     item_detail['total_sc_value'], item_detail['cmp_code'],
                                                     item_detail['acc_value'], global_variables.GLOBAL_USER_CURRENCY)

    return manager_detail, msg_info


# Function to check if the user who is accessing the document must be either creator or requester
def validate_document_access(sc_requester, sc_creator, request, guid, access_type):
    """
    :param sc_requester:
    :param sc_creator:
    :param request:
    :param guid:
    :param access_type:
    :return:
    """
    if 'user_roles' in request.session:
        user_roles = request.session['user_roles']
    else:
        user_roles = update_user_roles_to_session(request)

    login_username = global_variables.GLOBAL_LOGIN_USERNAME

    if login_username == sc_requester or login_username == sc_creator or user_roles:
        return True
    else:
        if access_type == 'approvals':
            if CONST_SHOP_MANAGER in user_roles:
                if ScApproval.objects.filter(app_id=global_variables.GLOBAL_LOGIN_USERNAME,
                                             proc_lvl_sts=CONST_ACTIVE, header_guid=guid,
                                             client=global_variables.GLOBAL_CLIENT).exists():
                    return True
    return False


def get_purchaser_user_company_code():
    client = global_variables.GLOBAL_CLIENT
    user_object_id_list = get_object_id_list_user(client, global_variables.GLOBAL_LOGIN_USER_OBJ_ID)

    get_org_model_obj_list = list(
        OrgModel.objects.filter(object_id__in=user_object_id_list, node_type=CONST_COMPANY_CODE,
                                del_ind=False, client=client).values_list('object_id', flat=True)
    )

    company_code = list(OrgCompanies.objects.filter(object_id__in=get_org_model_obj_list, client=client, del_ind=False)
                        .values_list('company_id', flat=True))[0]

    return company_code


# To check if product category exists in porg if not then it directly returns false
def check_in_porg(client, porg_obj_id_list, product_category_id):
    """
    :param client:
    :param porg_obj_id_list:
    :param product_category_id:
    :return:
    """
    purch_org_det = OrgAttributesLevel.objects.filter(client=client, attribute_id=CONST_PROD_CAT,
                                                      object_id__in=porg_obj_id_list, del_ind=False)
    for low_high in purch_org_det:
        if int(product_category_id) in range(int(low_high.low), int(low_high.high) + 1):
            return True

    return False


# Once the product category is available in porg then it checks in pgroup else it returns false
def check_in_pgroup(client, product_category_id, list_of_obj_id_for_user):
    """
    :param list_of_obj_id_for_user:
    :param product_category_id:
    :param client:
    :return:
    """
    pgroup_obj_id_list = OrgModel.objects.filter(object_id__in=list_of_obj_id_for_user
                                                 , client=client, del_ind=False,
                                                 node_type=CONST_PGROUP).values_list('object_id', flat=True)

    pgroup_org_det = OrgAttributesLevel.objects.filter(client=client, attribute_id=CONST_RESP_PROD_CAT,
                                                       object_id__in=pgroup_obj_id_list, del_ind=False)
    for low_high in pgroup_org_det:
        if int(product_category_id) in range(int(low_high.low), int(low_high.high) + 1):
            return True

    return False


def validate_product_category_id_with_purchaser(document_company_code, product_category_id):
    purchaser_obj_id = global_variables.GLOBAL_LOGIN_USER_OBJ_ID
    client = global_variables.GLOBAL_CLIENT
    list_of_obj_id_for_user = get_object_id_list_user(client, purchaser_obj_id)

    porg_obj_id_list = OrgModel.objects.filter(object_id__in=list_of_obj_id_for_user,
                                               client=client, del_ind=False,
                                               node_type=CONST_PORG).values_list('object_id', flat=True)

    get_cc_from_attribute_level = OrgAttributesLevel.objects.filter(client=client, attribute_id=CONST_CO_CODE,
                                                                    object_id__in=porg_obj_id_list,
                                                                    del_ind=False).values_list('low', flat=True)

    if document_company_code in get_cc_from_attribute_level:
        is_porg_valid = check_in_porg(client, porg_obj_id_list, product_category_id)

        if is_porg_valid:
            return check_in_pgroup(client, product_category_id, list_of_obj_id_for_user)

    return False


def update_sc_with_supplier_data(supplier_id, item_guid):
    payment_term = None
    incoterm = None

    get_items_purchasing_data = django_query_instance.django_filter_only_query(PurchasingData, {
        'sc_item_guid': item_guid, 'del_ind': False, 'client': global_variables.GLOBAL_CLIENT
    })

    if len(get_items_purchasing_data) > 0:

        porg_id = get_items_purchasing_data[0].purch_org

        get_supplier_instance = django_query_instance.django_get_query(OrgSuppliers, {
            'supplier_id': supplier_id, 'del_ind': False, 'client': global_variables.GLOBAL_CLIENT, 'porg_id': porg_id
        })

        if get_supplier_instance:
            payment_term = str(get_supplier_instance.payment_term_key)
            incoterm = str(get_supplier_instance.incoterm_key)

            django_query_instance.django_filter_only_query(ScItem, {
                'guid': item_guid, 'del_ind': False, 'client': global_variables.GLOBAL_CLIENT
            }).update(payment_term=payment_term, incoterm=incoterm)

    return payment_term, incoterm


def update_purchasing_user(sc_header_guid, status):
    """

    """
    if django_query_instance.django_filter_value_list_query(
            ScHeader, {'guid': sc_header_guid,
                       'client': global_variables.GLOBAL_CLIENT},'status')[0] == CONST_SC_HEADER_INCOMPLETE:
        if django_query_instance.django_existence_check(PurchasingUser,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'sc_header_guid': sc_header_guid,
                                                         'purchaser_user_id':global_variables.GLOBAL_LOGIN_USERNAME}
                                                        ):
            django_query_instance.django_update_query(PurchasingUser,
                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                       'sc_header_guid': sc_header_guid,
                                                       'purchaser_user_id':global_variables.GLOBAL_LOGIN_USERNAME},
                                                      {'status':status,
                                                       'purchasing_user_changed_at':datetime.now(),
                                                       'purchasing_user_changed_by':global_variables.GLOBAL_LOGIN_USERNAME})
        else:
            django_query_instance.django_create_query(PurchasingUser,
                                                      {'purchasing_user_guid':guid_generator(),
                                                          'client': global_variables.GLOBAL_CLIENT,
                                                       'sc_header_guid': django_query_instance.django_get_query(ScHeader,
                                                                                                                {'guid':sc_header_guid,
                                                                                                                 'client':global_variables.GLOBAL_CLIENT,
                                                                                                                 'del_ind':False}),
                                                       'status':status,
                                                       'purchaser_user_id':global_variables.GLOBAL_LOGIN_USERNAME,
                                                       'purchasing_user_created_by':global_variables.GLOBAL_LOGIN_USERNAME,
                                                       'purchasing_user_changed_at':datetime.now(),
                                                       })
    if status == CONST_SC_ASSIST_SUBMIT:
        django_query_instance.django_update_query(PurchasingData,
                                                  {'sc_header_guid':sc_header_guid,
                                                   'client':global_variables.GLOBAL_CLIENT,
                                                   'del_ind':False},
                                                  {'purchaser_user':global_variables.GLOBAL_LOGIN_USERNAME})
