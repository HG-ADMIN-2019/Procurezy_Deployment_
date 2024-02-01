import operator
import re
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models


class arch_ScHeader(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    doc_number = models.CharField(db_column='DOC_NUMBER', max_length=10, blank=False, null=False,
                                  verbose_name='SC Number')
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True,
                                   verbose_name='SC Name')
    total_value = models.CharField(db_column='TOTAL_VALUE', max_length=15, blank=False, null=False,
                                   verbose_name='Total Value')
    currency = models.CharField(db_column='CURRENCY', max_length=3, blank=False, null=False, verbose_name='Currency')
    requester = models.CharField(db_column='REQUESTER', max_length=12, blank=False, null=False,
                                 verbose_name='Requester')
    status = models.CharField(db_column='STATUS', max_length=20, blank=False, null=False, verbose_name='Status')
    created_at = models.DateTimeField(db_column='CREATED_AT', blank=False, null=False, verbose_name='Created At')
    created_by = models.CharField(db_column='CREATED_BY', max_length=12, blank=False, null=False,
                                  verbose_name='Creator')
    changed_at = models.DateTimeField(db_column='CHANGED_AT', blank=True, null=True, verbose_name='Changed At')
    changed_by = models.CharField(db_column='CHANGED_BY', max_length=12, blank=False, null=False,
                                  verbose_name='Changed By')
    ordered_at = models.DateTimeField(db_column='ORDERED_AT', blank=True, null=True, verbose_name='Ordered At')
    time_zone = models.CharField(db_column='TIME_ZONE', max_length=6, blank=True, null=True, verbose_name='Time Zone')
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False,
                               db_column='CLIENT')
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        managed = True
        unique_together = ('client', 'doc_number')
        db_table = 'MSS_SC_HEADER'

    # Get header data by guid
    def get_hdr_data_by_guid(self, guid):
        return arch_ScHeader.objects.filter(guid=guid)

    # Get header guid by object id
    @staticmethod
    def get_hdr_guid_by_objid(objid):
        try:
            hdr = arch_ScHeader.objects.get(doc_number=objid)
            return getattr(hdr, 'guid')
        except ObjectDoesNotExist:
            return 'error'


# Definition of SC Item table structure
class arch_ScItem(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    header_guid = models.ForeignKey(arch_ScHeader, models.DO_NOTHING, db_column='HEADER_GUID', blank=True, null=True)
    item_num = models.PositiveIntegerField(db_column='ITEM_NUM', blank=False, null=False, verbose_name='Line Number')
    po_num = models.CharField(db_column='PO_NUM', max_length=10, blank=True, null=True, verbose_name='PO Number')
    po_item_num = models.CharField(db_column='PO_ITEM_NUM', max_length=10, blank=True, null=True,
                                   verbose_name='Item Number')
    prod_description = models.CharField(db_column='PROD_DESCRIPTION', max_length=255, blank=False, null=False,
                                        verbose_name='Description')
    comp_code = models.CharField(db_column='COMP_CODE', max_length=10, blank=False, null=False,
                                 verbose_name='Company Code')
    purch_grp = models.CharField(db_column='PURCH_GRP', max_length=20, blank=True, null=True,
                                 verbose_name='Purchasing Group')
    purch_org = models.CharField(db_column='PURCH_ORG', max_length=20, blank=True, null=True,
                                 verbose_name='Purchasing Organization')
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=12, blank=True, null=True,
                                   verbose_name='Supplier ID')
    item_cat = models.CharField(db_column='ITEM_CAT', max_length=20, blank=True, null=True,
                                verbose_name='Item Category')
    prod_cat = models.CharField(db_column='PROD_CAT', max_length=20, blank=False, null=False,
                                verbose_name='Product Category')
    hiring_level = models.CharField(db_column='HIRING_LEVEL', max_length=255, blank=True, null=True,
                                    verbose_name='Hiring level')
    hiring_role = models.CharField(db_column='HIRING_ROLE', max_length=255, blank=True, null=True,
                                   verbose_name='Hiring role')
    hiring_skill = models.CharField(db_column='HIRING_SKILL', max_length=255, blank=True, null=True,
                                    verbose_name='Hiring skill')
    prod_type = models.CharField(db_column='PROD_TYPE', max_length=10, blank=False, null=False,
                                 verbose_name='Product Type')
    catalog_id = models.CharField(db_column='CATALOG_ID', max_length=20, blank=True, null=True,
                                  verbose_name='Catalog ID')
    unspsc = models.CharField(db_column='UNSPSC', max_length=10, blank=True, null=True, verbose_name='UNSPSC')
    fin_entry_ind = models.CharField(db_column='FIN_ENTRY_IND', max_length=1, blank=True, null=True,
                                     verbose_name='fin_entry_ind')
    item_del_date = models.DateField(db_column='ITEM_DEL_DATE', blank=False, null=True, verbose_name='Delivery Date')
    quantity = models.CharField(db_column='QUANTITY', max_length=16, blank=True, null=True, verbose_name='Quantity')
    price = models.CharField(db_column='PRICE', max_length=15, blank=False, null=False, verbose_name='Price')
    price_unit = models.CharField(db_column='PRICE_UNIT', max_length=5, blank=True, null=True,
                                  verbose_name='Price Unit')
    unit = models.CharField(db_column='UNIT', max_length=3, blank=False, null=False, verbose_name='Unit')
    gross_price = models.CharField(db_column='GROSS_PRICE', max_length=15, blank=False, null=False,
                                   verbose_name='Gross Price')
    overall_limit = models.CharField(db_column='OVERALL_LIMIT', max_length=15, blank=False, null=False,
                                     verbose_name='overall limit')
    expected_value = models.CharField(db_column='EXPECTED_VALUE', max_length=15, blank=False, null=False,
                                      verbose_name='expected value')
    undef_limit = models.CharField(db_column='UNDEF_LIMIT', max_length=1, blank=True, null=True,
                                   verbose_name='undef limit')
    gr_ind = models.CharField(db_column='GR_IND', max_length=1, blank=True, null=True, verbose_name='Gr ind')
    dis_rej_ind = models.CharField(db_column='DIS_REJ_IND', max_length=1, blank=True, null=True,
                                   verbose_name='dis rej ind')
    supp_prod_num = models.CharField(db_column='SUPP_PROD_NUM', max_length=40, blank=True, null=True,
                                     verbose_name='Supplier Product Number')
    manu_part_num = models.CharField(db_column='MANU_PART_NUM', max_length=40, blank=True, null=True,
                                     verbose_name='manu part num')
    manu_code_num = models.CharField(db_column='MANU_CODE_NUM', max_length=10, blank=True, null=True,
                                     verbose_name='manu code num')
    status = models.CharField(db_column='STATUS', max_length=20, blank=True, null=True, verbose_name='Status')
    ctr_num = models.CharField(db_column='CTR_NUM', max_length=50, blank=True, null=True, verbose_name='ctr num')
    supp_ord_addr = models.CharField(db_column='SUPP_ORD_ADDR', max_length=10, blank=True, null=True,
                                     verbose_name='Supplier Ordering Address')
    goods_recep = models.CharField(db_column='GOODS_RECEP', max_length=12, blank=False, null=False,
                                   verbose_name='Goods Recipient')
    bill_to_addr_num = models.CharField(db_column='BILL_TO_ADDR_NUM', max_length=10, blank=False, null=False,
                                        verbose_name='bill to addr num')
    ship_to_addr_num = models.CharField(db_column='SHIP_TO_ADDR_NUM', max_length=10, blank=False, null=False,
                                        verbose_name='ship to addr num')
    manu_name = models.CharField(db_column='MANU_NAME', max_length=50, blank=True, null=True, verbose_name='manu name')
    supp_txt = models.CharField(db_column='SUPP_TXT', max_length=1000, blank=True, null=True,
                                verbose_name='Supplier Text')
    internal_note = models.CharField(db_column='INTERNAL_NOTE', max_length=1000, blank=True, null=True,
                                     verbose_name='Internal Note')
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False,
                               db_column='CLIENT')
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        managed = True
        db_table = 'MSS_SC_ITEM'

    # Get item data by header guid
    def get_itms_by_guid(self, hdr_guid):
        return arch_ScItem.objects.filter(header_guid=hdr_guid).order_by('item_num')


# Definition of SC Accounting table structure
class arch_ScAccounting(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    item_guid = models.ForeignKey('arch_ScItem', models.DO_NOTHING, db_column='ITEM_GUID')
    acc_item_num = models.PositiveIntegerField(db_column='ACC_ITEM_NUM', null=True, blank=True)
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
    generic_acc_ass = models.CharField(db_column='GENERIC_ACC_ASS', max_length=64, blank=True, null=True,
                                       verbose_name='Generic Acc Ass')
    wbs_ele = models.CharField(db_column='WBS_ELE', max_length=24, blank=True, null=True, verbose_name='WBS Element')
    project = models.CharField(db_column='PROJECT', max_length=24, blank=True, null=True, verbose_name='Project')
    task_id = models.CharField(db_column='TASK_ID', max_length=25, blank=True, null=True, verbose_name='Task Id')
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False,
                               db_column='CLIENT')
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        managed = True
        db_table = 'MSS_SC_ACCOUNTING'

    # Get accounting data by item guid
    def get_acc_data_by_guid(self, itm_guid):
        return arch_ScAccounting.objects.filter(item_guid__in=itm_guid).order_by('acc_item_num')


# Definition of SC Approval table structure
class arch_ScApproval(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    header_guid = models.ForeignKey('arch_ScHeader', models.DO_NOTHING, db_column='HEADER_GUID')
    step_num = models.CharField(db_column='STEP_NUM', max_length=3, blank=True, null=True, verbose_name='Sequence')
    app_desc = models.CharField(db_column='APP_DESC', max_length=60, blank=True, null=True,
                                verbose_name='Agent Determination')
    proc_lvl_sts = models.CharField(db_column='PROC_LVL_STS', max_length=10, blank=True, null=True,
                                    verbose_name='Level Status')
    app_sts = models.CharField(db_column='APP_STS', max_length=20, blank=True, null=True, verbose_name='Status')
    app_id = models.CharField(db_column='APP_ID', max_length=70, blank=True, null=True, verbose_name='Processor')
    recevied_time = models.DateTimeField(db_column='RECEVIED_TIME', blank=True, null=True, verbose_name='Received On')
    proc_time = models.DateTimeField(db_column='PROC_TIME', blank=True, null=True, verbose_name='Processed On')
    time_zone = models.CharField(db_column='TIME_ZONE', max_length=6, blank=True, null=True, verbose_name='Time Zone')
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False,
                               db_column='CLIENT')
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        managed = True
        db_table = 'MSS_SC_APPROVAL'

    # Get approval data by header guid
    def get_apprs_by_guid(self, hdr_guid):
        return arch_ScApproval.objects.filter(header_guid=hdr_guid).order_by('step_num')


class arch_PoHeader(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    doc_number = models.CharField(db_column='DOC_NUMBER', max_length=10, blank=False, null=False,
                                  verbose_name='PO Number')
    version_type = models.CharField(db_column='VERSION_TYPE', max_length=1, blank=True, null=False,
                                    verbose_name='Version type')
    version_num = models.CharField(db_column='VERSION_NUM', max_length=8, blank=True, null=False,
                                   verbose_name='Version number')
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=False,
                                   verbose_name='PO NAME')
    total_value = models.CharField(db_column='TOTAL_VALUE', max_length=20, blank=False, null=False,
                                   verbose_name='Total Value')
    currency = models.CharField(db_column='CURRENCY', max_length=5, blank=False, null=False, verbose_name='Currency')
    requester = models.CharField(db_column='REQUESTER', max_length=12, blank=False, null=False,
                                 verbose_name='Requester')
    status = models.CharField(db_column='STATUS', max_length=20, blank=False, null=False, verbose_name='Status')
    created_at = models.DateTimeField(db_column='CREATED_AT', blank=False, null=False, verbose_name='Created At')
    created_by = models.CharField(db_column='CREATED_BY', max_length=12, blank=False, null=False,
                                  verbose_name='Creator')
    changed_at = models.DateTimeField(db_column='CHANGED_AT', blank=True, null=False, verbose_name='Changed At')
    changed_by = models.CharField(db_column='CHANGED_BY', max_length=12, blank=False, null=False,
                                  verbose_name='Changed By')
    ordered_at = models.DateTimeField(db_column='ORDERED_AT', blank=True, null=True, verbose_name='Ordered At')
    time_zone = models.CharField(db_column='TIME_ZONE', max_length=6, blank=True, null=False, verbose_name='Time Zone')
    item_cat = models.CharField(db_column='ITEM_CAT', max_length=4, blank=False, null=True,
                                verbose_name='Item Category')
    limit = models.CharField(db_column='LIMIT', max_length=20, blank=True, null=True, verbose_name='Limit')
    expected_value = models.CharField(db_column='EXPECTED_VALUE', max_length=20, blank=True, null=True,
                                      verbose_name='Limit')
    unlimited = models.CharField(db_column='UNLIMITED', max_length=1, blank=True, null=True, verbose_name='Unlimited')
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=12, blank=True, null=True,
                                   verbose_name='Supplier ID')
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False,
                               db_column='CLIENT')

    class Meta:
        managed = True
        unique_together = ('client', 'doc_number')
        db_table = 'MSS_PO_HEADER'

    # Get header data by supplier id
    def get_hdr_data_by_supplier(self, sup_id):
        return arch_PoHeader.objects.filter(supplier_id=sup_id).distinct()

    # Get header data by guid
    def get_hdr_data_by_guid(self, guid):
        return arch_PoHeader.objects.filter(guid=guid)

    # Get header guid by object id
    @staticmethod
    def get_hdr_guid_by_objid(objid):
        try:
            hdr = arch_PoHeader.objects.get(doc_number=objid)
            return getattr(hdr, 'guid')
        except ObjectDoesNotExist:
            return 'error'
        except MultipleObjectsReturned:
            hdr = arch_PoHeader.objects.filter(doc_number=objid)
            hdr = sorted(hdr, key=operator.attrgetter('version_num'))
            return getattr(hdr[0], 'guid')

    # Get object id by guid
    @staticmethod
    def get_objid_by_guid(guid):
        try:
            return str(getattr(arch_PoHeader.objects.get(guid=guid), 'doc_number'))
        except:
            return ''


class arch_PoItem(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    header_guid = models.ForeignKey('arch_PoHeader', models.DO_NOTHING, db_column='HEADER_GUID', blank=False,
                                    null=False)
    po_item_num = models.CharField(db_column='PO_ITEM_NUM', max_length=10, blank=True, null=True,
                                   verbose_name='Line Number')
    sc_num = models.CharField(db_column='SC_NUM', max_length=10, blank=True, null=True, verbose_name='SC Number')
    sc_header_guid = models.CharField(db_column='SC_HEADER_GUID', max_length=32, blank=True, null=True)
    item_num = models.PositiveIntegerField(db_column='ITEM_NUM', null=True, blank=True)
    sc_item_guid = models.CharField(db_column='SC_ITEM_GUID', max_length=32, blank=True, null=True)
    prod_description = models.CharField(db_column='PROD_DESCRIPTION', max_length=255, blank=False, null=False,
                                        verbose_name='Description')
    comp_code = models.CharField(db_column='COMP_CODE', max_length=10, blank=False, null=False,
                                 verbose_name='Company Code')
    purch_grp = models.CharField(db_column='PURCH_GRP', max_length=20, blank=True, null=True,
                                 verbose_name='Purchasing Group')
    purch_org = models.CharField(db_column='PURCH_ORG', max_length=20, blank=True, null=True,
                                 verbose_name='Purchasing Organization')
    item_del_date = models.DateField(db_column='ITEM_DEL_DATE', max_length=10, blank=False, null=True,
                                     verbose_name='Delivery Date')
    prod_cat = models.CharField(db_column='PROD_CAT', max_length=20, blank=False, null=False,
                                verbose_name='Product Category')
    hiring_level = models.CharField(db_column='HIRING_LEVEL', max_length=64, blank=True, null=True)
    hiring_role = models.CharField(db_column='HIRING_ROLE', max_length=64, blank=True, null=True)
    hiring_skill = models.CharField(db_column='HIRING_SKILL', max_length=64, blank=True, null=True)
    prod_type = models.CharField(db_column='PROD_TYPE', max_length=2, blank=False, null=False,
                                 verbose_name='Product Type')
    catalog_id = models.CharField(db_column='CATALOG_ID', max_length=20, blank=True, null=True,
                                  verbose_name='Catalog ID')
    unspsc = models.CharField(db_column='UNSPSC', max_length=10, blank=True, null=True, verbose_name='UNSPSC')
    fin_entry_ind = models.CharField(db_column='FIN_ENTRY_IND', max_length=1, blank=True, null=True,
                                     verbose_name='fin_entry_ind')
    quantity = models.CharField(db_column='QUANTITY', max_length=20, blank=True, null=True, verbose_name='Quantity')
    price = models.CharField(db_column='PRICE', max_length=15, blank=True, null=True, verbose_name='Price')
    price_unit = models.CharField(db_column='PRICE_UNIT', max_length=5, blank=True, null=True,
                                  verbose_name='Price Unit')
    unit = models.CharField(db_column='UNIT', max_length=3, blank=False, null=False, verbose_name='Unit')
    gross_price = models.CharField(db_column='GROSS_PRICE', max_length=15, blank=True, null=True,
                                   verbose_name='Gross Price')
    gr_ind = models.CharField(db_column='GR_IND', max_length=1, blank=True, null=True, verbose_name='Gr ind')
    supp_prod_num = models.CharField(db_column='SUPP_PROD_NUM', max_length=40, blank=True, null=True,
                                     verbose_name='Supplier Product Number')
    manu_part_num = models.CharField(db_column='MANU_PART_NUM', max_length=40, blank=True, null=True,
                                     verbose_name='manu part num')
    manu_code_num = models.CharField(db_column='MANU_CODE_NUM', max_length=10, blank=True, null=True,
                                     verbose_name='manu code num')
    ctr_num = models.CharField(db_column='CTR_NUM', max_length=50, blank=True, null=True, verbose_name='ctr num')
    supp_ord_addr = models.CharField(db_column='SUPP_ORD_ADDR', max_length=10, blank=True, null=True,
                                     verbose_name='Supplier Ordering Address')
    del_srm_purch_doc = models.CharField(db_column='DEL_SRM_PURCH_DOC', max_length=12, blank=True, null=True,
                                         verbose_name='Deletion Indicator SRM Purchasing Document')
    bill_to_addr_num = models.CharField(db_column='BILL_TO_ADDR_NUM', max_length=10, blank=False, null=False,
                                        verbose_name='bill to addr num')
    ship_to_addr_num = models.CharField(db_column='SHIP_TO_ADDR_NUM', max_length=10, blank=False, null=False,
                                        verbose_name='ship to addr num')
    goods_recep = models.CharField(db_column='GOODS_RECEP', max_length=12, blank=False, null=False,
                                   verbose_name='Goods Recipient')
    manu_name = models.CharField(db_column='MANU_NAME', max_length=50, blank=True, null=True, verbose_name='manu name')
    del_time_days = models.CharField(db_column='DEL_TIME_DAYS', max_length=5, blank=True, null=True,
                                     verbose_name='Delivery Days')
    internal_note = models.CharField(db_column='INTERNAL_NOTE', max_length=1000, blank=True, null=True,
                                     verbose_name='Internal Note')
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False,
                               db_column='CLIENT')

    class Meta:
        managed = True
        db_table = 'MSS_PO_ITEM'

    # Get item data by header guid
    def get_itms_by_guid(self, hdr_guid):
        return arch_PoItem.objects.filter(header_guid=hdr_guid).order_by('po_item_num')


class arch_PoApproval(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    header_guid = models.ForeignKey('arch_PoHeader', models.DO_NOTHING, db_column='HEADER_GUID', blank=True, null=True)
    step_num = models.CharField(db_column='STEP_NUM', max_length=3, blank=True, null=True, verbose_name='Sequence')
    app_desc = models.CharField(db_column='APP_DESC', max_length=60, blank=True, null=True,
                                verbose_name='Agent Determination')
    proc_lvl_sts = models.CharField(db_column='PROC_LVL_STS', max_length=10, blank=True, null=True,
                                    verbose_name='Level Status')
    app_sts = models.CharField(db_column='APP_STS', max_length=20, blank=True, null=True, verbose_name='Status')
    app_id = models.CharField(db_column='APP_ID', max_length=70, blank=True, null=True, verbose_name='Processor')
    recevied_time = models.DateTimeField(db_column='RECEVIED_TIME', max_length=32, blank=True, null=True,
                                         verbose_name='Received On')
    proc_time = models.DateTimeField(db_column='PROC_TIME', max_length=32, blank=True, null=True,
                                     verbose_name='Processed On')
    time_zone = models.CharField(db_column='TIME_ZONE', max_length=6, blank=True, null=True, verbose_name='Time Zone')
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False,
                               db_column='CLIENT')

    class Meta:
        managed = True
        db_table = 'MSS_PO_APPROVAL'

    # Get approval data by header guid
    def get_apprs_by_guid(self, hdr_guid):
        app_data = arch_PoApproval.objects.filter(header_guid=hdr_guid).order_by('step_num')
        return app_data


class arch_PoAccounting(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    item_guid = models.ForeignKey('arch_PoItem', models.DO_NOTHING, db_column='ITEM_GUID', blank=True, null=True)
    acc_item_num = models.PositiveIntegerField(db_column='ACC_ITEM_NUM', null=True, blank=True)
    acc_cat = models.CharField(db_column='ACC_CAT', max_length=5, blank=False, null=False,
                               verbose_name='Account Assignment Category')
    dist_perc = models.CharField(db_column='DIST_PERC', max_length=6, blank=True, null=True,
                                 verbose_name='Distribution Percentage')
    gl_acc_num = models.CharField(db_column='GL_ACC_NUM', max_length=10, blank=False, null=False,
                                  verbose_name='General Ledger Account')
    cost_center = models.CharField(db_column='COST_CENTER', max_length=10, blank=True, null=True,
                                   verbose_name='Cost Center')
    internal_order = models.CharField(db_column='INTERNAL_ORDER', max_length=12, blank=True, null=True,
                                      verbose_name='Internal Order')
    generic_acc_ass = models.CharField(db_column='GENERIC_ACC_ASS', max_length=64, blank=True, null=True,
                                       verbose_name='Generic Acc Ass')
    wbs_ele = models.CharField(db_column='WBS_ELE', max_length=24, blank=True, null=True, verbose_name='WBS Element')
    project = models.CharField(db_column='PROJECT', max_length=24, blank=True, null=True, verbose_name='Project')
    task_id = models.CharField(db_column='TASK_ID', max_length=25, blank=True, null=True, verbose_name='Task Id')
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False,
                               db_column='CLIENT')

    class Meta:
        managed = True
        db_table = 'MSS_PO_ACCOUNTING'

    # Get accounting data by item guid
    def get_acc_data_by_guid(self, itm_guid):
        return arch_PoAccounting.objects.filter(item_guid__in=itm_guid).order_by('acc_item_num')


# class arch_UserSearch(models.Model):
#     username = models.CharField(db_column='USERNAME', max_length=16, null=False)
#     first_name = models.CharField(db_column='FIRST_NAME', max_length=40, null=True)
#     last_name = models.CharField(db_column='LAST_NAME', max_length=40, null=True)
#     map_id = models.CharField(db_column='MAP_ID', max_length=8, null=False, primary_key=True)
#     client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False,
#                                db_column='CLIENT')
#
#     class Meta:
#         unique_together = ('client', 'username')
#         managed = True
#         db_table = 'MMD_USER_INFO'


class arch_SupplierSearch(models.Model):
    supplier_id = models.CharField(db_column='USERNAME', max_length=16, null=False)
    first_name = models.CharField(db_column='FIRST_NAME', max_length=40, null=True)
    last_name = models.CharField(db_column='LAST_NAME', max_length=40, null=True)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False,
                               db_column='CLIENT')
    map_id = models.CharField(db_column='MAP_ID', max_length=8, null=False, primary_key=True)

    class Meta:
        unique_together = ('client', 'supplier_id')
        managed = True
        db_table = 'MMD_SUPPLIER_SEARCH'

    # TO get supplier id by first name
    @staticmethod
    def get_suppid_by_first_name(fname):
        if '*' in fname:
            requester = re.search(r'[a-zA-Z0-9]+', fname)
            if fname[0] == '*' and fname[-1] == '*':
                queryset = arch_SupplierSearch.objects.values_list('supplier_id', flat=False).filter(
                    first_name__icontains=requester.group(0))
            elif fname[0] == '*':
                queryset = arch_SupplierSearch.objects.values_list('supplier_id', flat=False).filter(
                    first_name__iendswith=requester.group(0))
            else:
                queryset = arch_SupplierSearch.objects.values_list('supplier_id', flat=False).filter(
                    first_name__istartswith=requester.group(0))

        else:
            queryset = arch_SupplierSearch.objects.values_list('supplier_id', flat=False).filter(first_name=fname)
        supp_list = []
        for field in queryset:
            supp_list.append(field[0])
        return supp_list


class ConfHeader(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    doc_number = models.CharField(db_column='DOC_NUMBER', max_length=10, blank=False, null=False,
                                  verbose_name='PO Number')
    conf_sub_type = models.CharField(db_column='CONF_SUB_TYPE', max_length=4, blank=True, null=False,
                                     verbose_name='Confirmation Sub Type')
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=False,
                                   verbose_name='PO NAME')
    total_value = models.CharField(db_column='TOTAL_VALUE', max_length=20, blank=False, null=False,
                                   verbose_name='Total Value')
    currency = models.CharField(db_column='CURRENCY', max_length=5, blank=False, null=False, verbose_name='Currency')
    requester = models.CharField(db_column='REQUESTER', max_length=12, blank=False, null=False,
                                 verbose_name='Requester')
    status = models.CharField(db_column='STATUS', max_length=20, blank=False, null=False, verbose_name='Status')
    created_at = models.DateTimeField(db_column='CREATED_AT', blank=False, null=False, verbose_name='Created At')
    created_by = models.CharField(db_column='CREATED_BY', max_length=12, blank=False, null=False,
                                  verbose_name='Creator')
    changed_at = models.DateTimeField(db_column='CHANGED_AT', blank=True, null=False, verbose_name='Changed At')
    changed_by = models.CharField(db_column='CHANGED_BY', max_length=12, blank=False, null=False,
                                  verbose_name='Changed By')
    ordered_at = models.DateTimeField(db_column='ORDERED_AT', blank=True, null=True, verbose_name='Ordered At')
    time_zone = models.CharField(db_column='TIME_ZONE', max_length=6, blank=True, null=False, verbose_name='Time Zone')
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=12, blank=True, null=True,
                                   verbose_name='Supplier ID')
    supplier_name = models.CharField(db_column='SUPPLIER_Name', max_length=255, blank=True, null=True,
                                     verbose_name='Supplier Name')
    conf_movement = models.PositiveIntegerField(db_column='ACC_ITEM_NUM', null=True, blank=True)
    po_doc_number = models.CharField(db_column='PO_DOC_NUMBER', max_length=10, blank=False, null=False,
                                     verbose_name='PO Document Number')
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False,
                               db_column='CLIENT')

    class Meta:
        managed = True
        unique_together = ('client', 'doc_number')
        db_table = 'MSS_CONF_HEADER'

    def get_hdr_data_by_guid(self, guid):
        return ConfHeader.objects.filter(guid=guid)


class ConfItem(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    header_guid = models.ForeignKey('ConfHeader', models.DO_NOTHING, db_column='HEADER_GUID', blank=False, null=False)
    item_num = models.CharField(db_column='CONF_ITEM_NUM', max_length=10, blank=True, null=True,
                                verbose_name='Line Number')
    po_item_num = models.CharField(db_column='PO_ITEM_NUM', max_length=10, blank=True, null=True,
                                   verbose_name='Line Number')
    ref_item_guid = models.CharField(db_column='REF_ITEM_GUID', max_length=32)
    prod_description = models.CharField(db_column='PROD_DESCRIPTION', max_length=255, blank=False, null=False,
                                        verbose_name='Description')
    comp_code = models.CharField(db_column='COMP_CODE', max_length=10, blank=False, null=False,
                                 verbose_name='Company Code')
    purch_grp = models.CharField(db_column='PURCH_GRP', max_length=20, blank=True, null=True,
                                 verbose_name='Purchasing Group')
    purch_org = models.CharField(db_column='PURCH_ORG', max_length=20, blank=True, null=True,
                                 verbose_name='Purchasing Organization')
    po_item_del_date = models.DateField(db_column='PO_ITEM_DEL_DATE', max_length=10, blank=False, null=True,
                                        verbose_name='Po Item Delivery Date')
    del_note_date = models.DateField(db_column='DEL_NOTE_DATE', max_length=10, blank=False, null=True,
                                     verbose_name='Delivery Note Date')
    prod_cat = models.CharField(db_column='PROD_CAT', max_length=20, blank=False, null=False,
                                verbose_name='Product Category')
    prod_type = models.CharField(db_column='PROD_TYPE', max_length=2, blank=False, null=False,
                                 verbose_name='Product Type')
    catalog_id = models.CharField(db_column='CATALOG_ID', max_length=20, blank=True, null=True,
                                  verbose_name='Catalog ID')
    unspsc = models.CharField(db_column='UNSPSC', max_length=10, blank=True, null=True, verbose_name='UNSPSC')
    quantity = models.CharField(db_column='QUANTITY', max_length=20, blank=True, null=True, verbose_name='Quantity')
    price = models.CharField(db_column='PRICE', max_length=15, blank=True, null=True, verbose_name='Price')
    price_unit = models.CharField(db_column='PRICE_UNIT', max_length=5, blank=True, null=True,
                                  verbose_name='Price Unit')
    unit = models.CharField(db_column='UNIT', max_length=3, blank=False, null=False, verbose_name='Unit')
    gross_price = models.CharField(db_column='GROSS_PRICE', max_length=15, blank=True, null=True,
                                   verbose_name='Gross Price')
    supp_prod_num = models.CharField(db_column='SUPP_PROD_NUM', max_length=40, blank=True, null=True,
                                     verbose_name='Supplier Product Number')
    manu_part_num = models.CharField(db_column='MANU_PART_NUM', max_length=40, blank=True, null=True,
                                     verbose_name='manu part num')
    manu_code_num = models.CharField(db_column='MANU_CODE_NUM', max_length=10, blank=True, null=True,
                                     verbose_name='manu code num')
    ctr_num = models.CharField(db_column='CTR_NUM', max_length=50, blank=True, null=True, verbose_name='ctr num')
    goods_recep = models.CharField(db_column='GOODS_RECEP', max_length=12, blank=False, null=False,
                                   verbose_name='Goods Recipient')
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False,
                               db_column='CLIENT')

    class Meta:
        managed = True
        db_table = 'MSS_CONF_ITEM'

    def get_itms_by_guid(self, hdr_guid):
        return ConfItem.objects.filter(header_guid=hdr_guid).order_by('item_num')


class ConfAccounting(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    item_guid = models.ForeignKey('ConfItem', models.DO_NOTHING, db_column='ITEM_GUID', blank=True, null=True)
    acc_item_num = models.PositiveIntegerField(db_column='ACC_ITEM_NUM', null=True, blank=True)
    acc_cat = models.CharField(db_column='ACC_CAT', max_length=5, blank=False, null=False,
                               verbose_name='Account Assignment Category')
    dist_perc = models.CharField(db_column='DIST_PERC', max_length=6, blank=True, null=True,
                                 verbose_name='Distribution Percentage')
    gl_acc_num = models.CharField(db_column='GL_ACC_NUM', max_length=10, blank=False, null=False,
                                  verbose_name='General Ledger Account')
    cost_center = models.CharField(db_column='COST_CENTER', max_length=10, blank=True, null=True,
                                   verbose_name='Cost Center')
    internal_order = models.CharField(db_column='INTERNAL_ORDER', max_length=12, blank=True, null=True,
                                      verbose_name='Internal Order')
    generic_acc_ass = models.CharField(db_column='GENERIC_ACC_ASS', max_length=64, blank=True, null=True,
                                       verbose_name='Generic Acc Ass')
    wbs_ele = models.CharField(db_column='WBS_ELE', max_length=24, blank=True, null=True, verbose_name='WBS Element')
    project = models.CharField(db_column='PROJECT', max_length=24, blank=True, null=True, verbose_name='Project')
    task_id = models.CharField(db_column='TASK_ID', max_length=25, blank=True, null=True, verbose_name='Task Id')
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False,
                               db_column='CLIENT')

    class Meta:
        managed = True
        db_table = 'MSS_CONF_ACCOUNTING'

    # Get accounting data by item guid
    def get_acc_data_by_guid(self, itm_guid):
        return ConfAccounting.objects.filter(item_guid__in=itm_guid).order_by('acc_item_num')


class arch_CompanyGrpUser(models.Model):
    """
    Contains company code description
    """
    company_grp_user_guid = models.CharField(db_column='COMPANY_GUID', primary_key=True, max_length=32)
    company_grp_id = models.CharField(db_column='COMPANY_GRP_ID', max_length=20, null=False)
    username = models.CharField(db_column='USERNAME', max_length=16, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', db_column='Client', on_delete=models.PROTECT,
                               null=False)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "MSS_COMP_CODE_GRP_USER"
        managed = True

    def __str__(self):
        return self.company_grp_id


class arch_CompanyCodeGrp(models.Model):
    """
    Contains company code description
    """
    company_grp_guid = models.CharField(db_column='COMPANY_GUID', primary_key=True, max_length=32)
    company_grp_id = models.CharField(db_column='COMPANY_GRP_ID', max_length=20, null=False)
    company_code_id = models.CharField(db_column='COMPANY_CODE_ID', max_length=20, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', db_column='Client', on_delete=models.PROTECT,
                               null=False)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "MSS_COMP_CODE_GRP"
        managed = True

    def __str__(self):
        return self.company_grp_id
