"""Copyright (c) 2020 Hiranya Garbha, Inc.
    Name:
        user_details.py
    Usage:
        Story SP12-10
        Function to get the user details
        Taking the user email id and getting details and rendering back to the user details page

     Author:
        Varsha Prasad
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from eProc_Basic.Utilities.constants.constants import CONST_DECIMAL_NOTATION, CONST_DATE_FORMAT, CONST_USER_REG
from eProc_Basic.Utilities.functions.camel_case import convert_to_camel_case
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import decrypt, encrypt
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.functions.randam_generator import random_alpha_numeric
from eProc_Basic.Utilities.messages.messages import MSG183
from eProc_Configuration.models import *
from eProc_Emails.Utilities.email_notif_generic import email_notify
from eProc_Registration.Registration_Forms.user_registration_form import RegForm
from eProc_Registration.Utilities.registration_specific import RegFncts
from eProc_Registration.models import UserData
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import convert_to_boolean
from eProc_Shopping_Cart.context_processors import update_user_info

django_query_instance = DjangoQueries()


@login_required()
@transaction.atomic
def update_user_basic_details(request):
    message = ''
    update_user_info(request)
    if request.method == 'POST':
        message, encrypted_user, msg_type = save_user_data(request)

        return JsonResponse({'message': message, 'encrypted_user': encrypted_user, 'msg_type': msg_type})


def save_user_data(request):
    """

    """
    message = {}
    user_details = {}
    error_msg = ''
    status = request.POST.get('status')
    user_details['username'] = request.POST.get('username')
    user_details['first_name'] = convert_to_camel_case(request.POST.get('first_name'))
    user_details['last_name'] = convert_to_camel_case(request.POST.get('last_name'))
    user_details['employee_id'] = request.POST.get('employee_id')
    user_details['user_type'] = request.POST.get('user_type')
    user_details['language_id'] = request.POST.get('language_id')
    user_details['currency_id'] = request.POST.get('currency_id')
    user_details['time_zone'] = request.POST.get('time_zone')
    user_details['email'] = request.POST.get('email')
    user_details['phone_num'] = request.POST.get('phone_num')
    user_details['date_format'] = request.POST.get('date_format')
    user_details['decimal_notation'] = request.POST.get('decimal_notation')
    user_details['login_attempts'] = request.POST.get('login_attempts')
    user_details['is_superuser'] = request.POST.get('is_superuser')
    user_details['user_locked'] = request.POST.get('user_locked')
    user_details['pwd_locked'] = request.POST.get('pwd_locked')
    user_details['is_active'] = request.POST.get('is_active')
    encrypted_user = encrypt(user_details['employee_id'])

    if user_details['login_attempts'] == '':
        user_details['login_attempts'] = 0

    if status in ['UPDATE', 'update']:
        if django_query_instance.django_existence_check(UserData,
                                                        {'email': user_details['email'],
                                                         'del_ind': False,
                                                         'client': global_variables.GLOBAL_CLIENT}):
            django_query_instance.django_update_query(UserData,
                                                      {'email': user_details['email'],
                                                       'del_ind': False,
                                                       'client': global_variables.GLOBAL_CLIENT}, user_details)
            msgid = 'MSG183'
            error_msg = get_message_desc(msgid)[1]
            message['type'] = 'success'

            return error_msg, encrypted_user, message
    else:
        if django_query_instance.django_existence_check(UserData,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'username': user_details['username'],
                                                         'del_ind': False}):
            msgid = 'MSG084'
            error_msg = get_message_desc(msgid)[1]

            message['type'] = 'error'
            return error_msg, encrypted_user, message
        elif django_query_instance.django_existence_check(UserData,
                                                          {'client': global_variables.GLOBAL_CLIENT,
                                                           'employee_id': user_details[
                                                               'employee_id'],
                                                           'del_ind': False}):
            msgid = 'MSG205'
            error_msg = get_message_desc(msgid)[1]
            # error_msg = "Username exists"
            message['type'] = 'error'
            return error_msg, encrypted_user, message
        elif django_query_instance.django_existence_check(UserData,
                                                          {'client': global_variables.GLOBAL_CLIENT,
                                                           'email': user_details[
                                                               'email'],
                                                           'del_ind': False}):
            msgid = 'MSG083'
            error_msg = get_message_desc(msgid)[1]
            message['type'] = 'error'
            return error_msg, encrypted_user, message
        else:
            user_details['client'] = global_variables.GLOBAL_CLIENT
            user_details['time_zone'] = django_query_instance.django_get_query(TimeZone, {
                'time_zone': user_details['time_zone']})
            user_details['currency_id'] = django_query_instance.django_get_query(Currency, {
                'currency_id': user_details['currency_id']})
            user_details['language_id'] = django_query_instance.django_get_query(Languages, {
                'language_id': user_details['language_id']})
            password = random_alpha_numeric(8)
            user_details['password'] = password

            reg_form = RegForm(request.POST or None)
            new_user = reg_form.save(commit=False)
            password = random_alpha_numeric(8)
            new_user.password = make_password(password)
            new_user.password2 = make_password(password)

            # ----- create user and send email
            is_created = RegFncts.create_user(request, new_user, global_variables.GLOBAL_CLIENT, password)
            if is_created:
                msgid = 'MSG183'
                error_msg = get_message_desc(msgid)[1]
                message['type'] = 'success'

    return error_msg, encrypted_user, message
