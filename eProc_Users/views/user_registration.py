"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    user_registration.py
Usage:
    Saves the data for new user registration
    register_page : Get the form and the data from UI which user has entered  and saves the data to DB,returning the user_register.html page.
Author:
    Soni Vydyula
"""
import random
import string

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages

from eProc_Basic.Utilities.constants.constants import CONST_PWD
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.functions.randam_generator import random_alpha_numeric
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG017
from eProc_Configuration.models import Currency, Languages, TimeZone
from eProc_Registration.Utilities.registration_specific import RegFncts
from eProc_Registration.Registration_Forms.user_registration_form import RegForm

# Initializing message class from message.py
from eProc_Registration.models import UserData
from eProc_Shopping_Cart.context_processors import update_user_info

django_query_instance = DjangoQueries()


@login_required
@transaction.atomic
def register_page(request):
    """
    :param request: Request data from UI
    :return: render user_register.html
    """
    global error_msg
    message_desc = ''
    update_user_info(request)
    reg_form = RegForm()
    msg_flag = 0
    msg_response = ''
    if request.method == 'POST':
        reg_form = RegForm(request.POST or None)
        if reg_form.is_valid():
            new_user = reg_form.save(commit=False)
            password = random_alpha_numeric(8)
            new_user.password = make_password(password)
            new_user.password2 = make_password(password)
            emp_id = request.POST['employee_id']
            if django_query_instance.django_existence_check(UserData,
                                                            {'employee_id': emp_id,
                                                             'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT}):
                message_desc = get_message_desc('MSG205')[1]
                messages.error(request, message_desc)
                msg_response = message_desc
                msg_flag = 1
            else:
                is_created = RegFncts.create_user(request, new_user, global_variables.GLOBAL_CLIENT, password)
                if is_created:
                    message_desc = get_message_desc('MSG017')[1]
                messages.success(request, message_desc)
                msg_flag = 0
                msg_response = message_desc
                return redirect('eProc_Users:update_user_basic_details')
        else:
            msg_flag = 1

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'reg_form': reg_form,
        'currency_list': django_query_instance.django_filter_query(Currency, {'del_ind': False}, None,
                                                                   ['currency_id', 'description']),
        'language_list': django_query_instance.django_filter_query(Languages, {'del_ind': False}, None,
                                                                   ['language_id', 'description']),
        'time_zone': django_query_instance.django_filter_query(TimeZone, {'del_ind': False}, None,
                                                               ['time_zone', 'description']),
        'msg_flag': msg_flag,
        'msg_response': msg_response,
        'user_action': 'CREATE'
    }

    return render(request, 'Display Edit User/display_edit_user.html', context)
