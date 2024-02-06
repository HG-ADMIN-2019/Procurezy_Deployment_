from eProc_Basic.Utilities.constants.constants import CONST_CC, CONST_WBS, CONST_OR, CONST_AS, CONST_ALL
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import UnitOfMeasures, AccountAssignmentCategory, AccountingDataDesc

django_query_instance = DjangoQueries()


def get_description_uom(uom):
    """

    """
    if django_query_instance.django_existence_check(UnitOfMeasures,
                                                    {'uom_id': uom}):
        uom = django_query_instance.django_filter_value_list_query(UnitOfMeasures,
                                                                   {'uom_id': uom},
                                                                   'uom_description')[0]
    return uom


def get_accounting_description(acc_cat):
    if django_query_instance.django_existence_check(AccountAssignmentCategory,
                                                    {'account_assign_cat': acc_cat}):
        accounting = django_query_instance.django_filter_query(AccountAssignmentCategory,
                                                               {'account_assign_cat': acc_cat},
                                                               None,
                                                               None)[0]
        acc_cat = accounting['account_assign_cat'] + ' - ' + accounting['description']

    return acc_cat


def get_acc_value_desc_update(acc_detail, company_code):
    """

    """
    if acc_detail['acc_cat'] == CONST_CC:
        if django_query_instance.django_existence_check(AccountingDataDesc,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'account_assign_value': acc_detail['cost_center'],
                                                         'company_id': company_code}):
            description = django_query_instance.django_filter_value_list_query(AccountingDataDesc,
                                                                               {'client': global_variables.GLOBAL_CLIENT,
                                                                                'account_assign_value': acc_detail[
                                                                                       'cost_center'],
                                                                                   'company_id': company_code},
                                                                               'description')[0]
            acc_detail['cost_center'] = acc_detail['cost_center'] + ' - ' + description
        elif django_query_instance.django_existence_check(AccountingDataDesc,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'account_assign_value': acc_detail['cost_center'],
                                                         'company_id': CONST_ALL}):
            description = django_query_instance.django_filter_value_list_query(AccountingDataDesc,
                                                                               {
                                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                                   'account_assign_value': acc_detail[
                                                                                       'cost_center'],
                                                                                   'company_id': CONST_ALL},
                                                                               'description')[0]
            acc_detail['cost_center'] = acc_detail['cost_center'] + ' - ' + description

    elif acc_detail['acc_cat'] == CONST_WBS:
        if django_query_instance.django_existence_check(AccountingDataDesc,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'account_assign_value': acc_detail['wbs_ele'],
                                                         'company_id': company_code}):
            description = django_query_instance.django_filter_value_list_query(AccountingDataDesc,
                                                                               {
                                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                                   'account_assign_value': acc_detail[
                                                                                       'wbs_ele'],
                                                                                   'company_id': company_code},
                                                                               'description')[0]
            acc_detail['wbs_ele'] = acc_detail['wbs_ele'] + ' - ' + description
        elif django_query_instance.django_existence_check(AccountingDataDesc,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'account_assign_value': acc_detail['wbs_ele'],
                                                         'company_id': CONST_ALL}):
            description = django_query_instance.django_filter_value_list_query(AccountingDataDesc,
                                                                               {
                                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                                   'account_assign_value': acc_detail[
                                                                                       'wbs_ele'],
                                                                                   'company_id': CONST_ALL},
                                                                               'description')[0]
            acc_detail['wbs_ele'] = acc_detail['wbs_ele'] + ' - ' + description

    elif acc_detail['acc_cat'] == CONST_OR:
        if django_query_instance.django_existence_check(AccountingDataDesc,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'account_assign_value': acc_detail['internal_order'],
                                                         'company_id': company_code}):
            description = django_query_instance.django_filter_value_list_query(AccountingDataDesc,
                                                                               {
                                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                                   'account_assign_value': acc_detail[
                                                                                       'internal_order'],
                                                                                   'company_id': company_code},
                                                                               'description')[0]
            acc_detail['internal_order'] = acc_detail['internal_order'] + ' - ' + description
        elif django_query_instance.django_existence_check(AccountingDataDesc,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'account_assign_value': acc_detail['internal_order'],
                                                         'company_id': CONST_ALL}):
            description = django_query_instance.django_filter_value_list_query(AccountingDataDesc,
                                                                               {
                                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                                   'account_assign_value': acc_detail[
                                                                                       'internal_order'],
                                                                                   'company_id': CONST_ALL},
                                                                               'description')[0]
            acc_detail['internal_order'] = acc_detail['internal_order'] + ' - ' + description

    elif acc_detail['acc_cat'] == CONST_AS:
        if django_query_instance.django_existence_check(AccountingDataDesc,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'account_assign_value': acc_detail['asset_number'],
                                                         'company_id': company_code}):
            description = django_query_instance.django_filter_value_list_query(AccountingDataDesc,
                                                                               {
                                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                                   'account_assign_value': acc_detail[
                                                                                       'asset_number'],
                                                                                   'company_id': company_code},
                                                                               'description')[0]
            acc_detail['asset_number'] = acc_detail['asset_number'] + ' - ' + description
        elif django_query_instance.django_existence_check(AccountingDataDesc,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'account_assign_value': acc_detail['asset_number'],
                                                         'company_id': CONST_ALL}):
            description = django_query_instance.django_filter_value_list_query(AccountingDataDesc,
                                                                               {
                                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                                   'account_assign_value': acc_detail[
                                                                                       'asset_number'],
                                                                                   'company_id': CONST_ALL},
                                                                               'description')[0]
            acc_detail['asset_number'] = acc_detail['asset_number'] + ' - ' + description
    return acc_detail


def get_gl_acc_description(gl_acc_num, company_code):
    """
    """
    if django_query_instance.django_existence_check(AccountingDataDesc,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'account_assign_value': gl_acc_num,
                                                     'company_id': company_code}):
        description = django_query_instance.django_filter_value_list_query(AccountingDataDesc,
                                                                           {'client': global_variables.GLOBAL_CLIENT,
                                                                            'account_assign_value': gl_acc_num,
                                                                            'company_id': company_code},
                                                                           'description')[0]
        gl_acc_num = gl_acc_num + ' - ' + description
    elif django_query_instance.django_existence_check(AccountingDataDesc,
                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                       'account_assign_value': gl_acc_num,
                                                       'company_id': CONST_ALL}):
        description = django_query_instance.django_filter_value_list_query(AccountingDataDesc,
                                                                           {'client': global_variables.GLOBAL_CLIENT,
                                                                            'account_assign_value': gl_acc_num,
                                                                            'company_id': CONST_ALL},
                                                                           'description')[0]
        gl_acc_num = gl_acc_num + ' - ' + description

    return gl_acc_num
