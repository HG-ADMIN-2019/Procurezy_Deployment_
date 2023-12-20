
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from eProc_Basic.Utilities.functions.dict_check_key import checkKey
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.update_del_ind import query_update_del_ind
from eProc_Basic_Settings.Utilities.basic_settings_specific import *
from eProc_Catalog.Utilities.catalog_specific import save_prod_cat_cust_image_to_db
from eProc_Configuration_Check.Utilities.configuration_check_generic import *
from eProc_Master_Settings.Utilities.master_settings_specific import *
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Upload.Utilities.upload_data.upload_basic_pk_fk_tables import UploadPkFkTables
from eProc_Upload.Utilities.upload_data.upload_pk_tables import *
from eProc_Upload.Utilities.upload_specific.upload_suppliers import upload_suppliermaster_new

JsonParser_obj = JsonParser()

upload_data_response = ''


def create_update_master_data(request):
    update_user_info(request)
    master_data = JsonParser_obj.get_json_from_req(request)
    master_settings_save_instance = MasterSettingsSave()
    if master_data['table_name'] == 'UnspscCategoriesCust':
        master_data['data'], message = check_unspsc_category_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_product_cat_cust_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'UnspscCategoriesCustDesc':
        master_data['data'], message = check_unspsc_category_desc_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_product_cat_cust_desc_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'WorkflowSchema':
        master_data['data'], message = check_workflowschema_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_work_flow_schema_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'SpendLimitId':
        master_data['data'], message = check_spending_limit_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_spend_limit_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'OrgAddressMap':
        master_data['data'], message = check_address_types_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_address_type_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'DetermineGLAccount':
        master_data['data'], message = check_determine_gl_acc_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_glaccount_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'AccountingData':
        master_data['data'], message = check_acc_assign_values_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_aav_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'AccountingDataDesc':
        master_data['data'], message = check_acc_assign_desc_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_aad_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'ApproverLimit':
        master_data['data'], message = check_approv_limit_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_app_limit_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'ApproverLimitValue':
        master_data['data'], message = check_approv_limit_value_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_app_limit_value_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'SpendLimitValue':
        master_data['data'], message = check_spendlimit_value_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_spend_limit_value_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'OrgAddress':
        master_data['data'], message = check_address_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_address_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'ApproverType':
        master_data['data'], message = check_approvaltype_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_approval_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'WorkflowACC':
        master_data['data'], message = check_workflow_acc_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_workflow_acc_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'Incoterms':
        master_data['data'], message = check_inco_terms_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_incoterms_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'Payterms':
        master_data['data'], message = check_paymentterm_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_payterm_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'Payterms_desc':
        master_data['data'], message = check_paymentterm_desc_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_payment_desc_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'OrgPGroup':
        master_data['data'], message = check_purchasegrp_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_purgrp_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'OrgPorg':
        master_data['data'], message = check_purchaseorg_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_purorg_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'OrgCompanies':
        master_data['data'], message = check_company_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_company_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'UserData':
        master_data['data'], message = get_valid_employee_data(master_data['data'], 'SAVE')
        display_data = master_settings_save_instance.save_employee_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)


def account_ass_values(request):
    update_user_info(request)

    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)

    upload_data_company = list(
        OrgCompanies.objects.filter(del_ind=False).values('company_id'))

    upload_data_acccat = list(
        AccountAssignmentCategory.objects.filter(del_ind=False).values('account_assign_cat'))
    # get table data
    data = {'upload_account_assignment_value': get_account_assignment_value(),
            'upload_company_data': upload_data_company,
            'upload_data_acccat': upload_data_acccat,
            'messages_list': messages_list,
            'inc_nav': True}

    return render(request, 'Accounting_Data/account_assignment_values.html',
                  data)


def render_aav_data(request):
    if request.method == 'POST':
        upload_data_accounting = list(
            AccountingData.objects.filter(del_ind=False).values('account_assign_guid', 'account_assign_value',
                                                                'valid_from',
                                                                'valid_to', 'account_assign_cat', 'company_id'))

        print(upload_data_accounting)

    return JsonResponse(upload_data_accounting, safe=False)


def extract_aav_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Account Assingment Values.CSV"'

    writer = csv.writer(response)

    writer.writerow(['COMPANY_ID', 'ACCOUNT_ASSIGN_CAT', 'ACC_ASSIGN_VALUE', 'VAILD_FROM', 'VAILD_TO', 'del_ind'])

    accounting = django_query_instance.django_filter_query(AccountingData,
                                                           {'del_ind': False,
                                                            'client': global_variables.GLOBAL_CLIENT}, None,
                                                           ['account_assign_value',
                                                            'account_assign_cat', 'company_id', 'valid_from',
                                                            'valid_to', 'del_ind'])
    accounting_data = query_update_del_ind(accounting)

    for accountingData in accounting_data:
        accountingData_info = [accountingData['company_id'], accountingData['account_assign_cat'],
                               accountingData['account_assign_value'], accountingData['valid_from'],
                               accountingData['valid_to'], accountingData['del_ind']]
        writer.writerow(accountingData_info)

    return response


def extract_accdesc_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Account Assingment Description.CSV"'

    writer = csv.writer(response)

    writer.writerow(
        ['COMPANY_ID', 'ACCOUNT_ASSIGN_CAT', 'ACCOUNT_ASSIGN_VALUE', 'DESCRIPTION', 'LANGUAGE_ID', 'del_ind'])

    accountingdesc = django_query_instance.django_filter_query(AccountingDataDesc,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT}, None,
                                                               ['account_assign_value', 'description', 'company_id',
                                                                'language_id', 'account_assign_cat', 'del_ind'])
    accountingdesc_data = query_update_del_ind(accountingdesc)

    for accountingdescData in accountingdesc_data:
        accountingdescData_info = [accountingdescData['company_id'], accountingdescData['account_assign_cat'],
                                   accountingdescData['account_assign_value'], accountingdescData['description'],
                                   accountingdescData['language_id'],
                                   accountingdescData['del_ind']]
        writer.writerow(accountingdescData_info)

    return response


def extract_cusprodcat_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Customer Product Category.CSV"'

    writer = csv.writer(response)

    writer.writerow(['del_ind','PROD_CAT_ID'])

    customerprod = django_query_instance.django_filter_query(UnspscCategoriesCust,
                                                             {'del_ind': False,
                                                              'client': global_variables.GLOBAL_CLIENT}, None,
                                                             ['del_ind','prod_cat_id'])

    customerprod_data = query_update_del_ind(customerprod)

    for customerprodData in customerprod_data:
        customerprodData_info = [customerprodData['del_ind'],
                                 customerprodData['prod_cat_id']
                                 ]

        writer.writerow(customerprodData_info)

    return response


def extract_cusprodcat_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Customer Product Category Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(['del_ind','PROD_CAT_ID'])

    return response


def extract_cusprodcatdesc_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Customer Product Category Description.CSV"'

    writer = csv.writer(response)

    writer.writerow(['PROD_CAT_ID', 'LANGUAGE_ID', 'CATEGORY_DESC', 'del_ind'])
    # get only active record

    customerproddesc = django_query_instance.django_filter_query(UnspscCategoriesCustDesc,
                                                                 {'del_ind': False,
                                                                  'client': global_variables.GLOBAL_CLIENT}, None,
                                                                 ['prod_cat_id', 'language_id',
                                                                  'category_desc', 'del_ind',
                                                                  ])

    customerproddesc_data = query_update_del_ind(customerproddesc)

    for customerproddescData in customerproddesc_data:
        customerproddescData_info = [customerproddescData['prod_cat_id'],
                                     customerproddescData['language_id'],
                                     customerproddescData['category_desc'],
                                     customerproddescData['del_ind']]
        writer.writerow(customerproddescData_info)

    return response


def extract_cusprodcatdesc_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Customer Product Category Description Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(['PROD_CAT_ID', 'LANGUAGE_ID', 'CATEGORY_DESC', 'del_ind'])

    return response


def extract_workflowschema_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Work_Flow_Schema.CSV"'

    writer = csv.writer(response)

    writer.writerow(['COMPANY_ID', 'WORKFLOW_SCHEMA', 'APP_TYPES', 'del_ind'])

    workflowschema = django_query_instance.django_filter_query(WorkflowSchema,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT}, None,
                                                               ['company_id', 'workflow_schema', 'app_types',
                                                                'del_ind'])

    workflowschema_data = query_update_del_ind(workflowschema)

    for workflowschemaData in workflowschema_data:
        workflowschema_info = [workflowschemaData['company_id'],
                               workflowschemaData['workflow_schema'],
                               workflowschemaData['app_types'],
                               workflowschemaData['del_ind']]
        writer.writerow(workflowschema_info)

    return response


def extract_workflowaccount_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="WORK FLOW ACCOUNTING.CSV"'

    writer = csv.writer(response)

    writer.writerow(
        [ 'COMPANY_ID','ACCOUNT_ASSIGN_CAT', 'ACC_VALUE','APP_USERNAME', 'SUP_COMPANY_ID',  'SUP_ACCOUNT_ASSIGN_CAT',
          'SUP_ACC_VALUE', 'CURRENCY_ID', 'del_ind'])

    # get only active records
    workflow_acct = django_query_instance.django_filter_query(WorkflowACC,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT}, None,
                                                              ['company_id', 'account_assign_cat',
                                                               'acc_value', 'app_username',
                                                               'sup_company_id', 'sup_account_assign_cat',
                                                               'sup_acc_value', 'currency_id',
                                                               'del_ind'])

    workflow_acct_data = query_update_del_ind(workflow_acct)

    for workflowacct in workflow_acct_data:
        workflowacct_info = [workflowacct['company_id'],workflowacct['account_assign_cat'],
                             workflowacct['acc_value'],workflowacct['app_username'],
                             workflowacct['sup_company_id'],workflowacct['sup_account_assign_cat'],
                             workflowacct['sup_acc_value'], workflowacct['currency_id'],
                             workflowacct['del_ind']
                             ]

        writer.writerow(workflowacct_info)

    return response


def extract_workflowacct_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Work Flow Acct Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(
        ['COMPANY_ID','ACCOUNT_ASSIGN_CAT', 'ACC_VALUE', 'APP_USERNAME',  'SUP_COMPANY_ID', 'SUP_ACCOUNT_ASSIGN_CAT',
         'SUP_ACC_VALUE','CURRENCY_ID', 'del_ind'])

    return response


def save_product_cat_cust(request):
    """

    :param request:
    :return:
    """
    update_user_info(request)
    product_not_exist = ''
    ui_data = request.POST
    attached_file = request.FILES
    converted_dict = dict(ui_data.lists())
    product_data = json.loads(request.POST['update'])
    # save images
    if checkKey(converted_dict, 'Prod_cat'):
        prod_cat = converted_dict['Prod_cat']
        file_name = converted_dict['file_name']
        default_image = [True if img_flag else False for img_flag in converted_dict['default_image_value']]
        save_prod_cat_cust_image_to_db(prod_cat, file_name, attached_file, default_image)

    cust_prod_cat_not_exist: object = UnspscCategoriesCust.objects.filter(del_ind=False).exclude \
        (prod_cat_guid__in=[custprodcat['prod_cat_guid'] for custprodcat in product_data])

    for set_del_int in cust_prod_cat_not_exist:
        set_del_int.del_ind = True
        set_del_int.save()

    for save_custprodcat in product_data:
        product_category_id = save_custprodcat['prod_cat_id']

        # Below logic is for existing records changed.

        # Check if there is any change in the record if no then skip the record
        if (UnspscCategoriesCust.objects.filter(prod_cat_guid=save_custprodcat['prod_cat_guid'],
                                                prod_cat_id=product_category_id,
                                                client=global_variables.GLOBAL_CLIENT).exists()):
            continue

        elif not (UnspscCategoriesCust.objects.filter(prod_cat_guid=save_custprodcat['prod_cat_guid'],
                                                      prod_cat_id=product_category_id,
                                                      client=global_variables.GLOBAL_CLIENT).exists()):

            if (UnspscCategoriesCust.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                                    prod_cat_guid=save_custprodcat['prod_cat_guid'], ).exists()):
                UnspscCategoriesCust.objects.filter(prod_cat_guid=save_custprodcat['prod_cat_guid'],
                                                    client=global_variables.GLOBAL_CLIENT).update(
                    prod_cat_id=UnspscCategories.objects.get(prod_cat_id=product_category_id),
                    del_ind=False,
                    client=OrgClients.objects.get(client=global_variables.GLOBAL_CLIENT))

        # Below logic is for new records added. The GUID will be hardcoded to GUID from UI and sent to backend.
        if save_custprodcat['prod_cat_guid'] == '':
            UnspscCategoriesCust.objects.create(
                prod_cat_guid=guid_generator(),
                prod_cat_id=UnspscCategories.objects.get(prod_cat_id=product_category_id),
                del_ind=False,
                client=OrgClients.objects.get(client=global_variables.GLOBAL_CLIENT))
    catalog_data_response = list(
        UnspscCategoriesCust.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values(
            'prod_cat_guid', 'prod_cat_id'))
    return JsonResponse(catalog_data_response, safe=False)


def get_prod_cat_image_detail(request):
    """

    :param request:
    :return:
    """
    update_user_info(request)
    prod_cat_id = JsonParser().get_json_from_req(request)
    prod_cat_img_detail = ImagesUpload.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                                      image_id=str(prod_cat_id),
                                                      image_type=CONST_UNSPSC_IMAGE_TYPE)

    return JsonParser().get_json_from_obj(prod_cat_img_detail)


def data_upload_fk(request):
    db_header = request.POST.get('db_header_data')
    csv_file = request.FILES['file_attach']
    data_set_val = csv_file.read().decode('utf8')
    # fin_upload_data = io.StringIO(data_set_val)
    upload_csv = CompareTableHeader()
    # upload_csv.header_data = fin_upload_data
    upload_csv.app_name = request.POST.get('appname')
    upload_csv.table_name = request.POST.get('Tablename')
    upload_csv.request = request
    basic_save, header_detail = upload_csv.basic_header_condition()
    # if not basic_save:
    try:

        # retrieving correct ordered data from csv_data_arrangement() - basic_settings_specific.py
        correct_order_list = csv_data_arrangement(db_header, data_set_val)

        return JsonResponse(correct_order_list, safe=False)

    except MultiValueDictKeyError:
        csv_file = False
        error_msg = get_message_desc(MSG048)[1]
        # msgid = 'MSG048'
        # error_msg = get_msg_desc(msgid)
        # msg = error_msg['message_desc'][0]
        # error_msg = msg
        messages.error(request, error_msg)
        # messages.error(request, MSG048)

    else:
        return JsonResponse(basic_save, safe=False)


def check_data_acct_asst_val(request):
    if request.is_ajax():
        # retrieving data_list, Tablename, appname,db_header_data from UI
        table_data__array = JsonParser_obj.get_json_from_req(request)
        popup_data_list = table_data__array['data_list']
        db_header_data = table_data__array['db_header_data']
        client = getClients(request)
        check_data_class = UploadPkFkTables()
        check_data_class.app_name = table_data__array['appname']
        check_data_class.table_name = table_data__array['Tablename']
        # gets he count from basic_table_new_conditions() - upload_pk_tables.py
        check_variable = check_data_class.upload_master_data_new(popup_data_list, db_header_data, client)
        # print(check_variable)
        return JsonResponse(check_variable)

    return render(request, 'Accounting_Data/account_assignment_values.html')


def display_incoterms(request):
    incoterms_data = django_query_instance.django_filter_query(
        Incoterms, {'del_ind': False}, None, ['incoterm_key', 'description'])
    # incoterms_data = list(
    #     Incoterms.objects.filter(del_ind=False).values('incoterm_key', 'description'))
    dropdown_db_values = list(
        FieldTypeDescription.objects.filter(field_name='incoterm', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'
                                                                                          ))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    return render(request, 'Supplier_Management/incoterms.html',
                  {'incoterms_data': incoterms_data, 'dropdown_db_values': dropdown_db_values,
                   'messages_list': messages_list,
                   'inc_nav': True})


def payment_terms(request):
    payment_term_data = list(
        Payterms.objects.filter(del_ind=False).values('payment_term_key', 'payment_term_guid'))
    for payment_terms_fd in payment_term_data:
        if django_query_instance.django_existence_check(Payterms,
                                                        {'del_ind': False,
                                                         'payment_term_key': payment_terms_fd['payment_term_key']}):
            payment_terms_fd["del_ind_flag"] = False
        else:
            payment_terms_fd["del_ind_flag"] = True

    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    return render(request, 'Supplier_Management/payment_terms.html',
                  {'payment_term_data': payment_term_data,
                   'messages_list': messages_list,
                   'inc_nav': True})


def payment_terms_desc(request):
    client = getClients(request)
    payterm_key_list = list(Payterms.objects.filter(del_ind=False).values('payment_term_key'))
    language_list = list(Languages.objects.filter(del_ind=False).values('language_id', 'description'))
    # payment_desc_data = list(
    #     Payterms_desc.objects.filter(del_ind=False).values('payment_term_guid', 'payment_term_key', 'day_limit',
    #                                                         'description', 'language_id'))
    payment_desc_data = get_configuration_data(
        Payterms_desc, {'client': client, 'del_ind': False}, ['payment_term_guid', 'payment_term_key', 'day_limit',
                                                              'description', 'language_id'])
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    return render(request, 'Supplier_Management/payment_term_desc.html',
                  {'payment_desc_data': payment_desc_data, 'payterm_key_list': payterm_key_list,
                   'language_list': language_list, 'messages_list': messages_list, 'inc_nav': True})


def upload_supplier(request):
    update_user_info(request)
    supplier_data = list(
        SupplierMaster.objects.filter(del_ind=False, client=global_variables.GLOBAL_CLIENT).values('supplier_id',
                                                                                                   'supp_type', 'name1',
                                                                                                   'name2', 'city',
                                                                                                   'postal_code',
                                                                                                   'street', 'landline',
                                                                                                   'mobile_num', 'fax',
                                                                                                   'email', 'email1',
                                                                                                   'email2', 'email3',
                                                                                                   'email4', 'email5',
                                                                                                   'output_medium',
                                                                                                   'search_term1',
                                                                                                   'search_term2',
                                                                                                   'duns_number',
                                                                                                   'block_date',
                                                                                                   'block',
                                                                                                   'working_days',
                                                                                                   'is_active',
                                                                                                   'registration_number',
                                                                                                   'country_code',
                                                                                                   'currency_id',
                                                                                                   'language_id'))
    return render(request, 'Supplier_Management/supplier_upload.html',
                  {'supplier_data': supplier_data, 'inc_nav': True,
                   'supplier_data_json': json.dumps(supplier_data, cls=DjangoJSONEncoder)})


def upload(request):
    if request.is_ajax():
        Test_mode = 'on'
        # retrieving data_list, Tablename, appname,db_header_data from UI
        table_data__array = JsonParser_obj.get_json_from_req(request)
        table_data__array = JsonParser_obj.get_json_from_req(request)
        popup_data_list = table_data__array['data_list']
        # db_header_data = table_data__array['db_header_data']
        # check_data_class = upload_suppliermaster_new(request, popup_data_list, Test_mode)
        client = getClients(request)
        # check_data_class.app_name = table_data__array['appname']
        # check_data_class.table_name = table_data__array['Tablename']
        # gets he count from basic_table_new_conditions() - upload_pk_tables.py
        check_variable = upload_suppliermaster_new(request, popup_data_list, Test_mode)
        print("check", check_variable)
        return JsonResponse(check_variable, safe=False)

    return render(request, 'Supplier_Management/supplier_upload.html')


def address_type(request):
    client = getClients(request)
    address_type_data = list(
        OrgAddressMap.objects.filter(del_ind=False).values('address_guid', 'address_number', 'address_type',
                                                           'company_id', 'valid_from', 'valid_to'))
    for valid_from in address_type_data:

        if valid_from['valid_from'] == None:
            valid_from['valid_from'] = ''

    for valid_to in address_type_data:

        if valid_to['valid_to'] == None:
            valid_to['valid_to'] = ''

    dropdown_db_values = list(
        FieldTypeDescription.objects.filter(field_name='address_type', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'
                                                                                          ))
    address_data = list(
        OrgAddress.objects.filter(del_ind=False).values('address_guid', 'address_number', 'title', 'name1', 'name2',
                                                        'street', 'area', 'landmark', 'city', 'postal_code', 'region',
                                                        'mobile_number', 'telephone_number', 'fax_number', 'email',
                                                        'country_code',
                                                        'language_id', 'time_zone'))

    upload_data_OrgCompanies = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    return render(request, 'Address_Data/address_type.html',
                  {'address_type_data': address_type_data,
                   'dropdown_db_values': dropdown_db_values,
                   'upload_data_OrgCompanies': upload_data_OrgCompanies,
                   'address_data': address_data,
                   'messages_list': messages_list,
                   'inc_nav': True})


def address(request):
    language_list = list(Languages.objects.filter(del_ind=False).values('language_id', 'description'))
    country_list = get_country_data()
    time_zone_data = list(TimeZone.objects.filter(del_ind=False).values('time_zone', 'description'))
    add_partner_type_data = list(AddressPartnerType.objects.filter(del_ind=False).values('address_partner_type',
                                                                                         'address_partner_type_desc'))

    address_data = list(
        OrgAddress.objects.filter(del_ind=False).values('address_guid', 'address_number', 'title', 'name1', 'name2',
                                                        'street', 'area', 'landmark', 'city', 'postal_code', 'region',
                                                        'mobile_number', 'telephone_number', 'fax_number', 'email',
                                                        'country_code', 'org_address_source_system',
                                                        'address_partner_type',
                                                        'language_id', 'time_zone'))

    for address_partner_type in address_data:

        if address_partner_type['address_partner_type'] is None:
            address_partner_type['address_partner_type'] = ''

    for address_data_fd in address_data:
        if not django_query_instance.django_existence_check(OrgAddressMap,
                                                            {'client': client,
                                                             'address_number': address_data_fd['address_number'],
                                                             'del_ind': False}):
            address_data_fd["del_ind_flag"] = False
        else:
            address_data_fd["del_ind_flag"] = True
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)

    return render(request, 'Address_Data/address.html',
                  {'address_data': address_data, 'language_list': language_list, 'country_list': country_list,
                   'time_zone_data': time_zone_data,
                   'add_partner_type_data': add_partner_type_data,
                   'messages_list': messages_list,
                   'inc_nav': True})


def extract_approverlimit_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Approval Limit.CSV"'

    writer = csv.writer(response)

    writer.writerow(['APPROVER_USERNAME', 'APP_CODE_ID', 'COMPANY_ID', 'del_ind'])

    approverlimit = django_query_instance.django_filter_query(ApproverLimit,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT}, None,
                                                              ['approver_username', 'app_code_id', 'company_id',
                                                               'del_ind'])
    approverlim_data = query_update_del_ind(approverlimit)

    for approverlimitdata in approverlim_data:
        approverlimitdata_info = [approverlimitdata['approver_username'], approverlimitdata['app_code_id'],
                                  approverlimitdata['company_id'], approverlimitdata['del_ind']]
        writer.writerow(approverlimitdata_info)

    return response


def extract_approverlimitval_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Approval Limit Value.CSV"'

    writer = csv.writer(response)

    writer.writerow(['COMPANY_ID', 'APP_TYPES', 'APP_CODE_ID', 'UPPER_LIMIT_VALUE', 'CURRENCY_ID', 'del_ind'])

    approverlimitval = django_query_instance.django_filter_query(ApproverLimitValue,
                                                                 {'del_ind': False,
                                                                  'client': global_variables.GLOBAL_CLIENT}, None,
                                                                 ['company_id', 'app_types', 'app_code_id',
                                                                  'upper_limit_value', 'currency_id', 'del_ind'])
    approverlim_data = query_update_del_ind(approverlimitval)

    for approverlimitvaldata in approverlim_data:
        approverlimitvaldata_info = [approverlimitvaldata['company_id'], approverlimitvaldata['app_types'],
                                     approverlimitvaldata['app_code_id'], approverlimitvaldata['upper_limit_value'],
                                     approverlimitvaldata['currency_id'], approverlimitvaldata['del_ind']]
        writer.writerow(approverlimitvaldata_info)

    return response


def extract_spendlimit_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="SPEND LIMIT.CSV"'

    writer = csv.writer(response)

    writer.writerow(['COMPANY_ID', 'SPENDER_USERNAME', 'SPEND_CODE_ID', 'del_ind'])
    # get only active record

    spendlimitvals = django_query_instance.django_filter_query(SpendLimitId,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT}, None,
                                                               ['company_id', 'spender_username',
                                                                'spend_code_id', 'del_ind'])
    spendlim_data = query_update_del_ind(spendlimitvals)

    for spendlimitval in spendlim_data:
        spendlimitval_info = [spendlimitval['company_id'], spendlimitval['spender_username'],
                              spendlimitval['spend_code_id'], spendlimitval['del_ind']]
        writer.writerow(spendlimitval_info)

    return response


def extract_spendlimitval_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Spend Limit Value.CSV"'

    writer = csv.writer(response)

    writer.writerow(['COMPANY_ID', 'SPEND_CODE_ID', 'UPPER_LIMIT_VALUE', 'CURRENCY_ID', 'del_ind'])

    spendlimitvalues = django_query_instance.django_filter_query(SpendLimitValue, {'del_ind': False,
                                                                                   'client': global_variables.GLOBAL_CLIENT},
                                                                 None,
                                                                 ['company_id', 'spend_code_id',
                                                                  'upper_limit_value', 'currency_id', 'del_ind'])
    spendlim_data = query_update_del_ind(spendlimitvalues)

    for spendlimitvaluedata in spendlim_data:
        spendlimitvaluedata_info = [spendlimitvaluedata['company_id'], spendlimitvaluedata['spend_code_id'],
                                    spendlimitvaluedata['upper_limit_value'], spendlimitvaluedata['currency_id'],
                                    spendlimitvaluedata['del_ind']]
        writer.writerow(spendlimitvaluedata_info)

    return response


def extract_spendlimit_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Spend Limit.CSV"'

    writer = csv.writer(response)

    writer.writerow(['COMPANY_ID', 'SPENDER_USERNAME', 'SPEND_CODE_ID', 'del_ind'])

    return response


def extract_address_type_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Address Types.CSV"'

    writer = csv.writer(response)

    writer.writerow(['ADDRESS_TYPE', 'ADDRESS_NUMBER', 'COMPANY_ID', 'VALID_FROM', 'VALID_TO', 'del_ind'])

    address_type = django_query_instance.django_filter_query(OrgAddressMap,
                                                             {'del_ind': False,
                                                              'client': global_variables.GLOBAL_CLIENT}, None,
                                                             ['address_type', 'address_number', 'company_id',
                                                              'valid_from', 'valid_to',
                                                              'del_ind'])
    address_type_data = query_update_del_ind(address_type)

    for addresstypedata in address_type_data:
        address_type_info = [addresstypedata['address_type'],
                             addresstypedata['address_number'],
                             addresstypedata['company_id'],
                             addresstypedata['valid_from'],
                             addresstypedata['valid_to'],
                             addresstypedata['del_ind']]
        writer.writerow(address_type_info)

    return response


def extract_address_type_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Address Types Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(['ADDRESS_TYPE', 'ADDRESS_NUMBER', 'COMPANY_ID', 'VALID_FROM', 'VALID_TO', 'del_ind'])

    return response


def extract_approver_type_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Approver Types.CSV"'

    writer = csv.writer(response)

    writer.writerow(['APP_TYPES', 'APPROVAL_TYPE_DESC', 'del_ind'])

    approver_type = django_query_instance.django_filter_query(ApproverType,
                                                              {'del_ind': False}, None,
                                                              ['app_types', 'appr_type_desc', 'del_ind'])
    approver_type_data = query_update_del_ind(approver_type)

    for approvertypedata in approver_type_data:
        approver_type_info = [approvertypedata['app_types'],
                              approvertypedata['appr_type_desc'],
                              approvertypedata['del_ind']]
        writer.writerow(approver_type_info)

    return response


def extract_glaccount_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="DETERMINE GL ACCOUNT.CSV"'

    writer = csv.writer(response)

    writer.writerow(['PROD_CAT_ID', 'COMPANY_ID', 'ACCOUNT_ASSIGN_CAT', 'GL_ACC_NUM', 'GL_ACC_DEFAULT',
                     'ITEM_FROM_VALUE', 'ITEM_TO_VALUE', 'CURRENCY_ID', 'del_ind'])

    glaccount = django_query_instance.django_filter_query(DetermineGLAccount,
                                                          {'del_ind': False,
                                                           'client': global_variables.GLOBAL_CLIENT}, None,
                                                          ['prod_cat_id', 'gl_acc_num',
                                                           'gl_acc_default', 'account_assign_cat', 'company_id',
                                                           'item_from_value', 'item_to_value', 'currency_id',
                                                           'del_ind'])

    glaccount_data = query_update_del_ind(glaccount)

    for glaccountdata in glaccount_data:
        if glaccountdata['gl_acc_default']:
            glaccountdata['gl_acc_default'] = 1
        else:
            glaccountdata['gl_acc_default'] = 0
        glaccount_info = [glaccountdata['prod_cat_id'], glaccountdata['company_id'],
                          glaccountdata['account_assign_cat'], glaccountdata['gl_acc_num'],
                          glaccountdata['gl_acc_default'],
                          glaccountdata['item_from_value'],
                          glaccountdata['item_to_value'], glaccountdata['currency_id'],
                          glaccountdata['del_ind']]

        writer.writerow(glaccount_info)

    return response


def extract_glaccount_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Determine GL Account Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(['PROD_CAT_ID', 'GL_ACC_NUM', 'GL_ACC_DEFAULT', 'ACCOUNT_ASSIGN_CAT',
                     'COMPANY_ID', 'ITEM_FROM_VALUE', 'ITEM_TO_VALUE', 'CURRENCY_ID', 'del_ind'])

    return response


def extract_pgrp_data(request):
    client = getClients(request)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Maintain Purchasing Group.CSV"'

    writer = csv.writer(response)

    writer.writerow(['PGROUP_ID', 'DESCRIPTION', 'del_ind'])

    purgrp = django_query_instance.django_filter_query(OrgPGroup,
                                                       {'client': global_variables.GLOBAL_CLIENT, 'del_ind': False},
                                                       None,
                                                       ['pgroup_id', 'description', 'del_ind'])

    purgrp_data = query_update_del_ind(purgrp)

    for purgrpdata in purgrp_data:
        purgrp_info = [purgrpdata['pgroup_id'], purgrpdata['description'],
                       purgrpdata['del_ind']]

        writer.writerow(purgrp_info)

    return response


def extract_pgrp_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Maintain Purchasing Group Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(['PGROUP_ID', 'DESCRIPTION', 'del_ind'])

    return response


def extract_porg_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Maintain Purchasing Organisation.CSV"'

    writer = csv.writer(response)

    writer.writerow(['PORG_ID', 'DESCRIPTION', 'del_ind'])

    purorg = django_query_instance.django_filter_query(OrgPorg,
                                                       {'del_ind': False,
                                                        'client': global_variables.GLOBAL_CLIENT}, None,
                                                       ['porg_id', 'description',
                                                        'del_ind'])

    purorg_data = query_update_del_ind(purorg)

    for purorgdata in purorg_data:
        purorg_info = [purorgdata['porg_id'], purorgdata['description'],
                       purorgdata['del_ind']]

        writer.writerow(purorg_info)

    return response


def extract_porg_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Maintain Purchasing Organisation Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(['PORG_ID', 'DESCRIPTION', 'Object id', 'del_ind'])

    return response


def upload_prod_cat_images(request):
    """

    :param request:
    :return:
    """
    status = {}
    update_user_info(request)
    ui_data = request.POST
    attached_file = request.FILES
    converted_dict = dict(ui_data.lists())
    file_name = request.POST.get('file_name')
    prod_cat = request.POST.get('prod_cat_id')
    save_prod_cat_image_to_db(prod_cat, file_name, attached_file)
    status = get_unspsc_cat_cust_data()
    return JsonResponse(status, safe=False)


def extract_orgcompany_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="OrgCompany.CSV"'

    writer = csv.writer(response)

    writer.writerow(['COMPANY_ID', 'NAME1', 'NAME2', 'del_ind'])

    orgcompany = django_query_instance.django_filter_query(OrgCompanies,
                                                           {'del_ind': False,
                                                            'client': global_variables.GLOBAL_CLIENT}, None,
                                                           ['company_id', 'name1', 'name2',
                                                            'del_ind'])
    orgcompany_data = query_update_del_ind(orgcompany)

    for orgcompanydata in orgcompany_data:
        orgcompanydata_info = [orgcompanydata['company_id'],
                               orgcompanydata['name1'],
                               orgcompanydata['name2'],
                               orgcompanydata['del_ind']]
        writer.writerow(orgcompanydata_info)

    return response


def extract_address_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Address.CSV"'

    writer = csv.writer(response)

    writer.writerow(
        ['ADDRESS_NUMBER', 'TITLE', 'NAME1', 'NAME2', 'STREET', 'AREA', 'LANDMARK',
         'CITY', 'ADDRESS_PARTNER_TYPE', 'postal_code', 'REGION',
         'MOBILE_NUMBER', 'TELEPHONE_NUMBER', 'FAX_NUMBER', 'EMAIL',
         'COUNTRY_CODE',
         'LANGUAGE_ID', 'TIME_ZONE', 'del_ind'])

    address = django_query_instance.django_filter_query(OrgAddress,
                                                        {'del_ind': False,
                                                         'client': global_variables.GLOBAL_CLIENT}, None,
                                                        ['address_number', 'title', 'name1',
                                                         'name2', 'street', 'area',
                                                         'landmark', 'city', 'address_partner_type',
                                                         'postal_code', 'region',
                                                         'mobile_number',
                                                         'telephone_number', 'fax_number', 'email', 'country_code',
                                                         'language_id', 'time_zone',
                                                         'del_ind'])
    address_data = query_update_del_ind(address)

    for addressdata in address_data:
        address_info = [addressdata['address_number'],
                        addressdata['title'],
                        addressdata['name1'],
                        addressdata['name2'],
                        addressdata['street'],
                        addressdata['area'],
                        addressdata['landmark'],
                        addressdata['city'],
                        addressdata['address_partner_type'],
                        addressdata['postal_code'],
                        addressdata['region'],
                        addressdata['mobile_number'],
                        addressdata['telephone_number'],
                        addressdata['fax_number'],
                        addressdata['email'],
                        addressdata['country_code'],
                        addressdata['language_id'],
                        addressdata['time_zone'],
                        addressdata['del_ind']]
        writer.writerow(address_info)

    return response


def upload_cust_prod_cat(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    upload_cust_prod_catogories, product_cat_list, data = get_unspsc_cat_cust_data()
    dependent_dropdown = get_unspsc_drop_down()
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    data = {'content_managment_settings': 'content_managment_settings',
            'inc_nav': True,
            'upload_cust_prod_cat': upload_cust_prod_catogories, 'messages_list': messages_list,
            'upload_ProdCat': dependent_dropdown
            }

    return render(request,
                  'Customer_Product_Category/customer_product_category.html',
                  data)


def upload_cust_prod_cat_desc(request):
    update_user_info(request)
    upload_cust_prod_desc_catogories, product_cat_list, data = get_unspsc_cat_custdesc_data()
    upload_language = list(Languages.objects.filter(del_ind=False).values('language_id', 'description'))

    upload_ProdCat = list(UnspscCategories.objects.filter(del_ind=False).values('prod_cat_id', 'prod_cat_desc'))

    for prod_cat_desc in upload_ProdCat:
        if prod_cat_desc['prod_cat_desc'] == None:
            prod_cat_desc['prod_cat_desc'] = ''

    content_managment_settings = 'content_managment_settings'
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)

    return render(request,
                  'Customer_Product_Category/customer_product_category_description.html',
                  {'upload_cust_prod_cat_desc': upload_cust_prod_desc_catogories,
                   'upload_languages': upload_language,
                   'upload_ProdCat': upload_ProdCat, 'messages_list': messages_list,
                   'content_managment_settings': content_managment_settings,
                   'inc_nav': True})


def org_companies(request):
    update_user_info(request)
    org_companies = get_org_companies_data()
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    return render(request, 'Organizational_Data/org_companies.html',
                  {'org_companies': org_companies,
                   'messages_list': messages_list,
                   'inc_nav': True})


def purchasing_org(request):
    update_user_info(request)
    upload_porg = get_org_porg_data()
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    return render(request, 'Organizational_Data/purchase_org.html',
                  {'purchasing_org': upload_porg,
                   'messages_list': messages_list,
                   'inc_nav': True})


def purchasing_grp(request):
    client = getClients(request)
    upload_pgrp = get_configuration_data(
        OrgPGroup, {'client': client, 'del_ind': False}, ['pgroup_guid', 'pgroup_id', 'object_id',
                                                          'description', 'porg_id'])
    for pgrp_id_fd in upload_pgrp:
        if django_query_instance.django_existence_check(OrgPorg,
                                                        {'del_ind': False,
                                                         'porg_id': pgrp_id_fd['porg_id']}):
            pgrp_id_fd["del_ind_flag"] = False
        else:
            pgrp_id_fd["del_ind_flag"] = True
    upload_data_Orgmodel = get_configuration_data(OrgModel, {'client': client, 'del_ind': False}, ['object_id'])
    upload_data_OrgPGroup = get_configuration_data(OrgPGroup, {'client': client, 'del_ind': False}, ['porg_id'])
    master_data_settings = 'master_data_settings'

    for object_id in upload_pgrp:
        if object_id['object_id'] == None:
            object_id['object_id'] = ''
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)

    return render(request, 'Organizational_Data/purchase_grp.html',
                  {'purchasing_grp': upload_pgrp, 'upload_data_Orgmodel': upload_data_Orgmodel,
                   'messages_list': messages_list,
                   'upload_data_OrgPGroup': upload_data_OrgPGroup, 'master_data_settings': master_data_settings,
                   'inc_nav': True})


def account_assignment(request):
    client = getClients(request)
    upload_accassignment = get_configuration_data(AccountingDataDesc, {'client': client, 'del_ind': False},
                                                  ['acc_desc_guid', 'account_assign_value',
                                                   'description', 'account_assign_cat',
                                                   'company_id', 'language_id'])
    upload_accassvalues = get_configuration_data(AccountingData, {'del_ind': False},
                                                 ['account_assign_value', 'account_assign_cat',
                                                  'company_id'])

    upload_data_acccat = get_configuration_data(AccountAssignmentCategory, {'del_ind': False}, ['account_assign_cat'])
    upload_data_company = get_configuration_data(OrgCompanies, {'del_ind': False}, ['company_id'])
    upload_data_language = get_configuration_data(Languages, {'del_ind': False}, ['language_id'])
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    master_data_settings = 'master_data_settings'
    return render(request, 'Accounting_Data/account_assignment_description.html',
                  {'account_assignment': upload_accassignment, 'upload_data_company': upload_data_company,
                   'upload_data_acccat': upload_data_acccat, 'upload_data_language': upload_data_language,
                   'upload_accassvalues': upload_accassvalues, 'master_data_settings': master_data_settings,
                   'messages_list': messages_list, 'inc_nav': True})


def det_gl_acc(request):
    client = getClients(request)
    prod_catogories = list(
        UnspscCategoriesCust.objects.filter(client=client, del_ind=False).values('prod_cat_id'))

    upload_gl_acc_db = list(
        DetermineGLAccount.objects.filter(client=client, del_ind=False).values('det_gl_acc_guid', 'prod_cat_id',
                                                                               'item_from_value', 'item_to_value',
                                                                               'gl_acc_num',
                                                                               'gl_acc_default', 'company_id',
                                                                               'account_assign_cat', 'currency_id'))
    upload_gl_acc = []
    for data in upload_gl_acc_db:

        if data['gl_acc_num'] == None:
            data['gl_acc_num'] = ''

        data_dict = {
            'det_gl_acc_guid': data['det_gl_acc_guid'],
            'prod_cat_id': data['prod_cat_id'],
            'item_from_value': data['item_from_value'],
            'item_to_value': data['item_to_value'],
            'gl_acc_num': data['gl_acc_num'],
            'gl_acc_default': data['gl_acc_default'],
            'company_id': data['company_id'],
            'account_assign_cat': data['account_assign_cat'],
            'currency_id': data['currency_id'],

        }
        upload_gl_acc.append(data_dict)

    upload_value_glacc = list(
        AccountingData.objects.filter(client=client, del_ind=False).values('account_assign_value'))
    upload_value_accasscat = list(
        AccountAssignmentCategory.objects.filter(~Q(account_assign_cat='GLACC'), del_ind=False).values(
            'account_assign_cat'))
    upload_value_currency = list(Currency.objects.filter(del_ind=False).values('currency_id'))
    upload_value_company = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)

    return render(request, 'GL_Account/determine_gl_account.html',
                  {'upload_gl_acc': upload_gl_acc, 'upload_value_glacc': upload_value_glacc,
                   'upload_value_accasscat': upload_value_accasscat,
                   'upload_value_currency': upload_value_currency, 'messages_list': messages_list,
                   'upload_value_company': upload_value_company, 'prod_catogories': prod_catogories,
                   'inc_nav': True})


def approval_type(request):
    upload_apptype = list(ApproverType.objects.filter(del_ind=False).values('app_types', 'appr_type_desc'))

    for app_type_fd in upload_apptype:
        if django_query_instance.django_existence_check(WorkflowSchema,
                                                        {'del_ind': False,
                                                         'app_types': app_type_fd['app_types']}):
            app_type_fd["del_ind_flag"] = False
        else:
            app_type_fd["del_ind_flag"] = True

    dropdown_db_values = list(
        FieldTypeDescription.objects.filter(field_name='approval_type', del_ind=False, used_flag=0,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'
                                                                                          ))
    dropdown_db_values_onload = list(
        FieldTypeDescription.objects.filter(field_name='approval_type', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'
                                                                                          ))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    master_data_settings = 'master_data_settings'
    return render(request, 'Approval_Data/approval_type.html',
                  {'approval_type': upload_apptype, 'master_data_settings': master_data_settings,
                   'inc_nav': True,
                   'dropdown_db_values': dropdown_db_values, 'messages_list': messages_list,
                   'dropdown_db_values_onload': dropdown_db_values_onload})


def work_flow_schema(request):
    client = getClients(request)
    upload_wfschema = get_configuration_data(
        WorkflowSchema, {'client': client, 'del_ind': False}, ['workflow_schema_guid', 'workflow_schema',
                                                               'app_types', 'company_id'])
    upload_data_company = get_configuration_data(OrgCompanies, {'client': client, 'del_ind': False}, ['company_id'])
    upload_data_apptypes = get_configuration_data(ApproverType, {'del_ind': False}, ['app_types'])
    dropdown_db_values = list(
        FieldTypeDescription.objects.filter(field_name='workflow_schema', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values(
            'field_type_id',
            'field_type_desc'
        ))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    master_data_settings = 'master_data_settings'
    return render(request, 'Work_Flow_Data/work_flow_schema.html',
                  {'work_flow_schema': upload_wfschema, 'upload_data_company': upload_data_company,
                   'upload_data_apptypes': upload_data_apptypes,
                   'dropdown_db_values': dropdown_db_values, 'messages_list': messages_list,
                   'master_data_settings': master_data_settings,
                   'inc_nav': True})


def spend_limit_value(request):
    client = getClients(request)
    upload_spndlimval = list(
        SpendLimitValue.objects.filter(client=client, del_ind=False).values('spend_lim_value_guid', 'spend_code_id',
                                                                            'upper_limit_value', 'currency_id',
                                                                            'company_id'))
    for spend_code_fd in upload_spndlimval:
        if django_query_instance.django_existence_check(SpendLimitId,
                                                        {'del_ind': False,
                                                         'spend_code_id': spend_code_fd['spend_code_id']}):
            spend_code_fd["del_ind_flag"] = False
        else:
            spend_code_fd["del_ind_flag"] = True
    upload_data_company = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))
    upload_data_currency = list(Currency.objects.filter(del_ind=False).values('currency_id'))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    master_data_settings = 'master_data_settings'
    return render(request, 'Spend_Limit_data/spend_limit_value.html',
                  {'spend_limit_value': upload_spndlimval, 'upload_data_company': upload_data_company,
                   'upload_data_currency': upload_data_currency, 'messages_list': messages_list,
                   'master_data_settings': master_data_settings,
                   'inc_nav': True})


def approval_limit(request):
    client = getClients(request)

    upload_applimit = list(
        ApproverLimit.objects.filter(client=client, del_ind=False).values('app_guid', 'approver_username',
                                                                          'app_code_id', 'company_id'))
    upload_data_company = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))
    upload_data_app_code_id = list(
        ApproverLimitValue.objects.filter(client=client, del_ind=False).values('app_lim_dec_guid', 'app_types',
                                                                               'app_code_id', 'currency_id',
                                                                               'upper_limit_value', 'company_id'))

    user_details = list(UserData.objects.filter(is_active=True, client=client, del_ind=False).values('username'))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    master_data_settings = 'master_data_settings'
    return render(request, 'Approval_Data/approval_limit.html',
                  {'approval_limit': upload_applimit, 'upload_data_company': upload_data_company,
                   'upload_data_app_code_id': upload_data_app_code_id,
                   'master_data_settings': master_data_settings, 'messages_list': messages_list,
                   'user_details': user_details,
                   'inc_nav': True})


def approval_limit_value(request):
    client = getClients(request)
    upload_applimval = list(
        ApproverLimitValue.objects.filter(client=client, del_ind=False).values('app_lim_dec_guid', 'app_types',
                                                                               'app_code_id', 'currency_id',
                                                                               'upper_limit_value', 'company_id'))
    for app_lmtval_fd in upload_applimval:
        if django_query_instance.django_existence_check(ApproverLimit,
                                                        {'del_ind': False,
                                                         'app_code_id': app_lmtval_fd['app_code_id']}):
            app_lmtval_fd["del_ind_flag"] = False
        else:
            app_lmtval_fd["del_ind_flag"] = True
    upload_data_apptypes = list(ApproverType.objects.filter(del_ind=False).values('app_types'))
    upload_data_currency = list(Currency.objects.filter(del_ind=False).values('currency_id'))
    # upload_data_company = list(OrgCompanies.objects.filter(del_ind=False).values('company_id'))
    upload_data_company = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    master_data_settings = 'master_data_settings'
    return render(request, 'Approval_Data/approval_limit_value.html',
                  {'approval_limit_value': upload_applimval, 'upload_data_apptypes': upload_data_apptypes,
                   'upload_data_currency': upload_data_currency, 'upload_data_company': upload_data_company,
                   'master_data_settings': master_data_settings, 'messages_list': messages_list,
                   'inc_nav': True})


def spend_limit_id(request):
    client = getClients(request)
    upload_spndlimid = list(
        SpendLimitId.objects.filter(client=client, del_ind=False).values('spend_guid', 'spend_code_id',
                                                                         'spender_username', 'company_id'))

    upload_spndlimval = list(
        SpendLimitValue.objects.filter(client=client, del_ind=False).values('spend_lim_value_guid', 'spend_code_id',
                                                                            'upper_limit_value', 'currency_id',
                                                                            'company_id'))
    upload_data_company = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))
    user_details = list(UserData.objects.filter(is_active=True, client=client, del_ind=False).values('username'))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    master_data_settings = 'master_data_settings'
    return render(request, 'Spend_Limit_data/spend_limit_id.html',
                  {'spend_limit_id': upload_spndlimid, 'upload_data_company': upload_data_company,
                   'spend_limit_value': upload_spndlimval,
                   'master_data_settings': master_data_settings, 'messages_list': messages_list,
                   'user_details': user_details, 'inc_nav': True})


def work_flow_accounting(request):
    client = getClients(request)
    upload_wfacc = list(
        WorkflowACC.objects.filter(client=client, del_ind=False).values('workflow_acc_guid', 'app_username',
                                                                        'acc_value', 'sup_acc_value',
                                                                        'account_assign_cat', 'sup_account_assign_cat',
                                                                        'company_id', 'sup_company_id', 'currency_id'))
    upload_data_acccat = list(AccountAssignmentCategory.objects.filter(del_ind=False).values('account_assign_cat'))
    upload_data_currency = list(Currency.objects.filter(del_ind=False).values('currency_id'))
    upload_data_company = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))
    upload_data_OrgCompanies = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))
    user_details = list(UserData.objects.filter(is_active=True, client=client, del_ind=False).values('username'))
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    master_data_settings = 'master_data_settings'
    return render(request, 'Work_Flow_Data/work_flow_accounting.html',
                  {'work_flow_accounting': upload_wfacc, 'upload_data_acccat': upload_data_acccat,
                   'upload_data_currency': upload_data_currency, 'upload_data_company': upload_data_company,
                   'upload_data_OrgCompanies': upload_data_OrgCompanies, 'master_data_settings': master_data_settings
                      , 'user_details': user_details, 'messages_list': messages_list, 'inc_nav': True})


def extract_incoterms_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Incoterms.CSV"'

    writer = csv.writer(response)

    writer.writerow(['INCOTERM_KEY', 'DESCRIPTION', 'del_ind'])

    incoterm = django_query_instance.django_filter_query(Incoterms,
                                                         {'del_ind': False}, None,
                                                         ['incoterm_key', 'description', 'del_ind'])
    incoterm_data = query_update_del_ind(incoterm)

    for inco_data in incoterm_data:
        incotermdata_info = [inco_data['incoterm_key'], inco_data['description'], inco_data['del_ind']]
        writer.writerow(incotermdata_info)

    return response


def extract_payterms_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Payment_terms_desc.CSV"'

    writer = csv.writer(response)

    writer.writerow(['LANGUAGE_ID', 'PAYMENT_TERM_KEY', 'DESCRIPTION', 'DAY_LIMIT', 'del_ind'])

    payment_term = django_query_instance.django_filter_query(Payterms_desc,
                                                             {'del_ind': False,
                                                              'client': global_variables.GLOBAL_CLIENT}, None,
                                                             ['language_id', 'payment_term_key', 'description',
                                                              'day_limit', 'del_ind'])

    payterm_data = query_update_del_ind(payment_term)

    for paytem_desc_data in payterm_data:
        paytermdata_info = [paytem_desc_data['language_id'], paytem_desc_data['payment_term_key'],
                            paytem_desc_data['description'],
                            paytem_desc_data['day_limit'], paytem_desc_data['del_ind']]
        writer.writerow(paytermdata_info)

    return response


def extract_payterm_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Payterm_desc_template.CSV"'

    writer = csv.writer(response)

    writer.writerow(['LANGUAGE_ID', 'PAYMENT_TERM_KEY', 'DESCRIPTION', 'DAY_LIMIT', 'DEL_IND'])

    return response


def extract_spendlimitval_data_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Spend Limit Value Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(['COMPANY_ID', 'SPEND_CODE_ID', 'UPPER_LIMIT_VALUE', 'CURRENCY_ID', 'del_ind'])
    return response


def extract_accdesc_data_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Account Assingment Description Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(
        ['ACCOUNT_ASSIGN_VALUE', 'DESCRIPTION', 'ACCOUNT_ASSIGN_CAT', 'COMPANY_ID', 'LANGUAGE_ID', 'del_ind'])
    return response


def extract_aav_data_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Account Assingment Values Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(['ACC_ASSIGN_VALUE', 'ACCOUNT_ASSIGN_CAT', 'COMPANY_ID', 'VAILD_FROM', 'VAILD_TO', 'del_ind'])
    return response


def extract_address_data_Template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Address Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(
        ['ADDRESS_NUMBER', 'TITLE', 'NAME1', 'NAME2', 'STREET', 'AREA', 'LANDMARK', 'CITY',
         'ADDRESS_PARTNER_TYPE', 'postal_code', 'REGION', 'MOBILE_NUMBER', 'TELEPHONE_NUMBER',
         'FAX_NUMBER', 'EMAIL', 'COUNTRY_CODE',
         'LANGUAGE_ID', 'TIME_ZONE', 'del_ind'])
    return response


def extract_approverlimit_data_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Approval Limit Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(['APPROVER_USERNAME', 'APP_CODE_ID', 'COMPANY_ID', 'del_ind'])
    return response


def extract_approverlimitval_data_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Approval Limit Value Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(['COMPANY_ID', 'APP_TYPES', 'APP_CODE_ID', 'UPPER_LIMIT_VALUE', 'CURRENCY_ID', 'del_ind'])
    return response


def extract_orgcompany_data_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="OrgCompany Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(['COMPANY_ID', 'NAME1', 'NAME2', 'del_ind'])
    return response
