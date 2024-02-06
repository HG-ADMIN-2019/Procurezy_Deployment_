from django.http import JsonResponse

from eProc_Basic.Utilities.constants.constants import CONST_DEFAULT_LANGUAGE
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import requester_field_info
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models.development_data import *
from eProc_Registration.models import UserData

django_query_instance = DjangoQueries()


# Function to get the message details
def get_message_description(request):
    if request.method == "POST" and request.is_ajax():
        msgid = JsonParser().get_json_from_req(request)
        message_type, message_desc = get_message_desc(msgid)
        # message_type = django_query_instance.django_filter_value_list_query(MessagesId, {
        #     'del_ind': False, 'messages_id': msgid, 'client': client,
        # }, 'messages_type')
        # if django_query_instance.django_existence_check(MessagesIdDesc, {
        #     'del_ind': False, 'messages_id': msgid, 'client': client,
        #     'language_id': userlang
        # }):
        #
        #     message_desc = django_query_instance.django_filter_value_list_query(MessagesIdDesc, {
        #         'del_ind': False, 'messages_id': msgid, 'client': client,
        #         'language_id': userlang
        #     }, 'messages_id_desc')
        # else:
        #     message_desc = django_query_instance.django_filter_value_list_query(MessagesIdDesc, {
        #         'del_ind': False, 'messages_id': msgid, 'client': client,
        #         'language_id': CONST_DEFAULT_LANGUAGE,
        #     }, 'messages_id_desc')

        return JsonResponse({'messages_id_desc': message_desc, 'message_type': message_type})


def get_msg_desc(msgId):
    client = global_variables.GLOBAL_CLIENT
    message_type = django_query_instance.django_filter_value_list_query(MessagesId, {
        'del_ind': False, 'messages_id': msgId, 'client': client,
    }, 'messages_type')
    message_desc = django_query_instance.django_filter_value_list_query(MessagesIdDesc, {
        'del_ind': False, 'messages_id': msgId, 'client': client,
    }, 'messages_id_desc')
    message = {'message_type': message_type, 'message_desc': message_desc}

    return message


def get_msg_desc_without_client(msgId):
    client = global_variables.GLOBAL_CLIENT
    message_type = django_query_instance.django_filter_value_list_query(MessagesId, {
        'del_ind': False, 'messages_id': msgId,
    }, 'messages_type')
    message_desc = django_query_instance.django_filter_value_list_query(MessagesIdDesc, {
        'del_ind': False, 'messages_id': msgId,
    }, 'messages_id_desc')
    message = {'message_type': message_type, 'message_desc': message_desc}

    return message


def get_message_desc_without_client(msgId):
    """

    """
    message_desc = ''
    message_type = ''
    if django_query_instance.django_existence_check(MessagesId,
                                                    {'del_ind': False,
                                                     'messages_id': msgId}):
        message_type = django_query_instance.django_filter_value_list_query(MessagesId,
                                                                            {'del_ind': False,
                                                                             'messages_id': msgId}, 'messages_type')[0]
        if django_query_instance.django_existence_check(MessagesIdDesc, {
            'del_ind': False, 'messages_id': msgId,
            'language_id': CONST_DEFAULT_LANGUAGE,
        }):
            message_desc = django_query_instance.django_filter_value_list_query(MessagesIdDesc, {
                'del_ind': False, 'messages_id': msgId,
                'language_id': CONST_DEFAULT_LANGUAGE,
            }, 'messages_id_desc')[0]
    return message_type, message_desc


def get_message_desc(msgId):
    client = global_variables.GLOBAL_CLIENT
    message_desc = ''
    message_type = ''
    if django_query_instance.django_existence_check(MessagesId,
                                                    {'del_ind': False,
                                                     'messages_id': msgId,
                                                     'client': client}):
        message_type = django_query_instance.django_filter_value_list_query(MessagesId, {
            'del_ind': False, 'messages_id': msgId, 'client': client,
        }, 'messages_type')[0]
        if django_query_instance.django_existence_check(MessagesIdDesc,
                                                        {'del_ind': False,
                                                         'messages_id': msgId,
                                                         'language_id': global_variables.GLOBAL_USER_LANGUAGE,
                                                         'client': client}):
            message_desc = django_query_instance.django_filter_value_list_query(MessagesIdDesc, {
                'del_ind': False, 'messages_id': msgId, 'client': client,
                'language_id': global_variables.GLOBAL_USER_LANGUAGE,
            }, 'messages_id_desc')[0]
        elif django_query_instance.django_existence_check(MessagesIdDesc, {
            'del_ind': False, 'messages_id': msgId, 'client': client,
            'language_id': CONST_DEFAULT_LANGUAGE,
        }):
            message_desc = django_query_instance.django_filter_value_list_query(MessagesIdDesc, {
                'del_ind': False, 'messages_id': msgId, 'client': client,
                'language_id': CONST_DEFAULT_LANGUAGE,
            }, 'messages_id_desc')[0]
    return message_type, message_desc
