from django.db import transaction

from eProc_Attributes.Utilities.attributes_generic import OrgAttributeValues
from eProc_Basic.Utilities.functions.django_query_set import get_user_object_id, DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import get_object_id_from_username
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import OrgClients
from eProc_Configuration.models.development_data import NotificationType
from eProc_Emails.Utilities.email_notif_generic import appr_notify
from eProc_Notification.models import Notifications
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import get_SC_details_email
from eProc_Shopping_Cart.models import ScApproval, ScHeader, ScPotentialApproval
import datetime
from eProc_Shopping_Cart.models import ScItem
from eProc_Calendar_Settings.Utilities.calender_settings_generic import calculate_delivery_date
from eProc_Basic.Utilities.constants.constants import *
from eProc_User_Settings.Utilities.user_settings_generic import get_object_id_list_user

django_query_instance = DjangoQueries()


def get_appr_status(appr_status):
    """

    :param appr_status:
    :return:
    """
    approver_status = ''
    if appr_status == CONST_SC_APPR_APPROVED:
        approver_status = CONST_SC_APPR_APPROVED
    elif appr_status == CONST_SC_APPR_REJECTED:
        approver_status = CONST_SC_APPR_REJECTED
    elif appr_status == CONST_SC_APPR_INQUIRED:
        approver_status = CONST_SC_APPR_INQUIRED
    return approver_status


def get_header_status(appr_status):
    """

        :param appr_status:
        :return:
        """
    approver_status = ''
    if appr_status == CONST_SC_APPR_APPROVED:
        approver_status = CONST_SC_HEADER_APPROVED
    elif appr_status == CONST_SC_APPR_REJECTED:
        approver_status = CONST_SC_HEADER_REJECTED
    return approver_status


@transaction.atomic
def update_appr_status(appr_status):
    """

    :param appr_status:
    :return:
    """
    global next_level_approver
    next_level_approver = []
    mgr_details = {}
    header_status = ''
    org_attr_value_instance = OrgAttributeValues()
    approval_detail = appr_status['status'].split('-')
    header_guid = approval_detail[1]
    sc_header_instance = django_query_instance.django_get_query(ScHeader, {'guid': header_guid})
    sc_requester = sc_header_instance.requester
    user_object_id = get_object_id_from_username(sc_requester)
    object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT, user_object_id)
    default_calendar_id = org_attr_value_instance.get_user_default_attr_value_list_by_attr_id(object_id_list,
                                                                                              CONST_CALENDAR_ID)[1]
    item_details = django_query_instance.django_filter_only_query(ScItem, {'header_guid': header_guid})
    for items in item_details:
        if items.call_off not in [CONST_FREETEXT_CALLOFF, CONST_LIMIT_ORDER_CALLOFF]:
            if items.call_off == CONST_CATALOG_CALLOFF:
                supplier_id = items.pref_supplier
            else:
                supplier_id = items.supplier_id
            calculate_delivery_date(items.guid, int(items.lead_time), supplier_id,
                                    default_calendar_id, global_variables.GLOBAL_CLIENT, ScItem)
    app_status_val = get_appr_status(approval_detail[0])
    approver_guid = django_query_instance.django_filter_value_list_query(ScPotentialApproval,
                                                                         {'sc_header_guid': approval_detail[1],
                                                                          'client': global_variables.GLOBAL_CLIENT,
                                                                          'app_id': global_variables.GLOBAL_LOGIN_USERNAME},
                                                                         'sc_approval_guid')[0]
    django_query_instance.django_filter_only_query(ScPotentialApproval, {
        'sc_approval_guid': approver_guid,
        'client': global_variables.GLOBAL_CLIENT,
        'app_id': global_variables.GLOBAL_LOGIN_USERNAME
    }).update(app_sts=app_status_val)
    django_query_instance.django_filter_only_query(ScPotentialApproval,
                                                   {'sc_approval_guid': approver_guid,
                                                    'client': global_variables.GLOBAL_CLIENT
                                                    }).update(proc_lvl_sts=CONST_COMPLETED)

    django_query_instance.django_filter_only_query(ScApproval,
                                                   {'guid': approver_guid,
                                                    'client': global_variables.GLOBAL_CLIENT
                                                    }).update(app_sts=app_status_val,
                                                              proc_lvl_sts=CONST_COMPLETED,
                                                              proc_time=datetime.datetime.now(),
                                                              app_id=global_variables.GLOBAL_LOGIN_USERNAME)

    if approval_detail[0] != CONST_SC_APPR_REJECTED:

        step_num = django_query_instance.django_filter_value_list_query(ScApproval,
                                                                        {'guid': approver_guid,
                                                                         'header_guid': approval_detail[1],
                                                                         'client': global_variables.GLOBAL_CLIENT,
                                                                         'app_id': global_variables.GLOBAL_LOGIN_USERNAME
                                                                         }, 'step_num')

        step_num_inc = int(step_num[0]) + 1

        if django_query_instance.django_existence_check(ScApproval, {
            'header_guid': approval_detail[1],
            'step_num': step_num_inc,
            'client': global_variables.GLOBAL_CLIENT
        }):
            django_query_instance.django_filter_only_query(ScApproval, {
                'header_guid': approval_detail[1],
                'step_num': step_num_inc,
                'client': global_variables.GLOBAL_CLIENT
            }).update(proc_lvl_sts=CONST_ACTIVE, received_time=datetime.datetime.now())
            django_query_instance.django_filter_only_query(ScPotentialApproval,
                                                           {'sc_header_guid': approval_detail[1],
                                                            'step_num': step_num_inc,
                                                            'client': global_variables.GLOBAL_CLIENT
                                                            }).update(proc_lvl_sts=CONST_ACTIVE)

            next_level_approver = django_query_instance.django_filter_value_list_query(ScPotentialApproval,
                                                                                       {'sc_header_guid':
                                                                                            approval_detail[1],
                                                                                        'step_num': step_num_inc,
                                                                                        'client': global_variables.GLOBAL_CLIENT,
                                                                                        'proc_lvl_sts': CONST_ACTIVE,
                                                                                        'app_sts': CONST_SC_APPR_OPEN
                                                                                        }, 'app_id')
            if len(next_level_approver) > 1:
                mgr_details['app_id_detail'] = next_level_approver
            else:
                mgr_details['app_id_detail'] = next_level_approver[0]
            # send mail to next level approver
            context = get_SC_details_email(approval_detail[1])
            context['manager_details'] = mgr_details
            context['step_num_inc'] = step_num_inc
            context['email_document_monitoring_guid'] = ''
            appr_notify(context, 'SC_APPROVAL', global_variables.GLOBAL_CLIENT)
        else:
            header_status = get_header_status(app_status_val)
            django_query_instance.django_update_query(ScHeader, {
                'guid': approval_detail[1],
                'client': global_variables.GLOBAL_CLIENT
            }, {'status': header_status})
            sc_header_instance.status = header_status
            sc_header_instance.save()
    else:
        header_status = get_header_status(app_status_val)
        # django_query_instance.django_filter_only_query(ScHeader, {
        #     'guid': approval_detail[1],
        #     'client': global_variables.GLOBAL_CLIENT
        # }).update(status=header_status)
        django_query_instance.django_update_query(ScHeader, {
            'guid': approval_detail[1],
            'client': global_variables.GLOBAL_CLIENT
        }, {'status': header_status})

    trigger_notification(approval_detail[2], app_status_val)
    print("header_status", header_status)
    return header_status, sc_header_instance


def increment_max_of_notif_id():
    """

    :return:
    """
    if Notifications.objects.all():
        max_val = int(Notifications.objects.filter().values_list('notification_id', flat=True).order_by(
            '-notification_id').first())
    else:
        max_val = 0
    return max_val + 1


def trigger_notification(sc_number, app_status):
    if django_query_instance.django_existence_check(ScHeader, {
        'doc_number': sc_number,
        'client': global_variables.GLOBAL_CLIENT,
        'status': app_status
    }):

        sc_header_data = django_query_instance.django_get_query(ScHeader, {
            'doc_number': sc_number,
            'client': global_variables.GLOBAL_CLIENT,
            'status': app_status
        })

        if sc_header_data.created_by == sc_header_data.requester:
            notification_type = django_query_instance.django_get_query(NotificationType, {
                'notification_app': CONST_NOTIF_WF,
                'notification_group': CONST_BUS_TYPE_SC,
                'notification_type': app_status,
                'client': global_variables.GLOBAL_CLIENT
            })

            object_id = get_user_object_id(sc_header_data.created_by)

            django_query_instance.django_create_query(Notifications, {
                'notification_id': guid_generator(),
                'client': django_query_instance.django_get_query(OrgClients,
                                                                 {'client': global_variables.GLOBAL_CLIENT}),
                'username': sc_header_data.created_by,
                'values': sc_number,
                'read_status': False,
                'object_id': int(object_id),
                'notif_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                'notification_type_id': notification_type.notification_type_id,
                'notif_created_at': datetime.datetime.now(),
                'notif_changed_at': datetime.datetime.now()
            })
