import os

from django.db import models

from eProc_Configuration.models.development_data import OrgClients


class AccountAssignmentCategoryCust(models.Model):
    """
    Contains AccountAssignmentCategory List for user settings
    """
    acc_cat_cust_guid = models.CharField(db_column='ACC_CAT_CUST_GUID', max_length=32, primary_key=True)
    acc_cat_cust = models.CharField(db_column='ACC_CAT_CUST', max_length=5,
                                    verbose_name='AccountAssignmentCat')
    acc_cat_cust_description = models.CharField(db_column='ACC_CAT_CUST_DESCRIPTION', max_length=255, null=True,
                                                verbose_name='description')
    acc_cat_cust_created_by = models.CharField(db_column='ACC_CAT_CUST_CREATED_BY', max_length=30, null=True)
    acc_cat_cust_created_at = models.DateTimeField(db_column='ACC_CAT_CUST_CREATED_AT', max_length=50, null=True)
    acc_cat_cust_changed_by = models.CharField(db_column='ACC_CAT_CUST_CHANGED_BY', max_length=30, null=True)
    acc_cat_cust_changed_at = models.DateTimeField(db_column='ACC_CAT_CUST_CHANGED_AT', max_length=50, null=True)
    acc_cat_cust_source_system = models.CharField(db_column='ACC_CAT_CUST_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    account_assign_cat = models.ForeignKey('eProc_Configuration.AccountAssignmentCategory', on_delete=models.PROTECT,
                                           null=True, db_column='ACCOUNT_ASSIGN_CAT')
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=True,
                               db_column='CLIENT')

    class Meta:
        db_table = "MAD_ACC_AST_CAT_CUST"
        unique_together = ('client', 'acc_cat_cust_source_system', 'acc_cat_cust')
        managed = True


class CalenderConfig(models.Model):
    calender_config_guid = models.CharField(db_column='CALENDER_CONFIG_GUID', max_length=32, primary_key=True)
    calender_id = models.CharField(db_column='CALENDER_ID', max_length=10)
    description = models.CharField(db_column='DESCRIPTION', max_length=1000, null=False)
    year = models.CharField(db_column='YEAR', max_length=4, null=False)
    working_days = models.CharField(db_column='WORKING_DAYS', max_length=30, null=False)
    calender_config_created_at = models.DateTimeField(db_column='CALENDER_CONFIG_CREATED_AT', blank=False, null=True)
    calender_config_created_by = models.CharField(db_column='CALENDER_CONFIG_CREATED_BY', max_length=12, blank=False,
                                                  null=True)
    calender_config_changed_at = models.DateTimeField(db_column='CALENDER_CONFIG_CHANGED_AT', blank=True, null=True)
    calender_config_changed_by = models.CharField(db_column='CALENDER_CONFIG_CHANGED_BY', max_length=12, blank=False,
                                                  null=True)
    del_ind = models.BooleanField(db_column='DEL_IND', default=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False,
                               db_column='CLIENT')
    country_code = models.ForeignKey('eProc_Configuration.Country', db_column='COUNTRY_CODE', on_delete=models.PROTECT,
                                     verbose_name='country_code', null=True)

    class Meta:
        db_table = 'MAD_CALENDER_CONFIG'
        unique_together = ('client', 'calender_id', 'year', 'country_code')
        managed = True

    def __str__(self):
        return self.calender_id


class CalenderHolidays(models.Model):
    calender_holiday_guid = models.CharField(db_column='CALENDER_HOLIDAY_GUID', max_length=32, primary_key=True)
    holiday_description = models.CharField(db_column='DESCRIPTION', max_length=1000, null=False)
    from_date = models.DateField(db_column='FROM_DATE', null=False)
    to_date = models.DateField(db_column='TO_DATE', null=False)
    calender_id = models.CharField(db_column='CALENDER_ID', max_length=10)
    created_by = models.CharField(db_column='CREATED_BY', max_length=30, null=True)
    created_at = models.DateTimeField(db_column='CREATED_AT', max_length=50, null=True)
    changed_by = models.CharField(db_column='CHANGED_BY', max_length=30, null=True)
    changed_at = models.DateTimeField(db_column='CHANGED_AT', max_length=50, null=True)
    del_ind = models.BooleanField(db_column='DEL_IND', default=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False,
                               db_column='CLIENT')

    class Meta:
        db_table = 'MAD_CALENDER_HOLIDAYS'
        managed = True


class CatalogMapping(models.Model):
    catalog_mapping_guid = models.CharField(db_column='CATALOG_MAPPING_GUID', primary_key=True, max_length=32,
                                            null=False, default=None)
    catalog_id = models.CharField(db_column='CATALOG_ID', null=False, default=None, max_length=16)
    item_id = models.CharField(db_column="ITEM_ID", max_length=16, null=True)
    call_off = models.CharField(db_column='CALL_OFF', max_length=15, null=True)
    catalogs_mapping_source_system = models.CharField(db_column='CATALOGS_PRODUCT_MAPPING_SOURCE_SYSTEM',
                                                      max_length=20)
    catalogs_mapping_created_by = models.CharField(db_column='CATALOGS_MAPPING_CREATED_BY',
                                                   max_length=30, null=True)
    catalogs_mapping_created_at = models.DateTimeField(db_column='CATALOGS_MAPPING_CREATED_AT',
                                                       max_length=50, null=True)
    catalogs_mapping_changed_by = models.CharField(db_column='CATALOGS_MAPPING_CHANGED_BY',
                                                   max_length=30, null=True)
    catalogs_mapping_changed_at = models.DateTimeField(db_column='CATALOGS_MAPPING_CHANGED_AT',
                                                       max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        managed = True
        unique_together = ('client', 'item_id', 'catalog_id', 'catalogs_mapping_source_system')
        db_table = 'MAD_CATALOG_MAP'


class CountryCompCode(models.Model):
    """
    Contains company code description
    """
    country_comp_code_guid = models.CharField(db_column='COUNTRY_COMP_CODE_GUID', primary_key=True, max_length=32)
    company_code_id = models.CharField(db_column='COMPANY_CODE_ID', max_length=20, null=False)
    country_comp_code_created_by = models.CharField(db_column='COUNTRY_COMP_CODE_CREATED_BY', max_length=30, null=True)
    country_comp_code_created_at = models.DateTimeField(db_column='COUNTRY_COMP_CODE_CREATED_AT', max_length=50,
                                                        null=True)
    country_comp_code_changed_by = models.CharField(db_column='COUNTRY_COMP_CODE_CHANGED_BY', max_length=30, null=True)
    country_comp_code_changed_at = models.DateTimeField(db_column='COUNTRY_COMP_CODE_CHANGED_AT', max_length=50,
                                                        null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', db_column='CLIENT', on_delete=models.PROTECT,
                               null=False)
    country = models.ForeignKey('eProc_Configuration.Country', db_column='COUNTRY', on_delete=models.PROTECT,
                                null=False)

    class Meta:
        db_table = "MAD_COUNTRY_COMP_CODE"
        unique_together = ('client', 'company_code_id')
        managed = True


class CompanyGrpUser(models.Model):
    """
    Contains company code description
    """
    company_grp_user_guid = models.CharField(db_column='COMPANY_GRP_USER_GUID', primary_key=True, max_length=32)
    company_grp_id = models.CharField(db_column='COMPANY_GRP_ID', max_length=20, null=False)
    username = models.CharField(db_column='USERNAME', max_length=16, null=False)
    company_grp_user_created_by = models.CharField(db_column='COMPANY_GRP_USER_CREATED_BY', max_length=30, null=True)
    company_grp_user_created_at = models.DateTimeField(db_column='COMPANY_GRP_USER_CREATED_AT', max_length=50,
                                                       null=True)
    company_grp_user_changed_by = models.CharField(db_column='COMPANY_GRP_USER_CHANGED_BY', max_length=30, null=True)
    company_grp_user_changed_at = models.DateTimeField(db_column='COMPANY_GRP_USER_CHANGED_AT', max_length=50,
                                                       null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', db_column='Client', on_delete=models.PROTECT,
                               null=False)

    class Meta:
        db_table = "MAD_COMP_CODE_GRP_USER"
        managed = True

    def __str__(self):
        return self.company_grp_id


class CompanyCodeGrp(models.Model):
    """
    Contains company code description
    """
    company_grp_guid = models.CharField(db_column='COMPANY_GUID', primary_key=True, max_length=32)
    company_grp_id = models.CharField(db_column='COMPANY_GRP_ID', max_length=20, null=False)
    company_code_id = models.CharField(db_column='COMPANY_CODE_ID', max_length=20, null=False)
    company_code_grp_created_by = models.CharField(db_column='COMPANY_CODE_GRP_CREATED_BY', max_length=30, null=True)
    company_code_grp_created_at = models.DateTimeField(db_column='COMPANY_CODE_GRP_CREATED_AT', max_length=50,
                                                       null=True)
    company_code_grp_changed_by = models.CharField(db_column='COMPANY_CODE_GRP_CHANGED_BY', max_length=30, null=True)
    company_code_grp_changed_at = models.DateTimeField(db_column='COMPANY_CODE_GRP_CHANGED_AT', max_length=50,
                                                       null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', db_column='CLIENT', on_delete=models.PROTECT,
                               null=False)

    class Meta:
        db_table = "MAD_COMP_CODE_GRP"
        managed = True

    def __str__(self):
        return self.company_grp_id


class DiscountData(models.Model):
    discount_data_guid = models.CharField(db_column='DISCOUNT_DATA_GUID', primary_key=True,
                                          max_length=40,
                                          blank=False, null=False)
    discount_id = models.CharField(db_column='DISCOUNT_ID', max_length=40, blank=False, null=True)
    product_id = models.CharField(db_column="PRODUCT_ID", max_length=16, null=True)
    discount_name = models.CharField(db_column='DISCOUNT_NAME', max_length=500, blank=False, null=True)
    quantity = models.CharField(db_column="quantity", max_length=30, null=True)
    discount_percentage = models.DecimalField(db_column='DISCOUNT_PERCENTAGE', max_digits=15, decimal_places=2,
                                              null=True)
    discount_data_created_at = models.DateTimeField(db_column='DISCOUNT_DATA_CREATED_AT', blank=False,
                                                    null=True)
    discount_data_created_by = models.CharField(db_column='DISCOUNT_DATA_CREATED_BY', max_length=12,
                                                blank=False, null=True)
    discount_data_changed_at = models.DateTimeField(db_column='DISCOUNT_DATA_CHANGED_AT', blank=True,
                                                    null=True)
    discount_data_changed_by = models.CharField(db_column='DISCOUNT_DATA_CHANGED_BY', max_length=12,
                                                blank=False, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        managed = True
        db_table = "MAD_DISCOUNT_DATA"


class DocumentTypeCust(models.Model):
    document_type_cust_guid = models.CharField(db_column='DOCUMENT_TYPE_CUST_GUID', primary_key=True, max_length=32,
                                               null=False, default=None)
    document_type_cust_desc = models.CharField(db_column='DOCUMENT_TYPE_CUST_DESC', max_length=30, null=False)
    document_type_cust_created_by = models.CharField(db_column='DOCUMENT_TYPE_CREATED_BY', max_length=30, null=True)
    document_type_cust_created_at = models.DateTimeField(db_column='DOCUMENT_TYPE_CREATED_AT', max_length=50, null=True)
    document_type_cust_changed_by = models.CharField(db_column='DOCUMENT_TYPE_CHANGED_BY', max_length=30, null=True)
    document_type_cust_changed_at = models.DateTimeField(db_column='DOCUMENT_TYPE_CHANGED_AT', max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    document_type = models.ForeignKey('eProc_Configuration.DocumentType', models.DO_NOTHING, db_column='DOCUMENT_TYPE')

    class Meta:
        db_table = "MAD_DOCUMENT_TYPE_CUST"
        unique_together = ('client', 'document_type')
        managed = True


class EformFieldConfig(models.Model):
    # FREETEXT with eform and without eform
    # PRODUCT with eform
    eform_field_config_guid = models.CharField(db_column='EFORM_FIELD_CONFIG_GUID', primary_key=True, max_length=40,
                                               blank=False,
                                               null=False)
    eform_id = models.CharField(db_column='EFORM_ID', max_length=40, blank=False, null=True)
    eform_type = models.CharField(db_column='EFORM_TYPE', max_length=40, blank=False,
                                  null=False)  # CATALOG_ITEM_EFORM,FT_ITEM_EFORM
    eform_field_count = models.PositiveIntegerField(db_column='EFORM_FIELD_COUNT', blank=False, null=False,
                                                    verbose_name='field count', default=0)
    eform_field_name = models.CharField(db_column='EFORM_FIELD_NAME', null=True, max_length=200)
    eform_field_datatype = models.CharField(db_column='EFORM_FIELD_DATATYPE', null=True,
                                            max_length=50)  # input field datatype ex.. dropdown checkbox text,num
    eform_field_data = models.CharField(db_column='EFORM_FIELD_DATA', null=True, max_length=1000)
    default_eform_field_data = models.CharField(db_column='DEFAULT_EFORM_FIELD_DATA', null=True, max_length=100)
    required_flag = models.BooleanField(db_column='REQUIRED_FLAG', null=True)
    specialchar_flag = models.BooleanField(db_column='SPECIALCHAR_FLAG', null=True)
    # display_flag 0- nothing,1- only display the detail (non editable)
    display_flag = models.BooleanField(db_column='DISPLAY_FLAG', null=True, default=False)
    dropdown_pricetype = models.CharField(db_column='DROPDOWN_PRICETYPE', null=True,
                                          max_length=50)  # with price without price quantity
    # pricing_flag 0 - get price from product details, 1 - get price from ProductPricing
    price_flag = models.BooleanField(db_column='PRICE_FLAG', null=True, default=False)
    eform_field_config_created_at = models.DateTimeField(db_column='EFORM_FIELD_CONFIG_CREATED_AT', blank=False,
                                                         null=True)
    eform_field_config_created_by = models.CharField(db_column='EFORM_FIELD_CONFIG_CREATED_BY', max_length=12,
                                                     blank=False, null=True)
    eform_field_config_changed_at = models.DateTimeField(db_column='EFORM_FIELD_CONFIG_CHANGED_AT', blank=True,
                                                         null=True)
    eform_field_config_changed_by = models.CharField(db_column='EFORM_FIELD_CONFIG_CHANGED_BY', max_length=12,
                                                     blank=False, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        unique_together = ('client', 'eform_id', 'eform_field_count')
        db_table = "MAD_EFORM_FIELD_CONFIG"


class EmailObjectTypes(models.Model):
    """
    Contains keywords based on object type
    """
    email_object_types_guid = models.CharField(primary_key=True, db_column='EMAIL_OBJECT_TYPES_GUID', max_length=32)
    object_type = models.CharField(db_column='OBJECT_TYPE', max_length=20, null=False)
    email_object_types_created_by = models.CharField(db_column='EMAIL_OBJECT_TYPES_CREATED_BY', max_length=30,
                                                     null=True)
    email_object_types_created_at = models.DateTimeField(db_column='EMAIL_OBJECT_TYPES_CREATED_AT', max_length=50,
                                                         null=True)
    email_object_types_changed_by = models.CharField(db_column='EMAIL_OBJECT_TYPES_CHANGED_BY', max_length=30,
                                                     null=True)
    email_object_types_changed_at = models.DateTimeField(db_column='EMAIL_OBJECT_TYPES_CHANGED_AT', max_length=50,
                                                         null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        unique_together = ('object_type', 'client')
        db_table = "MAD_EMAIL_OBJECT_TYPES"
        managed = True


class EmailKeywords(models.Model):
    """
    Contains keywords based on object type
    """
    email_keywords_guid = models.CharField(primary_key=True, db_column='EMAIL_KEYWORDS_GUID', max_length=32)
    object_type = models.CharField(db_column='OBJECT_TYPE', max_length=20, null=False)
    keyword = models.CharField(db_column='KEYWORD', max_length=30, null=False)
    email_keywords_created_by = models.CharField(db_column='EMAIL_KEYWORDS_CREATED_BY', max_length=30,
                                                 null=True)
    email_keywords_created_at = models.DateTimeField(db_column='EMAIL_KEYWORDS_CREATED_AT', max_length=50,
                                                     null=True)
    email_keywords_changed_by = models.CharField(db_column='EMAIL_KEYWORDS_CHANGED_BY', max_length=30,
                                                 null=True)
    email_keywords_changed_at = models.DateTimeField(db_column='EMAIL_KEYWORDS_CHANGED_AT', max_length=50,
                                                     null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = "MAD_EMAIL_KEYWORDS"
        managed = True


class EmailContents(models.Model):
    """
    Contains notification & email format data
    """
    email_contents_guid = models.CharField(primary_key=True, db_column='EMAIL_CONTENTS_GUID', max_length=32)
    object_type = models.CharField(db_column='OBJECT_TYPE', max_length=20, null=False)
    subject = models.TextField(db_column='SUBJECT', null=False)
    header = models.TextField(db_column='HEADER', null=True, blank=True)
    body = models.TextField(db_column='BODY', null=False)
    footer = models.TextField(db_column='FOOTER', null=True, blank=True)
    email_contents_created_by = models.CharField(db_column='EMAIL_CONTENTS_CREATED_BY', max_length=30,
                                                 null=True)
    email_contents_created_at = models.DateTimeField(db_column='EMAIL_CONTENTS_CREATED_AT', max_length=50,
                                                     null=True)
    email_contents_changed_by = models.CharField(db_column='EMAIL_CONTENTS_CHANGED_BY', max_length=30,
                                                 null=True)
    email_contents_changed_at = models.DateTimeField(db_column='EMAIL_CONTENTS_CHANGED_AT', max_length=50,
                                                     null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    language_id = models.ForeignKey('eProc_Configuration.Languages', db_column='LANGUAGE_ID', on_delete=models.PROTECT,
                                    null=False)

    class Meta:
        db_table = "MAD_EMAIL_CONTENTS"
        unique_together = ('object_type', 'language_id', 'client')
        managed = True


class PoSplitType(models.Model):
    po_split_type = models.PositiveIntegerField(db_column='PO_SPLIT_TYPE', primary_key=True)
    # 01 - Supplier,02 - Currency,03 - Ship to address,04 - Purchasing Group, 05 - CallOff, 06 - Limit Order,
    # 07 - Purchase Requision,08- Incoterm,09 - Payment Terms,10 - product type
    po_split_type_desc = models.CharField(db_column='PO_SPLIT_TYPE_DESC', max_length=30, null=False)
    po_split_type_created_by = models.CharField(db_column='PO_SPLIT_TYPE_CREATED_BY', max_length=30,
                                                null=True)
    po_split_type_created_at = models.DateTimeField(db_column='PO_SPLIT_TYPE_CREATED_AT', max_length=50,
                                                    null=True)
    po_split_type_changed_by = models.CharField(db_column='PO_SPLIT_TYPE_CHANGED_BY', max_length=30,
                                                null=True)
    po_split_type_changed_at = models.DateTimeField(db_column='PO_SPLIT_TYPE_CHANGED_AT', max_length=50,
                                                    null=True)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "MAD_PO_SPLIT_TYPE"
        managed = True


class PoSplitGroupType(models.Model):
    po_split_group_type = models.PositiveIntegerField(db_column='PO_SPLIT_GROUP_TYPE', primary_key=True)
    # 01 - Supplier,02 - Currency,03 - Ship to address,04 - Purchasing Group, 05 - CallOff, 06 - Limit Order,
    # 07 - Purchase Requision,08- Incoterm,09 - Payment Terms,10 - product type
    po_split_group_type_desc = models.CharField(db_column='PO_SPLIT_GROUP_TYPE_DESC', max_length=30, null=False)
    po_split_group_type_created_by = models.CharField(db_column='PO_SPLIT_GROUP_TYPE_CREATED_BY', max_length=30,
                                                      null=True)
    po_split_group_type_created_at = models.DateTimeField(db_column='PO_SPLIT_GROUP_TYPE_CREATED_AT', max_length=50,
                                                          null=True)
    po_split_group_type_changed_by = models.CharField(db_column='PO_SPLIT_GROUP_TYPE_CHANGED_BY', max_length=30,
                                                      null=True)
    po_split_group_type_changed_at = models.DateTimeField(db_column='PO_SPLIT_GROUP_TYPE_CHANGED_AT', max_length=50,
                                                          null=True)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "MAD_SPLIT_GROUP_TYPE"
        managed = True


class PoSplitCriteria(models.Model):
    po_split_criteria_guid = models.CharField(db_column='PO_SPLIT_CRITERIA_GUID', max_length=32, primary_key=True)
    company_code_id = models.CharField(db_column='COMPANY_CODE_ID', max_length=20, null=False)
    activate = models.BooleanField(db_column='ACTIVATE', default=False, null=False)
    del_ind = models.BooleanField(default=False, null=False)
    po_split_criteria_created_by = models.CharField(db_column='PO_SPLIT_CRITERIA_CREATED_BY', max_length=30,
                                                    null=True)
    po_split_criteria_created_at = models.DateTimeField(db_column='PO_SPLIT_CRITERIA_CREATED_AT', max_length=50,
                                                        null=True)
    po_split_criteria_changed_by = models.CharField(db_column='PO_SPLIT_CRITERIA_CHANGED_BY', max_length=30,
                                                    null=True)
    po_split_criteria_changed_at = models.DateTimeField(db_column='PO_SPLIT_CRITERIA_CHANGED_AT', max_length=50,
                                                        null=True)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    po_split_type = models.ForeignKey('eProc_Configuration.PoSplitType', on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = "MAD_PO_SPLIT_CRITERIA"
        managed = True


class PoGroupCriteria(models.Model):
    po_group_criteria_guid = models.CharField(db_column='PO_GROUP_CRITERIA_GUID', max_length=32, primary_key=True)
    company_code_id = models.CharField(db_column='COMPANY_CODE_ID', max_length=20, null=False)
    activate = models.BooleanField(db_column='ACTIVATE', default=False, null=False)
    del_ind = models.BooleanField(default=False, null=False)
    po_group_criteria_created_by = models.CharField(db_column='PO_GROUP_CRITERIA_CREATED_BY', max_length=30,
                                                    null=True)
    po_group_criteria_created_at = models.DateTimeField(db_column='PO_GROUP_CRITERIA_CREATED_AT', max_length=50,
                                                        null=True)
    po_group_criteria_changed_by = models.CharField(db_column='PO_GROUP_CRITERIA_CHANGED_BY', max_length=30,
                                                    null=True)
    po_group_criteria_changed_at = models.DateTimeField(db_column='PO_GROUP_CRITERIA_CHANGED_AT', max_length=50,
                                                        null=True)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    po_split_group_type = models.ForeignKey('eProc_Configuration.PoSplitGroupType', on_delete=models.PROTECT,
                                            null=False)

    class Meta:
        db_table = "MAD_PO_GROUP_CRITERIA"
        managed = True


class ProductInfo(models.Model):
    product_info_guid = models.CharField(db_column='PRODUCT_INFO_GUID', primary_key=True, max_length=40, blank=False,
                                         null=False)
    product_info_id = models.CharField(db_column='PRODUCT_INFO_ID', max_length=40, blank=False, null=True)
    product_id = models.CharField(db_column="PRODUCT_ID", max_length=16, null=True)
    product_info_type = models.CharField(db_column="PRODUCT_INFO_TYPE", max_length=16, null=True)
    product_info_key = models.CharField(db_column='PRODUCT_INFO_KEY', max_length=200, blank=False, null=True)
    product_info_value = models.CharField(db_column='PRODUCT_INFO_VALUE', max_length=200, blank=False, null=True)
    product_info_created_at = models.DateTimeField(db_column='PRODUCT_INFO_CREATED_AT', blank=False, null=True)
    product_info_created_by = models.CharField(db_column='PRODUCT_INFO_CREATED_BY', max_length=12, blank=False,
                                               null=True)
    product_info_changed_at = models.DateTimeField(db_column='PRODUCT_INFO_CHANGED_AT', blank=True, null=True)
    product_info_changed_by = models.CharField(db_column='PRODUCT_INFO_CHANGED_BY', max_length=12, blank=False,
                                               null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = "MAD_PRODUCT_INFO"
        managed = True


class ProductEformPricing(models.Model):
    product_eform_pricing_guid = models.CharField(db_column='PRODUCT_EFORM_PRICING_GUID', primary_key=True,
                                                  max_length=40,
                                                  blank=False, null=False)
    eform_id = models.CharField(db_column='EFORM_ID', max_length=40, blank=False, null=True)
    pricing_type = models.CharField(db_column="PRICING_TYPE", max_length=30, null=True)  # base,additional,QUANTITY
    pricing_data = models.CharField(db_column="PRICING_DATA", max_length=30, null=True)
    pricing_data_default = models.BooleanField(db_column='PRICING_DATA_DEFAULT', default=False,
                                               null=False)
    price = models.DecimalField(db_column='PRICE', max_digits=15, decimal_places=2, null=True)
    price_unit = models.CharField(db_column='PRICE_UNIT', default="1", max_length=5, null=True)
    operator = models.CharField(db_column="OPERATOR", max_length=16, null=True)  # plus,minus, percentage
    product_description = models.CharField(db_column='PRODUCT_DESCRIPTION', max_length=500, blank=False, null=True,
                                           verbose_name='Product Short Description')

    product_eform_pricing_created_at = models.DateTimeField(db_column='PRODUCT_EFORM_PRICING_CREATED_AT', blank=False,
                                                            null=True)
    product_eform_pricing_created_by = models.CharField(db_column='PRODUCT_EFORM_PRICING_CREATED_BY', max_length=12,
                                                        blank=False, null=True)
    product_eform_pricing_changed_at = models.DateTimeField(db_column='PRODUCT_EFORM_PRICING_CHANGED_AT', blank=True,
                                                            null=True)
    product_eform_pricing_changed_by = models.CharField(db_column='PRODUCT_EFORM_PRICING_CHANGED_BY', max_length=12,
                                                        blank=False, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    eform_field_config_guid = models.ForeignKey(EformFieldConfig, on_delete=models.PROTECT, null=True)
    variant_config_guid = models.ForeignKey('eProc_Configuration.VariantConfig', on_delete=models.PROTECT, null=True)

    class Meta:
        managed = True
        db_table = "MAD_PRODUCT_EFORM_PRICING"


# class EformFieldDetails(models.Model):
#     # FREETEXT with eform and without eform REMOVE
#     # PRODUCT with eform
#     eform_field_details_guid = models.CharField(db_column='EFORM_FIELD_DETAILS_GUID', primary_key=True, max_length=40,
#                                                 blank=False,
#                                                 null=False)
#     eform_id = models.CharField(db_column='EFORM_ID', max_length=40, blank=False, null=True)
#     eform_type = models.CharField(db_column='EFORM_TYPE', max_length=40, blank=False, null=False)
#     eform_field_count = models.PositiveIntegerField(db_column='EFORM_FIELD_COUNT', blank=False, null=False,
#                                                     verbose_name='field count', default=0)
#     supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=10, verbose_name='Vendor Id', null=True)
#     prod_cat_id = models.CharField(db_column='PROD_CAT_ID', max_length=50, null=True, default=None)
#     supp_art_no = models.CharField(db_column='SUPP_ART_NO', max_length=40, blank=False, null=True)
#     lead_time = models.CharField(db_column='LEAD_TIME', null=True, max_length=20)
#     description = models.CharField(db_column='DESCRIPTION', max_length=255, null=True, default=None)
#     eform_field = models.CharField(db_column='EFORM_FIELD', null=True, max_length=200)
#     required_field_flag = models.BooleanField(db_column='REQUIRED_FIELD_FLAG', null=True)
#     input_type = models.CharField(db_column='INPUT_TYPE', null=True, max_length=50)
#     drop_down_type = models.CharField(db_column='DROP_DOWN_TYPE', null=True, max_length=50)
#     input_data = models.CharField(db_column='INPUT_DATA', null=True, max_length=1000)
#     default_input_data = models.CharField(db_column='DEFAULT_INPUT_DATA', null=True, max_length=100)
#     special_char_flag = models.BooleanField(db_column='SPECIAL_CHAR_FLAG', null=True)
#     # display_flag 0- nothing,1- only display the detail (non editable)
#     display_flag = models.BooleanField(db_column='DISPLAY_FLAG', null=True, default=False)
#     # pricing_flag 0 - get price from product details, 1 - get price from ProductPricing
#     pricing_flag = models.BooleanField(db_column='PRICING_FLAG', null=True, default=False)
#     eform_field_created_at = models.DateTimeField(db_column='EFORM_FIELD_CREATED_AT', blank=False, null=True)
#     eform_field_created_by = models.CharField(db_column='EFORM_FIELD_CREATED_BY', max_length=12, blank=False, null=True)
#     eform_field_changed_at = models.DateTimeField(db_column='EFORM_FIELD_CHANGED_AT', blank=True, null=True)
#     eform_field_changed_by = models.CharField(db_column='EFORM_FIELD_CHANGED_BY', max_length=12, blank=False, null=True)
#     del_ind = models.BooleanField(default=False, null=False)
#     client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
#
#     class Meta:
#         unique_together = ('client', 'supplier_id', 'prod_cat_id', 'eform_field_count')
#         db_table = "MAD_EFORM_FIELD_DEATILS"
#
#
# class EformProductPricing(models.Model):
#     eform_product_pricing_guid = models.CharField(db_column='EFORM_PRODUCT_PRICING_GUID', primary_key=True,
#                                                   max_length=40,
#                                                   blank=False, null=False)
#     pricing_eform_product_id = models.CharField(db_column="PRICING_EFORM_PRODUCT_ID", max_length=16, null=True)
#     price_type = models.CharField(db_column="PRICE_TYPE", max_length=16, null=True)  # DIRECT,DIFFERENTIAL,QUANTITY
#     price_data = models.CharField(db_column="PRICE_DATA", max_length=16, null=True)
#     price = models.DecimalField(db_column='PRICE', max_digits=15, decimal_places=2, null=True)
#     price_unit = models.CharField(db_column='PRICE_UNIT', max_length=5, null=True)
#     default_pricing_flag = models.BooleanField(db_column='DEFAULT_PRICING_FLAG', default=False,
#                                                null=False)
#     differential_pricing_flag = models.BooleanField(db_column='DIFFERENTIAL_PRICING_FLAG', default=False,
#                                                     null=False)  # False -  non differential true - differential pricing
#     operator = models.CharField(db_column="OPERATOR", max_length=16, null=True)  # plus,minus, percentage
#     del_ind = models.BooleanField(default=False, null=False)
#     client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
#     eform_field_details_guid = models.ForeignKey(EformFieldDetails, on_delete=models.PROTECT, null=True)
#     unit = models.ForeignKey('eProc_Configuration.UnitOfMeasures', db_column='UNIT_OF_MEASURE', null=True,
#                              on_delete=models.PROTECT)
#
#     class Meta:
#         managed = True
#         db_table = "MAD_EFORM_PRODUCT_PRICING"

class PurchaseControl(models.Model):
    purchase_control_guid = models.CharField(db_column='PURCHASE_CONTROL_GUID', max_length=32, primary_key=True)
    company_code_id = models.CharField(db_column='COMPANY_CODE_ID', max_length=20, null=False)
    call_off = models.CharField(db_column='CALL_OFF', max_length=15, null=True)
    purchase_ctrl_flag = models.BooleanField(db_column='PURCHASE_CTRL_FLAG', default=False, null=False)
    prod_cat_id = models.CharField(db_column='PROD_CAT_ID', max_length=50, null=False, default=None)
    del_ind = models.BooleanField(default=False, null=False)
    purchase_control_created_by = models.CharField(db_column='PURCHASE_CONTROL_CREATED_BY', max_length=30,
                                                   null=True)
    purchase_control_created_at = models.DateTimeField(db_column='PURCHASE_CONTROL_CREATED_AT', max_length=50,
                                                       null=True)
    purchase_control_changed_by = models.CharField(db_column='PURCHASE_CONTROL_CHANGED_BY', max_length=30,
                                                   null=True)
    purchase_control_changed_at = models.DateTimeField(db_column='PURCHASE_CONTROL_CHANGED_AT', max_length=50,
                                                       null=True)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = "MAD_PURCHASE_CONTROL"
        managed = True


class ProjectDetails(models.Model):
    project_detail_guid = models.CharField(db_column='PROJECT_DETAIL_GUID', primary_key=True, max_length=32)
    project_id = models.CharField(db_column='PROJECT_ID', max_length=20)
    project_name = models.CharField(db_column='PROJECT_NAME', max_length=30, null=False, blank=False)
    project_desc = models.CharField(db_column='PROJECT_DESC', max_length=255, null=False)
    start_date = models.DateField(db_column='START_DATE', null=False)
    end_date = models.DateField(db_column='END_DATE', null=False)
    del_ind = models.BooleanField(db_column='DEL_IND', default=False)
    project_details_created_by = models.CharField(db_column='PROJECT_DETAILS_CREATED_BY', max_length=30,
                                                  null=True)
    project_details_created_at = models.DateTimeField(db_column='PROJECT_DETAILS_CREATED_AT', max_length=50,
                                                      null=True)
    project_details_changed_by = models.CharField(db_column='PROJECT_DETAILS_CHANGED_BY', max_length=30,
                                                  null=True)
    project_details_changed_at = models.DateTimeField(db_column='PROJECT_DETAILS_CHANGED_AT', max_length=50,
                                                      null=True)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        managed = True
        db_table = 'MAD_PROJECT_DETAILS'
        unique_together = ('client', 'project_id')

    def get_project_fields(self, client, project_id_query, project_desc_query, project_name_query, search_count):
        return list(
            ProjectDetails.objects.filter(project_id_query, project_desc_query, project_name_query,
                                          client=client,
                                          del_ind=False).values().order_by('project_id')[:int(search_count)])


class ProjectsCategories(models.Model):
    project_categories_guid = models.CharField(db_column='PROJECT_CATEGORIES_GUID', primary_key=True, max_length=32)
    project_category_id = models.CharField(db_column='PROJECT_CATEGORY_ID', max_length=255, null=False)
    project_category_description = models.CharField(db_column='PROJECT_CATEGORY_DESCRIPTION', max_length=255,
                                                    null=False)
    projects_categories_created_by = models.CharField(db_column='PROJECTS_CATEGORIES_CREATED_BY', max_length=30,
                                                      null=True)
    projects_categories_created_at = models.DateTimeField(db_column='PROJECTS_CATEGORIES_CREATED_AT', max_length=50,
                                                          null=True)
    projects_categories_changed_by = models.CharField(db_column='PROJECTS_CATEGORIES_CHANGED_BY', max_length=30,
                                                      null=True)
    projects_categories_changed_at = models.DateTimeField(db_column='PROJECTS_CATEGORIES_CHANGED_AT', max_length=50,
                                                          null=True)
    del_ind = models.BooleanField(db_column='DEL_IND', default=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False,
                               db_column='CLIENT')

    class Meta:
        managed = True
        db_table = 'MAD_PROJECTS_CATEGORIES'
        unique_together = ('client', 'project_category_id')


class ProjectCategoriesMapping(models.Model):
    project_categories_mapping_guid = models.CharField(db_column='PROJECT_CATEGORIES_MAPPING_GUID', primary_key=True,
                                                       max_length=32)
    project_id = models.CharField(db_column='PROJECT_ID', max_length=20)
    project_category_id = models.CharField(db_column='PROJECT_CATEGORY_ID', max_length=255, null=False)
    project_categories_mapping_created_by = models.CharField(db_column='PROJECT_CATEGORIES_MAPPING_CREATED_BY',
                                                             max_length=30,
                                                             null=True)
    project_categories_mapping_created_at = models.DateTimeField(db_column='PROJECT_CATEGORIES_MAPPING_CREATED_AT',
                                                                 max_length=50,
                                                                 null=True)
    project_categories_mapping_changed_by = models.CharField(db_column='PROJECT_CATEGORIES_MAPPING_CHANGED_BY',
                                                             max_length=30,
                                                             null=True)
    project_categories_mapping_changed_at = models.DateTimeField(db_column='PROJECT_CATEGORIES_MAPPING_CHANGED_AT',
                                                                 max_length=50,
                                                                 null=True)
    del_ind = models.BooleanField(db_column='DEL_IND', default=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False,
                               db_column='CLIENT')

    class Meta:
        db_table = 'MAD_PROJECT_CATEGORIES_MAPPING'
        unique_together = ('client', 'project_category_id', 'project_id')
        managed = True


class FreeTextDetails(models.Model):
    freetext_details_guid = models.CharField(db_column='FREETEXT_DETAILS_GUID', primary_key=True, max_length=40,
                                             blank=False,
                                             null=False)
    freetext_id = models.CharField(db_column='FREETEXT_ID', max_length=40, blank=False, null=False)
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=10, verbose_name='Vendor Id', null=True)
    prod_cat_id = models.CharField(db_column='PROD_CAT_ID', max_length=50, null=True, default=None)
    supp_product_id = models.CharField(db_column='SUPP_PRODUCT_ID', max_length=40, blank=False,
                                       null=True)  # supplier gives article no
    lead_time = models.CharField(db_column='LEAD_TIME', null=True, max_length=20)
    description = models.CharField(db_column='DESCRIPTION', max_length=255, null=True, default=None)
    eform_id = models.CharField(db_column='EFORM_ID', max_length=40, blank=False, null=True)
    freetext_details_created_at = models.DateTimeField(db_column='FREETEXT_DETAILS_CREATED_AT', blank=False, null=True)
    freetext_details_created_by = models.CharField(db_column='FREETEXT_DETAILS_CREATED_BY', max_length=12, blank=False,
                                                   null=True)
    freetext_details_changed_at = models.DateTimeField(db_column='FREETEXT_DETAILS_CHANGED_AT', blank=True, null=True)
    freetext_details_changed_by = models.CharField(db_column='FREETEXT_DETAILS_CHANGED_BY', max_length=12, blank=False,
                                                   null=True)
    freetext_details_source_system = models.CharField(db_column='FREETEXT_DETAILS_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    currency_id = models.ForeignKey('eProc_Configuration.Currency', models.DO_NOTHING, db_column='CURRENCY_ID',
                                    null=True)

    class Meta:
        managed = True
        unique_together = ('client', 'freetext_id', 'supplier_id', 'prod_cat_id')
        db_table = "MAD_FREETEXT_DETAILS"


class FreeTextForm(models.Model):
    form_id = models.CharField(db_column='FORM_ID', primary_key=True, max_length=40, blank=False, null=False)
    supp_id = models.CharField(db_column='SUPP_ID', max_length=10, verbose_name='Vendor Id')
    prod_cat_id = models.CharField(db_column='PROD_CAT_ID', max_length=50, null=False, default=None)
    supp_art_no = models.CharField(db_column='SUPP_ART_NO', max_length=40, blank=False, null=False)
    lead_time = models.CharField(db_column='LEAD_TIME', null=False, max_length=20)
    form_field1 = models.CharField(db_column='FORM_FIELD1', null=True, max_length=20)
    form_field2 = models.CharField(db_column='FORM_FIELD2', null=True, max_length=20)
    form_field3 = models.CharField(db_column='FORM_FIELD3', null=True, max_length=20)
    form_field4 = models.CharField(db_column='FORM_FIELD4', null=True, max_length=20)
    form_field5 = models.CharField(db_column='FORM_FIELD5', null=True, max_length=20)
    form_field6 = models.CharField(db_column='FORM_FIELD6', null=True, max_length=20)
    form_field7 = models.CharField(db_column='FORM_FIELD7', null=True, max_length=20)
    form_field8 = models.CharField(db_column='FORM_FIELD8', null=True, max_length=20)
    form_field9 = models.CharField(db_column='FORM_FIELD9', null=True, max_length=20)
    form_field10 = models.CharField(db_column='FORM_FIELD10', null=True, max_length=20)
    description = models.CharField(db_column='DESCRIPTION', max_length=255, null=False, default=None)
    catalog_id = models.CharField(db_column='CATALOG_ID', max_length=40, blank=False, null=True)
    check_box1 = models.BooleanField(db_column='CHECK_BOX1', null=True)
    check_box2 = models.BooleanField(db_column='CHECK_BOX2', null=True)
    check_box3 = models.BooleanField(db_column='CHECK_BOX3', null=True)
    check_box4 = models.BooleanField(db_column='CHECK_BOX4', null=True)
    check_box5 = models.BooleanField(db_column='CHECK_BOX5', null=True)
    check_box6 = models.BooleanField(db_column='CHECK_BOX6', null=True)
    check_box7 = models.BooleanField(db_column='CHECK_BOX7', null=True)
    check_box8 = models.BooleanField(db_column='CHECK_BOX8', null=True)
    check_box9 = models.BooleanField(db_column='CHECK_BOX9', null=True)
    check_box10 = models.BooleanField(db_column='CHECK_BOX10', null=True)
    input_type1 = models.CharField(db_column='INPUT_TYPE1', null=True, max_length=1000)
    input_type2 = models.CharField(db_column='INPUT_TYPE2', null=True, max_length=1000)
    input_type3 = models.CharField(db_column='INPUT_TYPE3', null=True, max_length=1000)
    input_type4 = models.CharField(db_column='INPUT_TYPE4', null=True, max_length=1000)
    input_type5 = models.CharField(db_column='INPUT_TYPE5', null=True, max_length=1000)
    input_type6 = models.CharField(db_column='INPUT_TYPE6', null=True, max_length=1000)
    input_type7 = models.CharField(db_column='INPUT_TYPE7', null=True, max_length=1000)
    input_type8 = models.CharField(db_column='INPUT_TYPE8', null=True, max_length=1000)
    input_type9 = models.CharField(db_column='INPUT_TYPE9', null=True, max_length=1000)
    input_type10 = models.CharField(db_column='INPUT_TYPE10', null=True, max_length=1000)
    is_special_char1 = models.BooleanField(db_column='IS_SPECIAL_CHAR1', null=True)
    is_special_char2 = models.BooleanField(db_column='IS_SPECIAL_CHAR2', null=True)
    is_special_char3 = models.BooleanField(db_column='IS_SPECIAL_CHAR3', null=True)
    is_special_char4 = models.BooleanField(db_column='IS_SPECIAL_CHAR4', null=True)
    is_special_char5 = models.BooleanField(db_column='IS_SPECIAL_CHAR5', null=True)
    is_special_char6 = models.BooleanField(db_column='IS_SPECIAL_CHAR6', null=True)
    is_special_char7 = models.BooleanField(db_column='IS_SPECIAL_CHAR7', null=True)
    is_special_char8 = models.BooleanField(db_column='IS_SPECIAL_CHAR8', null=True)
    is_special_char9 = models.BooleanField(db_column='IS_SPECIAL_CHAR9', null=True)
    is_special_char10 = models.BooleanField(db_column='IS_SPECIAL_CHAR10', null=True)
    free_text_form_created_at = models.DateTimeField(db_column='FREE_TEXT_FORM_CREATED_AT', blank=False, null=True)
    free_text_form_created_by = models.CharField(db_column='FREE_TEXT_FORM_CREATED_BY', max_length=12, blank=False,
                                                 null=True)
    free_text_form_changed_at = models.DateTimeField(db_column='FREE_TEXT_FORM_CHANGED_AT', blank=True, null=True)
    free_text_form_changed_by = models.CharField(db_column='FREE_TEXT_FORM_CHANGED_BY', max_length=12, blank=False,
                                                 null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    def __str__(self):
        return self.form_id

    class Meta:
        unique_together = ('client', 'supp_id', 'prod_cat_id', 'catalog_id')
        db_table = "MAD_FREE_TEXT_FORM"


class ImagesUpload(models.Model):
    def get_images_path(self, filename):
        return os.path.join(str(self.image_type), (OrgClients.objects.get(client=self.client)).__str__(),
                            str(self.image_id),
                            str(self.image_name))

    images_upload_guid = models.CharField(db_column='IMAGES_UPLOAD_GUID', primary_key=True, max_length=32, null=False,
                                          default=None)
    image_id = models.CharField(db_column="IMAGE_ID", max_length=40, null=True)
    image_number = models.PositiveIntegerField(db_column='IMAGE_NUMBER', null=True)
    image_url = models.FileField(db_column='IMAGE_URL', upload_to=get_images_path, null=True)
    image_name = models.CharField(db_column="IMAGE_NAME", max_length=20, null=True)
    image_default = models.BooleanField(db_column='IMAGE_DEFAULT', null=True, default=False, verbose_name='Default '
                                                                                                          'image '
                                                                                                          'flag')

    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    image_type = models.CharField(db_column="IMAGE_TYPE", max_length=40, null=True)
    created_at = models.DateTimeField(db_column='CREATED_AT', blank=False, null=False, verbose_name='Created At')
    created_by = models.CharField(db_column='CREATED_BY', max_length=12, blank=False, null=False,
                                  verbose_name='Creator')
    changed_at = models.DateTimeField(db_column='CHANGED_AT', blank=True, null=True, verbose_name='Changed At')
    changed_by = models.CharField(db_column='CHANGED_BY', max_length=12, blank=False, null=True,
                                  verbose_name='Changed By')
    images_upload_source_system = models.CharField(db_column='IMAGES_UPLOAD_SOURCE_SYSTEM', max_length=20)
    images_upload_destination_system = models.CharField(db_column='IMAGES_UPLOAD_DESTINATION_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        managed = True
        db_table = 'MAD_IMAGES_UPLOAD'


class NumberRanges(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    sequence = models.CharField(db_column='SEQUENCE', null=False, max_length=5)
    starting = models.CharField(db_column='STARTING', max_length=10, null=False)
    ending = models.CharField(db_column='ENDING', max_length=10, null=False)
    current = models.CharField(db_column='CURRENT', max_length=10, null=True)
    number_ranges_created_by = models.CharField(db_column='NUMBER_RANGES_CREATED_BY', max_length=30, null=True)
    number_ranges_created_at = models.DateTimeField(db_column='NUMBER_RANGES_CREATED_AT', max_length=50, null=True)
    number_ranges_changed_by = models.CharField(db_column='NUMBER_RANGES_CHANGED_BY', max_length=30, null=True)
    number_ranges_changed_at = models.DateTimeField(db_column='NUMBER_RANGES_CHANGED_AT', max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    document_type = models.ForeignKey('eProc_Configuration.DocumentType', on_delete=models.DO_NOTHING,
                                      db_column='DOCUMENT_TYPE', null=False)

    class Meta:
        db_table = 'MAD_NUMBER_RANGES'
        managed = True
        unique_together = ('client', 'document_type', 'sequence')


class ProductPricing:
    product_pricing_guid = models.CharField(db_column='PRODUCT_PRICING_GUID', primary_key=True, max_length=40,
                                            blank=False, null=False)
    pricing_product_id = models.CharField(db_column="PRICING_PRODUCT_ID", max_length=16, null=True)
    price_type = models.CharField(db_column="PRICE_TYPE", max_length=16, null=True)  # DIRECT,DIFFERENTIAL,QUANTITY
    price_data = models.CharField(db_column="PRICE_DATA", max_length=16, null=True)
    price = models.DecimalField(db_column='PRICE', max_digits=15, decimal_places=2, null=True)
    price_unit = models.CharField(db_column='PRICE_UNIT', max_length=5, null=True)
    differencial_pricing_flag = models.BooleanField(db_column='DIFFERENCIAL_PRICING_FLAG', default=False,
                                                    null=False)  # fALSE non deffrential true differe
    operator = models.CharField(db_column="OPERATOR", max_length=16, null=True)  # plus,minus, percentage
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    unit = models.ForeignKey('eProc_Configuration.UnitOfMeasures', db_column='UNIT_OF_MEASURE', null=True,
                             on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = "MAD_PRODUCT_PRICING"


class SapConnector(models.Model):
    sys_name = models.CharField(db_column='sys_name', null=False, max_length=20)
    sys_id = models.PositiveIntegerField(db_column='sys_id', null=False, primary_key=True)
    ashost = models.GenericIPAddressField(db_column='ashost', null=False)
    sysnr = models.PositiveIntegerField(db_column='sysnr', null=False)
    user = models.CharField(db_column='user', max_length=8, null=False)
    passwd = models.CharField(db_column='passwd', null=False, max_length=10)
    del_ind = models.BooleanField(db_column='DEL_IND', null=True)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        managed = True
        unique_together = ('ashost', 'client')
        db_table = 'MAD_SAP_CONNECTOR'


class SourcingRule(models.Model):
    sourcing_rule_guid = models.CharField(db_column='SOURCING_RULE_GUID', primary_key=True, max_length=32,
                                          null=False, default=None)
    prod_cat_id_from = models.IntegerField(db_column='PROD_CAT_ID_FROM', null=False)
    prod_cat_id_to = models.IntegerField(db_column='PROD_CAT_ID_TO', null=False)
    sourcing_flag = models.BooleanField(default=False, null=False, db_column='SOURCING_FLAG')
    call_off = models.CharField(db_column='CALL_OFF', max_length=15, null=True)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=True)
    rule_type = models.CharField(db_column='RULE_TYPE', max_length=3, null=True)
    sourcing_rule_source_system = models.CharField(db_column='SOURCING_RULE_SOURCE_SYSTEM',
                                                   max_length=20)
    sourcing_rule_created_by = models.CharField(db_column='SOURCING_RULE_CREATED_BY',
                                                max_length=30, null=True)
    sourcing_rule_created_at = models.DateTimeField(db_column='SOURCING_RULE_CREATED_AT',
                                                    max_length=50, null=True)
    sourcing_rule_changed_by = models.CharField(db_column='SOURCING_RULE_CHANGED_BY',
                                                max_length=30, null=True)
    sourcing_rule_changed_at = models.DateTimeField(db_column='SOURCING_RULE_CHANGED_AT',
                                                    max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        managed = True
        db_table = 'MAD_SOURCING_RULE'


class SourcingMapping(models.Model):
    sourcing_mapping_guid = models.CharField(db_column='SOURCING_MAPPING_GUID', primary_key=True, max_length=32,
                                             null=False, default=None)
    prod_cat_id = models.CharField(db_column='PROD_CAT_ID', max_length=20, null=False)
    product_id = models.CharField(db_column="PRODUCT_ID", max_length=16, null=True)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    rule_type = models.CharField(db_column='RULE_TYPE', max_length=3, null=True)
    sourcing_mapping_source_system = models.CharField(db_column='SOURCING_MAPPING_SOURCE_SYSTEM',
                                                      max_length=20)
    sourcing_mapping_created_by = models.CharField(db_column='SOURCING_MAPPING_CREATED_BY',
                                                   max_length=30, null=True)
    sourcing_mapping_created_at = models.DateTimeField(db_column='SOURCING_MAPPING_CREATED_AT',
                                                       max_length=50, null=True)
    sourcing_mapping_changed_by = models.CharField(db_column='SOURCING_MAPPING_CHANGED_BY',
                                                   max_length=30, null=True)
    sourcing_mapping_changed_at = models.DateTimeField(db_column='SOURCING_MAPPING_CHANGED_AT',
                                                       max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        managed = True
        db_table = 'MAD_SOURCING_MAPPING'


# Model for system settings new table
class SystemSettingsConfig(models.Model):
    system_settings_config_guid = models.CharField(primary_key=True, db_column='SYSTEM_SETTINGS_CONFIG_GUID',
                                                   max_length=32)
    sys_attr_type = models.CharField(db_column='SYS_ATTR_TYPE', max_length=60)
    sys_attr_value = models.CharField(db_column='SYS_ATTR_VALUE', null=False, max_length=600)
    sys_settings_default_flag = models.BooleanField(db_column='SYS_SETTINGS_DEFAULT_FLAG', null=False)
    system_settings_config_created_by = models.CharField(db_column='SYSTEM_SETTINGS_CONFIG_CREATED_BY', max_length=30,
                                                         null=True)
    system_settings_config_created_at = models.DateTimeField(db_column='SYSTEM_SETTINGS_CONFIG_CREATED_AT',
                                                             max_length=50, null=True)
    system_settings_config_changed_by = models.CharField(db_column='SYSTEM_SETTINGS_CONFIG_CHANGED_BY', max_length=30,
                                                         null=True)
    system_settings_config_changed_at = models.DateTimeField(db_column='SYSTEM_SETTINGS_CONFIG_CHANGED_AT',
                                                             max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False, db_column='DEL_IND')
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = 'MAD_SYSTEM_SETTINGS_CONFIG'
        unique_together = ('sys_attr_type', 'sys_attr_value', 'client')
        managed = True


class UserRolesCust(models.Model):
    user_cust_role_guid = models.CharField(db_column='USER_CUST_ROLE_GUID', primary_key=True, max_length=32)
    user_cust_role_desc = models.CharField(db_column='USER_CUST_ROLE_DESC', max_length=60, null=False)
    user_roles_cust_created_by = models.CharField(db_column='user_roles_cust_created_by', max_length=30, null=True)
    user_roles_cust_created_at = models.DateTimeField(db_column='user_roles_cust_created_at', max_length=50, null=True)
    user_roles_cust_changed_by = models.CharField(db_column='user_roles_cust_changed_by', max_length=30, null=True)
    user_roles_cust_changed_at = models.DateTimeField(db_column='user_roles_cust_changed_at', max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    role = models.ForeignKey('eProc_Configuration.UserRoles', on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = 'MAD_ROLES_CUST'
        unique_together = ('client', 'role')
        managed = True


class VariantConfig(models.Model):
    variant_config_guid = models.CharField(db_column='VARIANT_CONFIG_GUID', primary_key=True, max_length=40,
                                           blank=False,
                                           null=False)
    variant_id = models.CharField(db_column='VARIANT_ID', max_length=40, blank=False, null=True)
    product_id = models.CharField(db_column="PRODUCT_ID", max_length=16, null=True)
    variant_count = models.PositiveIntegerField(db_column='VARIANT_COUNT', blank=False, null=False,
                                                verbose_name='field count', default=0)
    variant_name = models.CharField(db_column='VARIANT_NAME', null=True, max_length=200)
    variant_datatype = models.CharField(db_column='VARIANT_DATATYPE', null=True,
                                        max_length=50)  # input field datatype ex.. dropdown checkbox text,num
    variant_data = models.CharField(db_column='VARIANT_DATA', null=True, max_length=1000)
    default_variant_data = models.CharField(db_column='DEFAULT_VARIANT_DATA', null=True, max_length=100)
    required_flag = models.BooleanField(db_column='REQUIRED_FLAG', null=True)
    specialchar_flag = models.BooleanField(db_column='SPECIALCHAR_FLAG', null=True)
    # display_flag 0- nothing,1- only display the detail (non editable)
    display_flag = models.BooleanField(db_column='DISPLAY_FLAG', null=True, default=False)
    dropdown_pricetype = models.CharField(db_column='DROPDOWN_PRICETYPE', null=True,
                                          max_length=50)  # with price without price quantity
    # variant_flag 0 - get price from product details, 1 - get price from ProductPricing
    variant_flag = models.BooleanField(db_column='VARIANT_FLAG', null=True, default=False)
    variant_config_created_at = models.DateTimeField(db_column='VARIANT_CONFIG_CREATED_AT', blank=False,
                                                     null=True)
    variant_config_created_by = models.CharField(db_column='VARIANT_CONFIG_CREATED_BY', max_length=12,
                                                 blank=False, null=True)
    variant_config_changed_at = models.DateTimeField(db_column='VARIANT_CONFIG_CHANGED_AT', blank=True,
                                                     null=True)
    variant_config_changed_by = models.CharField(db_column='VARIANT_CONFIG_CHANGED_BY', max_length=12,
                                                 blank=False, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        unique_together = ('client', 'variant_id', 'variant_count')
        db_table = "MAD_VARIANT_CONFIG"


class WorkflowSchema(models.Model):
    workflow_schema_guid = models.CharField(primary_key=True, db_column='WORKFLOW_SCHEMA_GUID', max_length=32)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=8, null=False)
    workflow_schema = models.CharField(db_column='WORKFLOW_SCHEMA', max_length=40, null=False)
    workflow_schema_created_by = models.CharField(db_column='WORKFLOW_SCHEMA_CREATED_BY', max_length=30, null=True)
    workflow_schema_created_at = models.DateTimeField(db_column='WORKFLOW_SCHEMA_CREATED_AT', max_length=50, null=True)
    workflow_schema_changed_by = models.CharField(db_column='WORKFLOW_SCHEMA_CHANGED_BY', max_length=30, null=True)
    workflow_schema_changed_at = models.DateTimeField(db_column='WORKFLOW_SCHEMA_CHANGED_AT', max_length=50, null=True)
    workflow_schema_source_system = models.CharField(db_column='WORKFLOW_SCHEMA_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    app_types = models.ForeignKey('eProc_Configuration.ApproverType', models.DO_NOTHING, db_column='APP_TYPES',
                                  null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        managed = True
        db_table = 'MAD_WF_SCHEMA'
