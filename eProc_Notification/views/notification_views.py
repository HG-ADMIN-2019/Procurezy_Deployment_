"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    notification_views.py
Usage:
    get_notification_detail

Author:
   Deepika
"""
from django.http import JsonResponse
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Notification.Utilities.notification_specific import get_login_user_notification
from eProc_Notification.models import Notifications
from eProc_Shopping_Cart.context_processors import update_user_info

JsonParser_obj = JsonParser()
django_query_instance = DjangoQueries()


def get_notification_detail(request):
    """

    :param request:
    :return:
    """

    update_user_info(request)
    notification_messages = get_login_user_notification()

    return JsonResponse(notification_messages)


def update_read_status(request):
    """
    :param request:
    :return:
    """
    msg = {}
    read_status = request.POST.get('read_status')
    if read_status == 'false':
        read_status = False
    else:
        read_status = True
    notification = request.POST.get('notif_id')
    django_query_instance.django_filter_only_query(Notifications,
                                                   {'notification_id': notification}).update(read_status=read_status)

    msg['notification_count'] = django_query_instance.django_filter_count_query(Notifications, {
        'username': global_variables.GLOBAL_LOGIN_USERNAME,
        'client': global_variables.GLOBAL_CLIENT,
        'read_status': False
    })

    return JsonResponse(msg)


def set_notification_important(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT

    if request.method == 'POST':
        notification_id = request.POST.get('notif_id')

        notif_query = django_query_instance.django_filter_only_query(Notifications, {
            'notification_id': notification_id, 'client': client
        })

        notif_important_flag = list(notif_query.values_list('star_notif_flag', flat=True))

        if not notif_important_flag[0]:
            star_notif_flag = True
            notif_query.update(star_notif_flag=star_notif_flag)
            return JsonResponse({'success': 'IMPORTANT'}, status=201)
        else:
            star_notif_flag = False
            notif_query.update(star_notif_flag=star_notif_flag)
            return JsonResponse({'success': 'NOT_IMPORTANT'}, status=201)


def delete_notification(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    username = global_variables.GLOBAL_LOGIN_USERNAME

    if request.method == 'POST':
        notification_id = request.POST.get('notif_id')
        django_query_instance.django_filter_only_query(Notifications, {
            'notification_id': notification_id, 'client': client
        }).update(del_ind=True)

        return JsonResponse({'success': 'successfully_deleted'}, status=201)
