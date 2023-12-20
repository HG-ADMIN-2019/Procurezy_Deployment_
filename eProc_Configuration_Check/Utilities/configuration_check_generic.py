from django.db.models.query_utils import Q

from eProc_Basic.Utilities.functions.date_format_as_db import convert_date_to_str
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models.application_data import *
from eProc_Configuration.models.basic_data import *
from eProc_Configuration.models.development_data import *
from eProc_Configuration.models.master_data import *
from eProc_Registration.models import UserData

django_query_instance = DjangoQueries()


def get_check_message(message_count_dic):
    db_count_message = get_message_desc('MSG193')[1] + str(message_count_dic['db_count'])
    file_count_message = get_message_desc('MSG194')[1] + str(message_count_dic['file_count'])
    delete_count_message = get_message_desc('MSG197')[1] + str(message_count_dic['delete_count'])
    invalid_count_message = get_message_desc('MSG199')[1] + str(message_count_dic['invalid_count'])
    duplicate_count_message = get_message_desc('MSG198')[1] + str(message_count_dic['duplicate_count'])
    update_count_message = get_message_desc('MSG196')[1] + str(message_count_dic['update_count'])
    insert_count_message = get_message_desc('MSG195')[1] + str(message_count_dic['insert_count'])
    dependent_count_message = get_message_desc('MSG200')[1] + str(message_count_dic['dependent_count'])
    message = [db_count_message, file_count_message, insert_count_message, update_count_message,
               duplicate_count_message, delete_count_message, invalid_count_message, dependent_count_message]
    return message


def check_unspsc_category_desc_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(UnspscCategoriesCustDesc,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for unspsc_desc in ui_data:
        # dependent check
        if django_query_instance.django_existence_check(UnspscCategories,
                                                        {'del_ind': False,
                                                         'prod_cat_id': unspsc_desc['prod_cat_id']}):
            # check for deletion of record
            if unspsc_desc['del_ind'] in ['1', True]:

                if status == 'SAVE':
                    if django_query_instance.django_existence_check(UnspscCategoriesCustDesc,
                                                                    {'prod_cat_id': unspsc_desc[
                                                                        'prod_cat_id'],
                                                                     'client': global_variables.GLOBAL_CLIENT,
                                                                     'language_id': unspsc_desc['language_id']}):
                        delete_count = delete_count + 1
                        valid_data_list.append(unspsc_desc)
                else:
                    if django_query_instance.django_existence_check(UnspscCategoriesCustDesc,
                                                                    {'del_ind': False,
                                                                     'client': global_variables.GLOBAL_CLIENT,
                                                                     'prod_cat_id': unspsc_desc['prod_cat_id'],
                                                                     'language_id': unspsc_desc['language_id']}
                                                                    ):
                        delete_count = delete_count + 1
                        valid_data_list.append(unspsc_desc)
                    else:
                        # if del is set but record is not found in db then it is consider as invalid count
                        invalid_count = invalid_count + 1
                        valid_data_list.append(unspsc_desc)
            else:
                # duplicate check
                if django_query_instance.django_existence_check(UnspscCategoriesCustDesc,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'prod_cat_id': unspsc_desc['prod_cat_id'],
                                                                 'category_desc': unspsc_desc['description'],
                                                                 'language_id': unspsc_desc['language_id']}):
                    duplicate_count = duplicate_count + 1
                # update check
                elif django_query_instance.django_existence_check(UnspscCategoriesCustDesc,
                                                                  {'del_ind': False,
                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                   'prod_cat_id': unspsc_desc['prod_cat_id'],
                                                                   'language_id': unspsc_desc['language_id']}):
                    update_count = update_count + 1
                    valid_data_list.append(unspsc_desc)
                else:
                    # insert check
                    insert_count = insert_count + 1
                    valid_data_list.append(unspsc_desc)
        else:
            dependent_count = dependent_count + 1

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_unspsc_category_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(UnspscCategoriesCust,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for unspsc_desc in ui_data:
        if django_query_instance.django_existence_check(UnspscCategoriesCustDesc,
                                                        {'del_ind': False,
                                                         'prod_cat_id': unspsc_desc['prod_cat_id']}):
            if unspsc_desc['del_ind'] in ['1', True]:
                if status == 'SAVE':
                    if django_query_instance.django_existence_check(UnspscCategoriesCust,
                                                                    {'prod_cat_id': unspsc_desc[
                                                                        'prod_cat_id'],
                                                                     'client': global_variables.GLOBAL_CLIENT}):
                        delete_count = delete_count + 1
                        valid_data_list.append(unspsc_desc)
                else:
                    if django_query_instance.django_existence_check(UnspscCategoriesCust,
                                                                    {'del_ind': False,
                                                                     'prod_cat_id': unspsc_desc[
                                                                         'prod_cat_id'],
                                                                     'client': global_variables.GLOBAL_CLIENT}):
                        delete_count = delete_count + 1
                        valid_data_list.append(unspsc_desc)
                    else:
                        invalid_count = invalid_count + 1
                        valid_data_list.append(unspsc_desc)
            else:
                if django_query_instance.django_existence_check(UnspscCategoriesCust,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'prod_cat_id': unspsc_desc['prod_cat_id']
                                                                 }):
                    duplicate_count = duplicate_count + 1
                elif django_query_instance.django_existence_check(UnspscCategoriesCust,
                                                                  {'del_ind': False,
                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                   'prod_cat_id': unspsc_desc['prod_cat_id']
                                                                   }):
                    update_count = update_count + 1
                    valid_data_list.append(unspsc_desc)
                else:
                    insert_count = insert_count + 1
                    valid_data_list.append(unspsc_desc)
        else:
            dependent_count = dependent_count + 1

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_acc_assign_desc_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(AccountingDataDesc,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for acc_desc in ui_data:
        # check for deletion of record
        if acc_desc['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(AccountingDataDesc,
                                                                {'client': global_variables.GLOBAL_CLIENT,
                                                                 'account_assign_value': acc_desc[
                                                                     'account_assign_value'],
                                                                 'company_id': acc_desc['company_id'],
                                                                 'account_assign_cat': acc_desc[
                                                                     'account_assign_cat'],
                                                                 'language_id': acc_desc['language_id']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(acc_desc)
            else:
                if django_query_instance.django_existence_check(AccountingDataDesc,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'account_assign_value': acc_desc[
                                                                     'account_assign_value'],
                                                                 'company_id': acc_desc['company_id'],
                                                                 'account_assign_cat': acc_desc[
                                                                     'account_assign_cat'],
                                                                 'language_id': acc_desc['language_id']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(acc_desc)
                else:
                    # if del is set but record is not found in db then it is consider as invalid count
                    invalid_count = invalid_count + 1
                    valid_data_list.append(acc_desc)
        else:
            # duplicate check
            if django_query_instance.django_existence_check(AccountingDataDesc,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'account_assign_value': acc_desc[
                                                                 'account_assign_value'],
                                                             'description': acc_desc['description'],
                                                             'company_id': acc_desc['company_id'],
                                                             'account_assign_cat': acc_desc['account_assign_cat'],
                                                             'language_id': acc_desc['language_id']}):
                duplicate_count = duplicate_count + 1
            # update check
            elif django_query_instance.django_existence_check(AccountingDataDesc,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'account_assign_value': acc_desc[
                                                                   'account_assign_value'],
                                                               'company_id': acc_desc['company_id'],
                                                               'account_assign_cat': acc_desc[
                                                                   'account_assign_cat'],
                                                               'language_id': acc_desc['language_id']}):
                update_count = update_count + 1
                valid_data_list.append(acc_desc)
            else:
                # insert check
                insert_count = insert_count + 1
                valid_data_list.append(acc_desc)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_acc_assign_values_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(AccountingData,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for acc_value in ui_data:
        if acc_value['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(AccountingData,
                                                                {'client': global_variables.GLOBAL_CLIENT,
                                                                 'account_assign_value': acc_value[
                                                                     'account_assign_value'],
                                                                 'company_id': acc_value['company_id'],
                                                                 'account_assign_cat': acc_value['account_assign_cat'],
                                                                 }):
                    delete_count = delete_count + 1
                    valid_data_list.append(acc_value)
            else:
                if django_query_instance.django_existence_check(AccountingData,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'account_assign_value': acc_value[
                                                                     'account_assign_value'],
                                                                 'company_id': acc_value['company_id'],
                                                                 'account_assign_cat': acc_value['account_assign_cat'],
                                                                 }):
                    delete_count = delete_count + 1
                    valid_data_list.append(acc_value)
                else:
                    invalid_count = invalid_count + 1
        else:
            from_val = datetime.strptime(acc_value['valid_from'], "%d-%m-%Y")
            to_val = datetime.strptime(acc_value['valid_to'], "%d-%m-%Y")
            if django_query_instance.django_existence_check(AccountingData,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'account_assign_value': acc_value['account_assign_value'],
                                                             'company_id': acc_value['company_id'],
                                                             'account_assign_cat': acc_value['account_assign_cat'],
                                                             'valid_from': from_val,
                                                             'valid_to': to_val
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(AccountingData,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'account_assign_value': acc_value[
                                                                   'account_assign_value'],
                                                               'company_id': acc_value['company_id'],
                                                               'account_assign_cat': acc_value['account_assign_cat'],
                                                               }):
                update_count = update_count + 1
                valid_data_list.append(acc_value)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(acc_value)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_company_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(OrgCompanies,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for com_value in ui_data:
        if com_value['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(OrgCompanies,
                                                                {'company_id': com_value[
                                                                    'company_id'],
                                                                 'client': global_variables.GLOBAL_CLIENT}):
                    delete_count = delete_count + 1
                    valid_data_list.append(com_value)
            else:
                if django_query_instance.django_existence_check(OrgCompanies,
                                                                {'del_ind': False,
                                                                 'company_id': com_value[
                                                                     'company_id'],
                                                                 'client': global_variables.GLOBAL_CLIENT}):
                    delete_count = delete_count + 1
                    valid_data_list.append(com_value)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(OrgCompanies,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'company_id': com_value['company_id'],
                                                             'name1': com_value['name1'],
                                                             'name2': com_value['name2']
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(OrgCompanies,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'company_id': com_value['company_id']
                                                               }):
                update_count = update_count + 1
                valid_data_list.append(com_value)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(com_value)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_user_role_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(UserRoles,
                                                               {'del_ind': False
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for roles_detail in ui_data:
        if roles_detail['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(UserRoles,
                                                                {'role': roles_detail[
                                                                    'role'],
                                                                 }):
                    delete_count = delete_count + 1
                    valid_data_list.append(roles_detail)
            else:
                if django_query_instance.django_existence_check(UserRoles,
                                                                {'del_ind': False,
                                                                 'role': roles_detail['role']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(roles_detail)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(UserRoles,
                                                            {'del_ind': False,
                                                             'role': roles_detail['role'],
                                                             'role_desc': roles_detail['role_desc'],
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(UserRoles,
                                                              {'del_ind': False,
                                                               'role': roles_detail['role']
                                                               }):
                update_count = update_count + 1
                valid_data_list.append(roles_detail)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(roles_detail)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_authorization_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(Authorization,
                                                               {'del_ind': False
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for auth_detail in ui_data:
        if auth_detail['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(Authorization,
                                                                {'auth_obj_grp': auth_detail['auth_obj_grp'],
                                                                 'client': global_variables.GLOBAL_CLIENT
                                                                 }):
                    delete_count = delete_count + 1
                    valid_data_list.append(auth_detail)
            else:
                if django_query_instance.django_existence_check(Authorization,
                                                                {'del_ind': False,
                                                                 'auth_obj_grp': auth_detail['auth_obj_grp'],
                                                                 'client': global_variables.GLOBAL_CLIENT}):
                    delete_count = delete_count + 1
                    valid_data_list.append(auth_detail)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(Authorization,
                                                            {'del_ind': False,
                                                             'auth_obj_grp': auth_detail['auth_obj_grp'],
                                                             'role': auth_detail['role'],
                                                             'client': global_variables.GLOBAL_CLIENT
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(Authorization,
                                                              {'del_ind': False,
                                                               'auth_obj_grp': auth_detail['auth_obj_grp'],
                                                               'client': global_variables.GLOBAL_CLIENT
                                                               }):
                update_count = update_count + 1
                valid_data_list.append(auth_detail)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(auth_detail)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_authorization_grp_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(AuthorizationGroup,
                                                               {'del_ind': False,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for auth_group_detail in ui_data:
        if auth_group_detail['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(AuthorizationGroup,
                                                                {'auth_obj_grp': auth_group_detail['auth_obj_grp'],
                                                                 'auth_obj_id': auth_group_detail['auth_obj_id']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(auth_group_detail)
            else:
                if django_query_instance.django_existence_check(AuthorizationGroup,
                                                                {'del_ind': False,
                                                                 'auth_obj_grp': auth_group_detail['auth_obj_grp'],
                                                                 'auth_obj_id': auth_group_detail['auth_obj_id']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(auth_group_detail)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(AuthorizationGroup,
                                                            {'del_ind': False,
                                                             'auth_obj_grp': auth_group_detail['auth_obj_grp'],
                                                             'auth_grp_desc': auth_group_detail['auth_grp_desc'],
                                                             'auth_level': auth_group_detail['auth_level'],
                                                             'auth_obj_id': auth_group_detail['auth_obj_id'],
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(AuthorizationGroup,
                                                              {'del_ind': False,
                                                               'auth_obj_grp': auth_group_detail['auth_obj_grp'],
                                                               'auth_obj_id': auth_group_detail['auth_obj_id']
                                                               }):
                update_count = update_count + 1
                valid_data_list.append(auth_group_detail)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(auth_group_detail)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_authorization_object_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(AuthorizationObject,
                                                               {'del_ind': False
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for authobj_detail in ui_data:
        if authobj_detail['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(AuthorizationObject,
                                                                {'auth_obj_id': authobj_detail[
                                                                    'auth_obj_id']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(authobj_detail)
            else:
                if django_query_instance.django_existence_check(AuthorizationObject,
                                                                {'del_ind': False,
                                                                 'auth_obj_id': authobj_detail[
                                                                     'auth_obj_id']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(authobj_detail)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(AuthorizationObject,
                                                            {'del_ind': False,
                                                             'auth_obj_id': authobj_detail['auth_obj_id'],
                                                             'auth_level_ID': authobj_detail['auth_level_ID'],
                                                             'auth_level': authobj_detail['auth_level'],
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(AuthorizationObject,
                                                              {'del_ind': False,
                                                               'auth_obj_id': authobj_detail['auth_obj_id']
                                                               }):
                update_count = update_count + 1
                valid_data_list.append(authobj_detail)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(authobj_detail)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_nodetype_config_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(OrgModelNodetypeConfig,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for orgattlevel_detail in ui_data:
        if orgattlevel_detail['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(OrgModelNodetypeConfig,
                                                                {'node_type': orgattlevel_detail['node_type'],
                                                                 'node_values': orgattlevel_detail['node_values'],
                                                                 'org_model_types': 'ORG_ATTRIBUTES',
                                                                 'client': global_variables.GLOBAL_CLIENT}):
                    delete_count = delete_count + 1
                    valid_data_list.append(orgattlevel_detail)
            else:
                if django_query_instance.django_existence_check(OrgModelNodetypeConfig,
                                                                {'del_ind': False,
                                                                 'node_type': orgattlevel_detail['node_type'],
                                                                 'node_values': orgattlevel_detail['node_values'],
                                                                 'org_model_types': 'ORG_ATTRIBUTES',
                                                                 'client': global_variables.GLOBAL_CLIENT}):
                    delete_count = delete_count + 1
                    valid_data_list.append(orgattlevel_detail)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(OrgNodeTypes,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'node_type': orgattlevel_detail['node_type']}) \
                    or django_query_instance.django_existence_check(OrgAttributes,
                                                                    {'attribute_id': orgattlevel_detail[
                                                                        'node_values']}):
                if django_query_instance.django_existence_check(OrgModelNodetypeConfig,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'node_type': orgattlevel_detail['node_type'],
                                                                 'node_values': orgattlevel_detail['node_values'],
                                                                 'org_model_types': 'ORG_ATTRIBUTES',
                                                                 }):
                    duplicate_count = duplicate_count + 1
                elif django_query_instance.django_existence_check(OrgModelNodetypeConfig,
                                                                  {'del_ind': False,
                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                   'node_type': orgattlevel_detail['node_type'],
                                                                   'node_values': orgattlevel_detail['node_values'],
                                                                   'org_model_types': 'ORG_ATTRIBUTES',
                                                                   }):
                    update_count = update_count + 1
                    valid_data_list.append(orgattlevel_detail)
                else:
                    insert_count = insert_count + 1
                    valid_data_list.append(orgattlevel_detail)
            else:
                invalid_count = invalid_count + 1

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_orgattributes_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(OrgAttributes,
                                                               {'del_ind': False
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for org_attr in ui_data:
        if org_attr['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(OrgAttributes,
                                                                {'attribute_id': org_attr[
                                                                    'attribute_id']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(org_attr)
            else:
                if django_query_instance.django_existence_check(OrgAttributes,
                                                                {'del_ind': False,
                                                                 'attribute_id': org_attr[
                                                                     'attribute_id']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(org_attr)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(OrgAttributes,
                                                            {'del_ind': False,
                                                             'attribute_id': org_attr['attribute_id'],
                                                             'attribute_name': org_attr['attribute_name'],
                                                             'range_indicator': org_attr['range_indicator'],
                                                             'multiple_value': org_attr['multiple_value'],
                                                             'allow_defaults': org_attr['allow_defaults'],
                                                             'inherit_values': org_attr['inherit_values'],
                                                             'maximum_length': org_attr['maximum_length'],
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(OrgAttributes,
                                                              {'del_ind': False,
                                                               'attribute_id': org_attr['attribute_id']
                                                               }):
                update_count = update_count + 1
                valid_data_list.append(org_attr)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(org_attr)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_node_type_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(OrgNodeTypes,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for node_type in ui_data:
        if node_type['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(OrgNodeTypes,
                                                                {'node_type': node_type[
                                                                    'node_type'],
                                                                 'client': global_variables.GLOBAL_CLIENT}):
                    delete_count = delete_count + 1
                    valid_data_list.append(node_type)
            else:
                if django_query_instance.django_existence_check(OrgNodeTypes,
                                                                {'del_ind': False,
                                                                 'node_type': node_type[
                                                                     'node_type'],
                                                                 'client': global_variables.GLOBAL_CLIENT}):
                    delete_count = delete_count + 1
                    valid_data_list.append(node_type)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(OrgNodeTypes,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'node_type': node_type['node_type'],
                                                             'description': node_type['description'],
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(OrgNodeTypes,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'node_type': node_type['node_type']
                                                               }):
                update_count = update_count + 1
                valid_data_list.append(node_type)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(node_type)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_org_client_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(OrgClients,
                                                               {'del_ind': False
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for client in ui_data:
        if client['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(OrgClients,
                                                                {'client': client['client']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(client)
            else:
                if django_query_instance.django_existence_check(OrgClients,
                                                                {'del_ind': False,
                                                                 'client': client['client']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(client)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(OrgClients,
                                                            {'del_ind': False,
                                                             'client': client['client'],
                                                             'description': client['description'],
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(OrgClients,
                                                              {'del_ind': False,
                                                               'client': client['client']}):
                update_count = update_count + 1
                valid_data_list.append(client)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(client)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_document_type_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(DocumentType,
                                                               {'del_ind': False
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for document_type in ui_data:
        if document_type['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(DocumentType,
                                                                {'document_type': document_type['document_type']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(document_type)
            else:
                if django_query_instance.django_existence_check(DocumentType,
                                                                {'del_ind': False,
                                                                 'document_type': document_type['document_type']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(document_type)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(DocumentType,
                                                            {'del_ind': False,
                                                             'document_type': document_type['document_type'],
                                                             'document_type_desc': document_type['document_type_desc'],
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(DocumentType,
                                                              {'del_ind': False,
                                                               'document_type': document_type['document_type']}):
                update_count = update_count + 1
                valid_data_list.append(document_type)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(document_type)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_acc_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(AccountAssignmentCategory,
                                                               {'del_ind': False
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for acc_data in ui_data:
        if acc_data['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(AccountAssignmentCategory,
                                                                {'account_assign_cat': acc_data['account_assign_cat']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(acc_data)
            else:
                if django_query_instance.django_existence_check(AccountAssignmentCategory,
                                                                {'del_ind': False,
                                                                 'account_assign_cat': acc_data['account_assign_cat']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(acc_data)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(AccountAssignmentCategory,
                                                            {'del_ind': False,
                                                             'account_assign_cat': acc_data['account_assign_cat'],
                                                             'description': acc_data['description'],
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(AccountAssignmentCategory,
                                                              {'del_ind': False,
                                                               'account_assign_cat': acc_data['account_assign_cat']}):
                update_count = update_count + 1
                valid_data_list.append(acc_data)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(acc_data)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_po_split_type_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(PoSplitType,
                                                               {'del_ind': False
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for po_split_type in ui_data:
        if po_split_type['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(PoSplitType,
                                                                {'po_split_type': po_split_type['po_split_type']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(po_split_type)
            else:
                if django_query_instance.django_existence_check(PoSplitType,
                                                                {'del_ind': False,
                                                                 'po_split_type': po_split_type['po_split_type']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(po_split_type)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(PoSplitType,
                                                            {'del_ind': False,
                                                             'po_split_type': po_split_type['po_split_type'],
                                                             'po_split_type_desc': po_split_type['po_split_type_desc'],
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(PoSplitType,
                                                              {'del_ind': False,
                                                               'po_split_type': po_split_type['po_split_type']}):
                update_count = update_count + 1
                valid_data_list.append(po_split_type)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(po_split_type)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_calendar_config_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(CalenderConfig,
                                                               {'del_ind': False
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for calendar_conf in ui_data:
        if calendar_conf['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(CalenderConfig,
                                                                {'calender_id': calendar_conf['calender_id'],
                                                                 'client': global_variables.GLOBAL_CLIENT}):
                    delete_count = delete_count + 1
                    valid_data_list.append(calendar_conf)
        else:
            if django_query_instance.django_existence_check(CalenderConfig,
                                                            {'del_ind': False,
                                                             'calender_id': calendar_conf['calender_id'],
                                                             'client': global_variables.GLOBAL_CLIENT}):
                update_count = update_count + 1
                valid_data_list.append(calendar_conf)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(calendar_conf)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_message_id_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(MessagesId,
                                                               {'del_ind': False
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for msg_id in ui_data:
        if msg_id['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(MessagesId,
                                                                {'messages_id': msg_id['message_id'],
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'messages_type': msg_id['message_type']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(msg_id)
        else:
            if django_query_instance.django_existence_check(MessagesId,
                                                            {'del_ind': False,
                                                             'messages_id': msg_id['message_id'],
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'messages_type': msg_id['message_type'],
                                                             }):
                update_count = update_count + 1
                valid_data_list.append(msg_id)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(msg_id)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_po_split_creteria_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(PoSplitCriteria,
                                                               {'del_ind': False
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for po_split in ui_data:
        if po_split['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(PoSplitCriteria,
                                                                {'po_split_type': po_split['po_split_type'],
                                                                 'company_code_id':
                                                                     po_split['company_code_id'],
                                                                 'client': global_variables.GLOBAL_CLIENT
                                                                 }):
                    delete_count = delete_count + 1
                    valid_data_list.append(po_split)
        else:
            if django_query_instance.django_existence_check(PoSplitCriteria,
                                                            {'po_split_type': po_split['po_split_type'],
                                                             'company_code_id':
                                                                 po_split['company_code_id'],
                                                             'client': global_variables.GLOBAL_CLIENT
                                                             }):
                update_count = update_count + 1
                valid_data_list.append(po_split)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(po_split)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_purchase_control_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(PurchaseControl,
                                                               {'del_ind': False
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for po_split in ui_data:
        if po_split['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(PurchaseControl,
                                                                {'call_off': po_split['call_off'],
                                                                 'company_code_id':
                                                                     po_split['company_code_id'],
                                                                 'client': global_variables.GLOBAL_CLIENT
                                                                 }):
                    delete_count = delete_count + 1
                    valid_data_list.append(po_split)
        else:
            if django_query_instance.django_existence_check(PurchaseControl,
                                                            {'call_off': po_split['call_off'],
                                                             'company_code_id':
                                                                 po_split['company_code_id'],
                                                             'client': global_variables.GLOBAL_CLIENT
                                                             }):
                update_count = update_count + 1
                valid_data_list.append(po_split)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(po_split)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_source_rule_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(SourcingRule,
                                                               {'del_ind': False
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for sr_generic in ui_data:
        if sr_generic['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(SourcingRule,
                                                                {'prod_cat_id_from': sr_generic['prod_cat_id_from'],
                                                                 'prod_cat_id_to': sr_generic['prod_cat_id_to'],
                                                                 'company_id': sr_generic['company_id'],
                                                                 'call_off': sr_generic['call_off'],
                                                                 'rule_type': sr_generic['rule_type'],
                                                                 'sourcing_flag': sr_generic['sourcing_flag'],
                                                                 'client': global_variables.GLOBAL_CLIENT
                                                                 }):
                    delete_count = delete_count + 1
                    valid_data_list.append(sr_generic)
        else:
            if django_query_instance.django_existence_check(SourcingRule,
                                                            {'prod_cat_id_from': sr_generic['prod_cat_id_from'],
                                                             'prod_cat_id_to': sr_generic['prod_cat_id_to'],
                                                             'company_id': sr_generic['company_id'],
                                                             'call_off': sr_generic['call_off'],
                                                             'rule_type': sr_generic['rule_type'],
                                                             'sourcing_flag': sr_generic['sourcing_flag'],
                                                             'client': global_variables.GLOBAL_CLIENT
                                                             }):
                update_count = update_count + 1
                valid_data_list.append(sr_generic)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(sr_generic)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_source_mapping_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(SourcingMapping,
                                                               {'del_ind': False
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for sr_specific in ui_data:
        if sr_specific['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(SourcingMapping,
                                                                {'prod_cat_id': sr_specific['prod_cat_id'],
                                                                 'product_id': sr_specific['product_id'],
                                                                 'company_id': sr_specific['company_id'],
                                                                 'rule_type': sr_specific['rule_type'],
                                                                 'client': global_variables.GLOBAL_CLIENT
                                                                 }):
                    delete_count = delete_count + 1
                    valid_data_list.append(sr_specific)
        else:
            if django_query_instance.django_existence_check(SourcingMapping,
                                                            {'prod_cat_id': sr_specific['prod_cat_id'],
                                                             'product_id': sr_specific['product_id'],
                                                             'company_id': sr_specific['company_id'],
                                                             'rule_type': sr_specific['rule_type'],
                                                             'client': global_variables.GLOBAL_CLIENT
                                                             }):
                update_count = update_count + 1
                valid_data_list.append(sr_specific)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(sr_specific)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_message_id_desc_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(MessagesIdDesc,
                                                               {'del_ind': False
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for msg_id in ui_data:
        if msg_id['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(MessagesIdDesc,
                                                                {'messages_id': msg_id['messages_id'],
                                                                 'language_id': msg_id['language_id'],
                                                                 'client': global_variables.GLOBAL_CLIENT}):
                    delete_count = delete_count + 1
                    valid_data_list.append(msg_id)
        else:
            if django_query_instance.django_existence_check(MessagesIdDesc,
                                                            {'messages_id': msg_id['messages_id'],
                                                             'language_id': msg_id['language_id'],
                                                             'client': global_variables.GLOBAL_CLIENT}):
                update_count = update_count + 1
                valid_data_list.append(msg_id)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(msg_id)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_email_settings_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(EmailContents,
                                                               {'del_ind': False
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for email_data in ui_data:
        if email_data['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(EmailContents,
                                                                {'object_type': email_data['email_type'],
                                                                 'language_id': email_data['language_id'],
                                                                 'client': global_variables.GLOBAL_CLIENT
                                                                 }):
                    delete_count = delete_count + 1
                    valid_data_list.append(email_data)
        else:
            if django_query_instance.django_existence_check(EmailContents,
                                                            {'object_type': email_data['email_type'],
                                                             'language_id': email_data['language_id'],
                                                             'client': global_variables.GLOBAL_CLIENT
                                                             }):
                update_count = update_count + 1
                valid_data_list.append(email_data)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(email_data)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_unspsc_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(UnspscCategories,
                                                               {'del_ind': False
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for prod_cat in ui_data:
        if prod_cat['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(UnspscCategories,
                                                                {'prod_cat_id': prod_cat['prod_cat_id']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(prod_cat)
            else:
                if django_query_instance.django_existence_check(UnspscCategories,
                                                                {'del_ind': False,
                                                                 'prod_cat_id': prod_cat['prod_cat_id']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(prod_cat)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(UnspscCategories,
                                                            {'del_ind': False,
                                                             'prod_cat_id': prod_cat['prod_cat_id'],
                                                             'prod_cat_desc': prod_cat['prod_cat_desc'],
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(UnspscCategories,
                                                              {'del_ind': False,
                                                               'prod_cat_id': prod_cat['prod_cat_id']}):
                update_count = update_count + 1
                valid_data_list.append(prod_cat)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(prod_cat)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_purchaseorg_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(OrgPorg,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for prorg_value in ui_data:
        if prorg_value['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(OrgPorg,
                                                                {'porg_id': prorg_value[
                                                                    'porg_id'],
                                                                 'client': global_variables.GLOBAL_CLIENT}):
                    delete_count = delete_count + 1
                    valid_data_list.append(prorg_value)
            else:
                if django_query_instance.django_existence_check(OrgPorg,
                                                                {'del_ind': False,
                                                                 'porg_id': prorg_value[
                                                                     'porg_id'],
                                                                 'client': global_variables.GLOBAL_CLIENT}):
                    delete_count = delete_count + 1
                    valid_data_list.append(prorg_value)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(OrgPorg,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'porg_id': prorg_value['porg_id'],
                                                             'description': prorg_value['description'],
                                                             }):

                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(OrgPorg,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'porg_id': prorg_value[
                                                                   'porg_id'],
                                                               }):

                update_count = update_count + 1
                valid_data_list.append(prorg_value)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(prorg_value)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_purchasegrp_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(OrgPGroup,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for purgrp_value in ui_data:
        if purgrp_value['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(OrgPGroup,
                                                                {'pgroup_id': purgrp_value[
                                                                    'pgroup_id'],
                                                                 'client': global_variables.GLOBAL_CLIENT}):
                    delete_count = delete_count + 1
                    valid_data_list.append(purgrp_value)
            else:
                if django_query_instance.django_existence_check(OrgPGroup,
                                                                {'del_ind': False,
                                                                 'pgroup_id': purgrp_value[
                                                                     'pgroup_id'],
                                                                 'client': global_variables.GLOBAL_CLIENT}):
                    delete_count = delete_count + 1
                    valid_data_list.append(purgrp_value)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(OrgPGroup,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'pgroup_id': purgrp_value['pgroup_id'],
                                                             'description': purgrp_value['description'],
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(OrgPGroup,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'pgroup_id': purgrp_value[
                                                                   'pgroup_id']
                                                               }):
                update_count = update_count + 1
                valid_data_list.append(purgrp_value)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(purgrp_value)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_approvaltype_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(ApproverType,
                                                               {'del_ind': False,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for app_typ in ui_data:
        if app_typ['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(ApproverType,
                                                                {'app_types': app_typ[
                                                                    'app_types']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(app_typ)
            else:
                if django_query_instance.django_existence_check(ApproverType,
                                                                {'del_ind': False,
                                                                 'app_types': app_typ[
                                                                     'app_types']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(app_typ)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(ApproverType,
                                                            {'del_ind': False,
                                                             'app_types': app_typ['app_types'],
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(ApproverType,
                                                              {'del_ind': False,
                                                               'app_types': app_typ[
                                                                   'app_types'],
                                                               }):
                update_count = update_count + 1
                valid_data_list.append(app_typ)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(app_typ)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_workflowschema_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(WorkflowSchema,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for workflw_schema in ui_data:
        if workflw_schema['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(WorkflowSchema,
                                                                {'app_types': workflw_schema[
                                                                    'app_types'],
                                                                 'company_id': workflw_schema['company_id'],
                                                                 'client': global_variables.GLOBAL_CLIENT}):
                    delete_count = delete_count + 1
                    valid_data_list.append(workflw_schema)
            else:
                if django_query_instance.django_existence_check(WorkflowSchema,
                                                                {'del_ind': False,
                                                                 'workflow_schema': workflw_schema[
                                                                     'workflow_schema'],
                                                                 'client': global_variables.GLOBAL_CLIENT}):
                    delete_count = delete_count + 1
                    valid_data_list.append(workflw_schema)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(WorkflowSchema,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'workflow_schema': workflw_schema['workflow_schema'],
                                                             'company_id': workflw_schema['company_id'],
                                                             'app_types': workflw_schema['app_types']
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(WorkflowSchema,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'workflow_schema': workflw_schema[
                                                                   'workflow_schema'],
                                                               'company_id': workflw_schema['company_id']
                                                               }):
                update_count = update_count + 1
                valid_data_list.append(workflw_schema)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(workflw_schema)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_spendlimit_value_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(SpendLimitValue,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for spend_limit_value in ui_data:
        if spend_limit_value['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(SpendLimitValue,
                                                                {'spend_code_id': spend_limit_value[
                                                                    'spend_code_id'],
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'company_id': spend_limit_value['company_id'],
                                                                 'currency_id': spend_limit_value['currency_id']
                                                                 }):
                    delete_count = delete_count + 1
                    valid_data_list.append(spend_limit_value)
            else:
                if django_query_instance.django_existence_check(SpendLimitValue,
                                                                {'del_ind': False,
                                                                 'spend_code_id': spend_limit_value[
                                                                     'spend_code_id'],
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'company_id': spend_limit_value['company_id'],
                                                                 'currency_id': spend_limit_value['currency_id']
                                                                 }):
                    delete_count = delete_count + 1
                    valid_data_list.append(spend_limit_value)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(SpendLimitValue,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'spend_code_id': spend_limit_value['spend_code_id'],
                                                             'upper_limit_value': spend_limit_value[
                                                                 'upper_limit_value'],
                                                             'company_id': spend_limit_value['company_id'],
                                                             'currency_id': spend_limit_value['currency_id']
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(SpendLimitValue,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'spend_code_id': spend_limit_value[
                                                                   'spend_code_id'],
                                                               'company_id': spend_limit_value['company_id'],
                                                               'currency_id': spend_limit_value['currency_id']
                                                               }):
                update_count = update_count + 1
                valid_data_list.append(spend_limit_value)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(spend_limit_value)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_spending_limit_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(SpendLimitId,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for spending_limit in ui_data:
        # dependent check
        if django_query_instance.django_existence_check(SpendLimitValue,
                                                        {'del_ind': False,
                                                         'client': global_variables.GLOBAL_CLIENT,
                                                         'spend_code_id': spending_limit['spend_code_id']
                                                         }):

            if spending_limit['del_ind'] in ['1', True]:
                if status == 'SAVE':
                    if django_query_instance.django_existence_check(SpendLimitId,
                                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                                     'spender_username': spending_limit[
                                                                         'spender_username'],
                                                                     'company_id': spending_limit['company_id']}):
                        delete_count = delete_count + 1
                        valid_data_list.append(spending_limit)
                else:
                    if django_query_instance.django_existence_check(SpendLimitId,
                                                                    {'del_ind': False,
                                                                     'client': global_variables.GLOBAL_CLIENT,
                                                                     'spender_username': spending_limit[
                                                                         'spender_username'],
                                                                     'company_id': spending_limit['company_id']}):
                        delete_count = delete_count + 1
                        valid_data_list.append(spending_limit)
                    else:
                        invalid_count = invalid_count + 1
            else:
                # duplicate check
                if django_query_instance.django_existence_check(SpendLimitId,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'spend_code_id': spending_limit['spend_code_id'],
                                                                 'spender_username': spending_limit['spender_username'],
                                                                 'company_id': spending_limit['company_id']
                                                                 }):
                    duplicate_count = duplicate_count + 1
                # update check
                elif django_query_instance.django_existence_check(SpendLimitId,
                                                                  {'del_ind': False,
                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                   'spender_username': spending_limit[
                                                                       'spender_username'],
                                                                   'company_id': spending_limit[
                                                                       'company_id']}):
                    update_count = update_count + 1
                    valid_data_list.append(spending_limit)
                else:
                    # insert check
                    insert_count = insert_count + 1
                    valid_data_list.append(spending_limit)
        else:
            print(spending_limit['spend_code_id'])
            dependent_count = dependent_count + 1

        print(spending_limit)
    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_approv_limit_value_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(ApproverLimitValue,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for approv_limit_value in ui_data:
        if approv_limit_value['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(ApproverLimitValue,
                                                                {'client': global_variables.GLOBAL_CLIENT,
                                                                 'app_code_id': approv_limit_value[
                                                                     'app_code_id'],
                                                                 'company_id': approv_limit_value['company_id'],
                                                                 'app_types': approv_limit_value['app_types'],
                                                                 'currency_id': approv_limit_value['currency_id']
                                                                 }):
                    delete_count = delete_count + 1
                    valid_data_list.append(approv_limit_value)
            else:
                if django_query_instance.django_existence_check(ApproverLimitValue,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'app_code_id': approv_limit_value[
                                                                     'app_code_id'],
                                                                 'company_id': approv_limit_value['company_id'],
                                                                 'app_types': approv_limit_value['app_types'],
                                                                 'currency_id': approv_limit_value['currency_id']
                                                                 }):
                    delete_count = delete_count + 1
                    valid_data_list.append(approv_limit_value)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(ApproverLimitValue,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'app_code_id': approv_limit_value['app_code_id'],
                                                             'company_id': approv_limit_value['company_id'],
                                                             'app_types': approv_limit_value['app_types'],
                                                             'upper_limit_value': approv_limit_value[
                                                                 'upper_limit_value'],
                                                             'currency_id': approv_limit_value['currency_id']
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(ApproverLimitValue,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'app_code_id': approv_limit_value[
                                                                   'app_code_id'],
                                                               'company_id': approv_limit_value['company_id'],
                                                               'app_types': approv_limit_value['app_types'],
                                                               'currency_id': approv_limit_value['currency_id']
                                                               }):
                update_count = update_count + 1
                valid_data_list.append(approv_limit_value)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(approv_limit_value)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_approv_limit_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(ApproverLimit,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for approv_limit in ui_data:
        # dependent check
        if django_query_instance.django_existence_check(ApproverLimitValue,
                                                        {'del_ind': False,
                                                         'client': global_variables.GLOBAL_CLIENT,
                                                         'app_code_id': approv_limit['app_code_id'],
                                                         }):
            # check for deletion of record
            if approv_limit['del_ind'] in ['1', True]:
                if status == 'SAVE':
                    if django_query_instance.django_existence_check(ApproverLimit,
                                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                                     'app_code_id': approv_limit[
                                                                         'app_code_id'],
                                                                     'company_id': approv_limit['company_id']
                                                                     }):
                        delete_count = delete_count + 1
                        valid_data_list.append(approv_limit)
                else:
                    if django_query_instance.django_existence_check(ApproverLimit,
                                                                    {'del_ind': False,
                                                                     'client': global_variables.GLOBAL_CLIENT,
                                                                     'app_code_id': approv_limit[
                                                                         'app_code_id'],
                                                                     'company_id': approv_limit['company_id'],
                                                                     }):
                        delete_count = delete_count + 1
                        valid_data_list.append(approv_limit)
                    else:
                        invalid_count = invalid_count + 1
            else:
                # duplicate check
                if django_query_instance.django_existence_check(ApproverLimit,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'approver_username': approv_limit['approver_username'],
                                                                 'app_code_id': approv_limit['app_code_id'],
                                                                 'company_id': approv_limit['company_id']
                                                                 }):
                    duplicate_count = duplicate_count + 1
                # update check
                elif django_query_instance.django_existence_check(ApproverLimit,
                                                                  {'del_ind': False,
                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                   'approver_username': approv_limit[
                                                                       'approver_username'],
                                                                   'company_id': approv_limit[
                                                                       'company_id']}):
                    update_count = update_count + 1
                    valid_data_list.append(approv_limit)
                else:
                    # insert check
                    insert_count = insert_count + 1
                    valid_data_list.append(approv_limit)
        else:
            print(approv_limit['app_code_id'])
            dependent_count = dependent_count + 1

        print(approv_limit)
    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_workflow_acc_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(WorkflowACC,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for workflw_acc_value in ui_data:
        if workflw_acc_value['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(WorkflowACC,
                                                                {'client': global_variables.GLOBAL_CLIENT,
                                                                 'acc_value': workflw_acc_value['acc_value'],
                                                                 'company_id': workflw_acc_value['company_id'],
                                                                 'app_username': workflw_acc_value['app_username'],
                                                                 'sup_company_id': workflw_acc_value[
                                                                     'sup_company_id'],
                                                                 'sup_acc_value': workflw_acc_value['sup_acc_value']
                                                                 }):
                    delete_count = delete_count + 1
                    valid_data_list.append(workflw_acc_value)
            else:
                if django_query_instance.django_existence_check(WorkflowACC,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'acc_value': workflw_acc_value['acc_value'],
                                                                 'company_id': workflw_acc_value['company_id'],
                                                                 'app_username': workflw_acc_value['app_username'],
                                                                 'sup_company_id': workflw_acc_value[
                                                                     'sup_company_id'],
                                                                 'sup_acc_value': workflw_acc_value['sup_acc_value']
                                                                 }):
                    delete_count = delete_count + 1
                    valid_data_list.append(workflw_acc_value)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(WorkflowACC,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'acc_value': workflw_acc_value['acc_value'],
                                                             'company_id': workflw_acc_value['company_id'],
                                                             'app_username': workflw_acc_value['app_username'],
                                                             'sup_company_id': workflw_acc_value[
                                                                 'sup_company_id'],
                                                             'sup_acc_value': workflw_acc_value['sup_acc_value']
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(WorkflowACC,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'acc_value': workflw_acc_value['acc_value'],
                                                               'company_id': workflw_acc_value['company_id'],
                                                               'app_username': workflw_acc_value['app_username'],
                                                               'sup_company_id': workflw_acc_value[
                                                                   'sup_company_id'],
                                                               'sup_acc_value': workflw_acc_value['sup_acc_value']
                                                               }):
                update_count = update_count + 1
                valid_data_list.append(workflw_acc_value)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(workflw_acc_value)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_address_types_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(OrgAddressMap,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for address_type in ui_data:
        # dependent check
        if django_query_instance.django_existence_check(OrgAddress,
                                                        {'del_ind': False,
                                                         'client': global_variables.GLOBAL_CLIENT,
                                                         'address_number': address_type['address_number']
                                                         }):
            if address_type['del_ind'] in ['1', True]:
                if status == 'SAVE':
                    if django_query_instance.django_existence_check(OrgAddressMap,
                                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                                     'address_number': address_type['address_number'],
                                                                     'address_type': address_type['address_type'],
                                                                     'company_id': address_type['company_id']}):
                        delete_count = delete_count + 1
                        valid_data_list.append(address_type)
                else:
                    if django_query_instance.django_existence_check(OrgAddressMap,
                                                                    {'del_ind': False,
                                                                     'client': global_variables.GLOBAL_CLIENT,
                                                                     'address_number': address_type[
                                                                         'address_number'],
                                                                     'address_type': address_type['address_type'],
                                                                     'company_id': address_type['company_id']}):
                        delete_count = delete_count + 1
                        valid_data_list.append(address_type)
                    else:
                        invalid_count = invalid_count + 1
            else:
                # duplicate check
                if django_query_instance.django_existence_check(OrgAddressMap,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'address_type': address_type['address_type'],
                                                                 'address_number': address_type['address_number'],
                                                                 'company_id': address_type['company_id'],
                                                                 }):
                    duplicate_count = duplicate_count + 1
                # update check
                elif django_query_instance.django_existence_check(OrgAddressMap,
                                                                  {'del_ind': False,
                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                   'address_number': address_type['address_number'],
                                                                   'address_type': address_type['address_type'],
                                                                   'company_id': address_type['company_id']}):
                    update_count = update_count + 1
                    valid_data_list.append(address_type)
                else:
                    # insert check
                    insert_count = insert_count + 1
                    valid_data_list.append(address_type)
        else:
            dependent_count = dependent_count + 1

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_determine_gl_acc_data(ui_data, status):
    db_count = django_query_instance.django_filter_count_query(DetermineGLAccount, {'del_ind': False,
                                                                                    'client': global_variables.GLOBAL_CLIENT})
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []

    for glaccount_detail in ui_data:
        if 'gl_acc_num' in glaccount_detail:
            gl_acc_num_value = glaccount_detail['gl_acc_num']
        else:
            # Handle the case where 'gl_acc_num' key is missing
            # You can raise an error, log a message, or handle it as needed
            continue  # Skip this iteration and move to the next item

        if glaccount_detail['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(DetermineGLAccount, {
                    'prod_cat_id': glaccount_detail['prod_cat_id'],
                    'gl_acc_num': gl_acc_num_value,  # Use the variable we checked
                    'gl_acc_default': glaccount_detail['gl_acc_default'],
                    'account_assign_cat': glaccount_detail['account_assign_cat'],
                    'company_id': glaccount_detail['company_id'],
                    'item_from_value': glaccount_detail['item_from_value'],
                    'item_to_value': glaccount_detail['item_to_value'],
                    'currency_id': glaccount_detail['currency_id'],
                    'client': global_variables.GLOBAL_CLIENT,
                }):
                    delete_count += 1
                    valid_data_list.append(glaccount_detail)
            else:
                if django_query_instance.django_existence_check(DetermineGLAccount, {
                    'prod_cat_id': glaccount_detail['prod_cat_id'],
                    'gl_acc_num': gl_acc_num_value,  # Use the variable we checked
                    'gl_acc_default': glaccount_detail['gl_acc_default'],
                    'account_assign_cat': glaccount_detail['account_assign_cat'],
                    'company_id': glaccount_detail['company_id'],
                    'item_from_value': glaccount_detail['item_from_value'],
                    'item_to_value': glaccount_detail['item_to_value'],
                    'currency_id': glaccount_detail['currency_id'],
                    'client': global_variables.GLOBAL_CLIENT,
                    'del_ind': False,
                }):
                    delete_count += 1
                    valid_data_list.append(glaccount_detail)
                else:
                    invalid_count += 1
        else:
            if django_query_instance.django_existence_check(DetermineGLAccount, {
                'prod_cat_id': glaccount_detail['prod_cat_id'],
                'gl_acc_num': gl_acc_num_value,  # Use the variable we checked
                'gl_acc_default': glaccount_detail['gl_acc_default'],
                'account_assign_cat': glaccount_detail['account_assign_cat'],
                'company_id': glaccount_detail['company_id'],
                'item_from_value': glaccount_detail['item_from_value'],
                'item_to_value': glaccount_detail['item_to_value'],
                'currency_id': glaccount_detail['currency_id'],
                'client': global_variables.GLOBAL_CLIENT,
                'del_ind': False,
            }):
                duplicate_count += 1
            elif django_query_instance.django_existence_check(DetermineGLAccount, {
                'prod_cat_id': glaccount_detail['prod_cat_id'],
                'gl_acc_num': gl_acc_num_value,  # Use the variable we checked
                'gl_acc_default': glaccount_detail['gl_acc_default'],
                'account_assign_cat': glaccount_detail['account_assign_cat'],
                'company_id': glaccount_detail['company_id'],
                'item_from_value': glaccount_detail['item_from_value'],
                'item_to_value': glaccount_detail['item_to_value'],
                'currency_id': glaccount_detail['currency_id'],
                'client': global_variables.GLOBAL_CLIENT,
                'del_ind': False,
            }):
                update_count += 1
                valid_data_list.append(glaccount_detail)
            else:
                insert_count += 1
                valid_data_list.append(glaccount_detail)

    message_count_dic = {
        'file_count': file_count,
        'delete_count': delete_count,
        'invalid_count': invalid_count,
        'duplicate_count': duplicate_count,
        'update_count': update_count,
        'insert_count': insert_count,
        'dependent_count': dependent_count,
        'db_count': db_count,
    }
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_address_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(OrgAddress,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for com_value in ui_data:
        if com_value['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(OrgAddress,
                                                                {
                                                                    'client': global_variables.GLOBAL_CLIENT,
                                                                    'address_number': com_value['address_number'],
                                                                }):
                    delete_count = delete_count + 1
                    valid_data_list.append(com_value)
            else:
                if django_query_instance.django_existence_check(OrgAddress,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'address_number': com_value['address_number'],
                                                                 }):
                    delete_count = delete_count + 1
                    valid_data_list.append(com_value)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(OrgAddress,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'address_number': com_value['address_number'],
                                                             'name1': com_value['name1'],
                                                             'name2': com_value['name2'],
                                                             'street': com_value['street'],
                                                             'area': com_value['area'],
                                                             'landmark': com_value['landmark'],
                                                             'city': com_value['city'],
                                                             'address_partner_type': com_value['address_partner_type'],
                                                             'org_address_source_system': com_value[
                                                                 'org_address_source_system'],
                                                             'postal_code': com_value['postal_code'],
                                                             'region': com_value['region'],
                                                             'mobile_number': com_value['mobile_number'],
                                                             'telephone_number': com_value['telephone_number'],
                                                             'fax_number': com_value['fax_number'],
                                                             'email': com_value['email'],
                                                             'country_code': com_value['country_code'],
                                                             'language_id': com_value['language_id'],
                                                             'time_zone': com_value['time_zone']
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(OrgAddress,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'address_number': com_value['address_number'],
                                                               }):
                update_count = update_count + 1
                valid_data_list.append(com_value)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(com_value)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_paymentterm_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(Payterms,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for payment_term_desc in ui_data:
        # check for deletion of record
        if payment_term_desc['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(Payterms,
                                                                {
                                                                    'client': global_variables.GLOBAL_CLIENT,
                                                                    'payment_term_key': payment_term_desc[
                                                                        'payment_term_key']
                                                                }):
                    delete_count = delete_count + 1
                    valid_data_list.append(payment_term_desc)
            else:
                if django_query_instance.django_existence_check(Payterms,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'payment_term_key': payment_term_desc[
                                                                     'payment_term_key']
                                                                 }):
                    delete_count = delete_count + 1
                    valid_data_list.append(payment_term_desc)
                else:
                    invalid_count = invalid_count + 1
        else:
            # duplicate check
            if django_query_instance.django_existence_check(Payterms,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'payment_term_key': payment_term_desc[
                                                                 'payment_term_key']}):
                duplicate_count = duplicate_count + 1
            # update check
            elif django_query_instance.django_existence_check(Payterms,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'payment_term_key': payment_term_desc[
                                                                   'payment_term_key']}):
                update_count = update_count + 1
                valid_data_list.append(payment_term_desc)
            else:
                # insert check
                insert_count = insert_count + 1
                valid_data_list.append(payment_term_desc)

        print(payment_term_desc)
    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_paymentterm_desc_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(Payterms_desc,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for payment_term_desc in ui_data:
        # dependent check
        if django_query_instance.django_existence_check(Payterms,
                                                        {'del_ind': False,
                                                         'client': global_variables.GLOBAL_CLIENT,
                                                         'payment_term_key': payment_term_desc['payment_term_key']
                                                         }):
            # check for deletion of record
            if payment_term_desc['del_ind'] in ['1', True]:
                if status == 'SAVE':
                    if django_query_instance.django_existence_check(Payterms_desc,
                                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                                     'payment_term_key': payment_term_desc[
                                                                         'payment_term_key'],
                                                                     'language_id': payment_term_desc['language_id']}):
                        delete_count = delete_count + 1
                        valid_data_list.append(payment_term_desc)
                else:
                    if django_query_instance.django_existence_check(Payterms_desc,
                                                                    {'del_ind': False,
                                                                     'client': global_variables.GLOBAL_CLIENT,
                                                                     'payment_term_key': payment_term_desc[
                                                                         'payment_term_key'],
                                                                     'language_id': payment_term_desc[
                                                                         'language_id']}):
                        delete_count = delete_count + 1
                        valid_data_list.append(payment_term_desc)
                    else:
                        invalid_count = invalid_count + 1
            else:
                # duplicate check
                if django_query_instance.django_existence_check(Payterms_desc,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'payment_term_key': payment_term_desc[
                                                                     'payment_term_key'],
                                                                 'description': payment_term_desc['description'],
                                                                 'day_limit': payment_term_desc['day_limit'],
                                                                 'language_id': payment_term_desc['language_id']
                                                                 }):
                    duplicate_count = duplicate_count + 1
                # update check
                elif django_query_instance.django_existence_check(Payterms_desc,
                                                                  {'del_ind': False,
                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                   'payment_term_key': payment_term_desc[
                                                                       'payment_term_key'],
                                                                   'language_id': payment_term_desc['language_id']
                                                                   }):
                    update_count = update_count + 1
                    valid_data_list.append(payment_term_desc)
                else:
                    # insert check
                    insert_count = insert_count + 1
                    valid_data_list.append(payment_term_desc)
        else:
            print(payment_term_desc['payment_term_key'])
            dependent_count = dependent_count + 1

        print(payment_term_desc)
    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_inco_terms_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(Incoterms,
                                                               {'del_ind': False,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for inco_terms in ui_data:
        if inco_terms['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(Incoterms,
                                                                {
                                                                    'incoterm_key': inco_terms[
                                                                        'incoterm_key']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(inco_terms)
            else:
                if django_query_instance.django_existence_check(Incoterms,
                                                                {'del_ind': False,
                                                                 'incoterm_key': inco_terms[
                                                                     'incoterm_key']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(inco_terms)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(Incoterms,
                                                            {'del_ind': False,
                                                             'incoterm_key': inco_terms['incoterm_key'],
                                                             'description': inco_terms['description']
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(Incoterms,
                                                              {'del_ind': False,
                                                               'incoterm_key': inco_terms[
                                                                   'incoterm_key']

                                                               }):
                update_count = update_count + 1
                valid_data_list.append(inco_terms)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(inco_terms)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def check_product_detail_data(ui_data, status):
    """

    """
    db_count = django_query_instance.django_filter_count_query(ProductsDetail,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for productsdetail in ui_data:
        # dependent check
        country_check = django_query_instance.django_existence_check(Country,
                                                                     {'country_code': productsdetail[
                                                                         'country_of_origin']})
        currency_check = django_query_instance.django_existence_check(Currency,
                                                                      {'currency_id': productsdetail[
                                                                          'currency']})
        languages_check = django_query_instance.django_existence_check(Languages,
                                                                       {'language_id': productsdetail[
                                                                           'language']})
        prod_cat_id_check = django_query_instance.django_existence_check(UnspscCategories,
                                                                         {'prod_cat_id': productsdetail[
                                                                             'prod_cat_id']})
        supplier_master_check = django_query_instance.django_existence_check(SupplierMaster,
                                                                             {'supplier_id': productsdetail[
                                                                                 'supplier_id'],
                                                                              'client': global_variables.GLOBAL_CLIENT})
        if country_check and currency_check and languages_check and prod_cat_id_check and supplier_master_check:
            # check for deletion of record
            if productsdetail['del_ind'] in ['1', True]:
                if status == 'SAVE':
                    if django_query_instance.django_existence_check(ProductsDetail,
                                                                    {
                                                                        'client': global_variables.GLOBAL_CLIENT,
                                                                        'product_id': productsdetail['product_id']}):
                        delete_count = delete_count + 1
                        valid_data_list.append(productsdetail)
                else:
                    if django_query_instance.django_existence_check(ProductsDetail,
                                                                    {'del_ind': False,
                                                                     'client': global_variables.GLOBAL_CLIENT,
                                                                     'product_id': productsdetail['product_id']}):
                        delete_count = delete_count + 1
                        valid_data_list.append(productsdetail)
                    else:
                        invalid_count = invalid_count + 1
            else:
                # duplicate check
                if django_query_instance.django_existence_check(ProductsDetail,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'product_id': productsdetail['product_id']}):
                    duplicate_count = duplicate_count + 1
                # update check
                elif django_query_instance.django_existence_check(ProductsDetail,
                                                                  {'del_ind': False,
                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                   'product_id': productsdetail['product_id']}):
                    update_count = update_count + 1
                    valid_data_list.append(productsdetail)
                else:
                    # insert check
                    insert_count = insert_count + 1
                    valid_data_list.append(productsdetail)
        else:
            print(productsdetail['prod_cat_id'])
            dependent_count = dependent_count + 1

        print(productsdetail)
    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def get_valid_country_data(ui_data, status):
    db_count = django_query_instance.django_filter_count_query(Country,
                                                               {'del_ind': False,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for country_dictionary in ui_data:
        if country_dictionary['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(Country,
                                                                {'country_code': country_dictionary[
                                                                    'country_code']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(country_dictionary)
            else:
                if django_query_instance.django_existence_check(Country,
                                                                {'del_ind': False,
                                                                 'country_code': country_dictionary[
                                                                     'country_code']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(country_dictionary)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(Country,
                                                            {'del_ind': False,
                                                             'country_code': country_dictionary['country_code'],
                                                             'country_name': country_dictionary['country_name']
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(Country,
                                                              {'del_ind': False,
                                                               'country_code': country_dictionary['country_code']}):
                update_count = update_count + 1
                valid_data_list.append(country_dictionary)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(country_dictionary)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def get_valid_currency_data(ui_data, status):
    db_count = django_query_instance.django_filter_count_query(Currency,
                                                               {'del_ind': False,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for currency_dictionary in ui_data:
        if currency_dictionary['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(Currency,
                                                                {'currency_id': currency_dictionary[
                                                                    'currency_id']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(currency_dictionary)
            else:
                if django_query_instance.django_existence_check(Currency,
                                                                {'del_ind': False,
                                                                 'currency_id': currency_dictionary[
                                                                     'currency_id']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(currency_dictionary)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(Currency,
                                                            {'del_ind': False,
                                                             'currency_id': currency_dictionary['currency_id'],
                                                             'description': currency_dictionary['description']
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(Currency,
                                                              {'del_ind': False,
                                                               'currency_id': currency_dictionary['currency_id']}):
                update_count = update_count + 1
                valid_data_list.append(currency_dictionary)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(currency_dictionary)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def get_valid_language_data(ui_data, status):
    db_count = django_query_instance.django_filter_count_query(Languages,
                                                               {'del_ind': False,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for language_dictionary in ui_data:
        if language_dictionary['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(Languages,
                                                                {'language_id': language_dictionary[
                                                                    'language_id']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(language_dictionary)
            else:
                if django_query_instance.django_existence_check(Languages,
                                                                {'del_ind': False,
                                                                 'language_id': language_dictionary[
                                                                     'language_id']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(language_dictionary)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(Languages,
                                                            {'del_ind': False,
                                                             'language_id': language_dictionary['language_id'],
                                                             'description': language_dictionary['description']
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(Languages,
                                                              {'del_ind': False,
                                                               'language_id': language_dictionary['language_id']}):
                update_count = update_count + 1
                valid_data_list.append(language_dictionary)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(language_dictionary)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def get_valid_timezone_data(ui_data, status):
    db_count = django_query_instance.django_filter_count_query(TimeZone,
                                                               {'del_ind': False,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for timezone_dictionary in ui_data:
        if timezone_dictionary['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(TimeZone,
                                                                {'time_zone': timezone_dictionary[
                                                                    'time_zone']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(timezone_dictionary)
            else:
                if django_query_instance.django_existence_check(TimeZone,
                                                                {'del_ind': False,
                                                                 'time_zone': timezone_dictionary[
                                                                     'time_zone']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(timezone_dictionary)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(TimeZone,
                                                            {'del_ind': False,
                                                             'time_zone': timezone_dictionary['time_zone'],
                                                             'description': timezone_dictionary['description'],
                                                             'utc_difference': timezone_dictionary['utc_difference'],
                                                             'daylight_save_rule': timezone_dictionary[
                                                                 'daylight_save_rule']
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(TimeZone,
                                                              {'del_ind': False,
                                                               'time_zone': timezone_dictionary['time_zone']}):
                update_count = update_count + 1
                valid_data_list.append(timezone_dictionary)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(timezone_dictionary)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def get_valid_uom_data(ui_data, status):
    db_count = django_query_instance.django_filter_count_query(UnitOfMeasures,
                                                               {'del_ind': False,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for unitofmeasure_dictionary in ui_data:
        if unitofmeasure_dictionary['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(UnitOfMeasures,
                                                                {'uom_id': unitofmeasure_dictionary[
                                                                    'uom_id']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(unitofmeasure_dictionary)
            else:
                if django_query_instance.django_existence_check(UnitOfMeasures,
                                                                {'del_ind': False,
                                                                 'uom_id': unitofmeasure_dictionary[
                                                                     'uom_id']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(unitofmeasure_dictionary)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(UnitOfMeasures,
                                                            {'del_ind': False,
                                                             'uom_id': unitofmeasure_dictionary['uom_id'],
                                                             'uom_description': unitofmeasure_dictionary
                                                             ['uom_description'],
                                                             'iso_code_id': unitofmeasure_dictionary
                                                             ['iso_code_id']
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(UnitOfMeasures,
                                                              {'del_ind': False,
                                                               'uom_id': unitofmeasure_dictionary['uom_id']}):
                update_count = update_count + 1
                valid_data_list.append(unitofmeasure_dictionary)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(unitofmeasure_dictionary)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def get_valid_employee_data(ui_data, status):
    db_count = django_query_instance.django_filter_count_query(UserData,
                                                               {'del_ind': False,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for employee_dictionary in ui_data:
        if employee_dictionary['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(UserData,
                                                                {'email': employee_dictionary[
                                                                    'email']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(employee_dictionary)
            else:
                if django_query_instance.django_existence_check(UserData,
                                                                {'del_ind': False,
                                                                 'email': employee_dictionary[
                                                                     'email']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(employee_dictionary)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(UserData,
                                                            {'del_ind': False,
                                                             'email': employee_dictionary['email'],
                                                             # 'username': employee_dictionary
                                                             # ['username'],
                                                             # 'first_name': employee_dictionary
                                                             # ['first_name'],
                                                             # 'last_name': employee_dictionary
                                                             # ['last_name'],
                                                             # 'phone_num': employee_dictionary
                                                             # ['phone_num'],
                                                             # ['user_type']: employee_dictionary
                                                             #  ['user_type'],
                                                             # 'date_format': employee_dictionary
                                                             # ['date_format'],
                                                             # 'employee_id': employee_dictionary
                                                             # ['employee_id'],
                                                             # 'decimal_notation': employee_dictionary
                                                             # ['decimal_notation'],
                                                             # 'currency_id': employee_dictionary
                                                             # ['currency_id'],
                                                             # 'language_id': employee_dictionary
                                                             # ['language_id'],
                                                             # 'time_zone': employee_dictionary
                                                             # ['time_zone']
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(UserData,
                                                              {'del_ind': False,
                                                               'email': employee_dictionary['email']}):
                update_count = update_count + 1
                valid_data_list.append(employee_dictionary)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(employee_dictionary)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def get_valid_supplier_data(ui_data, status):
    db_count = django_query_instance.django_filter_count_query(SupplierMaster,
                                                               {'del_ind': False,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for supplier_dictionary in ui_data:
        if supplier_dictionary['del_ind'] in ['1', True]:
            if status == 'SAVE':
                if django_query_instance.django_existence_check(SupplierMaster,
                                                                {'supplier_id': supplier_dictionary[
                                                                    'supplier_id']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(supplier_dictionary)
            else:
                if django_query_instance.django_existence_check(SupplierMaster,
                                                                {'del_ind': False,
                                                                 'supplier_id': supplier_dictionary[
                                                                     'supplier_id']}):
                    delete_count = delete_count + 1
                    valid_data_list.append(supplier_dictionary)
                else:
                    invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(SupplierMaster,
                                                            {'del_ind': False,
                                                             'supplier_id': supplier_dictionary['supplier_id'],
                                                             # 'username': employee_dictionary
                                                             # ['username'],
                                                             # 'first_name': employee_dictionary
                                                             # ['first_name'],
                                                             # 'last_name': employee_dictionary
                                                             # ['last_name'],
                                                             # 'phone_num': employee_dictionary
                                                             # ['phone_num'],
                                                             # ['user_type']: employee_dictionary
                                                             #  ['user_type'],
                                                             # 'date_format': employee_dictionary
                                                             # ['date_format'],
                                                             # 'employee_id': employee_dictionary
                                                             # ['employee_id'],
                                                             # 'decimal_notation': employee_dictionary
                                                             # ['decimal_notation'],
                                                             # 'currency_id': employee_dictionary
                                                             # ['currency_id'],
                                                             # 'language_id': employee_dictionary
                                                             # ['language_id'],
                                                             # 'time_zone': employee_dictionary
                                                             # ['time_zone']
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(SupplierMaster,
                                                              {'del_ind': False,
                                                               'supplier_id': supplier_dictionary['supplier_id']}):
                update_count = update_count + 1
                valid_data_list.append(supplier_dictionary)
            else:
                insert_count = insert_count + 1
                valid_data_list.append(supplier_dictionary)

    # append message with count
    message_count_dic = {'file_count': file_count, 'delete_count': delete_count, 'invalid_count': invalid_count,
                         'duplicate_count': duplicate_count, 'update_count': update_count,
                         'insert_count': insert_count,
                         'dependent_count': dependent_count, 'db_count': db_count}
    message = get_check_message(message_count_dic)
    return valid_data_list, message


def get_valid_unspsc_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(prod_cat_id=data['prod_cat_id'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(UnspscCategories,
                                                                      {'del_ind': True}, filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_org_node_type_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(node_type=data['node_type'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(OrgNodeTypes,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_org_attributes_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(attribute_id=data['attribute_id'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(OrgAttributes,
                                                                      {'del_ind': True},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_org_nodetype_config_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(org_model_types=data['org_model_types'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(OrgModelNodetypeConfig,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_org_authorization_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(auth_obj_id=data['auth_obj_id'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(AuthorizationObject,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_SpendLimitValue_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(company_id=data['company_id'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(SpendLimitValue,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_payment_desc_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(payment_term_key=data['payment_term_key'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(Payterms_desc,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_UnspscCategoriesCustDesc_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(prod_cat_id=data['prod_cat_id'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(UnspscCategoriesCustDesc,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_ApproverType_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(app_types=data['app_types'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(ApproverType,
                                                                      {'del_ind': True},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_work_flow_schema_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(workflow_schema=data['workflow_schema'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(WorkflowSchema,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_ApproverType_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(app_types=data['app_types'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(ApproverType,
                                                                      {'del_ind': True},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list
