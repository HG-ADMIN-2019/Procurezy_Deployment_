import os
import re

from django.db import models

from eProc_Basic.Utilities.global_defination import global_variables


# from eProc_Registration.models import UserData


class AccountingData(models.Model):
    """
    Contains Accounting data related to MMD_ACC_AST_CAT
    """
    account_assign_guid = models.CharField(primary_key=True, db_column='ACCOUNT_ASSIGN_GUID', max_length=32)
    account_assign_value = models.CharField(db_column='ACC_ASSIGN_VALUE', max_length=40, null=False)
    valid_from = models.DateField(db_column='VAILD_FROM', null=False)
    valid_to = models.DateField(db_column='VAILD_TO', null=False)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    accounting_data_created_by = models.CharField(db_column='ACCOUNTING_DATA_CREATED_BY', max_length=30, null=True)
    accounting_data_created_at = models.DateTimeField(db_column='ACCOUNTING_DATA_CREATED_AT', max_length=50, null=True)
    accounting_data_changed_by = models.CharField(db_column='ACCOUNTING_DATA_CHANGED_BY', max_length=30, null=True)
    accounting_data_changed_at = models.DateTimeField(db_column='ACCOUNTING_DATA_CHANGED_AT', max_length=50, null=True)
    accounting_data_source_system = models.CharField(db_column='ACCOUNTING_DATA_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    account_assign_cat = models.ForeignKey('eProc_Configuration.AccountAssignmentCategory', models.DO_NOTHING,
                                           db_column='ACCOUNT_ASSIGN_CAT', null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        unique_together = (
            'client', 'account_assign_value', 'account_assign_cat', 'company_id', 'accounting_data_source_system')
        db_table = "MMD_ACCOUNTING_DATA"
        managed = True


class AccountingDataHistory(models.Model):
    account_assign_key = models.AutoField(primary_key=True, db_column='ACCOUNT_ASSIGN_KEY', null=False)
    account_assign_guid = models.CharField(db_column='ACCOUNT_ASSIGN_GUID', max_length=32)
    account_assign_value = models.CharField(db_column='ACC_ASSIGN_VALUE', max_length=40, null=False)
    valid_from = models.DateField(db_column='VAILD_FROM', null=False)
    valid_to = models.DateField(db_column='VAILD_TO', null=False)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    accounting_data_created_by = models.CharField(db_column='ACCOUNTING_DATA_CREATED_BY', max_length=30, null=True)
    accounting_data_created_at = models.DateTimeField(db_column='ACCOUNTING_DATA_CREATED_AT', max_length=50, null=True)
    accounting_data_changed_by = models.CharField(db_column='ACCOUNTING_DATA_CHANGED_BY', max_length=30, null=True)
    accounting_data_changed_at = models.DateTimeField(db_column='ACCOUNTING_DATA_CHANGED_AT', max_length=50, null=True)
    accounting_data_source_system = models.CharField(db_column='ACCOUNTING_DATA_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    account_assign_cat = models.CharField(db_column='ACCOUNT_ASSIGN_CAT', max_length=10,
                                          verbose_name='AccountAssignmentCat')
    client = models.CharField(max_length=8, db_column='CLIENT', null=True)

    class Meta:
        db_table = "MMD_ACCOUNTING_DATA_HISTORY"
        managed = True


class AccountingDataDesc(models.Model):
    """
    Contains accounting data description
    """
    acc_desc_guid = models.CharField(primary_key=True, db_column='ACC_DESC_GUID', max_length=32)
    account_assign_value = models.CharField(db_column='ACCOUNT_ASSIGN_VALUE', max_length=40, null=False)
    description = models.CharField(db_column='DESCRIPTION', max_length=255, null=False)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    accounting_data_desc_created_by = models.CharField(db_column='ACCOUNTING_DATA_DESC_CREATED_BY', max_length=30,
                                                       null=True)
    accounting_data_desc_created_at = models.DateTimeField(db_column='ACCOUNTING_DATA_DESC_CREATED_AT', max_length=50,
                                                           null=True)
    accounting_data_desc_changed_by = models.CharField(db_column='ACCOUNTING_DATA_DESC_CHANGED_BY', max_length=30,
                                                       null=True)
    accounting_data_desc_changed_at = models.DateTimeField(db_column='ACCOUNTING_DATA_DESC_CHANGED_AT', max_length=50,
                                                           null=True)
    accounting_data_desc_source_system = models.CharField(db_column='ACCOUNTING_DATA_DESC_SOURCE_SYSTEM', max_length=20)

    del_ind = models.BooleanField(default=False, null=False)
    account_assign_cat = models.ForeignKey('eProc_Configuration.AccountAssignmentCategory', models.DO_NOTHING,
                                           db_column='ACCOUNT_ASSIGN_CAT', null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    language_id = models.ForeignKey('eProc_Configuration.Languages', models.DO_NOTHING, db_column='LANGUAGE_ID')

    class Meta:
        db_table = "MMD_ACC_DATA_DESC"
        managed = True
        unique_together = ('client', 'account_assign_value', 'account_assign_cat', 'company_id', 'language_id',
                           'accounting_data_desc_source_system')


class AccountingDataDescHistory(models.Model):
    acc_desc_key = models.AutoField(primary_key=True, db_column='ACC_DESC_KEY', null=False)
    acc_desc_guid = models.CharField(db_column='ACC_DESC_GUID', max_length=32)
    account_assign_value = models.CharField(db_column='ACCOUNT_ASSIGN_VALUE', max_length=40, null=False)
    description = models.CharField(db_column='DESCRIPTION', max_length=255, null=False)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    accounting_data_desc_created_by = models.CharField(db_column='ACCOUNTING_DATA_DESC_CREATED_BY', max_length=30,
                                                       null=True)
    accounting_data_desc_created_at = models.DateTimeField(db_column='ACCOUNTING_DATA_DESC_CREATED_AT', max_length=50,
                                                           null=True)
    accounting_data_desc_changed_by = models.CharField(db_column='ACCOUNTING_DATA_DESC_CHANGED_BY', max_length=30,
                                                       null=True)
    accounting_data_desc_changed_at = models.DateTimeField(db_column='ACCOUNTING_DATA_DESC_CHANGED_AT', max_length=50,
                                                           null=True)
    accounting_data_desc_source_system = models.CharField(db_column='ACCOUNTING_DATA_DESC_SOURCE_SYSTEM', max_length=20)

    del_ind = models.BooleanField(default=False, null=False)
    account_assign_cat = models.CharField(db_column='ACCOUNT_ASSIGN_CAT', max_length=10, null=True,
                                          verbose_name='AccountAssignmentCat')
    client = models.CharField(max_length=8, db_column='CLIENT', null=True)
    language_id = models.CharField(db_column='LANGUAGE_ID', null=True, max_length=2)

    class Meta:
        db_table = "MMD_ACC_DATA_DESC_HISTORY"
        managed = True


class ApproverLimit(models.Model):
    app_guid = models.CharField(primary_key=True, db_column='APP_GUID', max_length=32)
    approver_username = models.CharField(db_column='APPROVER_USERNAME', max_length=16, null=False)
    app_code_id = models.CharField(db_column='APP_CODE_ID', max_length=8, null=False)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    approver_limit_created_by = models.CharField(db_column='APPROVER_LIMIT_CREATED_BY', max_length=30, null=True)
    approver_limit_created_at = models.DateTimeField(db_column='APPROVER_LIMIT_CREATED_AT', max_length=50, null=True)
    approver_limit_changed_by = models.CharField(db_column='APPROVER_LIMIT_CHANGED_BY', max_length=30, null=True)
    approver_limit_changed_at = models.DateTimeField(db_column='APPROVER_LIMIT_CHANGED_AT', max_length=50, null=True)
    approver_limit_source_system = models.CharField(db_column='APPROVER_LIMIT_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = "MMD_APPROVER_LIMIT_ID"
        managed = True


class ApproverLimitValue(models.Model):
    app_lim_dec_guid = models.CharField(primary_key=True, db_column='APP_LIM_DEC_GUID', max_length=32)
    app_code_id = models.CharField(db_column='APP_CODE_ID', max_length=8, null=False)
    upper_limit_value = models.PositiveIntegerField(db_column='UPPER_LIMIT_VALUE', null=True)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    approver_limit_value_created_by = models.CharField(db_column='APPROVER_LIMIT_VALUE_CREATED_BY', max_length=30,
                                                       null=True)
    approver_limit_value_created_at = models.DateTimeField(db_column='APPROVER_LIMIT_VALUE_CREATED_AT', max_length=50,
                                                           null=True)
    approver_limit_value_changed_by = models.CharField(db_column='APPROVER_LIMIT_VALUE_CHANGED_BY', max_length=30,
                                                       null=True)
    approver_limit_value_changed_at = models.DateTimeField(db_column='APPROVER_LIMIT_VALUE_CHANGED_AT', max_length=50,
                                                           null=True)
    approver_limit_value_source_system = models.CharField(db_column='APPROVER_LIMIT_VALUE_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    app_types = models.ForeignKey('eProc_Configuration.ApproverType', models.DO_NOTHING, db_column='APP_TYPES')
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    currency_id = models.ForeignKey('eProc_Configuration.Currency', models.DO_NOTHING, db_column='CURRENCY_ID',
                                    null=True)

    class Meta:
        unique_together = ('client', 'app_code_id', 'app_types', 'company_id', 'approver_limit_value_source_system', 'currency_id')
        db_table = "MMD_APPROVER_LIMIT_VALUE"
        managed = True


class ApproverLimitValueHistory(models.Model):
    app_lim_dec_key = models.AutoField(primary_key=True, db_column='APP_LIM_DEC_KEY', null=False)
    app_lim_dec_guid = models.CharField(db_column='APP_LIM_DEC_GUID', max_length=32)
    app_code_id = models.CharField(db_column='APP_CODE_ID', max_length=8, null=False)
    upper_limit_value = models.PositiveIntegerField(db_column='UPPER_LIMIT_VALUE', null=True)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    approver_limit_value_created_by = models.CharField(db_column='APPROVER_LIMIT_VALUE_CREATED_BY', max_length=30,
                                                       null=True)
    approver_limit_value_created_at = models.DateTimeField(db_column='APPROVER_LIMIT_VALUE_CREATED_AT', max_length=50,
                                                           null=True)
    approver_limit_value_changed_by = models.CharField(db_column='APPROVER_LIMIT_VALUE_CHANGED_BY', max_length=30,
                                                       null=True)
    approver_limit_value_changed_at = models.DateTimeField(db_column='APPROVER_LIMIT_VALUE_CHANGED_AT', max_length=50,
                                                           null=True)
    approver_limit_value_source_system = models.CharField(db_column='APPROVER_LIMIT_VALUE_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    app_types = models.CharField(db_column='APP_TYPES', null=True, max_length=30)
    client = models.CharField(max_length=8, db_column='CLIENT', null=True)
    currency_id = models.CharField(db_column='CURRENCY_ID', null=True, max_length=3)

    class Meta:
        db_table = "MMD_APPROVER_LIMIT_VALUE_HISTORY"
        managed = True


class ApproverLimitHistory(models.Model):
    app_guid = models.CharField(primary_key=True, db_column='APP_GUID', max_length=32)
    approver_username = models.CharField(db_column='APPROVER_USERNAME', max_length=16, null=False)
    app_code_id = models.CharField(db_column='APP_CODE_ID', max_length=8, null=False)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    approver_limit_created_by = models.CharField(db_column='APPROVER_LIMIT_CREATED_BY', max_length=30, null=True)
    approver_limit_created_at = models.DateTimeField(db_column='APPROVER_LIMIT_CREATED_AT', max_length=50, null=True)
    approver_limit_changed_by = models.CharField(db_column='APPROVER_LIMIT_CHANGED_BY', max_length=30, null=True)
    approver_limit_changed_at = models.DateTimeField(db_column='APPROVER_LIMIT_CHANGED_AT', max_length=50, null=True)
    approver_limit_source_system = models.CharField(db_column='APPROVER_LIMIT_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.CharField( max_length=8, db_column='CLIENT',null = True)

    class Meta:
        db_table = "MMD_APPROVER_LIMIT_ID_HISTORY"
        managed = True


class DBQueries:

    def get_catalog_fields(self, client, catalog_id_query, catalog_desc_query, catalog_name_query, product_type_query,
                           search_count):
        return list(
            Catalogs.objects.filter(catalog_id_query, catalog_desc_query, catalog_name_query, product_type_query,
                                    client=client,
                                    del_ind=False).values().order_by('catalog_id')[:int(search_count)])


class Catalogs(models.Model, DBQueries):
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    catalog_guid = models.CharField(db_column='CATALOG_guid', primary_key=True, max_length=32, null=False, default=None)
    catalog_id = models.CharField(db_column='CATALOG_ID', null=False, default=None, max_length=16)
    description = models.CharField(db_column='DESCRIPTION', max_length=255, null=False, blank=False)
    name = models.CharField(db_column='CATALOG_NAME', max_length=16, null=False)
    prod_type = models.CharField(db_column='PROD_TYPE', max_length=10, blank=False, null=True,
                                 verbose_name='Product Type')
    catalogs_created_by = models.CharField(db_column='CATALOGS_CREATED_BY', max_length=30, null=True)
    catalogs_created_at = models.DateTimeField(db_column='CATALOGS_CREATED_AT', max_length=50, null=True)
    catalogs_changed_by = models.CharField(db_column='CATALOGS_CHANGED_BY', max_length=30, null=True)
    catalogs_changed_at = models.DateTimeField(db_column='CATALOGS_CHANGED_AT', max_length=50, null=True)
    is_active_flag = models.BooleanField(default=True, null=True, db_column='IS_ACTIVE_FLAG')
    catalog_status = models.CharField(db_column='CATALOG_STATUS', max_length=20, null=True)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        managed = True
        unique_together = ('client', 'catalog_id')
        db_table = 'MMD_CATALOGS'


class DetermineGLAccount(models.Model):
    det_gl_acc_guid = models.CharField(primary_key=True, db_column='DET_GL_ACC_GUID', max_length=32)
    prod_cat_id = models.CharField(db_column='PROD_CAT_ID', max_length=20, null=False)
    item_from_value = models.PositiveIntegerField(db_column='ITEM_FROM_VALUE', null=True)
    item_to_value = models.PositiveIntegerField(db_column='ITEM_TO_VALUE', null=True)
    gl_acc_num = models.CharField(db_column='GL_ACC_NUM', max_length=10, null=True)
    gl_acc_default = models.BooleanField(default=False, null=False, db_column='GL_ACC_DEFAULT')
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    determine_gl_account_created_by = models.CharField(db_column='DETERMINE_GL_ACCOUNT_CREATED_BY', max_length=30,
                                                       null=True)
    determine_gl_account_created_at = models.DateTimeField(db_column='DETERMINE_GL_ACCOUNT_CREATED_AT', max_length=50,
                                                           null=True)
    determine_gl_account_changed_by = models.CharField(db_column='DETERMINE_GL_ACCOUNT_CHANGED_BY', max_length=30,
                                                       null=True)
    determine_gl_account_changed_at = models.DateTimeField(db_column='DETERMINE_GL_ACCOUNT_CHANGED_AT', max_length=50,
                                                           null=True)
    determine_gl_account_source_system = models.CharField(db_column='DETERMINE_GL_ACCOUNT_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    account_assign_cat = models.ForeignKey('eProc_Configuration.AccountAssignmentCategory', models.DO_NOTHING,
                                           db_column='ACCOUNT_ASSIGN_CAT')
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    currency_id = models.ForeignKey('eProc_Configuration.Currency', models.DO_NOTHING, db_column='CURRENCY_ID')

    class Meta:
        db_table = "MMD_DET_GL_ACC"
        managed = True


class DetermineGLAccountHistory(models.Model):
    det_gl_acc_key = models.AutoField(primary_key=True, db_column='DET_GL_ACC_KEY', null=False)
    det_gl_acc_guid = models.CharField(db_column='DET_GL_ACC_GUID', max_length=32)
    prod_cat_id = models.CharField(db_column='PROD_CAT_ID', max_length=20, null=False)
    item_from_value = models.PositiveIntegerField(db_column='ITEM_FROM_VALUE', null=True)
    item_to_value = models.PositiveIntegerField(db_column='ITEM_TO_VALUE', null=True)
    gl_acc_num = models.CharField(db_column='GL_ACC_NUM', max_length=10, null=True)
    gl_acc_default = models.BooleanField(default=False, null=False, db_column='GL_ACC_DEFAULT')
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    determine_gl_account_created_by = models.CharField(db_column='DETERMINE_GL_ACCOUNT_CREATED_BY', max_length=30,
                                                       null=True)
    determine_gl_account_created_at = models.DateTimeField(db_column='DETERMINE_GL_ACCOUNT_CREATED_AT', max_length=50,
                                                           null=True)
    determine_gl_account_changed_by = models.CharField(db_column='DETERMINE_GL_ACCOUNT_CHANGED_BY', max_length=30,
                                                       null=True)
    determine_gl_account_changed_at = models.DateTimeField(db_column='DETERMINE_GL_ACCOUNT_CHANGED_AT', max_length=50,
                                                           null=True)
    determine_gl_account_source_system = models.CharField(db_column='DETERMINE_GL_ACCOUNT_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    account_assign_cat = models.CharField(db_column='ACCOUNT_ASSIGN_CAT', max_length=10, null=True,
                                          verbose_name='AccountAssignmentCat')
    client = models.CharField(max_length=8, db_column='CLIENT', null=True)
    currency_id = models.CharField(db_column='CURRENCY_ID', null=True, max_length=3)

    class Meta:
        db_table = "MMD_DET_GL_ACC_HISTORY"
        managed = True


class Incoterms(models.Model):
    """
    Contains definition of incoterms
    """
    incoterm_key = models.CharField(db_column='INCOTERM_KEY', primary_key=True, max_length=3, null=False)
    description = models.CharField(db_column='DESCRIPTION', max_length=50, null=False)
    incoterms_created_by = models.CharField(db_column='INCOTERMS_CREATED_BY', max_length=30, null=True)
    incoterms_created_at = models.DateTimeField(db_column='INCOTERMS_CREATED_AT', max_length=50, null=True)
    incoterms_changed_by = models.CharField(db_column='INCOTERMS_CHANGED_BY', max_length=30, null=True)
    incoterms_changed_at = models.DateTimeField(db_column='INCOTERMS_CHANGED_AT', max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        managed = True
        db_table = 'MMD_INCOTERMS_KEY'

    def __str__(self):
        return self.incoterm_key


class OrgAddress(models.Model):
    """
    Contains address details
    """
    address_guid = models.CharField(primary_key=True, db_column='ADDRESS_GUID', max_length=32)
    address_number = models.PositiveIntegerField(db_column='ADDRESS_NUMBER', null=False)
    address_partner_type = models.ForeignKey('eProc_Configuration.AddressPartnerType', models.DO_NOTHING,
                                             db_column='ADDRESS_PARTNER_TYPE', null=True)
    title = models.CharField(db_column='TITLE', max_length=40, null=True)
    name1 = models.CharField(db_column='NAME1', max_length=40, null=False, verbose_name='First Name')
    name2 = models.CharField(db_column='NAME2', max_length=40, null=False, verbose_name='Last Name')
    street = models.CharField(db_column='STREET', max_length=100, null=False, verbose_name='Street')
    area = models.CharField(db_column='AREA', max_length=100, null=False, verbose_name='Area')
    landmark = models.CharField(db_column='LANDMARK', max_length=100, null=False, verbose_name='Landmark')
    city = models.CharField(db_column='CITY', max_length=20, null=False, verbose_name='City')
    postal_code = models.CharField(db_column='postal_code', max_length=10, null=False, verbose_name='Postal Code', )
    region = models.CharField(db_column='REGION', max_length=30, null=False, verbose_name='Region')
    mobile_number = models.CharField(db_column='MOBILE_NUMBER', max_length=20, verbose_name='Mobile', null=False,
                                     blank=True)
    telephone_number = models.CharField(db_column='TELEPHONE_NUMBER', max_length=20, verbose_name='Telephone',
                                        null=True, blank=True)
    fax_number = models.CharField(db_column='FAX_NUMBER', max_length=30, null=True, blank=False, verbose_name='Fax')
    email = models.EmailField(db_column='EMAIL', max_length=100, null=True)
    org_address_created_by = models.CharField(db_column='ORG_ADDRESS_CREATED_BY', max_length=30, null=True)
    org_address_created_at = models.DateTimeField(db_column='ORG_ADDRESS_CREATED_AT', max_length=50, null=True)
    org_address_changed_by = models.CharField(db_column='ORG_ADDRESS_CHANGED_BY', max_length=30, null=True)
    org_address_changed_at = models.DateTimeField(db_column='ORG_ADDRESS_CHANGED_AT', max_length=50, null=True)
    org_address_source_system = models.CharField(db_column='ORG_ADDRESS_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    country_code = models.ForeignKey('eProc_Configuration.Country', db_column='COUNTRY_CODE', on_delete=models.PROTECT,
                                     verbose_name='country_code')
    language_id = models.ForeignKey('eProc_Configuration.Languages', db_column='LANGUAGE_ID', on_delete=models.PROTECT,
                                    verbose_name='Language')
    time_zone = models.ForeignKey('eProc_Configuration.TimeZone', db_column='TIME_ZONE', on_delete=models.PROTECT,
                                  null=False)

    class Meta:
        unique_together = ('client', 'address_number', 'org_address_source_system')
        db_table = "MMD_ADDRESS"
        managed = True

    def __str__(self):
        return self.address_guid


class OrgAddressMap(models.Model):
    """
    Contains address mapping info
    """
    address_guid = models.CharField(primary_key=True, db_column='ADDRESS_GUID', max_length=32)
    address_type = models.CharField(db_column='ADDRESS_TYPE', max_length=1, null=False, blank=False)
    address_number = models.PositiveIntegerField(db_column='ADDRESS_NUMBER', null=False)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    valid_from = models.DateTimeField(db_column='VALID_FROM', blank=True, null=True)
    valid_to = models.DateTimeField(db_column='VALID_TO', blank=True, null=True)
    org_address_map_created_by = models.CharField(db_column='ORG_ADDRESS_MAP_CREATED_BY', max_length=30, null=True)
    org_address_map_created_at = models.DateTimeField(db_column='ORG_ADDRESS_MAP_CREATED_AT', max_length=50, null=True)
    org_address_map_changed_by = models.CharField(db_column='ORG_ADDRESS_MAP_CHANGED_BY', max_length=30, null=True)
    org_address_map_changed_at = models.DateTimeField(db_column='ORG_ADDRESS_MAP_CHANGED_AT', max_length=50, null=True)
    org_address_map_source_system = models.CharField(db_column='ORG_ADDRESS_MAP_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = "MMD_ADDRESS_TYPE"
        unique_together = ('client', 'address_type', 'address_number', 'org_address_map_source_system', 'company_id')
        managed = True


class OrgCompanies(models.Model):
    """
    Contains company code description
    """
    company_guid = models.CharField(db_column='COMPANY_GUID', primary_key=True, max_length=32)
    name1 = models.CharField(db_column='NAME1', max_length=100, null=False)
    name2 = models.CharField(db_column='NAME2', max_length=100, null=False)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    org_companies_created_by = models.CharField(db_column='ORG_COMPANIES_CREATED_BY', max_length=30, null=True)
    org_companies_created_at = models.DateTimeField(db_column='ORG_COMPANIES_CREATED_AT', max_length=50, null=True)
    org_companies_changed_by = models.CharField(db_column='ORG_COMPANIES_CHANGED_BY', max_length=30, null=True)
    org_companies_changed_at = models.DateTimeField(db_column='ORG_COMPANIES_CHANGED_AT', max_length=50, null=True)
    org_companies_source_system = models.CharField(db_column='ORG_COMPANIES_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', db_column='Client', on_delete=models.PROTECT,
                               null=False)
    object_id = models.ForeignKey('eProc_Org_Model.OrgModel', db_column='OBJECT_ID', on_delete=models.PROTECT,
                                  null=True, default=None)

    class Meta:
        unique_together = ('client', 'company_id', 'org_companies_source_system')
        db_table = "MMD_ORG_COMPANIES"
        managed = True

    def __str__(self):
        return self.company_id


class OrgCompaniesHistory(models.Model):
    company_key = models.AutoField(primary_key=True, db_column='COMPANY_KEY', null=False)
    company_guid = models.CharField(db_column='COMPANY_GUID', max_length=32)
    name1 = models.CharField(db_column='NAME1', max_length=100, null=False)
    name2 = models.CharField(db_column='NAME2', max_length=100, null=False)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    org_companies_created_by = models.CharField(db_column='ORG_COMPANIES_CREATED_BY', max_length=30, null=True)
    org_companies_created_at = models.DateTimeField(db_column='ORG_COMPANIES_CREATED_AT', max_length=50, null=True)
    org_companies_changed_by = models.CharField(db_column='ORG_COMPANIES_CHANGED_BY', max_length=30, null=True)
    org_companies_changed_at = models.DateTimeField(db_column='ORG_COMPANIES_CHANGED_AT', max_length=50, null=True)
    org_companies_source_system = models.CharField(db_column='ORG_COMPANIES_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.CharField(max_length=8, db_column='CLIENT', null=True)
    object_id = models.PositiveBigIntegerField(db_column='OBJECT_ID', null=True)

    class Meta:
        db_table = "MMD_ORG_COMPANIES_HISTORY"
        managed = True


class OrgPorg(models.Model):
    """
    Contains purchase organization description
    """
    porg_guid = models.CharField(db_column='PORG_GUID', primary_key=True, max_length=32)
    porg_id = models.CharField(db_column='PORG_ID', max_length=8)
    description = models.CharField(db_column='DESCRIPTION', max_length=100, null=False)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=True)
    org_porg_created_by = models.CharField(db_column='ORG_PORG_CREATED_BY', max_length=30, null=True)
    org_porg_created_at = models.DateTimeField(db_column='ORG_PORG_CREATED_AT', max_length=50, null=True)
    org_porg_changed_by = models.CharField(db_column='ORG_PORG_CHANGED_BY', max_length=30, null=True)
    org_porg_changed_at = models.DateTimeField(db_column='ORG_PORG_CHANGED_AT', max_length=50, null=True)
    org_porg_source_system = models.CharField(db_column='ORG_PORG_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    object_id = models.ForeignKey('eProc_Org_Model.OrgModel', db_column='OBJECT_ID', on_delete=models.PROTECT,
                                  null=True, default=None)

    class Meta:
        unique_together = ('client', 'porg_id', 'company_id', 'org_porg_source_system')
        db_table = "MMD_ORG_PORG"
        managed = True

    def __str__(self):
        return self.porg_id


class OrgPorgHistory(models.Model):
    porg_key = models.AutoField(primary_key=True, db_column='PORG_KEY', null=False)
    porg_guid = models.CharField(db_column='PORG_GUID', max_length=32)
    porg_id = models.CharField(db_column='PORG_ID', max_length=8)
    description = models.CharField(db_column='DESCRIPTION', max_length=100, null=False)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=True)
    org_porg_created_by = models.CharField(db_column='ORG_PORG_CREATED_BY', max_length=30, null=True)
    org_porg_created_at = models.DateTimeField(db_column='ORG_PORG_CREATED_AT', max_length=50, null=True)
    org_porg_changed_by = models.CharField(db_column='ORG_PORG_CHANGED_BY', max_length=30, null=True)
    org_porg_changed_at = models.DateTimeField(db_column='ORG_PORG_CHANGED_AT', max_length=50, null=True)
    org_porg_source_system = models.CharField(db_column='ORG_PORG_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.CharField(max_length=8, db_column='CLIENT', null=True)
    object_id = models.PositiveBigIntegerField(db_column='OBJECT_ID', null=True)

    class Meta:
        db_table = "MMD_ORG_PORG_HISTORY"
        managed = True


class OrgPorgMapping(models.Model):
    """
    Contains purchase organization description
    """
    org_porg_mapping_guid = models.CharField(db_column='ORG_PORG_MAPPING_GUID', primary_key=True, max_length=32)
    porg_id = models.CharField(db_column='PORG_ID', max_length=8)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=True)
    org_porg_mapping_created_by = models.CharField(db_column='ORG_PORG_MAPPING_CREATED_BY', max_length=30, null=True)
    org_porg_mapping_created_at = models.DateTimeField(db_column='ORG_PORG_MAPPING_CREATED_AT', max_length=50,
                                                       null=True)
    org_porg_mapping_changed_by = models.CharField(db_column='ORG_PORG_MAPPING_CHANGED_BY', max_length=30, null=True)
    org_porg_mapping_changed_at = models.DateTimeField(db_column='ORG_PORG_MAPPING_CHANGED_AT', max_length=50,
                                                       null=True)
    org_porg_mapping_source_system = models.CharField(db_column='ORG_PORG_MAPPING_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    object_id = models.ForeignKey('eProc_Org_Model.OrgModel', db_column='OBJECT_ID', on_delete=models.PROTECT,
                                  null=True, default=None)

    class Meta:
        db_table = "MMD_ORG_PORG_MAPPING"
        managed = True

    def __str__(self):
        return self.porg_id


class OrgPGroup(models.Model):
    """
    Contains purchase group description
    """
    pgroup_guid = models.CharField(db_column='PGROUP_GUID', primary_key=True, max_length=32)
    pgroup_id = models.CharField(db_column='PGROUP_ID', max_length=8, null=False)
    description = models.CharField(db_column='DESCRIPTION', max_length=100, null=False)
    porg_id = models.CharField(db_column='PORG_ID', max_length=8, null=True)
    org_pgroup_created_by = models.CharField(db_column='ORG_PGROUP_CREATED_BY', max_length=30, null=True)
    org_pgroup_created_at = models.DateTimeField(db_column='ORG_PGROUP_CREATED_AT', max_length=50, null=True)
    org_pgroup_changed_by = models.CharField(db_column='ORG_PGROUP_CHANGED_BY', max_length=30, null=True)
    org_pgroup_changed_at = models.DateTimeField(db_column='ORG_PGROUP_CHANGED_AT', max_length=50, null=True)
    org_pgroup_source_system = models.CharField(db_column='ORG_PGROUP_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    object_id = models.ForeignKey('eProc_Org_Model.OrgModel', db_column='OBJECT_ID', on_delete=models.PROTECT,
                                  null=True, default=None)

    class Meta:
        unique_together = ('client', 'pgroup_id')
        db_table = "MMD_ORG_PGROUP"
        managed = True

    def __str__(self):
        return self.pgroup_id


class OrgPGroupHistory(models.Model):
    pgroup_key = models.AutoField(primary_key=True, db_column='PGROUP_KEY', null=False)
    pgroup_guid = models.CharField(db_column='PGROUP_GUID', max_length=32)
    pgroup_id = models.CharField(db_column='PGROUP_ID', max_length=8, null=False)
    description = models.CharField(db_column='DESCRIPTION', max_length=100, null=False)
    porg_id = models.CharField(db_column='PORG_ID', max_length=8, null=True)
    org_pgroup_created_by = models.CharField(db_column='ORG_PGROUP_CREATED_BY', max_length=30, null=True)
    org_pgroup_created_at = models.DateTimeField(db_column='ORG_PGROUP_CREATED_AT', max_length=50, null=True)
    org_pgroup_changed_by = models.CharField(db_column='ORG_PGROUP_CHANGED_BY', max_length=30, null=True)
    org_pgroup_changed_at = models.DateTimeField(db_column='ORG_PGROUP_CHANGED_AT', max_length=50, null=True)
    org_pgroup_source_system = models.CharField(db_column='ORG_PGROUP_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.CharField(max_length=8, db_column='CLIENT', null=True)
    object_id = models.PositiveBigIntegerField(db_column='OBJECT_ID', null=True)

    class Meta:
        db_table = "MMD_ORG_PGROUP_HISTORY"
        managed = True


class Payterms(models.Model):
    """
    Contains definition of payment terms
    """
    payment_term_guid = models.CharField(db_column='PAYMENT_TERM_GUID', primary_key=True, max_length=32)
    payment_term_key = models.CharField(db_column='PAYMENT_TERM_KEY', max_length=4, null=False)
    payterms_created_by = models.CharField(db_column='PAYTERMS_CREATED_BY', max_length=30, null=True)
    payterms_created_at = models.DateTimeField(db_column='PAYTERMS_CREATED_AT', max_length=50, null=True)
    payterms_changed_by = models.CharField(db_column='PAYTERMS_CHANGED_BY', max_length=30, null=True)
    payterms_changed_at = models.DateTimeField(db_column='PAYTERMS_CHANGED_AT', max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        unique_together = (('client', 'payment_term_key'),)
        managed = True
        db_table = 'MMD_PAYMENT_TERMS'

    def __str__(self):
        return self.payment_term_key


class Payterms_desc(models.Model):
    """
    Contains definition of payment terms
    """
    payment_term_guid = models.CharField(db_column='PAYMENT_TERM_DESC_GUID', primary_key=True, max_length=32)
    payment_term_key = models.CharField(db_column='PAYMENT_TERM_KEY', max_length=4, null=False)
    day_limit = models.PositiveIntegerField(db_column='DAY_LIMIT', null=False)
    description = models.CharField(db_column='DESCRIPTION', max_length=50, null=False)
    payterms_desc_created_by = models.CharField(db_column='PAYTERMS_DESC_CREATED_BY', max_length=30, null=True)
    payterms_desc_created_at = models.DateTimeField(db_column='PAYTERMS_DESC_CREATED_AT', max_length=50, null=True)
    payterms_desc_changed_by = models.CharField(db_column='PAYTERMS_DESC_CHANGED_BY', max_length=30, null=True)
    payterms_desc_changed_at = models.DateTimeField(db_column='PAYTERMS_DESC_CHANGED_AT', max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False,
                               db_column='CLIENT_ID')
    language_id = models.ForeignKey('eProc_Configuration.Languages', db_column='LANGUAGE_ID', on_delete=models.PROTECT,
                                    null=False)

    class Meta:
        managed = True
        db_table = 'MMD_PAYMENT_TERM_DESC'


class DBQueries:

    @staticmethod
    def get_product_details_by_fields(client, obj, supp_query, product_category_query, product_id_query,
                                      short_desc_query, email_query,
                                      supp_type_query,
                                      products_detail_source_system_query, count):
        return list(ProductsDetail.objects.filter(supp_query, product_category_query,
                                                  product_id_query, email_query,
                                                  supp_type_query,
                                                  products_detail_source_system_query,
                                                  short_desc_query, client=client,
                                                  del_ind=False).values('product_id', 'short_desc', 'supplier_id',
                                                                        'lead_time', 'unit', 'price', 'currency',
                                                                        'prod_cat_id').order_by('product_id')[
                    :int(count)])


# Defining catalog model fields
class ProductsDetail(models.Model, DBQueries):
    catalog_item = models.CharField(db_column='CATALOG_ITEM', primary_key=True, max_length=32, null=False, default=None)
    product_id = models.CharField(db_column="PRODUCT_ID", max_length=16, null=True)
    short_desc = models.CharField(db_column='SHORT_DESC', max_length=255, blank=False, null=False,
                                  verbose_name='Product Short Description')
    long_desc = models.CharField(db_column='LONG_DESC', max_length=1000, blank=True, null=True,
                                 verbose_name='Product Long desc')
    bundle_flag = models.BooleanField(db_column='BUNDLE_FLAG', null=True)
    supp_product_id = models.CharField(db_column='SUPP_PRODUCT_ID', max_length=40, blank=True, null=True,
                                       verbose_name='Supplier Product Number')
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=10, verbose_name='Vendor Id', null=True)
    search_term1 = models.CharField(db_column='SEARCH_TERM1', null=True, max_length=15)
    search_term2 = models.CharField(db_column='SEARCH_TERM2', null=True, max_length=15)
    manufacturer = models.CharField(db_column='MANUFACTURER', max_length=15, null=True)
    brand = models.CharField(db_column="BRAND", null=True, max_length=15)
    offer_key = models.CharField(db_column='OFFER_KEY', null=True, max_length=15)
    price_on_request = models.BooleanField(db_column='PRICE_ON_REQUEST', null=True, default=False)
    manu_part_num = models.CharField(db_column='MANU_PART_NUM', max_length=40, null=True)
    manu_code_num = models.CharField(db_column='MANU_CODE_NUM', max_length=10, null=True)
    prod_type = models.CharField(db_column='PROD_TYPE', max_length=10, blank=True, null=True,
                                 verbose_name='Product Type')
    lead_time = models.PositiveIntegerField(db_column='LEAD_TIME', null=True)
    quantity_avail = models.PositiveIntegerField(db_column='QUANTITY_AVAIL', null=True,
                                                 verbose_name='Quantity Availability')
    price = models.DecimalField(db_column='GROSS_PRICE', max_digits=15, decimal_places=2, null=True)
    price_unit = models.CharField(db_column='PRICE_UNIT', max_length=3, null=True)
    cust_prod_cat_id = models.CharField(db_column='CUST_PROD_CAT_ID', null=True, max_length=20)
    quantity_min = models.PositiveIntegerField(db_column='QUANTITY_MIN', null=True)
    value_min = models.PositiveIntegerField(db_column='VALUE_MIN', null=True)
    quantity_max = models.PositiveIntegerField(db_column='QUANTITY_MAX', null=True, verbose_name='Quantity Max')
    tiered_flag = models.BooleanField(default=False, null=False, db_column='TIERED_FLAG')
    created_at = models.DateField(db_column='CREATED_AT', null=True)
    created_by = models.CharField(db_column='CREATED_BY', null=True, max_length=15)
    changed_at = models.DateField(db_column='CHANGED_AT', null=True)
    changed_by = models.CharField(db_column='CHANGED_BY', null=True, max_length=15)
    ctr_num = models.CharField(db_column='CTR_NUM', max_length=50, blank=True, null=True, verbose_name='ctr num')
    ctr_item_num = models.CharField(db_column='CTR_ITEM_NUM', max_length=50, blank=True, null=True,
                                    verbose_name='ctr num')
    ctr_name = models.CharField(db_column='CTR_NAME', blank=True, null=True, max_length=50,
                                verbose_name='Contract Name')
    # AWAITING_APPROVAL- UPON UPLOAD OF MASTER DATA BY SUPPLIER
    # ACTIVE - WHEN PRODUCT APPROVED BY PROD CAT MANAGER
    # INACTIVE - WHEN PRODUCT APPROVED BY PROD CAT MANAGER
    # DE-ACTIVE -WHEN PRODUCT IS DEPRECATED
    product_status = models.CharField(db_column='PRODUCT_STATUS', max_length=20, blank=False, null=True,
                                      verbose_name='Status')
    sgst = models.DecimalField(db_column='SGST', max_digits=15, decimal_places=2, blank=True, null=True,
                               verbose_name='State GST')
    cgst = models.DecimalField(db_column='CGST', max_digits=15, decimal_places=2, blank=True, null=True,
                               verbose_name='Central GST')
    vat = models.DecimalField(db_column='VAT', max_digits=15, decimal_places=2, blank=True, null=True,
                              verbose_name='Value Added Tax - VAT code (%age as decimal) returned from catalogue ')
    price_1 = models.DecimalField(db_column='PRICE_1', max_digits=15, decimal_places=2, null=True)
    quantity_1 = models.PositiveIntegerField(db_column='QUANTITY_1', null=True)
    price_2 = models.DecimalField(db_column='PRICE_2', max_digits=15, decimal_places=2, null=True)
    quantity_2 = models.PositiveIntegerField(db_column='QUANTITY_2', null=True)
    price_3 = models.DecimalField(db_column='PRICE_3', max_digits=15, decimal_places=2, null=True)
    quantity_3 = models.PositiveIntegerField(db_column='QUANTITY_3', null=True)
    external_link = models.CharField(db_column='EXTERNAL_LINK', max_length=200, blank=True, null=True)
    supplier_product_info = models.CharField(db_column="SUPPLIER_PRODUCT_INFO", max_length=16, null=True)
    eform_id = models.CharField(db_column='EFORM_ID', max_length=40, blank=False, null=True)
    discount_id = models.CharField(db_column='DISCOUNT_ID', max_length=40, blank=False, null=True)
    variant_id = models.CharField(db_column='VARIANT_ID', max_length=40, blank=False, null=True)
    product_info_id = models.CharField(db_column='PRODUCT_INFO_ID', max_length=40, blank=False, null=True)
    products_detail_source_system = models.CharField(db_column='PRODUCTS_DETAIL_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    country_of_origin = models.ForeignKey('eProc_Configuration.Country', db_column='COUNTRY_OF_ORIGIN',
                                          on_delete=models.PROTECT, verbose_name='Country', null=True)

    currency = models.ForeignKey('eProc_Configuration.Currency', db_column='CURRENCY', on_delete=models.PROTECT,
                                 null=True)
    language = models.ForeignKey('eProc_Configuration.Languages', db_column='LANGUAGE', on_delete=models.PROTECT,
                                 null=True,
                                 verbose_name='Language')
    unit = models.ForeignKey('eProc_Configuration.UnitOfMeasures', db_column='UNIT_OF_MEASURE', null=True,
                             on_delete=models.PROTECT)
    prod_cat_id = models.ForeignKey('eProc_Configuration.UnspscCategories', models.DO_NOTHING, db_column='PROD_CAT_ID',
                                    null=True)

    class Meta:
        managed = True
        unique_together = ('client', 'product_id', 'products_detail_source_system')
        db_table = 'MMD_PRODUCTS_DETAIL'


class purch_cockpit(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    from_prod_cat = models.CharField(db_column='FROM_PROD_CAT', max_length=10, null=False)
    to_prod_cat = models.CharField(db_column='TO_PROD_CAT', max_length=10, null=False)
    purch_cockpit_value = models.BooleanField(default=False, null=False, db_column='PURCH_COCKPIT_VALUE')
    purch_cockpit_created_by = models.CharField(db_column='purch_cockpit_created_by', max_length=30, null=True)
    purch_cockpit_created_at = models.DateTimeField(db_column='purch_cockpit_created_at', max_length=50, null=True)
    purch_cockpit_changed_by = models.CharField(db_column='purch_cockpit_changed_by', max_length=30, null=True)
    purch_cockpit_changed_at = models.DateTimeField(db_column='purch_cockpit_changed_at', max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False, db_column='DEL_IND')
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = 'MMD_PURCH_COCKPIT'
        managed = True


class SpendLimitId(models.Model):
    spend_guid = models.CharField(primary_key=True, db_column='SPEND_GUID', max_length=32)
    spend_code_id = models.CharField(db_column='SPEND_CODE_ID', max_length=8, null=False)
    spender_username = models.CharField(db_column='SPENDER_USERNAME', max_length=16, null=False)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    spend_limit_id_created_by = models.CharField(db_column='spend_limit_id_created_by', max_length=30, null=True)
    spend_limit_id_created_at = models.DateTimeField(db_column='spend_limit_id_created_at', max_length=50, null=True)
    spend_limit_id_changed_by = models.CharField(db_column='spend_limit_id_changed_by', max_length=30, null=True)
    spend_limit_id_changed_at = models.DateTimeField(db_column='spend_limit_id_changed_at', max_length=50, null=True)
    spend_limit_id_source_system = models.CharField(db_column='spend_limit_id_source_system', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = "MMD_SPENDER_LIMIT_ID"
        managed = True


class SpendLimitIdHistory(models.Model):
    spend_key = models.AutoField(primary_key=True, db_column='SPEND_KEY', null=False)
    spend_guid = models.CharField(db_column='SPEND_GUID', max_length=32)
    spend_code_id = models.CharField(db_column='SPEND_CODE_ID', max_length=8, null=False)
    spender_username = models.CharField(db_column='SPENDER_USERNAME', max_length=16, null=False)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    spend_limit_id_created_by = models.CharField(db_column='spend_limit_id_created_by', max_length=30, null=True)
    spend_limit_id_created_at = models.DateTimeField(db_column='spend_limit_id_created_at', max_length=50, null=True)
    spend_limit_id_changed_by = models.CharField(db_column='spend_limit_id_changed_by', max_length=30, null=True)
    spend_limit_id_changed_at = models.DateTimeField(db_column='spend_limit_id_changed_at', max_length=50, null=True)
    spend_limit_id_source_system = models.CharField(db_column='spend_limit_id_source_system', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.CharField(max_length=8, db_column='CLIENT', null=True)

    class Meta:
        db_table = "MMD_SPENDER_LIMIT_ID_HISTORY"
        managed = True


class SpendLimitValue(models.Model):
    spend_lim_value_guid = models.CharField(primary_key=True, db_column='SPEND_LIM_VALUE_GUID', max_length=32)
    spend_code_id = models.CharField(db_column='SPEND_CODE_ID', max_length=8, null=False)
    upper_limit_value = models.PositiveIntegerField(db_column='UPPER_LIMIT_VALUE')
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    spend_limit_value_created_by = models.CharField(db_column='SPEND_LIMIT_VALUE_CREATED_BY', max_length=30, null=True)
    spend_limit_value_created_at = models.DateTimeField(db_column='SPEND_LIMIT_VALUE_CREATED_AT', max_length=50,
                                                        null=True)
    spend_limit_value_changed_by = models.CharField(db_column='SPEND_LIMIT_VALUE_CHANGED_BY', max_length=30, null=True)
    spend_limit_value_changed_at = models.DateTimeField(db_column='SPEND_LIMIT_VALUE_CHANGED_AT', max_length=50,
                                                        null=True)
    spend_limit_value_source_system = models.CharField(db_column='SPEND_LIMIT_VALUE_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    currency_id = models.ForeignKey('eProc_Configuration.Currency', models.DO_NOTHING, db_column='CURRENCY_ID',
                                    null=True)

    class Meta:
        db_table = "MMD_SPENDER_LIMIT_VALUE"
        unique_together = ('spend_code_id', 'client', 'company_id', 'spend_limit_value_source_system', 'currency_id')
        managed = True


class SpendLimitValueHistory(models.Model):
    spend_lim_value_key = models.AutoField(primary_key=True, db_column='SPEND_LIM_VALUE_KEY', null=False)
    spend_lim_value_guid = models.CharField(db_column='SPEND_LIM_VALUE_GUID', max_length=32)
    spend_code_id = models.CharField(db_column='SPEND_CODE_ID', max_length=8, null=False)
    upper_limit_value = models.PositiveIntegerField(db_column='UPPER_LIMIT_VALUE')
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    spend_limit_value_created_by = models.CharField(db_column='SPEND_LIMIT_VALUE_CREATED_BY', max_length=30, null=True)
    spend_limit_value_created_at = models.DateTimeField(db_column='SPEND_LIMIT_VALUE_CREATED_AT', max_length=50,
                                                        null=True)
    spend_limit_value_changed_by = models.CharField(db_column='SPEND_LIMIT_VALUE_CHANGED_BY', max_length=30, null=True)
    spend_limit_value_changed_at = models.DateTimeField(db_column='SPEND_LIMIT_VALUE_CHANGED_AT', max_length=50,
                                                        null=True)
    spend_limit_value_source_system = models.CharField(db_column='SPEND_LIMIT_VALUE_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.CharField(max_length=8, db_column='CLIENT', null=True)
    currency_id = models.CharField(db_column='CURRENCY_ID', null=True, max_length=3)

    class Meta:
        db_table = "MMD_SPENDER_LIMIT_VALUE_HISTORY"
        managed = True


class DBQueriesSupplier:

    @staticmethod
    def get_supplier_details_by_fields(client, block, obj, name1_query, name2_query, supplier_id_query,
                                       email_query,
                                       supp_type_query, country_code_query, city_query):
        return list(SupplierMaster.objects.filter(name1_query, name2_query, supplier_id_query, email_query,
                                                  supp_type_query, country_code_query, city_query, client=client,
                                                  del_ind=False, block=block).values().order_by('supplier_id'))


class SupplierMaster(models.Model, DBQueriesSupplier):
    supp_guid = models.CharField(primary_key=True, db_column='SUPP_GUID', max_length=32)
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=10, verbose_name='Vendor Id')
    supp_type = models.CharField(db_column='SUPP_TYPE', max_length=35, blank=True, null=True,
                                 verbose_name='Supplier Type')
    name1 = models.CharField(db_column='NAME1', max_length=40, blank=False, null=False, verbose_name='Name 1')
    name2 = models.CharField(db_column='NAME2', max_length=40, blank=False, null=True, verbose_name='Name 2')
    supplier_username = models.CharField(db_column='SUPPLIER_USERNAME', null=True, max_length=16)
    city = models.CharField(db_column='CITY', max_length=40, blank=True, null=True, verbose_name='City')
    postal_code = models.CharField(db_column='POSTAL_CODE', max_length=10, blank=True, null=True,
                                   verbose_name='Postal Code')
    street = models.CharField(db_column='STREET', max_length=60, null=True, verbose_name='Street')
    landline = models.CharField(db_column='LANDLINE', max_length=30, null=True)
    mobile_num = models.CharField(db_column='MOBILE_NUM', max_length=30, null=True)
    fax = models.CharField(db_column='FAX', max_length=20, blank=True, null=True, verbose_name='Fax')
    email = models.EmailField(db_column='EMAIL', max_length=100, null=False)
    email1 = models.EmailField(db_column='EMAIL1', max_length=100, null=True)
    email2 = models.EmailField(db_column='EMAIL2', max_length=100, null=True)
    email3 = models.EmailField(db_column='EMAIL3', max_length=100, null=True)
    email4 = models.EmailField(db_column='EMAIL4', max_length=100, null=True)
    email5 = models.EmailField(db_column='EMAIL5', max_length=100, null=True)
    output_medium = models.CharField(db_column='OUTPUT_MEDIUM', max_length=10, blank=True, null=True,
                                     verbose_name='Output Medium')
    search_term1 = models.CharField(db_column='SEARCH_TERM1', max_length=20, blank=True, null=True,
                                    verbose_name='Search Term1')
    search_term2 = models.CharField(db_column='SEARCH_TERM2', max_length=20, blank=True, null=True,
                                    verbose_name='Search Term2')
    duns_number = models.CharField(db_column='DUNS_NUMBER', max_length=9, blank=True, null=True,
                                   verbose_name='Duns Number')
    block_date = models.DateField(db_column='BLOCK DATE', null=True, verbose_name='Block Date')
    block = models.BooleanField(db_column='BLOCK', default=False, null=False)
    delivery_days = models.CharField(db_column='DELIVERY_DAYS', max_length=20, null=True, blank=True)
    is_active = models.BooleanField(db_column='IS_ACTIVE', default=True, null=False)
    registration_number = models.CharField(db_column='REGISTRATION_NUMBER', unique=True, max_length=30, null=True)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    supplier_master_created_by = models.CharField(db_column='SUPPLIER_MASTER_CREATED_BY', max_length=30, null=True)
    supplier_master_created_at = models.DateTimeField(db_column='SUPPLIER_MASTER_CREATED_AT', max_length=50, null=True)
    supplier_master_changed_by = models.CharField(db_column='SUPPLIER_MASTER_CHANGED_BY', max_length=30, null=True)
    supplier_master_changed_at = models.DateTimeField(db_column='SUPPLIER_MASTER_CHANGED_AT', max_length=50, null=True)
    supplier_master_source_system = models.CharField(db_column='SUPPLIER_MASTER_SOURCE_SYSTEM', max_length=20)
    pref_routing = models.CharField(db_column='PREF_ROUTING', max_length=1, blank=True, null=True,
                                    verbose_name='Preferred Routing')
    lock_date = models.DateTimeField(db_column='LOCK_DATE', blank=True, null=True,
                                     verbose_name='Supplier will be locked on all Purch Orgs on this date')
    global_duns = models.CharField(db_column='GLOBAL_DUNS', max_length=9, null=True, verbose_name='Global Duns Number')
    domestic_duns = models.CharField(db_column='DOMESTIC_DUNS', max_length=9, null=True,
                                     verbose_name='Global Duns Number')
    ics_code = models.CharField(db_column='ICS_CODE', max_length=4, blank=True, null=True,
                                verbose_name='ICS code for vendor')
    internal_ind = models.BooleanField(db_column='INTERNAL_IND', default=False, null=False,
                                       verbose_name='Internal Supplier Indicator')
    sba_code = models.CharField(db_column='SBA_CODE', max_length=2, blank=True, null=True, verbose_name='SBA Code')
    ethnicity = models.CharField(db_column='ETHNICITY', max_length=2, blank=True, null=True,
                                 verbose_name='PEthnicity/Gender Code')
    hubzone = models.CharField(db_column='HUBZONE', max_length=2, blank=True, null=True, verbose_name='Hubzone')
    no_vend_text = models.BooleanField(db_column='NO_VEND_TEXT', default=False, null=False,
                                       verbose_name='Flag indication supplier not able to receive Vendor Text')
    agr_reg_no = models.CharField(db_column='AGR_REG_NO', max_length=40, blank=True, null=True,
                                  verbose_name='Agreement Registration Number')
    no_mult_addr = models.BooleanField(db_column='NO_MULT_ADDR', default=False, null=False,
                                       verbose_name='Flag indication for multiple ordering addresses not support')
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    country_code = models.ForeignKey('eProc_Configuration.Country', db_column='COUNTRY_CODE', on_delete=models.PROTECT,
                                     verbose_name='Country')
    currency_id = models.ForeignKey('eProc_Configuration.Currency', models.DO_NOTHING, db_column='CURRENCY_ID')
    language_id = models.ForeignKey('eProc_Configuration.Languages', db_column='LANGUAGE_ID', on_delete=models.PROTECT,
                                    null=False, verbose_name='Language')

    class Meta:
        managed = True
        unique_together = (('client', 'supplier_id', 'company_id', 'supplier_master_source_system'),
                           ('client', 'email', 'company_id', 'supplier_master_source_system'))
        db_table = 'MMD_SUPPLIERS'

    # TO get supplier id by first name
    @staticmethod
    def get_suppid_by_first_name(fname):
        if '*' in fname:
            requester = re.search(r'[a-zA-Z0-9]+', fname)
            if fname[0] == '*' and fname[-1] == '*':
                queryset = SupplierMaster.objects.values_list('supplier_id', flat=False).filter(
                    name1__icontains=requester.group(0))
            elif fname[0] == '*':
                queryset = SupplierMaster.objects.values_list('supplier_id', flat=False).filter(
                    name1__iendswith=requester.group(0))
            else:
                queryset = SupplierMaster.objects.values_list('supplier_id', flat=False).filter(
                    name1__istartswith=requester.group(0))

        else:
            queryset = SupplierMaster.objects.values_list('supplier_id', flat=False).filter(name1=fname)
        supp_list = []
        for field in queryset:
            supp_list.append(field[0])
        return supp_list


class SupplierMasterHistory(models.Model, DBQueriesSupplier):
    supp_key = models.AutoField(primary_key=True, db_column='SUPP_KEY', null=False)
    supp_guid = models.CharField(db_column='SUPP_GUID', max_length=32)
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=10, verbose_name='Vendor Id')
    supp_type = models.CharField(db_column='SUPP_TYPE', max_length=35, blank=True, null=True,
                                 verbose_name='Supplier Type')
    name1 = models.CharField(db_column='NAME1', max_length=40, blank=False, null=False, verbose_name='Name 1')
    name2 = models.CharField(db_column='NAME2', max_length=40, blank=False, null=True, verbose_name='Name 2')
    supplier_username = models.CharField(db_column='SUPPLIER_USERNAME', null=True, max_length=16)
    city = models.CharField(db_column='CITY', max_length=40, blank=True, null=True, verbose_name='City')
    postal_code = models.CharField(db_column='POSTAL_CODE', max_length=10, blank=True, null=True,
                                   verbose_name='Postal Code')
    street = models.CharField(db_column='STREET', max_length=60, null=True, verbose_name='Street')
    landline = models.CharField(db_column='LANDLINE', max_length=30, null=True)
    mobile_num = models.CharField(db_column='MOBILE_NUM', max_length=30, null=True)
    fax = models.CharField(db_column='FAX', max_length=20, blank=True, null=True, verbose_name='Fax')
    email = models.EmailField(db_column='EMAIL', max_length=100, null=False)
    email1 = models.EmailField(db_column='EMAIL1', max_length=100, null=True)
    email2 = models.EmailField(db_column='EMAIL2', max_length=100, null=True)
    email3 = models.EmailField(db_column='EMAIL3', max_length=100, null=True)
    email4 = models.EmailField(db_column='EMAIL4', max_length=100, null=True)
    email5 = models.EmailField(db_column='EMAIL5', max_length=100, null=True)
    output_medium = models.CharField(db_column='OUTPUT_MEDIUM', max_length=10, blank=True, null=True,
                                     verbose_name='Output Medium')
    search_term1 = models.CharField(db_column='SEARCH_TERM1', max_length=20, blank=True, null=True,
                                    verbose_name='Search Term1')
    search_term2 = models.CharField(db_column='SEARCH_TERM2', max_length=20, blank=True, null=True,
                                    verbose_name='Search Term2')
    duns_number = models.CharField(db_column='DUNS_NUMBER', max_length=9, blank=True, null=True,
                                   verbose_name='Duns Number')
    block_date = models.DateField(db_column='BLOCK DATE', null=True, verbose_name='Block Date')
    block = models.BooleanField(db_column='BLOCK', default=False, null=False)
    delivery_days = models.CharField(db_column='DELIVERY_DAYS', max_length=20, null=True, blank=True)
    is_active = models.BooleanField(db_column='IS_ACTIVE', default=True, null=False)
    registration_number = models.CharField(db_column='REGISTRATION_NUMBER', max_length=30, null=True)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    supplier_master_created_by = models.CharField(db_column='SUPPLIER_MASTER_CREATED_BY', max_length=30, null=True)
    supplier_master_created_at = models.DateTimeField(db_column='SUPPLIER_MASTER_CREATED_AT', max_length=50, null=True)
    supplier_master_changed_by = models.CharField(db_column='SUPPLIER_MASTER_CHANGED_BY', max_length=30, null=True)
    supplier_master_changed_at = models.DateTimeField(db_column='SUPPLIER_MASTER_CHANGED_AT', max_length=50, null=True)
    supplier_master_source_system = models.CharField(db_column='SUPPLIER_MASTER_SOURCE_SYSTEM', max_length=20)
    pref_routing = models.CharField(db_column='PREF_ROUTING', max_length=1, blank=True, null=True,
                                    verbose_name='Preferred Routing')
    lock_date = models.DateTimeField(db_column='LOCK_DATE', blank=True, null=True,
                                     verbose_name='Supplier will be locked on all Purch Orgs on this date')
    global_duns = models.CharField(db_column='GLOBAL_DUNS', max_length=9, null=True, verbose_name='Global Duns Number')
    domestic_duns = models.CharField(db_column='DOMESTIC_DUNS', max_length=9, null=True,
                                     verbose_name='Global Duns Number')
    ics_code = models.CharField(db_column='ICS_CODE', max_length=4, blank=True, null=True,
                                verbose_name='ICS code for vendor')
    internal_ind = models.BooleanField(db_column='INTERNAL_IND', default=False, null=False,
                                       verbose_name='Internal Supplier Indicator')
    sba_code = models.CharField(db_column='SBA_CODE', max_length=2, blank=True, null=True, verbose_name='SBA Code')
    ethnicity = models.CharField(db_column='ETHNICITY', max_length=2, blank=True, null=True,
                                 verbose_name='PEthnicity/Gender Code')
    hubzone = models.CharField(db_column='HUBZONE', max_length=2, blank=True, null=True, verbose_name='Hubzone')
    no_vend_text = models.BooleanField(db_column='NO_VEND_TEXT', default=False, null=False,
                                       verbose_name='Flag indication supplier not able to receive Vendor Text')
    agr_reg_no = models.CharField(db_column='AGR_REG_NO', max_length=40, blank=True, null=True,
                                  verbose_name='Agreement Registration Number')
    no_mult_addr = models.BooleanField(db_column='NO_MULT_ADDR', default=False, null=False,
                                       verbose_name='Flag indication for multiple ordering addresses not support')
    del_ind = models.BooleanField(default=False, null=False)
    client = models.CharField(max_length=8, db_column='CLIENT', null=True)
    country_code = models.CharField(db_column='COUNTRY_CODE', null=True, max_length=2)
    currency_id = models.CharField(db_column='CURRENCY_ID', null=True, max_length=3)
    language_id = models.CharField(db_column='LANGUAGE_ID', null=True, max_length=2)

    class Meta:
        managed = True
        db_table = 'MMD_SUPPLIERS_HISTORY'


class UnspscCategoriesCust(models.Model):
    prod_cat_guid = models.CharField(db_column='PROD_CAT_GUID', primary_key=True, max_length=32, null=False)
    unspsc_categories_cust_created_by = models.CharField(db_column='UNSPSC_CATEGORIES_CUST_CREATED_BY', max_length=30,
                                                         null=True)
    unspsc_categories_cust_created_at = models.DateTimeField(db_column='UNSPSC_CATEGORIES_CUST_CREATED_AT',
                                                             max_length=50, null=True)
    unspsc_categories_cust_changed_by = models.CharField(db_column='UNSPSC_CATEGORIES_CUST_CHANGED_BY', max_length=30,
                                                         null=True)
    unspsc_categories_cust_changed_at = models.DateTimeField(db_column='UNSPSC_CATEGORIES_CUST_CHANGED_AT',
                                                             max_length=50, null=True)
    unspsc_categories_cust_source_system = models.CharField(db_column='UNSPSC_CATEGORIES_CUST_SOURCE_SYSTEM',
                                                            max_length=20)

    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False,
                               db_column='CLIENT_ID')
    prod_cat_id = models.ForeignKey('eProc_Configuration.UnspscCategories', db_column='PROD_CAT_ID',
                                    on_delete=models.PROTECT, null=False)

    class Meta:
        unique_together = (('client', 'prod_cat_id', 'unspsc_categories_cust_source_system'),)
        managed = True
        db_table = 'MMD_UNSPSC_CATEGORIES_CUST'


class UnspscCategoriesCustHistory(models.Model):
    prod_cat_key = models.AutoField(primary_key=True, db_column='PROD_CAT_KEY', null=False)
    prod_cat_guid = models.CharField(db_column='PROD_CAT_GUID', max_length=32, null=False)
    unspsc_categories_cust_created_by = models.CharField(db_column='UNSPSC_CATEGORIES_CUST_CREATED_BY', max_length=30,
                                                         null=True)
    unspsc_categories_cust_created_at = models.DateTimeField(db_column='UNSPSC_CATEGORIES_CUST_CREATED_AT',
                                                             max_length=50, null=True)
    unspsc_categories_cust_changed_by = models.CharField(db_column='UNSPSC_CATEGORIES_CUST_CHANGED_BY', max_length=30,
                                                         null=True)
    unspsc_categories_cust_changed_at = models.DateTimeField(db_column='UNSPSC_CATEGORIES_CUST_CHANGED_AT',
                                                             max_length=50, null=True)
    unspsc_categories_cust_source_system = models.CharField(db_column='UNSPSC_CATEGORIES_CUST_SOURCE_SYSTEM',
                                                            max_length=20)

    del_ind = models.BooleanField(default=False, null=False)
    client = models.CharField(max_length=8, db_column='CLIENT', null=True)
    prod_cat_id = models.CharField(db_column='PROD_CAT_ID', null=True, max_length=20, verbose_name='Product Category')

    class Meta:
        managed = True
        db_table = 'MMD_UNSPSC_CATEGORIES_CUST_HISTORY'


class UnspscCategoriesCustDesc(models.Model):
    prod_cat_desc_guid = models.CharField(db_column='PROD_CAT_DESC_GUID', primary_key=True, max_length=32, null=False)
    category_desc = models.CharField(db_column='CATEGORY_DESC', max_length=200, blank=True, null=True,
                                     verbose_name='Category Description')
    unspsc_categories_cust_desc_created_by = models.CharField(db_column='UNSPSC_CATEGORIES_CUST_DESC_CREATED_BY',
                                                              max_length=30, null=True)
    unspsc_categories_cust_desc_created_at = models.DateTimeField(db_column='UNSPSC_CATEGORIES_CUST_DESC_CREATED_AT',
                                                                  max_length=50, null=True)
    unspsc_categories_cust_desc_changed_by = models.CharField(db_column='UNSPSC_CATEGORIES_CUST_DESC_CHANGED_BY',
                                                              max_length=30, null=True)
    unspsc_categories_cust_desc_changed_at = models.DateTimeField(db_column='UNSPSC_CATEGORIES_CUST_DESC_CHANGED_AT',
                                                                  max_length=50, null=True)
    unspsc_categories_cust_desc_source_system = models.CharField(db_column='UNSPSC_CATEGORIES_CUST_DESC_SOURCE_SYSTEM',
                                                                 max_length=20)

    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False,
                               db_column='CLIENT_ID')
    language_id = models.ForeignKey('eProc_Configuration.Languages', db_column='LANGUAGE_ID', on_delete=models.PROTECT,
                                    null=False)
    prod_cat_id = models.ForeignKey('eProc_Configuration.UnspscCategories', db_column='PROD_CAT_ID',
                                    on_delete=models.PROTECT, null=False)

    class Meta:
        unique_together = (('client', 'language_id', 'prod_cat_id', 'unspsc_categories_cust_desc_source_system'),)
        managed = True
        db_table = 'MMD_UNSPSC_CATEGORIES_CUST_DESC'

    @staticmethod
    def get_prod_cat_by_desc(fname):
        if '*' in fname:
            requester = re.search(r'[a-zA-Z0-9]+', fname)
            if fname[0] == '*' and fname[-1] == '*':
                queryset = UnspscCategoriesCustDesc.objects.values_list('prod_cat_id', flat=False).filter(
                    category_desc__icontains=requester.group(0), client=global_variables.GLOBAL_CLIENT,
                    del_ind=False)
            elif fname[0] == '*':
                queryset = UnspscCategoriesCustDesc.objects.values_list('prod_cat_id', flat=False).filter(
                    category_desc__iendswith=requester.group(0), client=global_variables.GLOBAL_CLIENT,
                    del_ind=False)
            else:
                queryset = UnspscCategoriesCustDesc.objects.values_list('prod_cat_id', flat=False).filter(
                    category_desc__istartswith=requester.group(0),
                    client=global_variables.GLOBAL_CLIENT,
                    del_ind=False)

        else:
            queryset = UnspscCategoriesCustDesc.objects.values_list('prod_cat_id', flat=False).filter(
                category_desc=fname,
                client=global_variables.GLOBAL_CLIENT,
                del_ind=False)
        prod_cat_list = []
        for field in queryset:
            prod_cat_list.append(field[0])
        return prod_cat_list


class UnspscCategoriesCustDescHistory(models.Model):
    prod_cat_desc_key = models.AutoField(primary_key=True, db_column='PROD_CAT_DESC_KEY', null=False)
    prod_cat_desc_guid = models.CharField(db_column='PROD_CAT_DESC_GUID', max_length=32, null=False)
    category_desc = models.CharField(db_column='CATEGORY_DESC', max_length=200, blank=True, null=True,
                                     verbose_name='Category Description')
    unspsc_categories_cust_desc_created_by = models.CharField(db_column='UNSPSC_CATEGORIES_CUST_DESC_CREATED_BY',
                                                              max_length=30, null=True)
    unspsc_categories_cust_desc_created_at = models.DateTimeField(db_column='UNSPSC_CATEGORIES_CUST_DESC_CREATED_AT',
                                                                  max_length=50, null=True)
    unspsc_categories_cust_desc_changed_by = models.CharField(db_column='UNSPSC_CATEGORIES_CUST_DESC_CHANGED_BY',
                                                              max_length=30, null=True)
    unspsc_categories_cust_desc_changed_at = models.DateTimeField(db_column='UNSPSC_CATEGORIES_CUST_DESC_CHANGED_AT',
                                                                  max_length=50, null=True)
    unspsc_categories_cust_desc_source_system = models.CharField(db_column='UNSPSC_CATEGORIES_CUST_DESC_SOURCE_SYSTEM',
                                                                 max_length=20)

    del_ind = models.BooleanField(default=False, null=False)
    client = models.CharField(max_length=8, db_column='CLIENT', null=True)
    language_id = models.CharField(db_column='LANGUAGE_ID', null=True, max_length=2)
    prod_cat_id = models.CharField(db_column='PROD_CAT_ID', null=True, max_length=20, verbose_name='Product Category')

    class Meta:
        managed = True
        db_table = 'MMD_UNSPSC_CATEGORIES_CUST_DESC_HISTORY'


class WorkflowACC(models.Model):
    workflow_acc_guid = models.CharField(primary_key=True, db_column='WORKFLOW_ACC_GUID', max_length=32)
    acc_value = models.CharField(db_column='ACC_VALUE', max_length=40, null=False)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    app_username = models.CharField(db_column='APP_USERNAME', max_length=16, null=False)
    sup_company_id = models.CharField(db_column='SUP_COMPANY_ID', max_length=8, null=False)
    sup_acc_value = models.CharField(db_column='SUP_ACC_VALUE', max_length=40, null=False)
    workflow_acc_created_by = models.CharField(db_column='WORKFLOW_ACC_CREATED_BY', max_length=30, null=True)
    workflow_acc_created_at = models.DateTimeField(db_column='WORKFLOW_ACC_CREATED_AT', max_length=50, null=True)
    workflow_acc_changed_by = models.CharField(db_column='WORKFLOW_ACC_CHANGED_BY', max_length=30, null=True)
    workflow_acc_changed_at = models.DateTimeField(db_column='WORKFLOW_ACC_CHANGED_AT', max_length=50, null=True)
    workflow_acc_source_system = models.CharField(db_column='WORKFLOW_ACC_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    account_assign_cat = models.ForeignKey('eProc_Configuration.AccountAssignmentCategory', models.DO_NOTHING,
                                           db_column='ACCOUNT_ASSIGN_CAT', related_name='acc_assign_cat',
                                           null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    currency_id = models.ForeignKey('eProc_Configuration.Currency', models.DO_NOTHING, db_column='CURRENCY_ID')
    sup_account_assign_cat = models.ForeignKey('eProc_Configuration.AccountAssignmentCategory', models.DO_NOTHING,
                                               db_column='SUP_ACCOUNT_ASSIGN_CAT', related_name='sup_acc_assign_cat',
                                               null=False)

    class Meta:
        managed = True
        db_table = 'MMD_WF_ACC'


class WorkflowACCHistory(models.Model):
    workflow_acc_key = models.AutoField(primary_key=True, db_column='WORKFLOW_ACC_KEY', null=False)
    workflow_acc_guid = models.CharField(db_column='WORKFLOW_ACC_GUID', max_length=32)
    acc_value = models.CharField(db_column='ACC_VALUE', max_length=40, null=False)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    app_username = models.CharField(db_column='APP_USERNAME', max_length=16, null=False)
    sup_company_id = models.CharField(db_column='SUP_COMPANY_ID', max_length=8, null=False)
    sup_acc_value = models.CharField(db_column='SUP_ACC_VALUE', max_length=40, null=False)
    workflow_acc_created_by = models.CharField(db_column='WORKFLOW_ACC_CREATED_BY', max_length=30, null=True)
    workflow_acc_created_at = models.DateTimeField(db_column='WORKFLOW_ACC_CREATED_AT', max_length=50, null=True)
    workflow_acc_changed_by = models.CharField(db_column='WORKFLOW_ACC_CHANGED_BY', max_length=30, null=True)
    workflow_acc_changed_at = models.DateTimeField(db_column='WORKFLOW_ACC_CHANGED_AT', max_length=50, null=True)
    workflow_acc_source_system = models.CharField(db_column='WORKFLOW_ACC_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    account_assign_cat = models.CharField(db_column='ACCOUNT_ASSIGN_CAT', max_length=10, null=True,
                                          verbose_name='AccountAssignmentCat')
    client = models.CharField(max_length=8, db_column='CLIENT', null=True)
    currency_id = models.CharField(db_column='CURRENCY_ID', null=True, max_length=3)
    sup_acc_assign_cat = models.CharField(db_column='SUP_ACC_ASSIGN_CAT', max_length=10, null=True,
                                          verbose_name='AccountAssignmentCat')

    class Meta:
        managed = True
        db_table = 'MMD_WF_ACC_HISTORY'
