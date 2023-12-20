"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    shopping_cart_specific.py
Usage:
     Functions specific to shopping cart are defined here
     get_supp_names        : To display list of suppliers configured free text form
     check_for_limit       : Function to check if limit item already exists in cart
     check_for_free_text   : Function to check if free_text item already exists in cart
     check_for_requisition : Function to check if requisition item already exists in cart
     check_for_catalog     : Function to check if catalog item already exists in cart
     check_for_eform       : Function to check if eform fields are configured for suppliers for free text form
     Classes:
        SaveShoppingCart   : This class is used to save the shopping cart details into their respective DB tables
                             This class has 5 methods
                             1) save_header_details     : This method is used to save header details of the cart
                             2) save_item_details       : This method is used to save item details of the cart
                             3) save_accounting_details : This method is used to save accounting details at item level
                             4) save_address            : This method is used to save address at item level
                             5) link_eform              : This method is used to link eform in case of free-text item
                                                          if free text form configured for extra fields
                             6) save_address            : This method is used to save addresses at item level
                             7) generate_document_number: This method is used to generate doc number for sc
                             8) get_purchasing_data     : This method is used to get purchasing data based on product category
                             9) save_notes_data         : This method is used to save notes like approval note, internal note, supplier note.
                             10) save_attachments       : This method is used to store attachments at item level
    get_manger_detail - get manger detail based on total value of the Cart Item
"""
from eProc_Attributes.models.org_attribute_models import OrgAttributesLevel
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG172, MSG173, MSG174, MSG175, MSG176, MSG188
from eProc_Configuration.models.application_data import WorkflowSchema, FreeTextForm
from eProc_Configuration.models.development_data import AuthorizationObject, AccountAssignmentCategory, Authorization, \
    AuthorizationGroup
from eProc_Configuration.models.master_data import WorkflowACC
from eProc_Configuration.models import *
from django.core.exceptions import ObjectDoesNotExist
from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.get_db_query import getClients, getUsername, get_login_user_roles_by_obj_id
from eProc_Shopping_Cart.Utilities.prod_cat import get_prod_cat1
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import *
from eProc_Shopping_Cart.models import CartItemDetails, ScHeader, ScItem, ScPotentialApproval, ScApproval, ScAccounting
from eProc_Registration.models import *
from eProc_Exchange_Rates.Utilities.exchange_rates_specific import get_currency_by_max_spending_value
from eProc_Exchange_Rates.Utilities.exchange_rates_generic import convert_currency
from eProc_System_Settings.Utilities.system_settings_generic import sys_attributes
from eProc_Workflow.Utilities.work_flow_generic import save_sc_approval
import datetime

django_query_instance = DjangoQueries()


#  Function to Display configured freetext form in select supplier page
def get_supp_names(request):
    """
    :param request:
    :return:
    """
    client = getClients(request)
    suppliers = django_query_instance.django_filter_only_query(FreeTextForm, {'client': client}).values('supp_id')
    supplier_id = []
    name1 = []
    name2 = []
    s_id = []
    for supp in suppliers:
        supp_id = supp['supp_id']
        supplier_id.append(supp_id)
        supplier_info = django_query_instance.django_filter_only_query(SupplierMaster, {
            'client': client, 'supplier_id': supp_id, 'del_ind': False
        }).values('supplier_id', 'name1', 'name2')

        for supp_det in supplier_info:
            supplier_name1 = supp_det['name1']
            supplier_name2 = supp_det['name2']
            supp = supp_det['supplier_id']
            name1.append(supplier_name1)
            name2.append(supplier_name2)
            s_id.append(supp)

    return zip(name1, name2, s_id)


# Function to check if eform fields are configured for suppliers for free text
def check_for_eform(request):
    """
    :param request:
    :return:
    """
    username = getUsername(request)
    supplier = []
    client = getClients(request)
    cart_items = django_query_instance.django_filter_only_query(CartItemDetails, {
        'username': username, 'client': client, 'call_off': CONST_FREETEXT_CALLOFF
    })
    for items in cart_items:
        try:
            supplier_id = django_query_instance.django_get_query(FreeTextForm, {
                'supp_id': items.supplier_id, 'prod_cat_id': items.prod_cat_id, 'client': client
            })
            if not supplier_id:
                return supplier
            if supplier_id.form_field1 == '' and supplier_id.form_field2 == '' and supplier_id.form_field3 == '' and supplier_id.form_field4 == '' and supplier_id.form_field5 == '' and supplier_id.form_field6 == '' and supplier_id.form_field7 == '' and supplier_id.form_field8 == '' and supplier_id.form_field9 == '' and supplier_id.form_field10 == '':
                supplier.append(supplier_id.supp_id)
        except ObjectDoesNotExist:
            return supplier
    return supplier


class AuthorizationLevel:

    def __init__(self, client, login_user_obj_id):
        self.client = client
        self.login_user_obj_id = login_user_obj_id

    def get_main_menu(self, auth_level):
        """
        Enable main based on user role
        :param auth_level:
        :return:
        """
        slide_menu = dict.fromkeys([CONST_WORK_OVERVIEW, CONST_USER_SETTINGS, CONST_APPL_SETTINGS, CONST_SHOPPING,
                                    CONST_SHOPPING_PLUS, CONST_GOODS_RECEIPTS, CONST_APPROVALS, CONST_PURCHASING,
                                    CONST_ADMIN_TOOL, CONST_SYSTEM_SETTINGS, CONST_CONTENT_MANAGEMENT,
                                    CONST_TIME_SHEET, CONST_SOM, CONST_SHOPPER_ASSIST, CONST_SC_SOURCING], False)

        auth_feature = self.get_auth_level_id(auth_level)
        for auth_feature_value in auth_feature:
            slide_menu[auth_feature_value] = True
        return slide_menu

    def get_sub_menu(self, auth_level):
        sub_menu = dict.fromkeys(
            [CONST_HOME, CONST_LIMIT_ORDER, CONST_FREE_TEXT, CONST_REQUISITION, CONST_CATALOG, CONST_MY_ORDER,
             CONST_EMAIL_NOTIF, CONST_REPORTS, CONST_USER_ADMIN, CONST_SUBSTITUTION, CONST_SUPPLIER_MANAGEMENT,
             CONST_EMPLOYEE_MANAGEMENT, CONST_SC_COMPLETION,
             CONST_GROUP_CATEGORY, CONST_CHANGE_PO, CONST_PERSONAL_SETTINGS, CONST_PURCHASE_SETTINGS,
             CONST_FORM_BUILDER, CONST_ORG_MODEL, CONST_CONFIRMATION, CONST_CANCELLATION, CONST_RETURN_DELIVERY,
             CONST_WORK_FLOW_ITEMS, CONST_PRODUCT_AND_SERVICE_CONFIG, CONST_CATALOG_CONFIG, CONST_BASIC_SETTINGS,
             CONST_CONFIG_HOME, CONST_APPLICATION_MONITOR, CONST_PROJECTS, CONST_EFFORTS, CONST_SUB_SOM,
             CONST_SC_GROUPING, CONST_RFQ,CONST_SEND_MESSAGE],
            False)
        auth_feature = self.get_auth_level_id(auth_level)
        for auth_feature_value in auth_feature:
            sub_menu[auth_feature_value] = True
        return sub_menu

    def get_auth_level_id(self, auth_level):
        """
        get authorization level id
        :param auth_level:
        :return:
        """
        global_variables.GLOBAL_PURCHASER_FLAG = False
        user_role = get_login_user_roles_by_obj_id(self.login_user_obj_id)
        if CONST_SHOP_PURCHASER in user_role:
            global_variables.GLOBAL_PURCHASER_FLAG = True

        auth_grp = django_query_instance.django_filter_value_list_query(Authorization, {
            'role__in': user_role, 'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
        }, 'auth_obj_grp')

        auth_obj_id = django_query_instance.django_filter_value_list_query(AuthorizationGroup, {
            'auth_obj_grp__in': auth_grp, 'auth_level': auth_level, 'del_ind': False
        }, 'auth_obj_id')

        auth_feature = django_query_instance.django_filter_value_list_query(AuthorizationObject, {
            'auth_obj_id__in': auth_obj_id, 'auth_level': auth_level, 'del_ind': False
        }, 'auth_level_ID')

        return auth_feature


# To display product category in update forms
def get_prod_cat_dropdown(request):
    """
    :param request:
    :return:
    """
    product_category = get_prod_cat1(request, prod_det=None)
    prod_cat = []
    for prod_id, prod_desc in product_category:
        prod_cat.append(prod_id + ' - ' + prod_desc)
    return prod_cat


# To get limit item form instance
def get_limit_update_content(item_details):
    """
    :param item_details:
    :return:
    """
    item_name = item_details.description
    prod_cat = item_details.prod_cat
    currency = item_details.currency
    overall_limit = item_details.overall_limit
    expected_value = item_details.expected_value
    start_date = item_details.start_date
    end_date = item_details.end_date
    item_del_date = item_details.item_del_date

    if item_del_date is not None:
        required = 'On'
    elif end_date is None and item_del_date is None:
        required = 'From'
    else:
        required = 'Between'

    supp_id = item_details.supplier_id
    ir_gr_flag = item_details.ir_gr_ind_limi
    if ir_gr_flag:
        follow_up_action = CONST_IC
    else:
        follow_up_action = CONST_IO
    limit_context = {
        'item_name': item_name,
        'prod_cat': prod_cat,
        'currency': currency,
        'overall_limit': overall_limit,
        'expected_value': expected_value,
        'start_date': start_date,
        'end_date': end_date,
        'supp_id': supp_id,
        'item_del_date': item_del_date,
        'required': required,
        'follow_up_action': follow_up_action
    }
    return limit_context


# Function to get free text form fields and field values from guid
def get_free_text_content(guid):
    """
    :param guid:
    :return:
    """
    eform_data = {}
    if django_query_instance.django_existence_check(EformFieldData, {
        'cart_guid': guid}) or django_query_instance.django_existence_check(EformFieldData, {'item_guid': guid}):

        if django_query_instance.django_existence_check(EformFieldData, {'cart_guid': guid}):
            get_eform_fields = django_query_instance.django_get_query(EformFieldData, {'cart_guid': guid})
        else:
            get_eform_fields = django_query_instance.django_get_query(EformFieldData, {'item_guid': guid})

        form_id = get_eform_fields.form_id
        get_fields = django_query_instance.django_get_query(FreeTextForm, {'form_id': form_id})
        eform_data = {
            'item_guid': guid,
            'form_field1': get_fields.form_field1,
            'form_field2': get_fields.form_field2,
            'form_field3': get_fields.form_field3,
            'form_field4': get_fields.form_field4,
            'form_field5': get_fields.form_field5,
            'form_field6': get_fields.form_field6,
            'form_field7': get_fields.form_field7,
            'form_field8': get_fields.form_field8,
            'form_field9': get_fields.form_field9,
            'form_field10': get_fields.form_field10,
            'form_field1_value': get_eform_fields.form_field1,
            'form_field2_value': get_eform_fields.form_field2,
            'form_field3_value': get_eform_fields.form_field3,
            'form_field4_value': get_eform_fields.form_field4,
            'form_field5_value': get_eform_fields.form_field5,
            'form_field6_value': get_eform_fields.form_field6,
            'form_field7_value': get_eform_fields.form_field7,
            'form_field8_value': get_eform_fields.form_field8,
            'form_field9_value': get_eform_fields.form_field9,
            'form_field10_value': get_eform_fields.form_field10,
            'check_box1': get_fields.check_box1,
            'check_box2': get_fields.check_box2,
            'check_box3': get_fields.check_box3,
            'check_box4': get_fields.check_box4,
            'check_box5': get_fields.check_box5,
            'check_box6': get_fields.check_box6,
            'check_box7': get_fields.check_box7,
            'check_box8': get_fields.check_box8,
            'check_box9': get_fields.check_box9,
            'check_box10': get_fields.check_box10,
        }

    return eform_data


def convert_to_boolean(string):
    if string == 'true':
        return True
    else:
        return False


def get_gl_account_default_value(client, total_value, cc, account_assign_cat):
    """
    :param client:
    :param total_value:
    :param cc:
    :param account_assign_cat:a
    :return:
    """
    available_gl_account = []
    django_query_instance.django_filter_only_query(DetermineGLAccount, {
        'client': client, 'prod_cat_id': 'ALL',
        'account_assign_cat': django_query_instance.django_get_query(AccountAssignmentCategory,
                                                                     {'account_assign_cat': account_assign_cat}),
        'company_id': cc, 'del_ind': False
    })

    gl_account_number = django_query_instance.django_filter_only_query(DetermineGLAccount, {
        'client': client, 'prod_cat_id': 'ALL', 'company_id': cc, 'del_ind': False,
        'account_assign_cat': django_query_instance.django_get_query(AccountAssignmentCategory,
                                                                     {'account_assign_cat': account_assign_cat}),
    })

    for gl_numbers in gl_account_number:
        if int(gl_numbers.from_value) <= float(total_value) <= int(gl_numbers.to_value):
            # available_gl_account.append(gl_numbers.gl_account)
            gl_account_number_data = gl_numbers.gl_account

            get_gl_account_description = django_query_instance.django_filter_value_list_query(AccountingDataDesc, {
                'client': client, 'company_id': cc,
                'account_assign_value': gl_account_number_data,
                'account_assign_cat': 'GLACC'
            }, 'description')[0]

            available_gl_account.append(
                {'gl_account_number': gl_account_number_data, 'gl_account_description': get_gl_account_description})

    default_gl_acc_num = django_query_instance.django_filter_only_query(DetermineGLAccount, {
        'client': client, 'prod_cat_id': 'ALL',
        'account_assign_cat': django_query_instance.django_get_query(AccountAssignmentCategory,
                                                                     {'account_assign_cat': account_assign_cat}),
        'gl_acc_default': True, 'company_id': cc, 'del_ind': False
    })

    default_gl_value = ''
    get_default_gl_account_description = ''
    for data in default_gl_acc_num:
        if int(data.from_value) <= float(total_value) <= int(data.to_value):
            default_gl_value = data.gl_account
            get_default_gl_account_description = \
                django_query_instance.django_filter_value_list_query(AccountingDataDesc, {
                    'client': client, 'company_id': cc,
                    'account_assign_value': default_gl_value,
                    'account_assign_cat': 'GLACC'
                }, 'description')[0]

    return {'default_gl_account_number': default_gl_value,
            'default_gl_account_description': get_default_gl_account_description}, available_gl_account


def get_login_user_spend_limit(company_code, client, login_username):
    """
    get login user spending limit
    :param company_code:
    :param client:
    :param login_username:
    :return:
    """
    max_sl_value = 0

    sl_code_id = django_query_instance.django_filter_value_list_query(SpendLimitId, {
        'company_id': company_code, 'spender_username': login_username, 'client': client, 'del_ind': False
    }, 'spend_code_id')

    if sl_code_id:
        sl_value = django_query_instance.django_filter_value_list_query(SpendLimitValue, {
            'company_id': company_code, 'spend_code_id__in': sl_code_id, 'client': client, 'del_ind': False
        }, 'upper_limit_value')
        if sl_value:
            max_sl_value = max(sl_value)

    return max_sl_value, sl_code_id


def get_appr_limit(default_cmp_code, app_user, client, schema_step_type, app_limit_value, manger_list):
    msg_info = ''
    currency = ''

    app_code_id = django_query_instance.django_filter_value_list_query(ApproverLimit, {
        'company_id': default_cmp_code, 'approver_username': app_user, 'del_ind': False, 'client': client
    }, 'app_code_id')

    if app_code_id:
        app_val = django_query_instance.django_filter_value_list_query(ApproverLimitValue, {
            'company_id': default_cmp_code, 'app_code_id__in': app_code_id, 'del_ind': False,
            'app_types': schema_step_type, 'client': client
        }, 'upper_limit_value')

        if app_val:
            app_val = max(app_val)

            approval_currency = django_query_instance.django_filter_value_list_query(ApproverLimitValue, {
                'company_id': default_cmp_code, 'app_code_id__in': app_code_id,
                'del_ind': False, 'app_types': schema_step_type, 'client': client
            }, 'currency_id')

            currency = approval_currency[0]
            app_limit_value.append(int(app_val))
        else:
            manger_list = []
            msgid = 'MSG172'
            error_msg = get_message_desc(msgid)[1]

            msg_info = error_msg
            return manger_list, msg_info, app_limit_value, currency
    else:
        manger_list = []
        msgid = 'MSG172'
        error_msg = get_message_desc(msgid)[1]

        msg_info = error_msg
        return manger_list, msg_info, app_limit_value, currency

    return manger_list, msg_info, app_limit_value, currency


def get_manger_detail_old(client, login_username, acc_default, total_value, default_cmp_code, acc_value, user_currency):
    """
    get manger detail based on total value of the Cart Item
    :param user_currency:
    :param client:login user client id
    :param login_username: login user id
    :param acc_default:Account assignment category [cc,wbs,as,or]
    :param total_value:cart item total value
    :param default_cmp_code:default company code assigned to the login user
    :param acc_value: Account assignment category value[5000,5001 etc]
    :return:
    """
    const_total_value = float(total_value)
    manger_list = []
    app_limit_value = []
    msg_info = ""
    workflow_schema = django_query_instance.django_filter_value_list_query(WorkflowSchema, {'client': client,
                                                                                            'company_id': default_cmp_code},
                                                                           'app_types')

    if workflow_schema:

        login_user_spend_limit, sl_code_id = get_login_user_spend_limit(default_cmp_code, client, login_username)

        if login_user_spend_limit:
            spender_currency = get_currency_by_max_spending_value(default_cmp_code, client, sl_code_id)
            total_value = convert_currency(total_value, str(global_variables.GLOBAL_USER_CURRENCY),
                                           str(spender_currency))
            if float(total_value) <= float(login_user_spend_limit):
                manger_list.append(CONST_AUTO)
                return manger_list, msg_info
            else:
                for schema_step_type in workflow_schema:
                    app_limit = list(django_query_instance.django_filter_only_query(WorkflowACC, {
                        'company_id': default_cmp_code, 'account_assign_cat': acc_default,
                        'acc_value': acc_value, 'client': client
                    }).values_list('app_username', 'sup_acc_value', 'sup_company_id'))

                    if app_limit:
                        for app_user, sup_acc_val, sup_company_id in app_limit:
                            if not sup_acc_val:
                                manger_list = []
                                msgid = 'MSG172'
                                error_msg = get_message_desc(msgid)[1]

                                msg_info = error_msg
                                return manger_list, msg_info
                            manger_list.append(app_user)
                            manger_list, msg_info, app_limit_value, currency = get_appr_limit(default_cmp_code,
                                                                                              app_user,
                                                                                              client,
                                                                                              schema_step_type,
                                                                                              app_limit_value,
                                                                                              manger_list)
                            if msg_info:
                                return manger_list, msg_info
                            acc_value = sup_acc_val
                            default_cmp_code = sup_company_id
                            total_value = convert_currency(const_total_value, str(user_currency), currency)
                        if float(total_value) <= max(app_limit_value):
                            return manger_list, msg_info
                        else:
                            while float(total_value) > max(app_limit_value):
                                app_limit = list(django_query_instance.django_filter_only_query(WorkflowACC, {
                                    'company_id': default_cmp_code, 'account_assign_cat': acc_default,
                                    'acc_value': acc_value, 'client': client
                                }).values_list('app_username', 'sup_acc_value', 'sup_company_id'))

                                if not app_limit:
                                    manger_list = []
                                    msgid = 'MSG172'
                                    error_msg = get_message_desc(msgid)[1]

                                    msg_info = error_msg
                                    return manger_list, msg_info
                                else:
                                    for app_user, sup_acc_val, sup_company_id in app_limit:
                                        if not django_query_instance.django_existence_check(UserData, {
                                            'client': client, 'username': app_user
                                        }):
                                            msgid = 'MSG176'
                                            error_msg = get_message_desc(msgid)[1]

                                            msg_info = error_msg
                                            return None, msg_info
                                        manger_list.append(app_user)

                                        manger_list, msg_info, app_limit_value, currency = get_appr_limit(
                                            default_cmp_code,
                                            app_user,
                                            client,
                                            schema_step_type,
                                            app_limit_value,
                                            manger_list)
                                        if msg_info:
                                            return manger_list, msg_info
                                        acc_value = sup_acc_val
                                        default_cmp_code = sup_company_id
                    else:
                        msgid = 'MSG173'
                        error_msg = get_message_desc(msgid)[1]

                        msg_info = error_msg
        else:
            msgid = 'MSG174'
            error_msg = get_message_desc(msgid)[1]

            msg_info = error_msg
    else:
        msgid = 'MSG175'
        error_msg = get_message_desc(msgid)[1]

        msg_info = error_msg

    return manger_list, msg_info


def get_manger_detail(client, login_username, acc_default, total_value, default_cmp_code, acc_value,
                      user_currency):
    """
    get manger detail based on total value of the Cart Item
    :param user_currency:
    :param client:login user client id
    :param login_username: login user id
    :param acc_default:Account assignment category [cc,wbs,as,or]
    :param total_value:cart item total value
    :param default_cmp_code:default company code assigned to the login user
    :param acc_value: Account assignment category value[5000,5001 etc]
    :return:
    """
    const_total_value = float(total_value)
    manger_list = []
    app_limit_value = []
    msg_info = ""
    workflow_schema = django_query_instance.django_filter_value_list_query(WorkflowSchema, {'client': client,
                                                                                            'company_id': default_cmp_code,
                                                                                            'del_ind': False},
                                                                           'app_types')
    acc_detail_list = []

    if workflow_schema:

        login_user_spend_limit, sl_code_id = get_login_user_spend_limit(default_cmp_code, client, login_username)

        if login_user_spend_limit:
            spender_currency = get_currency_by_max_spending_value(default_cmp_code, client, sl_code_id)
            total_value = convert_currency(total_value, str(global_variables.GLOBAL_USER_CURRENCY),
                                           str(spender_currency))
            if float(total_value) <= float(login_user_spend_limit):
                manger_list.append({'app_id_value': CONST_AUTO, 'app_id_detail': CONST_AUTO})
                return manger_list, msg_info
            else:
                for count, schema_step_type in enumerate(workflow_schema):
                    if schema_step_type == 'FIN':
                        app_limit = list(django_query_instance.django_filter_only_query(WorkflowACC, {
                            'company_id': default_cmp_code, 'account_assign_cat': acc_default,
                            'acc_value': acc_value, 'client': client, 'del_ind': False
                        }).values_list('app_username', 'sup_acc_value', 'sup_company_id', 'currency_id',
                                       'sup_account_assign_cat', 'company_id', 'account_assign_cat', 'acc_value'))
                        count = 1
                        if app_limit:
                            for app_user, sup_acc_val, sup_company_id, currency_id, sup_account_assign_cat, company_id, account_assign_cat, acc_value in app_limit:
                                app_username = []
                                if not sup_acc_val:
                                    manger_list = []
                                    msgid = 'MSG172'
                                    error_msg = get_message_desc(msgid)[1]

                                    msg_info = error_msg
                                    return manger_list, msg_info
                            msg_info, approver_detail, app_limit_value = get_approvers_id_and_limit_value(app_limit,
                                                                                                          company_id,
                                                                                                          user_currency,
                                                                                                          client,
                                                                                                          schema_step_type)

                            # manger_list.append(app_user)
                            # manger_list, msg_info, app_limit_value, currency = get_appr_limit(default_cmp_code,
                            #                                                                   app_user,
                            #                                                                   client,
                            #                                                                   schema_step_type,
                            #                                                                   app_limit_value,
                            #                                                                   manger_list)

                            if msg_info:
                                return manger_list, msg_info
                            approver_detail = list(approver_detail)
                            app_id = []
                            for app_datails in approver_detail:
                                app_id.append(app_datails[0])
                                acc_detail_list.append({'acc_value': acc_value, 'account_assign_cat': acc_default,
                                                        'company_id': default_cmp_code
                                                        })
                                if ((app_datails[7] == app_datails[1]) and (app_datails[2] == app_datails[5]) and (
                                        app_datails[4] == app_datails[6])):
                                    msgid = 'MSG173'
                                    error_msg = get_message_desc(msgid)[1]
                                    msg_info = error_msg
                                    return manger_list, msg_info

                            if len(app_id) > 1:
                                app_id_value = CONST_MULTIPLE
                                app_id_detail = ",".join(app_id)
                            else:
                                app_id_value = app_id[0]
                            app_id_detail = ",".join(list(app_id))
                            manger_list.append({'app_id_value': app_id_value, 'app_id_detail': app_id_detail})

                            # approver_detail = list(approver_detail)
                            # acc_value = approver_detail[2]
                            # default_cmp_code = approver_detail[3]
                            # total_value = convert_currency(const_total_value, str(user_currency), currency)
                            if float(total_value) <= max(app_limit_value):
                                return manger_list, msg_info
                            else:
                                while float(total_value) > max(app_limit_value):
                                    superior_flag = False
                                    current_acc_detail = approver_detail
                                    for approver_detail in approver_detail:

                                        workflow_approver_details = list(
                                            django_query_instance.django_filter_only_query(WorkflowACC, {
                                                'company_id': approver_detail[2],
                                                'account_assign_cat': approver_detail[4],
                                                'acc_value': approver_detail[1], 'client': client, 'del_ind': False
                                            }).values_list('app_username', 'sup_acc_value', 'sup_company_id',
                                                           'currency_id',
                                                           'sup_account_assign_cat', 'company_id', 'account_assign_cat',
                                                           'acc_value'))

                                        if not workflow_approver_details:
                                            manger_list = []
                                            msgid = 'MSG188'
                                            error_msg = get_message_desc(msgid)[1]

                                            msg_info = error_msg
                                            return manger_list, msg_info
                                        for workflow_approver_detail in workflow_approver_details:
                                            app_limit.append(workflow_approver_detail)
                                    # app_limit = list(django_query_instance.django_filter_only_query(WorkflowACC, {
                                    #     'company_id': default_cmp_code, 'account_assign_cat': acc_default,
                                    #     'acc_value': acc_value, 'client': client
                                    # }).values_list('app_username', 'sup_acc_value', 'sup_company_id'))

                                    if not app_limit:
                                        manger_list = []
                                        msgid = 'MSG172'
                                        error_msg = get_message_desc(msgid)[1]

                                        msg_info = error_msg
                                        return manger_list, msg_info
                                    else:
                                        for app_user, sup_acc_val, sup_company_id, currency_id, sup_account_assign_cat, company_id, account_assign_cat, acc_value in app_limit:
                                            if not django_query_instance.django_existence_check(UserData, {
                                                'client': client, 'username': app_user
                                            }):
                                                msgid = 'MSG176'
                                                error_msg = get_message_desc(msgid)[1]

                                                msg_info = error_msg
                                                return None, msg_info
                                            # manger_list.append(app_user)
                                        msg_info, approver_detail, app_limit_value = get_approvers_id_and_limit_value(
                                            app_limit,
                                            company_id,
                                            user_currency,
                                            client,
                                            schema_step_type)
                                        check_flag = check_approver_exists(acc_detail_list,
                                                                           approver_detail)
                                        if check_flag:
                                            msgid = 'MSG173'
                                            manger_list = []
                                            error_msg = get_message_desc(msgid)[1]
                                            msg_info = error_msg
                                            return manger_list, msg_info
                                        # manger_list, msg_info, app_limit_value, currency = get_appr_limit(
                                        #     default_cmp_code,
                                        #     app_user,
                                        #     client,
                                        #     schema_step_type,
                                        #     app_limit_value,
                                        #     manger_list)
                                        if msg_info:
                                            manger_list = []
                                            return manger_list, msg_info
                                            # acc_value = sup_acc_val
                                            # default_cmp_code = sup_company_id
                                        approver_detail = list(approver_detail)
                                        app_id = []

                                        for app_datails in approver_detail:
                                            app_id.append(app_datails[0])
                                            app_datails = list(app_datails)
                                            acc_detail_list.append(
                                                {'acc_value': app_datails[1],
                                                 'account_assign_cat': app_datails[4],
                                                 'company_id': app_datails[2],
                                                 })
                                            if ((app_datails[7] == app_datails[1]) and (
                                                    app_datails[2] == app_datails[5]) and (
                                                    app_datails[4] == app_datails[6])):
                                                msgid = 'MSG173'
                                                error_msg = get_message_desc(msgid)[1]
                                                msg_info = error_msg
                                                manger_list = []
                                                return manger_list, msg_info
                                        if len(app_id) > 1:
                                            app_id_value = CONST_MULTIPLE
                                            app_id_detail = ",".join(app_id)
                                        else:
                                            app_id_value = app_id[0]
                                        app_id_detail = ",".join(list(app_id))
                                        manger_list.append(
                                            {'app_id_value': app_id_value, 'app_id_detail': app_id_detail})
                        else:
                            msgid = 'MSG173'
                            error_msg = get_message_desc(msgid)[1]

                            msg_info = error_msg
        else:
            msgid = 'MSG174'
            error_msg = get_message_desc(msgid)[1]

            msg_info = error_msg
    else:
        msgid = 'MSG175'
        error_msg = get_message_desc(msgid)

        msg_info = error_msg

    return manger_list, msg_info


def check_approver_exists(acc_detail_list, app_details):
    """
    """
    approve_exists_flag = False
    for app_detail in app_details:
        app_detail = list(app_detail)
        for acc_detail in acc_detail_list:
            if (acc_detail['acc_value'] == app_detail[7]) and (acc_detail['account_assign_cat'] == app_detail[6]) and (
                    acc_detail['company_id'] == app_detail[5]):
                approve_exists_flag = True
                return approve_exists_flag
    return approve_exists_flag


def get_approvers_id_and_limit_value(app_limit, default_cmp_code, user_currency, client, schema_step_type):
    """
    """
    approvers_id = []
    app_limit_value = []
    approver_limit_value = []
    manger_list = []
    approver_detail = []
    max_app_limit_value = 0
    msg_info = None
    for app_user, sup_acc_val, sup_company_id, currency_id, sup_account_assign_cat, company_id, account_assign_cat, acc_value in app_limit:
        app_limit_value = []
        manger_list, msg_info, approver_limit, currency = get_appr_limit(company_id,
                                                                         app_user,
                                                                         client,
                                                                         schema_step_type,
                                                                         app_limit_value,
                                                                         manger_list)

        if msg_info:
            return msg_info, approver_detail, max_app_limit_value
        if currency != global_variables.GLOBAL_REQUESTER_CURRENCY:
            approver_limit = convert_currency(approver_limit, str(user_currency), currency)
        approver_limit_value.append(approver_limit)
    max_app_limit_value = max(approver_limit_value)
    approver_limit_index = []
    approver_detail = []
    for count, appr_limit_value in enumerate(approver_limit_value):
        if appr_limit_value == max_app_limit_value:
            approver_limit_index.append(count)
    for count, app_details in enumerate(app_limit):
        for app_limit_index in approver_limit_index:
            if count == app_limit_index:
                approver_detail.append(app_details)
    return msg_info, approver_detail, max_app_limit_value


def get_users_first_name_old(manager_details):
    """
    """
    user_data_list = []
    user_id_list = []
    first_name_list = []
    for manager_detail in manager_details:
        user_data_dictionary = {}
        if django_query_instance.django_existence_check(UserData, {'username': manager_detail,
                                                                   'client': global_variables.GLOBAL_CLIENT}):

            user_data = django_query_instance.django_filter_only_query(UserData,
                                                                       {'username': manager_detail,
                                                                        'client': global_variables.GLOBAL_CLIENT}).values(
                'username',
                'first_name')[0]
            user_data_dictionary = user_data
        elif manager_detail == CONST_AUTO:
            user_data_dictionary = {'username': manager_detail, 'first_name': manager_detail}
        else:
            user_data_dictionary = {'username': manager_detail, 'first_name': ''}
        user_data_list.append(user_data_dictionary)
    if user_data_list:
        for user_data in user_data_list:
            user_id_list.append(user_data['username'])
            first_name_list.append(user_data['first_name'])
    return first_name_list, user_id_list


def get_users_first_name(manager_details):
    """
    """
    user_data_list = []
    for manager_detail in manager_details:
        user_data_dictionary = manager_detail
        if manager_detail['app_id_value'] in [CONST_AUTO, CONST_MULTIPLE]:
            user_data_dictionary['first_name'] = manager_detail['app_id_value']
        elif django_query_instance.django_existence_check(UserData, {'username': manager_detail['app_id_value'],
                                                                     'client': global_variables.GLOBAL_CLIENT}):

            user_data = django_query_instance.django_filter_only_query(UserData,
                                                                       {'username': manager_detail['app_id_value'],
                                                                        'client': global_variables.GLOBAL_CLIENT}).values(
                'username',
                'first_name')[0]
            user_data_dictionary['first_name'] = user_data['first_name']
        else:
            user_data_dictionary['first_name'] = ''
        user_data_list.append(user_data_dictionary)
    return user_data_list, user_data_list


def get_completion_work_flow(client, prod_cat_list, default_cmp_code):
    """
    :param client:
    :param prod_cat_list:
    :param default_cmp_code:
    :return:
    """
    list_user = []
    prod_cat_list = list(set(prod_cat_list))

    org_porg_object_id = django_query_instance.django_filter_value_list_query(OrgModel, {
        'client': client, 'del_ind': False, 'node_type': CONST_PORG
    }, 'object_id')

    orgattr_porg_object_id = django_query_instance.django_filter_value_list_query(OrgAttributesLevel, {
        'attribute_id': CONST_CO_CODE, 'low__in': default_cmp_code, 'object_id__in': org_porg_object_id,
        'client': client, 'del_ind': False
    }, 'object_id')

    porg_id = django_query_instance.django_filter_value_list_query(OrgPorg, {
        'object_id__in': orgattr_porg_object_id, 'client': client, 'del_ind': False
    }, 'porg_id')

    pgrp_object_id = django_query_instance.django_filter_value_list_query(OrgPGroup, {
        'porg_id__in': porg_id, 'client': client, 'del_ind': False
    }, 'object_id')

    default_cmp_code.append("ALL")
    company_code_list = default_cmp_code

    prod_cat_range = django_query_instance.django_filter_only_query(OrgAttributesLevel, {
        'object_id__in': pgrp_object_id, 'attribute_id': CONST_RESP_PROD_CAT, 'extended_value__in': company_code_list,
        'client': client, 'del_ind': False
    }).values_list('low', 'high', 'object_id')

    for low, high, object_id in prod_cat_range:
        for prod_cat in prod_cat_list:
            if int(prod_cat) in range(int(low), int(high) + 1):
                pgrp_name_desc = django_query_instance.django_filter_only_query(OrgPGroup, {
                    'object_id': object_id, 'client': client, 'del_ind': False
                })
                for pgrp in pgrp_name_desc:
                    list_user.append(pgrp.pgroup_id)

    if len(list_user) > 1:
        list_user[0] = CONST_MULTIPLE
    return list_user


def empty_shopping_cart_data(username, client):
    """
    :param username:
    :param client:
    :return:
    """
    item_details = django_query_instance.django_filter_only_query(CartItemDetails,
                                                                  {'username': username, 'client': client})
    for eform_guid in item_details:
        django_query_instance.django_filter_delete_query(EformFieldData, {'cart_guid': eform_guid.guid})
    item_details.delete()


def unpack_accounting_data(accounting_data, sc_check_instance):
    default_account_assignment_value = ''
    default_account_assignment_category = ''
    if accounting_data['acc_default']:
        default_account_assignment_category = accounting_data['acc_default'].split(' - ')[0]

    get_account_assignment_value = accounting_data['acc_value'][0]
    if len(get_account_assignment_value) > 0:
        default_account_assignment_value = get_account_assignment_value.split(' - ')[0]

    default_gl_account = accounting_data['gl_acc_item_level_default']

    if default_account_assignment_category == '' or default_account_assignment_value == '' or len(
            default_gl_account) == 0:
        sc_check_instance.account_assignment_check(default_account_assignment_category,
                                                   default_account_assignment_value,
                                                   '',
                                                   '0')

    item_number = 1
    for gl_account in default_gl_account:
        gl_account_number = gl_account['default_gl_acc'].split(' - ')[0]
        sc_check_instance.account_assignment_check(default_account_assignment_category,
                                                   default_account_assignment_value,
                                                   gl_account_number,
                                                   item_number)
        item_number = item_number + 1

    return default_account_assignment_category, default_account_assignment_value


def get_limit_item_details(cart_item_guid):
    limit_item_details = {}
    limit_item_data = django_query_instance.django_get_query(CartItemDetails, {'guid': cart_item_guid})
    if limit_item_data:
        follow_up_actions = limit_item_data.ir_gr_ind_limi

        if follow_up_actions:
            limit_item_details['follow_up_actions'] = 'Invoice and confirmation only'
        else:
            limit_item_details['follow_up_actions'] = 'Confirmations Only'

        limit_item_details['item_name'] = limit_item_data.description
        limit_item_details['overall_limit'] = limit_item_data.overall_limit
        limit_item_details['expected_value'] = limit_item_data.expected_value
        limit_item_details['product_category'] = limit_item_data.prod_cat + ' - ' + limit_item_data.prod_cat_desc
        limit_item_details['from_date'] = limit_item_data.start_date
        limit_item_details['to_date'] = limit_item_data.end_date
        limit_item_details['item_del_date'] = limit_item_data.item_del_date
        limit_item_details['currency'] = limit_item_data.currency
        limit_item_details['supplier'] = limit_item_data.supplier_id

        from_date = limit_item_data.start_date
        to_date = limit_item_data.end_date
        item_del_date = limit_item_data.item_del_date

        if from_date:
            limit_item_details['timeframe'] = 'From Date'
            limit_item_details['dates'] = from_date

        if item_del_date:
            limit_item_details['timeframe'] = 'On'
            limit_item_details['dates'] = item_del_date

        if from_date and to_date:
            limit_item_details['between'] = 'From - To:'
            limit_item_details['from_date'] = from_date
            limit_item_details['to_date'] = to_date

    return limit_item_details


def get_limit_order_item_details(cart_items):
    """

    """
    is_limit_item = False
    limit_item_details = {}
    for items in cart_items:
        if items['call_off'] == CONST_LIMIT_ORDER_CALLOFF:
            is_limit_item = True
            limit_item_details = get_limit_item_details(items['guid'])
    return limit_item_details, is_limit_item


def update_supplier_uom(prod_detail):
    """

    """
    prod_detail = update_supplier_desc(prod_detail)

    if django_query_instance.django_existence_check(UnitOfMeasures,
                                                    {'uom_id': prod_detail['unit_id']}):
        prod_detail['unit_desc'] = django_query_instance.django_filter_value_list_query(UnitOfMeasures,
                                                                                        {'uom_id': prod_detail[
                                                                                            'unit_id']},
                                                                                        'uom_description')[0]
    return prod_detail


def update_supplier_uom_for_prod(prod_detail):
    """

    """
    prod_detail = update_supplier_desc(prod_detail)
    if django_query_instance.django_existence_check(UnitOfMeasures,
                                                    {'uom_id': prod_detail['unit']}):
        prod_detail['unit_desc'] = django_query_instance.django_filter_value_list_query(UnitOfMeasures,
                                                                                        {'uom_id': prod_detail[
                                                                                            'unit']},
                                                                                        'uom_description')[0]
    return prod_detail


def update_suppliers_uom_details(cart_items):
    """

    """
    for items in cart_items:
        items = update_supplier_uom_for_prod(items)
    return cart_items


def update_supplier_desc(prod_detail):
    """

    """
    if django_query_instance.django_existence_check(SupplierMaster,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'supplier_id': prod_detail['supplier_id'],
                                                     'del_ind': False}):
        prod_detail['supplier_desc'] = django_query_instance.django_filter_value_list_query(SupplierMaster,
                                                                                            {
                                                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                                                'supplier_id':
                                                                                                    prod_detail[
                                                                                                        'supplier_id'],
                                                                                                'del_ind': False},
                                                                                            'name1')[0]

    return prod_detail


def update_unspsc(prod_detail, prod_cat_id):
    """

    """
    if django_query_instance.django_existence_check(UnspscCategoriesCustDesc,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'language_id': global_variables.GLOBAL_USER_LANGUAGE,
                                                     'prod_cat_id': prod_detail[prod_cat_id]}):
        prod_detail['prod_cat_desc'] = django_query_instance.django_filter_value_list_query(UnspscCategoriesCustDesc,
                                                                                            {
                                                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                                                'language_id': global_variables.GLOBAL_USER_LANGUAGE,
                                                                                                'prod_cat_id':
                                                                                                    prod_detail[
                                                                                                        prod_cat_id]},
                                                                                            'category_desc')[0]
    else:
        prod_detail['prod_cat_id'] = prod_detail[prod_cat_id]
    return prod_detail


def update_country(prod_detail):
    """

    """
    if django_query_instance.django_existence_check(Country,
                                                    {'country_code': prod_detail['country_of_origin_id']}):
        prod_detail['country_desc'] = django_query_instance.django_filter_value_list_query(Country,
                                                                                           {'country_code': prod_detail[
                                                                                               'country_of_origin_id']},
                                                                                           'country_name')[0]
    return prod_detail


def save_approver_detail(header_guid):
    """

    """
    sc_header_data = django_query_instance.django_get_query(ScHeader, {'client': global_variables.GLOBAL_CLIENT,
                                                                       'guid': header_guid})
    account_assignment_category, account_assignment_value = get_highest_acc_detail(header_guid)
    approval_data = get_manger_detail(global_variables.GLOBAL_CLIENT, sc_header_data.requester,
                                      account_assignment_category, sc_header_data.total_value, sc_header_data.co_code,
                                      account_assignment_value,
                                      global_variables.GLOBAL_USER_CURRENCY)
    delete_approver_detail(header_guid)

    sc_completion_flag = False
    if django_query_instance.django_existence_check(ScItem, {'client': global_variables.GLOBAL_CLIENT,
                                                             'del_ind': False,
                                                             'header_guid': header_guid,
                                                             'call_off': CONST_PR_CALLOFF}):
        sc_completion_flag = True
    save_sc_approval(approval_data[0], header_guid, CONST_SC_HEADER_SAVED, sc_completion_flag)


def delete_approver_detail(header_guid):
    """

    """

    if django_query_instance.django_existence_check(ScPotentialApproval, {'sc_header_guid': header_guid,
                                                                          'client': global_variables.GLOBAL_CLIENT}):
        django_query_instance.django_filter_delete_query(ScPotentialApproval, {'sc_header_guid': header_guid,
                                                                               'client': global_variables.GLOBAL_CLIENT})
    if django_query_instance.django_existence_check(ScApproval, {'header_guid': header_guid,
                                                                 'client': global_variables.GLOBAL_CLIENT}):
        django_query_instance.django_filter_delete_query(ScApproval, {'header_guid': header_guid,
                                                                      'client': global_variables.GLOBAL_CLIENT})


def get_highest_acc_detail(header_guid):
    """

    """
    previous_item_highest_value = django_query_instance.django_filter_only_query(ScItem, {
        'header_guid': django_query_instance.django_get_query(ScHeader, {'guid': header_guid})
    }).order_by('-value')[0]

    highest_item_accounting_data = django_query_instance.django_get_query(ScAccounting, {
        'item_guid': previous_item_highest_value.guid
    })

    account_assignment_category = highest_item_accounting_data.acc_cat
    if account_assignment_category == 'CC':
        account_assignment_value = highest_item_accounting_data.cost_center

    elif account_assignment_category == 'AS':
        account_assignment_value = highest_item_accounting_data.asset_number

    elif account_assignment_category == 'OR':
        account_assignment_value = highest_item_accounting_data.internal_order

    else:
        account_assignment_value = highest_item_accounting_data.wbs_ele
    return account_assignment_category, account_assignment_value


def get_default_cart_name(requester_first_name):
    """

    """
    date_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    cart_name = concatenate_str_with_space(requester_first_name, date_time)

    return cart_name


def get_SC_details(sc_header_guid):
    """

    """
    po_header_details = django_query_instance.django_filter_query(ScHeader,
                                                                  {'sc_header_guid': sc_header_guid,
                                                                   'client': global_variables.GLOBAL_CLIENT},
                                                                  None,
                                                                  None)
    for po_header_detail in po_header_details:
        po_header_detail['supplier_description'] = django_query_instance.django_filter_value_list_query(SupplierMaster,
                                                                                                        {
                                                                                                            'client': global_variables.GLOBAL_CLIENT,
                                                                                                            'supplier_id':
                                                                                                                po_header_detail[
                                                                                                                    'supplier_id']},
                                                                                                        'name1')[0]
        # if django_query_instance.django_filter_count_query(ScData,
        #                                                    {'client': global_variables.GLOBAL_CLIENT,
        #                                                     'sc_header_guid': po_header_detail['sc_header_guid']}) > 1:
        #     po_header_detail['porg_description'] = 'MULTIPLE'
        # elif django_query_instance.django_existence_check(PurchasingData,
        #                                                   {'client': global_variables.GLOBAL_CLIENT,
        #                                                    'sc_header_guid': po_header_detail['sc_header_guid']}):
        # purchaser_detail = django_query_instance.django_filter_query(PurchasingData,
        #                                                              {'client': global_variables.GLOBAL_CLIENT,
        #                                                               'sc_header_guid': po_header_detail[
        #                                                                   'sc_header_guid']},
        #                                                              None,
        #                                                              None)[0]
        # if django_query_instance.django_existence_check(OrgPorg,
        #                                                 {'client': global_variables.GLOBAL_CLIENT,
        #                                                  'porg_id': purchaser_detail['purch_org']}):
        #     porg_description = django_query_instance.django_filter_value_list_query(OrgPorg,
        #                                                                             {
        #                                                                                 'client': global_variables.GLOBAL_CLIENT,
        #                                                                                 'porg_id': purchaser_detail[
        #                                                                                     'purch_org']},
        #                                                                             'description')[0]
        #
        #     po_header_detail['porg_description'] = purchaser_detail['purch_org'] + ' - ' + porg_description
        #
        # if django_query_instance.django_existence_check(OrgPGroup,
        #                                                 {'client': global_variables.GLOBAL_CLIENT,
        #                                                  'pgroup_id': purchaser_detail['purch_grp']}):
        #     pgrp_description = django_query_instance.django_filter_value_list_query(OrgPGroup,
        #                                                                             {'client': global_variables.GLOBAL_CLIENT,
        #                                                                              'pgroup_id': purchaser_detail['purch_grp']},
        #                                                                             'description')[0]
        #
        #     po_header_detail['pgrp_description'] = purchaser_detail['purch_grp'] + ' - ' + pgrp_description

    sc_item_details = django_query_instance.django_filter_query(ScItem,
                                                                {'sc_header_guid': sc_header_guid,
                                                                 'client': global_variables.GLOBAL_CLIENT},
                                                                None,
                                                                None)
    po_item_guid_list = dictionary_key_to_list(sc_item_details, 'po_item_guid')

    sc_accounting_details = django_query_instance.django_filter_query(ScAccounting,
                                                                      {'sc_item_guid__in': po_item_guid_list,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      None,
                                                                      None)
    for sc_header_guid in po_header_details:
        sc_header_guid['guid'] = sc_header_guid['sc_header_guid']
        del sc_header_guid['sc_header_guid']
        sc_header_guid['created_at'] = sc_header_guid['po_header_created_at']
        del sc_header_guid['po_header_created_at']
        sc_header_guid['created_by'] = sc_header_guid['po_header_created_by']
        del sc_header_guid['po_header_created_by']
    po_header_details, po_approver_details, sc_completion, requester_first_name = get_po_header_app(po_header_details,
                                                                                                    global_variables.GLOBAL_CLIENT)
    # po_header_level_address = django_query_instance.django_filter_query(ddresses,
    #                                                                     {'sc_header_guid': sc_header_guid,
    #                                                                      'client': global_variables.GLOBAL_CLIENT},
    #                                                                     None,
    #                                                                     None)
    # po_item_level_address = django_query_instance.django_filter_query(PoAddresses,
    #                                                                   {'po_item_guid__in': po_item_guid_list,
    #                                                                    'client': global_variables.GLOBAL_CLIENT},
    #                                                                   None,
    #                                                                   None)
    context = {'po_header_details': po_header_details,
               'sc_item_details': sc_item_details,
               'sc_accounting_details': sc_accounting_details,
               'po_approver_details': po_approver_details,
               'sc_completion': sc_completion,
               'requester_first_name': requester_first_name,

               }
    return context


def get_cart_default_name_and_user_first_name(first_name, last_name):
    """

    """
    requester_first_name = requester_field_info(global_variables.GLOBAL_LOGIN_USERNAME, 'first_name')
    # Get default shopping cart name
    cart_name = get_default_cart_name(requester_first_name)
    receiver_name = concatenate_str_with_space(first_name, last_name)
    return requester_first_name, cart_name, receiver_name


def get_cart_default_name_and_user_first_name_last_name():
    """

    """
    requester_first_name = requester_field_info(global_variables.GLOBAL_LOGIN_USERNAME, 'first_name')
    # Get default shopping cart name
    cart_name = get_default_cart_name(requester_first_name)
    return requester_first_name, cart_name
