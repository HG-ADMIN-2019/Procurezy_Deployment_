from eProc_Basic.Utilities.constants.constants import CONST_NOTIF_WF, CONST_BUS_TYPE_SC
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Chat.models import *
from eProc_Chat.models.chat_model import ChatParticipants
from eProc_Configuration.models import OrgClients, Languages
from eProc_Notification.Utilities.notification_generic import trigger_doc_notification
from eProc_Shopping_Cart.models import ScHeader, ScApproval, ScPotentialApproval

django_query_instance = DjangoQueries()


def get_participant_list(room_name):
    participant_list = []

    if django_query_instance.django_existence_check(ScHeader, {
        'doc_number': room_name, 'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
    }):

        scheader_detail = django_query_instance.django_get_query(ScHeader, {
            'doc_number': room_name, 'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
        })

        if scheader_detail.created_by == scheader_detail.requester:
            participant_list.append(scheader_detail.created_by)

        if django_query_instance.django_existence_check(ScPotentialApproval, {
            'sc_header_guid': scheader_detail.guid,
            'client': global_variables.GLOBAL_CLIENT,
            'del_ind': False,
            'app_id': global_variables.GLOBAL_LOGIN_USERNAME,
            'step_num': '1'
        }):
            participant_list.append(global_variables.GLOBAL_LOGIN_USERNAME)
        else:
            sc_approval_detail = django_query_instance.django_filter_only_query(ScPotentialApproval, {
                'sc_header_guid': scheader_detail.guid,
                'client': global_variables.GLOBAL_CLIENT,
                'del_ind': False,
                'app_id': global_variables.GLOBAL_LOGIN_USERNAME
            }).values()

            sc_approval_step_num = int(sc_approval_detail.values_list('step_num', flat=True)[0])

            participant_list.append(sc_approval_detail.values_list('app_id', flat=True)[0])
            while sc_approval_step_num != 1:
                sc_approval_step_num = sc_approval_step_num - 1
                sc_approval_detail = django_query_instance.django_filter_value_list_query(ScApproval, {
                    'header_guid': scheader_detail.guid,
                    'client': global_variables.GLOBAL_CLIENT,
                    'del_ind': False,
                    'step_num': sc_approval_step_num
                }, 'app_id')[0]

                participant_list.append(sc_approval_detail)
    return participant_list


def save_participants(chat_type, room_name, client):

    # get participant based on sc number
    participant_list = get_participant_list(room_name)
    title = ','.join(participant_list)
    create_chat_participant(participant_list, room_name, title, chat_type, client)

    trigger_doc_notification(participant_list, CONST_NOTIF_WF, CONST_BUS_TYPE_SC, chat_type, room_name)

    return title


def create_chat_participant(participant_list, room_name, title, chat_type, client):
    """

    """
    for participant in participant_list:

        if not django_query_instance.django_existence_check(ChatParticipants, {
            'room_no': room_name, 'client': client, 'username': participant, 'chat_type': chat_type
        }):
            django_query_instance.django_create_query(ChatParticipants, {
                'chat_participants_guid': guid_generator(),
                'room_no': room_name,
                'room_name': title,
                'username': participant,
                'chat_type': chat_type,
                'client': django_query_instance.django_get_query(OrgClients, {'client': client}),
                'language_id': django_query_instance.django_get_query(Languages,
                                                                      {'language_id': global_variables.GLOBAL_USER_LANGUAGE})
            })
        else:
            django_query_instance.django_filter_only_query(ChatParticipants, {
                'room_no': room_name,
                'client': client,
                'username': participant,
                'chat_type': chat_type
            }).update(room_name=title)
