"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    user_settings_generic.py
Usage:
    generic function like
    1. get_object_id_list_user - Get login user and its parents obj id
    2. get_obj_id_parent_guid -Get parent's obj id and node guid by sending parent guid of child
    3. get_user_obj_id - Get login user's obj id
    4. get_user_obj_id_parent_guid - Get obj id and parent guid of login user
    5. get_attr_value_based_user_obj_id - Get OrgAttributesLevel low value based on login user obj id
    6. get_attr_value - Get OrgAttributesLevel low value based on login user and its parent obj id
    7. get_cc_obj_id - get company code object id from MMD_ORG_COMPANIES db table
    8. get_node_type_guid - get OrgNodeTypes object of requested node_type
    9. get_node_guid_from_obj_id - get OrgModel object of requested company code object id
    10. get_addr_number_guid - get OrgAddress object of requested address number
    11. get_ccode_guid - get OrgCompanies object of requested company code value

Author:
    Deepika K
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render

from eProc_Attributes.Utilities.attributes_generic import OrgAttributeValues
from eProc_Attributes.models.org_attribute_models import OrgAttributesLevel
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages import messages
from eProc_Basic.Utilities.messages.messages import *
from eProc_Configuration.models import UnspscCategoriesCustDesc, OrgCompanies, \
    OrgPorg, OrgPGroup, SupplierMaster
from eProc_Configuration.models.development_data import OrgNodeTypes
from eProc_Org_Model.models import OrgModel

django_query_instance = DjangoQueries()


def get_object_id_list_user(client, login_user_obj_id):
    """
    get login user and its parents obj id
    :param login_user_obj_id:
    :param client: login client no
    :return:list of obj id of user and its parent
    """
    array_obj_id = []
    user_obj_id, parent_guid = get_user_obj_id_parent_guid(client, login_user_obj_id)
    if user_obj_id:
        array_obj_id.append(user_obj_id)
        while parent_guid:
            obj_id, parent_guid = get_obj_id_parent_guid(parent_guid, client)
            array_obj_id.append(obj_id)

    return array_obj_id


def get_obj_id_parent_guid(parent_guid, client):
    """
    Get parent's obj id and node guid by sending parent guid of child
    :param parent_guid:parent_node_guid of child
    :param client: login client value
    :return: obj id and parent guid
    """

    org_detail = django_query_instance.django_filter_only_query(OrgModel, {
        'node_guid': parent_guid,
        'client': client
    }).values('object_id', 'parent_node_guid')

    for data in org_detail:
        parent_node_guid = data['parent_node_guid']
        obj_id = data['object_id']

    return obj_id, parent_node_guid


def get_user_obj_id(client, login_username):
    """
    get login user's obj id
    :param client: login client value
    :param login_username: login username
    :return: loin user's obj id
    """
    get_odj_id = None
    if django_query_instance.django_existence_check(OrgModel, {'name': login_username, 'client': client}):
        org_model = django_query_instance.django_get_query(OrgModel, {'name': login_username, 'client': client})

        get_odj_id = org_model.object_id
    return get_odj_id


def get_user_obj_id_parent_guid(client, login_user_obj_id):
    """
    Get obj id and parent guid of login user
    :param client: login client value
    :param login_user_obj_id: login login_user_obj_id
    :return: obj id and parent guid of login user
    """
    get_odj_id = None
    parent_node = None

    if django_query_instance.django_existence_check(OrgModel, {'object_id': login_user_obj_id, 'client': client}):
        org_model = django_query_instance.django_get_query(OrgModel, {'object_id': login_user_obj_id, 'client': client})

        get_odj_id = org_model.object_id
        parent_node = org_model.parent_node_guid

    return get_odj_id, parent_node


def get_attr_value_based_user_obj_id(client, attr_id, object_id, edit_flag):
    """
    Get OrgAttributesLevel low value based on login user obj id
    :param client: log in client value
    :param attr_id: attribute id
    :param object_id: object id of login user
    :return: OrgAttributes low value list
    """
    attr_low_value = []
    if edit_flag:
        asc_data = OrgAttributesLevel.objects.values_list('low',
                                                          'attr_level_default',
                                                          flat=False).filter(Q(object_id=object_id,
                                                                               client=client,
                                                                               attribute_id=attr_id)).order_by(
            'object_id')
        for low, default_value in asc_data:
            if default_value:
                attr_low_value.insert(0, low)
            else:
                attr_low_value.append(low)
    else:
        default_attr_value = django_query_instance.django_filter_only_query(OrgAttributesLevel, {
            'object_id': object_id,
            'client': client,
            'attribute_id': attr_id,
            'attr_level_default': True
        }).values('low')

        for default_attr in default_attr_value:
            attr_low_value = default_attr['low']

    return attr_low_value


def get_attr_value(client, attr_id, object_id, edit_flag):
    """
    get attribute values of the user
    :param edit_flag:
    :param client: log in client value
    :param attr_id: attribute id
    :param object_id: object id of login user
    :return: OrgAttributes low value list
    """
    acc_asign_cat = []
    if edit_flag:
        acc_asign_cat = OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(object_id,attr_id)[0]

    else:
        acc_asign_cat = OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(object_id, attr_id)[1]

    return acc_asign_cat


def get_cc_obj_id(default_cc, client):
    """
    get company code object id from MMD_ORG_COMPANIES db table
    :param default_cc:company code id
    :param client: get login client no
    :return:object id of cc
    """
    cmp_obj_id = []
    cc_obj_id = django_query_instance.django_filter_only_query(OrgCompanies, {
        'company_id': default_cc, 'client': client
    }).values('object_id')

    for ccobj_id in cc_obj_id:
        cmp_obj_id = ccobj_id['object_id']

    return cmp_obj_id


def get_node_type_guid(client, node_type):
    """
    get OrgNodeTypes object of requested node_type
    :param client: loin client
    :param node_type: node type
    :return: node type guid
    """
    node_type_guid = None

    if django_query_instance.django_existence_check(OrgNodeTypes, {'node_type': node_type, 'client': client}):

        node_type_guid = django_query_instance.django_get_query(OrgNodeTypes,
                                                                {'node_type': node_type, 'client': client})

    else:
        return node_type_guid
    return node_type_guid


def get_node_guid_from_obj_id(client, cc_obj_id):
    """
    get OrgModel object of requested company code object id
    :param cc_obj_id: object id
    :param client: login client value
    :return: object of requested object id
    """
    org_object = None
    if django_query_instance.django_existence_check(OrgModel, {
        'object_id': cc_obj_id, 'client': client
    }):

        org_object = django_query_instance.django_get_query(OrgModel, {
            'object_id': cc_obj_id, 'client': client
        })
    else:
        return org_object
    return org_object


def get_prod_cat_desc_count(unique_unspsc_list):
    """

    :param unique_unspsc_list:
    :return:
    """
    unspsc_info = []
    for key, val in unique_unspsc_list.items():
        print(key)
        unspsc_detail = {}
        print(key)
        unspsc_detail['prod_cat'] = django_query_instance.django_filter_value_list_query(UnspscCategoriesCustDesc, {
            'client': global_variables.GLOBAL_CLIENT, 'del_ind': False, 'prod_cat_id': key
        }, 'category_desc')[0]

        unspsc_detail['prod_cat_id'] = key
        unspsc_detail['prod_cat_count'] = val
        unspsc_info.append(unspsc_detail)
    return unspsc_info


def get_supp_desc_count(supp_count):
    """

    :param supp_count:
    :return:
    """
    supp_info = []
    for key, val in supp_count.items():
        supp_detail = {}

        try:
            supp_detail['supplier'] = django_query_instance.django_filter_value_list_query(SupplierMaster, {
                'client': global_variables.GLOBAL_CLIENT, 'del_ind': False, 'supplier_id': key
            }, 'name1')[0]

            supp_detail['supplier_id'] = key
            supp_detail['supp_count'] = val
            supp_info.append(supp_detail)
        except Exception as e:
            print(e)
    return supp_info


def get_company_code_desc_append(cocode_list, default_cocode):
    """

    """
    company_code_drop_down = []
    default_cmp_code_desc = []

    cmp_code_desc = django_query_instance.django_filter_only_query(OrgCompanies, {
        'company_id__in': cocode_list,
        'client': global_variables.GLOBAL_CLIENT,
        'del_ind': False
    }).values('name1', 'company_id')
    for cmp_code in cmp_code_desc:
        if cmp_code['company_id'] == default_cocode:
            default_cmp_code_desc.append(cmp_code['company_id'] + ' - ' + cmp_code['name1'])
        company_code_description = cmp_code['company_id'] + ' - ' + cmp_code['name1']
        company_detail_dictionary = {'company_code_description': company_code_description,
                                     'company_id': cmp_code['company_id']}
        company_code_drop_down.append(company_detail_dictionary)
    company_code_dictionay_list = {'cmp_code_list': cocode_list,
                                   'cmp_code_desc_list': company_code_drop_down,
                                   'default_cmp_code': default_cocode,
                                   'default_cmp_code_desc': default_cmp_code_desc}
    return cocode_list, company_code_drop_down


def get_purch_org_detail(default_company_code):
    """

    """
    purchase_org_list = []
    purchase_org_details = []

    porg_details_query = django_query_instance.django_filter_only_query(OrgPorg, {
        'company_id': default_company_code,
        'client': global_variables.GLOBAL_CLIENT,
        'del_ind': False
    }).values('porg_id', 'description', 'company_id')

    for purch_org_detail in porg_details_query:
        porg_detail = {}
        purchase_org_list.append(purch_org_detail['porg_id'])
        porg_description = purch_org_detail['porg_id'] + ' - ' + purch_org_detail['description']
        porg_detail = {'porg_description': porg_description,
                       'porg_id': purch_org_detail['porg_id']
                       }
        purchase_org_details.append(porg_detail)

    return purchase_org_list, purchase_org_details


def get_purch_group_detail(default_purchase_org):
    """

    """
    purchase_group_details = []
    pgroup_details_query = django_query_instance.django_filter_only_query(OrgPGroup, {
        'porg_id': default_purchase_org,
        'client': global_variables.GLOBAL_CLIENT,
        'del_ind': False
    }).values('pgroup_id', 'description', 'porg_id')

    for purch_group_detail in pgroup_details_query:
        pgroup_description = purch_group_detail['pgroup_id'] + ' - ' + purch_group_detail['description']
        pgroup_detail = {'pgroup_description': pgroup_description,
                         'pgroup_id': purch_group_detail['pgroup_id']}
        purchase_group_details.append(pgroup_detail)

    return purchase_group_details
