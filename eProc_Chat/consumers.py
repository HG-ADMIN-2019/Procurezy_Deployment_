"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
   consumers.py
Usage:


Author:
   Deepika
"""

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from eProc_Basic.Utilities.constants.constants import CONST_NOTIF_WF, CONST_BUS_TYPE_SC
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import requester_field_info
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Chat.models import ChatContent
from eProc_Configuration.models import OrgClients
from eProc_Notification.Utilities.notification_generic import trigger_doc_notification

django_query_instance = DjangoQueries()


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        messages = django_query_instance.django_filter_only_query(ChatContent,
                                                                  {'room_no': data['room_name']}).order_by(
            'chat_timestamp')[:30]
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        username = data['from']
        room_name = data['room_name']
        action = data['action']
        chat_room_title = data['chat_room_title']
        user_list = chat_room_title.split(',')
        if action == 'RESPONSE':
            trigger_doc_notification(user_list, CONST_NOTIF_WF, CONST_BUS_TYPE_SC, action, room_name)

        client = django_query_instance.django_get_query(OrgClients, {'client': global_variables.GLOBAL_CLIENT})

        message = django_query_instance.django_create_query(ChatContent, {
            'chat_content_guid': guid_generator(),
            'room_no': room_name,
            'username': username,
            'chat_content': data['message'],
            'client': client
        })

        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        receiver_fn = requester_field_info(message.username, 'first_name')
        return {
            'author': message.username,
            'author_first_name': receiver_fn,
            'content': message.chat_content,
            'timestamp': str(message.chat_timestamp)
        }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))
