"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    personal_settings.py
Usage:
    on click of Personal settings tab in user settings page
    personal_settings_display - This function handle personal setting data in display mode and render personal_settings_display.html
    personal_settings_edit - This function handle personal setting data in edit mode and render personal_settings.html
Author:
    Deepika K
"""
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.shortcuts import render
from django.contrib import messages
from eProc_Basic.Utilities.constants.constants import CONST_PERSONAL_SETTINGS
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.messages.messages import *
from django.contrib.auth.decorators import login_required
from eProc_Basic.decorators import authorize_view
from eProc_Registration.models.registration_model import UserData
from eProc_Shopping_Cart.context_processors import clear_user_info, update_user_info_from_db
from eProc_User_Settings.User_Settings_Forms.personal_settings_forms import PersonalSettingsDisplayForm, \
    PersonalSettingsForm
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries

django_query_instance = DjangoQueries()


@login_required
@authorize_view(CONST_PERSONAL_SETTINGS)
def personal_settings_display(request):
    """
    handle personal setting data in display mode
    :param request: request data from UI
    :return: render personal_settings_display.html
    """
    action_flag = 'Edit'
    username = request.user.username
    client = request.user.client
    user_name = django_query_instance.django_get_query(UserData, {'username': username, 'client': client})

    if not (user_name.language_id and user_name.time_zone and user_name.currency_id):
        # msgid = 'MSG005'
        # error_msg = get_msg_desc(msgid)
        # msg = error_msg['message_desc'][0]
        # error_msg = msg
        message_desc = get_message_desc('MSG005')
        messages.warning(request, message_desc)
        # messages.warning(request, MSG005)
    if 'Edit' in request.POST:
        personal_settings = PersonalSettingsForm(instance=user_name)
        action_flag = 'Save'

    elif 'Save' in request.POST:
        action_flag = 'Edit'
        personal_settings_data = PersonalSettingsForm(request.POST, instance=user_name)

        if personal_settings_data.is_valid():
            personal_settings_data.save()
            clear_user_info()
            email_id = request.user.email
            query_dic = {'email': email_id}
            update_user_info_from_db(query_dic)
            # msgid = 'MSG003'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            message_desc = get_message_desc('MSG003')[1]
            messages.info(request, message_desc)
            # messages.info(request, MSG003)
            update_session_auth_hash(request, user_name)  # Important!
        else:
            # msgid = 'MSG004'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            message_desc = get_message_desc('MSG004')[1]
            messages.error(request, message_desc)

        personal_settings = PersonalSettingsDisplayForm(instance=user_name)

    else:
        personal_settings = PersonalSettingsDisplayForm(instance=user_name)

    context = {
        'inc_nav': True,
        'shopping': True,
        'action_flag': action_flag,
        'personal_settings': personal_settings,
        'is_slide_menu': True,
        'is_personalization_active': True,
        'password_change_form': PasswordChangeForm(request.user, request.POST)
    }
    return render(request, 'User_settings/personal_settings_display.html', context)


@login_required
@authorize_view(CONST_PERSONAL_SETTINGS)
@transaction.atomic
def personal_settings_edit(request):
    """
    handle personal setting data in edit mode
    :param request: request data from UI
    :return: render personal_settings.html
    """
    username = request.user.username
    client = request.user.client
    user_name = django_query_instance.django_get_query(UserData, {'username': username, 'client': client})

    user_name_display = request.user.username
    if not (user_name.language_id and user_name.time_zone and user_name.currency_id):
        # msgid = 'MSG005'
        # error_msg = get_msg_desc(msgid)
        # msg = error_msg['message_desc'][0]
        # error_msg = msg
        message_desc = get_message_desc('MSG005')
        messages.warning(request, message_desc)
    if request.method == 'POST':

        personal_settings_data = PersonalSettingsForm(request.POST, instance=user_name)

        if personal_settings_data.is_valid():
            personal_settings_data.save()
            # msgid = 'MSG003'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            message_desc = get_message_desc('MSG003')[1]
            messages.info(request,message_desc)
            # messages.info(request, MSG003)
        else:
            # msgid = 'MSG004'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            message_desc = get_message_desc('MSG004')[1]
            messages.error(request, message_desc)
            # messages.error(request, MSG004)

    personal_settings = PersonalSettingsForm(instance=user_name)

    context = {
        'inc_nav': True,
        'shopping': True,
        'personal_settings': personal_settings,
        'user_name_display': user_name_display,
        'is_slide_menu': True,
        'is_personalization_active': True,
        'password_change_form': PasswordChangeForm(request.user, request.POST)
    }
    return render(request, 'User_settings/personal_settings.html', context)
