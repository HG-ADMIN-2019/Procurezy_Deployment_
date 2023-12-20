"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    admin_tool.py
Usage:
   Renders admin tool page
Author:
    Varsha
"""

# Function to display home page of shopping cart app
import csv
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from pymysql import NULL

# from eProc_Application_Monitoring.Utilities.application_monitoring_generic import application_monitoring_docnum_search
from requests import request

from eProc_Attributes.models.org_attribute_models import OrgAttributesLevel
from eProc_Basic.Utilities.constants.constants import CONST_DATE_FORMAT, CONST_DECIMAL_NOTATION, \
    CONST_ERROR_SPLIT_CRITERIA, CONST_OTHER_ERROR, CONST_COFIG_UI_MESSAGE_LIST
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import encrypt, decrypt
from eProc_Basic.Utilities.functions.get_db_query import get_country_id, getClients, get_user_id_by_email_id
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.messages_config import get_message_desc
from eProc_Basic.Utilities.functions.str_concatenate import concatenate_str
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic_Settings.views import JsonParser_obj
from eProc_Configuration.Utilities.application_settings_generic import get_ui_messages
from eProc_Configuration.models import *
from eProc_Configuration.models.application_data import WorkflowSchema
from eProc_Configuration.models.basic_data import Country
from eProc_Configuration.models.development_data import FieldTypeDescription
from eProc_Configuration.models.master_data import OrgPorg, OrgCompanies, WorkflowACC, ApproverLimit, \
    ApproverLimitValue, AccountingData, AccountingDataDesc
from eProc_Doc_Search_and_Display.Utilities.search_display_generic import get_hdr_data, get_hdr_data_app_monitoring
from eProc_Emails.models import EmailUserMonitoring, EmailDocumentMonitoring, EmailSupplierMonitoring
from eProc_Org_Model.Utilities import client
from eProc_Org_Model.models.org_model import OrgModel
# from eProc_Org_Support.views import org_announcement_search
from eProc_Org_Support.models.org_support_models import OrgAnnouncements
from eProc_Org_Support.views import org_announcement_search
from eProc_Purchase_Order.Utilities.purchase_order_generic import CreatePurchaseOrder, retrigger_po, check_po
from eProc_Registration.models import UserData
from eProc_Registration.models.registration_model import UserDataHistory
from eProc_Reports.Report_Forms.SearchDoc_forms import DocumentSearchForm, ApplicationMonitoringForm, \
    EmailUserMonitoringForm
from eProc_Reports.Report_Forms.user_report_form import UserReportForm
from eProc_Reports.Utilities.reports_generic import get_companylist, get_usrid_by_username, get_account_assignlist, \
    get_langlist, get_companyDetails, get_account_assignvalues
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import get_supplier_details
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Shopping_Cart.models import ScItem, ScPotentialApproval, ScApproval
from eProc_Shopping_Cart.models.shopping_cart import ScHeader
from eProc_Suppliers.Utilities.supplier_generic import supplier_detail_search
from eProc_Suppliers.Utilities.supplier_specific import get_supplier_data, update_country_encrypt
from eProc_Suppliers.models import OrgSuppliers
from eProc_Users.Utilities.user_generic import user_detail_search, get_usertype_values, \
    get_emp_data, emp_search_data, set_search_data, get_supplier_type_values, get_output_medium_values
from django.http import QueryDict
import sys
from datetime import datetime
from time import mktime, strptime

django_query_instance = DjangoQueries()


@login_required
def admin_tool(req):
    """
    :param req:
    :return:
    """
    context = {
        'inc_nav': True,
        'inc_footer': True,
    }
    return render(req, 'Admin_Tool/admin_tool_nav.html', context)


def user_date_format_array():
    date_format_array = CONST_DATE_FORMAT
    date_format_list = date_format_array

    return date_format_list


def user_decimal_list():
    decimal_array = CONST_DECIMAL_NOTATION
    decimal_list = decimal_array

    return decimal_list


def user_currency_id():
    currency_id = django_query_instance.django_filter_query(Currency, {'del_ind': False}, None,
                                                            ['currency_id', 'description'])

    return currency_id


def user_time_zones():
    time_zones = django_query_instance.django_filter_query(TimeZone, {'del_ind': False}, None,
                                                           ['time_zone', 'description'])

    return time_zones


def user_language_list():
    language_list = django_query_instance.django_filter_query(Languages, {'del_ind': False}, None,
                                                              ['language_id', 'description'])

    return language_list


def user_details_drpdown():
    dropdown_usertype_values = ['Buyer', 'Support']

    return dropdown_usertype_values


def user_messages_list():
    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    return messages_list


def user_search(request):
    update_user_info(request)
    dropdown_user = user_details_drpdown()
    dropdown_user_date_format = user_date_format_array()
    dropdown_decimal_list = user_decimal_list()
    dropdown_currency_id = user_currency_id()
    dropdown_time_zones = user_time_zones()
    dropdown_language = user_language_list()
    dropdown_messages = user_messages_list()
    employee_results_onload = get_emp_data()
    count = len(employee_results_onload)
    form_method = 'POST'

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'get_country_id': get_country_id(),
        'is_admin_active': True,
        'dropdown_usertype_values': get_usertype_values(),
        'dropdown_user': dropdown_user,
        'dropdown_user_date_format': dropdown_user_date_format,
        'dropdown_decimal_list': dropdown_decimal_list,
        'dropdown_currency_id': dropdown_currency_id,
        'dropdown_time_zones': dropdown_time_zones,
        'dropdown_language': dropdown_language,
        'dropdown_messages': dropdown_messages,
        'employee_results_onload': employee_results_onload,
        'count': count,
    }

    if request.method == 'GET':
        encrypted_email = []
        employee_results = get_emp_data()
        context['employee_results'] = employee_results
        count = len(employee_results)
        context['count'] = count
        context['form_method'] = 'GET'
        return render(request, 'User Search/user_search.html', context)
    if request.method == 'POST':
        search_fields = {}
        for data in request.POST:
            if data != 'csrfmiddlewaretoken':
                value = request.POST[data]
                if data == 'user_locked':
                    value = set_search_data(value)
                if data == 'pwd_locked':
                    value = set_search_data(value)
                if data == 'is_active':
                    value = set_search_data(value)
                if value != '':
                    search_fields[data] = value

        search_fields['username'] = request.POST.get('username')
        search_fields['first_name'] = request.POST.get('first_name')
        search_fields['last_name'] = request.POST.get('last_name')
        search_fields['email'] = request.POST.get('email')
        search_fields['user_type'] = request.POST.get('user_type')
        search_fields['employee_id'] = request.POST.get('employee_id')
        if search_fields['username'] == '*':
            employee_results = get_emp_data()
        else:
            employee_results = emp_search_data(search_fields)
        count = len(employee_results)
        context['count'] = count
        context['form_method'] = 'POST'
        context['employee_results'] = employee_results

    return render(request, 'User Search/user_search.html', context)


def supplier_search(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    country_dictionary_list = django_query_instance.django_filter_query(Country,
                                                                        None, None, ['country_code', 'country_name'])
    supp_data_onload = get_supplier_data()
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'get_country_id': country_dictionary_list,
        'purch_org_list': django_query_instance.django_filter_value_list_query(OrgPorg, {
            'client': global_variables.GLOBAL_CLIENT,
            'del_ind': False}, 'porg_id'),
        'is_admin_active': True,
        'dropdown_suptype_values': get_supplier_type_values(),
        'supp_data_onload': supp_data_onload,
    }

    if request.method == 'GET':
        supplier_id_encrypted = []
        supplier_results = get_supplier_data()
        count = len(supplier_results)
        context['count'] = count
        context['form_method'] = 'GET'
        context['supplier_results'] = supplier_results

    if request.method == 'POST':
        supplier_id_encrypted = []
        search_fields = {}
        for data in request.POST:
            if data != 'csrfmiddlewaretoken':
                value = request.POST[data]
                if data == 'block':
                    if value == 'on':
                        value = True
                    else:
                        value = False
                if value != '':
                    search_fields[data] = value

        search_fields['name1'] = request.POST.get('name1')
        search_fields['name2'] = request.POST.get('name2')
        search_fields['supplier_id'] = request.POST.get('supplier_id')
        search_fields['email'] = request.POST.get('email')
        search_fields['supplier_type'] = request.POST.get('supplier_type')
        search_fields['country_code'] = request.POST.get('country_code')
        search_fields['city'] = request.POST.get('city')
        search_fields['block'] = request.POST.get('block')
        search_fields['purchasing_org'] = request.POST.get('purchasing_org')

        supplier_results = supplier_detail_search(**search_fields)
        count = len(supplier_results)
        context['count'] = count
        context['supplier_results'] = update_country_encrypt(supplier_results)

    return render(request, 'Supplier Search/supplier_search.html', context)


@login_required
def user_details(request, email):
    """
    Gets the user details and render it in the user details page
    :param request: Form Request
    :param email: Email id (login id)
    :return: User details page
    """
    if email != 'None':
        user_action = 'UPDATE'
        email = decrypt(email)
    else:
        user_action = 'CREATE'
    update_user_info(request)
    date_format_array = CONST_DATE_FORMAT
    decimal_array = CONST_DECIMAL_NOTATION

    user_info = django_query_instance.django_get_query(UserData,
                                                       {'email': email, 'client': getClients(request),
                                                        'del_ind': False})
    user_info1 = django_query_instance.django_filter_only_query(UserData,
                                                                {'email': email, 'client': getClients(request),
                                                                 'del_ind': False})

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'user_info': user_info,
        'user_action': user_action,
        'currency_id': django_query_instance.django_filter_query(Currency, {'del_ind': False}, None,
                                                                 ['currency_id', 'description']),
        'time_zones': django_query_instance.django_filter_query(TimeZone, {'del_ind': False}, None,
                                                                ['time_zone', 'description']),
        'language_list': django_query_instance.django_filter_query(Languages, {'del_ind': False}, None,
                                                                   ['language_id', 'description']),
        'dropdown_usertype_values': ['Buyer', 'Support'],
        'decimal_list': decimal_array,
        'date_format_list': date_format_array,
    }

    return render(request, 'Display Edit User/display_edit_user.html', context)


@login_required
def sup_details(req, supplier_id):
    """
    Gets the selected supplier details and render it in the supplier details pop-up page
    :param supplier_id:
    :param req: Form Request
    :return: Supplier details pop-up page
    """
    if supplier_id != 'None':
        supplier_action = 'UPDATE'
        supplier_id = decrypt(supplier_id)
        form_method = ''
    else:
        supplier_action = 'CREATE'
        form_method = 'GET'
    update_user_info(req)
    supplier_info = django_query_instance.django_get_query(SupplierMaster, {'supplier_id': supplier_id,
                                                                            'client': global_variables.GLOBAL_CLIENT})

    supplier_org_info = django_query_instance.django_filter_query(OrgSuppliers, {'supplier_id': supplier_id,
                                                                                 'client': getClients(req),
                                                                                 'del_ind': False}, None, None)

    django_query_instance.django_filter_value_list_query(Languages, {'del_ind': False}, 'language_id')

    supp_img_info = django_query_instance.django_filter_only_query(ImagesUpload, {
        'image_id': supplier_id, 'client': getClients(req), 'del_ind': False})

    img_url = []
    for img in supp_img_info:
        img_url.append(img.image_url)

    messages_list = get_ui_messages(CONST_COFIG_UI_MESSAGE_LIST)
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'supplier_action': supplier_action,
        'form_method': form_method,
        'supplier_info': supplier_info,
        'img_url': img_url,
        'supplier_org_info': supplier_org_info,
        'purch_org_list': django_query_instance.django_filter_value_list_query(OrgPorg, {
            'client': global_variables.GLOBAL_CLIENT,
            'del_ind': False}, 'porg_id'),

        'currency_id': django_query_instance.django_filter_query(Currency, {'del_ind': False}, None,
                                                                 ['currency_id', 'description']),
        'payterm_list': django_query_instance.django_filter_value_list_query(Payterms, {
            'client': global_variables.GLOBAL_CLIENT,
            'del_ind': False}, 'payment_term_key'),

        'incoterm_list': django_query_instance.django_filter_value_list_query(Incoterms, {'del_ind': False},
                                                                              'incoterm_key'),
        'country_list': django_query_instance.django_filter_query(Country, {'del_ind': False}, None,
                                                                  ['country_code', 'country_name']),
        'language_list': django_query_instance.django_filter_query(Languages, {'del_ind': False}, None,
                                                                   ['language_id', 'description']),
        'supp_img_info': supp_img_info,
        'dropdown_suptype_values': get_supplier_type_values(),
        'dropdown_output_med_values': get_output_medium_values(),
        'messages_list': messages_list,
    }

    return render(req, 'Display Edit Supplier/display_edit_supplier.html', context)


@login_required
def user_report(request):
    user_rep_form = UserReportForm()
    final_list = []
    client = getClients(request)
    page_range = 0
    company_list = get_companylist(request)
    # company_list.reverse()
    default_comp_id = ''

    if request.method == 'GET':
        default_comp_id = '2000'

        if 'final_list' in request.session:
            request.POST = request.session['final_list']
            request.method = 'POST'
        default_user_data = django_query_instance.django_filter_query(UserData,
                                                                      {'del_ind': False, 'is_active': True, },
                                                                      None, None)
        comp_details = django_query_instance.django_get_query(OrgCompanies, {'client': client, 'del_ind': False,
                                                                             'company_id': default_comp_id})

        # ---------------------------------------------------------------------
        user_list_star = django_query_instance.django_filter_only_query(UserData, {'is_active': True})
        ####################################################################################
        if default_comp_id is not None:
            # UserData
            company_details = OrgCompanies.objects.filter(client=client, del_ind=False, company_id=default_comp_id)
            # Using the company code number and CCODE node type get the company details from Org Model table
            for comp_det in company_details:
                comp_obj_id_info = OrgModel.objects.filter(Q(object_id=comp_det.object_id_id, node_type='CCODE',
                                                             client=client, del_ind=False))

                # Using the Company Details - node_guid read the NODE type which has company code node_guid
                # as parent_node from the Org Model table
                for comp in comp_obj_id_info:
                    node_info = OrgModel.objects.filter(Q(parent_node_guid=comp.node_guid, node_type='NODE',
                                                          client=client, del_ind=False))

                    # Using the node info guid read all the users that have parent_node as the node guid.
                    for node in node_info:
                        user_list = OrgModel.objects.filter(Q(parent_node_guid=node.node_guid, node_type='USER',
                                                              client=client, del_ind=False))

                        # Using the user_list from the Org Model read the user details
                        for user_obj_id in user_list:
                            user_details = UserData.objects.filter(
                                Q(object_id=user_obj_id.object_id, is_active=True,
                                  client=client, del_ind=False))

                            final_array = []

                            for user in user_details:
                                final_array.append(comp_det.company_id)
                                final_array.append(concatenate_str(comp_det.name1, comp_det.name2))
                                final_array.append(user.username)
                                final_array.append(user.last_name)
                                final_array.append(user.first_name)
                                final_array.append(user.email)
                                final_array.append(user.user_locked)
                                final_list.append(final_array)
        t_count = len(final_list)
        context = {
            'inc_nav': True,
            'inc_footer': True,
            'user_rep_form': user_rep_form,
            'final_list': final_list,
            'default_comp_id': default_comp_id,
            't_count': t_count,
            'page_range': page_range,
            'company_list': company_list,
            'is_slide_menu': True,
            'is_admin_active': True
        }
        return render(request, 'Reports/user_report.html', context)

    # If method is post get the form values and get header details accordingly
    if request.method == 'POST':
        request.session['final_list'] = request.POST
        user_rep_form = UserReportForm(request.POST)

        if user_rep_form.is_valid():
            inp_comp_code = request.POST.get('company_code')
            inp_username = request.POST.get('username')
            inp_active = request.POST.get('user_status')

            if inp_active == 'Active' or inp_active is None:  # Consider "Active" when inp_active is None
                active = True
            else:
                active = False

            if inp_username is not None and inp_username != '':
                username = inp_username

                user_list_star = get_usrid_by_username(username, active)

                for list in user_list_star:
                    print("* in user name list", list.username)
                    print(list.email)
            else:
                user_list_star = django_query_instance.django_filter_only_query(UserData, {'is_active': active})
            ####################################################################################
            if inp_comp_code is not None:
                # Check if inp_comp_code is '*'
                if inp_comp_code == '*':
                    # Retrieve data for all companies
                    company_details = OrgCompanies.objects.filter(client=client, del_ind=False)
                else:
                    # Retrieve data for the selected company code
                    company_details = OrgCompanies.objects.filter(client=client, del_ind=False,
                                                                  company_id=inp_comp_code)

                # Continue processing as before...
                # Using the company code number and CCODE node type get the company details from Org Model table
                for comp_det in company_details:
                    comp_obj_id_info = OrgModel.objects.filter(Q(object_id=comp_det.object_id_id, node_type='CCODE',
                                                                 client=client, del_ind=False))
                    ###################################################################
                    if inp_username is not None and inp_username != '':
                        for user_info in user_list_star:
                            confirm_in_comp = OrgModel.objects.filter(
                                Q(node_type='USER', name=user_info.username,
                                  client=client, del_ind=False))
                            final_array = []
                            if confirm_in_comp:
                                final_array.append(comp_det.company_id)
                                final_array.append(concatenate_str(comp_det.name1, comp_det.name2))
                                final_array.append(user_info.username)
                                final_array.append(user_info.last_name)
                                final_array.append(user_info.first_name)
                                final_array.append(user_info.email)
                                final_array.append(user_info.user_locked)
                                final_list.append(final_array)
                    else:
                        # Using the Company Details - node_guid read the NODE type which has company code node_guid
                        # as parent_node from the Org Model table
                        for comp in comp_obj_id_info:
                            node_info = OrgModel.objects.filter(Q(parent_node_guid=comp.node_guid, node_type='NODE',
                                                                  client=client, del_ind=False))

                            # Using the node info guid read all the users that have parent_node as the node guid.
                            for node in node_info:
                                user_list = OrgModel.objects.filter(Q(parent_node_guid=node.node_guid, node_type='USER',
                                                                      client=client, del_ind=False))

                                # Using the user_list from the Org Model read the user details
                                for user_obj_id in user_list:
                                    user_details = UserData.objects.filter(
                                        Q(object_id=user_obj_id.object_id, is_active=active,
                                          client=client, del_ind=False))
                                    final_array = []
                                    for user in user_details:
                                        print('User in Company:', user.first_name, user.username)
                                        final_array.append(comp_det.company_id)
                                        final_array.append(concatenate_str(comp_det.name1, comp_det.name2))
                                        final_array.append(user.username)
                                        final_array.append(user.last_name)
                                        final_array.append(user.first_name)
                                        final_array.append(user.email)
                                        final_array.append(user.user_locked)
                                        final_list.append(final_array)
            else:
                print(user_rep_form.errors)

            # Company code, Company name, Username, Last name, First name, Email address, Ship to address, user lock status
            user_rep_form = UserReportForm()
            t_count = len(final_list)

            context = {
                'inc_nav': True,
                'inc_footer': True,
                'user_rep_form': user_rep_form,
                'final_list': final_list,
                'default_comp_id': default_comp_id,
                'page_range': page_range,
                't_count': t_count,
                'company_list': company_list,
                'is_slide_menu': True,
                'is_admin_active': True
            }

            return render(request, 'Reports/user_report.html', context)


@login_required
def approval_report(request):
    client = getClients(request)
    final_list = []
    inp_acc_assgn_cat = []
    company_array = get_companyDetails(request)
    acc_value_array = get_account_assignvalues(request)

    if request.method == 'GET':
        # Handle the page load (GET) request
        inp_comp_code = company_array[0]  # Set to None by default
        inp_acc_assgn_cat = [acc['account_assign_cat'] for acc in acc_value_array]  # Select all account assignment categories
    elif request.method == 'POST':
        # Handle the form submission (POST) request
        inp_acc_assgn_cat = request.POST.getlist('acc_assgn_cat', default=None)
        inp_comp_code = request.POST.get('comp_code_app')

    workflow_schema = list(
        WorkflowSchema.objects.filter(Q(client=client)).values_list('app_types', flat=True))
    if workflow_schema:
        unique_entries = set()  # Create a set to store unique entries
        for schema_step_type in workflow_schema:
            if inp_comp_code == '*':
                # Query all companies and all account assignment categories when inp_comp_code is "*"
                workflow_acc_list = WorkflowACC.objects.filter(
                    Q(account_assign_cat__in=inp_acc_assgn_cat, client=client))
            else:
                # Query for a specific company and specified account assignment categories when inp_comp_code is not "*"
                workflow_acc_list = WorkflowACC.objects.filter(
                    Q(account_assign_cat__in=inp_acc_assgn_cat, company_id=inp_comp_code, client=client))

            if workflow_acc_list:
                for w_acc_list in workflow_acc_list:
                    app_code_id = ApproverLimit.objects.filter(
                        Q(approver_username=w_acc_list.app_username, del_ind=False, client=client)).values_list('app_code_id', flat=True)

                    if app_code_id:
                        app_val_list = ApproverLimitValue.objects.filter(
                            Q(app_code_id__in=app_code_id, del_ind=False, app_types=schema_step_type, client=client))

                        for app_val in app_val_list:
                            # Create a unique identifier for the entry
                            entry_identifier = (
                                w_acc_list.company_id,
                                w_acc_list.account_assign_cat_id,
                                w_acc_list.acc_value,
                                w_acc_list.app_username,
                                w_acc_list.currency_id,
                                w_acc_list.sup_company_id,
                                w_acc_list.sup_acc_value,
                                app_val.upper_limit_value,
                                app_val.currency_id,
                                app_val.app_code_id,
                                w_acc_list.sup_account_assign_cat_id,
                                app_val.app_code_id,
                            )

                            if entry_identifier not in unique_entries:
                                # Add the entry to final_list and mark it as visited in the set
                                final_list.append(entry_identifier)
                                unique_entries.add(entry_identifier)

    t_count = len(final_list)
    # Context to display in Doc_report.html
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'comp_list': company_array,
        'acct_val_list': acc_value_array,
        'final_list': final_list,
        'page_range': 0,
        't_count': t_count,
        'inp_acc_assgn_cat': inp_acc_assgn_cat,
        'inp_comp_code': inp_comp_code,
        'is_slide_menu': True,
        'is_admin_active': True
    }

    return render(request, 'Reports/approval_report.html', context)






@login_required
def m_docsearch_meth(request):
    """
    :param request:
    :return:
    """
    inp_doc_type = ''
    result = ''
    page_range = 0
    report_search = False
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    sc_header = []
    sc_appr = []
    sc_completion = []
    encrypted_header_guid = []
    sc_completion_flag = False
    page_type_flag = 'Doc_reports'
    rep_search_form = {}
    error_messages = ''
    # company code list- client n del indicator
    # users in selected company - client n del indicator
    comp_list = get_companylist(request)

    if request.method == 'GET':
        inp_doc_type = 'SC'
        inp_doc_num = None
        inp_from_date = datetime.today()
        inp_to_date = datetime.today()
        inp_supl = None
        inp_created_by = ''
        inp_requester = ''

        result = get_hdr_data(request,
                              inp_doc_type,
                              inp_doc_num,
                              inp_from_date,
                              inp_to_date,
                              inp_supl,
                              inp_created_by,
                              inp_requester, report_search)

        company_details = OrgCompanies.objects.filter(client=client, del_ind=False, company_guid=1000)
        for comp in company_details:
            if inp_doc_type == 'PO':
                result = result.filter(company_code_id=comp.company_id)
            else:  # For ScHeader queries
                result = result.filter(co_code=comp.company_id)

    if not request.method == 'POST':
        if 'results' in request.session:
            request.POST = request.session['results']
            request.method = 'POST'

    if request.method == 'POST':
        request.session['results'] = request.POST

    if request.method == 'POST':
        rep_search_form = DocumentSearchForm(request.POST)

        if rep_search_form.is_valid():
            inp_comp_code = request.POST.get('company_code')
            inp_doc_type = request.POST.get('doc_type')
            inp_doc_num = request.POST.get('doc_num')
            inp_from_date = request.POST.get('from_date')
            inp_to_date = request.POST.get('to_date')
            inp_supl = request.POST.get('supplier')
            inp_created_by = request.POST.get('created_by')
            inp_requester = request.POST.get('requester')

            result = get_hdr_data(request, inp_doc_type,
                                  inp_doc_num,
                                  inp_from_date,
                                  inp_to_date,
                                  inp_supl,
                                  inp_created_by,
                                  inp_requester, report_search)
            company_details = OrgCompanies.objects.filter(client=client, del_ind=False, company_guid=inp_comp_code)
            for comp in company_details:
                if inp_doc_type == 'PO':
                    result = result.filter(company_code_id=comp.company_id)
                else:  # For ScHeader queries
                    result = result.filter(co_code=comp.company_id)
    else:
        rep_search_form = DocumentSearchForm()

    error_messages = rep_search_form.errors
    t_count = len(result)

    for header_guid in result:
        encrypted_header_guid.append(encrypt(header_guid))

    result = zip(result, encrypted_header_guid)
    # Assuming you can retrieve the 'client' and 'supp_id_up' values from your code context
    client = getClients(request)
    supp_id_up = []

    # Call the function with the appropriate arguments
    supplier_details = get_supplier_details(client, supp_id_up)

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'nav_title': 'Search for document',
        'sform': rep_search_form,
        'results': result,
        'page_range': page_range,
        't_count': t_count,
        'inp_doc_type': inp_doc_type,
        'comp_list': comp_list,
        'is_slide_menu': True,
        'is_admin_active': True,
        'encrypted_header_guid': encrypted_header_guid,
        'sc_completion': sc_completion,
        'sc_completion_flag': sc_completion_flag,
        'sc_header': sc_header,
        'error_messages': error_messages,
        'supplier_details': supplier_details
    }

    return render(request, 'Reports/Doc_report.html', context)


@login_required
def accnt_report(request):
    client = getClients(request)
    lang_array = get_langlist(request)
    acc_value_array = get_account_assignvalues(request)
    acc_cat_array = get_account_assignlist(request)
    company_array = get_companylist(request)
    company_array.reverse()
    company_array.reverse()
    inp_acc_assgn_cat = [item['account_assign_cat'] for item in acc_value_array]
    inp_comp_code = company_array[0]['company_id'] if company_array else None
    inp_lang = lang_array[0]['language_id'] if lang_array else 'EN'

    if request.method == 'GET':
        # Check if inp_comp_code is not '*'
        if inp_comp_code and inp_comp_code != '*':
            account_list = AccountingData.objects.filter(
                client=client,
                company_id=inp_comp_code,
                account_assign_cat__in=inp_acc_assgn_cat,
                del_ind=False
            )
        else:
            account_list = AccountingData.objects.filter(
                client=client,
                account_assign_cat__in=inp_acc_assgn_cat,
                del_ind=False
            )

        final_list = []
        for account_data in account_list:
            account_desc_data_list = AccountingDataDesc.objects.filter(
                client=client,
                company_id=account_data.company_id,
                del_ind=False,
                language_id=inp_lang,
                account_assign_value=account_data.account_assign_value,
                account_assign_cat=account_data.account_assign_cat
            )
            result_array = []
            for data in account_desc_data_list:
                result_array.append(account_data.company_id)
                result_array.append(account_data.account_assign_cat)
                result_array.append(account_data.account_assign_value)
                result_array.append(data.description)
                lang_id = data.language_id
                for lang in lang_array:
                    if lang['language_id'] == str(lang_id):
                        lang_desc = lang['description']
                result_array.append(lang_desc)
                result_array.append(account_data.valid_from)
                result_array.append(account_data.valid_to)
            if result_array:
                final_list.append(result_array)  # Only add non-empty records

        t_count = len(final_list)

        context = {
            'inc_nav': True,
            'inc_footer': True,
            'is_slide_menu': True,
            'is_admin_active': True,
            'comp_list': company_array,
            'lang_list': lang_array,
            'acct_val_list': acc_value_array,
            'final_list': final_list,
            'page_range': 0,
            't_count': t_count,
            'inp_account_assgn_cat': inp_acc_assgn_cat,
            'acc_value_array': acc_value_array,
            'inp_comp_code': inp_comp_code,
            'inp_lang': inp_lang,
        }

        return render(request, 'Reports/accnt_report.html', context)

    if request.method == 'POST' or request.is_ajax():
        inp_comp_code = request.POST.get('comp_code_app')
        inp_account_assgn_cat = request.POST.getlist('acc_assgn_cat')
        inp_lang = request.POST.get('language')

        account_list = []

        if inp_comp_code is not None and inp_account_assgn_cat is not None:
            if inp_comp_code == '*':
                # Fetch data for all companies
                account_list = AccountingData.objects.filter(
                    client=client,
                    account_assign_cat__in=inp_account_assgn_cat,
                    del_ind=False
                )
            else:
                account_list = AccountingData.objects.filter(
                    client=client,
                    company_id=inp_comp_code,
                    account_assign_cat__in=inp_account_assgn_cat,
                    del_ind=False
                )

        final_list = []
        for account_data in account_list:
            account_desc_data_list = AccountingDataDesc.objects.filter(
                client=client,
                company_id=account_data.company_id,
                del_ind=False,
                language_id=inp_lang,
                account_assign_value=account_data.account_assign_value,
                account_assign_cat=account_data.account_assign_cat
            )
            result_array = []
            for data in account_desc_data_list:
                result_array.append(account_data.company_id)
                result_array.append(account_data.account_assign_cat)
                result_array.append(account_data.account_assign_value)
                result_array.append(data.description)
                lang_id = data.language_id
                for lang in lang_array:
                    if lang['language_id'] == str(lang_id):
                        lang_desc = lang['description']
                result_array.append(lang_desc)
                result_array.append(account_data.valid_from)
                result_array.append(account_data.valid_to)
            if result_array:
                final_list.append(result_array)  # Only add non-empty records

        t_count = len(final_list)

        context = {
            'inc_nav': True,
            'inc_footer': True,
            'is_slide_menu': True,
            'comp_list': company_array,
            'lang_list': lang_array,
            'acct_val_list': acc_cat_array,
            'final_list': final_list,
            'page_range': 0,
            't_count': t_count,
            'is_admin_active': True,
            'inp_account_assgn_cat': inp_acc_assgn_cat,
            'acc_value_array': acc_value_array,
            'inp_comp_code': inp_comp_code,
            'inp_lang': inp_lang,
        }

        return render(request, 'Reports/accnt_report.html', context)


def get_acct_report(request):
    client = getClients(request)
    final_list = []
    page_range = 0
    account_desc_data_list = ''

    acc_cat_array = get_account_assignlist(request)
    company_array = get_companylist(request)
    lang_array = get_langlist(request)
    inp_acc_assgn_cat = acc_cat_array[0]
    account_list = ''

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_admin_active': True,
        'comp_list': company_array,
        'lang_list': lang_array,
        'acct_val_list': acc_cat_array,
        'page_range': page_range,
        'inp_account_assgn_cat': acc_cat_array[0]
    }

    if request.method == 'POST' and request.is_ajax():
        data = JsonParser().get_json_from_req(request)
        inp_comp_code = data['comp_code']
        inp_account_assgn_cat = data['selected_acct_assmt']
        inp_lang = data['lang']

        if inp_comp_code is not None and inp_account_assgn_cat is not None:
            account_list = AccountingData.objects.filter(client=client, company_id=inp_comp_code,
                                                         account_assign_cat__in=inp_account_assgn_cat, del_ind=False)

        result_array = []
        for account_data in account_list:
            account_desc_data_list = AccountingDataDesc.objects.filter(client=client,
                                                                       company_id=account_data.company_id,
                                                                       del_ind=False,
                                                                       language_id=inp_lang,
                                                                       account_assign_value=account_data.account_assign_value,
                                                                       account_assign_cat=account_data.account_assign_cat)
            for data in account_desc_data_list:
                result_array.append(account_data.company_id)
                result_array.append(account_data.account_assign_cat)
                result_array.append(account_data.account_assign_value)
                result_array.append(data.description)
                result_array.append(data.language_id)
                result_array.append(account_data.valid_from)
                result_array.append(account_data.valid_to)
                final_list.append(result_array)
            # return final_list

        context['final_list'] = final_list
        t_count = len(final_list)
        context['t_count'] = t_count
        # print("final_list", final_list)

        # Context to display in Doc_report.html
        # context = {
        #     'inc_nav': True,
        #     'inc_footer': True,
        #     'comp_list': company_array,
        #     'lang_list': lang_array,
        #     'acct_val_list': acc_cat_array,
        #     # 'acct_rep_form' : acct_rep_form,
        #     'final_list': final_list,
        #     'page_range': page_range,
        #     't_count': t_count,
        #     'is_slide_menu': True,
        #     'is_admin_active': True,
        #     'inp_account_assgn_cat': acc_cat_array[0]
        # }
    return render(request, 'Reports/accnt_report.html', context)


def org_announcements_search(request):
    global t_count, announcement_result1
    encrypted_guid = []
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    status_dropdown_values = django_query_instance.django_filter_value_list_query(FieldTypeDescription, {
        'del_ind': False, 'field_name': 'status', 'client': global_variables.GLOBAL_CLIENT
    }, 'field_type_id')
    priority_dropdown_values = django_query_instance.django_filter_value_list_query(FieldTypeDescription, {
        'del_ind': False, 'field_name': 'Priority', 'client': global_variables.GLOBAL_CLIENT
    }, 'field_type_id')
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_admin_active': True,
        'status_dropdown_values': status_dropdown_values,
        'priority_dropdown_values': priority_dropdown_values,
    }

    if request.method == 'GET':
        announcement_result1 = OrgAnnouncements.objects.filter(client=client, del_ind=False)
        context['announcement_result1'] = announcement_result1
        return render(request, 'org_announcements_display.html', context)
    if request.method == 'POST':
        search_fields = {}
        for data in request.POST:
            if data != 'csrfmiddlewaretoken':
                value = request.POST[data]
                if data == 'block':
                    if value == 'on':
                        value = True
                    else:
                        value = False
                if value != '':
                    search_fields[data] = value

        search_fields['client'] = client
        search_fields['del_ind'] = False
        search_fields['status'] = request.POST.get('status')
        search_fields['priority'] = request.POST.get('priority')
        search_fields['announcement_subject'] = request.POST.get('announcement_subject')
        announcement_result1 = org_announcement_search(**search_fields)
        t_count = len(announcement_result1)

    for annsmt in announcement_result1:
        encrypted_guid.append(encrypt(annsmt['unique_announcement_id']))

    # print(encrypted_guid)
    context['announcement_result1'] = zip(announcement_result1, encrypted_guid)

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_admin_active': True,
        'status_dropdown_values': status_dropdown_values,
        'priority_dropdown_values': priority_dropdown_values,
        'announcement_result1': announcement_result1,
        't_count': t_count,
    }

    return render(request, 'org_announcements_display.html', context)


@login_required
def org_announcement_details(req, announcement_guid):
    """
    Gets the selected announcement details and render it in the Org Announcement details pop-up page
    :param announcement_guid:
    :param req: Form Request
    :return: Org Announcement details pop-up page
    """
    # supplier_id = decrypt(supplier_id)
    context = {}
    encrypted_guid = []
    update_user_info(req)
    # annsmt_guid = decrypt(announcement_guid)
    announcement_details = django_query_instance.django_get_query(OrgAnnouncements,
                                                                  {'unique_announcement_id': announcement_guid})
    from_date = announcement_details.announcement_from_date.strftime("%Y-%m-%d")
    to_date = announcement_details.announcement_to_date.strftime("%Y-%m-%d")
    selected_status = announcement_details.status

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
        'announcement_details': announcement_details,
        'status_dropdown_values': status_dropdown_values,
        'priority_dropdown_values': priority_dropdown_values,
        'selected_status': selected_status,
        'from_date': from_date,
        'to_date': to_date
    }

    return render(req, 'org_announcement_details.html', context)


def delete_user(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    success_message = ''
    user_data = JsonParser_obj.get_json_from_req(request)
    user_info = django_query_instance.django_filter_query(UserData,
                                                          {'email__in': user_data['data'],
                                                           'del_ind': False}, None, None)
    for user in user_info:
        delete_org_model_emp_data(user)
        delete_master_emp_data(user)
        django_query_instance.django_filter_delete_query(UserData, {'email': user['email'],
                                                                    'client': global_variables.GLOBAL_CLIENT})
        create_emp_history_data(user)
        success_message = get_message_desc('MSG206')[1]

    employee_results = django_query_instance.django_filter_query(UserData, {
        'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
    }, None, None)

    for emails in employee_results:
        encrypted_email1 = encrypt(emails['email'])
        emails['encrypted_email'] = encrypted_email1

    response = {'employee_results': employee_results, 'success_message': success_message}
    return JsonResponse(response, safe=False)


def create_emp_history_data(user):
    django_query_instance.django_create_query(UserDataHistory, {
        'client': global_variables.GLOBAL_CLIENT,
        'username': user['username'],
        'email': user['email'],
        'person_no': user['person_no'],
        'form_of_address': user['form_of_address'],
        'first_name': user['first_name'],
        'last_name': user['last_name'],
        'gender': user['gender'],
        'phone_num': user['phone_num'],
        'password': user['password'],
        'date_joined': user['date_joined'],
        'first_login': user['first_login'],
        'last_login': user['last_login'],
        'is_active': user['is_active'],
        'is_superuser': user['is_superuser'],
        'is_staff': user['is_staff'],
        'date_format': user['date_format'],
        'employee_id': user['employee_id'],
        'decimal_notation': user['decimal_notation'],
        'user_type': user['user_type'],
        'login_attempts': user['login_attempts'],
        'user_locked': user['user_locked'],
        'pwd_locked': user['pwd_locked'],
        'sso_user': user['sso_user'],
        'user_data_created_at': user['user_data_created_at'],
        'user_data_created_by': user['user_data_created_by'],
        'user_data_changed_at': user['user_data_changed_at'],
        'user_data_changed_by': user['user_data_changed_by'],
        'valid_from': user['valid_from'],
        'valid_to': user['valid_to'],
        'del_ind': user['del_ind'],
        'object_id': django_query_instance.django_get_query(OrgModel, {'object_id': user['object_id_id']}),
        'language_id': django_query_instance.django_get_query(Languages, {'language_id': user['language_id_id']}),
        'time_zone': django_query_instance.django_get_query(TimeZone, {'time_zone': user['time_zone_id']}),
        'currency_id': django_query_instance.django_get_query(Currency, {'currency_id': user['currency_id_id']})
    })


def delete_master_emp_data(user):
    if django_query_instance.django_existence_check(WorkflowACC,
                                                    {'app_username': user['username'],
                                                     'del_ind': False}):
        django_query_instance.django_filter_delete_query(WorkflowACC, {'app_username': user['username'],
                                                                       'client': global_variables.GLOBAL_CLIENT})
    if django_query_instance.django_existence_check(ApproverLimit,
                                                    {'approver_username': user['username'],
                                                     'del_ind': False}):
        django_query_instance.django_filter_delete_query(ApproverLimit, {'approver_username': user['username'],
                                                                         'client': global_variables.GLOBAL_CLIENT})
    if django_query_instance.django_existence_check(SpendLimitId,
                                                    {'spender_username': user['username'],
                                                     'del_ind': False}):
        django_query_instance.django_filter_delete_query(SpendLimitId, {'spender_username': user['username'],
                                                                        'client': global_variables.GLOBAL_CLIENT})


def delete_org_model_emp_data(user):
    if django_query_instance.django_existence_check(OrgAttributesLevel,
                                                    {'object_id': user['object_id_id'] and user[
                                                        'object_id_id'] is not NULL,
                                                     'del_ind': False}):
        django_query_instance.django_filter_delete_query(OrgAttributesLevel, {'object_id': user['object_id_id'],
                                                                              'client': global_variables.GLOBAL_CLIENT})
    if django_query_instance.django_existence_check(OrgModel,
                                                    {'object_id': user['object_id_id'] and user[
                                                        'object_id_id'] is not NULL,
                                                     'del_ind': False}):
        django_query_instance.django_filter_delete_query(OrgModel, {'object_id': user['object_id_id'],
                                                                    'client': global_variables.GLOBAL_CLIENT})


def delete_supplier(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    success_message = ''
    supp_data = JsonParser_obj.get_json_from_req(request)
    supp_info = django_query_instance.django_filter_query(SupplierMaster,
                                                          {'supplier_id__in': supp_data['data'],
                                                           'del_ind': False}, None, None)
    for supp in supp_info:
        if django_query_instance.django_existence_check(OrgSuppliers,
                                                        {'supplier_id__in': supp['data'],
                                                         'del_ind': False}):
            django_query_instance.django_update_query(ScItem,
                                                      {'supplier_id__in': supp['data'],
                                                       'client': global_variables.GLOBAL_CLIENT},
                                                      {'del_ind': True})
        if django_query_instance.django_existence_check(OrgSuppliers,
                                                        {'supplier_id__in': supp['data'],
                                                         'del_ind': False}) and \
                django_query_instance.django_existence_check(ScItem,
                                                             {'supplier_id__in': supp['data'],
                                                              'del_ind': False}):
            django_query_instance.django_update_query(OrgSuppliers,
                                                      {'supplier_id__in': supp['data'],
                                                       'client': global_variables.GLOBAL_CLIENT},
                                                      {'del_ind': True})

        if not django_query_instance.django_existence_check(OrgSuppliers,
                                                            {'supplier_id__in': supp['data'],
                                                             'del_ind': False}) and \
                django_query_instance.django_existence_check(ScItem,
                                                             {'supplier_id__in': supp['data'],
                                                              'del_ind': False}):
            django_query_instance.django_update_query(OrgSuppliers,
                                                      {'supplier_id__in': supp['data'],
                                                       'client': global_variables.GLOBAL_CLIENT},
                                                      {'del_ind': True})
        if django_query_instance.django_existence_check(SupplierMaster,
                                                        {'supplier_id__in': supp['data'],
                                                         'del_ind': False}) and \
                not django_query_instance.django_existence_check(OrgSuppliers,
                                                                 {'supplier_id__in': supp['data'],
                                                                  'del_ind': False}) and \
                not django_query_instance.django_existence_check(ScItem,
                                                                 {'supplier_id__in': supp['data'],
                                                                  'del_ind': False}):
            django_query_instance.django_filter_delete_query(SupplierMaster,
                                                             {'supplier_id__in': supp['data'],
                                                              'client': global_variables.GLOBAL_CLIENT})
        success_message = "Supplier deleted"

    employee_results = django_query_instance.django_filter_query(SupplierMaster, {
        'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
    }, None, None)

    response = {'employee_results': employee_results, 'success_message': success_message}
    return JsonResponse(response, safe=False)


def delete_org_announcement(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    success_message = ''
    annsmt_data = JsonParser_obj.get_json_from_req(request)
    # org_info = django_query_instance.django_filter_query(UserData,
    #                                                       {'email__in': user_data['data'],
    #                                                        'del_ind': False}, None, None)
    # print(annsmt_data)
    announcement_details = django_query_instance.django_get_query(OrgAnnouncements,
                                                                  {'unique_announcement_id': annsmt_data})
    if django_query_instance.django_existence_check(OrgAnnouncements,
                                                    {'unique_announcement_id__in': annsmt_data,
                                                     'del_ind': False}):
        django_query_instance.django_update_query(OrgAnnouncements,
                                                  {'unique_announcement_id__in': annsmt_data,
                                                   'client': global_variables.GLOBAL_CLIENT},
                                                  {'del_ind': True})
        success_message = "Org Announcement deleted"

    announcement_result1 = django_query_instance.django_filter_query(OrgAnnouncements, {
        'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
    }, None, None)
    t_count = len(announcement_result1)

    announcement_ids = [annsmt_data['unique_announcement_id'] for annsmt_data in announcement_result1]

    response = {'announcement_ids': announcement_ids, 'success_message': success_message, 't_count': t_count,
                'announcement_result1': announcement_result1}
    return JsonResponse(response, safe=False)


def lock_unlock_emp(request):
    """
    """
    emp_lock_flag_detail = JsonParser_obj.get_json_from_req(request)
    employee_id = emp_lock_flag_detail['employee_id']
    status = emp_lock_flag_detail['employee_id'].split('-')[1]
    empId = emp_lock_flag_detail['employee_id'].split('-')[0]
    if status in ('LOCKED', 'UNLOCKED'):
        django_query_instance.django_update_query(UserData,
                                                  {'client': global_variables.GLOBAL_CLIENT,
                                                   'employee_id': empId,
                                                   'del_ind': False},
                                                  {'user_locked': emp_lock_flag_detail['flag']})
    if status in ('PWDLOCKED', 'PWDUNLOCKED'):
        django_query_instance.django_update_query(UserData,
                                                  {'client': global_variables.GLOBAL_CLIENT,
                                                   'employee_id': empId,
                                                   'del_ind': False},
                                                  {'pwd_locked': emp_lock_flag_detail['flag']})
    response = {}
    return JsonResponse(response, safe=False)


def get_username(request):
    user_data = JsonParser_obj.get_json_from_req(request)
    if user_data:
        username = get_user_id_by_email_id(user_data)

    return JsonResponse(username, safe=False)


def extract_employee_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Employee_Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(
        ['EMAIL', 'USERNAME', 'PERSON_NO', 'FORM_OF_ADDRESS', 'FIRST_NAME', 'LAST_NAME', 'GENDER', 'PHONE_NUM',
         'PASSWORD',
         'DATE_JOINED', 'FIRST_LOGIN', 'LAST_LOGIN', 'IS_ACTIVE', 'IS_SUPERUSER', 'IS_STAFF', 'DATE_FORMAT',
         'EMPLOYEE_ID', 'DECIMAL_NOTATION', 'USER_TYPE', 'LOGIN_ATTEMPTS', 'USER_LOCKED', 'PWD_LOCKED', 'SSO_USER',
         'VALID_FROM', 'VALID_TO', 'del_ind', 'CURRENCY', 'LANGUAGE_ID', 'OBJECT_ID', 'TIME_ZONE'])

    return response


def extract_supplier_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Supplier_Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(
        ['SUPPLIER_ID', 'SUPP_TYPE', 'NAME1', 'NAME2', 'SUPPLIER_USERNAME', 'CITY', 'POSTAL_CODE', 'STREET',
         'LANDLINE', 'MOBILE_NUM', 'FAX', 'EMAIL', 'EMAIL1', 'EMAIL2', 'EMAIL3',
         'EMAIL4', 'EMAIL5', 'OUTPUT_MEDIUM', 'SEARCH_TERM1', 'SEARCH_TERM2', 'DUNS_NUMBER', 'BLOCK DATE',
         'BLOCK', 'DELIVERY_DAYS', 'IS_ACTIVE', 'REGISTRATION_NUMBER', 'COMPANY_ID', 'SUPPLIER_MASTER_SOURCE_SYSTEM',
         'PREF_ROUTING', 'LOCK_DATE', 'GLOBAL_DUNS', 'DOMESTIC_DUNS', 'ICS_CODE', 'INTERNAL_IND', 'SBA_CODE',
         'ETHNICITY',
         'HUBZONE', 'NO_VEND_TEXT', 'AGR_REG_NO', 'NO_MULT_ADDR', 'del_ind', 'COUNTRY_CODE', 'CURRENCY_ID',
         'LANGUAGE_ID'])

    return response


def application_monitoring(request):
    """

    """
    update_user_info(request)
    report_search = False
    sc_header_list = []
    if request.method == 'POST' and request.is_ajax():
        print('submit')
        doc_num_list = request.POST.getlist('doc_num[]')
        status = request.POST.getlist('status')
        error_type = request.POST.getlist('error_type')

        sc_header_details = django_query_instance.django_filter_query(ScHeader,
                                                                      {'doc_number__in': doc_num_list,
                                                                       'client': global_variables.GLOBAL_CLIENT,
                                                                       'del_ind': False},
                                                                      None,
                                                                      None)
        result = check_po(sc_header_details)
        sc_header_list = django_query_instance.django_filter_query(ScHeader,
                                                                   {'client': global_variables.GLOBAL_CLIENT,
                                                                    'transmission_error_type': error_type[0],
                                                                    'transmission_error': True}, None, None)
        for sc_header in sc_header_list:
            sc_header['encrypted_header_guid'] = encrypt(sc_header['guid'])
        return JsonResponse({'sc_header_list': sc_header_list,
                             'result': result})
    elif request.method == 'POST':
        search_fields = {}
        print("post")
        application_monitoring_form = ApplicationMonitoringForm(request.POST)
        if application_monitoring_form.is_valid():
            inp_comp_code = request.POST.get('company_code')
            inp_doc_type = request.POST.get('doc_type')
            inp_doc_num = request.POST.get('doc_num')
            inp_from_date = request.POST.get('from_date')
            inp_to_date = request.POST.get('to_date')
            inp_supl = request.POST.get('supplier')
            inp_created_by = request.POST.get('created_by')
            inp_requester = request.POST.get('requester')
            error_type = request.POST.get('doc_types')
            # results
            sc_header_list = get_hdr_data_app_monitoring(
                inp_doc_type,
                inp_doc_num,
                inp_from_date,
                inp_to_date,
                inp_supl,
                inp_created_by,
                inp_requester, report_search, error_type, inp_comp_code)

            search_fields['doc_type'] = inp_doc_type
            search_fields['doc_num'] = inp_doc_num
            search_fields['created_by'] = inp_created_by
            search_fields['requester'] = inp_requester

            # sc_header_list = application_monitoring_docnum_search(**search_fields)

            # company_details = OrgCompanies.objects.filter(client=client, del_ind=False, company_guid=inp_comp_code)
            # for comp in company_details:
            #     result = result.filter(co_code=comp.company_id)
        # sc_header_list = django_query_instance.django_filter_query(ScHeader,
        #                                                            {'client': global_variables.GLOBAL_CLIENT,
        #                                                             'transmission_error': True}, None, None)
    else:
        application_monitoring_form = ApplicationMonitoringForm()
        sc_header_list = django_query_instance.django_filter_query(ScHeader,
                                                                   {'client': global_variables.GLOBAL_CLIENT,
                                                                    'transmission_error_type': CONST_ERROR_SPLIT_CRITERIA,
                                                                    'transmission_error': True}, None, None)

    for sc_header in sc_header_list:
        sc_header['encrypted_header_guid'] = encrypt(sc_header['guid'])

    inp_doc_type = 'SC'
    context = {
        'application_monitoring_form': application_monitoring_form,
        'sc_header_list': sc_header_list,
        'inp_doc_type': inp_doc_type,
        'is_slide_menu': True,
        'is_admin_active': True,
        'inc_nav': True,
        'inc_footer': True,
        'sc_completion_flag': False
    }
    return render(request, 'ApplicationMonitoring/application_monitoring.html', context)


def email_user_monitoring(request):
    """

    """
    global t_count, email_list, inp_email_type, inp_email_status, num
    update_user_info(request)
    email_user_monitoring_form = EmailUserMonitoringForm()
    final_data = {}
    final_data_list = []
    final_data1 = []
    email_list = ''
    inp_email_type = ''
    inp_email_status = 0
    error_messages = ''
    search_type = 'Internal'

    if request.method == 'GET':
        inp_email_type = 'REGISTRATION'
        inp_email_status = 2
        inp_email_type_ext = 'PO_SUPPLIER'
        # minimum_search_date = datetime.combine(datetime.today(), datetime.time.min)
        # maximum_search_date = datetime.combine(datetime.today(), datetime.time.max)
        email_list = django_query_instance.django_filter_query(EmailUserMonitoring,
                                                               {'client': global_variables.GLOBAL_CLIENT,
                                                                'object_type': inp_email_type,
                                                                'email_status': inp_email_status,
                                                                'email_user_monitoring_created_at__date': datetime.today(),
                                                                'del_ind': False}, None, None)
        email_list_supp = django_query_instance.django_filter_query(EmailSupplierMonitoring,
                                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                                     'object_type': inp_email_type_ext,
                                                                     'email_status': inp_email_status,
                                                                     'email_supplier_monitoring_created_at__date': datetime.today(),
                                                                     'del_ind': False}, None, None)
        for supp_data in email_list_supp:
            final_data['object_type'] = supp_data['object_type']
            final_data['doc_number'] = supp_data['doc_number']
            final_data['receiver_email'] = supp_data['receiver_email']
            dt = str(supp_data['email_supplier_monitoring_created_at'])
            final_data['email_supplier_monitoring_created_at'] = str(datetime.strptime(dt, '%Y-%m-%d %H:%M:%S.%f'))
            final_data['email_status'] = supp_data['email_status']
            final_data['error_type'] = supp_data['error_type']
            final_data['email_user_monitoring_guid'] = supp_data['email_supplier_monitoring_guid']
            final_data_list.append(final_data)
        # email_list = final_data_list
        inp_email_type_ext = inp_email_type

        t_count = len(email_list)
        context = {
            'email_user_monitoring_form': email_user_monitoring_form,
            'email_data': email_list,
            'email_list_supp': final_data_list,
            'inp_email_type': inp_email_type,
            'inp_email_type_ext': inp_email_type_ext,
            'inp_email_status': int(inp_email_status),
            't_count': t_count,
            'is_slide_menu': True,
            'is_admin_active': True,
            'inc_nav': True,
            'inc_footer': True,
            'sc_completion_flag': False
        }
        return render(request, 'ApplicationMonitoring/Email_user_monitoring.html', context)
    num = 0
    if request.method == 'POST' or request.is_ajax():
        email_user_monitoring_form = EmailUserMonitoringForm(request.POST)
        t_count = 0
        inp_email_type = request.POST.get('email_types')
        inp_email_type_ext = request.POST.get('email_types_ext')
        inp_type = request.POST.get('type')
        inp_email_status = request.POST.get('email_status')
        inp_from_date = request.POST.get('from_date')
        inp_to_date = request.POST.get('to_date')
        num = int(inp_email_status)
        from_date = datetime.combine(datetime.strptime(inp_from_date, '%Y-%m-%d'), datetime.min.time())
        to_date = datetime.combine(datetime.strptime(inp_to_date, '%Y-%m-%d'), datetime.max.time())
        if inp_type == 'Internal':
            search_type = inp_email_type
        elif inp_type == 'External':
            search_type = inp_email_type_ext

        if search_type in ['REGISTRATION', 'APPROVED_SC', 'PASSWORD_LOCK', 'ACCT_DEACTIVATED', 'RESET_PASSWORD',
                           'SC_REJECTED']:
            email_list = list(EmailUserMonitoring.objects.filter(
                client=global_variables.GLOBAL_CLIENT,
                object_type=search_type, email_status=num,
                del_ind=False,
                email_user_monitoring_created_at__gte=from_date,
                email_user_monitoring_created_at__lte=to_date
            ).values())
        elif search_type == 'SC_APPROVAL':
            # check_resend()
            email_list = list(EmailDocumentMonitoring.objects.filter(
                client=global_variables.GLOBAL_CLIENT,
                object_type=search_type, email_status=num,
                del_ind=False,
                email_document_monitoring_created_at__gte=from_date,
                email_document_monitoring_created_at__lte=to_date,
            ).values())
        elif search_type == 'PO_SUPPLIER':
            email_list = list(EmailSupplierMonitoring.objects.filter(
                client=global_variables.GLOBAL_CLIENT,
                object_type=search_type, email_status=num,
                del_ind=False,
                email_supplier_monitoring_created_at__gte=from_date,
                email_supplier_monitoring_created_at__lte=to_date
            ).values())
        final_data1.append(email_list)
        email_list_supp = django_query_instance.django_filter_query(EmailSupplierMonitoring,
                                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                                     'object_type': 'PO_SUPPLIER',
                                                                     'email_status': 2,
                                                                     'email_supplier_monitoring_created_at__date': datetime.today(),
                                                                     'del_ind': False}, None, None)
        email_list_default = list(EmailUserMonitoring.objects.filter(
            client=global_variables.GLOBAL_CLIENT,
            object_type=search_type, email_status=num,
            del_ind=False,
            email_user_monitoring_created_at__gte=from_date,
            email_user_monitoring_created_at__lte=to_date
        ).values())
        t_count = len(email_list)

        context = {
            'email_user_monitoring_form': email_user_monitoring_form,
            'email_data': email_list,
            'email_list_supp': email_list_supp,
            'email_list_default': email_list_default,
            'inp_email_type': inp_email_type,
            'inp_email_type_ext': inp_email_type_ext,
            'inp_email_status': int(inp_email_status),
            'search_type': search_type,
            't_count': t_count,
            'status': num,
            'is_slide_menu': True,
            'is_admin_active': True,
            'inc_nav': True,
            'inc_footer': True,
            'error_messages': error_messages
        }
        return render(request, 'ApplicationMonitoring/Email_user_monitoring.html', context)


def check_resend(request):
    update_user_info(request)
    getClients(request)
    sc_guid = ''
    approved_docs = []
    context = {}
    approved_flag = 0
    doc_num_list = JsonParser_obj.get_json_from_req(request)
    if request.is_ajax():
        # doc_num_list = request.POST.getlist('doc_num[]')
        guid_list = []
        sc_header_details = django_query_instance.django_filter_query(ScHeader,
                                                                      {'doc_number__in': doc_num_list,
                                                                       'client': global_variables.GLOBAL_CLIENT,
                                                                       'del_ind': False},
                                                                      None,
                                                                      None)
        for sc_data in sc_header_details:
            guid_list.append(sc_data['guid'])
        approval_data = django_query_instance.django_filter_query(ScApproval,
                                                                  {
                                                                      'header_guid__in': guid_list,
                                                                      'client': global_variables.GLOBAL_CLIENT,
                                                                  }, None, None)
        for data in approval_data:
            if data['proc_lvl_sts'] == 'COMPLETED' and data['app_sts'] == 'APPROVER_APPROVED':
                sc_guid = data['header_guid_id']
                approved_docs = django_query_instance.django_filter_value_list_query(ScHeader,
                                                                                     {
                                                                                         'guid': sc_guid,
                                                                                         'client': global_variables.GLOBAL_CLIENT,
                                                                                     },
                                                                                     'doc_number')
                approved_flag = 1
    print(approved_docs)
    email_data = list(EmailDocumentMonitoring.objects.filter(
        client=global_variables.GLOBAL_CLIENT,
        object_type='SC_APPROVAL', email_status=2,
        del_ind=False,
        doc_number__in=doc_num_list
    ).values())
    context = {
        'is_slide_menu': True,
        'is_admin_active': True,
        'inc_nav': True,
        'inc_footer': True,
        'email_data': email_data,
        'approved_flag': approved_flag
    }
    print(email_data)
    return JsonParser_obj.get_json_from_obj(context)
    # return render(request, 'ApplicationMonitoring/Email_user_monitoring.html', context)


def clear_filter_data(req):
    update_user_info(req)
    table_data = JsonParser_obj.get_json_from_req(req)
    if table_data['table_name'] == 'employee':
        data = get_emp_data()
        return JsonResponse(data, safe=False)
    if table_data['table_name'] == 'supplier':
        supplier_results = get_supplier_data()
        response = {'supplier_results': supplier_results}
        return JsonResponse(response, safe=False)
