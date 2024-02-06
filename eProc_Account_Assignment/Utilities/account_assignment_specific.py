from django.db.models import Q

from eProc_Attributes.Utilities.attributes_generic import OrgAttributeValues
from eProc_Attributes.Utilities.attributes_specific import append_description_atrr_value_exists
from eProc_Basic.Utilities.constants.constants import CONST_GLACC, CONST_DEFAULT_LANGUAGE
from eProc_Basic.Utilities.functions.dictionary_check_value_based_for_key import dictionary_check_value_based_for_key, \
    dictionary_check_get_value_based_for_key
from eProc_Basic.Utilities.functions.insert_remove import list_remove_insert_first
from eProc_Basic.Utilities.functions.str_concatenate import concatenate_str, concatenate_array_str
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import *
from eProc_Configuration.models import AccountAssignmentCategory, AccountingDataDesc, DetermineGLAccount
from eProc_Org_Model.Utilities import client
from eProc_System_Settings.Utilities.system_settings_generic import sys_attributes


class ACC_CAT:

    @staticmethod
    def get_acc_cat_description(attr_value_list):
        """
        get account assignment category description
        :param attr_value_list:
        :return:
        """
        aac_asg_cat = []
        if AccountAssignmentCategory.objects.filter(Q(account_assign_cat__in=attr_value_list, del_ind=False)).exists():
            aac_asg_cat = AccountAssignmentCategory.objects.filter(
                Q(account_assign_cat__in=attr_value_list, del_ind=False)).values('account_assign_cat',
                                                                                 'description')
        return aac_asg_cat

    @staticmethod
    def append_acc_val_desc(acc_val_desc, acc_cat_default_value):
        """

        :param acc_val_desc:
        :param acc_cat_default_value:
        :return:
        """
        attr_val = []
        attr_desc = []
        acc_append_default_val_desc = []
        acc_append_val_desc = []
        if acc_val_desc:
            for value_desc in acc_val_desc:
                if acc_cat_default_value:
                    if acc_cat_default_value == value_desc['account_assign_cat']:
                        acc_append_default_val_desc = concatenate_str(value_desc['account_assign_cat'],
                                                                      value_desc['description'])
                attr_val.append(value_desc['account_assign_cat'])
                attr_desc.append(value_desc['description'])
            acc_append_val_desc = concatenate_array_str(attr_val, attr_desc)
            if acc_append_default_val_desc:
                acc_append_val_desc = remove_insert(acc_append_val_desc, acc_append_default_val_desc)
        return acc_append_val_desc, acc_append_default_val_desc

    @staticmethod
    def append_acc_ass_desc(acc_val_desc):
        """

        :param acc_val_desc:
        :return:
        """

        append_val_desc = []
        if acc_val_desc:
            for value_desc in acc_val_desc:
                myDict = {}
                myDict["account_assign_cat"] = value_desc['account_assign_cat']
                desc = concatenate_str(value_desc['account_assign_cat'], value_desc['description'])
                myDict["append_val"] = desc
                append_val_desc.append(myDict)

        return append_val_desc

    @staticmethod
    def get_accounting_desc_append_acc_value(acc_drop_down_list, default_acc_list):
        acc_default_list = []
        error_msg = ''
        acc_list = []
        acc_val_desc = ACC_CAT.get_acc_cat_description(acc_drop_down_list)
        if acc_val_desc:
            acc_list_desc = append_description_atrr_value_exists(acc_val_desc,
                                                                 acc_drop_down_list,
                                                                 'account_assign_cat',
                                                                 'description')[1]
            default_acc_val_desc = ACC_CAT.get_acc_cat_description([default_acc_list])
            acc_default_list = append_description_atrr_value_exists(default_acc_val_desc,
                                                                    [default_acc_list],
                                                                    'account_assign_cat',
                                                                    'description')[1]
            if acc_default_list:
                acc_list = list_remove_insert_first(acc_list_desc, acc_default_list[0])
        return acc_list, acc_default_list, error_msg

    @staticmethod
    def get_org_model_configured_acc_and_desc(user_parent_object_id_list, org_attr_id):
        acc_desc_list = ''
        acc_default_desc = ''

        # get account assignment category list and its default from org attribute level table
        acc_list, default_acc = OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(
            user_parent_object_id_list,
            org_attr_id)

        # get account assignment category description  and append it to its respective ACC
        if acc_list:
            acc_val_desc = ACC_CAT.get_acc_cat_description(acc_list)
            acc_desc_list, acc_default_desc = ACC_CAT.append_acc_val_desc(acc_val_desc, default_acc)
        acc_dictionary = {'acc_list': acc_list,
                          'default_acc': default_acc,
                          'acc_desc_list': acc_desc_list,
                          'acc_default_desc': acc_default_desc}
        return acc_dictionary

    @staticmethod
    def get_acc_append_desc(acc_list, default_acc):
        """

        """
        default_acc_desc = None
        acc_desc_append_list = []
        if acc_list:
            acc_val_desc = ACC_CAT.get_acc_cat_description(acc_list)
            for acc in acc_list:
                acc_desc_detail = dictionary_check_get_value_based_for_key(acc_val_desc, 'account_assign_cat', acc)
                if acc_desc_detail:
                    acc_dic = {'account_assign_cat': acc,
                               'account_assign_cat_desc': concatenate_str(acc_desc_detail['account_assign_cat'],
                                                           acc_desc_detail['description'])}
                else:
                    acc_dic = {'account_assign_cat': acc,
                               'account_assign_cat_desc': acc}
                if default_acc == acc:
                    acc_desc_append_list.insert(0, acc_dic)
                    default_acc_desc = acc_dic
                else:
                    acc_desc_append_list.append(acc_dic)
        return acc_desc_append_list, default_acc_desc


class ACCValueDesc:

    @staticmethod
    def get_acc_value_desc_append_acc_value_desc(acc_drop_down_list, default_acc_list, company_code_id, acc_asg_cat):
        """

        :param acc_drop_down_list:
        :param default_acc_list:
        :param company_code_id:
        :param acc_asg_cat:
        :return:
        """
        error_msg = ''
        acc_list = ''
        acc_asg_value_desc = ACCValueDesc.get_acc_value_desc(acc_drop_down_list, company_code_id, acc_asg_cat)
        if acc_asg_value_desc:
            acc_drop_down_list = append_description_atrr_value_exists(acc_asg_value_desc,
                                                                      acc_drop_down_list,
                                                                      'account_assign_value',
                                                                      'description')[1]
            default_acc_val_desc = ACCValueDesc.get_acc_value_desc([default_acc_list], company_code_id, acc_asg_cat)
            default_acc_list = append_description_atrr_value_exists(default_acc_val_desc,
                                                                    [default_acc_list],
                                                                    'account_assign_value',
                                                                    'description')[1]
            if default_acc_list:
                acc_drop_down_list = list_remove_insert_first(acc_drop_down_list, default_acc_list[0])

        # if acc_asg_value_desc:
        #     acc_drop_down_list, default_acc_list = ACCValueDesc.append_acc_val_desc(acc_asg_value_desc,
        #                                                                             default_acc_list)
        #     default_acc_list = [default_acc_list]
        # else:
        #     error_msg = MSG117 + acc_asg_cat
        #     default_acc_list = [default_acc_list]
        return acc_drop_down_list, default_acc_list, error_msg

    @staticmethod
    def get_acc_value_desc(attr_value_list, company_code, account_assign_cat):
        """

        """
        acc_description = []
        if AccountingDataDesc.objects.filter(Q(account_assign_value__in=attr_value_list) &
                                             Q(account_assign_cat=account_assign_cat) &
                                             Q(language_id=global_variables.GLOBAL_USER_LANGUAGE) &
                                             Q(company_id=company_code) &
                                             Q(client=global_variables.GLOBAL_CLIENT) &
                                             Q(del_ind=False)).exists():
            acc_description = AccountingDataDesc.objects.filter(Q(account_assign_value__in=attr_value_list) &
                                                                Q(account_assign_cat=account_assign_cat) &
                                                                Q(language_id=global_variables.GLOBAL_USER_LANGUAGE) &
                                                                Q(company_id=company_code) &
                                                                Q(client=global_variables.GLOBAL_CLIENT) &
                                                                Q(del_ind=False)).values()
        elif AccountingDataDesc.objects.filter(Q(account_assign_value__in=attr_value_list) &
                                               Q(account_assign_cat=account_assign_cat) &
                                               Q(language_id=CONST_DEFAULT_LANGUAGE) &
                                               Q(company_id=company_code) &
                                               Q(client=global_variables.GLOBAL_CLIENT) &
                                               Q(del_ind=False)).exists():
            acc_description = AccountingDataDesc.objects.filter(Q(account_assign_value__in=attr_value_list) &
                                                                Q(account_assign_cat=account_assign_cat) &
                                                                Q(language_id=CONST_DEFAULT_LANGUAGE) &
                                                                Q(company_id=company_code) &
                                                                Q(client=global_variables.GLOBAL_CLIENT) &
                                                                Q(del_ind=False)).values()
        return acc_description

    @staticmethod
    def get_acc_asg_cat_value_desc(attr_value, company_code, account_assign_cat, language_id):
        """

        """
        acc_description = []
        if AccountingDataDesc.objects.filter(Q(account_assign_value=attr_value) &
                                             Q(account_assign_cat=account_assign_cat) &
                                             Q(language_id=language_id) &
                                             Q(company_id=company_code) &
                                             Q(client=global_variables.GLOBAL_CLIENT) &
                                             Q(del_ind=False)).exists():
            acc_description = AccountingDataDesc.objects.filter(Q(account_assign_value=attr_value) &
                                                                Q(account_assign_cat=account_assign_cat) &
                                                                Q(language_id=language_id) &
                                                                Q(company_id=company_code) &
                                                                Q(client=global_variables.GLOBAL_CLIENT) &
                                                                Q(del_ind=False)).values()
        elif AccountingDataDesc.objects.filter(Q(account_assign_value=attr_value) &
                                               Q(account_assign_cat=account_assign_cat) &
                                               Q(language_id=CONST_DEFAULT_LANGUAGE) &
                                               Q(company_id=company_code) &
                                               Q(client=global_variables.GLOBAL_CLIENT) &
                                               Q(del_ind=False)).exists():
            acc_description = AccountingDataDesc.objects.filter(Q(account_assign_value=attr_value) &
                                                                Q(account_assign_cat=account_assign_cat) &
                                                                Q(language_id=CONST_DEFAULT_LANGUAGE) &
                                                                Q(company_id=company_code) &
                                                                Q(client=global_variables.GLOBAL_CLIENT) &
                                                                Q(del_ind=False)).values()
        return acc_description

    @staticmethod
    def get_acc_value_description(client, attr_value_list):
        """
        get account assignment category description
        :param attr_value_list:
        :return:
        """
        cc_value = []
        if AccountingDataDesc.objects.filter(Q(account_assign_value__in=attr_value_list) &
                                             Q(client=client) & Q(del_ind=False)).exists():
            cc_value = AccountingDataDesc.objects.filter(Q(account_assign_value__in=attr_value_list) &
                                                         Q(client=client) & Q(del_ind=False)).values()
        return cc_value

    @staticmethod
    def append_acc_val_desc(acc_val_desc, acc_default_value):
        """

        :param acc_val_desc:
        :param acc_cat_default_value:
        :return:
        """
        attr_val = []
        attr_desc = []
        acc_append_default_val_desc = []
        acc_append_val_desc = []
        if acc_val_desc:
            for value_desc in acc_val_desc:
                if acc_default_value:
                    if acc_default_value == value_desc['account_assign_value']:
                        acc_append_default_val_desc = concatenate_str(value_desc['account_assign_value'],
                                                                      value_desc['description'])
                attr_val.append(value_desc['account_assign_value'])
                attr_desc.append(value_desc['description'])
            acc_append_val_desc = concatenate_array_str(attr_val, attr_desc)
            if acc_append_default_val_desc:
                acc_append_val_desc = remove_insert(acc_append_val_desc, acc_append_default_val_desc)
        return acc_append_val_desc, acc_append_default_val_desc

    @staticmethod
    def append_acc_val_desc_if_exists(acc_val_desc, acc_default_value, acc_value_list):
        acc_append_val_desc = []
        acc_append_default_val_desc = None
        for acc_value in acc_value_list:
            acc_value_detail = dictionary_check_get_value_based_for_key(acc_val_desc, 'account_assign_value', acc_value)
            if acc_value_detail:
                concate_val_desc = concatenate_str(acc_value_detail['account_assign_value'],
                                                   acc_value_detail['description'])
                acc_append_val_desc.append(concate_val_desc)
            else:
                acc_append_val_desc.append(acc_value)
        if acc_default_value:
            acc_default_value_detail = dictionary_check_get_value_based_for_key(acc_val_desc,
                                                                                'account_assign_value',
                                                                                acc_default_value)
            if acc_default_value_detail:
                acc_append_default_val_desc = concatenate_str(acc_default_value_detail['account_assign_value'],
                                                              acc_default_value_detail['description'])
            else:
                acc_append_default_val_desc = acc_default_value
        if acc_append_default_val_desc:
            acc_append_val_desc = remove_insert(acc_append_val_desc, acc_append_default_val_desc)
        return acc_append_val_desc, acc_append_default_val_desc

    @staticmethod
    def append_acc_desc(acc_val_desc):
        """

        :param acc_val_desc:
        :return:
        """

        append_val_desc = []
        if acc_val_desc:
            for value_desc in acc_val_desc:
                myDict = {}
                myDict["account_assign_cat"] = value_desc['account_assign_cat_id']
                myDict["account_assign_value"] = value_desc['account_assign_value']
                desc = concatenate_str(value_desc['account_assign_value'], value_desc['description'])
                myDict["append_val"] = desc
                append_val_desc.append(myDict)

        return append_val_desc

    @staticmethod
    def append_gl_account_value_desc(gl_acc_num, default_company_code, language_id):
        """

        """
        gl_acc_desc = AccountingDataDesc.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                                        company_id=default_company_code,
                                                        account_assign_value=gl_acc_num,
                                                        account_assign_cat=CONST_GLACC,
                                                        language_id=language_id).values('account_assign_value',
                                                                                        'description')

        if gl_acc_desc:
            for gl_desc in gl_acc_desc:
                gl_acc_detail = concatenate_str(gl_desc['account_assign_value'],
                                                gl_desc['description'])
        else:
            gl_acc_detail = gl_acc_num
        return gl_acc_detail

    @staticmethod
    def get_acc_values_and_desc_append_list(object_id_list, attribute_id, company_code, account_assignment_cat):
        """

        """
        acc_value_list = OrgAttributeValues.get_user_attr_value_list_by_attr_id(object_id_list, attribute_id)
        acc_value_desc = ACCValueDesc.get_acc_value_desc(acc_value_list, company_code, account_assignment_cat)
        append_acc_value_desc = append_description_atrr_value_exists(acc_value_desc,
                                                                     acc_value_list,
                                                                     'account_assign_value',
                                                                     'description')[0]
        return append_acc_value_desc

    @staticmethod
    def get_acc_default_values_and_desc_append_list(object_id_list, attribute_id, company_code, account_assignment_cat):
        """

        """
        append_acc_value_desc = ''
        acc_value_desc_list, acc_value_default_desc = OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(
            object_id_list, attribute_id)
        if acc_value_default_desc:
            acc_value_desc = ACCValueDesc.get_acc_value_desc([acc_value_default_desc], company_code,
                                                             account_assignment_cat)
            append_acc_value_desc = append_description_atrr_value_exists(acc_value_desc,
                                                                         [acc_value_default_desc],
                                                                         'account_assign_value',
                                                                         'description')[0]

        return append_acc_value_desc


def get_gl_account_value(client, total_value, cc, account_assign_cat):
    """
    :param client:
    :param total_value:
    :param cc:
    :param account_assign_cat:
    :return:
    """
    acc_val = AccountAssignmentCategory.objects.filter(account_assign_cat__in=account_assign_cat)
    available_gl_account = []
    gl_account_number = DetermineGLAccount.objects.filter(client=client, prod_cat_id='ALL',
                                                          account_assign_cat__in=acc_val,
                                                          company_id__in=cc, del_ind=False)

    for gl_numbers in gl_account_number:
        gl_acc_dic = {}
        if int(total_value) in range(int(gl_numbers.from_value), int(gl_numbers.to_value)):
            gl_acc_dic['gl_account'] = gl_numbers.gl_account
            gl_acc_dic['account_assign_cat'] = gl_numbers.account_assign_cat_id
            available_gl_account.append(gl_acc_dic)

    default_gl_acc_num = DetermineGLAccount.objects.filter(client=client, prod_cat_id='ALL',
                                                           account_assign_cat__in=acc_val,
                                                           gl_acc_default=True, company_id__in=cc, del_ind=False)

    default_gl_value = ''
    for data in default_gl_acc_num:
        if total_value in range(int(data.from_value), int(data.to_value)):
            default_gl_value = data.gl_account

    return default_gl_value, available_gl_account


def remove_insert(value_list, remove_val):
    """

    :param value_list:
    :param remove_val:
    :return:
    """
    value_list.remove(str(remove_val))
    value_list.insert(0, remove_val)
    return value_list
