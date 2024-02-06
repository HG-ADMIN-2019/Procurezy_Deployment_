from eProc_Account_Assignment.Utilities.account_assignment_specific import ACC_CAT, ACCValueDesc
from eProc_Attributes.Utilities.attributes_generic import OrgAttributeValues
from eProc_Attributes.Utilities.attributes_specific import append_description_atrr_value_exists, \
    append_attribute_value_description
from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.dictionary_check_value_based_for_key import dictionary_check_value_based_for_key, \
    dictionary_check_get_value_based_for_key
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.ignore_duplicates import remove_duplicates_in_dic_list, \
    remove_duplicate_element_array
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.functions.str_concatenate import concatenate_array_str, concatenate_str
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG115
from eProc_Configuration.models import AccountingDataDesc, DetermineGLAccount
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import get_gl_account_default_value
from eProc_System_Settings.Utilities.system_settings_generic import sys_attributes
from eProc_User_Settings.Utilities.user_settings_generic import get_attr_value
from eProc_User_Settings.Utilities.user_settings_specific import UserSettings, append_attrlow_desc


def get_default_gl_acc(default_company_code, default_acc, item_prod_cat, item_total_value, item_currency, language_id):
    """

    """
    det_default_gl_acc_filter_dict = {
        'client': global_variables.GLOBAL_CLIENT,
        'prod_cat_id': item_prod_cat,
        'account_assign_cat': default_acc,
        'item_from_value__lt': int(item_total_value),
        'item_to_value__gt': int(item_total_value),
        'company_id': default_company_code,
        'currency_id': item_currency,
        'gl_acc_default': True,
        'del_ind': False
    }
    gl_acc_num_detail = ''
    gl_acc_detail = ''
    if DjangoQueries.django_existence_check(DetermineGLAccount, det_default_gl_acc_filter_dict):
        gl_acc_num_detail = DjangoQueries.django_filter_value_list_query(DetermineGLAccount,
                                                                         det_default_gl_acc_filter_dict,
                                                                         'gl_acc_num')[0]
        gl_acc_detail = ACCValueDesc.append_gl_account_value_desc(gl_acc_num_detail, default_company_code, language_id)

    return gl_acc_detail


class AccountAssignment:

    def __init__(self, user_object_id_list):
        self.user_object_id_list = user_object_id_list
        self.user_setting = UserSettings()
        self.client = global_variables.GLOBAL_CLIENT
        self.get_attribute_id = {
            'CC': CONST_CT_CTR,
            'WBS': CONST_WBS_ELEM,
            'AS': CONST_AS_SET,
            'OR': CONST_INT_ORD
        }

    def get_account_assignment_default_and_available_list(self):
        return self.user_setting.get_attr_value(self.user_object_id_list, CONST_ACC_CAT)

    def get_accounting_data(self, total_value, company_code):
        """

        """
        acc_list = []
        acc_value = []
        acc_value_list = []
        acc_default = []
        default_acc = []
        default_gl_account = ''

        acc_cat_value, acc_cat_default_value = AccountAssignment(self.user_object_id_list) \
            .get_account_assignment_default_and_available_list()

        if acc_cat_value:
            acc_val_desc = ACC_CAT.get_acc_cat_description(acc_cat_value)
            acc_list, acc_default = ACC_CAT.append_acc_val_desc(acc_val_desc, acc_cat_default_value)
            description = AccountingDataDesc

            attribute_id = self.get_attribute_id[acc_cat_default_value]
            default_acc = get_attr_value(self.client, attribute_id, self.user_object_id_list, False)
            ct_ctr_value = get_attr_value(self.client, attribute_id, self.user_object_id_list, True)
            acc_value = append_attrlow_desc(self.client, attribute_id, description, default_acc, False)
            acc_value_list = append_attrlow_desc(self.client, attribute_id, description, ct_ctr_value, True)
            default_gl_account = get_gl_account_default_value(self.client, total_value, company_code,
                                                              acc_cat_default_value)

        return {
            'acc_list': acc_list,
            'acc_default': acc_default,
            'acc_value': acc_value,
            'acc_value_list': acc_value_list,
            'default_gl_account': default_gl_account,
            'default_acc': default_acc
        }

    def change_account_assignment_category(self, account_assignment_type, company_code, item_prod_cat,
                                           item_total_value, item_currency, item_language):
        """

        """
        acc_value = ''
        attribute_id = get_attribute_id_based_on_acc(account_assignment_type)
        default_gl_account = get_default_gl_acc(company_code, account_assignment_type, item_prod_cat, item_total_value,
                                                item_currency, item_language)
        acc_value_default_desc = ACCValueDesc.get_acc_default_values_and_desc_append_list(self.user_object_id_list,
                                                                                          attribute_id, company_code,
                                                                                          account_assignment_type)

        if acc_value_default_desc:
            acc_value = acc_value_default_desc[0]['attribute_values_description']
        return {
            'acc_value': acc_value,
            'default_gl_account': default_gl_account,

        }


class AccountAssignmentCategoryDetails:
    def __init__(self, user_parent_object_id_list, default_company_code, item_detail_list):
        self.user_parent_object_id_list = user_parent_object_id_list
        self.default_company_code = default_company_code
        self.item_detail_list = item_detail_list

    def get_acc_list_and_default1(self):
        """

        """
        acc_value_list = []
        default_acc_value = []
        acc_desc_list = []
        acc_default_desc = []
        acc_details = ACC_CAT.get_org_model_configured_acc_and_desc(self.user_parent_object_id_list,
                                                                    CONST_ACC_CAT)

        # get default account assignment categories value configured in org attribute level table
        if acc_details['default_acc'] == CONST_CC:
            acc_value_list, default_acc_value = OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(
                self.user_parent_object_id_list,
                CONST_CT_CTR)
        elif acc_details['default_acc'] == CONST_WBS:
            acc_value_list, default_acc_value = OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(
                self.user_parent_object_id_list,
                CONST_WBS_ELEM)
        elif acc_details['default_acc'] == CONST_OR:
            acc_value_list, default_acc_value = OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(
                self.user_parent_object_id_list,
                CONST_INT_ORD)
        elif acc_details['default_acc'] == CONST_AS:
            acc_value_list, default_acc_value = OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(
                self.user_parent_object_id_list,
                CONST_AS_SET)
        else:
            msgid = 'MSG115'
            error_msg = get_message_desc(msgid)[1]

        acc_value_desc = ACCValueDesc.get_acc_value_desc(acc_value_list, self.default_company_code,
                                                         acc_details['default_acc'])

        acc_value_list_desc, acc_default_val_desc = ACCValueDesc.append_acc_val_desc_if_exists(acc_value_desc,
                                                                                               default_acc_value,
                                                                                               acc_value_list)
        gl_acc_item_level_default, header_level_gl_acc = AccountAssignmentCategoryDetails.get_gl_acc_default_value(self,
                                                                                                                   acc_details[
                                                                                                                       'default_acc'])
        client = global_variables.GLOBAL_CLIENT
        sys_attributes_instance = sys_attributes(client)
        acct_assignment_category = sys_attributes_instance.get_acct_assignment_category()
        acc_details = {
            'acc_list': acc_details['acc_desc_list'],
            'acc_default': acc_details['acc_default_desc'],
            'acc_value': [acc_default_val_desc],
            'acc_value_list': acc_value_list_desc,
            'default_acc': default_acc_value,
            'default_acc_ass_cat': acc_details['default_acc'],
            'gl_acc_item_level_default': gl_acc_item_level_default,
            'header_level_gl_acc': header_level_gl_acc,
            'acct_assignment_category': acct_assignment_category
        }
        return acc_details

    def get_acc_list_and_default(self):
        """

        """
        acc_value_list = []
        default_acc_value = []
        acc_desc_list = []
        acc_default_desc = []
        acc_details = ACC_CAT.get_org_model_configured_acc_and_desc(self.user_parent_object_id_list,
                                                                    CONST_ACC_CAT)
        # get account assignment category list and its default from org attribute level table
        acc_list, default_acc = OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(
            self.user_parent_object_id_list,
            CONST_ACC_CAT)
        acc_desc_append_list, default_acc_desc = ACC_CAT.get_acc_append_desc(acc_list, default_acc)

        if default_acc_desc:
            # get default account assignment categories value configured in org attribute level table
            if default_acc_desc['account_assign_cat'] == CONST_CC:
                acc_value_list, default_acc_value = OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(
                    self.user_parent_object_id_list,
                    CONST_CT_CTR)
            elif default_acc_desc['account_assign_cat'] == CONST_WBS:
                acc_value_list, default_acc_value = OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(
                    self.user_parent_object_id_list,
                    CONST_WBS_ELEM)
            elif default_acc_desc['account_assign_cat'] == CONST_OR:
                acc_value_list, default_acc_value = OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(
                    self.user_parent_object_id_list,
                    CONST_INT_ORD)
            elif default_acc_desc['account_assign_cat'] == CONST_AS:
                acc_value_list, default_acc_value = OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(
                    self.user_parent_object_id_list,
                    CONST_AS_SET)

        acc_value_desc = ACCValueDesc.get_acc_value_desc(acc_value_list, self.default_company_code,
                                                         acc_details['default_acc'])

        acc_value_list_desc, acc_default_val_desc = ACCValueDesc.append_acc_val_desc_if_exists(acc_value_desc,
                                                                                               default_acc_value,
                                                                                               acc_value_list)
        gl_acc_item_level_default, header_level_gl_acc = AccountAssignmentCategoryDetails.get_gl_acc_default_value(self,
                                                                                                                   acc_details[
                                                                                                                       'default_acc'])
        client = global_variables.GLOBAL_CLIENT
        sys_attributes_instance = sys_attributes(client)
        acct_assignment_category = sys_attributes_instance.get_acct_assignment_category()
        acc_details = {
            'acc_list': acc_details['acc_desc_list'],
            'acc_default': acc_details['acc_default_desc'],
            'acc_value': [acc_default_val_desc],
            'acc_value_list': acc_value_list_desc,
            'default_acc': default_acc_value,
            'default_acc_ass_cat': acc_details['default_acc'],
            'gl_acc_item_level_default': gl_acc_item_level_default,
            'header_level_gl_acc': header_level_gl_acc,
            'acct_assignment_category': acct_assignment_category,
            'acc_desc_append_list': acc_desc_append_list,
            'default_acc_desc': default_acc_desc,
            'account_assign_cat_list':acc_list
        }
        return acc_details

    def get_gl_acc_default_value(self, default_acc):
        """
        :param client:
        :param total_value:
        :param cc:
        :param account_assign_cat:
        :return:
        """
        single_multiple = []
        gl_acc_default = []
        header_level_gl_acc = ''
        for item in self.item_detail_list:
            gl_acc_detail = {'cart_item_guid': item['guid']}
            item_value = float(item['value'])
            gl_acc_detail['default_gl_acc'] = get_default_gl_acc(self.default_company_code, default_acc,
                                                                 item['prod_cat'], item_value,
                                                                 global_variables.GLOBAL_REQUESTER_CURRENCY,
                                                                 global_variables.GLOBAL_REQUESTER_LANGUAGE)
            gl_acc_default.append(gl_acc_detail)
            single_multiple.append(gl_acc_detail['default_gl_acc'])
            header_level_gl_acc = get_header_level_gl_acc(single_multiple)

        return gl_acc_default, header_level_gl_acc


def get_gl_acc_value(item_detail_list, company_code):
    """
    :param client:
    :param total_value:
    :param cc:
    :param account_assign_cat:
    :return:
    """
    gl_acc_default = []
    gl_acc_num = []
    gl_desc = []
    det_gl_acc_filter_dict = {
        'client': global_variables.GLOBAL_CLIENT,
        'prod_cat_id': item_detail_list['prod_cat'],
        'account_assign_cat': item_detail_list['acc'],
        'item_from_value__lt': item_detail_list['value'],
        'item_to_value__gt': item_detail_list['value'],
        'company_id': company_code,
        'del_ind': False
    }
    gl_acc_num_detail = DjangoQueries.django_filter_value_list_query(DetermineGLAccount,
                                                                     det_gl_acc_filter_dict,
                                                                     'gl_acc_num')
    acc_data_desc_filter = {'client': global_variables.GLOBAL_CLIENT,
                            'company_id': company_code,
                            'account_assign_value__in': gl_acc_num_detail,
                            'account_assign_cat': CONST_GLACC}
    acc_data_desc_values = ['account_assign_value', 'description']
    gl_acc_desc = DjangoQueries.django_filter_query(AccountingDataDesc, acc_data_desc_filter, None,
                                                    acc_data_desc_values)
    gl_acc_asg_desc_list = append_description_atrr_value_exists(gl_acc_desc,
                                                                gl_acc_num_detail,
                                                                'account_assign_value',
                                                                'description')[0]
    return gl_acc_asg_desc_list


def get_header_level_gl_acc(glacc_list):
    """

    """
    gl_acc_list = remove_duplicate_element_array(glacc_list)
    if len(gl_acc_list) == 1:
        header_level_gl_acc = 'Single'
    elif len(gl_acc_list) > 1:
        header_level_gl_acc = 'Multiple'
    else:
        header_level_gl_acc = None
    return header_level_gl_acc

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

def get_acc_value_and_description_append(acc_detail, acc_asg_cat, default_company_code, language_id):
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


def get_attribute_id_based_on_acc(account_assignment_cat):
    """

    """
    attribute_id = ''
    if account_assignment_cat == CONST_CC:
        attribute_id = CONST_CT_CTR
    elif account_assignment_cat == CONST_OR:
        attribute_id = CONST_INT_ORD
    elif account_assignment_cat == CONST_WBS:
        attribute_id = CONST_WBS_ELEM
    elif account_assignment_cat == CONST_AS:
        attribute_id = CONST_AS_SET
    return attribute_id


def get_acc_details(object_id_list, company_code, item_detail_list):
    """

    """
    acc_obj = AccountAssignmentCategoryDetails(object_id_list, company_code, item_detail_list)
    accounting_data = acc_obj.get_acc_list_and_default()
    return accounting_data


def get_prod_cat_value_guid(cart_items):
    """

    """
    item_list = []
    for cart_item in cart_items:
        item_list.append({'guid': cart_item['guid'],
                          'prod_cat': cart_item['prod_cat_id'],
                          'value': cart_item['value']})
    return item_list
