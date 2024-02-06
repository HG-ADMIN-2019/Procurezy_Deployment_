"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    first_time_password_change.py
Usage:
     This function is called on users first login
     first_time_password_change - this functionality allows user to reset password on the first login and render first_time_password_change.html

Author:
    Babu / Siddarth
"""
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.db import transaction
from django.utils import timezone
import re
from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients, getUsername
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import *
from eProc_Login.Utilities.login_specific import pwd_attribute
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from eProc_Login.Login_Forms.password_change_form import PasswordChangeCustomForm
from eProc_Org_Model.Utilities import client
from eProc_Registration.models import UserData
from eProc_Shopping_Cart.context_processors import update_user_info

django_query_instance = DjangoQueries()


@login_required
@transaction.atomic
def first_time_password_change(request):
    """
    :param request: first_time_password_change(request):
    :return: Forgot_Password/first_time_password_change.html
    """
    # Start of MEP:08-Gets the password policy for the logged in client
    client = getClients(request)
    pwd_policy = pwd_attribute(client)
    # End of MEP:08
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password1']
            if old_password == new_password:
                msgid = 'MSG119'
                error_msg = get_message_desc(msgid)[1]

                messages.error(request, error_msg)
            else:
                # Start of MEP:08-Password validation based on client
                if pwd_policy is None or pwd_policy == [CONST_NO_PSWD_POLICY]:
                    user = form.save()
                    update_session_auth_hash(request, user)  # Important!
                    user_first_login = django_query_instance.django_get_query(UserData, {
                        'username': getUsername(request), 'client': client
                    })
                    user_first_login.date_joined = timezone.now()
                    user_first_login.save()
                    return HttpResponseRedirect('/home')
                if not (pwd_policy == [CONST_NO_PSWD_POLICY]):
                    if not (re.match((pwd_policy[0]), new_password)):
                        messages.error(request, pwd_policy[1])
                    # End of MEP:08
                    else:
                        user = form.save()
                        update_session_auth_hash(request, user)  # Important!
                        user_first_login = django_query_instance.django_get_query(UserData, {
                            'username': getUsername(request), 'client': client
                        })
                        user_first_login.date_joined = timezone.now()
                        user_first_login.save()
                        return HttpResponseRedirect('/home')
    else:
        form = PasswordChangeCustomForm(request.user)
    return render(request, 'Forgot_Password/first_time_password_change.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        update_user_info(request)
        pwd_policy = pwd_attribute(global_variables.GLOBAL_CLIENT)
        password_change_form = PasswordChangeForm(request.user, request.POST)

        if password_change_form.is_valid():
            old_password = request.POST.get('old_password')
            new_password1 = request.POST.get('new_password1')
            if old_password == new_password1:
                msgid = 'MSG119'
                error_msg = get_message_desc(msgid)[1]

            return JsonResponse({'error_message': error_msg}, status=400)

            if not (pwd_policy == ['No Password Policy']):
                if not (re.match((pwd_policy[0]), new_password1)):
                    return JsonResponse({'error_message': pwd_policy[1]}, status=400)

            user = password_change_form.save()
            update_session_auth_hash(request, user)  # Important!
            msgid = 'MSG120'
            error_msg = get_message_desc(msgid)[1]
            m
            return JsonResponse({'success_message': error_msg}, status=200)

        else:
            msgid = 'MSG122'
            error_msg = get_message_desc(msgid)[1]

            return JsonResponse({'error_message': error_msg}, status=400)


def forgot_password(request):
    if request.method == 'POST' and request.is_ajax():
        # update_user_info(request)
        client_val = 700
        pwd_policy = pwd_attribute(client_val)
        # print(client_val)
        password_set_form = SetPasswordForm(request.user, request.POST)

        if password_set_form.is_valid():
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            if new_password2 == new_password1:
                msgid = 'MSG119'
                error_msg = get_message_desc(msgid)[1]

            return JsonResponse({'error_message': error_msg}, status=400)

            if not (pwd_policy == ['No Password Policy']):
                if not (re.match((pwd_policy[0]), new_password1)):
                    return JsonResponse({'error_message': pwd_policy[1]}, status=400)

            user = password_set_form.save()
            update_session_auth_hash(request, user)  # Important!
            msgid = 'MSG120'
            error_msg = get_message_desc(msgid)[1]

            return JsonResponse({'success_message': error_msg}, status=200)

        else:
            msgid = 'MSG122'
            error_msg = get_message_desc(msgid)[1]

            return JsonResponse({'error_message': error_msg}, status=400)
