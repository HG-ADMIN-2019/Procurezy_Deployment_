from eProc_Basic.Utilities.constants.constants import CONST_LINK_DOC_DETAIL, CONST_LINK_CHAT
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import encrypt
from eProc_Basic.Utilities.functions.replace_str import replace_val1_val2
from eProc_Basic.Utilities.functions.type_casting import date_to_diff_days
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models.development_data import NotificationTypeDesc
from eProc_Notification.Utilities.notification_generic import get_dictionary_instance
from eProc_Notification.models import Notifications
from eProc_Shopping_Cart.models import ScHeader

django_query_instance = DjangoQueries()


def get_notification_url(notification_type_id, notif_val):
    modified_url_link = ''
    client = global_variables.GLOBAL_CLIENT
    if notification_type_id in CONST_LINK_DOC_DETAIL:
        if django_query_instance.django_existence_check(ScHeader, {
            'doc_number': notif_val, 'client': client, 'del_ind': False
        }):
            scheader_guid = django_query_instance.django_filter_value_list_query(ScHeader, {
                'doc_number': notif_val, 'client': client, 'del_ind': False
            }, 'guid')

            url_link = '/doc_details/my_order_doc_details/False/SC/&scheader_guid&/display/my_order'
            modified_url_link = replace_val1_val2(url_link, '&scheader_guid&', encrypt(scheader_guid[0]))
        return modified_url_link

    if notification_type_id in CONST_LINK_CHAT:
        url_link = '/chat/RESPONSE/INQUIRED/&room_no&/&client&'
        modified_url_link = replace_val1_val2(url_link, '&room_no&', notif_val)
        modified_url_link = replace_val1_val2(modified_url_link, '&client&', global_variables.GLOBAL_CLIENT.client)
        return modified_url_link


def get_login_user_notification():
    """

    :return:
    """
    notification_messages = {}
    notification_message_list = []
    order_list = ['read_status', 'notif_changed_at']
    notification_details = django_query_instance.django_filter_only_query(Notifications, {
        'client': global_variables.GLOBAL_CLIENT,
        'username': global_variables.GLOBAL_LOGIN_USERNAME,
        'del_ind': False
    }).values().order_by(*order_list)

    unread_notification_count = django_query_instance.django_filter_count_query(Notifications, {
        'client': global_variables.GLOBAL_CLIENT,
        'username': global_variables.GLOBAL_LOGIN_USERNAME,
        'del_ind': False,
        'read_status': False
    })

    if notification_details:
        notification_type_id = notification_details.values_list('notification_type_id', flat=True)

        notif_type_desc = django_query_instance.django_filter_only_query(NotificationTypeDesc, {
            'client': global_variables.GLOBAL_CLIENT, 'notification_type_id__in': notification_type_id, 'del_ind': False
        }).values('notification_message', 'notification_type_id')

        for notification_detail in notification_details:
            notification_msg = {}
            notif_message = get_dictionary_instance(notif_type_desc, notification_detail['notification_type_id'],
                                                    'notification_type_id')
            modified_msg = replace_val1_val2(notif_message['notification_message'], '&key&',
                                             notification_detail['values'])
            notification_msg['msg_info'] = modified_msg
            notification_msg['url_link'] = get_notification_url(notification_detail['notification_type_id'],
                                                                notification_detail['values'])
            notification_msg['read_status'] = notification_detail['read_status']
            notification_msg['notif_id'] = notification_detail['notification_id']
            notification_msg['notif_changed_at'] = date_to_diff_days(notification_detail['notif_changed_at'])
            notification_msg['star_notif_flag'] = notification_detail['star_notif_flag']
            notification_msg['notification_type_id'] = notification_detail['notification_type_id']

            notification_message_list.append(notification_msg)
    notification_messages['notification'] = notification_message_list
    notification_messages['unread_notification_count'] = unread_notification_count

    return notification_messages
