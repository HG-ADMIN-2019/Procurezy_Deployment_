"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    user_settings_specific.py
Usage:
    Attributes page related function
    list of functions
    1. get_attr_value_list - get attribute value list
    2. get_parents_obj_id - get login user and its parent obj_id
    3. get_parent_guid_obj_id - get parent guid and obj_id

Author:
    Deepika K
"""
from eProc_Attributes.models.org_attribute_models import OrgAttributesLevel
from eProc_Basic.Utilities.functions.dict_check_key import checkKey
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.ignore_duplicates import remove_duplicates_in_dic_list
from eProc_Basic.Utilities.functions.sort_dictionary import sort_list_dictionary_key_values

from Majjaka_eProcure import settings
from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.type_casting import convert_query_set_list
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import OrgClients, \
     OrgAddressMap, AccountingData, SpendLimitId, OrgAddress, OrgPorg, OrgPGroup, OrgCompanies, \
    ApproverLimit,  CalenderConfig, Catalogs
from eProc_Configuration.models.application_data import ProjectDetails
from eProc_Configuration.models.development_data import *
from eProc_Configuration.models.development_data import *
from eProc_Org_Model.models import OrgModel
from eProc_User_Settings.Utilities.user_settings_generic import get_obj_id_parent_guid
from eProc_Configuration.models import AccountingDataDesc


def get_attr_value_list(client, attr_object_id):
    """
    get attribute value list
    :param client:
    :param attr_object_id:
    :return:
    """
    attr_detail_list = []
    obj_id_list = get_parents_obj_id(client, attr_object_id)
    obj_id_list.reverse()
    attr_id_list = DjangoQueries.django_filter_value_list_ordered_by_distinct_query(OrgAttributesLevel,
                                                                                    {'object_id__in': obj_id_list,
                                                                                     'client': client},
                                                                                    'attribute_id', ['attribute_id'])
    if attr_id_list:
        attr_id_desc = list(DjangoQueries.django_filter_query(OrgAttributes,
                                                              {'attribute_id__in': attr_id_list},
                                                              ['attribute_id'],
                                                              ['attribute_name', 'attribute_id']))
        org_model_node_detail = list(DjangoQueries.django_filter_query(OrgModel,
                                                                       {'object_id__in': obj_id_list},
                                                                       None,
                                                                       ['object_id', 'name']))
        attr_detail_list = get_attr_level_detail_from_attr_id(attr_id_list, obj_id_list, attr_id_desc,
                                                              org_model_node_detail)
    return attr_detail_list


def get_attr_level_detail_from_attr_id(attr_id_list, obj_id_list, attr_id_desc, org_model_node_detail):
    """
    
    :param attr_id_list: 
    :param obj_id_list: 
    :return: 
    """
    attr_detail_list = []
    for attr_id in attr_id_list:
        attr_details = DjangoQueries.django_filter_query(OrgAttributesLevel,
                                                         {'object_id__in': obj_id_list,
                                                          'attribute_id': attr_id,
                                                          'client': global_variables.GLOBAL_CLIENT,
                                                          'del_ind': False},
                                                         None,
                                                         ['object_id', 'attribute_id',
                                                          'low', 'attr_level_default',
                                                          'attr_level_exclude',
                                                          'attr_level_guid', 'high',
                                                          'attribute_value_desc',
                                                          'extended_value'])
        for attr_detail in attr_details:
            # add attribute description to OrgAttributesLevel detail
            for attr_desc in attr_id_desc:
                if attr_desc['attribute_id'] == attr_detail['attribute_id']:
                    attr_detail['attribute_name'] = attr_desc['attribute_name']
            for org_model_node_name in org_model_node_detail:
                if org_model_node_name['object_id'] == attr_detail['object_id']:
                    attr_detail['org_node_name'] = org_model_node_name['name']
        attr_detail_list += sort_list_dictionary_key_values(obj_id_list, attr_details, 'object_id')
    return attr_detail_list


def get_parents_obj_id(client, attr_object_id):
    """
    get login user and its parent obj_id
    :param attr_object_id:
    :return:
    """
    array_obj_id = []
    parent_odj_id, parent_guid = get_parent_guid_obj_id(attr_object_id)
    if parent_odj_id:
        array_obj_id.append(parent_odj_id)
        while parent_guid:
            obj_id, parent_guid = get_obj_id_parent_guid(parent_guid, client)
            array_obj_id.append(obj_id)

    return array_obj_id


def get_parent_guid_obj_id(attr_object_id):
    """
    get parent guid and obj_id
    :param attr_object_id:
    :return:
    """
    parent_odj_id = None
    parent_guid = None
    if DjangoQueries.django_existence_check(OrgModel,
                                            {'object_id': attr_object_id,
                                             'client': global_variables.GLOBAL_CLIENT,
                                             'del_ind': False}):
        org_model = DjangoQueries.django_get_query(OrgModel,
                                                   {'object_id': attr_object_id,
                                                    'client': global_variables.GLOBAL_CLIENT,
                                                    'del_ind': False})

        parent_odj_id = org_model.object_id
        parent_guid = org_model.parent_node_guid

    return parent_odj_id, parent_guid


def append_attribute_value_description(query_values_list, attribute_value_field, description_field):
    attribute_values_list = []
    attribute_append_id_desc_list = []
    if query_values_list:
        for query_values in query_values_list:
            if query_values[description_field]:
                attribute_values_description = query_values[attribute_value_field] + ' - ' + query_values[description_field]
            else:
                attribute_values_description = query_values[attribute_value_field]
            attribute_values = {'attribute_values': query_values[attribute_value_field],
                                'attribute_values_description': attribute_values_description}
            attribute_append_id_desc_list.append(attribute_values_description)
            attribute_values_list.append(attribute_values)
    return attribute_values_list,attribute_append_id_desc_list


def append_description_atrr_value_exists(desc_query_list,attr_value_list, value_field_name, description_field_name):
    """

    """
    attribute_values_list = []
    desc_attr_value = []
    append_attr_val_and_desc = []
    if desc_query_list:
        for query_values in desc_query_list:
            desc_attr_value.append(query_values[value_field_name])
            attribute_values_description = query_values[value_field_name]
            if query_values[value_field_name] in attr_value_list:
                if query_values[description_field_name]:
                    attribute_values_description = query_values[value_field_name] + ' - ' + query_values[description_field_name]
            attribute_values = {'attribute_values': query_values[value_field_name],
                                'attribute_values_description': attribute_values_description}
            append_attr_val_and_desc.append(attribute_values_description)
            attribute_values_list.append(attribute_values)
        for attr_value in attr_value_list:
            if attr_value not in desc_attr_value:
                attribute_values = {'attribute_values': attr_value,
                                    'attribute_values_description': attr_value}
                append_attr_val_and_desc.append(attr_value)
                attribute_values_list.append(attribute_values)
    else:
        for attr_value in attr_value_list:
            attribute_values = {'attribute_values': attr_value,
                                'attribute_values_description': attr_value}
            append_attr_val_and_desc.append(attr_value)
            attribute_values_list.append(attribute_values)

    return attribute_values_list,append_attr_val_and_desc


def get_acc_value_desc_list(acc_asg_cat):
    """

    """
    accounting_data = DjangoQueries.django_filter_value_list_query(AccountingData,
                                                                   {'client': global_variables.GLOBAL_CLIENT,
                                                                    'del_ind': False,
                                                                    'account_assign_cat': acc_asg_cat},
                                                                   'account_assign_value')
    accounting_data_desc = DjangoQueries.django_filter_query(AccountingDataDesc,
                                                             {'client': global_variables.GLOBAL_CLIENT,
                                                              'del_ind': False,
                                                              'account_assign_cat': acc_asg_cat,
                                                              'account_assign_value__in': accounting_data,
                                                              'language_id': global_variables.GLOBAL_USER_LANGUAGE},
                                                             None,
                                                             ['account_assign_value', 'description'])
    attr_values_list = append_description_atrr_value_exists(accounting_data_desc,
                                                            accounting_data, 'account_assign_value', 'description')[0]
    return attr_values_list


def get_dropdown_value(client, attr_value):
    """

    :param attr_value:
    :return:
    """
    del_addr_list = []
    invoice_addr_list = []
    if attr_value == CONST_ACC_CAT:
        acc_value_list = DjangoQueries.django_filter_query(AccountAssignmentCategory,
                                                           None,
                                                           None,
                                                           ['account_assign_cat', 'description'])
        attribute_values_list = append_attribute_value_description(acc_value_list, 'account_assign_cat', 'description')[0]

        return attribute_values_list
    if attr_value == CONST_CT_CTR:
        attribute_values_list = get_acc_value_desc_list(CONST_CC)
        return attribute_values_list
    if attr_value == CONST_WBS_ELEM:
        attribute_values_list = get_acc_value_desc_list(CONST_WBS)
        return attribute_values_list
    if attr_value == CONST_INT_ORD:
        attribute_values_list = get_acc_value_desc_list(CONST_OR)
        return attribute_values_list
    if attr_value == CONST_AS_SET:
        attribute_values_list = get_acc_value_desc_list(CONST_AS)
        return attribute_values_list
    if attr_value == CONST_CO_CODE:
        attr_val_desc_list = DjangoQueries.django_filter_query(OrgCompanies,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'del_ind': False},
                                                             None,
                                                             ['company_id', 'name1'])
        attribute_values_list = append_attribute_value_description(attr_val_desc_list, 'company_id', 'name1')[0]
        return attribute_values_list
    if attr_value == CONST_DEF_DOC_SEARCH:
        attr_val_desc_list = DjangoQueries.django_filter_query(DocumentType,
                                                               None,
                                                               None,
                                                               ['document_type', 'document_type_desc'])
        attribute_values_list = append_attribute_value_description(attr_val_desc_list,
                                                                   'document_type',
                                                                   'document_type_desc')[0]
        return attribute_values_list
    if attr_value == CONST_DEL_ADDR:
        del_addrs = OrgAddressMap.objects.filter(client=client)
        for del_addr in del_addrs:
            if del_addr.address_type == 'D':
                if OrgAddress.objects.filter(address_number=del_addr.address_number, client=client).exists():
                    addr_detail = OrgAddress.objects.get(address_number=del_addr.address_number, client=client)
                    del_addr_list.append(addr_detail.address_number)
        del_addr_list = append_description_atrr_value_exists(None,del_addr_list,None,None)[0]
        return del_addr_list
    if attr_value == CONST_INV_ADDR:
        invoice_addrs = OrgAddressMap.objects.filter(client=client)
        for invoice_addr in invoice_addrs:
            if invoice_addr.address_type == 'I':
                if OrgAddress.objects.filter(address_number=invoice_addr.address_number, client=client).exists():
                    addr_detail = OrgAddress.objects.get(address_number=invoice_addr.address_number, client=client)
                    invoice_addr_list.append(addr_detail.address_number)
        invoice_addr_list = append_description_atrr_value_exists(None, invoice_addr_list, None, None)[0]
        return invoice_addr_list
    if attr_value == CONST_US_ROLE:
        attr_val_desc_list = DjangoQueries.django_filter_query(UserRoles,
                                                               None,
                                                               None,
                                                               ['role', 'role_desc'])
        attribute_values_list = append_attribute_value_description(attr_val_desc_list,
                                                                   'role',
                                                                   'role_desc')[0]
        return attribute_values_list
    if attr_value == CONST_CAT_ID:
        attr_val_desc_list = DjangoQueries.django_filter_query(Catalogs,
                                                               {'client' : client
                                                                   ,
                                                                'is_active_flag': True
                                                                   ,
                                                                'del_ind' :False},
                                                               None,
                                                               ['catalog_id', 'description'])
        attribute_values_list = append_attribute_value_description(attr_val_desc_list,
                                                                   'catalog_id',
                                                                   'description')[0]
        return attribute_values_list
    if attr_value == CONST_SC_TRANS_TYPE:
        attr_val_desc_list = DjangoQueries.django_filter_query(TransactionTypes,
                                                               {'client': client,
                                                                'del_ind': False,
                                                                'document_type':CONST_DOC_TYPE_SC},
                                                               None,
                                                               ['transaction_type', 'description'])
        attribute_values_list = append_attribute_value_description(attr_val_desc_list,
                                                                   'transaction_type',
                                                                   'description')[0]
        return attribute_values_list
    if attr_value == CONST_PO_TRANS_TYPE:
        attr_val_desc_list = DjangoQueries.django_filter_query(TransactionTypes,
                                                               {'client': client,
                                                                'del_ind': False,
                                                                'document_type':CONST_DOC_TYPE_PO},
                                                               None,
                                                               ['transaction_type', 'description'])
        attribute_values_list = append_attribute_value_description(attr_val_desc_list,
                                                                   'transaction_type',
                                                                   'description')[0]
        return attribute_values_list
    if attr_value == CONST_FC_TRANS_TYPE:
        attr_val_desc_list = DjangoQueries.django_filter_query(TransactionTypes,
                                                               {'client': client,
                                                                'del_ind': False,
                                                                'document_type': CONST_DOC_TYPE_FC},
                                                               None,
                                                               ['transaction_type', 'description'])
        attribute_values_list = append_attribute_value_description(attr_val_desc_list,
                                                                   'transaction_type',
                                                                   'description')[0]
        return attribute_values_list
    if attr_value == CONST_CALENDAR_ID:
        attr_val_desc_list = DjangoQueries.django_filter_query(CalenderConfig,
                                                               {'client': client,
                                                                'del_ind': False},
                                                               None,
                                                               ['calender_id', 'description'])
        attribute_values_list = append_attribute_value_description(attr_val_desc_list,
                                                                   'calender_id',
                                                                   'description')[0]
        return attribute_values_list
    if attr_value == CONST_PROJECT_ID:
        attr_val_desc_list = DjangoQueries.django_filter_query(ProjectDetails,
                                                               {'client': client,
                                                                'del_ind': False},
                                                               None,
                                                               ['project_id', 'project_name'])
        attribute_values_list = append_attribute_value_description(attr_val_desc_list,
                                                                   'project_id',
                                                                   'project_name')[0]
        return attribute_values_list


def get_extended_att_list(client, object_id, attr_id):
    """
        get extended attribute value list
        :param client:
        :param attr_object_id:
        :return:
        """
    obj_id_list = get_parents_obj_id(client, object_id)
    attr_value = OrgAttributesLevel.objects.filter(object_id__in=obj_id_list, attribute_id=attr_id).order_by(
        'attribute_id')
    return attr_value


def get_dropdown_attr_id_list(client, attribute_id, obj_id_user):
    """
    based on attribute id get dropdown and get attribute values based on object id of selected nod and its parent
    :param client:
    :param attr_level_pk:
    :param obj_id_user:
    :return:
    """

    object_id_list = get_parents_obj_id(client, obj_id_user)
    object_id_list.reverse()
    drop_down = get_dropdown_value(client, attribute_id)
    attr_id_list = OrgAttributesLevel.objects.filter(attribute_id=attribute_id,
                                                     object_id__in=object_id_list).values('object_id', 'attribute_id',
                                                                                          'low',
                                                                                          'attr_level_default',
                                                                                          'attr_level_exclude',
                                                                                          'attr_level_guid',
                                                                                          'attribute_value_desc')
    attr_id_list = sort_list_dictionary_key_values(object_id_list, attr_id_list, 'object_id')
    return drop_down, attr_id_list


def append_dropdown_attr_id_list(drop_down, attr_id_list):
    """
    Append two query set
    :param drop_down:
    :param attr_id_list:
    :return:
    """
    list_result = [drop_down]
    list_result_value = convert_query_set_list(attr_id_list)
    list_result.extend(list_result_value)
    return list_result


def save_attr_level_data(current_attr_list, inherited_list, attr_object_id,client):
    created = ''
    # check if exclude is present in inherited_list
    for count, current_attr in enumerate(current_attr_list):
        exclude_consider_flag = False
        for inherit_value in reversed(inherited_list):
            if inherit_value['value'] == current_attr['value']:
                if inherit_value['attr_level_exclude']:
                    exclude_consider_flag = True
                    break
    # check if default is present in inherited_list then set flag
    for count, current_attr in enumerate(current_attr_list):
        default_consider_flag = False
        for inherit_value in reversed(inherited_list):
            if inherit_value['value'] == current_attr['value']:
                if inherit_value['attr_level_default']:
                    default_consider_flag = True
                    break
        # check if current attribute is not present in inherited attributes then
        # save attribute to org attribute level table
        if (current_attr not in inherited_list) or (exclude_consider_flag == True) or (default_consider_flag == True):
            if current_attr['attr_level_default']:
                default_flag = True
            else:
                default_flag = False
            if current_attr['attr_level_exclude']:
                exclude_flag = True
            else:
                exclude_flag = False
            if OrgAttributesLevel.objects.filter(client=client,
                                                 attribute_id=current_attr['attribute_id'],
                                                 low=current_attr['value'],
                                                 object_id=attr_object_id).exists():
                if not OrgAttributesLevel.objects.filter(client=client,
                                                         attribute_id=current_attr['attribute_id'],
                                                         low=current_attr['value'],
                                                         attr_level_exclude=True,
                                                         object_id=attr_object_id).exists():
                    if default_flag:
                        OrgAttributesLevel.objects.filter(client=client,
                                                          attribute_id=current_attr['attribute_id'],
                                                          low=current_attr['value'],
                                                          object_id=attr_object_id).update(
                            attr_level_default=default_flag)
                if exclude_flag:
                    OrgAttributesLevel.objects.filter(client=client,
                                                      attribute_id=current_attr['attribute_id'],
                                                      low=current_attr['value'],
                                                      object_id=attr_object_id).update(attr_level_default=default_flag,
                                                                                       attr_level_exclude=exclude_flag)

            else:
                if exclude_flag:
                    default_flag = False
                attribute_value_desc = get_attr_value_desc(current_attr['attribute_id'], current_attr['value'])
                created = OrgAttributesLevel.objects.create(
                    client=OrgClients.objects.get(client=client),
                    attr_level_guid=guid_generator(),
                    attr_level_default=default_flag,
                    attr_level_exclude=exclude_flag,
                    attribute_id=OrgAttributes.objects.get(attribute_id=current_attr['attribute_id']),
                    low=current_attr['value'],
                    version_number=1,
                    object_type='O',
                    attribute_value_desc=attribute_value_desc,
                    del_ind=False,
                    object_id=OrgModel.objects.get(object_id=attr_object_id))
            if current_attr['attribute_id'] == CONST_US_ROLE:
                global_variables.GLOBAL_SUB_MENU = {}
                global_variables.GLOBAL_SLIDE_MENU = {}
    return created


def save_attr_id_data_into_db(attr_id_data, attr_object_id,client):
    """

    :param kwargs:
    :return:
    """
    inherited_list = []
    current_attr_list = []
    inherited_exclude_save = []
    empty_array = []
    response = {}
    for attr_details in attr_id_data:
        if attr_details['inherit']:
            del attr_details['inherit']
            if int(attr_details['object_id']) == int(attr_object_id):
                inherited_exclude_save.append(attr_details)
            del attr_details['object_id']
            inherited_list.append(attr_details)
        else:
            del attr_details['object_id']
            del attr_details['inherit']
            current_attr_list.append(attr_details)
    current_attr_list = remove_duplicates_in_dic_list(current_attr_list)
    for curr_count, current_attr in enumerate(current_attr_list):
        for inherited_exclude_detail in inherited_exclude_save:
            if current_attr['value'] == inherited_exclude_detail['value']:
                if current_attr['attr_level_default'] == inherited_exclude_detail['attr_level_default']:
                    del current_attr_list[curr_count]
    # save node level attributes
    save_node_level_attr = save_attr_level_data(current_attr_list, inherited_list, attr_object_id,client)
    # save exclude in node level
    created = save_attr_level_data(inherited_exclude_save, empty_array, attr_object_id,client)

    # if attr_data['attribute_id'] == CONST_CAT_ID:
    #     trigger_org_notification(attr_data)
    if created:
        response['created'] = True

    else:
        response['created'] = False

    return attr_object_id


def get_attr_value_desc(attr_id, attr_value):
    """
    get description for attribute value
    """
    attr_val_desc = ''
    client = global_variables.GLOBAL_CLIENT
    if attr_id == CONST_ACC_CAT:
        if AccountAssignmentCategory.objects.filter(account_assign_cat=attr_value).exists():
            attr_val_desc = list(
                AccountAssignmentCategory.objects.filter(account_assign_cat=attr_value).values_list('description',
                                                                                                    flat=True))[0]
            return attr_val_desc
    if attr_id == CONST_CT_CTR:
        if AccountingDataDesc.objects.filter(client=client,
                                             account_assign_value=attr_value,
                                             account_assign_cat=CONST_CC).exists():
            attr_val_desc = list(AccountingDataDesc.objects.filter(client=client,
                                                                   account_assign_value=attr_value,
                                                                   account_assign_cat=CONST_CC).values_list(
                'description',
                flat=True))[0]
            return attr_val_desc
    if attr_id == CONST_WBS_ELEM:
        if AccountingDataDesc.objects.filter(client=client,
                                             account_assign_value=attr_value,
                                             account_assign_cat=CONST_WBS).exists():
            attr_val_desc = list(AccountingDataDesc.objects.filter(client=client,
                                                                   account_assign_value=attr_value,
                                                                   account_assign_cat=CONST_WBS).values_list(
                'description',
                flat=True))[0]
            return attr_val_desc
    if attr_id == CONST_INT_ORD:
        if AccountingDataDesc.objects.filter(client=client,
                                             account_assign_value=attr_value,
                                             account_assign_cat=CONST_OR).exists():
            attr_val_desc = list(AccountingDataDesc.objects.filter(client=client,
                                                                   account_assign_value=attr_value,
                                                                   account_assign_cat=CONST_OR).values_list(
                'description',
                flat=True))[0]
            return attr_val_desc
    if attr_id == CONST_AS_SET:
        if AccountingDataDesc.objects.filter(client=client,
                                             account_assign_value=attr_value,
                                             account_assign_cat=CONST_AS).exists():
            attr_val_desc = list(AccountingDataDesc.objects.filter(client=client,
                                                                   account_assign_value=attr_value,
                                                                   account_assign_cat=CONST_AS).values_list(
                'description',
                flat=True))[0]
            return attr_val_desc
    if attr_id == CONST_CO_CODE:
        if OrgCompanies.objects.filter(client=client,
                                       company_id=attr_value).exists():
            attr_val_desc = list(OrgCompanies.objects.filter(client=client,
                                                             company_id=attr_value).values_list('name1', flat=True))[0]
            return attr_val_desc
    if attr_id == CONST_DEF_DOC_SEARCH:
        if DocumentType.objects.filter(document_type=attr_value).exists():
            attr_val_desc = list(DocumentType.objects.filter(document_type=attr_value).values_list('document_type_desc',
                                                                                                   flat=True))[0]
            return attr_val_desc
    if attr_id == CONST_US_ROLE:
        if UserRoles.objects.filter(role=attr_value).exists():
            attr_val_desc = list(UserRoles.objects.filter(role=attr_value).values_list('role_desc', flat=True))[0]
            return attr_val_desc
    if attr_id == CONST_CAT_ID:
        if Catalogs.objects.filter(client=client,
                                   del_ind=False,
                                   catalog_id=attr_value).exists():
            attr_val_desc = list(Catalogs.objects.filter(client=client,
                                                         del_ind=False,
                                                         catalog_id=attr_value).values_list('description', flat=True))[
                0]
            return attr_val_desc
    if attr_id == CONST_SC_TRANS_TYPE:
        if TransactionTypes.objects.filter(client=client,
                                           del_ind=False,
                                           document_type=CONST_DOC_TYPE_SC,
                                           transaction_type=attr_value).exists():
            attr_val_desc = list(TransactionTypes.objects.filter(client=client,
                                                                 del_ind=False,
                                                                 document_type=CONST_DOC_TYPE_SC,
                                                                 transaction_type=attr_value).values_list('description',
                                                                                                          flat=True))[0]
            return attr_val_desc
    if attr_id == CONST_PO_TRANS_TYPE:
        if TransactionTypes.objects.filter(client=client,
                                           del_ind=False,
                                           document_type=CONST_DOC_TYPE_PO,
                                           transaction_type=attr_value).exists():
            attr_val_desc = list(TransactionTypes.objects.filter(client=client,
                                                                 del_ind=False,
                                                                 document_type=CONST_DOC_TYPE_PO,
                                                                 transaction_type=attr_value).values_list('description',
                                                                                                          flat=True))[0]
            return attr_val_desc
    if attr_id == CONST_FC_TRANS_TYPE:
        if TransactionTypes.objects.filter(document_type=CONST_DOC_TYPE_FC,
                                           client=client,
                                           del_ind=False,
                                           transaction_type=attr_value).exists():
            attr_val_desc = list(TransactionTypes.objects.filter(document_type=CONST_DOC_TYPE_FC,
                                                                 client=client,
                                                                 del_ind=False,
                                                                 transaction_type=attr_value).values_list('description',
                                                                                                          flat=True))[0]
            return attr_val_desc
    if attr_id == CONST_CALENDAR_ID:
        if CalenderConfig.objects.filter(client=client,
                                         del_ind=False,
                                         calender_id=attr_value).exists():
            attr_val_desc = list(CalenderConfig.objects.filter(client=client,
                                                               del_ind=False,
                                                               calender_id=attr_value).values_list('description',
                                                                                                   flat=True))[0]
            return attr_val_desc
    return None


def get_comp_code_drop_down(attr_object_id):
    """
    get company code drop down for porg and pgrp
    """
    org_comp_dropdown_list = []
    centralize_purch_level_flag = False
    parent_node_type_list = []
    node_type = list(OrgModel.objects.filter(object_id=attr_object_id,
                                             client=global_variables.GLOBAL_CLIENT,
                                             del_ind=False).values_list('node_type', flat=True))[0]
    purch_list = [CONST_PORG, CONST_PGROUP]
    if node_type in purch_list:
        obj_id_list = get_parents_obj_id(global_variables.GLOBAL_CLIENT, attr_object_id)
        org_model_details = list(OrgModel.objects.filter(object_id__in=obj_id_list,
                                                         client=global_variables.GLOBAL_CLIENT,
                                                         del_ind=False).values('node_type', 'object_id'))
        for org_model_detail in org_model_details:
            parent_node_type_list.append(org_model_detail['node_type'])
            if org_model_detail['node_type'] == CONST_COMPANY_CODE:
                # company code id for localized purchasing
                org_comp_dropdown_list = list(OrgCompanies.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                                                          del_ind=False,
                                                                          object_id=org_model_detail[
                                                                              'object_id']).values_list('company_id',
                                                                                                        flat=True))
        # company code id for centralize purchasing
        if not CONST_COMPANY_CODE in parent_node_type_list:
            org_comp_dropdown_list = list(OrgCompanies.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                                                      del_ind=False).values_list('company_id',
                                                                                                 flat=True))
            centralize_purch_level_flag = True
    return org_comp_dropdown_list, centralize_purch_level_flag


def get_attr_values_company_Code_list(client, attr_object_id):
    """

    """
    attr_detail = {}
    attr_value_list = get_attr_value_list(client, attr_object_id)

    attr_detail['attr_value_list'] = attr_value_list
    org_comp_dropdown_list, centralize_purch_level_flag = get_comp_code_drop_down(attr_object_id)
    attr_detail['org_comp_dropdown_list'] = org_comp_dropdown_list
    attr_detail['centralize_purch_level_flag'] = centralize_purch_level_flag

    return attr_detail


def delete_org_attributes_based_on_object_id(attribute_id, attr_object_id):
    """

    """
    attr_id_list = DjangoQueries.django_filter_only_query(OrgAttributesLevel,
                                                          {'attribute_id': attribute_id,
                                                           'object_id': attr_object_id})

    # Delete attr id based on selected node's object id
    for attr_data in attr_id_list:
        attr_data.delete()


def get_org_attribute_id_list(select_node_detail):
    """

    """
    attr_id = ''
    org_model_dictionary_list = {'object_id': select_node_detail['object_id'],
                                 'client': global_variables.GLOBAL_CLIENT}
    node_type = DjangoQueries.django_filter_value_list_query(OrgModel, org_model_dictionary_list, 'node_type')
    if node_type:
        node_type_detail = {'client': global_variables.GLOBAL_CLIENT,
                            'del_ind': False,
                            'node_type__in': node_type}

        node_type_list = DjangoQueries.django_filter_value_list_query(OrgModelNodetypeConfig,
                                                                      node_type_detail,
                                                                      'node_values')
        filter_dictionary = {'attribute_id__in': node_type_list}
        attr_id = DjangoQueries.django_filter_query(OrgAttributes, filter_dictionary, None, None)
    return attr_id


def save_extended_responsibility(save_ext_data):
    """

    """
    key_exit = checkKey(save_ext_data, 'low')
    attr_id_list = OrgAttributesLevel.objects.filter(attribute_id=save_ext_data[0]['attr_id'],
                                                     object_id=save_ext_data[0]['obj_id'])
    for attr_data in attr_id_list:
        attr_data.delete()
    if key_exit:
        for save_ext_attr in save_ext_data:
            extended_value = save_ext_attr['extended_value']
            created = OrgAttributesLevel.objects.create(
                client=OrgClients.objects.get(client=global_variables.GLOBAL_CLIENT),
                attr_level_guid=guid_generator(),
                attribute_id=OrgAttributes.objects.get(
                    attribute_id=save_ext_attr['attr_id']),
                low=save_ext_attr['low'],
                high=save_ext_attr['high'],
                version_number=1,
                extended_value=extended_value,
                object_type='O',
                del_ind=False,
                object_id=OrgModel.objects.get(
                    object_id=save_ext_attr['obj_id']))
