import operator
import os
from datetime import date

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models

from eProc_Configuration.models import OrgClients
from eProc_Shopping_Cart.models import DBQueries


class PoHeader(models.Model, DBQueries):
    po_header_guid = models.CharField(db_column='PO_HEADER_GUID', primary_key=True, max_length=32)
    doc_number = models.CharField(db_column='DOC_NUMBER', max_length=10, blank=False, null=False,
                                  verbose_name='PO Number')
    transaction_type = models.CharField(db_column='TRANSACTION_TYPE', null=False, max_length=10)  # eg SHC1
    posting_date = models.DateTimeField(db_column='POSTING_DATE', blank=True, null=True)
    version_type = models.CharField(db_column='VERSION_TYPE', max_length=1, blank=True, null=True,
                                    verbose_name='Version type')
    version_num = models.CharField(db_column='VERSION_NUM', max_length=8, blank=True, null=False,
                                   verbose_name='Version number')
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=False,
                                   verbose_name='PO NAME')
    language_id = models.CharField(db_column='LANGUAGE_ID', blank=True, null=True, max_length=2)
    gross_amount = models.CharField(db_column='GROSS_AMOUNT', max_length=15, blank=True, null=True,
                                    verbose_name='Gross Amount')
    total_tax = models.CharField(db_column='TOTAL_TAX', max_length=15, blank=True, null=True,
                                 verbose_name='Total Tax')  # sum of tax(item level sgst,cgst,vat)
    total_value = models.CharField(db_column='TOTAL_VALUE', max_length=15, blank=False, null=False,
                                   verbose_name='Total Value')  # sum(currency converted item value)
    total_value_appr = models.CharField(db_column='TOTAL_VALUE_APPR', max_length=15, blank=True, null=True,
                                        verbose_name='Total Value Appr')
    usr_budget_value = models.CharField(db_column='USR_BUDGET_VALUE', max_length=15, blank=True, null=True,
                                        verbose_name='User Budget Value')
    currency = models.CharField(db_column='CURRENCY', max_length=3, blank=False, null=False, verbose_name='Currency')
    payment_term = models.CharField(max_length=4, db_column='PAYMENT_TERM', blank=True, null=True)
    incoterm = models.CharField(max_length=3, db_column='INCOTERM', blank=True, null=True)
    incoterm_loc = models.CharField(max_length=28, db_column='INCOTERM_LOC', blank=True, null=True,
                                    verbose_name='Incoterm location')
    val_po_e = models.CharField(max_length=15, db_column='VAL_PO_E', blank=True, null=True,
                                verbose_name='Value of POs/Confirmations/Invoices Created for Contract')
    val_po_e_agg = models.CharField(max_length=15, db_column='VAL_PO_E_AGG', blank=True, null=True,
                                    verbose_name='Value of POs/Confirmations/Invoices Created for Contract')
    requester = models.CharField(db_column='REQUESTER', max_length=12, blank=False, null=False,
                                 verbose_name='Requester')
    status = models.CharField(db_column='STATUS', max_length=20, blank=False, null=False, verbose_name='Status')
    gr_gi_slip_no = models.CharField(db_column='GR_GI_SLIP_NO', max_length=10, blank=False, null=False,
                                     verbose_name='Status')
    bill_of_lading = models.CharField(db_column='BILL_OF_LADING', max_length=16, blank=False, null=False,
                                      verbose_name='Status')
    posting_date_FI = models.DateTimeField(db_column='POSTING_DATE_FI', blank=True, null=True,
                                           verbose_name='Transaction Posting Date in Accounting	POSTING_DATE_FI')
    ref_doc_no = models.CharField(db_column='REF_DOC_NO', max_length=16, blank=True, null=True,
                                  verbose_name='Ref Doc Number')
    po_header_created_at = models.DateTimeField(db_column='PO_HEADER_CREATED_AT', blank=False, null=False,
                                                verbose_name='Created At')
    po_header_created_by = models.CharField(db_column='PO_HEADER_CREATED_BY', max_length=12, blank=False, null=False,
                                            verbose_name='Creator')
    po_header_changed_at = models.DateTimeField(db_column='PO_HEADER_CHANGED_AT', blank=True, null=False,
                                                verbose_name='Changed At')
    po_header_changed_by = models.CharField(db_column='PO_HEADER_CHANGED_BY', max_length=12, blank=False, null=False,
                                            verbose_name='Changed By')
    document_type = models.CharField(db_column='DOCUMENT_TYPE', max_length=5, null=True)  # Doc02
    silent_po = models.BooleanField(default=False, null=False, db_column='SILENT_PO')
    ordered_at = models.DateTimeField(db_column='ORDERED_AT', blank=True, null=True, verbose_name='Ordered At')
    time_zone = models.CharField(db_column='TIME_ZONE', max_length=6, blank=True, null=False, verbose_name='Time Zone')
    company_code_id = models.CharField(db_column='COMPANY_CODE_ID', max_length=20, null=False)
    inv_addr_num = models.PositiveIntegerField(db_column='INV_ADDR_NUM', blank=True, null=True,
                                               verbose_name='Invoice address number')
    ship_addr_num = models.PositiveIntegerField(db_column='SHIP_ADDR_NUM', blank=True, null=True,
                                                verbose_name='Ship to Address Number')
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=12, blank=True, null=True,
                                   verbose_name='Supplier ID')
    supplier_username = models.CharField(max_length=40, db_column='SUPPLIER_USERNAME', blank=True, null=True)
    supplier_mobile_num = models.CharField(max_length=40, db_column='SUPPLIER_MOBILE_NUM', blank=True, null=True)
    supplier_fax_no = models.CharField(max_length=30, db_column='SUPPLIER_FAX_NO', blank=True, null=True)
    supplier_email = models.CharField(max_length=100, db_column='SUPPLIER_EMAIL', blank=True, null=True)
    pref_supplier = models.CharField(db_column='PREF_SUPPLIER', max_length=10, null=True,
                                     verbose_name='preferred supplier ')
    supp_type = models.CharField(db_column='SUPP_TYPE', max_length=35, blank=True, null=True,
                                 verbose_name='Supplier Type')
    delivery_days = models.CharField(db_column='DELIVERY_DAYS', max_length=20, null=True, blank=True)
    blocked_supplier = models.BooleanField(db_column='BLOCKED_SUPPLIER', default=False, null=False)
    # flag for checking po pdf successful generation
    po_pdf_creation_flag = models.BooleanField(db_column='PO_PDF_CREATION_FLAG', default=False, null=False)
    # flag for checking po pdf sent to supplier
    po_pdf_email_flag = models.BooleanField(db_column='PO_PDF_EMAIL_FLAG', default=False, null=False)
    tax_code = models.CharField(db_column='TAX_CODE', max_length=5, null=True, verbose_name='Tax Code')
    sgst = models.PositiveIntegerField(db_column='SGST', blank=True, null=True, verbose_name='State GST')
    cgst = models.PositiveIntegerField(db_column='CGST', blank=True, null=True, verbose_name='Central GST')
    vat = models.PositiveIntegerField(db_column='VAT', blank=True, null=True,
                                      verbose_name='Value Added Tax - VAT code (%age as decimal) returned from catalogue ')
    po_header_source_system = models.CharField(db_column='PO_HEADER_SOURCE_SYSTEM', max_length=20)
    pd_header_destination_system = models.CharField(db_column='PO_HEADER_DESTINATION_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        managed = True
        unique_together = ('client', 'doc_number')
        db_table = 'MTD_PO_HEADER'

    def __str__(self):
        return self.po_header_guid

    # Get header data by supplier id
    def get_hdr_data_by_supplier(self, sup_id):
        return PoHeader.objects.filter(supplier_id=sup_id).distinct()

    # Get header data by guid
    def get_hdr_data_by_guid(self, guid):
        return PoHeader.objects.filter(guid=guid)

    # Get header guid by object id
    @staticmethod
    def get_hdr_guid_by_objid(objid):
        try:
            hdr = PoHeader.objects.get(doc_number=objid)
            return getattr(hdr, 'guid')
        except ObjectDoesNotExist:
            return 'error'
        except MultipleObjectsReturned:
            hdr = PoHeader.objects.filter(doc_number=objid)
            hdr = sorted(hdr, key=operator.attrgetter('version_num'))
            return getattr(hdr[0], 'guid')

    # Get object id by guid
    @staticmethod
    def get_objid_by_guid(guid):
        try:
            return str(getattr(PoHeader.objects.get(guid=guid), 'doc_number'))
        except:
            return ''


class PoItem(models.Model):
    po_item_guid = models.CharField(db_column='PO_ITEM_GUID', primary_key=True, max_length=32)
    po_item_num = models.CharField(db_column='PO_ITEM_NUM', max_length=10, blank=True, null=True,
                                   verbose_name='Line Number')
    sc_doc_num = models.CharField(db_column='SC_DOC_NUM', max_length=10, blank=True, null=True,
                                  verbose_name='SC Number')
    rfq_doc_num = models.CharField(db_column='RFQ_DOC_NUM', max_length=10, blank=True, null=True,
                                   verbose_name='SC Number')
    sc_item_num = models.PositiveIntegerField(db_column='SC_ITEM_NUM', blank=False, null=False,
                                              verbose_name='Line Number')
    rfq_item_num = models.PositiveIntegerField(db_column='RFQ_ITEM_NUM', blank=True, null=True,
                                               verbose_name='Line Number')
    document_type = models.CharField(max_length=10, db_column='DOCUMENT_TYPE', null=True, blank=True)
    int_product_id = models.CharField(db_column='INT_PRODUCT_ID', max_length=20, null=True)
    supp_product_id = models.PositiveIntegerField(db_column='SUPP_PRODUCT_ID', null=True, blank=True)
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)
    long_desc = models.CharField(db_column='LONG_DESC', max_length=3000, blank=True, null=True,
                                 verbose_name='Product Long desc')
    stock_keeping_unit = models.CharField(db_column='STOCK_KEEPING_UNIT', max_length=32, null=True, blank=True)
    univeral_product_code = models.CharField(db_column='UNIVERAL_PRODUCT_CODE', max_length=32, null=True, blank=True)
    barcode = models.CharField(db_column='BARCODE', max_length=20, null=True, blank=True)
    itm_language_id = models.CharField(db_column='ITM_LANGUAGE_ID', blank=True, null=True, max_length=2,
                                       verbose_name=' Short Text Language for an Item ')
    order_date = models.DateTimeField(db_column='ORDER_DATE', null=True, blank=True)
    grp_ind = models.BooleanField(db_column='GRP_IND', default=False, null=True,
                                  verbose_name='Grouping logic for different product categories in purchaser cockpit')
    company_code_id = models.CharField(db_column='COMPANY_CODE_ID', max_length=20, null=False)
    del_datcat = models.CharField(db_column='DEL_DATCAT', blank=True, null=True, max_length=2,
                                  verbose_name='Date type (day, week, month, interval)')
    item_del_date = models.DateTimeField(db_column='ITEM_DEL_DATE', blank=False, null=True,
                                         verbose_name='Delivery Date')
    prod_cat_id = models.CharField(db_column='PROD_CAT_ID', max_length=20, null=False,
                                   verbose_name='UnspscCategories')
    prod_cat_desc = models.CharField(db_column='PROD_CAT_DESC', max_length=255, blank=True, null=True,
                                     verbose_name='Description')
    cust_prod_cat_id = models.CharField(db_column='CUST_PROD_CAT_ID', null=True, max_length=20,
                                        verbose_name='UnspscCategoriesCust')
    lead_time = models.PositiveIntegerField(db_column='LEAD_TIME', null=True, blank=True, verbose_name='Lead time')
    final_inv = models.BooleanField(default=False, null=True, blank=True, db_column='FINAL_INV')
    final_entry_ind = models.BooleanField(default=False, null=True, blank=True, db_column='FINAL_ENTRY_IND')
    overall_limit = models.DecimalField(db_column='OVERALL_LIMIT', max_digits=15, decimal_places=2, blank=True,
                                        null=True, verbose_name='overall limit')
    expected_value = models.DecimalField(db_column='EXPECTED_VALUE', max_digits=15, decimal_places=2, blank=True,
                                         null=True, verbose_name='expected value')
    start_date = models.DateTimeField(db_column='START_DATE', null=True, verbose_name='Start Date')
    end_date = models.DateTimeField(db_column='END_DATE', null=True, verbose_name='End date')
    required_on = models.DateField(null=True, blank=True, db_column='REQUIRED_ON')
    undef_limit = models.BooleanField(default=False, null=True, blank=True, db_column='UNDEF_LIMIT')
    ir_gr_ind_limi = models.BooleanField(db_column='IR_GR_IND_LIMI', default=False, null=True,
                                         verbose_name='Gr ind for LO')
    gr_ind_limi = models.BooleanField(db_column='GR_IND_LIMI', null=True, default=False, verbose_name='Gr ind for LO')
    val_cf_e = models.DecimalField(db_column='VAL_CF_E', max_digits=15, decimal_places=2, blank=True, null=True,
                                   verbose_name='Value of Entered Confirmations')
    val_cf = models.DecimalField(db_column='VAL_CF', max_digits=15, decimal_places=2, blank=True, null=True,
                                 verbose_name=' Value of Confirmations Released')
    val_iv_e = models.DecimalField(db_column='VAL_IV_E', max_digits=15, decimal_places=2, null=True, blank=True)
    val_iv = models.DecimalField(db_column='VAL_IV', max_digits=15, decimal_places=2, null=True, blank=True)
    val_po_e = models.DecimalField(db_column='VAL_PO_E', max_digits=15, decimal_places=2, null=True, blank=True)
    val_po_e_agg = models.DecimalField(db_column='VAL_PO_E_AGG', max_digits=15, decimal_places=2, null=True, blank=True)
    quan_cf_e = models.PositiveIntegerField(db_column='QUAN_CF_E', null=True, blank=True,
                                            verbose_name='Quantity of Entered Confirmation')
    quan_cf = models.PositiveIntegerField(db_column='QUAN_CF', null=True, blank=True,
                                          verbose_name='Quantity of Released Confirmations')
    quan_po_e = models.PositiveIntegerField(db_column='QUAN_PO_E', null=True, blank=True)
    num_cf = models.PositiveIntegerField(db_column='NUM_CF', null=True, blank=True,
                                         verbose_name='Number of Entered Confirmations for a Purchase Order')
    source_relevant_ind = models.BooleanField(db_column='SOURCE_RELEVANT_IND', default=False, null=True,
                                              verbose_name='Indicator - If the Document is Sourcing-Relevant ')
    ext_demid = models.CharField(db_column='EXT_DEMID', blank=True, null=True, max_length=2,
                                 verbose_name='External Requirement Number')
    ext_dem_posid = models.CharField(db_column='EXT_DEM_POSID', blank=True, null=True, max_length=2,
                                     verbose_name='External Requirement Tracking Number')
    offcatalog = models.BooleanField(db_column='OFFCATALOG', blank=True, null=True, default=False,
                                     verbose_name='Off Catalog Flag(false=Not from catalog)')
    process_flow = models.CharField(db_column='PROCESS_FLOW', max_length=20, blank=True, null=True,
                                    verbose_name='Item Category')
    # green - catalog,yellow - FT,red - PR
    quantity_min = models.PositiveIntegerField(db_column='QUANTITY_MIN', null=True, verbose_name='Quantity Min')
    quantity_max = models.PositiveIntegerField(db_column='QUANTITY_MAX', null=True, verbose_name='Quantity Max')
    tiered_flag = models.BooleanField(default=False, blank=True, null=True,
                                      db_column='TIERED_FLAG')  # set this if any dicount
    bundle_flag = models.BooleanField(default=False, blank=True, null=True, db_column='BUNDLE_FLAG')
    material_no = models.CharField(max_length=18, db_column='MATERIAL_NO', blank=True, null=True)
    sgst = models.DecimalField(db_column='SGST', max_digits=15, decimal_places=2, blank=True, null=True,
                               verbose_name='State GST')
    cgst = models.DecimalField(db_column='CGST', max_digits=15, decimal_places=2, blank=True, null=True,
                               verbose_name='Central GST')
    vat = models.DecimalField(db_column='VAT', max_digits=15, decimal_places=2, blank=True, null=True,
                              verbose_name='Value Added Tax - VAT code (%age as decimal) returned from catalogue ')
    prod_type = models.CharField(db_column='PROD_TYPE', max_length=2, blank=True, null=False,
                                 verbose_name='Product Type')  # 01-product,02- service
    catalog_id = models.CharField(db_column='CATALOG_ID', max_length=20, blank=True, null=True,
                                  verbose_name='Catalog ID')
    catalog_name = models.CharField(max_length=40, blank=True, null=True, db_column='CATALOG_NAME')
    fin_entry_ind = models.CharField(db_column='FIN_ENTRY_IND', max_length=1, blank=True, null=True,
                                     verbose_name='Fin entry ind')
    price_origin = models.CharField(max_length=1, db_column='PRICE_ORIGIN', null=True, blank=True)
    quantity = models.PositiveIntegerField(db_column='QUANTITY', null=False, verbose_name='Quantity')
    base_price = models.DecimalField(db_column='BASE_PRICE', max_digits=15, decimal_places=2, blank=True, null=True,
                                     verbose_name='base price of the item')
    additional_price = models.DecimalField(db_column='ADDITIONAL_PRICE', max_digits=15, decimal_places=2, blank=True,
                                           null=True,
                                           verbose_name='additionalprice of the item')
    actual_price = models.DecimalField(db_column='ACTUAL_PRICE', max_digits=15, decimal_places=2, blank=True, null=True,
                                       verbose_name='Price without discount')  # base price+ additional price
    discount_percentage = models.DecimalField(db_column='DISCOUNT_PERCENTAGE', max_digits=15, decimal_places=2,
                                              blank=True, null=True,
                                              verbose_name='Discount percentage')
    discount_value = models.DecimalField(db_column='DISCOUNT_VALUE', max_digits=15, decimal_places=2, blank=True,
                                         null=True,
                                         verbose_name='Discount value')  # (base_price)*discount_percentage
    price = models.DecimalField(db_column='PRICE', max_digits=15, decimal_places=2, blank=True, null=True,
                                verbose_name='Price')
    tax_value = models.DecimalField(db_column='TAX_VALUE', max_digits=15, decimal_places=2, blank=True, null=True,
                                    verbose_name='tax Value')  # (SGST *quantity)+(CGST *quantity)
    price_unit = models.CharField(db_column='PRICE_UNIT', max_length=5, blank=True, null=True,
                                  verbose_name='Price Unit')
    unit = models.CharField(db_column='UNIT', max_length=3, blank=False, null=False, verbose_name='Unit')
    gross_price = models.DecimalField(db_column='GROSS_PRICE', max_digits=15, decimal_places=2, blank=False, null=False,
                                      verbose_name='Gross Price')  # price + sales tax
    value = models.DecimalField(db_column='VALUE', max_digits=15, decimal_places=2, blank=True, null=True,
                                verbose_name='Value')  # (float(quantity) * float(gross price)) / int(price_unit)
    value_min = models.DecimalField(db_column='VALUE_MIN', max_digits=15, decimal_places=2, blank=True, null=True,
                                    verbose_name='Value')
    currency = models.CharField(db_column='CURRENCY', max_length=3, blank=False, null=False, verbose_name='Currency')
    tax_code = models.CharField(db_column='TAX_CODE', max_length=5, null=True, verbose_name='Tax Code')
    gr_ind = models.CharField(db_column='GR_IND', max_length=1, blank=True, null=True, verbose_name='Gr ind')
    ir_gr_ind = models.BooleanField(db_column='IR_GR_IND', default=False, null=True)
    ir_ind = models.BooleanField(db_column='IR_IND', default=False, null=True)
    po_resp = models.BooleanField(db_column='PO_RESP', default=False, null=True, verbose_name='PO Response')
    asn_ind = models.BooleanField(db_column='ASN_IND', default=False, null=True, verbose_name='Advance shipment Notice')
    eform_id = models.CharField(db_column='EFORM_ID', max_length=40, blank=False, null=True)
    discount_id = models.CharField(db_column='DISCOUNT_ID', max_length=40, blank=False, null=True)
    variant_id = models.CharField(db_column='VARIANT_ID', max_length=40, blank=False, null=True)
    product_info_id = models.CharField(db_column='PRODUCT_INFO_ID', max_length=40, blank=True, null=True)
    dis_rej_ind = models.BooleanField(default=False, null=True, blank=True, db_column='DIS_REJ_IND')
    goods_marking = models.CharField(max_length=60, db_column='GOODS_MARKING', blank=True, null=True)
    confirmed_qty = models.PositiveIntegerField(db_column='CONFIRMED_QTY', null=True, blank=True,
                                                verbose_name='Qunatity to be updated upon creation of confirmation')
    ctr_name = models.CharField(db_column='CTR_NAME', blank=True, null=True, max_length=50,
                                verbose_name='Contract Name')
    ctr_num = models.CharField(db_column='CTR_NUM', max_length=50, blank=True, null=True, verbose_name='ctr num')
    ctr_item_num = models.CharField(db_column='CTR_ITEM_NUM', max_length=50, blank=True, null=True,
                                    verbose_name='ctr num')
    pref_supplier = models.CharField(db_column='PREF_SUPPLIER', max_length=10, null=True,
                                     verbose_name='preferred supplier ')
    approved_by = models.CharField(max_length=16, db_column='APPROVED_BY', blank=True, null=True)
    call_off = models.CharField(db_column='CALL_OFF', null=True, max_length=20)
    manu_part_num = models.CharField(db_column='MANU_PART_NUM', max_length=40, blank=True, null=True,
                                     verbose_name='manu part num')
    manu_code_num = models.CharField(db_column='MANU_CODE_NUM', max_length=10, blank=True, null=True,
                                     verbose_name='manu code num')
    ship_from_addr_num = models.CharField(db_column='SHIP_from_ADDR_NUM', max_length=10, blank=True, null=True,
                                          verbose_name='ship from addr num')
    status = models.CharField(db_column='STATUS', max_length=20, blank=True, null=True, verbose_name='Status')
    bill_to_addr_num = models.CharField(db_column='BILL_TO_ADDR_NUM', max_length=10, blank=True, null=True,
                                        verbose_name='bill to addr num')
    ship_to_addr_num = models.CharField(db_column='SHIP_TO_ADDR_NUM', max_length=10, blank=True, null=True,
                                        verbose_name='ship to addr num')
    cash_disc1 = models.PositiveIntegerField(db_column='CASH_DISC1', blank=True, null=True,
                                             verbose_name='Discount % value to be filled (from eform table - qty based discount)')
    cash_disc2 = models.PositiveIntegerField(db_column='CASH_DISC2', blank=True, null=True,
                                             verbose_name='Discount % value to be filled (from eform table - qty based discount)')
    goods_recep = models.CharField(db_column='GOODS_RECEP', max_length=12, blank=True, null=True,
                                   verbose_name='Goods Recipient')
    manufacturer = models.CharField(db_column='MANUFACTURER', max_length=50, blank=True, null=True,
                                    verbose_name='Manufacturer')
    delivery_days = models.CharField(db_column='DELIVERY_DAYS', max_length=20, null=True,
                                     blank=True)  # supplier working day
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
    po_item_created_at = models.DateTimeField(db_column='CREATED_AT', blank=False, null=False,
                                              verbose_name='Created At')
    po_item_created_by = models.CharField(db_column='PO_ITEM_CREATED_BY', max_length=12, blank=False, null=False,
                                          verbose_name='Creator')
    po_item_changed_at = models.DateTimeField(db_column='PO_ITEM_CHANGED_AT', blank=True, null=False,
                                              verbose_name='Changed At')
    po_item_changed_by = models.CharField(db_column='PO_ITEM_CHANGED_BY', max_length=12, blank=False, null=False,
                                          verbose_name='Changed By')
    po_item_source_system = models.CharField(db_column='PO_ITEM_SOURCE_SYSTEM', max_length=20)
    po_item_destination_system = models.CharField(db_column='PO_ITEM_DESTINATION_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    po_header_guid = models.ForeignKey('eProc_Purchase_Order.PoHeader', models.DO_NOTHING, db_column='PO_HEADER_GUID',
                                       blank=False, null=False)
    sc_header_guid = models.ForeignKey('eProc_Shopping_Cart.ScHeader', models.DO_NOTHING, db_column='SC_HEADER_GUID',
                                       blank=True, null=True)
    sc_item_guid = models.ForeignKey('eProc_Shopping_Cart.ScItem', models.DO_NOTHING, db_column='SC_ITEM_GUID',
                                     blank=True,
                                     null=True)

    class Meta:
        managed = True
        db_table = 'MTD_PO_ITEM'

    def __str__(self):
        return self.po_item_guid

    # Get item data by header guid
    def get_itms_by_guid(self, hdr_guid):
        return PoItem.objects.filter(header_guid=hdr_guid).order_by('po_item_num')


class PoAccounting(models.Model):
    po_accounting_guid = models.CharField(db_column='PO_ACCOUNTING_GUID', primary_key=True, max_length=32)
    acc_item_num = models.DecimalField(db_column='ACC_ITEM_NUM', max_digits=4, decimal_places=0, blank=False,
                                       null=True, verbose_name='Number')
    acc_cat = models.CharField(db_column='ACC_CAT', max_length=5, blank=False, null=True,
                               verbose_name='Account Assignment Category')
    dist_perc = models.CharField(db_column='DIST_PERC', max_length=5, blank=True, null=True,
                                 verbose_name='Distribution Percentage')
    gl_acc_num = models.CharField(db_column='GL_ACC_NUM', max_length=10, blank=True, null=True,
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
    dist_qty = models.PositiveIntegerField(db_column='DIST_QTY', null=True)
    dist_val = models.PositiveIntegerField(db_column='DIST_VAL', null=True)
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

    po_accounting_created_at = models.DateTimeField(db_column='PO_ACCOUNTING_CREATED_AT', blank=False, null=True)
    po_accounting_created_by = models.CharField(db_column='PO_ACCOUNTING_CREATED_BY', max_length=12, blank=False,
                                                null=True)
    po_accounting_changed_at = models.DateTimeField(db_column='PO_ACCOUNTING_CHANGED_AT', blank=True, null=True)
    po_accounting_changed_by = models.CharField(db_column='PO_ACCOUNTING_CHANGED_BY', max_length=12, blank=False,
                                                null=True)
    po_accounting_source_system = models.CharField(db_column='PO_ACCOUNTING_SOURCE_SYSTEM', max_length=20)
    po_accounting_destination_system = models.CharField(db_column='PO_ACCOUNTING_DESTINATION_SYSTEM', max_length=20,
                                                        null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    po_header_guid = models.ForeignKey('eProc_Purchase_Order.PoHeader', models.DO_NOTHING, db_column='PO_HEADER_GUID',
                                       blank=True, null=True)
    po_item_guid = models.ForeignKey('eProc_Purchase_Order.PoItem', models.DO_NOTHING, db_column='PO_ITEM_GUID',
                                     blank=True,
                                     null=True)

    class Meta:
        managed = True
        db_table = 'MTD_PO_ACCOUNTING'

    def __str__(self):
        return self.po_accounting_guid

    # Get accounting data by item guid
    def get_acc_data_by_guid(self, itm_guid):
        return PoAccounting.objects.filter(item_guid__in=itm_guid).order_by('acc_item_num')


class PoApproval(models.Model):
    po_approval_guid = models.CharField(db_column='PO_APPROVAL_GUID', primary_key=True, max_length=32)
    step_num = models.CharField(db_column='STEP_NUM', max_length=3, blank=True, null=True, verbose_name='Sequence')
    app_desc = models.CharField(db_column='APP_DESC', max_length=60, blank=True, null=True,
                                verbose_name='Agent Determination')
    proc_lvl_sts = models.CharField(db_column='PROC_LVL_STS', max_length=10, blank=True, null=True,
                                    verbose_name='Level Status')
    app_sts = models.CharField(db_column='APP_STS', max_length=20, blank=True, null=True, verbose_name='Status')
    app_id = models.CharField(db_column='APP_ID', max_length=70, blank=True, null=True, verbose_name='Processor')
    received_time = models.DateTimeField(db_column='RECEIVED_TIME', blank=True, null=True, verbose_name='Received On')
    proc_time = models.DateTimeField(db_column='PROC_TIME', blank=True, null=True, verbose_name='Processed On')
    time_zone = models.CharField(db_column='TIME_ZONE', max_length=6, blank=True, null=True, verbose_name='Time Zone')
    app_types = models.CharField(db_column='APP_TYPES', max_length=30, null=True)
    multiple_approver_flag = models.BooleanField(db_column='MULTIPLE_APPROVER_FLAG', default=False, null=True,
                                                 verbose_name='Multiple Approver flag')
    po_approval_created_at = models.DateTimeField(db_column='PO_APPROVAL_CREATED_AT', blank=False, null=True)
    po_approval_created_by = models.CharField(db_column='PO_APPROVAL_CREATED_BY', max_length=12, blank=False,
                                              null=True)
    po_approval_changed_at = models.DateTimeField(db_column='PO_APPROVAL_CHANGED_AT', blank=True, null=True)
    po_approval_changed_by = models.CharField(db_column='PO_APPROVAL_CHANGED_BY', max_length=12, blank=False,
                                              null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    po_header_guid = models.ForeignKey('eProc_Purchase_Order.PoHeader', models.DO_NOTHING, db_column='PO_HEADER_GUID')
    po_item_guid = models.ForeignKey('eProc_Purchase_Order.PoItem', models.DO_NOTHING, db_column='PO_ITEM_GUID',
                                     blank=True,
                                     null=True)

    class Meta:
        managed = True
        db_table = 'MTD_PO_APPROVAL'

    def __str__(self):
        return self.po_approval_guid

    # Get approval data by header guid
    def get_apprs_by_guid(self, hdr_guid):
        app_data = PoApproval.objects.filter(header_guid=hdr_guid).order_by('step_num')
        return app_data


class PoPotentialApproval(models.Model):
    po_potential_approval_guid = models.CharField(db_column='po_potential_approval_guid', primary_key=True,
                                                  max_length=32)
    app_id = models.CharField(db_column='APP_ID', max_length=70, blank=True, null=True, verbose_name='Approver ID')
    step_num = models.CharField(db_column='STEP_NUM', max_length=3, blank=True, null=True, verbose_name='Sequence')
    app_sts = models.CharField(db_column='APP_STS', max_length=20, blank=True, null=True, verbose_name='Status')
    proc_lvl_sts = models.CharField(db_column='PROC_LVL_STS', max_length=10, blank=True, null=True,
                                    verbose_name='Level Status')
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    po_approval_guid = models.ForeignKey('eProc_Purchase_Order.PoApproval', models.DO_NOTHING,
                                         db_column='PO_APPROVAL_GUID', blank=True,
                                         null=True)
    po_header_guid = models.ForeignKey('eProc_Purchase_Order.PoHeader', models.DO_NOTHING, db_column='PO_HEADER_GUID',
                                       null=True)

    class Meta:
        managed = True
        db_table = 'MTD_PO_POTENTIAL_APPROVAL'

    def __str__(self):
        return self.po_potential_approval_guid


class PoAddresses(models.Model):
    po_addresses_guid = models.CharField(db_column='PO_ADDRESSES_GUID', primary_key=True, max_length=32)
    item_num = models.PositiveIntegerField(db_column='ITEM_NUM', blank=False, null=False, verbose_name='Item Number',
                                           default=0)
    address_number = models.PositiveIntegerField(db_column='ADDRESS_NUMBER', null=True)
    address_type = models.CharField(db_column='ADDRESS_TYPE', max_length=1, null=True, blank=True)
    address_partner_type = models.ForeignKey('eProc_Configuration.AddressPartnerType', models.DO_NOTHING,
                                             db_column='ADDRESS_PARTNER_TYPE', null=True)
    title = models.CharField(db_column='TITLE', max_length=40, null=True)
    name1 = models.CharField(db_column='NAME1', max_length=40, null=True, verbose_name='First Name')
    name2 = models.CharField(db_column='NAME2', max_length=40, null=True, verbose_name='Last Name')
    street = models.CharField(db_column='STREET', max_length=100, null=False, verbose_name='Street')
    area = models.CharField(db_column='AREA', max_length=100, null=False, verbose_name='Area')
    landmark = models.CharField(db_column='LANDMARK', max_length=50, null=False, verbose_name='Landmark')
    city = models.CharField(db_column='CITY', max_length=20, null=False, verbose_name='City')
    postal_code = models.CharField(db_column='POSTAL_CODE', max_length=10, null=False, verbose_name='Postal Code', )
    region = models.CharField(db_column='REGION', max_length=30, null=False, verbose_name='Region')
    country_code = models.CharField(db_column='COUNTRY_CODE', max_length=2, null=True,
                                    verbose_name='Country')
    language_id = models.CharField(db_column='LANGUAGE_ID', max_length=2, verbose_name='Language', null=True)
    mobile_number = models.CharField(db_column='MOBILE_NUMBER', max_length=20, verbose_name='Mobile', null=True,
                                     blank=True)
    telephone_number = models.CharField(db_column='TELEPHONE_NUMBER', max_length=20, verbose_name='Telephone',
                                        null=True, blank=True)
    fax_number = models.CharField(db_column='FAX_NUMBER', max_length=30, null=True, blank=False, verbose_name='Fax')
    email = models.EmailField(db_column='EMAIL', max_length=100, null=True)
    time_zone = models.CharField(db_column='TIME_ZONE', max_length=6, null=True)
    po_addr_created_at = models.DateTimeField(db_column='PO_ADDR_CREATED_AT', blank=False, null=True)
    po_addr_created_by = models.CharField(db_column='PO_ADDR_CREATED_BY', max_length=12, blank=False, null=True)
    po_addr_changed_at = models.DateTimeField(db_column='PO_ADDR_CHANGED_AT', blank=True, null=True)
    po_addr_changed_by = models.CharField(db_column='PO_ADDR_CHANGED_BY', max_length=12, blank=False, null=True)
    po_addresses_source_system = models.CharField(db_column='PO_ADDRESSES_SOURCE_SYSTEM', max_length=20)
    po_addresses_destination_system = models.CharField(db_column='PO_ADDRESSES_DESTINATION_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=True)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=True)
    po_header_guid = models.ForeignKey('eProc_Purchase_Order.PoHeader', models.DO_NOTHING, db_column='PO_HEADER_GUID',
                                       null=True)
    po_item_guid = models.ForeignKey('eProc_Purchase_Order.PoItem', models.DO_NOTHING, db_column='PO_ITEM_GUID',
                                     blank=True, null=True)

    class Meta:
        db_table = "MTD_PO_ADDRESSES"
        managed = True

    def __str__(self):
        return self.po_addresses_guid
