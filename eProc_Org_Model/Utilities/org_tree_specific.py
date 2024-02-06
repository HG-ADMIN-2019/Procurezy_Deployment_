from django.shortcuts import get_object_or_404

from eProc_Attributes.Utilities.attributes_specific import get_attr_values_company_Code_list
from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import OrgPGroup, OrgPorg, OrgCompanies
from eProc_Configuration.models.development_data import OrgNodeTypes
from eProc_Configuration.models.master_data import OrgPorgMapping
from eProc_Org_Model.Utilities.org_specific import get_porg_id_by_pgrp
from eProc_Org_Model.models import OrgModel
from eProc_Registration.models import UserData

django_query_instance = DjangoQueries()


def get_org_model_attr_detail(object_id):
    """

    """
    basic_node_detail = {}
    node_type_desc = ''
    basic_org_details = {}
    org_model_query = {'client': global_variables.GLOBAL_CLIENT,
                       'object_id': object_id}
    if DjangoQueries().django_existence_check(OrgModel, org_model_query):
        basic_data = DjangoQueries().django_get_query(OrgModel, org_model_query)
        if DjangoQueries().django_existence_check(OrgNodeTypes, {'node_type': basic_data.node_type,
                                                                 'client': global_variables.GLOBAL_CLIENT}):
            node_type_desc = \
            DjangoQueries().django_filter_value_list_query(OrgNodeTypes, {'node_type': basic_data.node_type,
                                                                          'client': global_variables.GLOBAL_CLIENT},
                                                           'description')[0]
        node_type = basic_data.node_type
        object_id = basic_data.object_id
        basic_node_details = get_basic_node_details(node_type, object_id)
        porg_id = get_porg_id_by_pgrp(object_id)
        attr_detail = get_attr_values_company_Code_list(global_variables.GLOBAL_CLIENT, object_id)
        porg_mapping_details = get_porg_mapping(object_id)
        basic_node = {'node_type': node_type,
                      'node_type_desc': node_type_desc,
                      'object_id': object_id,
                      'node_desc': basic_data.name,
                      'porg_id':porg_id
                      }
        basic_org_details = {'basic_node': basic_node,
                             'basic_node_details': basic_node_details,
                             'attr_detail': attr_detail,
                             'porg_mapping_details':porg_mapping_details
                             }
    return basic_org_details


def get_basic_node_details(node_type, object_id):
    """

    """
    sel = {'client': global_variables.GLOBAL_CLIENT,'del_ind':False}
    obj = ''
    node_det = {}
    if node_type == CONST_RNODE or node_type == CONST_NODE:
        return []
    elif node_type == CONST_COMPANY_CODE:
        obj = OrgCompanies
        if obj.objects.filter(object_id=object_id).exists():
            sel['object_id'] = object_id
        else:
            sel['object_id__isnull'] = True
        node_det = list(obj.objects.filter(**sel).values('object_id',
                                                         'name1',
                                                         'name2',
                                                         'company_id'))
        return node_det
    elif node_type == CONST_PORG:
        obj = OrgPorg
        if obj.objects.filter(object_id=object_id).exists():
            sel['object_id'] = object_id
        else:
            sel['object_id__isnull'] = True
        node_det = list(obj.objects.filter(**sel).values('porg_id',
                                                         'description',
                                                         'object_id'))
        return node_det
    elif node_type == CONST_PGROUP:
        obj = OrgPGroup
        if obj.objects.filter(object_id=object_id).exists():
            sel['object_id'] = object_id
        else:
            sel['object_id__isnull'] = True
        node_det = list(obj.objects.filter(**sel).values('pgroup_id',
                                                         'description',
                                                         'object_id',
                                                         'porg_id'))
        return node_det
    elif node_type == CONST_USER:
        obj = UserData
        sel['object_id'] = object_id
        node_det = list(obj.objects.filter(**sel).values())
        return node_det
    return [node_det]


def get_porg_mapping(object_id):
    """

    """
    porg_mapping_details = django_query_instance.django_filter_query(OrgPorgMapping,
                                                                     {'client': global_variables.GLOBAL_CLIENT,
                                                                      'object_id': object_id}, None,
                                                                     ['porg_id', 'company_id', 'object_id'])

    return porg_mapping_details
