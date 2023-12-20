"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    data_upload.py
Usage:
    on click of User Settings in nav bar dropdown
    purchase_settings - This function handle getting purchase data and render purchase_settings.html
Author:
    Deepika K
"""
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages
from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import *
from django.contrib.auth.decorators import login_required
from eProc_Basic.decorators import authorize_view
from eProc_Configuration.models.development_data import UserRoles
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_User_Settings.Utilities.user_settings_generic import get_object_id_list_user, get_purch_org_detail, \
    get_purch_group_detail
from eProc_User_Settings.Utilities.user_settings_specific import get_org_attr_list, update_or_create_default, \
    update_or_delete_previous_default
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries

django_query_instance = DjangoQueries()


@login_required
@authorize_view(CONST_PURCHASE_SETTINGS)
def purchase_settings(request):
    """
    This function handle getting purchase data
    :param request: request data from UI
    :return: render purchase_settings.html
    """
    update_user_info(request)
    edit_flag = False
    user_setting_list, user_setting_default_list, error_msg, delivery_addr_desc, invoice_addr_desc, \
    company_code_list, company_code_dictionary_list, purchase_org_list, purchase_org_dictionary_list, \
    purchase_group_dictionary_list = get_org_attr_list()

    user_roles_assigned_values = list(
        django_query_instance.django_filter_only_query(UserRoles, {
            'role__in': user_setting_list[8], 'del_ind': False
        }).values('role', 'role_desc')
    )
    user_setting_list.append(user_roles_assigned_values)

    context = {
        'inc_nav': True,
        'shopping': True,
        'user_setting_list': user_setting_list,
        'user_setting_default_list': user_setting_default_list,
        'edit_flag': edit_flag,
        'error_msg': error_msg,
        'is_slide_menu': True,
        'is_personalization_active': True,
        'delivery_addr_desc': delivery_addr_desc,
        'invoice_addr_desc': invoice_addr_desc,
        'company_code_list': company_code_list,
        'company_code_dictionary_list': company_code_dictionary_list,
        'purchase_org_list': purchase_org_list,
        'purchase_org_dictionary_list': purchase_org_dictionary_list,
        'purchase_group_dictionary_list': purchase_group_dictionary_list
    }
    return render(request, 'User_settings/purchase_settings.html', context)


# End of SC-US-US01
# End of SC-US-US02 and SC-US-US03
def save_purchase_settings(request):
    """

    :param request:
    :return:
    """
    update_user_info(request)
    update_default = json.loads(request.POST['update_default'])
    login_user_obj_id = global_variables.GLOBAL_LOGIN_USER_OBJ_ID
    object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT,
                                             global_variables.GLOBAL_LOGIN_USER_OBJ_ID)
    inherite_object_id_list = object_id_list
    inherite_object_id_list.remove(login_user_obj_id)
    for field, field_value in update_default.items():
        if field_value:
            #  For Previous default value
            # 1. if any default is set for login user level then update default flag to False
            # 2. if attribute value already maintained and no exclude in its parent level then delete entry in login
            #    user level
            # 3. if default is not maintained in its parent level then update default flag to False
            update_or_delete_previous_default(field, inherite_object_id_list, login_user_obj_id)

            #  For current default value
            # if attribute value already exists in login user level then update default flag to True
            # if attribute value is not exists in login user level then create new entry in OrgAttributesLevel table
            update_or_create_default(field, field_value, inherite_object_id_list, login_user_obj_id)

    # msgid = 'MSG002'
    # error_msg = get_msg_desc(msgid)
    # msg = error_msg['message_desc'][0]
    # error_msg = msg
    message_desc = get_message_desc('MSG002')[1]
    messages.success(request, message_desc)
    return JsonResponse({'message': message_desc})

    # messages.success(request, MSG002)
    # return JsonResponse({'message': MSG002})


def get_porg_pgrp(request):
    """

    """
    update_user_info(request)
    pgroup_detail = {}
    porg_detail = {}
    onchange_action = request.POST.get('onchange_action')
    selected_drop_down_value = request.POST.get('selected_drop_down_value')
    if onchange_action == "company_code":
        porg_list, porg_detail = get_purch_org_detail(selected_drop_down_value)
        porg_id = porg_list[0]
    else:
        porg_id = selected_drop_down_value
    if porg_id:
        pgroup_detail = get_purch_group_detail(porg_id)
    context = {
        'porg_detail': porg_detail,
        'pgroup_detail': pgroup_detail
    }
    return JsonResponse(context, safe=False)
