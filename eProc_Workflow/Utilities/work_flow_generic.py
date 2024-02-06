"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    attributes.py
Usage:
    on click of Attributes in nav bar dropdown
    attributes - This function handle getting attribute level data and render attributes.html
Author:
    Deepika K
"""

from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG185
from eProc_Configuration.models import *
from eProc_Shopping_Cart.models import ScHeader, ScApproval, ScPotentialApproval
import datetime

django_query_instance = DjangoQueries()


def save_sc_approval(manager_detail, header_guid, button_status, sc_completion_flag):
    step_num = 1
    for manage_detail in manager_detail:
        approver_id_list = manage_detail['app_id_detail'].split(',')
        received_time, proc_time = get_date_time(step_num, manage_detail, button_status, sc_completion_flag)
        proc_status, app_status = get_proc_level_status(step_num, manage_detail, button_status, sc_completion_flag)
        app_desc = get_app_type(manage_detail)
        sc_approver_guid = guid_generator()
        django_query_instance.django_create_query(ScApproval, {
            'client': django_query_instance.django_get_query(OrgClients, {'client': global_variables.GLOBAL_CLIENT}),
            'app_desc': app_desc,
            'guid': sc_approver_guid,
            'step_num': step_num,
            'proc_lvl_sts': proc_status,
            'app_sts': app_status,
            'received_time': received_time,
            'proc_time': proc_time,
            'time_zone': django_query_instance.django_get_query(TimeZone, {'time_zone': 'IST'}),
            'header_guid': django_query_instance.django_get_query(ScHeader, {'guid': header_guid})
        })
        for approver_id in approver_id_list:
            django_query_instance.django_create_query(ScPotentialApproval,
                                                      {'sc_potential_approval_guid': guid_generator(),
                                                       'app_id': approver_id,
                                                       'step_num': step_num,
                                                       'app_sts': app_status,
                                                       'proc_lvl_sts': proc_status,
                                                       'client': global_variables.GLOBAL_CLIENT,
                                                       'sc_approval_guid': django_query_instance.django_get_query(
                                                           ScApproval, {
                                                               'guid': sc_approver_guid}),
                                                       'sc_header_guid': django_query_instance.django_get_query(
                                                           ScHeader, {
                                                               'guid': header_guid})
                                                       })
        step_num = step_num + 1

    if len(manager_detail) > 1:
        django_query_instance.django_filter_only_query(ScHeader, {'pk': header_guid}).update(approval_step='M')
    else:
        django_query_instance.django_filter_only_query(ScHeader, {'pk': header_guid}).update(approval_step='S')


def get_proc_level_status(step_num, manage_detail, button_status, sc_completion_flag):
    proc_lvl_sts = CONST_INITIATED
    app_sts = CONST_SC_APPR_OPEN
    if button_status != CONST_SC_HEADER_SAVED:
        if sc_completion_flag == 'False' or sc_completion_flag == False:
            if step_num == 1:
                proc_lvl_sts = CONST_ACTIVE
            if manage_detail == CONST_AUTO:
                proc_lvl_sts = CONST_COMPLETED
                app_sts = CONST_SC_APPR_APPROVED
    return proc_lvl_sts, app_sts


def get_app_type(manage_detail):
    """
    :param manage_detail:
    :return:
    """
    msgid = 'MSG185'
    error_msg = get_message_desc(msgid)[1]

    if manage_detail == CONST_AUTO:
        return error_msg
    else:
        return CONST_FIN_APP


def get_date_time(step_num, manage_detail, button_status, sc_completion_flag):
    received_time = None
    proc_time = None
    if button_status != CONST_SC_HEADER_SAVED:
        if sc_completion_flag == 'False':
            if manage_detail == CONST_AUTO:
                received_time = datetime.datetime.now()
                proc_time = datetime.datetime.now()
            elif step_num == 1:
                received_time = datetime.datetime.now()
    return received_time, proc_time
