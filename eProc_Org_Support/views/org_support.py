import ast
import datetime

from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from django.shortcuts import render
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic_Settings.views.basic_settings import JsonParser_obj
from eProc_Chat.Utitlities.doc_chat_specific import create_chat_participant
from eProc_Org_Model.models.org_model import OrgModel
from eProc_Org_Support.models.org_support_models import OrgSupport, OrgAnnouncements
from eProc_Registration.models.registration_model import UserData
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Basic.Utilities.functions.get_db_query import django_query_instance, get_login_obj_id
from eProc_Configuration.models.development_data import *
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.guid_generator import random_int, guid_generator
from eProc_Basic.Utilities.functions.django_q_query import django_q_query
from eProc_Basic.Utilities.global_defination import global_variables


def customer_support_chat(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    username = global_variables.GLOBAL_LOGIN_USERNAME

    if request.method == 'POST':
        customer_support_username_list = list(
            OrgSupport.objects.filter(org_support_types='CHAT', client=client, del_ind=False).values_list(
                'username', flat=True))
        customer_support_username_list.append(username)

        room_name = '12345'
        title = 'CUSTOMER_SUPPORT'
        chat_type = 'CUSTOMER_SUPPORT'
        context = {}
        create_chat_participant(customer_support_username_list, room_name, title, chat_type, client)
        return render(request, 'eProc_Sho_Home\home.html', context)


def org_announcement_save(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    obj_id = django_query_instance.django_get_query(OrgModel, {
        'object_id': global_variables.GLOBAL_LOGIN_USER_OBJ_ID, 'del_ind': False
    })

    status_dropdown_values = django_query_instance.django_filter_only_query(FieldTypeDescription, {
        'del_ind': False, 'field_name': 'status', 'client': global_variables.GLOBAL_CLIENT
    })
    priority_dropdown_values = django_query_instance.django_filter_only_query(FieldTypeDescription, {
        'del_ind': False, 'field_name': 'priority', 'client': global_variables.GLOBAL_CLIENT
    })
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_admin_active': True,
        'status_dropdown_values': status_dropdown_values,
        'priority_dropdown_values': priority_dropdown_values,
    }

    if request.method == "POST" and request.is_ajax():
        org_announcement_data = JsonParser().get_json_from_req(request)

        guid = org_announcement_data['announcement_guid']
        if guid == '':
            guid = guid_generator()

        defaults = {
            'unique_announcement_id': guid,
            'announcement_subject': org_announcement_data['announcement_subject'],
            'announcement_description': org_announcement_data['announcement_description'],
            'status': org_announcement_data['status'],
            'priority': org_announcement_data['priority'],
            'announcement_from_date': org_announcement_data['announcement_from_date'],
            'announcement_to_date': org_announcement_data['announcement_to_date'],
            'client': client,
            'del_ind': False,
            'object_id': obj_id,
            'announcements_created_at': datetime.datetime.now(),
            'announcements_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
            'announcements_changed_at': datetime.datetime.now(),
            'announcements_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
        }

        # Check if an announcement with the given unique_announcement_id already exists
        existing_announcement = django_query_instance.django_get_query(OrgAnnouncements, {
            'unique_announcement_id': guid
        })

        if existing_announcement:
            # Preserve the original announcement_id when updating
            defaults['announcement_id'] = existing_announcement.announcement_id
            django_query_instance.django_update_query(OrgAnnouncements, {'unique_announcement_id': guid}, defaults)
            msgid = 'MSG156'  # Use a different message code for update success
            success_msg = get_message_desc(msgid)[1]
        else:
            # Generate a new announcement_id for new announcements
            defaults['announcement_id'] = random_int(8)
            django_query_instance.django_create_query(OrgAnnouncements, defaults)
            msgid = 'MSG155'
            success_msg = get_message_desc(msgid)[1]

        # Create a new dictionary with announcement data
        announcement_result1 = {
            'unique_announcement_id': guid,
            'announcement_id': defaults['announcement_id'],
            'announcement_subject': org_announcement_data['announcement_subject'],
            'announcement_description': org_announcement_data['announcement_description'],
            'status': org_announcement_data['status'],
            'priority': org_announcement_data['priority'],
            'announcement_from_date': org_announcement_data['announcement_from_date'],
            'announcement_to_date': org_announcement_data['announcement_to_date'],
        }

        announcement_result1 = django_query_instance.django_filter_query(OrgAnnouncements, {
            'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
        }, None, None)
        t_count = len(announcement_result1)

        announcement_ids = [annsmt_data['unique_announcement_id'] for annsmt_data in announcement_result1]
        # Include the 'announcement_results1' dictionary in the JSON response
        response_data = {
            'announcement_ids': announcement_ids,
            't_count': t_count,
            'message': success_msg,
            'updated_guid': guid,
            'announcement_result1': announcement_result1,
        }

        return JsonResponse(response_data)

    return render(request, 'org_announcements_display.html', context)


@login_required
def update_org_announcement_details(request):
    update_user_info(request)
    if request.method == 'POST' and request.is_ajax():
        org_announcement_data = JsonParser().get_json_from_req(request)

        update_announcement_guid = org_announcement_data['announcement_guid']
        update_announcement_id = org_announcement_data['announcement_id']
        update_announcement_subject = org_announcement_data['announcement_subject']
        update_announcement_description = org_announcement_data['announcement_description']
        update_status = org_announcement_data['status']
        update_priority = org_announcement_data['priority']
        update_announcement_from_date = org_announcement_data['announcement_from_date']
        update_announcement_to_date = org_announcement_data['announcement_to_date']

        update_announcement_data = django_query_instance.django_filter_only_query(OrgAnnouncements, {
            'unique_announcement_id': update_announcement_guid,
            'del_ind': False})
        if org_announcement_data['del_ind']:
            OrgAnnouncements.objects.filter(unique_announcement_id=org_announcement_data['announcement_guid']).update(
                del_ind=True)
            msgid = 'MSG113'
            error_msg = get_message_desc(msgid)[1]
            message = error_msg
        else:
            update_announcement_data.update(
                announcement_subject=update_announcement_subject,
                announcement_id=update_announcement_id,
                announcement_description=update_announcement_description,
                status=update_status,
                priority=update_priority,
                announcement_from_date=update_announcement_from_date,
                announcement_to_date=update_announcement_to_date,
            )
            msgid = 'MSG156'
            error_msg = get_message_desc(msgid)[1]

            message = error_msg

    return JsonResponse({'message': message})


def org_support_save(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    obj_id = django_query_instance.django_get_query(OrgModel, {
        'object_id': global_variables.GLOBAL_LOGIN_USER_OBJ_ID, 'del_ind': False
    })

    username_values = []
    user_dropdown_values = django_query_instance.django_filter_only_query(UserData, {
        'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
    })
    for val in user_dropdown_values:
        username_values.append(val.username)

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_admin_active': True,
        'username_values': username_values,
    }

    if request.method == "POST" and request.is_ajax():
        org_support_data = JsonParser().get_json_from_req(request)

        for data in org_support_data:
            guid = data['org_support_guid']
            if guid == '':
                guid = guid_generator()

            defaults = {
                'org_support_guid': guid,
                'org_support_types': data['support_type'],
                'org_support_email': data['support_email'],
                'org_support_number': data['support_number'],
                'username': data['username'],
                'client': client,
                'del_ind': False,
                'object_id': obj_id,
                'org_support_created_at': datetime.datetime.now(),
                'org_support_created_by': global_variables.GLOBAL_LOGIN_USERNAME,  # Assuming the user is logged in
                'org_support_changed_at': datetime.datetime.now(),
                'org_support_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
            }

            django_query_instance.django_update_or_create_query(OrgSupport, {'org_support_guid': guid},
                                                                defaults)
            msgid = 'MSG157'
            error_msg = get_message_desc(msgid)[1]

        return JsonResponse({'message': error_msg, 'updated_guid': guid})

    return render(request, 'org_support.html', context)


@login_required
def update_org_support_details(request):
    update_user_info(request)
    if request.method == 'POST' and request.is_ajax():
        org_support_data = JsonParser().get_json_from_req(request)

        org_support_guid = org_support_data['org_support_guid'],
        org_support_types = org_support_data['support_type'],
        org_support_email = org_support_data['support_email'],
        org_support_number = org_support_data['support_number'],
        username = org_support_data['username'],

        update_announcement_data = django_query_instance.django_filter_only_query(OrgSupport, {
            'org_support_guid': org_support_guid,
            'del_ind': False})

        OrgSupport.objects.filter(org_support_guid=org_support_data['org_support_guid']).update(
            org_support_types=org_support_types,
            org_support_email=org_support_email,
            org_support_number=org_support_number,
            username=username,

        )
        msgid = 'MSG156'
        error_msg = get_message_desc(msgid)[1]

        message = error_msg

    return JsonResponse({'message': message})


def org_support_config(request):
    username_values = []
    user_dropdown_values = django_query_instance.django_filter_only_query(UserData, {
        'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
    })
    user_names = list()
    user_first_names = list()
    for names in user_dropdown_values:
        user_names = {'user_name': names.username,
                      'user_data': names.first_name + ' ' + names.last_name + ' - ' + names.email}
        user_first_names.append(user_names)
    chat_data_array = []
    chat_data = django_query_instance.django_filter_only_query(OrgSupport, {
        'client': global_variables.GLOBAL_CLIENT, 'del_ind': False, 'org_support_types': 'CHAT'
    })
    for val in chat_data:
        res = (val.username).split(',')
        chat_data_array = res

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_admin_active': True,
        'user_first_names': user_first_names,
        'chat_data': chat_data_array,
        'chat_data1': chat_data
    }

    return render(request, 'org_support_config.html', context)


def get_support_data(request):
    call_support_data_array = []
    call_support_guid_array = []
    email_support_data_array = []
    email_support_guid_array = []
    chat_support_data_array = []
    chat_support_guid_array = []

    call_support_data = django_query_instance.django_filter_only_query(OrgSupport, {
        'client': global_variables.GLOBAL_CLIENT, 'del_ind': False, 'org_support_types': 'Call'
    })

    for val in call_support_data:
        call_support_data_array.append(val.org_support_number)
        call_support_guid_array.append(val.org_support_guid)

    email_support_data = django_query_instance.django_filter_only_query(OrgSupport, {
        'client': global_variables.GLOBAL_CLIENT, 'del_ind': False, 'org_support_types': 'EMAIL'
    })
    for val in email_support_data:
        email_support_data_array.append(val.org_support_email)
        email_support_guid_array.append(val.org_support_guid)

    chat_support_data = django_query_instance.django_filter_only_query(OrgSupport, {
        'client': global_variables.GLOBAL_CLIENT, 'del_ind': False, 'org_support_types': 'CHAT'
    })
    # user_dropdown_values = django_query_instance.django_filter_only_query(UserData, {
    #     'client': global_variables.GLOBAL_CLIENT, 'del_ind': False, 'username': val.username
    # })
    user_data_values = []
    for val in chat_support_data:
        username_str = val.username  # Assuming val.username = '\'CHAITRA\''
        username_str = username_str.replace('\\', '')  # Remove backslashes
        username = ast.literal_eval(username_str)  # Convert to Python object

        selected_user_data = django_query_instance.django_filter_only_query(UserData, {
            'client': global_variables.GLOBAL_CLIENT, 'del_ind': False, 'username__in': username
        })
        for names in selected_user_data:
            user_names = names.first_name + ' ' + names.last_name + ' - ' + names.email
            user_data_values.append(user_names)

        chat_support_data_array = username
        chat_support_guid_array.append(val.org_support_guid)

    return JsonResponse(
        {'call_support_data_array': call_support_data_array, 'call_support_guid_array': call_support_guid_array,
         'email_support_data_array': email_support_data_array, 'email_support_guid_array': email_support_guid_array,
         'chat_support_data_array': chat_support_data_array, 'chat_support_guid_array': chat_support_guid_array,
         'user_data': user_data_values})


def org_announcement_search(**kwargs):
    """

    """
    status_query = Q()
    client = global_variables.GLOBAL_CLIENT
    subject_query = Q()
    priority_query = Q()
    announcement_subject = Q()

    instance = OrgAnnouncements()
    for key, value in kwargs.items():
        value_list = []
        if value:
            if key == 'announcement_subject':
                if value == '*':
                    result = list(OrgAnnouncements.objects.filter(client=client, del_ind=False).values().order_by(
                        'announcement_id'))
                    annsment_query = result
                if '*' not in value:
                    value_list = [value]
                subject_query = django_q_query(value, value_list, 'announcement_subject')
            if key == 'status':
                value_list = [value]
                status_query = django_q_query(value, value_list, 'status')
            if key == 'priority':
                value_list = [value]
                priority_query = django_q_query(value, value_list, 'priority')

            annsment_query = list(instance.get_annsmt_details_by_fields(client,
                                                                        instance,
                                                                        subject_query,
                                                                        status_query,
                                                                        priority_query
                                                                        ))

    return annsment_query


def delete_table_row(request):
    update_user_info(request)
    if request.method == 'POST' and request.is_ajax():
        call_support_data = JsonParser().get_json_from_req(request)
        for data in call_support_data:
            guid = data['org_support_guid']
        call_support_guid = guid
        django_query_instance.django_update_query(OrgSupport,
                                                  {'client': global_variables.GLOBAL_CLIENT,
                                                   'org_support_guid': call_support_guid}, {'del_ind': True})
    return True


def active_inactive_org(request):
    emp_lock_flag_detail = JsonParser_obj.get_json_from_req(request)
    announcement_id = emp_lock_flag_detail['announcement_id']
    flag = emp_lock_flag_detail['flag']

    # Determine the new status based on the flag value
    if flag:
        new_status = 'Active'
    else:
        new_status = 'Inactive'

    announcementid = announcement_id.split('-')[0]

    # Update the status in the database
    django_query_instance.django_update_query(
        OrgAnnouncements,
        {'client': global_variables.GLOBAL_CLIENT,
         'announcement_id': announcementid,
         'del_ind': False},
        {'status': new_status}
    )

    # Prepare the response
    response = {
        'status': new_status,
        'message': 'Status updated successfully'
    }

    return JsonResponse(response, safe=False)

