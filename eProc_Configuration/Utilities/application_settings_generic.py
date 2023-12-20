from re import sub

from eProc_Attributes.models.org_attribute_models import OrgAttributesLevel
from eProc_Basic.Utilities.constants.constants import CONST_SC_TRANS_TYPE, CONST_ACTION_DELETE, CONST_DEFAULT_LANGUAGE
from eProc_Basic.Utilities.functions.dictionary_key_to_list import dictionary_key_to_list
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_uncommon_in_list import get_uncommon_element_list
from eProc_Basic.Utilities.functions.messages_config import get_message_desc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models.application_data import *
from eProc_Configuration.models.basic_data import UnspscCategories
from eProc_Configuration.models.development_data import *
from eProc_Configuration.models.master_data import *

django_query_instance = DjangoQueries()


def get_configuration_data(db_name, filter_query, value_list):
    """

    """
    result = django_query_instance.django_filter_query(db_name, filter_query, None, value_list)
    return result


def get_configuration_data_image(db_name, filter_query, value_list):
    """

    """
    result = django_query_instance.django_filter_query(db_name, filter_query, None, value_list)
    return result


class FieldTypeDescriptionUpdate:
    @staticmethod
    def update_usedFlag(field_type_id):
        if django_query_instance.django_existence_check(FieldTypeDescription, {
            'del_ind': False, 'field_type_id': field_type_id, 'client': global_variables.GLOBAL_CLIENT
        }):
            django_query_instance.django_filter_only_query(FieldTypeDescription, {
                'del_ind': False, 'field_type_id': field_type_id, 'client': global_variables.GLOBAL_CLIENT
            }).update(used_flag=True)

    @staticmethod
    def reset_usedFlag(field_type_id):
        if django_query_instance.django_existence_check(FieldTypeDescription, {
            'del_ind': False, 'field_type_id': field_type_id, 'client': global_variables.GLOBAL_CLIENT
        }):
            django_query_instance.django_filter_only_query(FieldTypeDescription, {
                'del_ind': False, 'field_type_id': field_type_id, 'client': global_variables.GLOBAL_CLIENT
            }).update(used_flag=False)

    @staticmethod
    def get_field_type_desc_values(db_name, filter_query, value_list):
        result = django_query_instance.django_filter_query(db_name, filter_query, None, value_list)
        return result

    @staticmethod
    def reset_used_flag(field_type_id, field_name):
        if django_query_instance.django_existence_check(FieldTypeDescription, {
            'del_ind': False, 'field_type_id': field_type_id, 'client': global_variables.GLOBAL_CLIENT
        }):
            django_query_instance.django_filter_only_query(FieldTypeDescription,
                                                           {'del_ind': False,
                                                            'field_type_id': field_type_id,
                                                            'field_name': field_name,
                                                            'client': global_variables.GLOBAL_CLIENT}).update(
                used_flag=False)

    @staticmethod
    def update_used_flag(field_type_id, field_name):
        if django_query_instance.django_existence_check(FieldTypeDescription, {
            'del_ind': False, 'field_type_id': field_type_id, 'client': global_variables.GLOBAL_CLIENT
        }):
            django_query_instance.django_filter_only_query(FieldTypeDescription, {
                'del_ind': False, 'field_type_id': field_type_id, 'field_name': field_name,
                'client': global_variables.GLOBAL_CLIENT
            }).update(used_flag=True)


def set_field_used_flag(field_type_id_list, field_name):
    django_query_instance.django_filter_only_query(FieldTypeDescription, {
        'del_ind': False, 'field_type_id__in': field_type_id_list, 'field_name': field_name,
        'client': global_variables.GLOBAL_CLIENT
    }).update(used_flag=True)


def reset_field_used_flag(field_type_id_list, field_name):
    django_query_instance.django_filter_only_query(FieldTypeDescription, {
        'del_ind': False, 'field_type_id__in': field_type_id_list, 'field_name': field_name,
        'client': global_variables.GLOBAL_CLIENT
    }).update(used_flag=False)


def get_field_unused_list_values(field_name):
    result = list(FieldTypeDescription.objects.filter(del_ind=False,
                                                      used_flag=False,
                                                      field_name=field_name,
                                                      client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                                    'field_type_desc',
                                                                                                    ))
    return result


def get_field_list_values(field_name):
    result = list(FieldTypeDescription.objects.filter(del_ind=False,
                                                      field_name=field_name,
                                                      client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                                    'field_type_desc',
                                                                                                    ))
    return result


def set_reset_field(used_flag_reset, used_flag_set, field_name):
    if used_flag_reset:
        reset_field_used_flag(used_flag_reset, field_name)
    if used_flag_set:
        set_field_used_flag(used_flag_set, field_name)


def get_message_detail_based_on_action(action):
    if action == CONST_ACTION_DELETE:
        msgid = 'MSG113'
    else:
        msgid = 'MSG112'
    message = get_message_desc(msgid)[1]
    return message


def get_product_criteria():
    """

    """
    client = global_variables.GLOBAL_CLIENT
    upload_account_assign_cat = get_configuration_data(PoSplitCriteria,
                                                       {'del_ind': False,
                                                        'client': client},
                                                       ['po_split_criteria_guid', 'company_code_id', 'activate',
                                                        'po_split_type'])
    data = get_po_split_creteria_dropdown(upload_account_assign_cat)
    data['upload_account_assign_cat'] = upload_account_assign_cat
    return data


def get_po_split_creteria_dropdown(upload_account_assign_cat):
    """

    """
    po_split_types = django_query_instance.django_filter_query(PoSplitType, {'del_ind': False}, None, None)
    for po_criteria in upload_account_assign_cat:
        for po_split_type in po_split_types:
            if po_split_type['po_split_type'] == po_criteria['po_split_type']:
                po_criteria['po_split_type_desc'] = str(po_split_type['po_split_type']) + ' - ' + po_split_type[
                    'po_split_type_desc']

    po_split_typ = get_configuration_data(PoSplitType, {'del_ind': False},
                                          ['po_split_type', 'po_split_type_desc'])
    for po_dropdown in po_split_typ:
        po_dropdown['po_split_type_desc'] = str(po_dropdown['po_split_type']) + ' - ' + po_dropdown[
            'po_split_type_desc']

    dropdown_activate = list(
        FieldTypeDescription.objects.filter(field_name='activate', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values(
            'field_type_id',
            'field_type_desc'
        ))

    upload_data_company = list(
        OrgCompanies.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('company_id'))

    data = {'po_split_typ': po_split_typ,
            'dropdown_activate': dropdown_activate,
            'upload_data_company': upload_data_company}
    return data


def get_unspsc_data():
    upload_product_category = get_configuration_data(UnspscCategories, {'del_ind': False}, ['prod_cat_id',
                                                                                            'prod_cat_desc'
                                                                                            ])
    for prod_cat_desc in upload_product_category:
        if django_query_instance.django_existence_check(UnspscCategoriesCustDesc,
                                                        {'del_ind': False,
                                                         'prod_cat_id': prod_cat_desc['prod_cat_id']}):
            prod_cat_desc["del_ind_flag"] = False
        else:
            prod_cat_desc["del_ind_flag"] = True

        if prod_cat_desc['prod_cat_desc'] == None:
            prod_cat_desc['prod_cat_desc'] = ''

    return upload_product_category


def get_ui_messages(messages_id_list):
    """

    """
    client = global_variables.GLOBAL_CLIENT

    message_desc_user = django_query_instance.django_filter_query(MessagesIdDesc, {
        'del_ind': False, 'messages_id__in': messages_id_list, 'client': client,
        'language_id': global_variables.GLOBAL_USER_LANGUAGE,
    }, ['messages_id'], ['messages_id_desc', 'messages_id'])
    db_message_id_list = dictionary_key_to_list(message_desc_user, 'messages_id')
    if db_message_id_list:
        subset_message_id_list = get_uncommon_element_list(messages_id_list,db_message_id_list)
    else:
        subset_message_id_list = messages_id_list
    if subset_message_id_list:
        message_desc_default = django_query_instance.django_filter_query(MessagesIdDesc, {
            'del_ind': False, 'messages_id__in': subset_message_id_list, 'client': client,
            'language_id': CONST_DEFAULT_LANGUAGE,
        },  ['messages_id'], ['messages_id_desc', 'messages_id'])
        message_desc = message_desc_user + message_desc_default
    else:
        message_desc = message_desc_user
    return message_desc
