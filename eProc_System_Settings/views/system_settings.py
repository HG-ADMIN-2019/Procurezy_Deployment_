from django.http import JsonResponse
from django.shortcuts import render
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.Utilities.application_settings_specific import SystemSettingConfig
from eProc_Configuration.models import SystemSettingsConfig
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Basic.Utilities.functions.get_db_query import django_query_instance


def system_settings_new(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    password_policy = django_query_instance.django_filter_only_query(SystemSettingsConfig, {
        'client': client, 'del_ind': False, 'sys_attr_type': 'PWD_POLICY'
    })
    login_attempts = django_query_instance.django_filter_only_query(SystemSettingsConfig, {
        'client': client, 'del_ind': False, 'sys_attr_type': 'LOGIN_ATTEMPTS'
    })
    session_timeout = django_query_instance.django_filter_only_query(SystemSettingsConfig, {
        'client': client, 'del_ind': False, 'sys_attr_type': 'SESSION_TIMEOUT'
    })
    msg_display = django_query_instance.django_filter_only_query(SystemSettingsConfig, {
        'client': client, 'del_ind': False, 'sys_attr_type': 'MSG_DISPLAY'
    })
    theme_color = django_query_instance.django_filter_only_query(SystemSettingsConfig, {
        'client': client, 'del_ind': False, 'sys_attr_type': 'THEME_COLOUR'
    })
    pagination_count = django_query_instance.django_filter_only_query(SystemSettingsConfig, {
        'client': client, 'del_ind': False, 'sys_attr_type': 'PAGINATION_COUNT'
    })
    attachment_size = django_query_instance.django_filter_only_query(SystemSettingsConfig, {
        'client': client, 'del_ind': False, 'sys_attr_type': 'ATTACHMENT_SIZE'
    })
    attachment_extension = django_query_instance.django_filter_only_query(SystemSettingsConfig, {
        'client': client, 'del_ind': False, 'sys_attr_type': 'ATTACHMENT_EXTENSION'
    })
    acct_assignment_category = django_query_instance.django_filter_value_list_query(SystemSettingsConfig, {
        'client': client, 'del_ind': False, 'sys_attr_type': 'ACCOUNT_ASSIGNMENT_CATEGORY',
        'sys_settings_default_flag': True
    }, 'sys_attr_value')
    purchase_group = django_query_instance.django_filter_value_list_query(SystemSettingsConfig, {
        'client': client, 'del_ind': False, 'sys_attr_type': 'PURCHASE_GROUPS', 'sys_settings_default_flag': True
    }, 'sys_attr_value')
    edit_address = django_query_instance.django_filter_value_list_query(SystemSettingsConfig, {
        'client': client, 'del_ind': False, 'sys_attr_type': 'EDIT_ADDRESS', 'sys_settings_default_flag': True
    }, 'sys_attr_value')
    recently_viewed_items = django_query_instance.django_filter_value_list_query(SystemSettingsConfig, {
        'client': client, 'del_ind': False, 'sys_attr_type': 'RECENTLY_VIEWED_ITEMS', 'sys_settings_default_flag': True
    }, 'sys_attr_value')
    frequently_purchased_items = django_query_instance.django_filter_value_list_query(SystemSettingsConfig, {
        'client': client, 'del_ind': False, 'sys_attr_type': 'FREQUENTLY_PURCHASED_ITEMS',
        'sys_settings_default_flag': True
    }, 'sys_attr_value')
    change_shipping_address = django_query_instance.django_filter_value_list_query(SystemSettingsConfig, {
        'client': client, 'del_ind': False, 'sys_attr_type': 'CHANGE_SHIPPING_ADDRESS',
        'sys_settings_default_flag': True
    }, 'sys_attr_value')
    limit_item = django_query_instance.django_filter_value_list_query(SystemSettingsConfig, {
        'client': client, 'del_ind': False, 'sys_attr_type': 'LIMIT_ITEM',
        'sys_settings_default_flag': True
    }, 'sys_attr_value')
    add_favourites = django_query_instance.django_filter_value_list_query(SystemSettingsConfig, {
        'client': client, 'del_ind': False, 'sys_attr_type': 'ADD_TO_FAVOURITES',
        'sys_settings_default_flag': True
    }, 'sys_attr_value')
    system_settings_instance = list(
        SystemSettingsConfig.objects.filter(client=client, del_ind=False, sys_settings_default_flag=True).values(
            'system_settings_config_guid', 'sys_attr_type',
            'sys_attr_value', 'sys_settings_default_flag'))
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_system_settings_active': True,
        'system_settings_instance': system_settings_instance,
        'password_policy': password_policy,
        'login_attempts': login_attempts,
        'session_timeout': session_timeout,
        'msg_display': msg_display,
        'theme_color': theme_color,
        'pagination_count': pagination_count,
        'attachment_size': attachment_size,
        'attachment_extension': attachment_extension,
        'acct_assignment_category': acct_assignment_category,
        'purchase_group': purchase_group,
        'edit_address': edit_address,
        'recently_viewed_items': recently_viewed_items,
        'frequently_purchased_items': frequently_purchased_items,
        'change_shipping_address': change_shipping_address,
        'limit_item': limit_item,
        'add_favourites': add_favourites,
    }
    if request.method == "POST" and request.is_ajax():
        system_setting_config_instance = SystemSettingConfig(client)
        sys_settings_data = JsonParser().get_json_from_req(request)
        filter_query = django_query_instance.django_filter_only_query(SystemSettingsConfig, {
            'client': client, 'del_ind': False
        })
        filter_query.update(sys_settings_default_flag=False)
        pwd_policy = sys_settings_data['pwd_policy']
        system_setting_config_instance.update_system_attributes(pwd_policy, 'PWD_POLICY')
        login_attempts = sys_settings_data['login_attempts']
        system_setting_config_instance.update_system_attributes(login_attempts, 'LOGIN_ATTEMPTS')
        session_timeout = sys_settings_data['session_timeout']
        system_setting_config_instance.update_system_attributes(session_timeout, 'SESSION_TIMEOUT')
        msg_display = sys_settings_data['msg_display']
        system_setting_config_instance.update_system_attributes(msg_display, 'MSG_DISPLAY')
        theme_color = sys_settings_data['theme_color']
        system_setting_config_instance.update_system_attributes(theme_color, 'THEME_COLOR')
        pagination_count = sys_settings_data['pagination_count']
        system_setting_config_instance.update_system_attributes(pagination_count, 'PAGINATION_COUNT')
        attachment_size = sys_settings_data['attachment_size']
        system_setting_config_instance.update_system_attributes(attachment_size, 'ATTACHMENT_SIZE')
        attachment_extension = sys_settings_data['attachment_extension']
        system_setting_config_instance.update_system_attributes(attachment_extension, 'ATTACHMENT_EXTENSION')
        acct_assignment_category = sys_settings_data['acct_assignment_category']
        system_setting_config_instance.update_system_attributes(acct_assignment_category, 'ACCOUNT_ASSIGNMENT_CATEGORY')
        purchase_group = sys_settings_data['purchase_group']
        system_setting_config_instance.update_system_attributes(purchase_group, 'PURCHASE_GROUPS')
        edit_address = sys_settings_data['edit_address']
        system_setting_config_instance.update_system_attributes(edit_address, 'EDIT_ADDRESS')
        recently_viewed_items = sys_settings_data['recently_viewed_items']
        system_setting_config_instance.update_system_attributes(recently_viewed_items, 'RECENTLY_VIEWED_ITEMS')
        frequently_purchased_items = sys_settings_data['frequently_purchased_items']
        system_setting_config_instance.update_system_attributes(frequently_purchased_items,
                                                                'FREQUENTLY_PURCHASED_ITEMS')
        change_shipping_address = sys_settings_data['change_shipping_address']
        system_setting_config_instance.update_system_attributes(change_shipping_address,
                                                                'CHANGE_SHIPPING_ADDRESS')
        add_favourites = sys_settings_data['add_favourites']
        system_setting_config_instance.update_system_attributes(add_favourites,
                                                                'ADD_TO_FAVOURITES')
        limit_item = sys_settings_data['limit_item']
        system_setting_config_instance.update_system_attributes(limit_item, 'LIMIT_ITEM')
        error_msg = get_message_desc('MSG112')[1]
        return JsonResponse({'success_message': error_msg})
    return render(request, 'System_Settings/system_settings_new.html', context)
