from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import re

# Definition of SC Header table structure
from eProc_Basic.Utilities.global_defination import global_variables


class RfqHeader(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    doc_number = models.CharField(db_column='DOC_NUMBER', max_length=10, blank=False, null=False,
                                  verbose_name='SC Number')
    ref_doc_no = models.CharField(db_column='REF_DOC_NO', max_length=16, blank=True, null=True,
                                  verbose_name='Ref Doc Number')
    co_code = models.CharField(db_column='CO_CODE', max_length=8, blank=True, null=True, verbose_name='Company Code')
    gross_amount = models.CharField(db_column='GROSS_AMOUNT', max_length=15, blank=True, null=True,
                                    verbose_name='Gross Amount')  # sum(gross price in item*quantity for all the items)
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True,
                                   verbose_name='SC Name')
    # total_value = sum(currency converted item value)
    total_value = models.CharField(db_column='TOTAL_VALUE', max_length=15, blank=False, null=False,
                                   verbose_name='Total Value')  # sum(value in item)
    currency = models.CharField(db_column='CURRENCY', max_length=3, blank=False, null=False, verbose_name='Currency')
    # total_tax = sum of (tax value in scitem)
    total_tax = models.CharField(db_column='TOTAL_TAX', max_length=15, blank=True, null=True, verbose_name='Total Tax')
    total_value_appr = models.CharField(db_column='TOTAL_VALUE_APPR', max_length=15, blank=True, null=True,
                                        verbose_name='Total Value Appr')
    usr_budget_value = models.CharField(db_column='USR_BUDGET_VALUE', max_length=15, blank=True, null=True,
                                        verbose_name='User Budget Value')
    subtype = models.CharField(db_column='SUBTYPE', max_length=10, blank=True, null=True,
                               verbose_name='Specification of a Purchasing Doc.e.g. Credit Memo/Invoice')
    transaction_type = models.CharField(db_column='TRANSACTION_TYPE', null=False,
                                        max_length=10)  # Transaction number of sc eg SHC1,SHC2
    ref_object_id = models.CharField(db_column='REF_OBJECT_ID', max_length=10, blank=True, null=True,
                                     verbose_name='Reference Object Id')
    requester = models.CharField(db_column='REQUESTER', max_length=40, blank=False, null=False,
                                 verbose_name='Requester')
    approval_step = models.CharField(db_column='APPROVAL_STEP', max_length=2, blank=True, null=True,
                                     verbose_name='Approval Ind')
    transmission_error = models.BooleanField(db_column='TRANSMISSION_ERROR', default=False, null=True,
                                             verbose_name='RFQ creation error flag')
    transmission_error_type = models.CharField(db_column='TRANSMISSION_ERROR_TYPE', max_length=30, blank=True,
                                               null=True,
                                               verbose_name='RFQ creation error type eg:PO_GROUP,TRANSACTION_TYPE ')
    status = models.CharField(db_column='STATUS', max_length=20, blank=False, null=False, verbose_name='Status')
    follow_on_doc_type = models.CharField(db_column='FOLLOW_ON_DOC_TYPE', max_length=5, null=True)
    created_at = models.DateTimeField(db_column='CREATED_AT', blank=False, null=False, verbose_name='Created At')
    created_by = models.CharField(db_column='CREATED_BY', max_length=12, blank=False, null=False,
                                  verbose_name='Creator')
    changed_at = models.DateTimeField(db_column='CHANGED_AT', blank=True, null=True, verbose_name='Changed At')
    changed_by = models.CharField(db_column='CHANGED_BY', max_length=12, blank=False, null=False,
                                  verbose_name='Changed By')
    ordered_at = models.DateTimeField(db_column='ORDERED_AT', blank=True, null=True, verbose_name='Ordered At')
    time_zone_difference = models.CharField(db_column='TIME_ZONE_DIFFERENCE', max_length=6, blank=True, null=True,
                                            verbose_name='Time Zone Difference')
    inv_addr_num = models.PositiveIntegerField(db_column='INV_ADDR_NUM', blank=True, null=True,
                                               verbose_name='Invoice address number')
    ship_addr_num = models.PositiveIntegerField(db_column='SHIP_ADDR_NUM', blank=True, null=True,
                                                verbose_name='Ship to Address Number')
    version_type = models.CharField(db_column='VERSION_TYPE', max_length=1, blank=True, null=True,
                                    verbose_name='Version Type')
    time_zone = models.CharField(db_column='TIME_ZONE', max_length=6, blank=True, null=True, verbose_name='Time Zone')
    posting_date = models.DateTimeField(db_column='POSTING_DATE', blank=True, null=True)
    language_id = models.CharField(db_column='LANGUAGE_ID', blank=True, null=True, max_length=2)

    document_type = models.CharField(db_column='DOCUMENT_TYPE', max_length=5, null=True)

    archivable_flag = models.BooleanField(db_column='ARCHIVABLE_FLAG', default=False, null=True,
                                          verbose_name='Achievable Flag')
    rfq_header_source_system = models.CharField(db_column='RFQ_HEADER_SOURCE_SYSTEM', max_length=20)
    rfq_header_destination_system = models.CharField(db_column='RFQ_HEADER_DESTINATION_SYSTEM', max_length=20)
    response_date = models.DateTimeField(db_column='RESPONSE_DATE', blank=False, null=True,
                                         verbose_name='Response Date')
    delivery_date = models.DateTimeField(db_column='DELIVERY_DATE', blank=False, null=True,
                                         verbose_name='Delivery Date')
    rfq_name = models.CharField(db_column='RFQ_NAME', max_length=1000, blank=False, null=False)
    org_address_num = models.CharField(db_column='ORG_ADDRESS_NUM', max_length=10, blank=False, null=False,
                                       verbose_name='Org addr num')
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        managed = True
        unique_together = ('client', 'doc_number', 'rfq_header_source_system'), \
                          ('client', 'doc_number', 'rfq_header_destination_system')
        db_table = 'MTD_RFQ_HEADER'


# Definition of RFQ Item table structure
class RfqItem(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    item_num = models.PositiveIntegerField(db_column='ITEM_NUM', blank=False, null=False, verbose_name='Line Number')
    po_doc_num = models.CharField(db_column='po_doc_num', max_length=10, blank=True, null=True,
                                  verbose_name='PO Doc Number')
    po_header_guid = models.CharField(db_column='PO_HEADER_GUID', max_length=32, blank=True, null=True)
    po_item_num = models.CharField(db_column='PO_ITEM_NUM', max_length=10, blank=True, null=True,
                                   verbose_name='Item Number')
    prod_cat_desc = models.CharField(db_column='PROD_CAT_DESC', max_length=255, blank=False, null=False,
                                     verbose_name='Description')
    item_guid = models.CharField(db_column='ITEM_GUID', max_length=32)
    header_guid = models.CharField(db_column='HEADER_GUID', max_length=32)
    product_info_id = models.CharField(db_column='PRODUCT_INFO_ID', max_length=40, blank=True, null=True)
    comp_code = models.CharField(db_column='COMP_CODE', max_length=10, blank=False, null=False,
                                 verbose_name='Company Code')
    purch_grp = models.CharField(db_column='PURCH_GRP', max_length=20, blank=True, null=True,
                                 verbose_name='Purchasing Group')
    purch_org = models.CharField(db_column='PURCH_ORG', max_length=20, blank=True, null=True,
                                 verbose_name='Purchasing Organization')
    process_flow = models.CharField(db_column='PROCESS_FLOW', max_length=20, blank=True, null=True,
                                    verbose_name='Item Category')
    prod_cat_id = models.CharField(db_column='PROD_CAT_ID', max_length=20, blank=False, null=False, default=None,
                                   verbose_name='Product Category')
    prod_type = models.CharField(db_column='PROD_TYPE', max_length=2, blank=False, null=True,
                                 verbose_name='Product Type')
    cust_prod_cat_id = models.CharField(db_column='CUST_PROD_CAT_ID', max_length=20, blank=True, null=True,
                                        verbose_name='UNSPSC')
    fin_entry_ind = models.BooleanField(db_column='FIN_ENTRY_IND', blank=True, default=False, null=True,
                                        verbose_name='Fin entry ind')
    item_del_date = models.DateTimeField(db_column='ITEM_DEL_DATE', blank=False, null=True,
                                         verbose_name='Delivery Date')
    start_date = models.DateTimeField(db_column='START_DATE', null=True, verbose_name='Start Date')
    end_date = models.DateTimeField(db_column='END_DATE', null=True, verbose_name='End date')
    quantity = models.PositiveIntegerField(db_column='QUANTITY', null=True, verbose_name='Quantity')
    int_product_id = models.CharField(db_column='INT_PRODUCT_ID', max_length=20, null=True)
    tax_code = models.CharField(db_column='TAX_CODE', max_length=5, null=True, verbose_name='Tax Code')
    price = models.DecimalField(db_column='PRICE', max_digits=15, decimal_places=2, blank=True, null=True,
                                verbose_name='Price')
    gross_price = models.DecimalField(db_column='GROSS_PRICE', max_digits=15, decimal_places=2, blank=False, null=True,
                                      verbose_name='Gross Price')  # price + sales tax
    value = models.DecimalField(db_column='VALUE', max_digits=15, decimal_places=2, blank=True, null=True,
                                verbose_name='Value')  # (float(quantity) * float(price)) / int(price_unit)
    tax_value = models.DecimalField(db_column='TAX_VALUE', max_digits=15, decimal_places=2, blank=True, null=True,
                                    verbose_name='tax Value')  # (SGST *quantity)+(CGST *quantity)
    currency = models.CharField(db_column='CURRENCY', null=True, max_length=3, verbose_name='Currency')
    price_unit = models.CharField(db_column='PRICE_UNIT', max_length=5, blank=True, null=True,
                                  verbose_name='Price Unit')
    unit = models.CharField(db_column='UNIT', max_length=3, blank=False, null=False, verbose_name='Unit')
    call_off = models.CharField(db_column='CALL_OFF', null=True, max_length=20)
    status = models.CharField(db_column='STATUS', max_length=20, blank=True, null=True, verbose_name='Status')
    goods_recep = models.CharField(db_column='GOODS_RECEP', max_length=12, blank=False, null=False,
                                   verbose_name='Goods Recipient')
    bill_to_addr_num = models.CharField(db_column='BILL_TO_ADDR_NUM', max_length=10, blank=False, null=False,
                                        verbose_name='bill to addr num')
    ship_to_addr_num = models.CharField(db_column='SHIP_TO_ADDR_NUM', max_length=10, blank=False, null=False,
                                        verbose_name='ship to addr num')
    manufacturer = models.CharField(db_column='MANUFACTURER', max_length=15, null=True)
    created_at = models.DateTimeField(null=True, db_column='CREATED_AT', blank=True)
    created_by = models.CharField(max_length=10, db_column='CREATED_BY', null=True, blank=True)
    changed_at = models.DateTimeField(null=True, db_column='CHANGED_AT', blank=True)
    changed_by = models.CharField(max_length=10, db_column='CHANGED_BY', null=True, blank=True)
    document_type = models.CharField(max_length=10, db_column='DOCUMENT_TYPE', null=True, blank=True)
    order_date = models.DateTimeField(db_column='ORDER_DATE', null=True, blank=True)
    material_no = models.CharField(max_length=18, db_column='MATERIAL_NO', blank=True, null=True)
    be_obj_item = models.CharField(max_length=10, db_column='BE_OBJ_ITEM', blank=True, null=True)
    be_object_id = models.CharField(max_length=20, db_column='BE_OBJECT_ID', blank=True, null=True)
    be_stge_loc = models.CharField(max_length=4, db_column='BE_STGE_LOC', blank=True, null=True)
    be_plant = models.CharField(max_length=4, db_column='BE_PLANT', blank=True, null=True)
    be_doc_type = models.CharField(max_length=4, db_column='BE_doc_type', blank=True, null=True)
    goods_marking = models.CharField(max_length=60, db_column='GOODS_MARKING', blank=True, null=True)
    approved_by = models.CharField(max_length=16, db_column='APPROVED_BY', blank=True, null=True)
    po_transaction_type = models.CharField(db_column='PO_TRANSACTION_TYPE', null=True, blank=True,
                                           max_length=10)  # Transaction number of PO eg SHC1,SHC2
    required_on = models.DateField(null=True, blank=True, db_column='REQUIRED_ON')
    description = models.CharField(db_column='DESCRIPTION', max_length=1000, blank=False, null=False)
    long_desc = models.CharField(db_column='LONG_DESC', max_length=3000, blank=True, null=True,
                                 verbose_name='Product Long desc')
    itm_language_id = models.CharField(db_column='ITM_LANGUAGE_ID', blank=True, null=True, max_length=2,
                                       verbose_name=' Short Text Language for an Item ')
    be_po_trans_type = models.CharField(db_column='BE_PO_TRANS_TYPE', blank=True, null=True, max_length=10,
                                        verbose_name='PO transaction type in ERP system (ECPO)')
    sgst = models.DecimalField(db_column='SGST', max_digits=15, decimal_places=2, blank=True, null=True,
                               verbose_name='State GST')
    cgst = models.DecimalField(db_column='CGST', max_digits=15, decimal_places=2, blank=True, null=True,
                               verbose_name='Central GST')
    vat = models.DecimalField(db_column='VAT', max_digits=15, decimal_places=2, blank=True, null=True,
                              verbose_name='Value Added Tax - VAT code (%age as decimal) returned from catalogue ')

    supplier_note_existence_flag = models.BooleanField(db_column='SUPPLIER_NOTE_EXISTENCE_FLAG', default=False,
                                                       blank=True, null=True,
                                                       verbose_name='Supplier note existence flag')
    internal_note_existence_flag = models.BooleanField(db_column='INTERNAL_NOTE_EXISTENCE_FLAG', default=False,
                                                       blank=True, null=True,
                                                       verbose_name='Internal note existence flag')
    attachment_existence_flag = models.BooleanField(db_column='ATTACHMENT_EXISTENCE_FLAG', default=False, blank=True,
                                                    null=True,
                                                    verbose_name='Attachment existence flag')
    accounting_change_flag = models.BooleanField(db_column='ACCOUNTING_CHANGE_FLAG', default=False, blank=True,
                                                 null=True,
                                                 verbose_name='Accounting change flag')
    address_change_flag = models.BooleanField(db_column='ADDRESS_CHANGE_FLAG', default=False, blank=True, null=True,
                                              verbose_name='Address change flag')
    rfq_item_source_system = models.CharField(db_column='RFQ_ITEM_SOURCE_SYSTEM', max_length=20)
    rfq_item_destination_system = models.CharField(db_column='RFQ_ITEM_DESTINATION_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    sc_doc_num = models.CharField(db_column='sc_doc_num', max_length=10, blank=True, null=True,
                                  verbose_name='SC Doc Number')
    sc_header_guid = models.ForeignKey('eProc_Shopping_Cart.ScHeader', models.DO_NOTHING, db_column='SC_HEADER_GUID',
                                       blank=True, null=True)
    sc_item_guid = models.ForeignKey('eProc_Shopping_Cart.ScItem', models.DO_NOTHING, db_column='SC_ITEM_GUID',
                                     blank=True, null=True)
    sc_item_num = models.PositiveIntegerField(db_column='SC_ITEM_NUM', blank=False, null=False,
                                              verbose_name='Line Number')

    class Meta:
        managed = True
        db_table = 'MTD_RFQ_ITEM'


# Definition of RFQ Accounting table structure
class RfqAccounting(models.Model):
    rfq_accounting_guid = models.CharField(db_column='RFQ_ACCOUNTING_GUID', primary_key=True, max_length=32)
    acc_item_num = models.DecimalField(db_column='ACC_ITEM_NUM', max_digits=4, decimal_places=0, blank=False,
                                       null=False, verbose_name='Number')
    acc_cat = models.CharField(db_column='ACC_CAT', max_length=5, blank=False, null=False,
                               verbose_name='Account Assignment Category')
    dist_perc = models.CharField(db_column='DIST_PERC', max_length=5, blank=True, null=True,
                                 verbose_name='Distribution Percentage')
    gl_acc_num = models.CharField(db_column='GL_ACC_NUM', max_length=10, blank=False, null=False,
                                  verbose_name='General Ledger Account')
    cost_center = models.CharField(db_column='COST_CENTER', max_length=10, blank=True, null=True,
                                   verbose_name='Cost Center')
    internal_order = models.CharField(db_column='INTERNAL_ORDER', max_length=12, blank=True, null=True,
                                      verbose_name='Internal Order')
    generic_acc_str = models.CharField(db_column='GENERIC_ACC_STR', max_length=64, blank=True, null=True,
                                       verbose_name='Generic Acc Ass')

    wbs_ele = models.CharField(db_column='WBS_ELE', max_length=24, blank=True, null=True,
                               verbose_name='WBS Element')
    project = models.CharField(db_column='PROJECT', max_length=24, blank=True, null=True, verbose_name='Project')
    task_id = models.CharField(db_column='TASK_ID', max_length=25, blank=True, null=True, verbose_name='Task Id')
    network = models.CharField(db_column='NETWORK', max_length=12, blank=True, null=True, verbose_name='Network')
    ref_date = models.DateField(db_column='REF_DATE', null=True, verbose_name='Ref Date')
    dist_qty = models.PositiveIntegerField(db_column='DST_QTY', null=True)
    dist_val = models.PositiveIntegerField(db_column='DST_VAL', null=True)
    dist_ind = models.BooleanField(default=False, null=False, db_column='DIST_IND')
    custom1 = models.CharField(db_column='CUSTOM1', max_length=12, null=True)
    custom2 = models.CharField(db_column='CUSTOM2', max_length=12, null=True)
    custom3 = models.CharField(db_column='CUSTOM3', max_length=12, null=True)
    custom4 = models.CharField(db_column='CUSTOM4', max_length=12, null=True)
    asset_number = models.CharField(db_column='ASSET_NUMBER', max_length=24, null=True)
    gl_acc_origin = models.CharField(db_column='GL_ACC_ORIGIN', max_length=1, blank=True, null=True,
                                     verbose_name='Original Account (determination/manual entry)')
    asset_sub_no = models.CharField(db_column='ASSET_SUB_NO', max_length=4, blank=True, null=True,
                                    verbose_name='Asset Subnumber')
    order_no = models.CharField(db_column='ORDER_NO', max_length=12, blank=True, null=True,
                                verbose_name='Controlling Area')
    prof_segm = models.CharField(db_column='PROF_SEGM', max_length=10, blank=True, null=True,
                                 verbose_name='Profit Center')
    part_acct = models.CharField(db_column='PART_ACCT', max_length=10, blank=True, null=True,
                                 verbose_name='Partner account number')
    fund = models.CharField(db_column='FUND', max_length=10, blank=True, null=True, verbose_name='Functional Area')
    budget_period = models.CharField(db_column='BUDGET_PERIOD', max_length=10, blank=True, null=True,
                                     verbose_name='Budget Period')

    rfq_accounting_created_at = models.DateTimeField(db_column='RFQ_ACCOUNTING_CREATED_AT', blank=False, null=True)
    rfq_accounting_created_by = models.CharField(db_column='RFQ_ACCOUNTING_CREATED_BY', max_length=12, blank=False,
                                                 null=True)
    rfq_accounting_changed_at = models.DateTimeField(db_column='RFQ_ACCOUNTING_CHANGED_AT', blank=True, null=True)
    rfq_accounting_changed_by = models.CharField(db_column='RFQ_ACCOUNTING_CHANGED_BY', max_length=12, blank=False,
                                                 null=True)
    rfq_accounting_source_system = models.CharField(db_column='RFQ_ACCOUNTING_SOURCE_SYSTEM', max_length=20)
    rfq_accounting_destination_system = models.CharField(db_column='RFQ_ACCOUNTING_DESTINATION_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    rfq_header_guid = models.ForeignKey('eProc_Rfq.RfqHeader', models.DO_NOTHING, db_column='RFQ_HEADER_GUID',
                                        blank=True, null=True)
    rfq_item_guid = models.ForeignKey('eProc_Rfq.RfqItem', models.DO_NOTHING, db_column='RFQ_ITEM_GUID',
                                      blank=True,
                                      null=True)

    class Meta:
        managed = True
        db_table = 'MTD_RFQ_ACCOUNTING'


# Definition of RFQ Accounting table structure
class RfqQuestionnaireType(models.Model):
    guid = models.CharField(db_column='RFQ_QUESTIONNAIRE_TYPE_GUID', primary_key=True, max_length=32)
    rfq_doc_num = models.CharField(db_column='rfq_doc_num', max_length=10, blank=True, null=True,
                                   verbose_name='RFQ Doc Number')
    question_num = models.PositiveIntegerField(db_column='QUESTION_NUM', blank=False, null=False,
                                               verbose_name='Question Number')
    yes_no_desc_type = models.BooleanField(default=False, null=False)
    question = models.CharField(db_column='QUESTION', max_length=2000)
    mandatory = models.BooleanField(default=False, null=False)
    rfq_item_num = models.PositiveIntegerField(db_column='RFQ_ITEM_NUM', blank=False, null=False)
    rfq_header_guid = models.ForeignKey('eProc_Rfq.RfqHeader', on_delete=models.PROTECT, null=False)
    rfq_item_guid = models.ForeignKey('eProc_Rfq.RfqItem', on_delete=models.PROTECT, null=False)
    rfq_questionnaire_type_created_at = models.DateTimeField(db_column='RFQ_QUESTIONNAIRE_TYPE_CREATED_AT', blank=False,
                                                             null=True)
    rfq_questionnaire_type_created_by = models.CharField(db_column='RFQ_QUESTIONNAIRE_TYPE_CREATED_BY', max_length=12,
                                                         blank=False,
                                                         null=True)
    rfq_questionnaire_type_changed_at = models.DateTimeField(db_column='RFQ_QUESTIONNAIRE_TYPE_CHANGED_AT', blank=True,
                                                             null=True)
    rfq_questionnaire_type_changed_by = models.CharField(db_column='RFQ_QUESTIONNAIRE_TYPE_CHANGED_BY', max_length=12,
                                                         blank=False,
                                                         null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        managed = True
        db_table = 'MAD_RFQ_QUESTIONNAIRE_TYPE'
        unique_together = ('question_num', 'client', 'rfq_doc_num')


class RfqAnswers(models.Model):
    guid = models.CharField(db_column='RFQ_ANSWERS_GUID', primary_key=True, max_length=32)
    rfq_header_guid = models.ForeignKey('eProc_Rfq.RfqHeader', on_delete=models.PROTECT, null=False)
    rfq_doc_num = models.CharField(db_column='RFQ_DOC_NUM', max_length=10, blank=True, null=True,
                                   verbose_name='RFQ Doc Number')
    question_num = models.PositiveIntegerField(db_column='QUESTION_NUM', blank=False, null=False)
    yes_no_desc_type = models.BooleanField(default=False, null=False)
    rfq_item_num = models.PositiveIntegerField(db_column='RFQ_ITEM_NUM', blank=False, null=False)
    rfq_item_guid = models.ForeignKey('eProc_Rfq.RfqItem', on_delete=models.PROTECT, null=False)
    rfq_answers_created_at = models.DateTimeField(db_column='RFQ_ANSWERS_CREATED_AT', blank=False,
                                                  null=True)
    rfq_answers_created_by = models.CharField(db_column='RFQ_ANSWERS_CREATED_BY', max_length=12,
                                              blank=False,
                                              null=True)
    rfq_answers_changed_at = models.DateTimeField(db_column='RFQ_ANSWERS_CHANGED_AT', blank=True,
                                                  null=True)
    rfq_answers_changed_by = models.CharField(db_column='RFQ_ANSWERS_CHANGED_BY', max_length=12,
                                              blank=False,
                                              null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        managed = True
        db_table = 'MTD_RFQ_ANSWERS'
        unique_together = ('question_num', 'client', 'rfq_doc_num')


class RfqSuppliers(models.Model):
    guid = models.CharField(db_column='RFQ_SUPPLIERS_GUID', primary_key=True, max_length=32)
    rfq_doc_num = models.CharField(db_column='RFQ_DOC_NUM', max_length=10, blank=True, null=True,
                                   verbose_name='RFQ Doc Number')
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=12, blank=True, null=True,
                                   verbose_name='Supplier ID')
    supplier_email = models.CharField(max_length=100, db_column='SUPPLIER_EMAIL', blank=True, null=True)
    rfq_header_guid = models.ForeignKey('eProc_Rfq.RfqHeader', on_delete=models.PROTECT, null=False)
    rfq_suppliers_created_at = models.DateTimeField(db_column='RFQ_SUPPLIERS_CREATED_AT', blank=False,
                                                    null=True)
    rfq_suppliers_created_by = models.CharField(db_column='RFQ_SUPPLIERS_CREATED_BY', max_length=12,
                                                blank=False,
                                                null=True)
    rfq_suppliers_changed_at = models.DateTimeField(db_column='RFQ_SUPPLIERS_CHANGED_AT', blank=True,
                                                    null=True)
    rfq_suppliers_changed_by = models.CharField(db_column='RFQ_SUPPLIERS_CHANGED_BY', max_length=12,
                                                blank=False,
                                                null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        managed = True
        db_table = 'MTD_RFQ_SUPPLIERS'
