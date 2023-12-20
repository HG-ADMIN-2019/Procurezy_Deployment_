"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    notification_generic.py
Usage:
    trigger_org_notification
    trigger_doc_notification


Author:
   Deepika
"""

from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.django_query_set import get_user_object_id, DjangoQueries
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import OrgClients
from eProc_Configuration.models.development_data import NotificationType
from eProc_Notification.models import Notifications
from eProc_Workflow.Utilities.work_flow_specific import increment_max_of_notif_id
import datetime

django_query_instance = DjangoQueries()


def trigger_org_notification(attr_data):
    """

    :param attr_data:
    :return:
    """
    if attr_data['attribute_id'] == CONST_CAT_ID:
        notification_type = django_query_instance.django_get_query(NotificationType, {
            'notification_app': CONST_NOTIF_ORGMODEL,
            'notification_group': CONST_BUS_TYPE_ATTRIBUTES,
            'notification_type': attr_data['attribute_id'],
            'client': global_variables.GLOBAL_CLIENT
        })

        notification_id = increment_max_of_notif_id()

        django_query_instance.django_create_query(Notifications, {
            'notification_id': notification_id,
            'client': django_query_instance.django_get_query(OrgClients, {'client': global_variables.GLOBAL_CLIENT}),
            'values': attr_data['value'],
            'read_status': False,
            'object_id': attr_data['object_id'],
            'notif_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
            'notification_type_id': notification_type.notification_type_id,
            'notif_created_at': datetime.datetime.now(),
        })


def trigger_doc_notification(notif_usernames, notification, bus_type, notification_subtype, value):
    """

    :param notif_usernames:
    :param notification:
    :param bus_type:
    :param notification_subtype:
    :param value:
    :return:
    """
    if global_variables.GLOBAL_LOGIN_USERNAME in notif_usernames:
        notif_usernames.remove(global_variables.GLOBAL_LOGIN_USERNAME)

    notification_type_id = django_query_instance.django_filter_value_list_query(NotificationType, {
        'notification_app': notification,
        'notification_group': bus_type,
        'notification_type': notification_subtype,
        'client': global_variables.GLOBAL_CLIENT
    }, 'notification_type_id')

    for notif_username in notif_usernames:
        if not django_query_instance.django_existence_check(Notifications, {
            'client': global_variables.GLOBAL_CLIENT, 'username': notif_username, 'values': value,
            'notification_type_id': notification_type_id, 'del_ind': False
        }):
            object_id = get_user_object_id(notif_username)
            django_query_instance.django_create_query(Notifications, {
                'notification_id': guid_generator(),
                'client': django_query_instance.django_get_query(OrgClients,
                                                                 {'client': global_variables.GLOBAL_CLIENT}),
                'username': notif_username,
                'values': value,
                'read_status': False,
                'object_id': int(object_id),
                'notif_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                'notification_type_id': notification_type_id,
                'notif_created_at': datetime.datetime.now(),
                'notif_changed_at': datetime.datetime.now(),
            })
        else:
            django_query_instance.django_filter_only_query(Notifications, {
                'client': global_variables.GLOBAL_CLIENT, 'username': notif_username,
                'values': value, 'notification_type_id': notification_type_id, 'del_ind': False
            }).update(read_status=False,  notif_changed_at=datetime.datetime.now())


def get_dictionary_instance(dictionary_list, dic_val, key):
    """

    :param dictionary_list:
    :param dic_val:
    :param key:
    :return:
    """
    result = ''
    for sub in dictionary_list:
        if sub[key] == dic_val:
            result = sub
            break
    # result = next((dict_instance for dict_instance in dictionary_list if dict_instance[key] == dic_val), None)
    return result
