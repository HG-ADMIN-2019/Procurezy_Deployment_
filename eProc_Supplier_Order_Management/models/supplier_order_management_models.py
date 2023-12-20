from django.db import models

from eProc_Basic.Utilities.global_defination import global_variables


class SOMPoHeader(models.Model):
    som_po_header_guid = models.CharField(db_column='SOM_PO_HEADER_GUID', primary_key=True, max_length=32)
    doc_number = models.CharField(db_column='DOC_NUMBER', max_length=10, blank=False, null=False,
                                  verbose_name='PO Number')
    posting_date = models.DateTimeField(db_column='POSTING_DATE', blank=True, null=True)
    total_value = models.CharField(db_column='TOTAL_VALUE', max_length=15, blank=False, null=False,
                                   verbose_name='Total Value')  # sum(currency converted item value)
    currency = models.CharField(db_column='CURRENCY', max_length=3, blank=False, null=False, verbose_name='Currency')
    payment_term = models.CharField(max_length=255, db_column='PAYMENT_TERM', blank=True, null=True)
    incoterm = models.CharField(max_length=255, db_column='INCOTERM', blank=True, null=True)
    requester = models.CharField(db_column='REQUESTER', max_length=50, blank=False, null=False,
                                 verbose_name='Requester')
    requester_company_name = models.CharField(max_length=80, db_column='REQUESTER_COMPANY_NAME', blank=True, null=True)
    requester_email = models.CharField(max_length=100, db_column='REQUESTER_EMAIL', blank=True, null=True)
    requester_mobile_num = models.CharField(max_length=40, db_column='REQUESTER_MOBILE_NUM', blank=True, null=True)
    requester_fax_no = models.CharField(max_length=40, db_column='REQUESTER_FAX_NO', blank=True, null=True)
    status = models.CharField(db_column='STATUS', max_length=20, blank=False, null=True, verbose_name='Status')
    # ORDERED,READY_TO_SHIP,
    goods_recep = models.CharField(db_column='GOODS_RECEP', max_length=50, blank=True, null=True,
                                   verbose_name='Goods Recipient')
    supplier_note_text = models.CharField(db_column='SUPPLIER_NOTE_TEXT', null=True, max_length=1000)
    som_po_header_created_at = models.DateTimeField(db_column='SOM_PO_HEADER_CREATED_AT', blank=False, null=False,
                                                    verbose_name='Created At')
    som_po_header_created_by = models.CharField(db_column='SOM_PO_HEADER_CREATED_BY', max_length=12, blank=False,
                                                null=False,
                                                verbose_name='Creator')
    som_po_header_changed_at = models.DateTimeField(db_column='SOM_PO_HEADER_CHANGED_AT', blank=True, null=False,
                                                    verbose_name='Changed At')
    som_po_header_changed_by = models.CharField(db_column='SOM_PO_HEADER_CHANGED_BY', max_length=12, blank=False,
                                                null=False,
                                                verbose_name='Changed By')
    ordered_at = models.DateTimeField(db_column='ORDERED_AT', blank=True, null=True, verbose_name='Ordered At')
    time_zone = models.CharField(db_column='TIME_ZONE', max_length=6, blank=True, null=False, verbose_name='Time Zone')
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=12, blank=True, null=True,
                                   verbose_name='Supplier ID')
    supplier_username = models.CharField(max_length=40, db_column='SUPPLIER_USERNAME', blank=True, null=True)
    supplier_contact = models.CharField(db_column='SUPPLIER_CONTACT', max_length=100, blank=False, null=True,
                                        verbose_name='supplier contact name')
    supplier_mobile_num = models.CharField(max_length=40, db_column='SUPPLIER_MOBILE_NUM', blank=True, null=True)
    supplier_fax_no = models.CharField(max_length=30, db_column='SUPPLIER_FAX_NO', blank=True, null=True)
    supplier_email = models.CharField(max_length=100, db_column='SUPPLIER_EMAIL', blank=True, null=True)
    pdf_invoice_address = models.CharField(max_length=100, db_column='PDF_INVOICE_ADDRESS', blank=True, null=True)
    invoicing_detail = models.CharField(max_length=100, db_column='INVOICING_DETAIL', blank=True, null=True)
    som_po_header_source_system = models.CharField(db_column='SOM_PO_HEADER_SOURCE_SYSTEM', max_length=20)
    som_po_header_destination_system = models.CharField(db_column='SOM_PO_HEADER_DESTINATION_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        managed = True
        db_table = 'MTD_SOM_PO_HEADER'


def get_som_po_details_by_fields(doc_number):
    return list(SOMPoHeader.objects.filter(doc_number,
                                           client=global_variables.GLOBAL_CLIENT,
                                           del_ind=False).values().order_by('ordered_at'))


class SOMPoItem(models.Model):
    som_po_item_guid = models.CharField(db_column='SOM_PO_ITEM_GUID', primary_key=True, max_length=32)
    som_po_item_num = models.CharField(db_column='SOM_PO_ITEM_NUM', max_length=10, blank=True, null=True,
                                       verbose_name='Line Number')
    int_product_id = models.CharField(db_column='INT_PRODUCT_ID', max_length=100, null=True)
    supplier_product_id = models.CharField(db_column='SUPPLIER_PRODUCT_ID', max_length=100, null=True, blank=True)
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)
    item_del_date = models.DateTimeField(db_column='ITEM_DEL_DATE', blank=False, null=True,
                                         verbose_name='Delivery Date')
    quantity = models.PositiveIntegerField(db_column='QUANTITY', null=False, verbose_name='Quantity')
    price = models.DecimalField(db_column='PRICE', max_digits=15, decimal_places=2, blank=True, null=True,
                                verbose_name='Price')
    value = models.DecimalField(db_column='VALUE', max_digits=15, decimal_places=2, blank=True, null=True,
                                verbose_name='Value')  # (float(quantity) * float(gross price)) / int(price_unit)
    tax_value = models.DecimalField(db_column='TAX_VALUE', max_digits=15, decimal_places=2, blank=True, null=True,
                                    verbose_name='tax Value')  # (SGST *quantity)+(CGST *quantity)
    price_unit = models.CharField(db_column='PRICE_UNIT', max_length=5, blank=True, null=True,
                                  verbose_name='Price Unit')
    unit = models.CharField(db_column='UNIT', max_length=3, blank=False, null=False, verbose_name='Unit')
    currency = models.CharField(db_column='CURRENCY', max_length=3, blank=False, null=False, verbose_name='Currency')
    eform_id = models.CharField(db_column='EFORM_ID', max_length=40, blank=False, null=True)
    goods_recep = models.CharField(db_column='GOODS_RECEP', max_length=12, blank=True, null=True,
                                   verbose_name='Goods Recipient')
    som_po_item_created_at = models.DateTimeField(db_column='SOM_PO_ITEM_CREATED_AT', blank=False, null=False,
                                                  verbose_name='Created At')
    som_po_item_created_by = models.CharField(db_column='SOM_PO_ITEM_CREATED_BY', max_length=12, blank=False,
                                              null=False,
                                              verbose_name='Creator')
    som_po_item_changed_at = models.DateTimeField(db_column='SOM_PO_ITEM_CHANGED_AT', blank=True, null=False,
                                                  verbose_name='Changed At')
    som_po_item_changed_by = models.CharField(db_column='SOM_PO_ITEM_CHANGED_BY', max_length=12, blank=False,
                                              null=False,
                                              verbose_name='Changed By')
    som_po_item_source_system = models.CharField(db_column='SOM_PO_ITEM_SOURCE_SYSTEM', max_length=20)
    som_po_item_destination_system = models.CharField(db_column='SOM_PO_ITEM_DESTINATION_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    som_po_header_guid = models.ForeignKey('eProc_Supplier_Order_Management.SOMPoHeader', models.DO_NOTHING,
                                           db_column='SOM_PO_HEADER_GUID',
                                           blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'MTD_SOM_PO_ITEM'


class SOMEformFieldData(models.Model):
    som_eform_field_data_guid = models.CharField(db_column='SOM_EFORM_FIELD_DATA_GUID', primary_key=True, max_length=40,
                                                 blank=False, null=False)
    eform_id = models.CharField(db_column='EFORM_ID', max_length=40, blank=False, null=True)
    eform_type = models.CharField(db_column='EFORM_TYPE', max_length=40, blank=False, null=True)
    eform_description = models.CharField(db_column='EFORM_DESCRIPTION', max_length=400, blank=True, null=True)
    eform_field_name = models.CharField(db_column='EFORM_FIELD_NAME', null=True, max_length=200)
    eform_field_data = models.CharField(db_column='EFORM_FIELD_DATA', null=True, max_length=1000)
    eform_field_count = models.PositiveIntegerField(db_column='EFORM_FIELD_COUNT', blank=False, null=True)
    eform_field_data_created_at = models.DateTimeField(db_column='EFORM_FIELD_DATA_CREATED_AT', blank=False, null=True)
    som_eform_field_data_created_by = models.CharField(db_column='SOM_EFORM_FIELD_DATA_CREATED_BY', max_length=12,
                                                       blank=False,
                                                       null=True)
    som_eform_field_data_changed_at = models.DateTimeField(db_column='SOM_EFORM_FIELD_DATA_CHANGED_AT', blank=True,
                                                           null=True)
    som_eform_field_data_changed_by = models.CharField(db_column='SOM_EFORM_FIELD_DATA_CHANGED_BY', max_length=12,
                                                       blank=False,
                                                       null=True)
    som_eform_field_data_source_system = models.CharField(db_column='SOM_EFORM_FIELD_DATA_SOURCE_SYSTEM', max_length=20)
    som_eform_field_data_destination_system = models.CharField(db_column='SOM_EFORM_FIELD_DATA_DESTINATION_SYSTEM',
                                                               max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    som_po_item_guid = models.ForeignKey('eProc_Supplier_Order_Management.SOMPoItem', models.DO_NOTHING,
                                         db_column='SOM_PO_ITEM_GUID',
                                         blank=True, null=True)

    class Meta:
        db_table = "MTD_SOM_EFORM_FIELD_DATA"
        managed = True


class SOMPoAccounting(models.Model):
    som_po_accounting_guid = models.CharField(db_column='SOM_PO_ACCOUNTING_GUID', primary_key=True, max_length=32)
    acc_item_num = models.DecimalField(db_column='ACC_ITEM_NUM', max_digits=4, decimal_places=0, blank=False,
                                       null=True, verbose_name='Number')
    acc_cat = models.CharField(db_column='ACC_CAT', max_length=5, blank=False, null=True,
                               verbose_name='Account Assignment Category')
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
    asset_number = models.CharField(db_column='ASSET_NUMBER', max_length=24, null=True)

    som_po_accounting_created_at = models.DateTimeField(db_column='SOM_PO_ACCOUNTING_CREATED_AT', blank=False,
                                                        null=True)
    som_po_accounting_created_by = models.CharField(db_column='SOM_PO_ACCOUNTING_CREATED_BY', max_length=12,
                                                    blank=False,
                                                    null=True)
    som_po_accounting_changed_at = models.DateTimeField(db_column='SOM_PO_ACCOUNTING_CHANGED_AT', blank=True, null=True)
    som_po_accounting_changed_by = models.CharField(db_column='SOM_PO_ACCOUNTING_CHANGED_BY', max_length=12,
                                                    blank=False,
                                                    null=True)
    som_po_accounting_source_system = models.CharField(db_column='SOM_PO_ACCOUNTING_SOURCE_SYSTEM', max_length=20)
    som_po_accounting_destination_system = models.CharField(db_column='SOM_PO_ACCOUNTING_DESTINATION_SYSTEM',
                                                            max_length=20,
                                                            null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    som_po_item_guid = models.ForeignKey('eProc_Supplier_Order_Management.SOMPoItem', models.DO_NOTHING,
                                         db_column='SOM_PO_ITEM_GUID',
                                         blank=True,
                                         null=True)

    class Meta:
        managed = True
        db_table = 'MTD_SOM_PO_ACCOUNTING'


class SOMPoAddresses(models.Model):
    som_po_addresses_guid = models.CharField(db_column='SOM_PO_ADDRESSES_GUID', primary_key=True, max_length=32)
    item_num = models.PositiveIntegerField(db_column='ITEM_NUM', blank=False, null=False, verbose_name='Item Number',
                                           default=0)
    address_number = models.PositiveIntegerField(db_column='ADDRESS_NUMBER', null=True)
    address_type = models.CharField(db_column='ADDRESS_TYPE', max_length=1, null=True, blank=True)
    address_partner_type = models.ForeignKey('eProc_Configuration.AddressPartnerType', models.DO_NOTHING,
                                             db_column='ADDRESS_PARTNER_TYPE', null=True)
    address_details = models.CharField(db_column='ADDRESS_DETAILS', max_length=400, null=True)
    mobile_number = models.CharField(db_column='MOBILE_NUMBER', max_length=20, verbose_name='Mobile', null=True,
                                     blank=True)
    telephone_number = models.CharField(db_column='TELEPHONE_NUMBER', max_length=20, verbose_name='Telephone',
                                        null=True, blank=True)
    fax_number = models.CharField(db_column='FAX_NUMBER', max_length=30, null=True, blank=False, verbose_name='Fax')
    email = models.EmailField(db_column='EMAIL', max_length=100, null=True)
    time_zone = models.CharField(db_column='TIME_ZONE', max_length=6, null=True)
    som_po_addr_created_at = models.DateTimeField(db_column='SOM_PO_ADDR_CREATED_AT', blank=False, null=True)
    som_po_addr_created_by = models.CharField(db_column='SOM_PO_ADDR_CREATED_BY', max_length=12, blank=False, null=True)
    som_po_addr_changed_at = models.DateTimeField(db_column='SOM_PO_ADDR_CHANGED_AT', blank=True, null=True)
    som_po_addr_changed_by = models.CharField(db_column='SOM_PO_ADDR_CHANGED_BY', max_length=12, blank=False, null=True)
    som_po_addresses_source_system = models.CharField(db_column='SOM_PO_ADDRESSES_SOURCE_SYSTEM', max_length=20)
    som_po_addresses_destination_system = models.CharField(db_column='SOM_PO_ADDRESSES_DESTINATION_SYSTEM',
                                                           max_length=20)
    del_ind = models.BooleanField(default=False, null=True)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=True)
    som_po_header_guid = models.ForeignKey('eProc_Supplier_Order_Management.SOMPoHeader', models.DO_NOTHING,
                                           db_column='SOM_PO_HEADER_GUID',
                                           null=True)

    class Meta:
        db_table = "MTD_SOM_PO_ADDRESSES"
        managed = True


class SOMSupplierMaster(models.Model):
    som_supp_guid = models.CharField(primary_key=True, db_column='SOM_SUPP_GUID', max_length=32)
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
    email = models.EmailField(db_column='EMAIL', max_length=100, null=True)
    email1 = models.EmailField(db_column='EMAIL1', max_length=100, null=True)
    email2 = models.EmailField(db_column='EMAIL2', max_length=100, null=True)
    email3 = models.EmailField(db_column='EMAIL3', max_length=100, null=True)
    email4 = models.EmailField(db_column='EMAIL4', max_length=100, null=True)
    email5 = models.EmailField(db_column='EMAIL5', max_length=100, null=True)
    delivery_days = models.CharField(db_column='DELIVERY_DAYS', max_length=20, null=True, blank=True)
    som_supplier_master_created_by = models.CharField(db_column='SOM_SUPPLIER_MASTER_CREATED_BY', max_length=30,
                                                      null=True)
    som_supplier_master_created_at = models.DateTimeField(db_column='SOM_SUPPLIER_MASTER_CREATED_AT', max_length=50,
                                                          null=True)
    som_supplier_master_changed_by = models.CharField(db_column='SOM_SUPPLIER_MASTER_CHANGED_BY', max_length=30,
                                                      null=True)
    som_supplier_master_changed_at = models.DateTimeField(db_column='SOM_SUPPLIER_MASTER_CHANGED_AT', max_length=50,
                                                          null=True)
    som_supplier_master_source_system = models.CharField(db_column='SOM_SUPPLIER_MASTER_SOURCE_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    country_code = models.ForeignKey('eProc_Configuration.Country', db_column='COUNTRY_CODE', on_delete=models.PROTECT,
                                     verbose_name='Country', null=True)

    class Meta:
        managed = True
        db_table = 'MMD_SOM_SUPPLIERS'
