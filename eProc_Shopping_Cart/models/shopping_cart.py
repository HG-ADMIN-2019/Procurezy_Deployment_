from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import re

# Definition of SC Header table structure
from eProc_Basic.Utilities.global_defination import global_variables


class DBQueries():
    def get_hdr_data_by_objid(self, obj, objid, client):
        return obj.objects.filter(doc_number=objid, client=client, del_ind=False).values().order_by('doc_number')

    def get_hdr_data_by_doc_num(self, obj, client):
        return obj.objects.filter(client=client, del_ind=False).values().order_by('doc_number')

    def get_hdr_data_by_objid_app_monitoring(self, obj, objid, error_type, client):
        return obj.objects.filter(doc_number=objid, transmission_error_type=error_type, client=client,
                                  del_ind=False).values().order_by('doc_number')

    # start of MEP:19
    def get_order_data_by_fields(self, client, obj, supp_query, creator_query, requester_query, SCName_query, **kwargs):
        return obj.objects.filter(supp_query, creator_query, requester_query, SCName_query, client=client,
                                  del_ind=False, **kwargs).order_by('doc_number')

    # End of MEP:19
    def get_hdr_data_by_fields(self, obj, objid, client):
        return obj.objects.filter(doc_number=objid, client=client,
                                  del_ind=False).values('doc_number').order_by('doc_number')

    def get_hdr_data_for_docnum(self, client, obj, doc_num_query,
                                **kwargs):
        return obj.objects.filter(doc_num_query, client=client,
                                  del_ind=False,
                                  **kwargs).values().order_by('doc_number')

    def get_hdr_data_by_fields_value(self, client, obj, supp_query, creator_query, requester_query, doc_num_query,
                                     **kwargs):
        return obj.objects.filter(supp_query, creator_query, requester_query, doc_num_query, client=client,
                                  del_ind=False,
                                  **kwargs).values().order_by('doc_number')

    def get_hdr_data_by_fields1(self, client, obj, supp_query, creator_query, requester_query, **kwargs):
        return obj.objects.filter(supp_query, creator_query, requester_query, client=client, del_ind=False,
                                  **kwargs).order_by('doc_number')


class ScHeader(models.Model, DBQueries):
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
    doc_closed = models.BooleanField(default=False, null=False, db_column='DOC_CLOSED')
    doc_incomplete = models.BooleanField(default=False, null=False, db_column='DOC_INCOMPLETE')
    doc_flow_ctrl = models.BooleanField(default=False, null=False, db_column='DOC_FLOW_CTRL')
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
                                             verbose_name='PO creation error flag')
    transmission_error_type = models.CharField(db_column='TRANSMISSION_ERROR_TYPE', max_length=30, blank=True,
                                               null=True,
                                               verbose_name='PO creation error type eg:PO_SPLIT,TRANSACTION_TYPE ')
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
    gl_acc_num = models.CharField(db_column='GL_ACC_NUM', max_length=10, blank=True, null=True,
                                  verbose_name='GL Account Number')
    version_type = models.CharField(db_column='VERSION_TYPE', max_length=1, blank=True, null=True,
                                    verbose_name='Version Type')
    group_sc = models.CharField(db_column='GROUP_SC', max_length=8, blank=True, null=True, verbose_name='Group SC')
    time_zone = models.CharField(db_column='TIME_ZONE', max_length=6, blank=True, null=True, verbose_name='Time Zone')
    posting_date = models.DateTimeField(db_column='POSTING_DATE', blank=True, null=True)
    language_id = models.CharField(db_column='LANGUAGE_ID', blank=True, null=True, max_length=2)

    document_type = models.CharField(db_column='DOCUMENT_TYPE', max_length=5, null=True)

    archivable_flag = models.BooleanField(db_column='ARCHIVABLE_FLAG', default=False, null=True,
                                          verbose_name='Achievable Flag')
    sc_header_source_system = models.CharField(db_column='SC_HEADER_SOURCE_SYSTEM', max_length=20)
    sc_header_destination_system = models.CharField(db_column='SC_HEADER_DESTINATION_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        managed = True
        unique_together = ('client', 'doc_number', 'sc_header_source_system'), \
                          ('client', 'doc_number', 'sc_header_destination_system')
        db_table = 'MTD_SC_HEADER'

    def __str__(self):
        return self.guid

    # Get header data by guid
    def get_hdr_data_by_guid(self, guid):
        return ScHeader.objects.filter(guid=guid, del_ind=False).values()

    # Get header guid by object id
    @staticmethod
    def get_hdr_guid_by_objid(objid):
        try:
            hdr = ScHeader.objects.get(doc_number=objid, del_ind=False)
            return getattr(hdr, 'guid')
        except ObjectDoesNotExist:
            return 'error'

    # start of MEP:19
    @staticmethod
    def get_desc_by_scname(scname):

        if '*' in scname:
            created_by = re.search(r'[a-zA-Z0-9]+', scname)
            if scname[0] == '*' and scname[-1] == '*':
                queryset = ScHeader.objects.values_list('description', flat=False).filter(
                    description__icontains=created_by.group(0), del_ind=False)
            elif scname[0] == '*':
                queryset = ScHeader.objects.values_list('description', flat=False).filter(
                    description__iendswith=created_by.group(0), del_ind=False)
            else:
                queryset = ScHeader.objects.values_list('description', flat=False).filter(
                    description__istartswith=created_by.group(0), del_ind=False)
        else:
            queryset = ScHeader.objects.values_list('description', flat=False).filter(description=scname, del_ind=False)
        scname_list = []
        for field in queryset:
            scname_list.append(field[0])
        return scname_list
    # End of MEP:19


# Definition of SC Item table structure
class ScItem(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    item_num = models.PositiveIntegerField(db_column='ITEM_NUM', blank=False, null=False, verbose_name='Line Number')
    po_doc_num = models.CharField(db_column='po_doc_num', max_length=10, blank=True, null=True,
                                  verbose_name='PO Doc Number')
    po_header_guid = models.CharField(db_column='PO_HEADER_GUID', max_length=32, blank=True, null=True)
    po_item_num = models.CharField(db_column='PO_ITEM_NUM', max_length=10, blank=True, null=True,
                                   verbose_name='Item Number')
    prod_cat_desc = models.CharField(db_column='PROD_CAT_DESC', max_length=255, blank=False, null=False,
                                     verbose_name='Description')
    eform_id = models.CharField(db_column='EFORM_ID', max_length=40, blank=False, null=True)
    discount_id = models.CharField(db_column='DISCOUNT_ID', max_length=40, blank=False, null=True)
    variant_id = models.CharField(db_column='VARIANT_ID', max_length=40, blank=False, null=True)
    product_info_id = models.CharField(db_column='PRODUCT_INFO_ID', max_length=40, blank=True, null=True)
    comp_code = models.CharField(db_column='COMP_CODE', max_length=10, blank=False, null=False,
                                 verbose_name='Company Code')
    purch_grp = models.CharField(db_column='PURCH_GRP', max_length=20, blank=True, null=True,
                                 verbose_name='Purchasing Group')
    purch_org = models.CharField(db_column='PURCH_ORG', max_length=20, blank=True, null=True,
                                 verbose_name='Purchasing Organization')
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=12, blank=True, null=True,
                                   verbose_name='Supplier ID')
    ship_from_addr_num = models.CharField(db_column='SHIP_FROM_ADDR_NUM', max_length=10, blank=True, null=True,
                                          verbose_name='ship from addr num')
    pref_supplier = models.CharField(db_column='PREF_SUPPLIER', max_length=10, null=True,
                                     verbose_name='preferred supplier ')
    process_flow = models.CharField(db_column='PROCESS_FLOW', max_length=20, blank=True, null=True,
                                    verbose_name='Item Category')
    prod_cat_id = models.CharField(db_column='PROD_CAT_ID', max_length=20, blank=False, null=False, default=None,
                                   verbose_name='Product Category')
    prod_type = models.CharField(db_column='PROD_TYPE', max_length=2, blank=False, null=True,
                                 verbose_name='Product Type')
    catalog_id = models.CharField(db_column='CATALOG_ID', max_length=20, blank=True, null=True,
                                  verbose_name='Catalog ID')
    ctr_num = models.CharField(db_column='CTR_NUM', max_length=50, blank=True, null=True, verbose_name='ctr num')
    ctr_item_num = models.CharField(db_column='CTR_ITEM_NUM', max_length=50, blank=True, null=True,
                                    verbose_name='ctr num')
    cust_prod_cat_id = models.CharField(db_column='CUST_PROD_CAT_ID', max_length=20, blank=True, null=True,
                                        verbose_name='UNSPSC')
    fin_entry_ind = models.BooleanField(db_column='FIN_ENTRY_IND', blank=True, default=False, null=True,
                                        verbose_name='Fin entry ind')
    item_del_date = models.DateTimeField(db_column='ITEM_DEL_DATE', blank=False, null=True,
                                         verbose_name='Delivery Date')
    start_date = models.DateTimeField(db_column='START_DATE', null=True, verbose_name='Start Date')
    end_date = models.DateTimeField(db_column='END_DATE', null=True, verbose_name='End date')
    quantity = models.PositiveIntegerField(db_column='QUANTITY', null=True, verbose_name='Quantity')
    quantity_min = models.PositiveIntegerField(db_column='QUANTITY_MIN', null=True, verbose_name='Quantity Min')
    quantity_max = models.PositiveIntegerField(db_column='QUANTITY_MAX', null=True, verbose_name='Quantity Max')
    value_min = models.PositiveIntegerField(db_column='VALUE_MIN', null=True, verbose_name='Value Min')
    min_order_value = models.DecimalField(db_column='MIN_ORDER_VALUE', max_digits=15, decimal_places=2, blank=True,
                                          null=True, verbose_name='Value')
    tiered_flag = models.BooleanField(default=False, null=False, db_column='TIERED_FLAG')
    bundle_flag = models.CharField(db_column='BUNDLE_FLAG', null=True, max_length=1)
    int_product_id = models.CharField(db_column='INT_PRODUCT_ID', max_length=20, null=True)
    tax_code = models.CharField(db_column='TAX_CODE', max_length=5, null=True, verbose_name='Tax Code')
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
    overall_limit = models.DecimalField(db_column='OVERALL_LIMIT', max_digits=15, decimal_places=2, blank=True,
                                        null=True, verbose_name='overall limit')
    expected_value = models.DecimalField(db_column='EXPECTED_VALUE', max_digits=15, decimal_places=2, blank=True,
                                         null=True, verbose_name='expected value')
    ir_gr_ind_limi = models.BooleanField(db_column='IR_GR_IND_LIMI', null=True, default=False)  # only for limit order
    gr_ind_limi = models.BooleanField(db_column='GR_IND_LIMI', null=True, default=False,
                                      verbose_name='Gr ind')  # only for limit order
    undef_limit = models.BooleanField(default=False, null=False, db_column='UNDEF_LIMIT')
    gr_ind = models.BooleanField(db_column='GR_IND', null=True, default=False, verbose_name='Gr ind')
    ir_ind = models.BooleanField(db_column='IR_IND', null=True, default=False)
    ir_gr_ind = models.BooleanField(db_column='IR_GR_IND', default=False, null=True)
    po_resp = models.BooleanField(db_column='PO_RESP', default=False, null=True, verbose_name='PO Response')
    asn_ind = models.BooleanField(db_column='ASN_IND', default=False, null=True, verbose_name='Advance shipment Notice')
    dis_rej_ind = models.BooleanField(default=False, null=False, db_column='DIS_REJ_IND')
    supp_product_id = models.CharField(db_column='supp_product_id', max_length=40, blank=True, null=True,
                                       verbose_name='Supplier Product Number')
    manu_part_num = models.CharField(db_column='MANU_PART_NUM', max_length=40, blank=True, null=True,
                                     verbose_name='manu part num')
    manu_code_num = models.CharField(db_column='MANU_CODE_NUM', max_length=10, blank=True, null=True,
                                     verbose_name='manu code num')
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
    catalog_name = models.CharField(max_length=40, blank=True, null=True, db_column='CATALOG_NAME')
    lead_time = models.PositiveIntegerField(db_column='LEAD_TIME', null=True, blank=True, verbose_name='Lead time')
    price_origin = models.CharField(max_length=1, db_column='PRICE_ORIGIN', null=True, blank=True)
    final_inv = models.BooleanField(default=False, null=False, db_column='FINAL_INV')
    val_cf_e = models.DecimalField(db_column='VAL_CF_E', max_digits=15, decimal_places=2, blank=True, null=True,
                                   verbose_name='Value of Entered Confirmations')
    val_cf = models.DecimalField(db_column='VAL_CF', max_digits=15, decimal_places=2, blank=True, null=True,
                                 verbose_name='Value of Confirmations Released')
    val_iv_e = models.PositiveIntegerField(db_column='VAL_IV_E', null=True, blank=True)
    val_iv = models.PositiveIntegerField(db_column='VAL_IV', null=True, blank=True)
    val_po_e = models.PositiveIntegerField(db_column='VAL_PO_E', null=True, blank=True)
    val_po_e_agg = models.PositiveIntegerField(db_column='VAL_PO_E_AGG', null=True, blank=True)
    quan_cf_e = models.PositiveIntegerField(db_column='QUAN_CF_E', null=True, blank=True)
    quan_cf = models.PositiveIntegerField(db_column='QUAN_CF', null=True, blank=True)
    quan_po_e = models.PositiveIntegerField(db_column='QUAN_PO_E', null=True, blank=True)
    offcatalog = models.BooleanField(db_column='OFFCATALOG', blank=True, default=False, null=True)
    supp_type = models.CharField(db_column='SUPP_TYPE', max_length=35, blank=True, null=True,
                                 verbose_name='Supplier Type')
    catalog_qty = models.PositiveIntegerField(db_column='CATALOG_QTY', null=True, blank=True)
    material_no = models.CharField(max_length=18, db_column='MATERIAL_NO', blank=True, null=True)
    incoterm = models.CharField(max_length=3, db_column='INCOTERM', blank=True, null=True)
    incoterm_loc = models.CharField(max_length=28, db_column='INCOTERM_LOC', blank=True, null=True)
    payment_term = models.CharField(max_length=4, db_column='PAYMENT_TERM', blank=True, null=True)
    be_obj_item = models.CharField(max_length=10, db_column='BE_OBJ_ITEM', blank=True, null=True)
    be_object_id = models.CharField(max_length=20, db_column='BE_OBJECT_ID', blank=True, null=True)
    be_stge_loc = models.CharField(max_length=4, db_column='BE_STGE_LOC', blank=True, null=True)
    be_plant = models.CharField(max_length=4, db_column='BE_PLANT', blank=True, null=True)
    be_doc_type = models.CharField(max_length=4, db_column='BE_doc_type', blank=True, null=True)
    goods_marking = models.CharField(max_length=60, db_column='GOODS_MARKING', blank=True, null=True)
    approved_by = models.CharField(max_length=16, db_column='APPROVED_BY', blank=True, null=True)
    silent_po = models.BooleanField(default=False, null=False, db_column='SILENT_PO')
    supplier_username = models.CharField(max_length=40, db_column='SUPPLIER_USERNAME', blank=True, null=True)
    supplier_mobile_num = models.CharField(max_length=40, db_column='SUPPLIER_MOBILE_NUM', blank=True, null=True)
    supplier_fax_no = models.CharField(max_length=30, db_column='SUPPLIER_FAX_NO', blank=True, null=True)
    supplier_email = models.CharField(max_length=100, db_column='SUPPLIER_EMAIL', blank=True, null=True)
    delivery_days = models.CharField(db_column='DELIVERY_DAYS', max_length=20, null=True, blank=True)
    po_transaction_type = models.CharField(db_column='PO_TRANSACTION_TYPE', null=True, blank=True,
                                           max_length=10)  # Transaction number of PO eg SHC1,SHC2
    blocked_supplier = models.CharField(max_length=10, db_column='BLOCKED_SUPPLIER', blank=True, null=True)
    required_on = models.DateField(null=True, blank=True, db_column='REQUIRED_ON')
    description = models.CharField(db_column='DESCRIPTION', max_length=1000, blank=False, null=False)
    long_desc = models.CharField(db_column='LONG_DESC', max_length=3000, blank=True, null=True,
                                 verbose_name='Product Long desc')
    stock_keeping_unit = models.CharField(db_column='STOCK_KEEPING_UNIT', max_length=32, null=True, blank=True)
    univeral_product_code = models.CharField(db_column='UNIVERAL_PRODUCT_CODE', max_length=32, null=True, blank=True)
    barcode = models.CharField(db_column='BARCODE', max_length=20, null=True, blank=True)
    saved_item_flag = models.BooleanField(default=False, null=True, db_column='SAVED_ITEM_FLAG')
    itm_language_id = models.CharField(db_column='ITM_LANGUAGE_ID', blank=True, null=True, max_length=2,
                                       verbose_name=' Short Text Language for an Item ')
    grp_ind = models.BooleanField(db_column='GRP_IND', default=False, null=True,
                                  verbose_name='Grouping logic for different product categories in purchaser cockpit')
    del_datcat = models.CharField(db_column='DEL_DATCAT', blank=True, null=True, max_length=2,
                                  verbose_name='Date type (day, week, month, interval)')
    source_relevant_ind = models.BooleanField(db_column='SOURCE_RELEVANT_IND', default=False, null=True,
                                              verbose_name='Indicator - If the Document is Sourcing-Relevant ')
    grouping_ind = models.BooleanField(db_column='grouping_ind', default=False, null=True,
                                       verbose_name='grouping_ind ')
    ext_demid = models.CharField(db_column='EXT_DEMID', blank=True, null=True, max_length=2,
                                 verbose_name='External Requirement Number')
    ext_dem_posid = models.CharField(db_column='EXT_DEM_POSID', blank=True, null=True, max_length=2,
                                     verbose_name='External Requirement Tracking Number')
    be_po_trans_type = models.CharField(db_column='BE_PO_TRANS_TYPE', blank=True, null=True, max_length=10,
                                        verbose_name='PO transaction type in ERP system (ECPO)')
    ctr_name = models.CharField(db_column='CTR_NAME', blank=True, null=True, max_length=50,
                                verbose_name='Contract Name')
    confirmed_qty = models.PositiveIntegerField(db_column='CONFIRMED_QTY', null=True, blank=True,
                                                verbose_name='Qunatity to be updated upon creation of confirmation')
    sgst = models.DecimalField(db_column='SGST', max_digits=15, decimal_places=2, blank=True, null=True,
                               verbose_name='State GST')
    cgst = models.DecimalField(db_column='CGST', max_digits=15, decimal_places=2, blank=True, null=True,
                               verbose_name='Central GST')
    vat = models.DecimalField(db_column='VAT', max_digits=15, decimal_places=2, blank=True, null=True,
                              verbose_name='Value Added Tax - VAT code (%age as decimal) returned from catalogue ')

    cash_disc1 = models.PositiveIntegerField(db_column='CASH_DISC1', blank=True, null=True,
                                             verbose_name='Discount % value to be filled (from eform table - qty based discount)')
    cash_disc2 = models.PositiveIntegerField(db_column='CASH_DISC2', blank=True, null=True,
                                             verbose_name='Discount % value to be filled (from eform table - qty based discount)')
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
    sc_item_source_system = models.CharField(db_column='SC_ITEM_SOURCE_SYSTEM', max_length=20)
    sc_item_destination_system = models.CharField(db_column='SC_ITEM_DESTINATION_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    header_guid = models.ForeignKey('eProc_Shopping_Cart.ScHeader', models.DO_NOTHING, db_column='HEADER_GUID',
                                    blank=True, null=True)
    po_item_guid = models.ForeignKey('eProc_Purchase_Order.PoItem', models.DO_NOTHING, db_column='ITEM_GUID',
                                     blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'MTD_SC_ITEM'

    # Get item data by header guid
    def get_itms_by_guid(self, hdr_guid):
        return ScItem.objects.filter(header_guid=hdr_guid, del_ind=False).order_by('item_num')

    @staticmethod
    def get_prod_cat_id(prod_cat):
        if '*' in prod_cat:
            prd_cat = re.search(r'[a-zA-Z0-9]+', prod_cat)
            if prod_cat[0] == '*' and prod_cat[-1] == '*':
                queryset = ScItem.objects.values_list('description', flat=False).filter(
                    description__icontains=prd_cat.group(0))
            elif prod_cat[0] == '*':
                queryset = ScItem.objects.values_list('description', flat=False).filter(
                    description__iendswith=prd_cat.group(0))
            else:
                queryset = ScItem.objects.values_list('description', flat=False).filter(
                    description__istartswith=prd_cat.group(0))

        else:
            queryset = ScItem.objects.values_list('description', flat=False).filter(description=prod_cat)
        prod_cat_list = []
        for field in queryset:
            prod_cat_list.append(field[0])
        return prod_cat_list

    @staticmethod
    def get_item_data_by_objid(self, obj, objid, client):
        return obj.objects.filter(doc_number=objid, client=client, del_ind=False).values().order_by('doc_number')

    @staticmethod
    def get_item_data_by_fields(client, obj, prod_cat_query, **kwargs):
        return obj.objects.filter(prod_cat_query, client=client, del_ind=False,
                                  **kwargs).values().order_by()

    @staticmethod
    def get_item_data_by_fields_src(client, obj, prod_cat_query, company_query, **kwargs):
        return list(obj.objects.filter(prod_cat_query, company_query, source_relevant_ind=True, po_doc_num=None,
                                       client=client, del_ind=False,
                                       **kwargs).values().order_by())


# Definition of SC Accounting table structure
class ScAccounting(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
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

    sc_accounting_created_at = models.DateTimeField(db_column='SC_ACCOUNTING_CREATED_AT', blank=False, null=True)
    sc_accounting_created_by = models.CharField(db_column='SC_ACCOUNTING_CREATED_BY', max_length=12, blank=False,
                                                null=True)
    sc_accounting_changed_at = models.DateTimeField(db_column='SC_ACCOUNTING_CHANGED_AT', blank=True, null=True)
    sc_accounting_changed_by = models.CharField(db_column='SC_ACCOUNTING_CHANGED_BY', max_length=12, blank=False,
                                                null=True)
    sc_accounting_source_system = models.CharField(db_column='SC_ACCOUNTING_SOURCE_SYSTEM', max_length=20)
    sc_accounting_destination_system = models.CharField(db_column='SC_ACCOUNTING_DESTINATION_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    header_guid = models.ForeignKey('eProc_Shopping_Cart.ScHeader', models.DO_NOTHING, db_column='HEADER_GUID',
                                    blank=True, null=True)
    item_guid = models.ForeignKey('eProc_Shopping_Cart.ScItem', models.DO_NOTHING, db_column='ITEM_GUID', blank=True,
                                  null=True)

    class Meta:
        managed = True
        db_table = 'MTD_SC_ACCOUNTING'

    # Get accounting data by item guid
    def get_acc_data_by_guid(self, itm_guid):
        return ScAccounting.objects.filter(item_guid__in=itm_guid, del_ind=False).order_by('acc_item_num').values()


# Definition of SC Approval table structure
class ScApproval(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
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
    sc_approval_created_at = models.DateTimeField(db_column='SC_APPROVAL_CREATED_AT', blank=False, null=True)
    sc_approval_created_by = models.CharField(db_column='SC_APPROVAL_CREATED_BY', max_length=12, blank=False,
                                              null=True)
    sc_approval_changed_at = models.DateTimeField(db_column='SC_APPROVAL_CHANGED_AT', blank=True, null=True)
    sc_approval_changed_by = models.CharField(db_column='SC_APPROVAL_CHANGED_BY', max_length=12, blank=False,
                                              null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    header_guid = models.ForeignKey('eProc_Shopping_Cart.ScHeader', models.DO_NOTHING, db_column='HEADER_GUID')
    item_guid = models.ForeignKey('eProc_Shopping_Cart.ScItem', models.DO_NOTHING, db_column='ITEM_GUID', blank=True,
                                  null=True)

    class Meta:
        managed = True
        db_table = 'MTD_SC_APPROVAL'

    # Get approval data by header guid
    def get_apprs_by_guid(self, hdr_guid):
        return ScApproval.objects.filter(header_guid=hdr_guid, del_ind=False).order_by('step_num')


class ScPotentialApproval(models.Model):
    sc_potential_approval_guid = models.CharField(db_column='sc_potential_approval_guid', primary_key=True,
                                                  max_length=32)
    app_id = models.CharField(db_column='APP_ID', max_length=70, blank=True, null=True, verbose_name='Approver ID')
    step_num = models.CharField(db_column='STEP_NUM', max_length=3, blank=True, null=True, verbose_name='Sequence')
    app_sts = models.CharField(db_column='APP_STS', max_length=20, blank=True, null=True, verbose_name='Status')
    proc_lvl_sts = models.CharField(db_column='PROC_LVL_STS', max_length=10, blank=True, null=True,
                                    verbose_name='Level Status')
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    sc_approval_guid = models.ForeignKey('eProc_Shopping_Cart.ScApproval', models.DO_NOTHING,
                                         db_column='SC_APPROVAL_GUID', blank=True,
                                         null=True)
    sc_header_guid = models.ForeignKey('eProc_Shopping_Cart.ScHeader', models.DO_NOTHING, db_column='SC_HEADER_GUID',
                                       null=True)

    class Meta:
        managed = True
        db_table = 'MTD_SC_POTENTIAL_APPROVAL'


class ScAddresses(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
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
    fax_number = models.CharField(db_column='FAX_NUMBER', max_length=30, null=True, blank=True, verbose_name='Fax')
    email = models.EmailField(db_column='EMAIL', max_length=100, null=True)
    time_zone = models.CharField(db_column='TIME_ZONE', max_length=6, null=True)
    sc_addr_created_at = models.DateTimeField(db_column='SC_ADDR_CREATED_AT', blank=False, null=True)
    sc_addr_created_by = models.CharField(db_column='SC_ADDR_CREATED_BY', max_length=12, blank=False, null=True)
    sc_addr_changed_at = models.DateTimeField(db_column='SC_ADDR_CHANGED_AT', blank=True, null=True)
    sc_addr_changed_by = models.CharField(db_column='SC_ADDR_CHANGED_BY', max_length=12, blank=False, null=True)
    sc_addresses_source_system = models.CharField(db_column='SC_ADDRESSES_SOURCE_SYSTEM', max_length=20)
    sc_addresses_destination_system = models.CharField(db_column='SC_ADDRESSES_DESTINATION_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=True)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=True)
    header_guid = models.ForeignKey('ScHeader', models.DO_NOTHING, db_column='HEADER_GUID', blank=True, null=True)
    item_guid = models.ForeignKey('ScItem', models.DO_NOTHING, db_column='ITEM_GUID', blank=True, null=True)

    class Meta:
        db_table = "MTD_SC_ADDRESSES"
        managed = True

    def __str__(self):
        return self.guid

    # Get accounting data by item guid
    def get_addr_by_guid(self, itm_guid):
        return ScAddresses.objects.filter(item_guid__in=itm_guid,
                                          client=global_variables.GLOBAL_CLIENT,
                                          address_type='D',
                                          del_ind=False).order_by('item_num')


class PurchasingData(models.Model):
    purch_guid = models.CharField(db_column='PURCH_GUID', primary_key=True, max_length=32)
    item_num = models.PositiveIntegerField(db_column='ITEM_NUM', blank=False, null=False, verbose_name='Item Number',
                                           default=0)
    prod_cat = models.CharField(db_column='PROD_CAT', max_length=20, blank=False, null=False,
                                verbose_name='Product Category')
    comp_code = models.CharField(db_column='COMP_CODE', max_length=10, blank=False, null=False,
                                 verbose_name='Company Code')
    purch_grp = models.CharField(db_column='PURCH_GRP', max_length=20, blank=True, null=True,
                                 verbose_name='Purchasing Group')
    purch_org = models.CharField(db_column='PURCH_ORG', max_length=20, blank=True, null=True,
                                 verbose_name='Purchasing Organization')
    # purchaser_user filled on submit of purchaser user
    purchaser_user = models.CharField(db_column='PURCHASER_USER', null=True, max_length=16)
    purchasing_data_created_at = models.DateTimeField(db_column='PURCHASING_DATA_CREATED_AT', blank=False, null=True)
    purchasing_data_created_by = models.CharField(db_column='PURCHASING_DATA_CREATED_BY', max_length=12, blank=False,
                                                  null=True)
    purchasing_data_changed_at = models.DateTimeField(db_column='PURCHASING_DATA_CHANGED_AT', blank=True, null=True)
    purchasing_data_changed_by = models.CharField(db_column='PURCHASING_DATA_CHANGED_BY', max_length=12, blank=False,
                                                  null=True)
    purchasing_data_source_system = models.CharField(db_column='PURCHASING_DATA_SOURCE_SYSTEM', max_length=20)
    purchasing_data_destination_system = models.CharField(db_column='PURCHASING_DATA_DESTINATION_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=True)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT)
    po_header_guid = models.ForeignKey('eProc_Purchase_Order.PoHeader', models.DO_NOTHING, db_column='PO_HEADER_GUID',
                                       blank=True, null=True)
    po_item_guid = models.ForeignKey('eProc_Purchase_Order.PoItem', models.DO_NOTHING, db_column='PO_ITEM_GUID',
                                     blank=True,
                                     null=True)
    sc_header_guid = models.ForeignKey('eProc_Shopping_Cart.ScHeader', models.DO_NOTHING, db_column='SC_HEADER_GUID',
                                       null=True)
    sc_item_guid = models.ForeignKey('eProc_Shopping_Cart.ScItem', models.DO_NOTHING, db_column='SC_ITEM_GUID')

    class Meta:
        db_table = 'MTD_PURCHASING_DATA'


class PurchasingUser(models.Model):
    purchasing_user_guid = models.CharField(db_column='PURCHASING_USER_GUID', primary_key=True, max_length=32)
    purchaser_user_id = models.CharField(db_column='PURCHASER_USER_ID', null=True, max_length=16)
    status = models.CharField(db_column='STATUS', max_length=20, blank=False, null=False, verbose_name='Status')
    document_type = models.CharField(max_length=10, db_column='DOC_TYPE', null=True, blank=True)
    purchasing_user_created_at = models.DateTimeField(db_column='PURCHASING_USER_CREATED_AT', blank=False, null=True,
                                                      verbose_name='Created At')

    purchasing_user_created_by = models.CharField(db_column='PURCHASING_USER_CREATED_BY', max_length=12, blank=False,
                                                  null=True,
                                                  verbose_name='Creator')
    purchasing_user_changed_at = models.DateTimeField(db_column='PURCHASING_USER_CHANGED_AT', blank=True, null=True,
                                                      verbose_name='Changed At')
    purchasing_user_changed_by = models.CharField(db_column='PURCHASING_USER_CHANGED_BY', max_length=12, blank=False,
                                                  null=True,
                                                  verbose_name='Changed By')
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    po_header_guid = models.ForeignKey('eProc_Purchase_Order.PoHeader', models.DO_NOTHING, db_column='PO_HEADER_GUID',
                                       blank=True, null=True)
    po_item_guid = models.ForeignKey('eProc_Purchase_Order.PoItem', models.DO_NOTHING, db_column='PO_ITEM_GUID',
                                     blank=True,
                                     null=True)
    sc_header_guid = models.ForeignKey('eProc_Shopping_Cart.ScHeader', models.DO_NOTHING, db_column='SC_HEADER_GUID',
                                       null=True)
    sc_item_guid = models.ForeignKey('eProc_Shopping_Cart.ScItem', models.DO_NOTHING, db_column='SC_ITEM_GUID',
                                     null=True)

    class Meta:
        managed = True
        db_table = 'MTD_PURCHASING_USER'
