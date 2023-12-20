from django.db import models


# Define favourite carts
class FavouriteCart(models.Model):
    favourite_cart_guid = models.CharField(db_column='FAVOURITE_CART_GUID', primary_key=True, max_length=32, null=False,
                                           default=None)
    favourite_cart_number = models.PositiveIntegerField(db_column='FAVOURITE_CART_NUMBER', null=False,
                                                        verbose_name='Favourite Cart Number')
    favourite_cart_name = models.CharField(db_column='FAVOURITE_CART_NAME', max_length=255, blank=True, null=True,
                                           verbose_name='Favourite cart Name')
    item_num = models.PositiveIntegerField(db_column='ITEM_NUM', blank=False, null=True, verbose_name='Item Number')
    description = models.CharField(db_column='DESCRIPTION', max_length=250, null=True)
    long_desc = models.CharField(db_column='LONG_DESC', max_length=3000, blank=True, null=True,
                                 verbose_name='Product Long desc')
    prod_cat_desc = models.CharField(db_column='PROD_CAT_DESC', max_length=255, blank=False, null=True,
                                     verbose_name='Product Category Description')
    prod_cat_id = models.CharField(db_column='PROD_CAT_ID', max_length=20, null=True)
    cust_prod_cat_id = models.CharField(db_column='CUST_PROD_CAT_ID', null=True, max_length=20)
    int_product_id = models.CharField(db_column='INT_PRODUCT_ID', max_length=20, null=True)
    quantity = models.CharField(db_column='QUANTITY', max_length=20, null=True)
    unit = models.CharField(db_column='UNIT', max_length=30, null=True)
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
    price = models.DecimalField(db_column='PRICE', max_digits=15, decimal_places=2, null=True)
    tax_value = models.DecimalField(db_column='TAX_VALUE', max_digits=15, decimal_places=2, blank=True, null=True,
                                    verbose_name='tax Value')  # (SGST *quantity)+(CGST *quantity)
    gross_price = models.DecimalField(db_column='GROSS_PRICE', max_digits=13, decimal_places=2, null=True)
    price_unit = models.CharField(db_column='PRICE_UNIT', max_length=5, null=True)
    currency = models.CharField(db_column='CURRENCY', max_length=3, null=True)
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=10, null=True)
    pref_supplier = models.CharField(db_column='PREF_SUPPLIER', max_length=10, null=True)
    lead_time = models.PositiveIntegerField(db_column='LEAD_TIME', null=True)
    value = models.CharField(db_column='VALUE', max_length=20, null=True)
    fc_total_value = models.CharField(db_column='FC_TOTAL_VALUE', max_length=15, blank=False, null=True,
                                      verbose_name='Total Value')
    fc_total_currency = models.CharField(db_column='FC_TOTAL_CURRENCY', max_length=3, blank=False, null=True,
                                         verbose_name='Currency')
    manufacturer = models.CharField(db_column='MANUFACTURER', max_length=15, null=True)
    manu_part_num = models.CharField(db_column='MANU_PART_NUM', max_length=40, null=True)
    manu_code_num = models.CharField(db_column='MANU_CODE_NUM', max_length=10, null=True)
    supp_product_id = models.CharField(db_column='SUPP_PRODUCT_ID', max_length=40, null=True)
    call_off = models.CharField(db_column='CALL_OFF', max_length=15, null=True)
    supplier_username = models.CharField(db_column='SUPPLIER_USERNAME', null=True, max_length=16)
    supplier_mobile_num = models.CharField(db_column='SUPPLIER_MOBILE_NUM', max_length=30, null=True)
    supplier_fax_no = models.CharField(max_length=30, db_column='SUPPLIER_FAX_NO', blank=True, null=True)
    supplier_email = models.CharField(max_length=100, db_column='SUPPLIER_EMAIL', blank=True, null=True)
    quantity_min = models.PositiveIntegerField(db_column='QUANTITY_MIN', null=True)
    quantity_max = models.PositiveIntegerField(db_column='QUANTITY_MAX', null=True, verbose_name='Quantity Max')
    value_min = models.PositiveIntegerField(db_column='VALUE_MIN', null=True)
    tiered_flag = models.BooleanField(db_column='TIERED_FLAG', null=True)
    bundle_flag = models.BooleanField(db_column='BUNDLE_FLAG', null=True)
    tax_code = models.CharField(db_column='TAX_CODE', max_length=5, null=True, verbose_name='Tax Code')
    sgst = models.DecimalField(db_column='SGST', max_digits=15, decimal_places=2, blank=True, null=True,
                               verbose_name='State GST')
    cgst = models.DecimalField(db_column='CGST', max_digits=15, decimal_places=2, blank=True, null=True,
                               verbose_name='Central GST')
    vat = models.DecimalField(db_column='VAT', max_digits=15, decimal_places=2, blank=True, null=True,
                              verbose_name='Value Added Tax - VAT code (%age as decimal) returned from catalogue ')
    delivery_days = models.DateField(db_column='DELIVERY_DAYS', null=True)
    catalog_id = models.CharField(db_column='CATALOG_ID', max_length=20, null=True)
    catalog_item = models.CharField(db_column='CATALOG_ITEM', max_length=32, null=True)
    ctr_num = models.CharField(db_column='CTR_NUM', max_length=50, null=True)
    ctr_name = models.CharField(db_column='CTR_NAME', blank=True, null=True, max_length=50,
                                verbose_name='Contract Name')
    ctr_item_num = models.CharField(db_column='CTR_ITEM_NUM', max_length=50, blank=True, null=True,
                                    verbose_name='ctr num')
    prod_type = models.CharField(db_column='PROD_TYPE', max_length=2, null=True)
    item_del_date = models.DateField(db_column='ITEM_DEL_DATE', blank=False, null=True)
    process_type = models.CharField(db_column='PROCESS_TYPE', max_length=8, null=True)
    start_date = models.DateField(db_column='START_DATE', null=True)
    end_date = models.DateField(db_column='END_DATE', null=True)
    ir_gr_ind_limi = models.BooleanField(db_column='IR_GR_IND_LIMI', null=True)
    gr_ind_limi = models.BooleanField(db_column='GR_IND_LIMI', null=True, verbose_name='Gr ind')
    overall_limit = models.DecimalField(db_column='OVERALL_LIMIT', max_digits=15, decimal_places=2, null=True)
    expected_value = models.DecimalField(db_column='EXPECTED_VALUE', max_digits=15, decimal_places=2, null=True)
    gr_ind = models.BooleanField(db_column='GR_IND', null=True, verbose_name='Gr ind')
    ir_gr_ind = models.BooleanField(db_column='IR_GR_IND', null=True, verbose_name='Ir Gr ind')
    ir_ind = models.BooleanField(db_column='IR_IND', null=True, verbose_name='ir ind')
    po_resp = models.BooleanField(db_column='PO_RESP', null=True, verbose_name='PO Response')
    asn_ind = models.BooleanField(db_column='ASN_IND', null=True, verbose_name='Advance shipment Notice')
    username = models.CharField(db_column='USERNAME', max_length=16, null=False)
    eform_id = models.CharField(db_column='EFORM_ID', max_length=40, blank=False, null=True)
    discount_id = models.CharField(db_column='DISCOUNT_ID', max_length=40, blank=False, null=True)
    variant_id = models.CharField(db_column='VARIANT_ID', max_length=40, blank=False, null=True)
    product_info_id = models.CharField(db_column='PRODUCT_INFO_ID', max_length=40, blank=True, null=True)
    favourite_cart_created_at = models.DateTimeField(db_column='FAVOURITE_CART_CREATED_AT', blank=True, null=True)
    favourite_cart_created_by = models.CharField(db_column='FAVOURITE_CART_CREATED_BY', max_length=30, null=True)
    favourite_cart_changed_at = models.DateTimeField(db_column='FAVOURITE_CART_CHANGED_AT', blank=True, null=True)
    favourite_cart_changed_by = models.CharField(db_column='FAVOURITE_CART_CHANGED_BY', max_length=30, null=True)
    favourite_cart_source_system = models.CharField(db_column='FAVOURITE_CART_SOURCE_SYSTEM', max_length=20)
    favourite_cart_destination_system = models.CharField(db_column='FAVOURITE_CART_DESTINATION_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        managed = True
        db_table = 'MTD_FAVOURITE_CART'


# Define recently viewed products
class RecentlyViewedProducts(models.Model):
    recently_viewed_prod_guid = models.CharField(db_column='RECENTLY_VIEWED_PROD_GUID', primary_key=True, max_length=32,
                                                 null=False, default=None)
    username = models.CharField(db_column='USERNAME', null=False, unique=False, max_length=16)
    product_id = models.CharField(db_column="PRODUCT_ID", max_length=16, null=True)
    catalog_id = models.CharField(db_column='CATALOG_ID', null=False, default=None, max_length=16)
    recently_viewed_prod_created_at = models.DateTimeField(db_column='RECENTLY_VIEWED_PROD_CREATED_AT', blank=True,
                                                           null=True)
    recently_viewed_prod_created_by = models.CharField(db_column='RECENTLY_VIEWED_PROD_CREATED_BY', max_length=30,
                                                       null=True)
    recently_viewed_prod_changed_at = models.DateTimeField(db_column='RECENTLY_VIEWED_PROD_CHANGED_AT', blank=True,
                                                           null=True)
    recently_viewed_prod_changed_by = models.CharField(db_column='RECENTLY_VIEWED_PROD_CHANGED_BY', max_length=30,
                                                       null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        managed = True
        db_table = 'MTD_RECENTLY_VIEWED_PRODUCTS'
