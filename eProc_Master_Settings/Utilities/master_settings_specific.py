import time

from django.db.models.query_utils import Q
from requests import request

from eProc_Basic.Utilities.functions.camel_case import convert_to_camel_case, convert_to_camel_case_v2
from eProc_Basic.Utilities.functions.dictionary_key_to_list import dictionary_key_to_list

from eProc_Basic.Utilities.functions.distinct_list import *
from eProc_Basic.Utilities.functions.image_type_funtions import get_image_type
from eProc_Basic.Utilities.functions.log_function import update_log_info
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Configuration.models.application_data import *
from eProc_Configuration.models.basic_data import *
from eProc_Configuration.models.master_data import *

from eProc_Org_Model.Utilities import client
from eProc_Org_Model.models import *
import datetime
from eProc_Basic.Utilities.constants.constants import CONST_ACTION_DELETE, CONST_UNSPSC_IMAGE_TYPE, CONST_GLACC
from eProc_Basic.Utilities.functions.django_query_set import bulk_create_entry_db
from eProc_Basic.Utilities.functions.get_db_query import django_query_instance, get_country_data
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Configuration.Utilities.application_settings_generic import *
from eProc_Configuration.models import *
from eProc_Basic.Utilities.messages.messages import *
from eProc_Configuration.models.development_data import *
from eProc_Configuration.models.development_data import AccountAssignmentCategory
from eProc_Org_Model.models.org_model import *
from eProc_Registration.models import *
from eProc_Registration.models.registration_model import *
from eProc_Shopping_Cart.context_processors import update_user_info

fieldtypedesc_instance = FieldTypeDescriptionUpdate()


class MasterSettingsSave:
    def __init__(self):
        self.current_date_time = datetime.today()
        self.username = global_variables.GLOBAL_LOGIN_USERNAME
        self.client = global_variables.GLOBAL_CLIENT

    def save_product_cat_cust(self, prodcat_data):
        """

        """
        prodcat_db_list = []
        for prodcat_detail in prodcat_data:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(UnspscCategoriesCust,
                                                                {'prod_cat_id': prodcat_detail['prod_cat_id'],
                                                                 'client': self.client}):
                guid = guid_generator()
                prodcat_db_dictionary = {'prod_cat_guid': guid,
                                         'prod_cat_id': UnspscCategories.objects.get(
                                             prod_cat_id=prodcat_detail['prod_cat_id']),
                                         'unspsc_categories_cust_created_at': self.current_date_time,
                                         'unspsc_categories_cust_created_by': self.username,
                                         'unspsc_categories_cust_changed_at': self.current_date_time,
                                         'unspsc_categories_cust_changed_by': self.username,
                                         'client': self.client
                                         }

                prodcat_db_list.append(prodcat_db_dictionary)
            else:
                if prodcat_detail['del_ind'] in ['1', True]:
                    django_query_instance.django_filter_delete_query(UnspscCategoriesCust,
                                                                     {'prod_cat_id': prodcat_detail['prod_cat_id'],
                                                                      'client': self.client})
                    prod_cat = prodcat_detail['prod_cat_id']

                    delete_prod_cat_image_to_db(prod_cat)
                else:
                    if django_query_instance.django_existence_check(UnspscCategoriesCust,
                                                                    {'prod_cat_id': prodcat_detail['prod_cat_id'],
                                                                     'client': self.client}):
                        django_query_instance.django_update_query(UnspscCategoriesCust,
                                                                  {'prod_cat_id': prodcat_detail['prod_cat_id'],
                                                                   'client': self.client},
                                                                  {'prod_cat_id': UnspscCategories.objects.get(
                                                                      prod_cat_id=prodcat_detail['prod_cat_id']),
                                                                      'unspsc_categories_cust_changed_at': self.current_date_time,
                                                                      'unspsc_categories_cust_changed_by': self.username,
                                                                      'del_ind': prodcat_detail['del_ind'],
                                                                      'client': OrgClients.objects.get(
                                                                          client=self.client)})
                    else:
                        django_query_instance.django_filter_delete_query(UnspscCategoriesCust,
                                                                         {'prod_cat_id': prodcat_detail['prod_cat_id'],
                                                                          'client': self.client})

        if prodcat_db_list:
            bulk_create_entry_db(UnspscCategoriesCust, prodcat_db_list)

    def save_product_cat_cust_data_into_db(self, prodcat_data):
        """

        """
        # save data into UnspscCategoriesCust db table
        self.save_product_cat_cust(prodcat_data['data'])

        # get message based on action
        message = get_message_detail_based_on_action(prodcat_data['action'])

        upload_response = get_unspsc_cat_cust_data()

        return upload_response, message

    def save_product_cat_custdesc(self, prodcatdesc_data):
        """

        """
        prodcatdesc_db_list = []

        for prodcatdesc_detail in prodcatdesc_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(UnspscCategoriesCustDesc,
                                                                {'prod_cat_id': prodcatdesc_detail['prod_cat_id'],
                                                                 'language_id': prodcatdesc_detail['language_id'],
                                                                 'client': self.client}):
                guid = guid_generator()
                prodcatdesc_db_dictionary = {'prod_cat_desc_guid': guid,
                                             'prod_cat_id': UnspscCategories.objects.get(
                                                 prod_cat_id=prodcatdesc_detail['prod_cat_id']),
                                             'category_desc': convert_to_camel_case(prodcatdesc_detail['description']),
                                             'language_id': Languages.objects.get(
                                                 language_id=prodcatdesc_detail['language_id']),
                                             'unspsc_categories_cust_desc_created_at': self.current_date_time,
                                             'unspsc_categories_cust_desc_created_by': self.username,
                                             'unspsc_categories_cust_desc_changed_at': self.current_date_time,
                                             'unspsc_categories_cust_desc_changed_by': self.username,
                                             'client': self.client
                                             }

                prodcatdesc_db_list.append(prodcatdesc_db_dictionary)
            else:
                if prodcatdesc_detail['del_ind'] in ['1', True]:
                    django_query_instance.django_filter_delete_query(UnspscCategoriesCustDesc,
                                                                     {'prod_cat_id': prodcatdesc_detail['prod_cat_id'],
                                                                      'language_id': prodcatdesc_detail['language_id'],
                                                                      'client': self.client})
                    if prodcatdesc_detail['language_id'] == 'EN':
                        django_query_instance.django_filter_delete_query(UnspscCategoriesCust,
                                                                         {'prod_cat_id': prodcatdesc_detail[
                                                                             'prod_cat_id'],
                                                                          'client': self.client})
                else:
                    if django_query_instance.django_existence_check(UnspscCategoriesCustDesc,
                                                                    {'prod_cat_id': prodcatdesc_detail['prod_cat_id'],
                                                                     'client': self.client}):
                        django_query_instance.django_update_query(UnspscCategoriesCustDesc,
                                                                  {'prod_cat_id': prodcatdesc_detail['prod_cat_id'],
                                                                   'language_id': prodcatdesc_detail['language_id'],
                                                                   'client': self.client},
                                                                  {'category_desc': convert_to_camel_case(
                                                                      prodcatdesc_detail['description']),
                                                                      'prod_cat_id': UnspscCategories.objects.get(
                                                                          prod_cat_id=prodcatdesc_detail[
                                                                              'prod_cat_id']),
                                                                      'language_id': Languages.objects.get(
                                                                          language_id=prodcatdesc_detail[
                                                                              'language_id']),
                                                                      'unspsc_categories_cust_desc_changed_at': self.current_date_time,
                                                                      'unspsc_categories_cust_desc_changed_by': self.username,
                                                                      'del_ind': prodcatdesc_detail['del_ind'],
                                                                      'client': OrgClients.objects.get(
                                                                          client=self.client)})
                    else:
                        django_query_instance.django_filter_delete_query(UnspscCategoriesCustDesc,
                                                                         {'prod_cat_id': prodcatdesc_detail[
                                                                             'prod_cat_id'],
                                                                          'client': self.client})

        if prodcatdesc_db_list:
            bulk_create_entry_db(UnspscCategoriesCustDesc, prodcatdesc_db_list)

    def save_product_cat_cust_desc_data_into_db(self, prodcatdesc_data):
        """

        """
        # save data into UnspscCategoriesCustdesc db table
        self.save_product_cat_custdesc(prodcatdesc_data)

        # get message based on action
        message = get_message_detail_based_on_action(prodcatdesc_data['action'])

        upload_response = get_unspsc_cat_custdesc_data()[0]

        return upload_response, message

    def save_incoterms(self, incoterms_data):
        """

        """
        incoterms_db_list = []
        for incoterms_detail in incoterms_data:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(Incoterms,
                                                                {'incoterm_key': incoterms_detail['incoterm_key']}):
                incoterms_db_dictionary = {'incoterm_key': (incoterms_detail['incoterm_key']).upper(),
                                           'description': convert_to_camel_case(incoterms_detail['description']),
                                           'incoterms_created_at': self.current_date_time,
                                           'incoterms_created_by': self.username,
                                           'incoterms_changed_at': self.current_date_time,
                                           'incoterms_changed_by': self.username
                                           }
                incoterms_db_list.append(incoterms_db_dictionary)
            else:
                django_query_instance.django_update_query(Incoterms,
                                                          {'incoterm_key': incoterms_detail['incoterm_key']},
                                                          {'incoterm_key': incoterms_detail['incoterm_key'],
                                                           'description': convert_to_camel_case(
                                                               incoterms_detail['description']),
                                                           'incoterms_changed_at': self.current_date_time,
                                                           'incoterms_changed_by': self.username,
                                                           'del_ind': incoterms_detail['del_ind']})
        if incoterms_db_list:
            bulk_create_entry_db(Incoterms, incoterms_db_list)

    def save_incoterms_data_into_db(self, incoterms_data):
        """

        """
        self.save_incoterms(incoterms_data['data'])
        message = get_message_detail_based_on_action(incoterms_data['action'])

        upload_response = get_incoterms_data()

        return upload_response, message

    def save_payterm(self, payterm_data):
        """

        """
        payterm_db_list = []
        for payterm_detail in payterm_data:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(Payterms,
                                                                {'payment_term_key': payterm_detail[
                                                                    'payment_term_key'],
                                                                 'client': self.client
                                                                 }):

                payterm_db_dictionary = {'payment_term_guid': guid_generator(),
                                         'payment_term_key': (payterm_detail['payment_term_key']),
                                         'payterms_created_at': self.current_date_time,
                                         'payterms_created_by': self.username,
                                         'payterms_changed_at': self.current_date_time,
                                         'payterms_changed_by': self.username,
                                         'client': self.client
                                         }
                payterm_db_list.append(payterm_db_dictionary)
            else:
                django_query_instance.django_update_query(Payterms,
                                                          {'payment_term_key': payterm_detail['payment_term_key'],
                                                           'client': self.client},
                                                          {'payment_term_key': payterm_detail['payment_term_key'],
                                                           'payterms_changed_at': self.current_date_time,
                                                           'payterms_changed_by': self.username,
                                                           'del_ind': payterm_detail['del_ind'],
                                                           'client': self.client})
        if payterm_db_list:
            bulk_create_entry_db(Payterms, payterm_db_list)

    def save_payterm_data_into_db(self, payterm_data):
        """

        """
        self.save_payterm(payterm_data['data'])
        message = get_message_detail_based_on_action(payterm_data['action'])

        upload_response = get_payment_data()

        return upload_response, message

    def save_company_data(self, company_data):
        """

        """
        company_db_list = []
        for company_detail in company_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(OrgCompanies,
                                                                {'company_id': company_detail['company_id'],
                                                                 'client': self.client}):
                guid = guid_generator()
                company_db_dictionary = {'company_guid': guid,
                                         'name1': convert_to_camel_case(company_detail['name1']),
                                         'name2': convert_to_camel_case(company_detail['name2']),
                                         'company_id': company_detail['company_id'],
                                         'client': OrgClients.objects.get(client=self.client),
                                         'org_companies_changed_at': self.current_date_time,
                                         'org_companies_changed_by': self.username,
                                         'org_companies_created_at': self.current_date_time,
                                         'org_companies_created_by': self.username,
                                         }
                company_db_list.append(company_db_dictionary)

            else:
                django_query_instance.django_update_query(OrgCompanies,
                                                          {'company_id': company_detail['company_id'],
                                                           'client': self.client},
                                                          {'name1': convert_to_camel_case(company_detail['name1']),
                                                           'name2': convert_to_camel_case(company_detail['name2']),
                                                           'company_id': company_detail['company_id'],
                                                           'org_companies_created_at': self.current_date_time,
                                                           'org_companies_created_by': self.username,
                                                           'del_ind': company_detail['del_ind'],
                                                           'client': OrgClients.objects.get(client=self.client), })
        if company_db_list:
            bulk_create_entry_db(OrgCompanies, company_db_list)

    def save_company_data_into_db(self, company_data):
        self.save_company_data(company_data)

        message = get_message_detail_based_on_action(company_data['action'])

        upload_response = get_org_companies_data()

        return upload_response, message

    def save_porg_data(self, pgorg_data):
        pgorg_data_db_list = []
        for pgorg_detail in pgorg_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(OrgPorg,
                                                                {'porg_id': pgorg_detail['porg_id'],
                                                                 'client': self.client}):
                guid = guid_generator()
                pgorg_db_dictionary = {'porg_guid': guid,
                                       'porg_id': (pgorg_detail['porg_id']).upper(),
                                       'description': convert_to_camel_case(pgorg_detail['description']),
                                       'object_id': None,
                                       'del_ind': False,
                                       'client': self.client,
                                       'org_porg_changed_at': self.current_date_time,
                                       'org_porg_changed_by': self.username,
                                       'org_porg_created_at': self.current_date_time,
                                       'org_porg_created_by': self.username,
                                       }

                pgorg_data_db_list.append(pgorg_db_dictionary)

            else:

                django_query_instance.django_update_query(OrgPorg,
                                                          {'porg_id': pgorg_detail['porg_id'],
                                                           'client': global_variables.GLOBAL_CLIENT},
                                                          {'porg_id': pgorg_detail['porg_id'],
                                                           'description': convert_to_camel_case(
                                                               pgorg_detail['description']),
                                                           'object_id': None,
                                                           'org_porg_changed_at': self.current_date_time,
                                                           'org_porg_changed_by': self.username,
                                                           'client': self.client,
                                                           'del_ind': pgorg_detail['del_ind']})
        if pgorg_data_db_list:
            bulk_create_entry_db(OrgPorg, pgorg_data_db_list)

    def save_purorg_data_into_db(self, pgorg_data):
        self.save_porg_data(pgorg_data)
        message = get_message_detail_based_on_action(pgorg_data['action'])
        upload_response = get_org_porg_data()

        return upload_response, message

    def save_pgrp_data(self, pggrp_data):
        """

        """
        pggrp_data_db_list = []

        for pggrp_detail in pggrp_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(OrgPGroup,
                                                                {'pgroup_id': pggrp_detail['pgroup_id'],
                                                                 'client': self.client}):
                guid = guid_generator()
                pggrp_db_dictionary = {'pgroup_guid': guid,
                                       'pgroup_id': (pggrp_detail['pgroup_id']).upper(),
                                       'description': convert_to_camel_case(pggrp_detail['description']),
                                       'object_id': None,
                                       'del_ind': False,
                                       'client': self.client,
                                       'org_pgroup_changed_at': self.current_date_time,
                                       'org_pgroup_changed_by': self.username,
                                       'org_pgroup_created_at': self.current_date_time,
                                       'org_pgroup_created_by': self.username,
                                       }

                pggrp_data_db_list.append(pggrp_db_dictionary)

            else:
                django_query_instance.django_update_query(OrgPGroup,
                                                          {'pgroup_id': pggrp_detail['pgroup_id'],
                                                           'client': self.client},
                                                          {'pgroup_id': pggrp_detail['pgroup_id'],
                                                           'description': convert_to_camel_case(
                                                               pggrp_detail['description']),
                                                           'object_id': None,
                                                           'org_pgroup_changed_at': self.current_date_time,
                                                           'org_pgroup_changed_by': self.username,
                                                           'client': self.client,
                                                           'del_ind': pggrp_detail['del_ind']})
        if pggrp_data_db_list:
            bulk_create_entry_db(OrgPGroup, pggrp_data_db_list)

    def save_purgrp_data_into_db(self, pggrp_data):
        self.save_pgrp_data(pggrp_data)
        message = get_message_detail_based_on_action(pggrp_data['action'])
        upload_response = get_orgpgroup_data()

        return upload_response, message

    def save_emp_data(self, emp_data):
        """

        """

        emp_data_db_list = []

        for emp_detail in emp_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(UserData,
                                                                {'email': emp_detail['email'],
                                                                 'client': self.client}):

                emp_db_dictionary = {
                    'email': emp_detail['email'],
                    'username': emp_detail['username'],
                    'first_name': emp_detail['first_name'],
                    'last_name': emp_detail['last_name'],
                    'phone_num': emp_detail['phone_num'],
                    'date_format': emp_detail['date_format'],
                    'employee_id': emp_detail['employee_id'],
                    'decimal_notation': emp_detail['decimal_notation'],
                    'user_type': emp_detail['user_type'],
                    'currency_id': Currency.objects.get(
                        currency_id=emp_detail['currency_id']),
                    'language_id': Languages.objects.get(
                        language_id=emp_detail['language_id']),
                    'time_zone': TimeZone.objects.get(
                        time_zone=emp_detail['time_zone']),
                    'del_ind': False,
                    'client': self.client,
                    'user_data_changed_at': self.current_date_time,
                    'user_data_changed_by': self.username,
                    'user_data_created_at': self.current_date_time,
                    'user_data_created_by': self.username,
                }
                emp_data_db_list.append(emp_db_dictionary)
            else:
                if emp_detail['del_ind'] == 1:
                    django_query_instance.django_update_query(UserData,
                                                              {'email': emp_detail['email'],
                                                               'client': self.client},
                                                              {'email': emp_detail['email'],
                                                               'user_data_changed_at': self.current_date_time,
                                                               'user_data_changed_by': self.username,
                                                               'client': self.client,
                                                               'del_ind': emp_detail['del_ind']})
                else:
                    django_query_instance.django_update_query(UserData,
                                                              {'email': emp_detail['email'],
                                                               'client': self.client},
                                                              {'email': emp_detail['email'],
                                                               'username': emp_detail['username'],
                                                               'first_name': emp_detail['first_name'],
                                                               'last_name': emp_detail['last_name'],
                                                               'phone_num': emp_detail['phone_num'],
                                                               'date_format': emp_detail['date_format'],
                                                               'employee_id': emp_detail['employee_id'],
                                                               'decimal_notation': emp_detail['decimal_notation'],
                                                               'user_type': emp_detail['user_type'],
                                                               'currency_id': Currency.objects.get(
                                                                   currency_id=emp_detail['currency_id']),
                                                               'language_id': Languages.objects.get(
                                                                   language_id=emp_detail['language_id']),
                                                               'time_zone': TimeZone.objects.get(
                                                                   time_zone=emp_detail['time_zone']),
                                                               'del_ind': False,
                                                               'client': self.client,
                                                               'user_data_changed_at': self.current_date_time,
                                                               'user_data_changed_by': self.username
                                                               })

        if emp_data_db_list:
            bulk_create_entry_db(UserData, emp_data_db_list)

    def save_employee_data_into_db(self, emp_data):
        self.save_emp_data(emp_data)
        message = get_message_detail_based_on_action(emp_data['action'])

        return message

    def save_workflow_schema(self, workflowschema_data):
        """

        """
        workflowschema_db_list = []
        used_flag_set = []
        used_flag_reset = []
        for workflowschema_detail in workflowschema_data['data']:
            # if entry is not exists in db

            if not django_query_instance.django_existence_check(WorkflowSchema,
                                                                {'workflow_schema': workflowschema_detail[
                                                                    'workflow_schema'],
                                                                 'company_id': workflowschema_detail['company_id'],
                                                                 'client': self.client
                                                                 }):
                guid = guid_generator()
                workflowschema_db_dictionary = {'workflow_schema_guid': guid,
                                                'workflow_schema': (
                                                    workflowschema_detail['workflow_schema']).upper(),
                                                'app_types': ApproverType.objects.get(
                                                    app_types=workflowschema_detail['app_types']),
                                                'company_id': workflowschema_detail['company_id'],
                                                'workflow_schema_created_at': self.current_date_time,
                                                'workflow_schema_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                'workflow_schema_changed_at': self.current_date_time,
                                                'workflow_schema_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                'client': self.client}
                workflowschema_db_list.append(workflowschema_db_dictionary)
            else:
                django_query_instance.django_update_query(WorkflowSchema,
                                                          {'workflow_schema': workflowschema_detail[
                                                              'workflow_schema'],
                                                           'company_id': workflowschema_detail['company_id'],
                                                           'client': self.client},
                                                          {'workflow_schema': (
                                                              workflowschema_detail['workflow_schema']).upper(),
                                                           'app_types': ApproverType.objects.get(
                                                               app_types=workflowschema_detail['app_types']),
                                                           'company_id': workflowschema_detail['company_id'],
                                                           'workflow_schema_changed_at': self.current_date_time,
                                                           'workflow_schema_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'client': self.client,
                                                           'del_ind': workflowschema_detail['del_ind']})
            if workflowschema_detail['del_ind']:
                used_flag_reset.append(workflowschema_detail['workflow_schema'])
            else:
                used_flag_set.append(workflowschema_detail['workflow_schema'])
        if workflowschema_db_list:
            bulk_create_entry_db(WorkflowSchema, workflowschema_db_list)
        set_reset_field(used_flag_reset, used_flag_set, 'workflow_schema')

    def save_work_flow_schema_data_into_db(self, workflowschema_data):

        self.save_workflow_schema(workflowschema_data)

        message = get_message_detail_based_on_action(workflowschema_data['action'])
        upload_response = get_workflowschema_data()
        data = get_workflowschema_drop_down()

        return upload_response, message, data

    def save_spend_limit(self, spendlimit_data):
        """

        """
        spendlimit_db_list = []

        for spendlimit_detail in spendlimit_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(SpendLimitId,
                                                                {'spender_username': spendlimit_detail[
                                                                    'spender_username'],
                                                                 'company_id': spendlimit_detail['company_id'],
                                                                 'client': self.client}):
                guid = guid_generator()
                spendlimit_db_dictionary = {'spend_guid': guid,
                                            'spend_code_id': spendlimit_detail['spend_code_id'],
                                            'spender_username': (spendlimit_detail['spender_username']).upper(),
                                            'company_id': spendlimit_detail['company_id'],
                                            'spend_limit_id_created_at': self.current_date_time,
                                            'spend_limit_id_created_by': self.username,
                                            'spend_limit_id_changed_at': self.current_date_time,
                                            'spend_limit_id_changed_by': self.username,
                                            'client': OrgClients.objects.get(client=self.client),
                                            }
                spendlimit_db_list.append(spendlimit_db_dictionary)
            else:
                django_query_instance.django_update_query(SpendLimitId,
                                                          {'spender_username': spendlimit_detail['spender_username'],
                                                           'company_id': spendlimit_detail['company_id'],
                                                           'client': self.client},
                                                          {'spend_code_id': spendlimit_detail['spend_code_id'],
                                                           'spender_username': (
                                                               spendlimit_detail['spender_username']).upper(),
                                                           'company_id': spendlimit_detail['company_id'],
                                                           'spend_limit_id_changed_at': self.current_date_time,
                                                           'spend_limit_id_changed_by': self.username,
                                                           'client': OrgClients.objects.get(client=self.client),
                                                           'del_ind': spendlimit_detail['del_ind']})

        if spendlimit_db_list:
            bulk_create_entry_db(SpendLimitId, spendlimit_db_list)

    def save_spend_limit_data_into_db(self, spendlimit_data):
        self.save_spend_limit(spendlimit_data)

        message = get_message_detail_based_on_action(spendlimit_data['action'])
        upload_response = get_spendlimitid_data()
        data = get_spendlimitid_dropdown()

        return upload_response, message, data

    def save_org_addr_map(self, addresstype_data):
        """

        """

        addresstype_db_list = []
        for addresstype_detail in addresstype_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(OrgAddressMap,
                                                                {'address_number': addresstype_detail[
                                                                    'address_number'],
                                                                 'address_type': addresstype_detail[
                                                                     'address_type'],
                                                                 'company_id': addresstype_detail['company_id'],
                                                                 'client': self.client}):
                guid = guid_generator()
                addresstype_db_dictionary = {'address_guid': guid,
                                             'address_number': addresstype_detail['address_number'],
                                             'address_type': (addresstype_detail['address_type']).upper(),
                                             'company_id': addresstype_detail['company_id'],
                                             'valid_from': datetime.strptime(addresstype_detail['valid_from'],
                                                                             "%d-%m-%Y"),
                                             'valid_to': datetime.strptime(addresstype_detail['valid_to'], "%d-%m-%Y"),
                                             'org_address_map_created_at': self.current_date_time,
                                             'org_address_map_created_by': self.username,
                                             'org_address_map_changed_at': self.current_date_time,
                                             'org_address_map_changed_by': self.username,
                                             'client': OrgClients.objects.get(client=self.client),
                                             }
                addresstype_db_list.append(addresstype_db_dictionary)
            else:
                django_query_instance.django_update_query(OrgAddressMap,
                                                          {'address_number': addresstype_detail[
                                                              'address_number'],
                                                           'address_type': addresstype_detail[
                                                               'address_type'],
                                                           'client': self.client,
                                                           'company_id': addresstype_detail['company_id']},
                                                          {'address_number': addresstype_detail['address_number'],
                                                           'address_type': (
                                                               addresstype_detail['address_type']).upper(),
                                                           'company_id': addresstype_detail['company_id'],
                                                           'valid_from': datetime.strptime(
                                                               addresstype_detail['valid_from'], "%d-%m-%Y"),
                                                           'valid_to': datetime.strptime(addresstype_detail['valid_to'],
                                                                                         "%d-%m-%Y"),
                                                           'org_address_map_changed_at': self.current_date_time,
                                                           'org_address_map_changed_by': self.username,
                                                           'client': OrgClients.objects.get(client=self.client),
                                                           'del_ind': addresstype_detail['del_ind']})
        if addresstype_db_list:
            bulk_create_entry_db(OrgAddressMap, addresstype_db_list)

    def save_address_type_data_into_db(self, addresstype_data):
        self.save_org_addr_map(addresstype_data)
        message = get_message_detail_based_on_action(addresstype_data['action'])

        upload_response = get_orgaddtype_data()

        data = get_orgaddtype_dropdown()

        return upload_response, message, data

    def save_al_acc_data(self, glaccount_data):
        glaccount_db_list = []
        for glaccount_detail in glaccount_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(DetermineGLAccount,
                                                                {'prod_cat_id': glaccount_detail['prod_cat_id'],
                                                                 'gl_acc_num': glaccount_detail['gl_acc_num'],
                                                                 'gl_acc_default': glaccount_detail['gl_acc_default'],
                                                                 'account_assign_cat': glaccount_detail[
                                                                     'account_assign_cat'],
                                                                 'company_id': glaccount_detail['company_id'],
                                                                 'item_from_value': glaccount_detail['item_from_value'],
                                                                 'item_to_value': glaccount_detail['item_to_value'],
                                                                 'currency_id': glaccount_detail['currency_id'],
                                                                 'client': self.client}):
                guid = guid_generator()
                glaccount_db_dictionary = {'det_gl_acc_guid': guid,
                                           'prod_cat_id': glaccount_detail['prod_cat_id'],
                                           'gl_acc_num': glaccount_detail['gl_acc_num'],
                                           'gl_acc_default': glaccount_detail['gl_acc_default'],
                                           'account_assign_cat': AccountAssignmentCategory.objects.
                                           get(account_assign_cat=glaccount_detail['account_assign_cat']),
                                           'company_id': glaccount_detail['company_id'],
                                           'item_from_value': glaccount_detail['item_from_value'],
                                           'item_to_value': glaccount_detail['item_to_value'],
                                           'currency_id': Currency.objects.
                                           get(currency_id=glaccount_detail['currency_id']),
                                           'determine_gl_account_created_at': self.current_date_time,
                                           'determine_gl_account_created_by': self.username,
                                           'determine_gl_account_changed_at': self.current_date_time,
                                           'determine_gl_account_changed_by': self.username,
                                           'client': OrgClients.objects.get(client=self.client),
                                           }
                glaccount_db_list.append(glaccount_db_dictionary)
            else:
                django_query_instance.django_update_query(DetermineGLAccount,
                                                          {'prod_cat_id': glaccount_detail['prod_cat_id'],
                                                           'gl_acc_num': glaccount_detail['gl_acc_num'],
                                                           'gl_acc_default': glaccount_detail['gl_acc_default'],
                                                           'account_assign_cat': glaccount_detail[
                                                               'account_assign_cat'],
                                                           'company_id': glaccount_detail['company_id'],
                                                           'item_from_value': glaccount_detail['item_from_value'],
                                                           'item_to_value': glaccount_detail['item_to_value'],
                                                           'currency_id': glaccount_detail['currency_id'],
                                                           'client': self.client},
                                                          {'del_ind': glaccount_detail['del_ind']})
        if glaccount_db_list:
            bulk_create_entry_db(DetermineGLAccount, glaccount_db_list)

    def save_glaccount_data_into_db(self, glaccount_data):
        self.save_al_acc_data(glaccount_data)

        message = get_message_detail_based_on_action(glaccount_data['action'])

        upload_response = get_gl_acc_data()

        data = get_gl_acc_dropdown()

        return upload_response, message, data

    def accounting_data(self, aav_data):
        aav_db_list = []
        for aav_detail in aav_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(AccountingData,
                                                                {'account_assign_value': aav_detail[
                                                                    'account_assign_value'],
                                                                 'account_assign_cat': aav_detail[
                                                                     'account_assign_cat'],
                                                                 'company_id': aav_detail['company_id'],
                                                                 'client': self.client}):
                guid = guid_generator()
                aav_db_dictionary = {'account_assign_guid': guid,
                                     'account_assign_value': aav_detail['account_assign_value'],
                                     'account_assign_cat': AccountAssignmentCategory.objects.get(
                                         account_assign_cat=aav_detail['account_assign_cat']),
                                     'valid_from': datetime.strptime(aav_detail['valid_from'], "%d-%m-%Y"),
                                     'valid_to': datetime.strptime(aav_detail['valid_to'], "%d-%m-%Y"),
                                     'company_id': aav_detail['company_id'],
                                     'del_ind': False,
                                     'client': self.client,
                                     'accounting_data_changed_at': self.current_date_time,
                                     'accounting_data_changed_by': self.username,
                                     'accounting_data_created_at': self.current_date_time,
                                     'accounting_data_created_by': self.username,
                                     }

                aav_db_list.append(aav_db_dictionary)

            else:

                django_query_instance.django_update_query(AccountingData,
                                                          {'account_assign_value': aav_detail[
                                                              'account_assign_value'],
                                                           'account_assign_cat': aav_detail['account_assign_cat'],
                                                           'company_id': aav_detail['company_id'],
                                                           'client': self.client},
                                                          {'account_assign_value': aav_detail[
                                                              'account_assign_value'],
                                                           'account_assign_cat': aav_detail['account_assign_cat'],
                                                           'valid_from': datetime.strptime(aav_detail['valid_from'],
                                                                                           "%d-%m-%Y"),
                                                           'valid_to': datetime.strptime(aav_detail['valid_to'],
                                                                                         "%d-%m-%Y"),
                                                           'company_id': aav_detail['company_id'],
                                                           'accounting_data_changed_at': self.current_date_time,
                                                           'accounting_data_changed_by': self.username,
                                                           'client': self.client,
                                                           'del_ind': aav_detail['del_ind']})
        if aav_db_list:
            bulk_create_entry_db(AccountingData, aav_db_list)

    def save_aav_data_into_db(self, aav_data):
        """

        """
        self.accounting_data(aav_data)
        message = get_message_detail_based_on_action(aav_data['action'])
        upload_response = get_account_assignment_value()
        data = get_acc_value_dropdown()
        return upload_response, message, data

    def app_limit_data(self, applim_data):
        applim_db_list = []

        for applim_detail in applim_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(ApproverLimit,
                                                                {'approver_username': applim_detail[
                                                                    'approver_username'],
                                                                 'company_id': applim_detail['company_id'],
                                                                 'client': self.client}):
                guid = guid_generator()
                applim_db_dictionary = {'app_guid': guid,
                                        'approver_username': applim_detail['approver_username'],
                                        'app_code_id': applim_detail['app_code_id'],
                                        'company_id': applim_detail['company_id'],
                                        'del_ind': False,
                                        'client': self.client,
                                        'approver_limit_changed_at': self.current_date_time,
                                        'approver_limit_changed_by': self.username,
                                        'approver_limit_created_at': self.current_date_time,
                                        'approver_limit_created_by': self.username,
                                        }
                applim_db_list.append(applim_db_dictionary)

            else:
                django_query_instance.django_update_query(ApproverLimit,
                                                          {'approver_username': applim_detail['approver_username'],
                                                           'company_id': applim_detail['company_id'],
                                                           'client': self.client},
                                                          {'approver_username': applim_detail['approver_username'],
                                                           'app_code_id': applim_detail['app_code_id'],
                                                           'company_id': applim_detail['company_id'],
                                                           'approver_limit_changed_at': self.current_date_time,
                                                           'approver_limit_changed_by': self.username,
                                                           'client': self.client,
                                                           'del_ind': applim_detail['del_ind']})

        if applim_db_list:
            bulk_create_entry_db(ApproverLimit, applim_db_list)

    def save_app_limit_data_into_db(self, applim_data):
        self.app_limit_data(applim_data)
        message = get_message_detail_based_on_action(applim_data['action'])

        upload_response = get_approverid_data()
        data = get_approverid_dropdown()

        return upload_response, message, data

    def save_app_limit_value_data(self, applimval_data):
        applimval_db_list = []
        delete_app_code_ids = []

        for applimval_detail in applimval_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(ApproverLimitValue,
                                                                {'app_code_id': applimval_detail['app_code_id'],
                                                                 'company_id': applimval_detail['company_id'],
                                                                 'app_types': applimval_detail['app_types'],
                                                                 'currency_id': applimval_detail['currency_id'],
                                                                 'client': self.client}):
                guid = guid_generator()
                applimval_db_dictionary = {'app_lim_dec_guid': guid,
                                           'app_types': ApproverType.objects.get(
                                               app_types=applimval_detail['app_types']),
                                           'app_code_id': applimval_detail['app_code_id'],
                                           'upper_limit_value': applimval_detail['upper_limit_value'],
                                           'company_id': applimval_detail['company_id'],
                                           'currency_id': Currency.objects.get(
                                               currency_id=applimval_detail['currency_id']),
                                           'del_ind': False,
                                           'client': self.client,
                                           'approver_limit_value_changed_at': self.current_date_time,
                                           'approver_limit_value_changed_by': self.username,
                                           'approver_limit_value_created_at': self.current_date_time,
                                           'approver_limit_value_created_by': self.username,
                                           }

                applimval_db_list.append(applimval_db_dictionary)

            else:
                if applimval_detail['del_ind']:
                    delete_app_code_ids.extend([applimval_detail['company_id'],
                                                applimval_detail['app_code_id']])

                django_query_instance.django_update_query(ApproverLimitValue,
                                                          {'app_code_id': applimval_detail['app_code_id'],
                                                           'company_id': applimval_detail['company_id'],
                                                           'app_types': applimval_detail['app_types'],
                                                           'currency_id': applimval_detail['currency_id'],
                                                           'client': self.client},
                                                          {
                                                              'app_types': applimval_detail['app_types'],
                                                              'app_code_id': applimval_detail['app_code_id'],
                                                              'upper_limit_value': applimval_detail[
                                                                  'upper_limit_value'],
                                                              'company_id': applimval_detail['company_id'],
                                                              'currency_id': applimval_detail['currency_id'],
                                                              'client': self.client,
                                                              'del_ind': applimval_detail['del_ind'],
                                                              'approver_limit_value_changed_at': self.current_date_time,
                                                              'approver_limit_value_changed_by': self.username,
                                                          })

        if delete_app_code_ids:
            ApproverLimit.objects.filter(company_id__in=delete_app_code_ids,
                                         app_code_id__in=delete_app_code_ids).delete()

            ApproverLimitValue.objects.filter(company_id__in=delete_app_code_ids,
                                              app_code_id__in=delete_app_code_ids).delete()

        if applimval_db_list:
            bulk_create_entry_db(ApproverLimitValue, applimval_db_list)

    def save_app_limit_value_data_into_db(self, applimval_data):
        self.save_app_limit_value_data(applimval_data)

        message = get_message_detail_based_on_action(applimval_data['action'])
        upload_response = get_approvervalue_data()
        data = get_approvervalue_dropdown()

        return upload_response, message, data

    def save_spending_limit_value_data(self, spend_limit_value_data):
        spend_limit_value_db_list = []
        delete_spend_code_ids = []

        for spend_limit_value_detail in spend_limit_value_data['data']:
            # Check if entry exists in SpendLimitValue table
            if not django_query_instance.django_existence_check(SpendLimitValue,
                                                                {'spend_code_id': spend_limit_value_detail[
                                                                    'spend_code_id'],
                                                                 'company_id': spend_limit_value_detail['company_id'],
                                                                 'currency_id': spend_limit_value_detail['currency_id'],
                                                                 'client': self.client}):
                # Entry does not exist, create a new entry
                guid = guid_generator()
                spend_limit_value_db_dictionary = {
                    'spend_lim_value_guid': guid,
                    'spend_code_id': spend_limit_value_detail['spend_code_id'].upper(),
                    'upper_limit_value': spend_limit_value_detail['upper_limit_value'],
                    'company_id': OrgCompanies.objects.get(company_id=spend_limit_value_detail['company_id']),
                    'currency_id': Currency.objects.get(currency_id=spend_limit_value_detail['currency_id']),
                    'del_ind': False,
                    'client': self.client,
                    'spend_limit_value_created_at': self.current_date_time,
                    'spend_limit_value_created_by': self.username,
                    'spend_limit_value_changed_at': self.current_date_time,
                    'spend_limit_value_changed_by': self.username
                }
                spend_limit_value_db_list.append(spend_limit_value_db_dictionary)
            else:
                # Entry exists, update the existing entry
                if spend_limit_value_detail['del_ind']:
                    delete_spend_code_ids.extend([spend_limit_value_detail['company_id'],
                                                  spend_limit_value_detail['spend_code_id']])

                django_query_instance.django_update_query(SpendLimitValue,
                                                          {'spend_code_id': spend_limit_value_detail['spend_code_id'],
                                                           'company_id': spend_limit_value_detail['company_id'],
                                                           'currency_id': spend_limit_value_detail['currency_id'],
                                                           'client': self.client},
                                                          {'spend_code_id': spend_limit_value_detail['spend_code_id'],
                                                           'upper_limit_value': spend_limit_value_detail[
                                                               'upper_limit_value'],
                                                           'company_id': spend_limit_value_detail['company_id'],
                                                           'currency_id': spend_limit_value_detail['currency_id'],
                                                           'client': self.client,
                                                           'spend_limit_value_changed_at': self.current_date_time,
                                                           'spend_limit_value_changed_by': self.username,
                                                           'del_ind': spend_limit_value_detail['del_ind']})

        # Delete entries from SpendLimitValue and SpendLimitId tables
        if delete_spend_code_ids:
            # Delete corresponding records in SpendLimitId table
            # for delete_data in delete_spend_code_ids:
            # SpendLimitId.objects.filter(company_id=delete_data).delete()
            SpendLimitId.objects.filter(company_id__in=delete_spend_code_ids,
                                        spend_code_id__in=delete_spend_code_ids).delete()

            # Delete entries from SpendLimitValue table
            SpendLimitValue.objects.filter(company_id__in=delete_spend_code_ids,
                                           spend_code_id__in=delete_spend_code_ids).delete()

        if spend_limit_value_db_list:
            bulk_create_entry_db(SpendLimitValue, spend_limit_value_db_list)

    def save_spend_limit_value_data_into_db(self, spend_limit_value_data):
        """

            """
        self.save_spending_limit_value_data(spend_limit_value_data)
        message = get_message_detail_based_on_action(spend_limit_value_data['action'])

        upload_response = get_spendlimitvalue_data()
        data = get_spendlimitvalue_dropdown()
        return upload_response, message, data

    def save_address_data(self, address_data):
        address_db_list = []
        for address_detail in address_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(OrgAddress,
                                                                {'address_number': address_detail['address_number'],
                                                                 'client': self.client}):
                guid = guid_generator()
                address_db_dictionary = {'address_guid': guid,
                                         'address_number': address_detail['address_number'],
                                         'title': convert_to_camel_case_v2(address_detail['title']),
                                         'name1': convert_to_camel_case_v2(address_detail['name1']),
                                         'name2': convert_to_camel_case_v2(address_detail['name2']),
                                         'street': convert_to_camel_case_v2(address_detail['street']),
                                         'area': convert_to_camel_case_v2(address_detail['area']),
                                         'landmark': convert_to_camel_case_v2(address_detail['landmark']),
                                         'city': convert_to_camel_case_v2(address_detail['city']),
                                         'address_partner_type': AddressPartnerType.objects.get(
                                             address_partner_type=address_detail['address_partner_type']),
                                         'org_address_source_system': convert_to_camel_case_v2
                                         (address_detail['org_address_source_system']),
                                         'postal_code': address_detail['postal_code'],
                                         'region': convert_to_camel_case_v2(address_detail['region']),
                                         'mobile_number': address_detail['mobile_number'],
                                         'telephone_number': address_detail['telephone_number'],
                                         'fax_number': address_detail['fax_number'],
                                         'email': address_detail['email'],
                                         'country_code': Country.objects.get(
                                             country_code=address_detail['country_code']),
                                         'language_id': Languages.objects.get(
                                             language_id=address_detail['language_id']),
                                         'time_zone': TimeZone.objects.get(time_zone=address_detail['time_zone']),

                                         'del_ind': False,
                                         'client': OrgClients.objects.get(client=self.client),
                                         'org_address_changed_at': self.current_date_time,
                                         'org_address_changed_by': self.username,
                                         'org_address_created_at': self.current_date_time,
                                         'org_address_created_by': self.username,
                                         }
                address_db_list.append(address_db_dictionary)
            else:
                if address_detail['del_ind'] == 1:
                    django_query_instance.django_update_query(OrgAddress,
                                                              {'address_number': address_detail['address_number'],
                                                               'client': self.client},
                                                              {'address_number': address_detail['address_number'],
                                                               'org_address_changed_at': self.current_date_time,
                                                               'org_address_changed_by': self.username,
                                                               'client': self.client,
                                                               'del_ind': address_detail['del_ind']})
                else:
                    django_query_instance.django_update_query(OrgAddress,
                                                              {'address_number': address_detail['address_number'],
                                                               'client': self.client},
                                                              {'address_number': address_detail['address_number'],
                                                               'title': address_detail['title'],
                                                               'name1': convert_to_camel_case_v2(address_detail['name1']),
                                                               'name2': convert_to_camel_case_v2(address_detail['name2']),
                                                               'street': convert_to_camel_case_v2(
                                                                   address_detail['street']),
                                                               'area': convert_to_camel_case_v2(address_detail['area']),
                                                               'landmark': convert_to_camel_case_v2(
                                                                   address_detail['landmark']),
                                                               'city': convert_to_camel_case_v2(address_detail['city']),
                                                               'address_partner_type': AddressPartnerType.objects.get
                                                               (address_partner_type=address_detail[
                                                                   'address_partner_type']),
                                                               'org_address_source_system': convert_to_camel_case_v2
                                                               (address_detail['org_address_source_system']),
                                                               'postal_code': address_detail['postal_code'],
                                                               'region': convert_to_camel_case_v2(
                                                                   address_detail['region']),
                                                               'mobile_number': address_detail['mobile_number'],
                                                               'telephone_number': address_detail['telephone_number'],
                                                               'fax_number': address_detail['fax_number'],
                                                               'email': address_detail['email'],
                                                               'country_code': Country.objects.get(
                                                                   country_code=address_detail['country_code']),
                                                               'language_id': Languages.objects.get(
                                                                   language_id=address_detail['language_id']),
                                                               'time_zone': TimeZone.objects.get(
                                                                   time_zone=address_detail['time_zone']),
                                                               'org_address_changed_at': self.current_date_time,
                                                               'org_address_changed_by': self.username,
                                                               'client': self.client,
                                                               'del_ind': address_detail['del_ind'] == 'True', })
        if address_db_list:
            bulk_create_entry_db(OrgAddress, address_db_list)

    def save_address_data_into_db(self, address_data):
        self.save_address_data(address_data)
        message = get_message_detail_based_on_action(address_data['action'])

        upload_response = get_orgaddress_data()
        return upload_response, message

    def save_approval_data(self, approval_data):
        approval_db_list = []
        used_flag_set = []
        used_flag_reset = []
        for approval_detail in approval_data['data']:
            appr_type_field = approval_detail['app_types']
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(ApproverType,
                                                                {'app_types': approval_detail[
                                                                    'app_types'],
                                                                 # 'client': self.client
                                                                 }):
                approval_db_dictionary = {'app_types': (approval_detail['app_types']).upper(),
                                          'appr_type_desc': convert_to_camel_case(
                                              approval_detail['appr_type_desc']),
                                          'del_ind': False,
                                          'approver_type_created_at': self.current_date_time,
                                          'approver_type_created_by': self.username,
                                          'approver_type_changed_at': self.current_date_time,
                                          'approver_type_changed_by': self.username
                                          }
                approval_db_list.append(approval_db_dictionary)
            else:
                django_query_instance.django_update_query(ApproverType,
                                                          {'app_types': approval_detail[
                                                              'app_types'],
                                                           # 'client': self.client
                                                           },
                                                          {'app_types': approval_detail[
                                                              'app_types'],
                                                           'appr_type_desc': convert_to_camel_case(
                                                               approval_detail['appr_type_desc']),
                                                           'approver_type_changed_at': self.current_date_time,
                                                           'approver_type_changed_by': self.username,
                                                           'del_ind': approval_detail['del_ind']
                                                           })
            if approval_detail['del_ind']:
                used_flag_reset.append(approval_detail['app_types'])
            else:
                used_flag_set.append(approval_detail['app_types'])
        if approval_db_list:
            bulk_create_entry_db(ApproverType, approval_db_list)

        set_reset_field(used_flag_reset, used_flag_set, 'approval_type')

    def save_approval_data_into_db(self, approval_data):
        """

        """
        self.save_approval_data(approval_data)
        message = get_message_detail_based_on_action(approval_data['action'])
        upload_response = get_approver_type_data()
        data = get_approver_type_drop_down()

        return upload_response, message, data

    def save_field_desc(self, field_desc_data):
        """

        """
        field_desc_list = []
        for field_desc in field_desc_data:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(FieldDesc,
                                                                {'field_name': field_desc['field_name']}):
                field_desc_dictionary = {'field_name': field_desc['field_name'],
                                         'field_desc': field_desc['field_desc'].upper(),
                                         'del_ind': False,
                                         'field_desc_created_by': self.username,
                                         'field_desc_created_at': self.current_date_time,
                                         'field_desc_changed_by': self.username,
                                         'field_desc_changed_at': self.current_date_time,
                                         }
                field_desc_list.append(field_desc_dictionary)

            else:

                django_query_instance.django_update_query(FieldDesc,
                                                          {'field_name': field_desc['field_name']},
                                                          {'field_name': field_desc['field_name'],
                                                           'field_desc': convert_to_camel_case(
                                                               field_desc['field_desc']),
                                                           'field_desc_changed_by': self.username,
                                                           'field_desc_changed_at': self.current_date_time,
                                                           'del_ind': field_desc['del_ind']})
        bulk_create_entry_db(FieldDesc, field_desc_list)

    def save_field_type_desc(self, field_desc_data):
        """

        """
        field_desc_list = []
        for field_desc in field_desc_data:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(FieldTypeDescription,
                                                                {'field_type_id': field_desc['field_type_id'],
                                                                 'field_name': field_desc['field_name'],
                                                                 'client': self.client}):
                field_desc_dictionary = {'field_type_description_guid': guid_generator(),
                                         'field_type_id': field_desc['field_type_id'],
                                         'field_type_desc': convert_to_camel_case(field_desc['field_type_desc']),
                                         'field_name': FieldDesc.objects.get(field_name=field_desc['field_name']),
                                         'used_flag': field_desc['used_flag'],
                                         'del_ind': False,
                                         'client': self.client,
                                         'field_type_desc_created_by': self.username,
                                         'field_type_desc_created_at': self.current_date_time,
                                         'field_type_desc_changed_by': self.username,
                                         'field_type_desc_changed_at': self.current_date_time,
                                         }
                field_desc_list.append(field_desc_dictionary)

            else:

                django_query_instance.django_update_query(FieldTypeDescription,
                                                          {'field_type_id': field_desc['field_type_id'],
                                                           'field_name': field_desc['field_name'],
                                                           'client': self.client},
                                                          {'field_type_id': field_desc['field_type_id'],
                                                           'field_type_desc': convert_to_camel_case(
                                                               field_desc['field_type_desc']),
                                                           'field_name': FieldDesc.objects.get(
                                                               field_name=field_desc['field_name']),
                                                           'used_flag': field_desc['used_flag'],
                                                           'field_type_desc_changed_at': self.current_date_time,
                                                           'field_type_desc_changed_by': self.username,
                                                           'del_ind': field_desc['del_ind'],
                                                           'client': self.client})
        bulk_create_entry_db(FieldTypeDescription, field_desc_list)

    fieldtypedesc_instance = FieldTypeDescriptionUpdate()

    def save_aad_data(self, aad_data):
        aad_db_list = []
        for aad_detail in aad_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(AccountingDataDesc,
                                                                {'account_assign_value': aad_detail[
                                                                    'account_assign_value'],
                                                                 'account_assign_cat': aad_detail[
                                                                     'account_assign_cat'],
                                                                 'company_id': aad_detail['company_id'],
                                                                 'language_id': aad_detail['language_id'],
                                                                 'client': self.client
                                                                 }):
                guid = guid_generator()
                aad_db_dictionary = {'acc_desc_guid': guid,
                                     'account_assign_value': aad_detail['account_assign_value'],
                                     'description': convert_to_camel_case(aad_detail['description']),
                                     'account_assign_cat': AccountAssignmentCategory.objects.get(
                                         account_assign_cat=aad_detail['account_assign_cat']),
                                     'company_id': aad_detail['company_id'],
                                     'language_id': Languages.objects.get(
                                         language_id=aad_detail['language_id']),
                                     'del_ind': False,
                                     'client': self.client,
                                     'accounting_data_desc_changed_at': self.current_date_time,
                                     'accounting_data_desc_changed_by': self.username,
                                     'accounting_data_desc_created_at': self.current_date_time,
                                     'accounting_data_desc_created_by': self.username,
                                     }
                aad_db_list.append(aad_db_dictionary)
            else:
                django_query_instance.django_update_query(AccountingDataDesc,
                                                          {'account_assign_value': aad_detail[
                                                              'account_assign_value'],
                                                           'account_assign_cat': aad_detail['account_assign_cat'],
                                                           'company_id': aad_detail['company_id'],
                                                           'language_id': aad_detail['language_id'],
                                                           'client': self.client},
                                                          {'account_assign_value': aad_detail[
                                                              'account_assign_value'],
                                                           'description': convert_to_camel_case(
                                                               aad_detail['description']),
                                                           'account_assign_cat': aad_detail['account_assign_cat'],
                                                           'company_id': aad_detail['company_id'],
                                                           'language_id': aad_detail['language_id'].upper(),
                                                           'accounting_data_desc_changed_at': self.current_date_time,
                                                           'accounting_data_desc_changed_by': self.username,
                                                           'client': self.client,
                                                           'del_ind': aad_detail['del_ind']})

        if aad_db_list:
            bulk_create_entry_db(AccountingDataDesc, aad_db_list)

    def save_aad_data_into_db(self, aad_data):
        self.save_aad_data(aad_data)
        message = get_message_detail_based_on_action(aad_data['action'])
        upload_response = get_acc_value_desc_data()
        data = get_acc_value_desc_dropdown()
        return upload_response, message, data

    def save_workflow_acc_data(self, wfacc_data):
        wfacc_db_list = []
        for wfacc_detail in wfacc_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(WorkflowACC,
                                                                {
                                                                    'acc_value': wfacc_detail['acc_value'],
                                                                    'company_id': wfacc_detail['company_id'],
                                                                    'app_username': wfacc_detail['app_username'],
                                                                    'sup_company_id': wfacc_detail['sup_company_id'],
                                                                    'sup_acc_value': wfacc_detail['sup_acc_value'],
                                                                    'account_assign_cat': wfacc_detail[
                                                                        'account_assign_cat'],
                                                                    'sup_account_assign_cat': wfacc_detail[
                                                                        'sup_account_assign_cat'],
                                                                    'currency_id': wfacc_detail[
                                                                        'sup_currency_id'],
                                                                    'client': self.client}):
                guid = guid_generator()
                wfacc_db_dictionary = {'workflow_acc_guid': guid,
                                       'acc_value': wfacc_detail['acc_value'],
                                       'company_id': wfacc_detail['company_id'],
                                       'app_username': wfacc_detail['app_username'],
                                       'sup_company_id': wfacc_detail['sup_company_id'],
                                       'sup_acc_value': wfacc_detail['sup_acc_value'],
                                       'account_assign_cat': AccountAssignmentCategory.objects.get
                                       (account_assign_cat=wfacc_detail['account_assign_cat']),
                                       'sup_account_assign_cat': AccountAssignmentCategory.objects.get
                                       (account_assign_cat=wfacc_detail['sup_account_assign_cat']),
                                       'currency_id': Currency.objects.get(
                                           currency_id=wfacc_detail['sup_currency_id']),
                                       'del_ind': False,
                                       'workflow_acc_created_at': self.current_date_time,
                                       'workflow_acc_created_by': self.username,
                                       'workflow_acc_changed_at': self.current_date_time,
                                       'workflow_acc_changed_by': self.username,
                                       'client': self.client,
                                       }
                wfacc_db_list.append(wfacc_db_dictionary)
            else:
                django_query_instance.django_update_query(WorkflowACC,
                                                          {'workflow_acc_guid': wfacc_detail[
                                                              'workflow_acc_guid'],
                                                           'acc_value': wfacc_detail['acc_value'],
                                                           'company_id': wfacc_detail['company_id'],
                                                           'app_username': wfacc_detail['app_username'],
                                                           'sup_company_id': wfacc_detail['sup_company_id'],
                                                           'sup_acc_value': wfacc_detail['sup_acc_value'],
                                                           'account_assign_cat': wfacc_detail[
                                                               'account_assign_cat'],
                                                           'sup_account_assign_cat': wfacc_detail[
                                                               'sup_account_assign_cat'],
                                                           'currency_id': wfacc_detail[
                                                               'sup_currency_id'],
                                                           'client': self.client},
                                                          {'workflow_acc_guid': wfacc_detail[
                                                              'workflow_acc_guid'],
                                                           'acc_value': wfacc_detail['acc_value'],
                                                           'company_id': wfacc_detail['company_id'],
                                                           'app_username': wfacc_detail['app_username'],
                                                           'sup_company_id': wfacc_detail['sup_company_id'],
                                                           'sup_acc_value': wfacc_detail['sup_acc_value'],
                                                           'account_assign_cat': wfacc_detail['account_assign_cat'],
                                                           'sup_account_assign_cat': wfacc_detail[
                                                               'sup_account_assign_cat'],
                                                           'currency_id': wfacc_detail[
                                                               'sup_currency_id'],
                                                           'workflow_acc_changed_at': self.current_date_time,
                                                           'workflow_acc_changed_by': self.username,
                                                           'del_ind': wfacc_detail['del_ind'],
                                                           'client': OrgClients.objects.get(client=self.client),
                                                           })
        if wfacc_db_list:
            bulk_create_entry_db(WorkflowACC, wfacc_db_list)

    def save_workflow_acc_data_into_db(self, wfacc_data):
        """

        """
        self.save_workflow_acc_data(wfacc_data)
        message = get_message_detail_based_on_action(wfacc_data['action'])
        upload_response = get_workflowacc_data()
        data = get_workflowacc_dropdown()
        return upload_response, message, data

    def save_payment_desc(self, payment_desc_data):
        """

        """
        payment_desc_db_list = []

        for payment_desc_detail in payment_desc_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(Payterms_desc,
                                                                {'payment_term_key': payment_desc_detail[
                                                                    'payment_term_key'],
                                                                 'language_id': payment_desc_detail['language_id'],
                                                                 'client': self.client}):
                guid = guid_generator()
                payment_desc_db_dictionary = {'payment_term_guid': guid,
                                              'payment_term_key': payment_desc_detail['payment_term_key'],
                                              'day_limit': payment_desc_detail['day_limit'],
                                              'description': convert_to_camel_case(
                                                  payment_desc_detail['description']),
                                              'language_id': Languages.objects.get(
                                                  language_id=payment_desc_detail['language_id']),
                                              'del_ind': False,
                                              'client': self.client,
                                              'payterms_desc_created_at': self.current_date_time,
                                              'payterms_desc_created_by': self.username,
                                              'payterms_desc_changed_at': self.current_date_time,
                                              'payterms_desc_changed_by': self.username
                                              }
                payment_desc_db_list.append(payment_desc_db_dictionary)
            else:
                django_query_instance.django_update_query(Payterms_desc,
                                                          {'payment_term_key': payment_desc_detail[
                                                              'payment_term_key'],
                                                           'language_id': payment_desc_detail['language_id'],
                                                           'client': self.client},
                                                          {'payment_term_key': payment_desc_detail[
                                                              'payment_term_key'],
                                                           'day_limit': payment_desc_detail['day_limit'],
                                                           'description': convert_to_camel_case(
                                                               payment_desc_detail['description']),
                                                           'language_id': payment_desc_detail['language_id'],
                                                           'payterms_desc_changed_at': self.current_date_time,
                                                           'payterms_desc_changed_by': self.username,
                                                           'del_ind': payment_desc_detail['del_ind'],
                                                           'client': self.client
                                                           })
        if payment_desc_db_list:
            bulk_create_entry_db(Payterms_desc, payment_desc_db_list)

    def save_payment_desc_data_into_db(self, payment_desc_data):
        """

        """
        self.save_payment_desc(payment_desc_data)
        message = get_message_detail_based_on_action(payment_desc_data['action'])

        upload_response = get_paymentdesc_data()
        data = get_paymentdesc_dropdown()
        return upload_response, message, data


def get_unspsc_cat_cust_data():
    """

    """
    upload_cust_prod_catogories = django_query_instance.django_filter_query(UnspscCategoriesCust,
                                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                                             'del_ind': False}, None,
                                                                            ['prod_cat_guid', 'prod_cat_id'])

    product_cat_list = dictionary_key_to_list(upload_cust_prod_catogories, 'prod_cat_id')
    product_cat_list = list(set(product_cat_list))
    prod_cat_desc = django_query_instance.django_filter_query(UnspscCategoriesCustDesc,
                                                              {'prod_cat_id__in': product_cat_list,
                                                               'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT},
                                                              None,
                                                              ['prod_cat_id', 'language_id', 'category_desc'])
    for prod_cat in upload_cust_prod_catogories:
        prod_cat['prod_cat_desc'] = ' '
        for product_cat in prod_cat_desc:
            if prod_cat['prod_cat_id'] == product_cat['prod_cat_id']:
                if product_cat['language_id'] == global_variables.GLOBAL_USER_LANGUAGE.language_id:
                    prod_cat['prod_cat_desc'] = product_cat['category_desc']
                break

    for prod in upload_cust_prod_catogories:
        if prod['prod_cat_desc'] is None:
            prod['prod_cat_desc'] = ' '

        if django_query_instance.django_existence_check(ImagesUpload, {'client': global_variables.GLOBAL_CLIENT,
                                                                       'image_default': True,
                                                                       'image_id': prod['prod_cat_id'],
                                                                       'image_type': CONST_UNSPSC_IMAGE_TYPE,
                                                                       'del_ind': False}):
            prod['image_url'] = django_query_instance.django_filter_value_list_ordered_by_distinct_query(ImagesUpload, {
                'client': global_variables.GLOBAL_CLIENT, 'image_default': True, 'image_id': prod['prod_cat_id'],
                'image_type': CONST_UNSPSC_IMAGE_TYPE, 'del_ind': False
            }, 'image_url', None)[0]

        else:
            prod['image_url'] = ""

    upload_ProdCat = django_query_instance.django_filter_query(UnspscCategoriesCustDesc,
                                                               {'client': global_variables.GLOBAL_CLIENT,
                                                                'del_ind': False,
                                                                'language_id': CONST_DEFAULT_LANGUAGE,
                                                                },
                                                               ['prod_cat_id'], ['prod_cat_id', 'category_desc'])

    data = {'upload_ProdCat': upload_ProdCat}

    return upload_cust_prod_catogories, product_cat_list, data


def get_unspsc_drop_down():
    """

    """
    upload_ProdCat = django_query_instance.django_filter_query(UnspscCategoriesCustDesc,
                                                               {'client': global_variables.GLOBAL_CLIENT,
                                                                'del_ind': False,
                                                                'language_id': CONST_DEFAULT_LANGUAGE,
                                                                },
                                                               ['prod_cat_id'], ['prod_cat_id', 'category_desc'])

    data = {'upload_ProdCat': upload_ProdCat}
    return data


def get_unspsc_cat_custdesc_data():
    """

    """
    upload_cust_prod_desc_catogories = django_query_instance.django_filter_query(UnspscCategoriesCustDesc,
                                                                                 {
                                                                                     'client': global_variables.GLOBAL_CLIENT,
                                                                                     'del_ind': False},
                                                                                 None,
                                                                                 ['prod_cat_desc_guid', 'prod_cat_id',
                                                                                  'category_desc', 'language_id'])
    product_cat_list = dictionary_key_to_list(upload_cust_prod_desc_catogories, 'prod_cat_id')
    product_cat_list = list(set(product_cat_list))
    upload_cust_prod_desc_catogories = replace_none_with_empty_string(upload_cust_prod_desc_catogories)

    for prod in upload_cust_prod_desc_catogories:
        if prod['category_desc'] is None:
            prod['prod_cat_desc'] = ''
        else:
            prod['prod_cat_desc'] = prod['category_desc']

    upload_ProdCat = list(UnspscCategories.objects.filter(del_ind=False).values('prod_cat_id', 'prod_cat_desc'))
    upload_ProdCat = replace_none_with_empty_string(upload_ProdCat)
    for prod_cat_desc in upload_ProdCat:
        if prod_cat_desc['prod_cat_desc'] == None:
            prod_cat_desc['prod_cat_desc'] = ''

    upload_ProdCat = django_query_instance.django_filter_query(UnspscCategoriesCustDesc,
                                                               {'client': global_variables.GLOBAL_CLIENT,
                                                                'del_ind': False,
                                                                'language_id': CONST_DEFAULT_LANGUAGE,
                                                                },
                                                               ['prod_cat_id'], ['prod_cat_id', 'category_desc'])

    data = {'upload_ProdCat': upload_ProdCat}

    return upload_cust_prod_desc_catogories, product_cat_list, data


def get_unspscdesc_drop_down():
    """

    """
    upload_ProdCat = django_query_instance.django_filter_query(UnspscCategories, {'del_ind': False},
                                                               ['prod_cat_id'], ['prod_cat_id', 'prod_cat_desc'])

    for prod_cat_desc in upload_ProdCat:
        if not prod_cat_desc['prod_cat_desc']:
            prod_cat_desc['prod_cat_desc'] = ''

    upload_language = list(Languages.objects.filter(del_ind=False).values('language_id', 'description'))
    data = {'upload_ProdCat': upload_ProdCat,
            'upload_language': upload_language}

    return data


def get_org_companies_data():
    """

    """
    upload_orgcompany = django_query_instance.django_filter_query(OrgCompanies,
                                                                  {'client': global_variables.GLOBAL_CLIENT,
                                                                   'del_ind': False},
                                                                  ['company_id'],
                                                                  ['company_guid', 'object_id', 'name1', 'name2',
                                                                   'company_id'])
    for company_id_fd in upload_orgcompany:
        if django_query_instance.django_existence_check(OrgPorg,
                                                        {'del_ind': False,
                                                         'company_id': company_id_fd['company_id']}):
            company_id_fd["del_ind_flag"] = False
        else:
            company_id_fd["del_ind_flag"] = True

        if company_id_fd['object_id'] is None:
            company_id_fd['object_id'] = ''
    return upload_orgcompany


def get_org_porg_data():
    upload_porg = django_query_instance.django_filter_query(OrgPorg,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'del_ind': False},
                                                            ['company_id'],
                                                            ['porg_guid', 'porg_id', 'object_id', 'description',
                                                             'company_id'])
    for object_id in upload_porg:
        if object_id['object_id'] is None:
            object_id['object_id'] = ''
    return upload_porg


def get_orgpgroup_data():
    upload_pgrp = django_query_instance.django_filter_query(OrgPGroup,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'del_ind': False}, None,
                                                            ['pgroup_guid', 'pgroup_id', 'object_id',
                                                             'description'])

    for object_id in upload_pgrp:
        if object_id['object_id'] is None:
            object_id['object_id'] = ''

    return upload_pgrp


def get_account_assignment_value():
    """

    """
    upload_data_accounting = django_query_instance.django_filter_query(AccountingData,
                                                                       {'client': global_variables.GLOBAL_CLIENT,
                                                                        'del_ind': False},
                                                                       ['account_assign_value', 'account_assign_cat',
                                                                        'company_id'],
                                                                       ['account_assign_guid', 'account_assign_value',
                                                                        'valid_from', 'valid_to', 'account_assign_cat',
                                                                        'company_id'])

    for data in upload_data_accounting:
        if django_query_instance.django_existence_check(AccountingDataDesc,
                                                        {'del_ind': False,
                                                         'account_assign_value': data[
                                                             'account_assign_value']}):
            data["del_ind_flag"] = False
        else:
            data["del_ind_flag"] = True
        # data["valid_from"] = data["valid_from"].strftime("%Y-%m-%d")
        # data["valid_to"] = data["valid_to"].strftime("%Y-%m-%d")

    return upload_data_accounting


def get_acc_value_dropdown():
    """

    """
    upload_data_company = list(
        OrgCompanies.objects.filter(del_ind=False).values('company_id'))

    upload_data_acccat = list(
        AccountAssignmentCategory.objects.filter(del_ind=False).values('account_assign_cat'))
    data = {'upload_company_data': upload_data_company,
            'upload_data_acccat': upload_data_acccat}
    return data


def get_acc_value_desc_dropdown():
    """

    """

    prod_catogories = list(
        UnspscCategoriesCust.objects.filter(client=client, del_ind=False).values('prod_cat_id'))
    upload_accassvalues = django_query_instance.django_filter_query(AccountingData,
                                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                                     'del_ind': False
                                                                     }, None,
                                                                    ['account_assign_value', 'account_assign_cat',
                                                                     'company_id', 'valid_from', 'valid_to'])

    upload_data_acccat = list(
        AccountAssignmentCategory.objects.filter(del_ind=False).values('account_assign_cat'))
    upload_data_company = list(
        OrgCompanies.objects.filter(del_ind=False).values('company_id'))
    upload_data_language = django_query_instance.django_filter_query(Languages, {'del_ind': False}, None,
                                                                     ['language_id', 'description'])

    data = {'prod_catogories': prod_catogories,
            'upload_accassvalues': upload_accassvalues,
            'upload_data_acccat': upload_data_acccat,
            'upload_data_company': upload_data_company,
            'upload_data_language': upload_data_language
            }

    return data


def get_acc_value_desc_data():
    """

    """
    upload_accassignment = django_query_instance.django_filter_query(AccountingDataDesc,
                                                                     {'client': global_variables.GLOBAL_CLIENT,
                                                                      'del_ind': False}, None,
                                                                     ['acc_desc_guid', 'account_assign_value',
                                                                      'description', 'account_assign_cat',
                                                                      'company_id', 'language_id'])

    return upload_accassignment


def get_gl_acc_dropdown():
    datetime_datetime_object = ''
    today_date = datetime.today().strftime('%Y-%m-%d')
    prod_catogories = list(
        UnspscCategoriesCust.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('prod_cat_id'))
    upload_value_glacc = list(AccountingData.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                                            del_ind=False,
                                                            account_assign_cat='GLACC').values('account_assign_value',
                                                                                               'company_id',
                                                                                               'account_assign_cat'))
    gl_acc_details = django_query_instance.django_filter_query(AccountingData,
                                                               {'client': global_variables.GLOBAL_CLIENT,
                                                                'del_ind': False,
                                                                'account_assign_cat': CONST_GLACC,
                                                                'valid_from__lte': str(today_date),
                                                                'valid_to__gte': str(today_date)},
                                                               ['company_id'],
                                                               ['account_assign_value',
                                                                'company_id',
                                                                'valid_from',
                                                                'valid_to'])
    filter_queue = ~Q(account_assign_cat=CONST_GLACC)

    acc_details = django_query_instance.django_queue_query(AccountingData,
                                                           {'client': global_variables.GLOBAL_CLIENT,
                                                            'del_ind': False,
                                                            'valid_from__lte': str(today_date),
                                                            'valid_to__gte': str(today_date)},
                                                           filter_queue,
                                                           ['company_id'],
                                                           ['account_assign_cat',
                                                            'company_id',
                                                            'valid_from',
                                                            'valid_to',
                                                            'account_assign_value'])

    company_id_list = django_query_instance.django_filter_value_list_ordered_by_distinct_query(AccountingData,
                                                                                               {
                                                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                                                   'del_ind': False},
                                                                                               'company_id',
                                                                                               ['company_id'])
    acc_value_list = []
    for company_id in company_id_list:
        account_assign_cat_list = get_acc_list(acc_details, company_id)
        account_assign_cat_value_list = get_acc_asg_cat_value_list(gl_acc_details, company_id)
        if account_assign_cat_list:
            account_assign_cat_list = distinct_list(account_assign_cat_list)
        if account_assign_cat_value_list:
            account_assign_cat_value_list = distinct_list(account_assign_cat_value_list)
        acc_dic = {'company_id': company_id,
                   'account_assign_cat_list': list(account_assign_cat_list),
                   'account_assign_cat_value_list': list(account_assign_cat_value_list)}
        acc_value_list.append(acc_dic)

    upload_value_accasscat = list(
        AccountAssignmentCategory.objects.filter(del_ind=False).values(
            'account_assign_cat'))
    upload_value_currency = list(Currency.objects.filter(del_ind=False).values('currency_id'))
    upload_value_company = list(
        OrgCompanies.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('company_id'))

    data = {
        'upload_value_glacc': upload_value_glacc,
        'upload_value_accasscat': upload_value_accasscat,
        'upload_value_currency': upload_value_currency,
        'upload_value_company': upload_value_company,
        'prod_catogories': prod_catogories,
        'acc_value_list': acc_value_list
    }

    return data


def get_acc_asg_cat_value_list(gl_acc_details, company_id):
    """

    """
    acc_list = []
    for gl_acc_detail in gl_acc_details:
        if gl_acc_detail['company_id'] == company_id:
            acc_list.append(gl_acc_detail['account_assign_value'])
    return acc_list


def get_acc_list(acc_details, company_id):
    """

    """
    acc_list = []
    for acc_detail in acc_details:
        if acc_detail['company_id'] == company_id:
            acc_list.append(acc_detail['account_assign_cat'])
    return acc_list


def get_gl_acc_data():
    upload_gl_acc_db = list(
        DetermineGLAccount.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values(
            'det_gl_acc_guid', 'prod_cat_id',
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
    return upload_gl_acc


def get_workflowschema_drop_down():
    """

    """

    upload_data_company = django_query_instance.django_filter_query(OrgCompanies,
                                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                                     'del_ind': False}, None, ['company_id'])
    upload_data_apptypes = django_query_instance.django_filter_query(ApproverType, {'del_ind': False}, None,
                                                                     ['app_types'])
    dropdown_db_values = get_field_list_values('workflow_schema')
    data = {'upload_data_company': upload_data_company,
            'upload_data_apptypes': upload_data_apptypes,
            'dropdown_db_values': dropdown_db_values,
            }

    return data


def get_workflowschema_data():
    """

    """
    upload_wfschema = django_query_instance.django_filter_query(WorkflowSchema,
                                                                {'client': global_variables.GLOBAL_CLIENT,
                                                                 'del_ind': False}, None,
                                                                ['workflow_schema_guid', 'workflow_schema',
                                                                 'app_types', 'company_id'])
    return upload_wfschema


def get_approver_type_drop_down():
    """

    """
    dropdown_db_values = get_field_unused_list_values('approval_type')
    data = {
        'dropdown_db_values': dropdown_db_values
    }
    return data


def get_approver_type_data():
    """

    """
    upload_apptype = list(ApproverType.objects.filter(del_ind=False).values('app_types', 'appr_type_desc'))

    for app_type_fd in upload_apptype:
        if django_query_instance.django_existence_check(WorkflowSchema,
                                                        {'del_ind': False,
                                                         'app_types': app_type_fd['app_types']}):
            app_type_fd["del_ind_flag"] = False
        else:
            app_type_fd["del_ind_flag"] = True
    return upload_apptype


def get_spendlimitid_dropdown():
    """

    """
    upload_spndlimval = list(
        SpendLimitValue.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values(
            'spend_lim_value_guid', 'spend_code_id',
            'upper_limit_value', 'currency_id',
            'company_id'))
    upload_data_company = list(
        OrgCompanies.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('company_id'))
    user_details = list(
        UserData.objects.filter(is_active=True, client=global_variables.GLOBAL_CLIENT, del_ind=False).values(
            'username'))
    data = {
        'upload_spndlimval': upload_spndlimval,
        'upload_data_company': upload_data_company,
        'user_details': user_details,
    }
    return data


def get_spendlimitvalue_dropdown():
    """

    """
    upload_data_company = list(
        OrgCompanies.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('company_id'))
    upload_data_currency = list(Currency.objects.filter(del_ind=False).values('currency_id'))
    data = {
        'upload_data_company': upload_data_company,
        'upload_data_currency': upload_data_currency,
    }

    return data


def get_spendlimitid_data():
    """

    """
    upload_spndlimid = list(
        SpendLimitId.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('spend_guid',
                                                                                                 'spend_code_id',
                                                                                                 'spender_username',
                                                                                                 'company_id'))
    return upload_spndlimid


def get_spendlimitvalue_data():
    """

     """
    upload_spndlimval = list(
        SpendLimitValue.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values(
            'spend_lim_value_guid', 'spend_code_id',
            'upper_limit_value', 'currency_id',
            'company_id'))
    for spend_code_fd in upload_spndlimval:
        if django_query_instance.django_existence_check(SpendLimitId,
                                                        {'del_ind': False,
                                                         'spend_code_id': spend_code_fd['spend_code_id']}):
            spend_code_fd["del_ind_flag"] = False
        else:
            spend_code_fd["del_ind_flag"] = True

    return upload_spndlimval


def get_approverid_dropdown():
    upload_data_company = list(
        OrgCompanies.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('company_id'))
    upload_data_app_code_id = list(
        ApproverLimitValue.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('app_code_id',
                                                                                                       'company_id'))

    user_details = list(
        UserData.objects.filter(is_active=True, client=global_variables.GLOBAL_CLIENT, del_ind=False).values(
            'username'))
    data = {
        'upload_data_company': upload_data_company,
        'upload_data_app_code_id': upload_data_app_code_id,
        'user_details': user_details,
    }
    return data


def get_approverid_data():
    upload_applimit = list(
        ApproverLimit.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('app_guid',
                                                                                                  'approver_username',
                                                                                                  'app_code_id',
                                                                                                  'company_id'))
    return upload_applimit


def get_approvervalue_dropdown():
    upload_data_apptypes = list(ApproverType.objects.filter(del_ind=False).values('app_types'))
    upload_data_currency = list(Currency.objects.filter(del_ind=False).values('currency_id'))
    upload_data_company = list(
        OrgCompanies.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('company_id'))
    data = {
        'upload_data_apptypes': upload_data_apptypes,
        'upload_data_company': upload_data_company,
        'upload_data_currency': upload_data_currency,
    }

    return data


def get_approvervalue_data():
    upload_applimval = list(
        ApproverLimitValue.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values(
            'app_lim_dec_guid', 'app_types',
            'app_code_id', 'currency_id',
            'upper_limit_value', 'company_id'))
    for app_lmtval_fd in upload_applimval:
        if django_query_instance.django_existence_check(ApproverLimit,
                                                        {'del_ind': False,
                                                         'app_code_id': app_lmtval_fd['app_code_id']}):
            app_lmtval_fd["del_ind_flag"] = False
        else:
            app_lmtval_fd["del_ind_flag"] = True
    return upload_applimval


def get_workflowacc_dropdown():
    upload_data_acccat = list(AccountAssignmentCategory.objects.filter(del_ind=False).values('account_assign_cat'))
    upload_accassvalues = get_configuration_data(AccountingData, {'del_ind': False},
                                                 ['account_assign_value', 'account_assign_cat',
                                                  'company_id', 'valid_from', 'valid_to'])
    upload_data_currency = list(Currency.objects.filter(del_ind=False).values('currency_id'))
    upload_data_company = list(
        OrgCompanies.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('company_id'))
    upload_data_OrgCompanies = list(
        OrgCompanies.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('company_id'))
    user_details = list(
        UserData.objects.filter(is_active=True, client=global_variables.GLOBAL_CLIENT, del_ind=False).values(
            'username'))
    data = {
        'upload_data_acccat': upload_data_acccat,
        'upload_data_currency': upload_data_currency,
        'upload_data_company': upload_data_company,
        'upload_data_OrgCompanies': upload_data_OrgCompanies,
        'user_details': user_details,
        'upload_accassvalues': upload_accassvalues,

    }
    return data


def get_workflowacc_data():
    upload_wfacc = list(
        WorkflowACC.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('workflow_acc_guid',
                                                                                                'app_username',
                                                                                                'acc_value',
                                                                                                'sup_acc_value',
                                                                                                'account_assign_cat',
                                                                                                'sup_account_assign_cat',
                                                                                                'company_id',
                                                                                                'sup_company_id',
                                                                                                'currency_id'))
    return upload_wfacc


def get_orgaddress_dropdown():
    language_list = list(Languages.objects.filter(del_ind=False).values('language_id', 'description'))
    country_list = get_country_data()
    time_zone_data = list(TimeZone.objects.filter(del_ind=False).values('time_zone', 'description'))
    add_partner_type_data = list(AddressPartnerType.objects.filter(del_ind=False).values('address_partner_type',
                                                                                         'address_partner_type_desc'))
    data = {
        'language_list': language_list,
        'country_list': country_list,
        'time_zone_data': time_zone_data,
        'add_partner_type_data': add_partner_type_data,
    }
    return data


def get_orgaddress_data():
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
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'address_number': address_data_fd['address_number'],
                                                             'del_ind': False}):
            address_data_fd["del_ind_flag"] = False
        else:
            address_data_fd["del_ind_flag"] = True
    return address_data


def get_orgaddtype_dropdown():
    dropdown_db_values = get_field_list_values('address_type')
    address_data = list(
        OrgAddress.objects.filter(del_ind=False).values('address_guid', 'address_number', 'title', 'name1', 'name2',
                                                        'street', 'area', 'landmark', 'city', 'postal_code', 'region',
                                                        'mobile_number', 'telephone_number', 'fax_number', 'email',
                                                        'country_code',
                                                        'language_id', 'time_zone'))

    upload_data_OrgCompanies = list(
        OrgCompanies.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('company_id'))

    data = {'dropdown_db_values': dropdown_db_values,
            'address_data': address_data,
            'upload_data_OrgCompanies': upload_data_OrgCompanies}
    return data


def get_orgaddtype_data():
    address_type_data = list(
        OrgAddressMap.objects.filter(del_ind=False).values('address_guid', 'address_number', 'address_type',
                                                           'company_id', 'valid_from', 'valid_to'))
    for data in address_type_data:
        if data['valid_from'] is None:
            data['valid_from'] = ''
        else:
            data['valid_from'] = data['valid_from'].strftime('%d-%m-%Y')

        if data['valid_to'] is None:
            data['valid_to'] = ''
        else:
            data['valid_to'] = data['valid_to'].strftime('%d-%m-%Y')

    return address_type_data


def get_paymentdesc_dropdown():
    payterm_key_list = list(Payterms.objects.filter(del_ind=False).values('payment_term_key'))
    language_list = list(Languages.objects.filter(del_ind=False).values('language_id', 'description'))
    data = {
        'payterm_key_list': payterm_key_list,
        'language_list': language_list,
    }
    return data


def get_paymentdesc_data():
    payment_desc_data = django_query_instance.django_filter_query(
        Payterms_desc, {'client': global_variables.GLOBAL_CLIENT, 'del_ind': False}, None,
        ['payment_term_guid', 'payment_term_key', 'day_limit',
         'description', 'language_id', 'del_ind'])
    return payment_desc_data


def get_payment_data():
    payment_term_data = list(
        Payterms.objects.filter(del_ind=False).values('payment_term_key', 'payment_term_guid'))
    for payment_terms_fd in payment_term_data:
        if django_query_instance.django_existence_check(Payterms,
                                                        {'del_ind': False,
                                                         'payment_term_key': payment_terms_fd['payment_term_key']}):
            payment_terms_fd["del_ind_flag"] = False
        else:
            payment_terms_fd["del_ind_flag"] = True
    return payment_term_data


def get_incoterms_data():
    incoterms_data = django_query_instance.django_filter_query(
        Incoterms, {'del_ind': False}, None, ['incoterm_key', 'description'])
    return incoterms_data


def save_prod_cat_image_to_db(prod_cat, file_name, attached_file):
    """

    :param prod_cat:
    :param file_name:
    :param attached_file:
    :return:
    """
    image_type = get_image_type(CONST_UNSPSC_IMAGE_TYPE)
    if django_query_instance.django_existence_check(ImagesUpload,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'image_id': prod_cat}):
        django_query_instance.django_get_query(ImagesUpload,
                                               {'client': global_variables.GLOBAL_CLIENT,
                                                'image_id': prod_cat}).image_url.delete(save=True)
        django_query_instance.django_filter_delete_query(ImagesUpload,
                                                         {'client': global_variables.GLOBAL_CLIENT,
                                                          'image_id': prod_cat})
    django_query_instance.django_create_query(ImagesUpload, {
        'images_upload_guid': guid_generator(),
        'client': global_variables.GLOBAL_CLIENT,
        'image_id': prod_cat,
        'image_url': attached_file['prod_cat_image'],
        'image_name': file_name,
        'image_default': True,
        'image_type': image_type,
        'created_at': datetime.today(),
        'created_by': global_variables.GLOBAL_LOGIN_USERNAME,
        'del_ind': False
    })


def delete_prod_cat_image_to_db(prod_cat):
    if django_query_instance.django_existence_check(ImagesUpload,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'image_id': prod_cat}):
        django_query_instance.django_get_query(ImagesUpload,
                                               {'client': global_variables.GLOBAL_CLIENT,
                                                'image_id': prod_cat}).image_url.delete(save=True)
        django_query_instance.django_filter_delete_query(ImagesUpload,
                                                         {'client': global_variables.GLOBAL_CLIENT,
                                                          'image_default': False,
                                                          'image_id': prod_cat})
