"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    user_settings_specific.py
Usage:
    Purchase settings page related function
    list of functions
    1. user_settings_form - Get list of purchasing page values dropdown for login user
    2. append_attrlow_desc - concatenate attr low value and description
    3. get_purch_org_info - get purchase org and grp detail
    4. save_default_value - save default value to attribute level db table
    5. get_spending_limit_value - get spending limt value and its description apend to it
    6. get_approver_limt_value - get approver limt value and its description apend to it

Author:
    Deepika K
"""
from eProc_Account_Assignment.Utilities.account_assignment_specific import ACC_CAT, ACCValueDesc, remove_insert
from eProc_Attributes.Utilities.attributes_generic import OrgAttributeValues
from eProc_Attributes.Utilities.attributes_specific import sort_list_dictionary_key_values, \
    append_attribute_value_description, append_description_atrr_value_exists
from eProc_Basic.Utilities.functions.insert_remove import list_remove_insert_first
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.functions.str_concatenate import concatenate_str, concatenate_array_str, split_str
from eProc_Basic.Utilities.messages.messages import MSG001, MSG005, MSG115, MSG116, MSG117, MSG118
from eProc_Basic.Utilities.constants.constants import *
from eProc_Configuration.models import *
from eProc_Configuration.models.development_data import DocumentType
from eProc_Ship_To_Bill_To_Address.Utilites.ship_to_bill_to_specific import Address_desc
from eProc_User_Settings.Utilities import user_settings_generic
from eProc_User_Settings.Utilities.org_attributes_functions import get_org_attr_level_details
from eProc_User_Settings.Utilities.user_settings_generic import *
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries

django_query_instance = DjangoQueries()


def get_org_attr_list():
    error_message_list = []
    # initialize attribute level detail based on attribute id
    acc_list = []
    cost_center_list = []
    asset_list = []
    wbs_list = []
    internal_order_list = []
    delivery_addr_list = []
    inv_addr_list = []
    doc_type_list = []
    user_role_list = []
    cocode_list = []

    # drop down list of purchasing data
    acc_drop_down_list = []
    cc_drop_down_list = []
    wbs_drop_down_list = []
    internal_order_drop_down_list = []
    asset_drop_down_list = []
    delivery_addr_drop_down_list = []
    inv_addr_drop_down_list = []
    doc_type_drop_down_list = []
    user_role_drop_down_list = []
    cocode_drop_down_list = []

    #  Exclude list from attribute details
    exclude_acc_list = []
    exclude_cc_list = []
    exclude_wbs_list = []
    exclude_internal_order_list = []
    exclude_asset_list = []
    exclude_delivery_addr_list = []
    exclude_inv_addr_list = []
    exclude_doc_type_list = []
    exclude_cocode_list = []
    exclude_user_role_list = []
    default_user_role = []
    delivery_addr_desc = []
    invoice_addr_desc = []
    company_code_list = ''
    company_code_dictionary_list = ''
    purchase_org_list = ''
    purchase_org_dictionary_list = ''
    purchase_group_list = ''
    purchase_group_dictionary_list = ''
    default_cc_list = []
    default_wbs_list = []
    default_internal_order_list = []
    default_asset_list = []

    attribute_id_list = [CONST_ACC_CAT, CONST_CT_CTR, CONST_WBS_ELEM,
                         CONST_INT_ORD, CONST_AS_SET, CONST_DEL_ADDR,
                         CONST_INV_ADDR, CONST_DEF_DOC_SEARCH,
                         CONST_US_ROLE, CONST_CO_CODE]
    if global_variables.GLOBAL_LOGIN_USER_OBJ_ID:
        # get login user and its parents object id list
        object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT,
                                                 global_variables.GLOBAL_LOGIN_USER_OBJ_ID)

        order_by_list = ['attribute_id', 'low', 'attr_level_default']
        required_field_list = ['object_id', 'attribute_id', 'low', 'attr_level_default', 'attr_level_exclude',
                               'attr_level_guid']

        org_attr_level_filter = {'attribute_id__in': attribute_id_list,
                                 'object_id__in': object_id_list,
                                 'client': global_variables.GLOBAL_CLIENT,
                                 'del_ind': False}

        # get org attribute level details of login user and its parent object id
        org_attr_list = get_org_attr_level_details(required_field_list, order_by_list, **org_attr_level_filter)

        # sort attribute level details based on object id list
        attr_detail_list = sort_list_dictionary_key_values(object_id_list, org_attr_list, 'object_id')

        # Sort based on attribute id
        for attr_detail in attr_detail_list:
            if attr_detail['attribute_id'] == CONST_ACC_CAT:
                exclude_dic = {}
                if attr_detail['attr_level_exclude']:
                    exclude_dic['low'] = attr_detail['low']
                    exclude_dic['object_id'] = attr_detail['object_id']
                    exclude_acc_list.append(exclude_dic)
                acc_drop_down_list.append(attr_detail['low'])
                acc_list.append(attr_detail)
            elif attr_detail['attribute_id'] == CONST_CT_CTR:
                exclude_dic = {}
                if attr_detail['attr_level_exclude']:
                    exclude_dic['low'] = attr_detail['low']
                    exclude_dic['object_id'] = attr_detail['object_id']
                    exclude_cc_list.append(exclude_dic)
                cc_drop_down_list.append(attr_detail['low'])
                cost_center_list.append(attr_detail)
            elif attr_detail['attribute_id'] == CONST_WBS_ELEM:
                exclude_dic = {}
                if attr_detail['attr_level_exclude']:
                    exclude_dic['low'] = attr_detail['low']
                    exclude_dic['object_id'] = attr_detail['object_id']
                    exclude_wbs_list.append(exclude_dic)
                wbs_drop_down_list.append(attr_detail['low'])
                wbs_list.append(attr_detail)
            elif attr_detail['attribute_id'] == CONST_INT_ORD:
                exclude_dic = {}
                if attr_detail['attr_level_exclude']:
                    exclude_dic['low'] = attr_detail['low']
                    exclude_dic['object_id'] = attr_detail['object_id']
                    exclude_internal_order_list.append(exclude_dic)
                internal_order_drop_down_list.append(attr_detail['low'])
                internal_order_list.append(attr_detail)
            elif attr_detail['attribute_id'] == CONST_AS_SET:
                exclude_dic = {}
                if attr_detail['attr_level_exclude']:
                    exclude_dic['low'] = attr_detail['low']
                    exclude_dic['object_id'] = attr_detail['object_id']
                    exclude_asset_list.append(exclude_dic)
                asset_drop_down_list.append(attr_detail['low'])
                asset_list.append(attr_detail)
            elif attr_detail['attribute_id'] == CONST_DEL_ADDR:
                exclude_dic = {}
                if attr_detail['attr_level_exclude']:
                    exclude_dic['low'] = attr_detail['low']
                    exclude_dic['object_id'] = attr_detail['object_id']
                    exclude_delivery_addr_list.append(exclude_dic)
                delivery_addr_drop_down_list.append(attr_detail['low'])
                delivery_addr_list.append(attr_detail)
            elif attr_detail['attribute_id'] == CONST_INV_ADDR:
                exclude_dic = {}
                if attr_detail['attr_level_exclude']:
                    exclude_dic['low'] = attr_detail['low']
                    exclude_dic['object_id'] = attr_detail['object_id']
                    exclude_inv_addr_list.append(exclude_dic)
                inv_addr_drop_down_list.append(attr_detail['low'])
                inv_addr_list.append(attr_detail)
            elif attr_detail['attribute_id'] == CONST_DEF_DOC_SEARCH:
                exclude_dic = {}
                if attr_detail['attr_level_exclude']:
                    exclude_dic['low'] = attr_detail['low']
                    exclude_dic['object_id'] = attr_detail['object_id']
                    exclude_doc_type_list.append(exclude_dic)
                doc_type_drop_down_list.append(attr_detail['low'])
                doc_type_list.append(attr_detail)
            elif attr_detail['attribute_id'] == CONST_US_ROLE:
                exclude_dic = {}
                if attr_detail['attr_level_exclude']:
                    exclude_dic['low'] = attr_detail['low']
                    exclude_dic['object_id'] = attr_detail['object_id']
                    exclude_user_role_list.append(exclude_dic)
                user_role_drop_down_list.append(attr_detail['low'])
                user_role_list.append(attr_detail)
            elif attr_detail['attribute_id'] == CONST_CO_CODE:
                exclude_dic = {}
                if attr_detail['attr_level_exclude']:
                    exclude_dic['low'] = attr_detail['low']
                    exclude_dic['object_id'] = attr_detail['object_id']
                    exclude_cocode_list.append(exclude_dic)
                cocode_drop_down_list.append(attr_detail['low'])
                cocode_list.append(attr_detail)

        # get Account assignment category values list and default values and also append values with its description
        acc_drop_down_list, default_acc_list = OrgAttributeValues.get_configured_attr_values_attr_default(
            acc_drop_down_list,
            object_id_list,
            exclude_acc_list,
            acc_list)
        if not default_acc_list:
            msgid = 'MSG115'
            error_msg = get_message_desc(msgid)[1]

            error_message_list.append(error_msg + "Account Assignment Category")
        if acc_drop_down_list:
            acc_drop_down_list, default_acc_list, error_msg = ACC_CAT.get_accounting_desc_append_acc_value(
                acc_drop_down_list, default_acc_list)
            if error_msg:
                error_message_list.append(error_msg + "Account Assignment Category")
        else:
            msgid = 'MSG116'
            error_msg = get_message_desc(msgid)[1]

            error_message_list.append(error_msg + "Account Assignment Category")

        # get Company Code values list and default values and also append values with its description
        cocode_drop_down_list, default_cocode_list = OrgAttributeValues.get_configured_attr_values_attr_default(
            cocode_drop_down_list,
            object_id_list,
            exclude_cocode_list,
            cocode_list)

        if not default_cocode_list:
            msgid = 'MSG115'
            error_msg = get_message_desc(msgid)[1]

            error_message_list.append(error_msg + 'Company Code')
        if default_cocode_list:
            # get Cost Center values list and default values and also append values with its description
            cc_drop_down_list, default_cc_list = OrgAttributeValues.get_configured_attr_values_attr_default(
                cc_drop_down_list,
                object_id_list,
                exclude_cc_list,
                cost_center_list)
            if not default_cc_list:
                msgid = 'MSG115'
                error_msg = get_message_desc(msgid)[1]

                error_message_list.append(error_msg + "Cost Center")
            if default_cocode_list:
                if cc_drop_down_list:
                    cc_drop_down_list, default_cc_list, error_msg = ACCValueDesc.get_acc_value_desc_append_acc_value_desc(
                        cc_drop_down_list,
                        default_cc_list,
                        default_cocode_list,
                        CONST_CC)
                    if not default_cc_list:
                        msgid = 'MSG115'
                        error_msg = get_message_desc(msgid)[1]

                        error_message_list.append(error_msg + "Cost Center")
                else:
                    msgid = 'MSG116'
                    error_msg = get_message_desc(msgid)[1]

                    error_message_list.append(error_msg + "Cost Center")

            # get WBS element values list and default values and also append values with its description
            wbs_drop_down_list, default_wbs_list = OrgAttributeValues.get_configured_attr_values_attr_default(
                wbs_drop_down_list,
                object_id_list,
                exclude_wbs_list,
                wbs_list)

            if default_wbs_list:
                msgid = 'MSG115'
                error_msg = get_message_desc(msgid)[1]

                error_message_list.append(error_msg + "WBS element")
            if default_cocode_list:
                if wbs_drop_down_list:
                    wbs_drop_down_list, default_wbs_list, error_msg = ACCValueDesc.get_acc_value_desc_append_acc_value_desc(
                        wbs_drop_down_list,
                        default_wbs_list,
                        default_cocode_list,
                        CONST_WBS)
                    if default_wbs_list:
                        msgid = 'MSG115'
                        error_msg = get_message_desc(msgid)[1]
                        error_message_list.append(error_msg + "WBS element")
                else:
                    msgid = 'MSG116'
                    error_msg = get_message_desc(msgid)[1]

                    error_message_list.append(error_msg + "WBS element")

            # get Internal order values list and default values and also append values with its description
            internal_order_drop_down_list, default_internal_order_list = OrgAttributeValues.get_configured_attr_values_attr_default(
                internal_order_drop_down_list,
                object_id_list,
                exclude_internal_order_list,
                internal_order_list)
            if not default_internal_order_list:
                msgid = 'MSG115'
                error_msg = get_message_desc(msgid)[1]
                error_message_list.append(error_msg + "Internal order")
            if default_cocode_list:
                if internal_order_drop_down_list:
                    internal_order_drop_down_list, default_internal_order_list, error_msg = ACCValueDesc.get_acc_value_desc_append_acc_value_desc(
                        internal_order_drop_down_list,
                        default_internal_order_list,
                        default_cocode_list,
                        CONST_OR)
                    if error_msg:
                        error_message_list.append(error_msg + "Internal order")
                else:
                    msgid = 'MSG116'
                    error_msg = get_message_desc(msgid)[1]

                    error_message_list.append(error_msg + "Internal order")

            # get Asset values list and default values and also append values with its description
            asset_drop_down_list, default_asset_list = OrgAttributeValues.get_configured_attr_values_attr_default(
                asset_drop_down_list,
                object_id_list,
                exclude_asset_list,
                asset_list)
            if not default_asset_list:
                msgid = 'MSG115'
                error_msg = get_message_desc(msgid)[1]


            if default_cocode_list:
                if asset_drop_down_list:
                    asset_drop_down_list, default_asset_list, error_msg = ACCValueDesc.get_acc_value_desc_append_acc_value_desc(
                        asset_drop_down_list,
                        default_asset_list,
                        default_cocode_list,
                        CONST_AS)
                    if error_msg:
                        error_message_list.append(error_msg + "Asset")
                else:
                    msgid = 'MSG116'
                    error_msg = get_message_desc(msgid)[1]

                    error_message_list.append(error_msg + "Asset")
        else:
            cc_drop_down_list = []
            wbs_drop_down_list = []
            internal_order_drop_down_list = []
            asset_drop_down_list = []
        # get User Role list and default values and also append values with its description
        user_role_drop_down_list, exclude_list = OrgAttributeValues.get_org_attr_values_list(user_role_drop_down_list,
                                                                                             object_id_list,
                                                                                             exclude_user_role_list,
                                                                                             user_role_list)

        # get Document Type list and default values and also append values with its description
        doc_type_drop_down_list, default_doc_type_list = OrgAttributeValues.get_configured_attr_values_attr_default(
            doc_type_drop_down_list,
            object_id_list,
            exclude_doc_type_list,
            doc_type_list)
        if not default_doc_type_list:
            msgid = 'MSG115'
            error_msg = get_message_desc(msgid)[1]

            error_message_list.append(error_msg + "Document type")

        if doc_type_drop_down_list:
            doc_search_val_desc = DocSearch.get_doc_search_description(doc_type_drop_down_list)
            if doc_search_val_desc:
                doc_type_drop_down_list, default_doc_type_list = DocSearch.append_doc_search_desc(doc_search_val_desc,
                                                                                                  default_doc_type_list,
                                                                                                  doc_type_drop_down_list)
            else:
                msgid = 'MSG117'
                error_msg = get_message_desc(msgid)[1]

                error_message_list.append(error_msg + "Document type")
        else:
            msgid = 'MSG116'
            error_msg = get_message_desc(msgid)[1]

            error_message_list.append(error_msg + "Document type")

        # get Delivery Address list and default values and also append values with its description
        delivery_addr_drop_down_list, default_delivery_addr_list = OrgAttributeValues.get_configured_attr_values_attr_default(
            delivery_addr_drop_down_list,
            object_id_list,
            exclude_delivery_addr_list,
            delivery_addr_list)
        if not default_delivery_addr_list:
            msgid = 'MSG115'
            error_msg = get_message_desc(msgid)[1]

            error_message_list.append(error_msg + "Delivery Address")
        if delivery_addr_drop_down_list:
            default_delivery_addr_list = Address_desc.get_addr_description(global_variables.GLOBAL_CLIENT,
                                                                           [default_delivery_addr_list],
                                                                           CONST_DEL_ADDR, 'D')

            delivery_addr_drop_down_list = Address_desc.get_addr_description(global_variables.GLOBAL_CLIENT,
                                                                             delivery_addr_drop_down_list,
                                                                             CONST_DEL_ADDR, 'D')
            delivery_addr_desc = delivery_addr_drop_down_list
            if not delivery_addr_drop_down_list:
                msgid = 'MSG117'
                error_msg = get_message_desc(msgid)[1]

                error_message_list.append(error_msg + "Delivery Address")
        else:
            msgid = 'MSG116'
            error_msg = get_message_desc(msgid)[1]

            error_message_list.append(error_msg + "Delivery Address")

        # get Invoice Address list and default values and also append values with its description
        inv_addr_drop_down_list, default_inv_addr_list = OrgAttributeValues.get_configured_attr_values_attr_default(
            inv_addr_drop_down_list,
            object_id_list,
            exclude_inv_addr_list,
            inv_addr_list)
        if not default_inv_addr_list:
            msgid = 'MSG115'
            error_msg = get_message_desc(msgid)[1]

            error_message_list.append(error_msg + "Invoice Address")
        if inv_addr_drop_down_list:
            default_inv_addr_list = Address_desc.get_addr_description(global_variables.GLOBAL_CLIENT,
                                                                      [default_inv_addr_list],
                                                                      CONST_DEL_ADDR, 'I')

            inv_addr_drop_down_list = Address_desc.get_addr_description(global_variables.GLOBAL_CLIENT,
                                                                        inv_addr_drop_down_list,
                                                                        CONST_DEL_ADDR, 'I')
            invoice_addr_desc = inv_addr_drop_down_list
            if not inv_addr_drop_down_list:
                msgid = 'MSG117'
                error_msg = get_message_desc(msgid)[1]

                error_message_list.append(error_msg + " Invoice Address")
        else:
            msgid = 'MSG116'
            error_msg = get_message_desc(msgid)

            error_message_list.append(error_msg + " Invoice Address")

        purch_org_list = []
        purch_grp_list = []
        spending_limit_list = []
        approver_limit_list = []
        purch_org_default_list = []
        purch_grp_default_list = []
        spending_limit_default_list = []
        approver_limit_default_list = []
        # get company code value desc dictionary list
        company_code_list, company_code_dictionary_list = get_company_code_desc_append(cocode_drop_down_list,
                                                                                       default_cocode_list)
        if company_code_list:
            purchase_org_list, purchase_org_dictionary_list = get_purch_org_detail(default_cocode_list)
        if purchase_org_list:
            purchase_group_dictionary_list = get_purch_group_detail(purchase_org_list[0])
        description = OrgCompanies
        default_cocode_list = [default_cocode_list]
        if default_cocode_list:
            org_company_list = append_attrlow_desc(global_variables.GLOBAL_CLIENT, CONST_CO_CODE, description,
                                                   default_cocode_list, True)
            if org_company_list:
                description = OrgPorg
                purch_org_list, porg_data = get_purch_org_info(default_cocode_list, global_variables.GLOBAL_CLIENT,
                                                               description, True)

                description = OrgPGroup
                purch_grp_list = get_purch_grp_info(global_variables.GLOBAL_CLIENT, description, porg_data, True)

                spending_limit_list = get_spending_limit_value(global_variables.GLOBAL_CLIENT,
                                                               global_variables.GLOBAL_LOGIN_USERNAME,
                                                               default_cocode_list, True)

                approver_limit_list = get_approver_limt_value(global_variables.GLOBAL_CLIENT,
                                                              global_variables.GLOBAL_LOGIN_USERNAME,
                                                              default_cocode_list, True)

        user_setting_list = [acc_drop_down_list, cc_drop_down_list, wbs_drop_down_list, internal_order_drop_down_list,
                             asset_drop_down_list, doc_type_drop_down_list, delivery_addr_drop_down_list,
                             inv_addr_drop_down_list, user_role_drop_down_list, cocode_drop_down_list, purch_org_list,
                             purch_grp_list, spending_limit_list, approver_limit_list]
        user_setting_default_list = [default_acc_list, default_cc_list, default_wbs_list, default_internal_order_list,
                                     default_asset_list, default_doc_type_list, default_delivery_addr_list,
                                     default_inv_addr_list, default_user_role, default_cocode_list,
                                     purch_org_default_list, purch_grp_default_list, spending_limit_default_list,
                                     approver_limit_default_list]

    else:
        user_setting_list = []
        user_setting_default_list = []
        msgid = 'MSG118'
        error_msg = get_message_desc(msgid)[1]

        error_message_list.append(error_msg)

    return user_setting_list, user_setting_default_list, error_message_list, delivery_addr_desc, invoice_addr_desc, \
           company_code_list, company_code_dictionary_list, purchase_org_list, purchase_org_dictionary_list, purchase_group_dictionary_list


def update_or_delete_previous_default(field, inherite_object_id_list, login_user_obj_id):
    """

    :param field:
    :param inherite_object_id_list:
    :param login_user_obj_id:
    :return:
    """
    if django_query_instance.django_existence_check(OrgAttributesLevel, {
        'object_id': login_user_obj_id,
        'client': global_variables.GLOBAL_CLIENT,
        'attr_level_default': True,
        'attribute_id': field,
        'del_ind': False
    }):
        initial_default = django_query_instance.django_filter_value_list_query(OrgAttributesLevel, {
            'object_id': login_user_obj_id,
            'client': global_variables.GLOBAL_CLIENT,
            'attr_level_default': True,
            'attribute_id': field,
            'del_ind': False
        }, 'low')[0]
        if initial_default:
            if OrgAttributesLevel.objects.filter(Q(object_id__in=inherite_object_id_list) &
                                                 Q(client=global_variables.GLOBAL_CLIENT) &
                                                 Q(attribute_id=field) &
                                                 Q(low=initial_default) &
                                                 Q(del_ind=False) &
                                                 Q(attr_level_exclude=True)).exists():
                initial_detail = OrgAttributesLevel.objects.filter(Q(object_id__in=inherite_object_id_list) &
                                                                   Q(client=global_variables.GLOBAL_CLIENT) &
                                                                   Q(attribute_id=field) &
                                                                   Q(low=initial_default) &
                                                                   Q(del_ind=False)).values()[0]

                if initial_detail['attr_level_exclude']:
                    exclude_flag = True
                else:
                    exclude_flag = False

                if exclude_flag:
                    django_query_instance.django_filter_only_query(OrgAttributesLevel, {
                        'object_id': login_user_obj_id,
                        'client': global_variables.GLOBAL_CLIENT,
                        'attr_level_default': True,
                        'attribute_id': field,
                        'del_ind': False
                    }).update(attr_level_default=False)
                else:
                    django_query_instance.django_filter_delete_query(OrgAttributesLevel, {
                        'object_id': login_user_obj_id,
                        'client': global_variables.GLOBAL_CLIENT,
                        'attr_level_default': True,
                        'attribute_id': field,
                        'del_ind': False
                    }).delete()
            else:
                if OrgAttributesLevel.objects.filter(Q(object_id__in=inherite_object_id_list) &
                                                     Q(client=global_variables.GLOBAL_CLIENT) &
                                                     Q(attribute_id=field) &
                                                     Q(low=initial_default) &
                                                     Q(del_ind=False)).exists():

                    django_query_instance.django_filter_delete_query(OrgAttributesLevel, {
                        'object_id': login_user_obj_id,
                        'client': global_variables.GLOBAL_CLIENT,
                        'attr_level_default': True,
                        'attribute_id': field,
                        'del_ind': False
                    })

                else:
                    django_query_instance.django_filter_only_query(OrgAttributesLevel, {
                        'object_id': login_user_obj_id,
                        'client': global_variables.GLOBAL_CLIENT,
                        'attr_level_default': True,
                        'attribute_id': field, 'del_ind': False
                    }).update(attr_level_default=False)


def update_or_create_default(field, field_value, inherite_object_id_list, login_user_obj_id):
    """

    :param field:
    :param field_value:
    :param inherite_object_id_list:
    :param login_user_obj_id:
    :return:
    """

    if not django_query_instance.django_existence_check(OrgAttributesLevel, {
        'object_id__in': inherite_object_id_list,
        'client': global_variables.GLOBAL_CLIENT,
        'attribute_id': field,
        'low': field_value,
        'attr_level_default': True,
        'del_ind': False
    }):
        if django_query_instance.django_existence_check(OrgAttributesLevel, {
            'object_id': login_user_obj_id, 'client': global_variables.GLOBAL_CLIENT, 'attr_level_default': False,
            'low': field_value, 'attribute_id': field, 'del_ind': False
        }):
            django_query_instance.django_filter_only_query(OrgAttributesLevel, {
                'object_id': login_user_obj_id, 'client': global_variables.GLOBAL_CLIENT,
                'attr_level_default': False,
                'low': field_value,
                'attribute_id': field, 'del_ind': False
            }).update(attr_level_default=True)
        else:
            django_query_instance.django_create_query(OrgAttributesLevel, {
                'attr_level_guid': guid_generator(),
                'attr_level_default': True,
                'attr_level_exclude': False,
                'attribute_id': django_query_instance.django_get_query(OrgAttributes, {'attribute_id': field}),
                'low': field_value,
                'version_number': 1,
                'object_type': 'O',
                'del_ind': False,
                'object_id': django_query_instance.django_get_query(OrgModel, {'object_id': login_user_obj_id}),
                'client': django_query_instance.django_get_query(OrgClients, {'client': global_variables.GLOBAL_CLIENT})
            })
    else:
        inherit_default_attr_level_detail = django_query_instance.django_filter_only_query(OrgAttributesLevel, {
            'object_id__in': inherite_object_id_list,
            'client': global_variables.GLOBAL_CLIENT,
            'attribute_id': field,
            'attr_level_default': True,
            'del_ind': False
        }).values('low', 'object_id')

        if inherit_default_attr_level_detail:
            attr_detail_list = sort_list_dictionary_key_values(inherite_object_id_list,
                                                               inherit_default_attr_level_detail, 'object_id')
            inherit_default = attr_detail_list[0]['low']
            if inherit_default != field_value:
                django_query_instance.django_create_query(OrgAttributesLevel, {
                    'attr_level_guid': guid_generator(),
                    'attr_level_default': True,
                    'attr_level_exclude': False,
                    'attribute_id': django_query_instance.django_get_query(OrgAttributes, {'attribute_id': field}),
                    'low': field_value,
                    'version_number': 1,
                    'object_type': 'O',
                    'del_ind': False,
                    'object_id': django_query_instance.django_get_query(OrgModel, {'object_id': login_user_obj_id}),
                    'client': django_query_instance.django_get_query(OrgClients,
                                                                     {'client': global_variables.GLOBAL_CLIENT})
                })


class UserSettings:
    def __init__(self):
        self.client = global_variables.GLOBAL_CLIENT
        self.login_username = global_variables.GLOBAL_LOGIN_USERNAME
        self.login_user_obj_id = global_variables.GLOBAL_LOGIN_USER_OBJ_ID

    def user_settings_form(self):
        """
        Get list of purchasing page values dropdown for login user
        :param client: log in client value
        :param login_username: login user name
        :param db_username: login user name stored in UserData
        :return: list of drop down to be displayed in UI
        """
        # attr list initialisation
        acc_list = []
        cc_list = []
        wbs_list = []
        int_ord_list = []
        asset_list = []
        doc_search_list = []
        delivery_addr_list = []
        invoice_addr_list = []
        asg_role_list = []
        org_company_list = []
        purch_org_list = []
        purch_grp_list = []
        spending_limit_list = []
        approver_limit_list = []
        # default attr list initialisation
        acc_default_list = []
        cc_default_list = []
        wbs_default_list = []
        int_ord_default_list = []
        asset_default_list = []
        doc_search_default_list = []
        delivery_addr_default_list = []
        invoice_addr_default_list = []
        asg_role_default_list = []
        org_company_default_list = []
        purch_org_default_list = []
        purch_grp_default_list = []
        spending_limit_default_list = []
        approver_limit_default_list = []
        error_msg = None

        # Check User Assigned or not
        if self.login_user_obj_id:
            object_id = user_settings_generic.get_object_id_list_user(self.client, self.login_user_obj_id)
        else:
            # passing null if there is no entry in orgmodel
            user_setting_list = [acc_list, cc_list, wbs_list, int_ord_list, asset_list,
                                 doc_search_list, delivery_addr_list, invoice_addr_list,
                                 asg_role_list, org_company_list, purch_org_list,
                                 purch_grp_list, spending_limit_list, approver_limit_list]
            user_setting_default_list = [acc_default_list, cc_default_list, wbs_default_list, int_ord_default_list,
                                         asset_default_list,
                                         doc_search_default_list, delivery_addr_default_list, invoice_addr_default_list,
                                         asg_role_default_list, org_company_default_list, purch_org_default_list,
                                         purch_grp_default_list, spending_limit_default_list,
                                         approver_limit_default_list]
            # error_msg = MSG001
            # msgid = 'MSG001'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            message_desc = get_message_desc('MSG001')[1]

            return user_setting_list, user_setting_default_list, message_desc

        # Get ACC drop down list
        acc_cat_value, acc_cat_default_value = self.get_attr_value(object_id, CONST_ACC_CAT)
        # if there is entry in attr level then only append description else throw error msg
        if acc_cat_value:
            acc_val_desc = ACC_CAT.get_acc_cat_description(acc_cat_value)
            if acc_val_desc:
                acc_list, acc_default = ACC_CAT.append_acc_val_desc(acc_val_desc, acc_cat_default_value)
                if acc_default:
                    acc_default_list = [acc_default]
            else:
                error_msg = get_message_desc(MSG005)[1]
                # msgid = 'MSG005'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg
                # # error_msg = MSG005

        else:
            error_msg = get_message_desc(MSG005)[1]
            # msgid = 'MSG005'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            # error_msg = MSG005

        # Get cost center dropdown list
        ct_ctr_value, cc_default_value = self.get_attr_value(object_id, CONST_CT_CTR)
        # if there is entry in attr level then only append description else throw error msg
        if ct_ctr_value:
            cc_val_desc = ACCValueDesc.get_acc_value_description(self.client, ct_ctr_value)
            if cc_val_desc:
                cc_list, cc_default = ACCValueDesc.append_acc_val_desc(cc_val_desc, cc_default_value)
                cc_default_list = [cc_default]
            else:
                error_msg = get_message_desc(MSG005)[1]
                # msgid = 'MSG005'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg
                # error_msg = MSG005
        else:
            error_msg = get_message_desc(MSG005)[1]
            # msgid = 'MSG005'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            # # error_msg = MSG005

        # Get wbs dropdown list
        wbs_value, wbs_default_value = self.get_attr_value(object_id, CONST_WBS_ELEM)
        # if there is entry in attr level then only append description else throw error msg
        if wbs_value:
            wbs_val_desc = ACCValueDesc.get_acc_value_description(self.client, wbs_value)
            if wbs_val_desc:
                wbs_list, wbs_default = ACCValueDesc.append_acc_val_desc(wbs_val_desc, wbs_default_value)
                wbs_default_list = [wbs_default]
            else:
                error_msg = get_message_desc(MSG005)[1]
                # msgid = 'MSG005'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg
                # # error_msg = MSG005
        else:
            error_msg = get_message_desc(MSG005)[1]
            # msgid = 'MSG005'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            # error_msg = MSG005

        # Get internal order dropdown list
        int_ord_value, int_ord_default_value = self.get_attr_value(object_id, CONST_INT_ORD)
        # if there is entry in attr level then only append description else throw error msg
        if int_ord_value:
            int_ord_val_desc = ACCValueDesc.get_acc_value_description(self.client, int_ord_value)
            if int_ord_val_desc:
                int_ord_list, int_ord_default = ACCValueDesc.append_acc_val_desc(int_ord_val_desc,
                                                                                 int_ord_default_value)
                int_ord_default_list = [int_ord_default]
            else:
                error_msg = get_message_desc(MSG005)[1]
                # msgid = 'MSG005'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg
                # error_msg = MSG005
        else:
            error_msg = get_message_desc(MSG005)[1]
            # msgid = 'MSG005'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            # error_msg = MSG005

        # Get asset dropdown list
        asset_value, asset_default_value = self.get_attr_value(object_id, CONST_AS_SET)
        # if there is entry in attr level then only append description else throw error msg
        if asset_value:
            asset_val_desc = ACCValueDesc.get_acc_value_description(self.client, asset_value)
            if asset_val_desc:
                asset_list, asset_default = ACCValueDesc.append_acc_val_desc(asset_val_desc,
                                                                             asset_default_value)
                asset_default_list = [asset_default]
            else:
                error_msg = get_message_desc(MSG005)[1]
                # msgid = 'MSG005'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg
                # error_msg = MSG005
        else:
            error_msg = get_message_desc(MSG005)[1]
            # msgid = 'MSG005'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            # error_msg = MSG005

        # Get doc search dropdown list
        doc_search_value, doc_search_default_value = self.get_attr_value(object_id, CONST_DEF_DOC_SEARCH)
        # if there is entry in attr level then only append description else throw error msg
        if doc_search_value:
            doc_search_val_desc = DocSearch.get_doc_search_description(doc_search_value)
            if doc_search_val_desc:
                doc_search_list, doc_search_default = DocSearch.append_doc_search_desc(doc_search_val_desc,
                                                                                       doc_search_default_value)
            else:
                error_msg = get_message_desc(MSG005)[1]
                # msgid = 'MSG005'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg
                # error_msg = MSG005
        else:
            error_msg = get_message_desc(MSG005)[1]
            # msgid = 'MSG005'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            # error_msg = MSG005

        # Get delivery addr dropdown list
        addr_value, addr_default_value = self.get_attr_value(object_id, CONST_DEL_ADDR)
        # if there is entry in attr level then only append description else throw error msg
        if addr_value:
            addr_val_desc = Address_desc.get_addr_description(self.client, addr_value, CONST_DEL_ADDR, 'D')
            if addr_val_desc:
                delivery_addr_list, addr_default = Address_desc.append_addr_desc(addr_val_desc,
                                                                                 addr_default_value)
                delivery_addr_default_list = [addr_default]
            else:
                error_msg = get_message_desc(MSG005)[1]
                # msgid = 'MSG005'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg
                # error_msg = MSG005
        else:
            error_msg = get_message_desc(MSG005)[1]
            # msgid = 'MSG005'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            # error_msg = MSG005

        # Get Invoice addr dropdown list
        addr_value, addr_default_value = self.get_attr_value(object_id, CONST_INV_ADDR)
        # if there is entry in attr level then only append description else throw error msg
        if addr_value:
            addr_val_desc = Address_desc.get_addr_description(self.client, addr_value, CONST_INV_ADDR, 'I')
            if addr_val_desc:
                invoice_addr_list, addr_default = Address_desc.append_addr_desc(addr_val_desc,
                                                                                addr_default_value)
                invoice_addr_default_list = [addr_default]
            else:
                error_msg = get_message_desc(MSG005)[1]
                # msgid = 'MSG005'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg
                # error_msg = MSG005
        else:
            error_msg = get_message_desc(MSG005)[1]
            # msgid = 'MSG005'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            # error_msg = MSG005

        # User Role
        attr_id = CONST_US_ROLE
        asg_role_list, asg_role_default_value = self.get_attr_value(object_id, CONST_US_ROLE)

        if asg_role_default_value:
            asg_role_default_list = [asg_role_default_value]
        elif not asg_role_list:
            error_msg = get_message_desc(MSG005)[1]
            # msgid = 'MSG005'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            # error_msg = MSG005

        # Company Code
        attr_id = CONST_CO_CODE
        description = OrgCompanies
        attr_low_value_cc, cc_default = self.get_attr_value(object_id, CONST_CO_CODE)
        # if there is entry in attr level then only append description else throw error msg
        if attr_low_value_cc:
            org_company_list = append_attrlow_desc(self.client, CONST_CO_CODE, description, attr_low_value_cc, True)
            if org_company_list:
                description = OrgPorg
                purch_org_list, porg_data = get_purch_org_info(attr_low_value_cc, self.client, description, True)

                description = OrgPGroup
                purch_grp_list = get_purch_grp_info(self.client, description, porg_data, True)

                spending_limit_list = get_spending_limit_value(self.client, self.login_username, attr_low_value_cc,
                                                               True)

                approver_limit_list = get_approver_limt_value(self.client, self.login_username, attr_low_value_cc, True)

        else:
            error_msg = get_message_desc(MSG005)[1]
            # msgid = 'MSG005'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            # error_msg = MSG005

        user_setting_list = [acc_list, cc_list, wbs_list, int_ord_list, asset_list,
                             doc_search_list, delivery_addr_list, invoice_addr_list,
                             asg_role_list, org_company_list, purch_org_list, purch_grp_list,
                             spending_limit_list, approver_limit_list]
        user_setting_default_list = [acc_default_list, cc_default_list, wbs_default_list, int_ord_default_list,
                                     asset_default_list, doc_search_default_list, delivery_addr_default_list,
                                     invoice_addr_default_list, asg_role_default_list, org_company_default_list,
                                     purch_org_default_list, purch_grp_default_list, spending_limit_default_list,
                                     approver_limit_default_list]
        if '' in user_setting_list:
            error_msg = get_message_desc(MSG005)[1]
            # msgid = 'MSG005'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            # error_msg = MSG005
        if '' in user_setting_default_list:
            error_msg = get_message_desc(MSG005)[1]
            # msgid = 'MSG005'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            # error_msg = MSG005

        return user_setting_list, user_setting_default_list, error_msg

    def get_attr_value(self, object_id, attr_id):
        """
        get attribute values of the user
        :param edit_flag:
        :param client: log in client value
        :param attr_id: attribute id
        :param object_id: object id of login user
        :return: OrgAttributes low value list
        """
        # get attr value list from attr level table
        attr_value = self.get_attr_list(object_id, attr_id)
        # get default attr value
        attr_default = self.get_attr_default(object_id, attr_id)

        return attr_value, attr_default

    def get_attr_list(self, object_id, attr_id):
        """

        :param object_id:
        :param attr_id:
        :return:
        """
        acc_asign_cat = []
        acc_asign_cat = OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(object_id, attr_id)[0]
        return acc_asign_cat

    def get_attrs_list(self, object_id, attr_id):
        """

        :param object_id:
        :param attr_id:
        :return:
        """
        acc_asign_cat = []
        acc_asign_cat = OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(object_id, attr_id)[0]

        return acc_asign_cat

    def get_attr_default(self, object_id, attr_id):
        """
        get default attribute
        :param client:login client
        :param object_id:
        :param login_user_obj_id:
        :param attr_id:
        :return:
        """
        attr_default = []
        attr_default = OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(object_id, attr_id)[1]

        return attr_default


class DocSearch:

    @staticmethod
    def get_doc_search_description(attr_value_list):
        """
        get account assignment category description
        :param attr_value_list:
        :return:
        """
        doc_search_value = []
        if DocumentType.objects.filter(Q(document_type__in=attr_value_list) & Q(del_ind=False)).exists():
            doc_search_value = DocumentType.objects.filter(
                Q(document_type__in=attr_value_list) & Q(del_ind=False)).values('document_type',
                                                                                'document_type_desc')
        return doc_search_value

    @staticmethod
    def append_doc_search_desc(doc_search_val_desc, doc_search_default_value, doc_type_drop_down_list):
        """

        :param doc_search_val_desc:
        :param doc_search_default_value:
        :return:
        """
        doc_search_append_val_desc = append_description_atrr_value_exists(doc_search_val_desc,
                                                                          doc_type_drop_down_list,
                                                                          'document_type',
                                                                          'document_type_desc')[1]
        for doc_search_val_desc in doc_search_append_val_desc:
            doc_search = doc_search_val_desc.split(" - ")
            if doc_search[0] == doc_search_default_value:
                doc_search_default_value = doc_search_val_desc
        doc_search_append_val_desc = list_remove_insert_first(doc_search_append_val_desc, doc_search_default_value)

        return doc_search_append_val_desc, [doc_search_default_value]


def append_attrlow_desc(client, attr_id, description, attr_value_list, edit_flag):
    """
    concatenate attr low value and description
    :param client: login client
    :param attr_id:
    :param description:
    :param attr_value_list:
    :param edit_flag:
    :return: append attr low value and description
    """

    array_acc = []
    desc_value = None
    addr_detail = None

    if attr_id == 'ACC_CAT':
        if edit_flag:
            for acc_cat in attr_value_list:
                if description.objects.filter(Q(account_assign_cat=acc_cat)).exists():
                    aac_value = description.objects.get(Q(account_assign_cat=acc_cat))
                    array_acc.append(concatenate_str(acc_cat, aac_value.description))
            return array_acc

        else:
            if description.objects.filter(Q(account_assign_cat=attr_value_list)).exists():
                default_attr_value = description.objects.filter(Q(account_assign_cat=attr_value_list)).values(
                    'description')
                for default_attr in default_attr_value:
                    desc_value = default_attr['description']
                array_acc.append(concatenate_str(attr_value_list, desc_value))
                return array_acc
            else:
                return array_acc
    elif attr_id in ['CT_CTR', 'WBS_ELEM', 'INT_ORD', 'AS_SET']:
        if edit_flag:
            for acc_cat in attr_value_list:

                if description.objects.filter(Q(account_assign_value=acc_cat) &
                                              Q(client=client)).exists():
                    aac_value = description.objects.filter(Q(account_assign_value=acc_cat) &
                                                           Q(client=client))[0]

                    array_acc.append(concatenate_str(acc_cat, aac_value.description))
            return array_acc
        else:
            if description.objects.filter(Q(account_assign_value=attr_value_list) &
                                          Q(client=client)).exists():

                default_attr_value = description.objects.filter(Q(account_assign_value=attr_value_list,
                                                                  client=client)).values('description')
                if default_attr_value:
                    for default_attr in default_attr_value:
                        desc_value = default_attr['description']
                    array_acc.append(concatenate_str(attr_value_list, desc_value))
                    return array_acc
            else:
                return array_acc

    elif attr_id == CONST_DEF_DOC_SEARCH:
        if edit_flag:
            for Doc_search in attr_value_list:
                if description.objects.filter(Q(document_type=Doc_search)).exists():

                    doc_value_list = description.objects.filter(Q(document_type=Doc_search)).values(
                        'document_type_desc')
                    for aac_value in doc_value_list:
                        array_acc.append(concatenate_str(Doc_search, aac_value['document_type_desc']))
            return array_acc

        else:
            if description.objects.filter(Q(document_type=attr_value_list)).exists():

                default_attr_value = description.objects.filter(Q(document_type=attr_value_list)).values(
                    'document_type_desc')
                for default_attr in default_attr_value:
                    desc_value = default_attr['document_type_desc']
                array_acc.append(concatenate_str(attr_value_list, desc_value))
                return array_acc
            else:
                return array_acc

    elif attr_id in [CONST_DEL_ADDR, CONST_INV_ADDR]:
        if edit_flag:
            for acc_cat in attr_value_list:
                if description.objects.filter(address_number=acc_cat).exists():
                    aac_value = description.objects.values_list('address_number',
                                                                'address_type',
                                                                flat=False).filter(address_number=acc_cat)
                    for addr_num, addr_type, in aac_value:
                        if addr_type == 'D' and attr_id == CONST_DEL_ADDR:
                            addr_detail = OrgAddress.objects.get(Q(address_number=addr_num, client=client))
                        elif addr_type == 'I' and attr_id == CONST_INV_ADDR:
                            addr_detail = OrgAddress.objects.get(Q(address_number=addr_num, client=client))
                    if addr_detail:
                        addr = addr_detail.street + ' / ' + addr_detail.area + ' / ' + addr_detail.landmark + ' / ' + addr_detail.city + ' / ' + addr_detail.postal_code + ' / ' + addr_detail.region
                        array_acc.append(concatenate_str(acc_cat, addr))
            return array_acc
        else:

            if description.objects.filter(address_number=attr_value_list).exists():
                aac_value = description.objects.values_list('address_number',
                                                            'address_type',
                                                            flat=False).filter(address_number=attr_value_list)

                for addr_num, addr_type, in aac_value:
                    if addr_type == 'D' and attr_id == CONST_DEL_ADDR:
                        addr_detail = OrgAddress.objects.get(Q(address_number=addr_num, client=client))
                    elif addr_type == 'I' and attr_id == CONST_INV_ADDR:
                        addr_detail = OrgAddress.objects.get(Q(address_number=addr_num, client=client))
                if addr_detail:
                    desc_value = addr_detail.street + ' / ' + addr_detail.area + ' / ' + addr_detail.landmark + ' / ' + addr_detail.city + ' / ' + addr_detail.postal_code + ' / ' + addr_detail.region
                    array_acc.append(concatenate_str(attr_value_list, desc_value))
                return array_acc
            else:
                return array_acc

    elif attr_id == CONST_CO_CODE:
        if edit_flag:
            for co_code in attr_value_list:
                if description.objects.filter(Q(company_id=co_code) &
                                              Q(client=client)).exists():
                    aac_value = description.objects.get(Q(company_id=co_code) &
                                                        Q(client=client))
                    array_acc.append(concatenate_str(co_code, aac_value.name1))
            return array_acc
        else:
            if description.objects.filter(Q(company_id=attr_value_list) &
                                          Q(client=client)).exists():

                default_attr_value = description.objects.filter(Q(company_id=attr_value_list,
                                                                  client=client)).values('name1')

                for default_attr in default_attr_value:
                    desc_value = default_attr['name1']
                array_acc.append(concatenate_str(attr_value_list, desc_value))
                return array_acc
            else:
                return array_acc
    return array_acc


def get_purch_org_info(Company_code_list, client, description, edit_flag):
    """
    get purchase org and grp detail
    :param Company_code_list:
    :param client:
    :param description:
    :param nodetype:
    :param edit_flag:
    :return:
    """
    purch = []
    purch_default = []
    cc_nodeguid = None
    porg_data = []

    if edit_flag:
        for default_cc in Company_code_list:

            purch_org = description.objects.filter(Q(company_id=default_cc,
                                                     client=client)).values('porg_id',
                                                                            'description')

            for purch_org_array in purch_org:
                porg_data.append(purch_org_array['porg_id'])
                array_list = purch_org_array['porg_id'] + ' - ' + purch_org_array['description']
                purch.append(array_list)
        return purch, porg_data
    else:

        purch_org = description.objects.filter(Q(company_id=Company_code_list,
                                                 client=client)).values('porg_id',
                                                                        'description')
        for purch_org_array in purch_org:
            porg_data.append(purch_org_array['porg_id'])
            array_list = purch_org_array['porg_id'] + ' - ' + purch_org_array['description']
            purch.append(array_list)
    return purch, porg_data


def get_purch_grp_info(client, description, porg_data, edit_flag):
    purch = []
    if edit_flag:
        for porg_id in porg_data:
            if description.objects.filter(Q(porg_id=porg_id,
                                            client=client)).exists():

                purch_grp = description.objects.filter(Q(porg_id=porg_id,
                                                         client=client)).values('pgroup_id',
                                                                                'description')
                for purch_org_array in purch_grp:
                    array_list = purch_org_array['pgroup_id'] + ' - ' + purch_org_array['description']
                    purch.append(array_list)
        return purch
    else:

        if description.objects.filter(Q(porg_id=porg_data,
                                        client=client)).exists():

            purch_grp = description.objects.filter(Q(porg_id=porg_data,
                                                     client=client)).values('pgroup_id',
                                                                            'description')
            for purch_org_array in purch_grp:
                array_list = purch_org_array['pgroup_id'] + ' - ' + purch_org_array['description']
                purch.append(array_list)
        return purch


# def save_default_value(client, obj_id_list, login_user_obj_id, ui_input_value, attr_id):
#     """
#     save default value to attribute level db table
#     :param client: log in client value
#     :param obj_id_list: list of object id of login user and its parent
#     :param ui_input_value: value of dropdown selected by user
#     :param attr_id: attribute id
#     :param num_char: no. of characters of low value
#     """
#     attr_level_value = split_str(ui_input_value, " - ")
#     parent_obj_id = []
#     for obj_id in obj_id_list:
#         if obj_id != login_user_obj_id:
#             parent_obj_id.append(int(obj_id))
#
#     # remove/clear default entry for login user object id in attr level and attr level flag
#     django_query_instance.django_filter_delete_query(OrgAttributesLevelFlag, {
#         'object_id': login_user_obj_id, 'client': client, 'attribute_id': attr_id
#     })
#
#     django_query_instance.django_filter_only_query(OrgAttributesLevel, {
#         'object_id': login_user_obj_id, 'client': client, 'attr_level_default': True,
#         'attribute_id': attr_id, 'del_ind': False
#     }).update(attr_level_default=False)
#
#     # check if attr value exist in user node
#     if (OrgAttributesLevel.objects.filter(Q(object_id=login_user_obj_id,
#                                             client=client,
#                                             low=attr_level_value,
#                                             attribute_id=attr_id, del_ind=False)).exists()):
#         # check if attr low value inherited or not
#         if not (OrgAttributesLevel.objects.filter(Q(object_id__in=parent_obj_id,
#                                                     client=client,
#                                                     low=attr_level_value,
#                                                     attribute_id=attr_id, del_ind=False)).exists()):
#             # if attr value not inherited then update default flag
#             django_query_instance.django_filter_only_query(OrgAttributesLevel, {
#                 'object_id': login_user_obj_id,
#                 'client': client,
#                 'low': attr_level_value,
#                 'attribute_id': attr_id, 'del_ind': False
#             }).update(attr_level_default=True)
#     else:
#         # if default inherited then store in attr level flag
#         django_query_instance.django_create_query(OrgAttributesLevelFlag, {
#             'attr_level_flag_guid': guid_generator(),
#             'object_id': django_query_instance.django_get_query(OrgModel, {'object_id': login_user_obj_id}),
#             'client': django_query_instance.django_get_query(OrgClients, {'client': client}),
#             'value': attr_level_value,
#             'attr_level_flag_default': True,
#             'attribute_id': django_query_instance.django_get_query(OrgAttributes, {'attribute_id': attr_id})
#         })
#
#
# # END of SC-US-US02 and SC-US-US03

def get_spending_limit_value(client, login_username, attr_low_value_cc, edit_flag):
    """
    get spending limt value and its description apend to it
    :param client: log in client value
    :param login_username:  login user name
    :param attr_low_value_cc: company code value
    :param edit_flag: flag for disable and edit mode
    :return: appended spending limit value and description
    """
    sl_list_array = []
    if edit_flag:

        for company_code in attr_low_value_cc:
            sl_value = SpendLimitId.objects.values_list('spend_code_id',
                                                        flat=False).filter(Q(company_id=company_code,
                                                                             spender_username=login_username,
                                                                             client=client))
            for spend_code_id, in sl_value:
                sl_list = SpendLimitValue.objects.values_list('company_id',
                                                              'upper_limit_value',
                                                              'currency_id',
                                                              flat=False).filter(Q(company_id=company_code,
                                                                                   spend_code_id=spend_code_id,
                                                                                   client=client))

                if sl_list:
                    sl_list_cc = list(map(lambda x: str('%s - %s %s' % (company_code, x[1], x[2])), sl_list))

                    sl_list_array.append(sl_list_cc[0])
    else:
        sl_value = SpendLimitId.objects.values_list('spend_code_id',
                                                    flat=False).filter(Q(company_id=attr_low_value_cc,
                                                                         spender_username=login_username,
                                                                         client=client))
        for spend_code_id, in sl_value:
            sl_list = SpendLimitValue.objects.values_list('company_id',
                                                          'upper_limit_value',
                                                          'currency_id',
                                                          flat=False).filter(Q(company_id=attr_low_value_cc,
                                                                               spend_code_id=spend_code_id,
                                                                               client=client))

            if sl_list:
                sl_list_cc = list(map(lambda x: str('%s - %s %s' % (attr_low_value_cc, x[1], x[2])), sl_list))

                sl_list_array = [sl_list_cc[0]]

    return sl_list_array


def get_approver_limt_value(client, login_username, attr_low_value_cc, edit_flag):
    """
    get approver limt value and its description apend to it
    :param client: login client value
    :param login_username: login username
    :param attr_low_value_cc: company code value
    :param edit_flag: flag for disable and edit mode
    :return: appended approver limit value and description
    """
    al_list_array = []
    if edit_flag:
        for company_code in attr_low_value_cc:
            al_value = ApproverLimit.objects.values_list('app_code_id',
                                                         flat=False).filter(Q(company_id=company_code,
                                                                              approver_username=login_username,
                                                                              client=client))
            for app_code_id, in al_value:
                al_list = ApproverLimitValue.objects.values_list('company_id',
                                                                 'upper_limit_value',
                                                                 'currency_id',
                                                                 flat=False).filter(Q(company_id=company_code,
                                                                                      app_code_id=app_code_id,
                                                                                      app_types=CONST_FIN,
                                                                                      client=client))

                if al_list:
                    al_list_cc = list(map(lambda x: str('%s - %s %s' % (company_code, x[1], x[2])), al_list))
                    al_list_array.append(al_list_cc[0])
    else:
        al_value = ApproverLimit.objects.values_list('app_code_id',
                                                     flat=False).filter(Q(company_id=attr_low_value_cc,
                                                                          approver_username=login_username,
                                                                          client=client))

        for app_code_id, in al_value:
            al_list = ApproverLimitValue.objects.values_list('company_id',
                                                             'upper_limit_value',
                                                             'currency_id',
                                                             flat=False).filter(Q(company_id=attr_low_value_cc,
                                                                                  app_code_id=app_code_id,
                                                                                  app_id=CONST_FIN,
                                                                                  client=client))

            if al_list:
                al_list_cc = list(map(lambda x: str('%s - %s %s' % (attr_low_value_cc, x[1], x[2])), al_list))
                al_list_array = [al_list_cc[0]]

    return al_list_array
