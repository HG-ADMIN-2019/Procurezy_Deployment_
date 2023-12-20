from django.db.models import Max
from django.shortcuts import render
from eProc_Basic.Utilities.constants.constants import CONST_DOC_TYPE_SC, CONST_DEFAULT_CLIENT, CONST_DOC_TYPE_FC, \
    CONST_DOC_TYPE_PO, CONST_DOC_TYPE_CONF, CONST_COFIG_UI_MESSAGE_LIST
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients, get_country_data
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.Utilities.application_settings_generic import get_configuration_data, get_product_criteria, \
    get_unspsc_data, get_ui_messages
from eProc_Configuration.models import *

from eProc_Configuration.views import weekday
from eProc_Shopping_Cart.context_processors import update_user_info

django_query_instance = DjangoQueries()


def upload_clients(request):
    upload_client = get_configuration_data(OrgClients, {'del_ind': False}, ['client', 'description'])
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    return render(request, 'Application_Settings/upload_clients.html',
                  {'upload_clients': upload_client,
                   'messages_list': messages_list,
                   'inc_nav': True})


def upload_document_type(request):
    upload_doc_type = django_query_instance.django_filter_query(DocumentType, {'del_ind': False}, None,
                                                                ['document_type', 'document_type_desc'])
    dropdown_db_values = list(
        FieldTypeDescription.objects.filter(field_name='document_type', used_flag=False, del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values(
            'field_type_id',
            'field_type_desc'
        ))

    dropdown_db_values_onload = list(
        FieldTypeDescription.objects.filter(field_name='document_type', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'
                                                                                          ))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)

    return render(request, 'Application_Settings/upload_document_type.html',
                  {'upload_document_type': upload_doc_type,
                   'inc_nav': True,
                   'dropdown_db_values': dropdown_db_values,
                   'dropdown_db_values_onload': dropdown_db_values_onload,
                   'messages_list': messages_list})


def upload_acc_assign_categories(request):
    client = getClients(request)
    upload_account_assign_cat = get_configuration_data(AccountAssignmentCategory, {'del_ind': False},
                                                       ['account_assign_cat', 'description'])
    for acccat_fd in upload_account_assign_cat:
        if not django_query_instance.django_existence_check(DetermineGLAccount,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'account_assign_cat': acccat_fd['account_assign_cat'],
                                                             'del_ind': False}):
            acccat_fd["del_ind_flag"] = False
        else:
            acccat_fd["del_ind_flag"] = True
    dropdown_acct_assmt_values = list(
        FieldTypeDescription.objects.filter(field_name='acct_assignment_category', del_ind=False, used_flag=0,
                                            client=global_variables.GLOBAL_CLIENT).values(
            'field_type_id',
            'field_type_desc'
        ))
    dropdown_acct_assmt_values_onload = list(
        FieldTypeDescription.objects.filter(field_name='acct_assignment_category', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values(
            'field_type_id',
            'field_type_desc'
        ))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    # application_settings = 'application_settings'
    return render(request, 'Application_Settings/upload_acc_assign_categories.html',
                  {'upload_acc_assign_categories': upload_account_assign_cat,
                   'inc_nav': True,
                   'dropdown_acct_assmt_values': dropdown_acct_assmt_values,
                   'dropdown_acct_assmt_values_onload': dropdown_acct_assmt_values_onload,
                   'messages_list': messages_list})


def upload_po_split_criteria(request):
    update_user_info(request)
    response = get_product_criteria()

    # upload_data_company.insert(0,'*')
    # application_settings = 'application_settings'
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    return render(request, 'Application_Settings/po_split_criteria.html',
                  {'upload_acc_assign_categories': response['upload_account_assign_cat'],
                   'inc_nav': True,
                   'po_split_typ': response['po_split_typ'],
                   'dropdown_activate': response['dropdown_activate'],
                   'upload_data_company': response['upload_data_company'],
                   'messages_list': messages_list})


def upload_po_split_type(request):
    client = getClients(request)
    upload_account_assign_cat = get_configuration_data(PoSplitType, {'del_ind': False},
                                                       ['po_split_type', 'po_split_type_desc'])
    for potyp_fd in upload_account_assign_cat:
        if not django_query_instance.django_existence_check(PoSplitCriteria,
                                                            {'client': client,
                                                             'po_split_type': potyp_fd['po_split_type'],
                                                             'del_ind': False}):
            potyp_fd["del_ind_flag"] = False
        else:
            potyp_fd["del_ind_flag"] = True
    dropdown_acct_assmt_values = list(
        FieldTypeDescription.objects.filter(field_name='split_type', del_ind=False, used_flag=0,
                                            client=global_variables.GLOBAL_CLIENT).values(
            'field_type_id',
            'field_type_desc'
        ))
    dropdown_acct_assmt_values_onload = list(
        FieldTypeDescription.objects.filter(field_name='split_type', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values(
            'field_type_id',
            'field_type_desc'
        ))

    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    # application_settings = 'application_settings'
    return render(request, 'Application_Settings/po_split_type.html',
                  {'upload_acc_assign_categories': upload_account_assign_cat,
                   'inc_nav': True,
                   'dropdown_acct_assmt_values': dropdown_acct_assmt_values,
                   'dropdown_acct_assmt_values_onload': dropdown_acct_assmt_values_onload,
                   'messages_list': messages_list})


def display_purchase_control(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT

    upload_purchase_control = get_configuration_data(PurchaseControl, {'del_ind': False, 'client': client},
                                                     ['purchase_control_guid', 'company_code_id', 'call_off',
                                                      'prod_cat_id', 'purchase_ctrl_flag'])
    call_off_data = [
        {'value': '01', 'desc': '01-Catalog'},
        {'value': '02', 'desc': '02-Free text'},
        {'value': '03', 'desc': '03-PR'},
        {'value': '04', 'desc': '04-Limit'}
    ]

    for item in upload_purchase_control:
        call_off_value = item['call_off']
        for call_off_item in call_off_data:
            if call_off_item['value'] == call_off_value:
                item['call_off'] = call_off_item['desc']
                break

    dropdown_activate = list(
        FieldTypeDescription.objects.filter(field_name='purchase_ctrl_flag', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values(
            'field_type_id',
            'field_type_desc'
        ))

    upload_comapny_code = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))

    prod_catogories = list(
        UnspscCategoriesCust.objects.filter(del_ind=False).values('prod_cat_id'))

    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)

    return render(request, 'Application_Settings/purchase_control.html',
                  {'display_purchase_control': upload_purchase_control,
                   'dropdown_company_code_id': upload_comapny_code,
                   'dropdown_call_off': call_off_data,
                   'prod_catogories': prod_catogories,
                   'dropdown_activate': dropdown_activate,
                   'messages_list': messages_list,
                   'inc_nav': True, })


def display_sourcing_rule_generic(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT

    upload_sr_generic_cat = get_configuration_data(SourcingRule, {'del_ind': False},
                                                   ['prod_cat_id_from', 'prod_cat_id_to', 'company_id', 'call_off',
                                                    'rule_type', 'sourcing_flag', 'sourcing_rule_guid', 'del_ind'])

    call_off_data = [
        {'value': '01', 'desc': '01-Catalog'},
        {'value': '02', 'desc': '02-Free text'},
        {'value': '03', 'desc': '03-PR'},
        {'value': '04', 'desc': '04-Limit'}
    ]

    for item in upload_sr_generic_cat:
        call_off_value = item['call_off']
        for call_off_item in call_off_data:
            if call_off_item['value'] == call_off_value:
                item['call_off'] = call_off_item['desc']
                break

    upload_comapny_code = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))

    prod_catogories = list(
        UnspscCategoriesCust.objects.filter(del_ind=False).values('prod_cat_id'))

    rule_type = list(
        FieldTypeDescription.objects.filter(field_name='source_rule', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values(
            'field_type_id',
            'field_type_desc'
        ))

    dropdown_activate = list(
        FieldTypeDescription.objects.filter(field_name='sourcing_flag', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values(
            'field_type_id',
            'field_type_desc'
        ))

    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)

    return render(request, 'Application_Settings/sr_generic.html',
                  {'upload_sr_generic_cat': upload_sr_generic_cat,
                   'dropdown_company_code_id': upload_comapny_code,
                   'prod_catogories': prod_catogories,
                   'rule_type': rule_type,
                   'dropdown_activate': dropdown_activate,
                   'messages_list': messages_list,
                   'inc_nav': True, })


def display_sourcing_mapping_specific(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT

    upload_sr_specific = get_configuration_data(SourcingMapping, {'del_ind': False},
                                                ['prod_cat_id', 'company_id', 'rule_type', 'product_id',
                                                'sourcing_mapping_guid', 'del_ind'])

    upload_company_code = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))

    prod_catogories = list(
        UnspscCategoriesCust.objects.filter(del_ind=False).values('prod_cat_id'))

    rule_type = list(
        FieldTypeDescription.objects.filter(field_name='source_rule', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values(
            'field_type_id',
            'field_type_desc'
        ))

    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)

    return render(request, 'Application_Settings/sm_specific.html',
                  {'upload_sr_specific': upload_sr_specific,
                   'prod_catogories': prod_catogories,
                   'dropdown_company_code_id': upload_company_code,
                   'rule_type': rule_type,
                   'messages_list': messages_list,
                   'inc_nav': True, })


def display_calendar(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT

    country_list = get_country_data()
    val_dict = ''
    messages_list = ''
    calender_data = django_query_instance.django_filter_query(CalenderConfig,
                                                              {'del_ind': False, 'client': client},
                                                              None,
                                                              ['calender_config_guid', 'calender_id', 'description',
                                                               'year', 'working_days', 'country_code'])
    # calender_data = list(
    #     CalenderConfig.objects.filter(del_ind=False).values('calender_config_guid', 'calender_id', 'description',
    #                                                         'year', 'working_days', 'country_code'))
    country_code = list(CalenderConfig.objects.filter(del_ind=False).values_list('country_code', flat=True))
    country_desc = django_query_instance.django_filter_query(Country,
                                                             {'country_code__in': country_code,
                                                              'del_ind': False},
                                                             None, None)

    var1 = []
    var2 = []
    for calender in calender_data:
        for country in country_desc:
            if calender['country_code'] == country['country_code']:
                if country['country_name']:
                    calender['country_desc'] = country['country_name']
                else:
                    calender['country_desc'] = country['country_code']
        # for i in range(len(calender['working_days'])):
        res_array = []

        for cw in calender['working_days']:
            if not cw == ',':
                res_array.append(weekday(cw))
                val_dict = {'value': res_array}
        var1.append(res_array)
        var2.append(val_dict)
        calender['wday_array'] = res_array
        messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)

    return render(request, 'Application_Settings/calendar_settings.html',
                  {'calendar_data': calender_data,
                   'messages_list': messages_list,
                   'country_list': country_list,
                   'inc_nav': True,
                   })


def number_range_shopping_cart(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT

    upload_numberrange = get_configuration_data(NumberRanges,
                                                {'client': client, 'document_type': CONST_DOC_TYPE_SC,
                                                 'del_ind': False},
                                                ['guid', 'sequence', 'starting',
                                                 'ending', 'current'])
    for squence_fd in upload_numberrange:
        if not django_query_instance.django_existence_check(TransactionTypes,
                                                            {'client': client,
                                                             'sequence': squence_fd['sequence'],
                                                             'document_type': CONST_DOC_TYPE_SC,
                                                             'del_ind': False}):
            squence_fd["del_ind_flag"] = False
        else:
            squence_fd["del_ind_flag"] = True
    sequence = NumberRanges.objects.filter(client=client, document_type=CONST_DOC_TYPE_SC, del_ind=False).aggregate(
        Max('sequence'))
    sequence_max = sequence['sequence__max']

    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)

    application_settings = 'application_settings'
    return render(request, 'Shop_Number_Ranges/shopping_cart/shopping_cart_number_range.html',
                  {'upload_numberrange': upload_numberrange, 'application_settings': application_settings,
                   'sequence': sequence_max,
                   'messages_list': messages_list,
                   'inc_nav': True})


def number_range_favourite_cart(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT

    upload_numberrange = get_configuration_data(NumberRanges,
                                                {'client': client, 'document_type': CONST_DOC_TYPE_FC,
                                                 'del_ind': False},
                                                ['guid', 'sequence', 'starting',
                                                 'ending', 'current'])
    for squence_fd in upload_numberrange:
        if not django_query_instance.django_existence_check(TransactionTypes,
                                                            {'client': client,
                                                             'sequence': squence_fd['sequence'],
                                                             'document_type': CONST_DOC_TYPE_FC,
                                                             'del_ind': False}):
            squence_fd["del_ind_flag"] = False
        else:
            squence_fd["del_ind_flag"] = True

    upload_transactiontype = list(
        TransactionTypes.objects.filter(client=client, document_type=CONST_DOC_TYPE_FC, del_ind=False).values(
            'sequence'))

    sequence = NumberRanges.objects.filter(client=client, document_type=CONST_DOC_TYPE_FC, del_ind=False).aggregate(
        Max('sequence'))
    sequence_max = sequence['sequence__max']
    application_settings = 'application_settings'
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    return render(request, 'Shop_Number_Ranges/favourite_cart/favourite_cart_number_range.html',
                  {'upload_numberrange': upload_numberrange, 'application_settings': application_settings,
                   'upload_transactiontype': upload_transactiontype,
                   'sequence': sequence_max,
                   'inc_nav': True,
                   'messages_list': messages_list,
                   })


def number_range_purchase_order(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT

    upload_numberrange = get_configuration_data(NumberRanges,
                                                {'client': client, 'document_type': CONST_DOC_TYPE_PO,
                                                 'del_ind': False},
                                                ['guid', 'sequence', 'starting',
                                                 'ending', 'current'])
    for squence_fd in upload_numberrange:
        if not django_query_instance.django_existence_check(TransactionTypes,
                                                            {'client': client,
                                                             'sequence': squence_fd['sequence'],
                                                             'document_type': CONST_DOC_TYPE_PO,
                                                             'del_ind': False}):
            squence_fd["del_ind_flag"] = False
        else:
            squence_fd["del_ind_flag"] = True

    sequence = NumberRanges.objects.filter(client=client, document_type=CONST_DOC_TYPE_PO, del_ind=False).aggregate(
        Max('sequence'))
    sequence_max = sequence['sequence__max']
    application_settings = 'application_settings'
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    return render(request, 'Shop_Number_Ranges/purchase_orders/purchase_orders_number_range.html',
                  {'upload_numberrange': upload_numberrange, 'application_settings': application_settings,
                   'sequence': sequence_max,
                   'messages_list': messages_list,
                   'inc_nav': True})
    # client = getClients(request)
    # upload_numberrange_po = list(
    #     NumberRanges.objects.filter(client=client, document_type="DOC05", del_ind=False).values('guid', 'sequence',
    #                                                                                             'starting', 'ending',
    #                                                                                             'current'))
    # application_settings = 'application_settings'
    # return render(request,
    #               'Shop_Number_Ranges/purchase_orders/purchase_orders_number_range.html',
    #               {'upload_numberrange': upload_numberrange_po, 'application_settings': application_settings,
    #                'inc_nav': True})


def number_range_goods_verification(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT

    upload_numberrange_gv = list(
        NumberRanges.objects.filter(client=client, document_type=CONST_DOC_TYPE_CONF, del_ind=False).values('guid',
                                                                                                            'sequence',
                                                                                                            'starting',
                                                                                                            'ending',
                                                                                                            'current'))
    for squence_fd in upload_numberrange_gv:
        if not django_query_instance.django_existence_check(TransactionTypes,
                                                            {'client': client,
                                                             'sequence': squence_fd['sequence'],
                                                             'document_type': CONST_DOC_TYPE_CONF,
                                                             'del_ind': False}):
            squence_fd["del_ind_flag"] = False
        else:
            squence_fd["del_ind_flag"] = True

    sequence = NumberRanges.objects.filter(client=client, document_type=CONST_DOC_TYPE_CONF, del_ind=False).aggregate(
        Max('sequence'))
    sequence_max = sequence['sequence__max']
    application_settings = 'application_settings'
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    return render(request,
                  'Shop_Number_Ranges/goods_verification/goods_verification_number_range.html',
                  {'upload_numberrange': upload_numberrange_gv, 'application_settings': application_settings,
                   'sequence': sequence_max,
                   'messages_list': messages_list,
                   'inc_nav': True})


def display_holidays(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT

    country_list = get_country_data()
    calender_data = list(
        CalenderConfig.objects.filter(client=client, del_ind=False).values('calender_config_guid', 'calender_id',
                                                                           'description',
                                                                           'year', 'working_days', 'country_code'))
    holidays_data = list(
        CalenderHolidays.objects.filter(client=client, del_ind=False).values('calender_holiday_guid', 'calender_id',
                                                                             'holiday_description', 'from_date',
                                                                             'to_date'))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    return render(request, 'Application_Settings/holiday_calendar.html',
                  {'calendar_data': calender_data, 'country_list': country_list, 'holidays_data': holidays_data,
                   'messages_list': messages_list,
                   'inc_nav': True})


def display_messages_id(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT

    # message_id_data = list(
    #     MessagesId.objects.filter(del_ind=False, client=client).values('msg_id_guid', 'messages_id', 'messages_type'))
    message_id_data = get_configuration_data(MessagesId, {'del_ind': False, 'client': client},
                                             ['msg_id_guid', 'messages_id', 'messages_type'])
    dropdown_msg_type_values = list(
        FieldTypeDescription.objects.filter(field_name='messages_type', del_ind=False, used_flag=0,
                                            client=global_variables.GLOBAL_CLIENT).values(
            'field_type_id',
            'field_type_desc'
        ))
    dropdown_msg_id_values = list(
        FieldTypeDescription.objects.filter(field_name='messages_id', del_ind=False, used_flag=0,
                                            client=global_variables.GLOBAL_CLIENT).values(
            'field_type_id',
            'field_type_desc'
        ))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    return render(request, 'message_id_config.html',
                  {'message_id_data': message_id_data, 'dropdown_msg_type_values': dropdown_msg_type_values,
                   'dropdown_msg_id_values': dropdown_msg_id_values,
                   'messages_list': messages_list,
                   'inc_nav': True})


def display_messages_desc(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT

    # message_id_desc_data = list(
    #     MessagesIdDesc.objects.filter(del_ind=False, client=client).values('msg_id_desc_guid', 'messages_id',
    #                                                                        'messages_id_desc',
    #                                                                        'language_id'))
    message_id_desc_data = get_configuration_data(MessagesIdDesc, {'del_ind': False, 'client': client},
                                                  ['msg_id_desc_guid', 'messages_id', 'messages_id_desc',
                                                   'language_id'])
    messages_id_list = list(MessagesId.objects.filter(del_ind=False, client=client).values('messages_id'))
    language_list = list(Languages.objects.filter(del_ind=False).values('language_id', 'description'))
    for msg in message_id_desc_data:
        for lang in language_list:
            if msg['language_id'] == lang['language_id']:
                msg['lang_description'] = lang['description']
        messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    cache_version = int(datetime.now().timestamp())

    return render(request, 'message_id_desc_config.html',
                  {'message_id_desc_data': message_id_desc_data, 'language_list': language_list,
                   'messages_id_list': messages_id_list,
                   'messages_list': messages_list,
                   'inc_nav': True, 'cache_version': cache_version})


def upload_product_category(request):
    upload_product_category = get_unspsc_data()
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)

    return render(request, 'Basic_setting_Upload/upload_product_category.html',
                  {'upload_product_category': upload_product_category,
                   'messages_list': messages_list,
                   'inc_nav': True})


def org_node_types(request):
    client = getClients(request)
    upload_orgnodetypes = list(
        OrgNodeTypes.objects.filter(client=client, del_ind=False).values('node_type_guid', 'node_type', 'description'))

    for node_type_fd in upload_orgnodetypes:
        if django_query_instance.django_existence_check(OrgModelNodetypeConfig,
                                                        {'del_ind': False,
                                                         'node_type': node_type_fd['node_type']}):
            node_type_fd["del_ind_flag"] = False
        else:
            node_type_fd["del_ind_flag"] = True

    upload_dropdown_db_values = list(
        FieldTypeDescription.objects.filter(field_name='org_node_types', used_flag=False, del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values(
            'field_type_id',
            'field_type_desc'
        ))

    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)

    master_data_settings = 'master_data_settings'
    return render(request, 'Organizational_Data/org_node_types.html',
                  {'org_node_types': upload_orgnodetypes, 'master_data_settings': master_data_settings,
                   'upload_dropdown_db_values': upload_dropdown_db_values, 'messages_list': messages_list,
                   'inc_nav': True})


def org_attributes(request):
    upload_orgattributes = list(
        OrgAttributes.objects.filter(del_ind=False).values('attribute_id', 'attribute_name', 'range_indicator',
                                                           'multiple_value', 'allow_defaults', 'inherit_values',
                                                           'maximum_length'))

    for attribute_id_fd in upload_orgattributes:
        if django_query_instance.django_existence_check(OrgModelNodetypeConfig,
                                                        {'del_ind': False,
                                                         'node_values': attribute_id_fd['attribute_id']}):
            attribute_id_fd["del_ind_flag"] = False
        else:
            attribute_id_fd["del_ind_flag"] = True
    upload_dropdown_db_values = list(
        FieldTypeDescription.objects.filter(field_name='attribute_id', used_flag=False, del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'
                                                                                          ))
    upload_dropdown_db_values_onload = list(
        FieldTypeDescription.objects.filter(field_name='attribute_id', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'
                                                                                          ))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    master_data_settings = 'master_data_settings'
    return render(request, 'Organizational_Data/org_attributes.html',
                  {'org_attributes': upload_orgattributes, 'master_data_settings': master_data_settings,
                   'upload_dropdown_db_values': upload_dropdown_db_values,
                   'upload_dropdown_db_values_onload': upload_dropdown_db_values_onload, 'messages_list': messages_list,
                   'inc_nav': True})


def org_attributes_level(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT

    upload_orgattributes_level = django_query_instance.django_filter_query(
        OrgModelNodetypeConfig, {'del_ind': False, 'org_model_types': 'ORG_ATTRIBUTES', 'client': client}, None,
        ['org_model_nodetype_config_guid',
         'node_values', 'node_type'])
    upload_attributesid_dropdown = django_query_instance.django_filter_query(
        OrgAttributes, {'del_ind': False}, None, ['attribute_id'])

    upload_orgnodetypes_dropdown = django_query_instance.django_filter_query(
        OrgNodeTypes, {'client': client, 'del_ind': False}, None, ['node_type'])

    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)

    master_data_settings = 'master_data_settings'
    return render(request, 'Organizational_Data/orgattributes_level.html',
                  {'org_attributes_level': upload_orgattributes_level,
                   'upload_attributesid_dropdown': upload_attributesid_dropdown,
                   'upload_orgnodetypes_dropdown': upload_orgnodetypes_dropdown,
                   'master_data_settings': master_data_settings,
                   'messages_list': messages_list,
                   'inc_nav': True, })


def auth_objects(request):
    upload_authobj = list(
        AuthorizationObject.objects.filter(del_ind=False).values('auth_obj_id', 'auth_level_ID',
                                                                 'auth_level'))
    for authobject_fd in upload_authobj:
        if django_query_instance.django_existence_check(AuthorizationGroup,
                                                        {'del_ind': False,
                                                         'auth_obj_id': authobject_fd['auth_obj_id']}):
            authobject_fd["del_ind_flag"] = False
        else:
            authobject_fd["del_ind_flag"] = True
    auth_obj_id_db_values = list(
        FieldTypeDescription.objects.filter(field_name='auth_obj_id', used_flag=False, del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'))
    auth_obj_id_db_values_onload = list(
        FieldTypeDescription.objects.filter(field_name='auth_obj_id', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'))

    auth_type_db_values = list(
        FieldTypeDescription.objects.filter(field_name='auth_level', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    master_data_settings = 'master_data_settings'
    return render(request, 'Organizational_Data/authorization_objects.html',
                  {'upload_authobj': upload_authobj, 'master_data_settings': master_data_settings,
                   'auth_obj_id_db_values': auth_obj_id_db_values, 'auth_type_db_values': auth_type_db_values,
                   'auth_obj_id_db_values_onload': auth_obj_id_db_values_onload, 'messages_list': messages_list,
                   'inc_nav': True})


def auth_grp(request):
    upload_authgrp = list(
        AuthorizationGroup.objects.filter(del_ind=False).values('auth_grp_guid', 'auth_obj_grp', 'auth_obj_id',
                                                                'auth_grp_desc', 'auth_level'))
    for authgrp_fd in upload_authgrp:
        if django_query_instance.django_existence_check(Authorization,
                                                        {'del_ind': False,
                                                         'auth_obj_grp': authgrp_fd['auth_obj_grp']}):
            authgrp_fd["del_ind_flag"] = False
        else:
            authgrp_fd["del_ind_flag"] = True
    upload_data_AuthorizationGroup = list(
        AuthorizationObject.objects.filter(del_ind=False).values('auth_obj_id', 'auth_level_ID'))

    auth_group_db_values = list(
        FieldTypeDescription.objects.filter(field_name='auth_obj_grp', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'))
    auth_type_db_values = list(
        FieldTypeDescription.objects.filter(field_name='auth_level', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    master_data_settings = 'master_data_settings'
    return render(request, 'Organizational_Data/authorization_group.html',
                  {'auth_grp': upload_authgrp, 'upload_data_AuthorizationGroup': upload_data_AuthorizationGroup,
                   'master_data_settings': master_data_settings, 'auth_group_values': auth_group_db_values,
                   'auth_level_value': auth_type_db_values, 'messages_list': messages_list,
                   'inc_nav': True})


def roles(request):
    client = getClients(request)
    upload_roles = list(UserRoles.objects.filter(del_ind=False).values('role', 'role_desc'))
    for roles_fd in upload_roles:
        if django_query_instance.django_existence_check(Authorization,
                                                        {'del_ind': False,
                                                         'role': roles_fd['role']}):
            roles_fd["del_ind_flag"] = False
        else:
            roles_fd["del_ind_flag"] = True
    dropdown_db_values = list(
        FieldTypeDescription.objects.filter(field_name='roles', del_ind=False, used_flag=0,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'
                                                                                          ))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    master_data_settings = 'master_data_settings'
    return render(request, 'Organizational_Data/roles.html',
                  {'roles': upload_roles, 'master_data_settings': master_data_settings, 'inc_nav': True,
                   'dropdown_db_values': dropdown_db_values, 'messages_list': messages_list})


def auth(request):
    update_user_info(request)
    upload_auth = list(
        Authorization.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('auth_guid',
                                                                                                  'auth_obj_grp',
                                                                                                  'role'))
    upload_data_roles = list(
        FieldTypeDescription.objects.filter(field_name='roles', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'))

    upload_data_auth_grp_obj = list(
        FieldTypeDescription.objects.filter(field_name='auth_obj_grp', used_flag=0, del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'))

    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    master_data_settings = 'master_data_settings'
    return render(request, 'Organizational_Data/authorization.html',
                  {'auth': upload_auth, 'upload_data_roles': upload_data_roles,
                   'upload_data_auth_grp_obj': upload_data_auth_grp_obj,
                   'master_data_settings': master_data_settings,
                   'messages_list': messages_list, 'inc_nav': True})


def transaction_type(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT

    number_range_sequence = []
    document_type_render = list(
        DocumentType.objects.filter(del_ind=False, document_type=CONST_DOC_TYPE_FC).values('document_type'))
    upload_numberrange = list(
        NumberRanges.objects.filter(client=client, document_type=CONST_DOC_TYPE_FC,
                                    del_ind=False).values('sequence'))
    for number_range in upload_numberrange:
        if not django_query_instance.django_existence_check(TransactionTypes,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'sequence': number_range['sequence'],
                                                             'document_type': CONST_DOC_TYPE_FC,
                                                             'del_ind': False}):
            number_range_sequence.append(number_range)
    upload_transactiontype = list(
        TransactionTypes.objects.filter(client=client, document_type=CONST_DOC_TYPE_FC, del_ind=False).values('guid',
                                                                                                              'transaction_type',
                                                                                                              'description',
                                                                                                              'document_type',
                                                                                                              'sequence',
                                                                                                              'active_inactive'))
    rendered_active_inactive = list(
        FieldTypeDescription.objects.filter(field_name='active_inactive', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'))

    rendered_active_inactive_onload = list(
        FieldTypeDescription.objects.filter(field_name='active_inactive', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    application_settings = 'application_settings'
    return render(request,
                  'Transaction_type/Favourite_cart/transaction_type.html',
                  {'transaction_type': upload_transactiontype, 'application_settings': application_settings,
                   'document_type': document_type_render, 'upload_numberrange': number_range_sequence,
                   'rendered_active_inactive': rendered_active_inactive,
                   'rendered_active_inactive_onload': rendered_active_inactive_onload, 'messages_list': messages_list,
                   'inc_nav': True})


def transaction_type_sc(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT

    number_range_sequence = []
    document_type_render = list(
        DocumentType.objects.filter(del_ind=False, document_type=CONST_DOC_TYPE_SC).values('document_type'))
    upload_numberrange = list(
        NumberRanges.objects.filter(client=client, document_type=CONST_DOC_TYPE_SC,
                                    del_ind=False).values('sequence'))
    for number_range in upload_numberrange:
        if not django_query_instance.django_existence_check(TransactionTypes,
                                                            {'client': client,
                                                             'sequence': number_range['sequence'],
                                                             'document_type': CONST_DOC_TYPE_SC,
                                                             'del_ind': False}):
            number_range_sequence.append(number_range)

    upload_transactiontype = list(
        TransactionTypes.objects.filter(client=client, document_type=CONST_DOC_TYPE_SC,
                                        del_ind=False).values('guid',
                                                              'transaction_type',
                                                              'description',
                                                              'document_type',
                                                              'sequence',
                                                              'active_inactive'))
    rendered_active_inactive = list(
        FieldTypeDescription.objects.filter(field_name='active_inactive', del_ind=False,
                                            client=client).values('field_type_id',
                                                                  'field_type_desc'))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    application_settings = 'application_settings'
    return render(request,
                  'Transaction_type/Shopping_cart/transaction_type.html',
                  {'transaction_type': upload_transactiontype, 'application_settings': application_settings,
                   'document_type': document_type_render, 'upload_numberrange': number_range_sequence,
                   'rendered_active_inactive': rendered_active_inactive, 'messages_list': messages_list,
                   'inc_nav': True})


def transaction_type_po(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT

    number_range_sequence = []
    document_type_render = list(
        DocumentType.objects.filter(del_ind=False, document_type=CONST_DOC_TYPE_PO).values('document_type'))
    upload_numberrange = list(
        NumberRanges.objects.filter(client=client, document_type=CONST_DOC_TYPE_PO,
                                    del_ind=False).values('sequence'))

    for number_range in upload_numberrange:
        if not django_query_instance.django_existence_check(TransactionTypes,
                                                            {'client': client,
                                                             'sequence': number_range['sequence'],
                                                             'document_type': CONST_DOC_TYPE_PO,
                                                             'del_ind': False}):
            number_range_sequence.append(number_range)

    upload_transactiontype = list(
        TransactionTypes.objects.filter(client=client, document_type=CONST_DOC_TYPE_PO,
                                        del_ind=False).values('guid',
                                                              'transaction_type',
                                                              'description',
                                                              'document_type',
                                                              'sequence',
                                                              'active_inactive'))
    rendered_active_inactive = list(
        FieldTypeDescription.objects.filter(field_name='active_inactive', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    application_settings = 'application_settings'
    return render(request,
                  'Transaction_type/Purchase_order/transaction_type.html',
                  {'transaction_type': upload_transactiontype, 'application_settings': application_settings,
                   'document_type': document_type_render, 'upload_numberrange': number_range_sequence,
                   'rendered_active_inactive': rendered_active_inactive, 'messages_list': messages_list,
                   'inc_nav': True})


def transaction_type_gv(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT

    number_range_sequence = []
    document_type_render = list(
        DocumentType.objects.filter(del_ind=False, document_type=CONST_DOC_TYPE_CONF).values('document_type'))
    upload_numberrange = list(
        NumberRanges.objects.filter(client=client, document_type=CONST_DOC_TYPE_CONF,
                                    del_ind=False).values('sequence'))
    for number_range in upload_numberrange:
        if not django_query_instance.django_existence_check(TransactionTypes,
                                                            {'client': client,
                                                             'sequence': number_range['sequence'],
                                                             'document_type': CONST_DOC_TYPE_SC,
                                                             'del_ind': False}):
            number_range_sequence.append(number_range)

    upload_transactiontype = list(
        TransactionTypes.objects.filter(client=client, document_type=CONST_DOC_TYPE_CONF,
                                        del_ind=False).values('guid',
                                                              'transaction_type',
                                                              'description',
                                                              'document_type',
                                                              'sequence',
                                                              'active_inactive'))
    rendered_active_inactive = list(
        FieldTypeDescription.objects.filter(field_name='active_inactive', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    application_settings = 'application_settings'
    return render(request,
                  'Transaction_type/Goods_verfication/transaction_type.html',
                  {'transaction_type': upload_transactiontype, 'application_settings': application_settings,
                   'document_type': document_type_render, 'upload_numberrange': number_range_sequence,
                   'rendered_active_inactive': rendered_active_inactive, 'messages_list': messages_list,
                   'inc_nav': True})
