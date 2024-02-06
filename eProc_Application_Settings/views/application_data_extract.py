import csv

from django.http import HttpResponse
from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.update_del_ind import query_update_del_ind
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import OrgNodeTypes, OrgAttributes, UserRoles, AuthorizationObject, Authorization, \
    AuthorizationGroup, MessagesId, MessagesIdDesc, OrgModelNodetypeConfig, NumberRanges, \
    PoSplitType, PoSplitCriteria, TransactionTypes, PurchaseControl, AccountAssignmentCategory, SourcingRule, \
    SourcingMapping

django_query_instance = DjangoQueries()


def extract_node_type_data(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_ORG_NODE_TYPES_CSV

    writer = csv.writer(response)
    writer.writerow(['NODE_TYPE', 'DESCRIPTION', 'del_ind'])

    org_node_types = django_query_instance.django_filter_query(OrgNodeTypes,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT}, None,
                                                               ['node_type', 'description', 'del_ind'])
    org_node_types = query_update_del_ind(org_node_types)

    for org_node_type in org_node_types:
        org_node_type_info = [org_node_type['node_type'], org_node_type['description'],
                              org_node_type['del_ind']]
        writer.writerow(org_node_type_info)

    return response


def extract_attributes_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_ORG_ATTRIBUTES_CSV

    writer = csv.writer(response)
    writer.writerow(
        ['ATTRIBUTE_ID', 'ATTRIBUTE_NAME', 'RANGE_INDICATOR', 'MULTIPLE_VALUE', 'ALLOW_DEFAULTS', 'INHERIT_VALUES',
         'MAXIMUM_LENGTH', 'del_ind'])

    attributes = django_query_instance.django_filter_query(OrgAttributes,
                                                           {'del_ind': False}, None,
                                                           ['attribute_id', 'attribute_name', 'range_indicator',
                                                            'multiple_value', 'allow_defaults', 'inherit_values',
                                                            'maximum_length', 'del_ind'])
    attributes = query_update_del_ind(attributes)

    for attribute in attributes:
        if attribute['range_indicator']:
            attribute['range_indicator'] = 1
        else:
            attribute['range_indicator'] = 0
        if attribute['multiple_value']:
            attribute['multiple_value'] = 1
        else:
            attribute['multiple_value'] = 0
        if attribute['allow_defaults']:
            attribute['allow_defaults'] = 1
        else:
            attribute['allow_defaults'] = 0
        if attribute['inherit_values']:
            attribute['inherit_values'] = 1
        else:
            attribute['inherit_values'] = 0
        attributes_info = [attribute['attribute_id'], attribute['attribute_name'], attribute['range_indicator'],
                           attribute['multiple_value'], attribute['allow_defaults'], attribute['inherit_values'],
                           attribute['maximum_length'], attribute['del_ind']]
        writer.writerow(attributes_info)

    return response


def extract_node_level_attributes_data(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_ORG_NODE_LEVEL_ATTRIBUTES_CSV

    writer = csv.writer(response)
    writer.writerow(['NODE_TYPES', 'NODE_VALUES', 'del_ind'])

    org_node_level_attributes_data = django_query_instance.django_filter_query(OrgModelNodetypeConfig,
                                                                               {'del_ind': False,
                                                                                'client': global_variables.GLOBAL_CLIENT},
                                                                               None,
                                                                               ['node_type',
                                                                                'node_values',
                                                                                'del_ind'])
    org_node_level_attributes_types = query_update_del_ind(org_node_level_attributes_data)

    for org_node_level_attributes_type in org_node_level_attributes_types:
        org_node_level_attributes_info = [org_node_level_attributes_type['node_type'],
                                          org_node_level_attributes_type['node_values'],
                                          org_node_level_attributes_type['del_ind']]
        writer.writerow(org_node_level_attributes_info)

    return response


def extract_account_assignment_category_data(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_ACCOUNT_ASSIGNMENT_CATEGORY_CSV

    writer = csv.writer(response)
    writer.writerow(['ACCOUNT_ASSIGN_CAT', 'DESCRIPTION', 'del_ind'])

    account_assignment_category_data = django_query_instance.django_filter_query(AccountAssignmentCategory,
                                                                                 {'del_ind': False}, None,
                                                                                 ['account_assign_cat',
                                                                                  'description',
                                                                                  'del_ind'])
    account_assignment_category_types = query_update_del_ind(account_assignment_category_data)

    for account_assignment_category_type in account_assignment_category_types:
        account_assignment_category_info = [account_assignment_category_type['account_assign_cat'],
                                            account_assignment_category_type['description'],
                                            account_assignment_category_type['del_ind']]
        writer.writerow(account_assignment_category_info)

    return response


def extract_favourite_cart_number_range_data(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_FAVOURITE_CART_NUMBER_RANGE_CSV

    writer = csv.writer(response)
    writer.writerow(['SEQUENCE', 'STARTING', 'ENDING', 'CURRENT', 'del_ind'])

    favourite_cart_number_range_data = django_query_instance.django_filter_query(NumberRanges,
                                                                                 {'del_ind': False,
                                                                                  'client': global_variables.GLOBAL_CLIENT,
                                                                                  'document_type': CONST_DOC_TYPE_FC
                                                                                  }, None,
                                                                                 ['sequence', 'starting', 'ending',
                                                                                  'current', 'del_ind'])
    favourite_cart_number_range_data = query_update_del_ind(favourite_cart_number_range_data)

    for favourite_cart_number_range_type in favourite_cart_number_range_data:
        favourite_cart_number_range_type_info = [favourite_cart_number_range_type['sequence'],
                                                 favourite_cart_number_range_type['starting'],
                                                 favourite_cart_number_range_type['ending'],
                                                 favourite_cart_number_range_type['current'],
                                                 favourite_cart_number_range_type['del_ind']]
        writer.writerow(favourite_cart_number_range_type_info)

    return response


def extract_shopping_cart_number_range_data(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_SHOPPING_CART_NUMBER_RANGE_CSV

    writer = csv.writer(response)
    writer.writerow(['SEQUENCE', 'STARTING', 'ENDING', 'CURRENT', 'del_ind'])

    shopping_cart_number_range_data = django_query_instance.django_filter_query(NumberRanges,
                                                                                {'del_ind': False,
                                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                                 'document_type': CONST_DOC_TYPE_SC
                                                                                 }, None,
                                                                                ['sequence', 'starting', 'ending',
                                                                                 'current', 'del_ind'])
    shopping_cart_number_range_data = query_update_del_ind(shopping_cart_number_range_data)

    for shopping_cart_number_range_type in shopping_cart_number_range_data:
        shopping_cart_number_range_type_info = [shopping_cart_number_range_type['sequence'],
                                                shopping_cart_number_range_type['starting'],
                                                shopping_cart_number_range_type['ending'],
                                                shopping_cart_number_range_type['current'],
                                                shopping_cart_number_range_type['del_ind']]
        writer.writerow(shopping_cart_number_range_type_info)

    return response


def extract_purchase_order_number_range_data(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_PURCHASE_ORDER_NUMBER_RANGE_CSV

    writer = csv.writer(response)
    writer.writerow(['SEQUENCE', 'STARTING', 'ENDING', 'CURRENT', 'del_ind'])

    purchase_order_number_range_data = django_query_instance.django_filter_query(NumberRanges,
                                                                                 {'del_ind': False,
                                                                                  'client': global_variables.GLOBAL_CLIENT,
                                                                                  'document_type': CONST_DOC_TYPE_PO
                                                                                  }, None,
                                                                                 ['sequence', 'starting', 'ending',
                                                                                  'current', 'del_ind'])
    purchase_order_number_range_data = query_update_del_ind(purchase_order_number_range_data)

    for purchase_order_number_range_type in purchase_order_number_range_data:
        purchase_order_number_range_type_info = [purchase_order_number_range_type['sequence'],
                                                 purchase_order_number_range_type['starting'],
                                                 purchase_order_number_range_type['ending'],
                                                 purchase_order_number_range_type['current'],
                                                 purchase_order_number_range_type['del_ind']]
        writer.writerow(purchase_order_number_range_type_info)

    return response


def extract_goods_verification_number_range_data(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_GOODS_VERIFICATION_NUMBER_RANGE_CSV

    writer = csv.writer(response)
    writer.writerow(['SEQUENCE', 'STARTING', 'ENDING', 'CURRENT', 'del_ind'])

    goods_verification_number_range_data = django_query_instance.django_filter_query(NumberRanges,
                                                                                     {'del_ind': False,
                                                                                      'client': global_variables.GLOBAL_CLIENT,
                                                                                      'document_type': CONST_DOC_TYPE_CONF
                                                                                      }, None,
                                                                                     ['sequence', 'starting', 'ending',
                                                                                      'current', 'del_ind'])
    goods_verification_number_range_data = query_update_del_ind(goods_verification_number_range_data)

    for goods_verification_number_range_type in goods_verification_number_range_data:
        goods_verification_number_range_type_info = [goods_verification_number_range_type['sequence'],
                                                     goods_verification_number_range_type['starting'],
                                                     goods_verification_number_range_type['ending'],
                                                     goods_verification_number_range_type['current'],
                                                     goods_verification_number_range_type['del_ind']]
        writer.writerow(goods_verification_number_range_type_info)

    return response


def extract_favourite_transaction_type_data(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_FAVOURITE_TRANSACTION_TYPE_CSV

    writer = csv.writer(response)
    writer.writerow(['TRANSACTION_TYPE', 'DESCRIPTION', 'DOCUMENT_TYPE', 'SEQUENCE', 'ACTIVE_INACTIVE', 'del_ind'])

    favourite_transaction_type_data = django_query_instance.django_filter_query(TransactionTypes,
                                                                                {'del_ind': False,
                                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                                 'document_type': "DOC04"
                                                                                 }, None,
                                                                                ['transaction_type', 'description',
                                                                                 'document_type',
                                                                                 'sequence', 'active_inactive',
                                                                                 'del_ind'])
    favourite_transaction_type_data = query_update_del_ind(favourite_transaction_type_data)

    for favourite_transaction_type in favourite_transaction_type_data:
        favourite_transaction_type_info = [favourite_transaction_type['transaction_type'],
                                           favourite_transaction_type['description'],
                                           favourite_transaction_type['document_type'],
                                           favourite_transaction_type['sequence'],
                                           favourite_transaction_type['active_inactive'],
                                           favourite_transaction_type['del_ind']]
        writer.writerow(favourite_transaction_type_info)

    return response


def extract_shopping_cart_transaction_type_data(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_SHOPPING_CART_TRANSACTION_TYPE_CSV

    writer = csv.writer(response)
    writer.writerow(['TRANSACTION_TYPE', 'DESCRIPTION', 'DOCUMENT_TYPE', 'SEQUENCE', 'ACTIVE_INACTIVE', 'del_ind'])

    shopping_cart_transaction_type_data = django_query_instance.django_filter_query(TransactionTypes,
                                                                                    {'del_ind': False,
                                                                                     'client': global_variables.GLOBAL_CLIENT,
                                                                                     'document_type': "DOC01"
                                                                                     }, None,
                                                                                    ['transaction_type', 'description',
                                                                                     'document_type',
                                                                                     'sequence', 'active_inactive',
                                                                                     'del_ind'])
    shopping_cart_transaction_type_data = query_update_del_ind(shopping_cart_transaction_type_data)

    for shopping_cart_transaction_type in shopping_cart_transaction_type_data:
        shopping_cart_transaction_type_info = [shopping_cart_transaction_type['transaction_type'],
                                               shopping_cart_transaction_type['description'],
                                               shopping_cart_transaction_type['document_type'],
                                               shopping_cart_transaction_type['sequence'],
                                               shopping_cart_transaction_type['active_inactive'],
                                               shopping_cart_transaction_type['del_ind']]
        writer.writerow(shopping_cart_transaction_type_info)

    return response


def extract_purchase_order_transaction_type_data(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_PURCHASE_ORDER_TRANSACTION_TYPE_CSV

    writer = csv.writer(response)
    writer.writerow(['TRANSACTION_TYPE', 'DESCRIPTION', 'DOCUMENT_TYPE', 'SEQUENCE', 'ACTIVE_INACTIVE', 'del_ind'])

    purchase_order_transaction_type_data = django_query_instance.django_filter_query(TransactionTypes,
                                                                                     {'del_ind': False,
                                                                                      'client': global_variables.GLOBAL_CLIENT,
                                                                                      'document_type': "DOC02"
                                                                                      }, None,
                                                                                     ['transaction_type', 'description',
                                                                                      'document_type',
                                                                                      'sequence', 'active_inactive',
                                                                                      'del_ind'])
    purchase_order_transaction_type_data = query_update_del_ind(purchase_order_transaction_type_data)

    for purchase_order_transaction_type in purchase_order_transaction_type_data:
        purchase_order_transaction_type_info = [purchase_order_transaction_type['transaction_type'],
                                                purchase_order_transaction_type['description'],
                                                purchase_order_transaction_type['document_type'],
                                                purchase_order_transaction_type['sequence'],
                                                purchase_order_transaction_type['active_inactive'],
                                                purchase_order_transaction_type['del_ind']]
        writer.writerow(purchase_order_transaction_type_info)

    return response


def extract_goods_verification_transaction_type_data(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_GOODS_VERIFICATION_TRANSACTION_TYPE_CSV

    writer = csv.writer(response)
    writer.writerow(['TRANSACTION_TYPE', 'DESCRIPTION', 'DOCUMENT_TYPE', 'SEQUENCE', 'ACTIVE_INACTIVE', 'del_ind'])

    goods_verification_transaction_type_data = django_query_instance.django_filter_query(TransactionTypes,
                                                                                         {'del_ind': False,
                                                                                          'client': global_variables.GLOBAL_CLIENT,
                                                                                          'document_type': "DOC03"
                                                                                          }, None,
                                                                                         ['transaction_type',
                                                                                          'description',
                                                                                          'document_type',
                                                                                          'sequence', 'active_inactive',
                                                                                          'del_ind'])
    goods_verification_transaction_type_data = query_update_del_ind(goods_verification_transaction_type_data)

    for goods_verification_transaction_type in goods_verification_transaction_type_data:
        goods_verification_transaction_type_info = [goods_verification_transaction_type['transaction_type'],
                                                    goods_verification_transaction_type['description'],
                                                    goods_verification_transaction_type['document_type'],
                                                    goods_verification_transaction_type['sequence'],
                                                    goods_verification_transaction_type['active_inactive'],
                                                    goods_verification_transaction_type['del_ind']]
        writer.writerow(goods_verification_transaction_type_info)

    return response


def extract_po_split_type_data(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_PO_SPLIT_TYPE_CSV

    writer = csv.writer(response)
    writer.writerow(['PO_SPLIT_TYPE', 'PO_SPLIT_TYPE_DESC', 'del_ind'])

    po_split_type_data = django_query_instance.django_filter_query(PoSplitType,
                                                                   {'del_ind': False,
                                                                    }, None,
                                                                   ['po_split_type', 'po_split_type_desc', 'del_ind'])
    po_split_type_data = query_update_del_ind(po_split_type_data)

    for po_split_type in po_split_type_data:
        po_split_type_info = [po_split_type['po_split_type'],
                              po_split_type['po_split_type_desc'],
                              po_split_type['del_ind']]
        writer.writerow(po_split_type_info)

    return response


def extract_po_split_criteria_data(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_PO_SPLIT_CRITERIA_CSV

    writer = csv.writer(response)
    writer.writerow(['PO_SPLIT_TYPE', 'COMPANY_CODE_ID', 'ACTIVATE', 'del_ind'])

    po_split_criteria_data = django_query_instance.django_filter_query(PoSplitCriteria,
                                                                       {'del_ind': False,
                                                                        'client': global_variables.GLOBAL_CLIENT,
                                                                        }, None,
                                                                       ['po_split_type', 'company_code_id', 'activate',
                                                                        'del_ind'])
    po_split_criteria_data = query_update_del_ind(po_split_criteria_data)

    for po_split_criteria_type in po_split_criteria_data:
        po_split_criteria_info = [po_split_criteria_type['po_split_type'],
                                  po_split_criteria_type['company_code_id'],
                                  po_split_criteria_type['activate'],
                                  po_split_criteria_type['del_ind']]
        writer.writerow(po_split_criteria_info)

    return response


def extract_purchase_control_data(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_PURCHASE_CONTROL_CSV

    writer = csv.writer(response)
    writer.writerow(['company_code_id', 'call_off', 'purchase_ctrl_flag', 'del_ind'])

    purchase_control_data = django_query_instance.django_filter_query(PurchaseControl,
                                                                      {'del_ind': False,
                                                                       'client': global_variables.GLOBAL_CLIENT,
                                                                       }, None,
                                                                      ['company_code_id', 'call_off',
                                                                       'purchase_ctrl_flag',
                                                                       'del_ind'])
    purchase_control_data = query_update_del_ind(purchase_control_data)

    for purchase_control_type in purchase_control_data:
        purchase_control_info = [purchase_control_type['company_code_id'],
                                 purchase_control_type['call_off'],
                                 purchase_control_type['purchase_ctrl_flag'],
                                 purchase_control_type['del_ind']]
        writer.writerow(purchase_control_info)

    return response


def extract_source_rule_data(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_SOURCE_RULE_CSV

    writer = csv.writer(response)
    writer.writerow(['prod_cat_id_from', 'prod_cat_id_to', 'company_id', 'call_off', 'rule_type', 'sourcing_flag',
                     'del_ind'])

    source_rule_data = django_query_instance.django_filter_query(SourcingRule,
                                                                 {'del_ind': False,
                                                                  'client': global_variables.GLOBAL_CLIENT,
                                                                  }, None,
                                                                 ['prod_cat_id_from', 'prod_cat_id_to',
                                                                  'company_id', 'call_off', 'rule_type',
                                                                  'sourcing_flag', 'del_ind'])
    source_rule_data = query_update_del_ind(source_rule_data)

    for source_rule_type in source_rule_data:
        source_rule_info = [source_rule_type['prod_cat_id_from'], source_rule_type['prod_cat_id_to'],
                            source_rule_type['company_id'], source_rule_type['call_off'], source_rule_type['rule_type'],
                            source_rule_type['sourcing_flag'], source_rule_type['del_ind']]
        writer.writerow(source_rule_info)

    return response


def extract_source_mapping_data(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_SOURCE_MAPPING_CSV

    writer = csv.writer(response)
    writer.writerow(['prod_cat_id', 'company_id', 'rule_type', 'product_id', 'del_ind'])

    source_mapping_data = django_query_instance.django_filter_query(SourcingMapping,
                                                                    {'del_ind': False,
                                                                     'client': global_variables.GLOBAL_CLIENT,
                                                                     }, None,
                                                                    ['prod_cat_id', 'company_id', 'rule_type',
                                                                     'product_id', 'del_ind'])
    source_mapping_data = query_update_del_ind(source_mapping_data)

    for source_map_type in source_mapping_data:
        source_map_info = [source_map_type['prod_cat_id'], source_map_type['company_id'],
                           source_map_type['rule_type'], source_map_type['product_id'], source_map_type['del_ind']]
        writer.writerow(source_map_info)

    return response


def extract_user_role_data(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_USER_ROLES_CSV

    writer = csv.writer(response)
    writer.writerow(['ROLES', 'ROLE_DESC', 'del_ind'])

    user_roles = django_query_instance.django_filter_query(UserRoles,
                                                           {'del_ind': False,
                                                            }, None,
                                                           ['role', 'role_desc', 'del_ind'])
    user_roles = query_update_del_ind(user_roles)

    for user_role in user_roles:
        user_role_info = [user_role['role'], user_role['role_desc'],
                          user_role['del_ind']]
        writer.writerow(user_role_info)

    return response


def extract_authorization_object_data(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_AUTHORIZATION_OBJECT

    writer = csv.writer(response)
    writer.writerow(['AUTH_OBJ_ID', 'AUTH_LEVEL', 'AUTH_LEVEL_ID', 'AUTH_LEVEL_DESC', 'del_ind'])

    auth_obj = django_query_instance.django_filter_query(AuthorizationObject,
                                                         {'del_ind': False,
                                                          }, None,
                                                         ['auth_obj_id', 'auth_level', 'auth_level_ID',
                                                          'auth_level_desc', 'del_ind'])
    auth_objs = query_update_del_ind(auth_obj)

    for auth_obj in auth_objs:
        auth_obj_info = [auth_obj['auth_obj_id'], auth_obj['auth_level'],
                         auth_obj['auth_level_ID'], auth_obj['auth_level_desc'],
                         auth_obj['del_ind']]
        writer.writerow(auth_obj_info)

    return response


def extract_authorization_data(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_AUTHORIZATION

    writer = csv.writer(response)
    writer.writerow(['ROLE', 'AUTH_OBJ_GRP', 'del_ind'])

    auth_obj = django_query_instance.django_filter_query(Authorization,
                                                         {'del_ind': False,
                                                          'client': global_variables.GLOBAL_CLIENT
                                                          }, None,
                                                         ['role', 'auth_obj_grp',
                                                          'del_ind'])
    auth_objs = query_update_del_ind(auth_obj)

    for auth_obj in auth_objs:
        auth_obj_info = [auth_obj['role'], auth_obj['auth_obj_grp'],
                         auth_obj['del_ind']]
        writer.writerow(auth_obj_info)

    return response


def extract_attributes_group_data(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_AUTHORIZATION_GROUP

    writer = csv.writer(response)
    writer.writerow(['AUTH_OBJ_GRP', 'AUTH_GRP_DESC', 'AUTH_LEVEL', 'AUTH_OBJ_ID',
                     'del_ind'])

    auth_grps = django_query_instance.django_filter_query(AuthorizationGroup,
                                                          {'del_ind': False,
                                                           }, None,
                                                          ['auth_obj_grp', 'auth_grp_desc', 'auth_level', 'auth_obj_id',
                                                           'del_ind'])
    auth_grps = query_update_del_ind(auth_grps)

    for auth_grp in auth_grps:
        auth_obj_info = [auth_grp['auth_obj_grp'], auth_grp['auth_grp_desc'],
                         auth_grp['auth_level'], auth_grp['auth_obj_id'], auth_grp['del_ind']]
        writer.writerow(auth_obj_info)

    return response


def extract_message_id_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_MESSAGE_ID_CSV

    writer = csv.writer(response)
    writer.writerow(['MESSAGES_ID', 'MESSAGES_TYPE',
                     'del_ind'])

    message_id_details = django_query_instance.django_filter_query(MessagesId,
                                                                   {'del_ind': False,
                                                                    'client': global_variables.GLOBAL_CLIENT,
                                                                    }, None,
                                                                   ['messages_id', 'messages_type',
                                                                    'del_ind'])
    message_id_details = query_update_del_ind(message_id_details)

    for message_id_detail in message_id_details:
        message_id_info = [message_id_detail['messages_id'], message_id_detail['messages_type'],
                           message_id_detail['del_ind']]
        writer.writerow(message_id_info)

    return response


def extract_message_id_desc_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_MESSAGE_ID_DESC_CSV

    writer = csv.writer(response)
    writer.writerow(['MESSAGES_ID', 'MESSAGES_ID_DESC', 'MESSAGES_CATEGORY', 'LANGUAGE_ID'
                                                                             'del_ind'])

    message_id_details = django_query_instance.django_filter_query(MessagesIdDesc,
                                                                   {'del_ind': False,
                                                                    'client': global_variables.GLOBAL_CLIENT,
                                                                    }, None,
                                                                   ['messages_id', 'messages_id_desc',
                                                                    'messages_category', 'language_id',
                                                                    'del_ind'])
    message_id_details = query_update_del_ind(message_id_details)

    for message_id_detail in message_id_details:
        message_id_info = [message_id_detail['messages_id'], message_id_detail['messages_id_desc'],
                           message_id_detail['messages_category'], message_id_detail['language_id'],
                           message_id_detail['del_ind']]
        writer.writerow(message_id_info)

    return response
