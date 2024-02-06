"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
   consumers.py
Usage:


Author:
   Deepika Kodirangaiah
"""
import json
from datetime import datetime

from django.db import transaction
from django.shortcuts import render
from django.utils.safestring import mark_safe
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Chat.Utitlities.doc_chat_specific import save_participants
from eProc_Chat.models import ChatParticipants, ChatContent
from eProc_Registration.models import UserData
from eProc_Shopping_Cart.context_processors import update_user_info

django_query_instance = DjangoQueries()


def index(request):
    return render(request, 'eProc_Doc_Chat/chat_home.html')


@transaction.atomic
def room(request, action, chat_type, room_name, client):
    update_user_info(request)

    context = {
        'inc_nav': True,
    }
    if action == 'initiate':
        chat_room_title = save_participants(chat_type, room_name, client)

        chat_room_data = django_query_instance.django_get_query(ChatParticipants, {
            'chat_type': chat_type, 'room_no': room_name, 'client': client,
            'username': global_variables.GLOBAL_LOGIN_USERNAME
        })

        user_chats_list = django_query_instance.django_filter_only_query(ChatParticipants, {
            'client': client,
            'username': global_variables.GLOBAL_LOGIN_USERNAME
        })

    else:
        chat_room_data = django_query_instance.django_get_query(ChatParticipants, {
            'chat_type': chat_type, 'room_no': room_name, 'client': client,
            'username': global_variables.GLOBAL_LOGIN_USERNAME
        })

        user_chats_list = django_query_instance.django_filter_query(ChatParticipants, {
            'client': client,
            'username': global_variables.GLOBAL_LOGIN_USERNAME
        }, None, None)

        for data in user_chats_list:
            if ChatContent.objects.filter(client=client, room_no=data['room_no'], del_ind=False).exists():
                data['chat_content'] = (list(ChatContent.objects.filter(client=client, room_no=data['room_no'], del_ind=False).order_by('-chat_timestamp')[:1].values_list('chat_content', flat=True)))[0]
                chat_timestamp = (list(ChatContent.objects.filter(client=client, room_no=data['room_no'], del_ind=False).order_by('-chat_timestamp')[:1].values_list('chat_timestamp', flat=True)))[0]
                data['chat_timestamp'] = datetime.strftime(chat_timestamp, "%I:%M %p")

        chat_room_title = django_query_instance.django_filter_value_list_query(ChatParticipants, {
            'chat_type': chat_type, 'room_no': room_name, 'client': client
        }, 'room_name')[0]

    roomtitle = chat_room_title.split(",")

    participants_name = list(UserData.objects.filter(username__in=roomtitle, client=client).values('email', 'first_name', 'last_name'))

    context['chat_room_data'] = chat_room_data
    context['user_chats_list'] = user_chats_list
    context['room_name'] = mark_safe(json.dumps(room_name))
    context['username'] = mark_safe(json.dumps(request.user.username))
    context['chat_room_title'] = mark_safe(json.dumps(chat_room_title))
    context['action'] = mark_safe(json.dumps(action))
    context['participants_name'] = participants_name

    return render(request, 'eProc_Doc_Chat/chat_room.html', context)
