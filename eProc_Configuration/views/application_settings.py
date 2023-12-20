"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    application_settings.py
Usage:
     app_setting           - Renders application settings home page where the user is allowed to configure settings
     create_number_ranges  - Creates new number ranges and saves the data to DB through ajax calls
     edit_number_ranges    - Edit number ranges and saves the data to DB through ajax calls
Author:
    Sanjay
"""

import io
import csv
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic_Settings.Utilities.basic_settings_specific import *
from eProc_Configuration.Utilities.application_settings_specific import *
from eProc_Configuration.models import *
from eProc_Configuration_Check.Utilities.configuration_check_generic import *
from eProc_Master_Settings.Utilities.master_settings_specific import *
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Upload.Utilities.upload_data.upload_basic_pk_fk_tables import UploadPkFkTables
from eProc_Upload.Utilities.upload_data.upload_pk_tables import CompareTableHeader, MSG048

JsonParser_obj = JsonParser()
django_query_instance = DjangoQueries()


@login_required
def app_setting(request):
    """
    :param request: Gets the configured number ranges from the database and displays.
    :return: Renders application_settings.html where the user is allowed to create, edit, display the number ranges
    """
    return render(request, 'Application_Settings/application_settings.html')


def app_setting_latest(request):
    """
    :param request: Gets the configured number ranges from the database and displays.
    :return: Renders application_settings.html where the user is allowed to create, edit, display the number ranges
    """
    return render(request, 'Application_Settings/app_settings.html', {'inc_nav': True})


def create_update_application_data(request):
    """

    """
    update_user_info(request)
    app_data = JsonParser_obj.get_json_from_req(request)
    application_settings_save_instance = ApplicationSettingsSave()
    if app_data['table_name'] == 'OrgClients':
        app_data['data'] = check_org_client_data(app_data['data'], 'SAVE')[0]
        display_data = application_settings_save_instance.save_client_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'UnspscCategories':
        app_data['data'] = check_unspsc_data(app_data['data'], 'SAVE')[0]
        display_data = application_settings_save_instance.save_prodcat_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'OrgNodeTypes':
        app_data['data'] = check_node_type_data(app_data['data'], 'SAVE')[0]
        display_data = application_settings_save_instance.save_orgnode_types_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'OrgAttributes':
        app_data['data'] = check_orgattributes_data(app_data['data'], 'SAVE')[0]
        display_data = application_settings_save_instance.save_orgattributes_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'OrgModelNodetypeConfig':
        app_data['data'] = check_nodetype_config_data(app_data['data'], 'SAVE')[0]
        display_data = application_settings_save_instance.save_orgattributes_level_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'AuthorizationObject':
        app_data['data'] = check_authorization_object_data(app_data['data'], 'SAVE')[0]
        display_data = application_settings_save_instance.save_authorobject_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'AuthorizationGroup':
        app_data['data'] = check_authorization_grp_data(app_data['data'], 'SAVE')[0]
        display_data = application_settings_save_instance.save_auth_group_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'UserRoles':
        app_data['data'] = check_user_role_data(app_data['data'], 'SAVE')[0]
        display_data = application_settings_save_instance.save_roles_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'Authorization':
        app_data['data'] = check_authorization_data(app_data['data'], 'SAVE')[0]
        display_data = application_settings_save_instance.save_auth_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'DocumentType':
        app_data['data'] = check_document_type_data(app_data['data'], 'SAVE')[0]
        display_data = application_settings_save_instance.save_documenttype_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'NumberRanges':
        display_data = application_settings_save_instance.save_number_range_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'TransactionTypes':
        display_data = application_settings_save_instance.save_transactiontype_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'AccountAssignmentCategory':
        app_data['data'] = check_acc_data(app_data['data'], 'SAVE')[0]
        display_data = application_settings_save_instance.save_actasmt_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'CalenderConfig':
        app_data['data'] = check_calendar_config_data(app_data['data'], 'SAVE')[0]
        display_data = application_settings_save_instance.save_calendar_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'CalenderHolidays':
        display_data = application_settings_save_instance.save_calendarholiday_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'MessagesId':
        app_data['data'] = check_message_id_data(app_data['data'], 'SAVE')[0]
        display_data = application_settings_save_instance.save_messageId_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'MessagesIdDesc':
        app_data['data'] = check_message_id_desc_data(app_data['data'], 'SAVE')[0]
        display_data = application_settings_save_instance.save_messageIdDesc_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'PoSplitType':
        app_data['data'] = check_po_split_type_data(app_data['data'], 'SAVE')[0]
        display_data = application_settings_save_instance.save_po_split_type_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'PoSplitCriteria':
        app_data['data'] = check_po_split_creteria_data(app_data['data'], 'SAVE')[0]
        display_data = application_settings_save_instance.save_po_split_criteria_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'PurchaseControl':
        app_data['data'] = check_purchase_control_data(app_data['data'], 'SAVE')[0]
        display_data = application_settings_save_instance.save_purchase_control_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'SourcingRule':
        app_data['data'] = check_source_rule_data(app_data['data'], 'SAVE')[0]
        display_data = application_settings_save_instance.save_source_rule_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'SourcingMapping':
        app_data['data'] = check_source_mapping_data(app_data['data'], 'SAVE')[0]
        display_data = application_settings_save_instance.save_source_mapping_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'EmailContents':
        app_data['data'] = check_email_settings_data(app_data['data'], 'SAVE')[0]
        display_data = application_settings_save_instance.save_email_settings_into_db(app_data)
        return JsonResponse(display_data, safe=False)


def save_app_settings_data(request):
    """

    :param request:
    :return:
    """

    update_user_info(request)
    basic_data = JsonParser().get_json_from_req(request)
    Table_name = basic_data['Dbl_clck_tbl_id']
    del basic_data['Dbl_clck_tbl_id']

    basic_data_list = []

    for value in basic_data.values():
        basic_data_list.append(value)
    upload_data_response = {}
    # upload_data_response = save_app_data_into_db(basic_data_list, Table_name, client)
    return JsonResponse(upload_data_response, safe=False)


def data_upload_fk(request):
    db_header = request.POST.get('db_header_data')
    csv_file = request.FILES['file_attach']
    data_set_val = csv_file.read().decode('utf8')
    # fin_upload_data = io.StringIO(data_set_val)
    upload_csv = CompareTableHeader()
    result = {}
    # upload_csv.header_data = io.StringIO(data_set_val)
    upload_csv.app_name = request.POST.get('appname')
    upload_csv.table_name = request.POST.get('Tablename')
    upload_csv.request = request
    fin_data_upload_header = io.StringIO(data_set_val)
    upload_csv.header_data = fin_data_upload_header
    basic_save, header_detail = upload_csv.basic_header_condition()
    # if not basic_save:
    try:
        result['error_message'], result['data'] = upload_csv.csv_preview_data(header_detail, data_set_val)
        # correct_order_list = csv_preview_data(header_detail, data_set_val)
        # retrieving correct ordered data from csv_data_arrangement() - basic_settings_specific.py
        # correct_order_list = csv_data_arrangement(db_header, data_set_val)
        return JsonResponse(result, safe=False)

    except MultiValueDictKeyError:
        csv_file = False
        error_msg = get_message_desc(MSG048)[1]
        # msgid = 'MSG048'
        # error_msg = get_msg_desc(msgid)
        # msg = error_msg['message_desc'][0]
        # error_msg = msg
        messages.error(request, error_msg)
        # messages.error(request, MSG048)

    # else:
    return JsonResponse(basic_save, safe=False)


def save_catalog_data(request):
    """

    :param request:
    :return:
    """
    catalog_data = JsonParser_obj.get_json_from_req(request)
    for data in catalog_data:
        if not (
                Catalogs.objects.filter(catalog_id=data['catalog_id'], name=data['name'],
                                        description=data['description'],
                                        product_type=data['product_type']).exists()):
            obj, created = Catalogs.objects.update_or_create(
                client=OrgClients.objects.get(client=global_variables.GLOBAL_CLIENT),
                catalog_guid=guid_generator(),
                catalog_id=data['catalog_id'],
                name=data['name'],
                description=data['description'],
                prod_type=data['product_type'])
    catalog_data_response = Catalogs.objects.filter(del_ind=False)
    return JsonParser_obj.get_json_from_obj(catalog_data_response)


def save_productservice_data(request):
    """

    :param request:
    :return:
    """
    client = global_variables.GLOBAL_CLIENT
    product_data = JsonParser_obj.get_json_from_req(request)
    product_not_exist: object = ProductsDetail.objects.filter(del_ind=False).exclude(
        product_id__in=[product['product_id'] for product in product_data])

    for set_del_int in product_not_exist:
        set_del_int.del_ind = True
        set_del_int.save()
    for data in product_data:
        if not (ProductsDetail.objects.filter(product_id=data['product_id']).exists()):
            country_of_origin = data['country_of_origin']
            country = Country.objects.get(country_code=country_of_origin)
            obj, created = ProductsDetail.objects.update_or_create(client=OrgClients.objects.get(client=client),
                                                                   catalog_item=guid_generator(),
                                                                   product_id=int(data['product_id']),
                                                                   short_desc=data['short_desc'],
                                                                   long_desc=data['long_desc'],
                                                                   supplier_id=data['supplier_id'],
                                                                   prod_cat_id=data['prod_cat_id'],
                                                                   catalog_id=data['catalog_id'],
                                                                   product_type=data['product_type'],
                                                                   price_on_request=False,
                                                                   unit=UnitOfMeasures.objects.get(uom_id=data['unit']),
                                                                   price_unit=data['price_unit'],
                                                                   currency=Currency.objects.get(
                                                                       currency_id=data['currency']),
                                                                   price=data['price'],
                                                                   manufacturer=data['manufacturer'],
                                                                   manu_part_num=data['manu_prod'],
                                                                   unspsc=UnspscCategories.objects.get(
                                                                       prod_cat_id=data['unspsc']),
                                                                   brand=data['brand'], lead_time=data['lead_time'],
                                                                   quantity_avail=data['quantity_avail'],
                                                                   quantity_min=data['quantity_min'],
                                                                   offer_key=data['offer_key'],
                                                                   country_of_origin=country,
                                                                   language=Languages.objects.get(
                                                                       language_id=data['language']),
                                                                   search_term1=data['search_term1'],
                                                                   search_term2=data['search_term2'])
    catalog_data_response = ProductsDetail.objects.filter(client=client, del_ind=False)
    return JsonParser_obj.get_json_from_obj(catalog_data_response)


def check_data_fk(request):
    if request.is_ajax():
        # retrieving data_list, Tablename, appname,db_header_data from UI
        table_data__array = JsonParser_obj.get_json_from_req(request)
        popup_data_list = table_data__array['data_list']
        db_header_data = table_data__array['db_header_data']
        client = global_variables.GLOBAL_CLIENT
        print(client)
        check_data_class = UploadPkFkTables()
        check_data_class.app_name = table_data__array['appname']
        check_data_class.table_name = table_data__array['Tablename']

        # gets he count from basic_table_new_conditions() - upload_pk_tables.py
        check_variable = check_data_class.basic_table_new_conditions(popup_data_list, db_header_data, client)
        return JsonResponse(check_variable)

    return render(request, 'Application_Settings/Basic_setting_Upload/upload_countries.html')


def test():
    def monday():
        return "monday"

    def tuesday():
        return "tuesday"

    def wednesday():
        return "wednesday"

    def thursday():
        return "thursday"

    def friday():
        return "friday"

    def saturday():
        return "saturday"

    def sunday():
        return "sunday"

    def default():
        return "Invalid day"

    def switch(wday):
        switcher = {
            1: monday,
            2: tuesday,
            3: wednesday,
            4: thursday,
            5: friday,
            6: saturday,
            7: sunday
        }


def weekday(num):
    switch = {
        '1': 'Sun',
        '2': 'Mon',
        '3': 'Tue',
        '4': 'Wed',
        '5': 'Thur',
        '6': 'Fri',
        '7': 'Sat'
    }
    return switch.get(num, "Invalid input")


def get_holiday_from_calenderid(request):
    # if request.is_ajax():
    calender_id = request.POST.get('calender_id')
    # holiday_array = JsonParser_obj.get_json_from_req(request)
    # calender_id = holiday_array['calender_id']
    holidays_data = CalenderHolidays.objects.filter(del_ind=False, calender_id=calender_id)
    qs_json = serializers.serialize('json', holidays_data)
    return HttpResponse(qs_json, content_type='application/json')


def basic_settings(request):
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_configuration_active': True
    }
    return render(request, 'Basic_Data_Configuration/basic_data_configuration.html', context)


def application_data_configuration(request):
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_configuration_active': True
    }
    return render(request, 'Application_Data_Configuration/application_data_configuration.html', context)


def master_data_configuration(request):
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_configuration_active': True
    }
    return render(request, 'Master_Data_Configuration/master_data_configuration.html', context)


def transaction_data_configuration(request):
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_configuration_active': True
    }
    return render(request, 'Transaction_Data_Configuration/transaction_data_configuration.html', context)


# def dropdown_document_type(request):
#   update_user_info(request)
# client = global_variables.GLOBAL_CLIENT

# shopping_cart = django_query_instance.django_filter_only_query(FieldTypeDescription, {
#    'client': client, 'del_ind': False, 'document_type': 'DOC01'
# })
# context = {
#     'shopping_cart': shopping_cart,
# }
#  return render(request, 'Application_Settings/upload_document_type.html', context)

def update_po_criteria_dropdown(request):
    """

    """
    data = get_product_criteria()
    return JsonResponse(data, safe=False)


def create_update_delete_flags(request):
    """

    """
    update_user_info(request)
    app_data = JsonParser_obj.get_json_from_req(request)
    application_settings_save_instance = ApplicationSettingsSave()
    if app_data['table_name'] == 'Country':
        display_data = application_settings_save_instance.generate_country_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'Currency':
        display_data = application_settings_save_instance.generate_currency_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'Language':
        display_data = application_settings_save_instance.generate_language_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)

    if app_data['table_name'] == 'UnspscCategories':
        display_data = application_settings_save_instance.generate_prod_cat_id_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'OrgNodeTypes':
        display_data = application_settings_save_instance.generate_node_type_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'OrgAttributes':
        display_data = application_settings_save_instance.generate_attributes_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'AuthorizationGroup':
        display_data = application_settings_save_instance.generate_auth_grp_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'UserRoles':
        display_data = application_settings_save_instance.generate_roles_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'DocumentType':
        display_data = application_settings_save_instance.generate_DocumentType_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'NumberRanges':
        display_data = application_settings_save_instance.generate_number_range_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'TransactionTypes':
        display_data = application_settings_save_instance.generate_transaction_type_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'AccountAssignmentCategory':
        display_data = application_settings_save_instance.generate_aac_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'CalenderConfig':
        display_data = application_settings_save_instance.generate_calender_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'MessagesId':
        display_data = application_settings_save_instance.generate_message_id_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'PoSplitType':
        display_data = application_settings_save_instance.generate_po_split_type_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)

    if app_data['table_name'] == 'UnspscCategoriesCustDesc':
        display_data = application_settings_save_instance.generate_prod_cat_Cust_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'OrgCompanies':
        display_data = application_settings_save_instance.generate_company_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'AccountingData':
        display_data = application_settings_save_instance.generate_aav_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'AccountingDataDesc':
        display_data = application_settings_save_instance.generate_aad_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'DetermineGLAccount':
        display_data = application_settings_save_instance.generate_detgl_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'ApproverType':
        display_data = application_settings_save_instance.generate_approval_type_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'WorkflowSchema':
        display_data = application_settings_save_instance.generate_wf_schema_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'OrgAddress':
        display_data = application_settings_save_instance.generate_OrgAddress_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'Payterms':
        display_data = application_settings_save_instance.generate_payment_term_delete_flags(app_data)
        return JsonResponse(display_data, safe=False)


def get_dropdown_data(request):
    update_user_info(request)
    master_data = JsonParser_obj.get_json_from_req(request)
    if master_data['table_name'] == 'UnspscCategoriesCust':
        data = get_unspsc_drop_down()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'UnspscCategoriesCustDesc':
        data = get_unspscdesc_drop_down()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'AccountingData':
        data = get_acc_value_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'AccountingDataDesc':
        data = get_acc_value_desc_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'DetermineGLAccount':
        data = get_gl_acc_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'WorkflowSchema':
        data = get_workflowschema_drop_down()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'ApproverType':
        data = get_approver_type_drop_down()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'SpendLimitId':
        data = get_spendlimitid_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'SpendLimitValue':
        data = get_spendlimitvalue_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'ApproverLimit':
        data = get_approverid_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'ApproverLimitValue':
        data = get_approvervalue_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'WorkflowACC':
        data = get_workflowacc_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'OrgAddress':
        data = get_orgaddress_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'OrgAddressMap':
        data = get_orgaddtype_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'Payterms_desc':
        data = get_paymentdesc_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'OrgNodeTypes':
        data = node_type_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'OrgAttributes':
        data = org_attr_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'OrgModelNodetypeConfig':
        data = orgattr_level_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'AuthorizationObject':
        data = auth_object_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'AuthorizationGroup':
        data = auth_grp_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'UserRoles':
        data = user_roles_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'Authorization':
        data = authorization_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'DocumentType':
        data = document_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'TransactionTypesFC':
        data = transaction_fc_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'TransactionTypesSC':
        data = transaction_sc_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'TransactionTypesPO':
        data = transaction_po_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'TransactionTypesGV':
        data = transaction_gv_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'AccountAssignmentCategory':
        data = accasscat_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'CalenderConfig':
        data = calendar_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'MessagesId':
        data = msgid_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'MessagesIdDesc':
        data = msgdesc_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'PoSplitType':
        data = po_split_type_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'PoSplitCriteria':
        data = posplit_criteria_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'PurchaseControl':
        data = purchase_control_dropdown()
        return JsonResponse(data, safe=False)
    if master_data['table_name'] == 'SourcingRule' or master_data['table_name'] == 'SourcingMapping':
        data = sourcing_rule_dropdown()
        return JsonResponse(data, safe=False)
