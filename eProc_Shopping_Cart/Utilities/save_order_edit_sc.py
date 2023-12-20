from eProc_Attributes.Utilities.attributes_generic import OrgAttributeValues
from eProc_Attributes.models.org_attribute_models import OrgAttributesLevel
from eProc_Basic.Utilities.functions.dict_check_key import checkKey
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.generate_document_number import generate_document_number
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc

from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG161, MSG162, MSG163, MSG164, MSG165, MSG166, MSG167, MSG168, \
    MSG169, MSG170, MSG171, MSG192
from eProc_Calendar_Settings.Utilities.calender_settings_generic import calculate_delivery_date, \
    calculate_delivery_date_base_on_lead_time, get_list_of_holidays
from eProc_Chat.models import ChatContent
from eProc_Configuration.models.application_data import SourcingMapping, SourcingRule
from eProc_Configuration.models.development_data import *
from eProc_Configuration.models.master_data import OrgAddress, AccountingDataDesc, DetermineGLAccount, AccountingData, \
    OrgAddressMap, OrgPorgMapping
from eProc_Exchange_Rates.Utilities.exchange_rates_generic import convert_currency
from eProc_Form_Builder.models.form_builder import EformFieldData
from eProc_Notes_Attachments.models.notes_attachements_model import Attachments, Notes
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import convert_to_boolean, check_for_eform, get_manger_detail, \
    get_users_first_name, delete_approver_detail, get_highest_acc_detail
from eProc_Suppliers.models.suppliers_model import OrgSuppliers
from eProc_Workflow.Utilities.work_flow_generic import save_sc_approval
import datetime
from django.utils.datastructures import MultiValueDictKeyError
from eProc_Configuration.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max, Q
from eProc_Configuration.models import NumberRanges
from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.get_db_query import getClients, getUsername, get_login_obj_id, \
    get_requester_currency, get_user_info, requester_field_info
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Notes_Attachments.Utilities.notes_attachments_generic import save_attachment_data, save_approval_note, \
    save_internal_supplier_note
from eProc_Price_Calculator.Utilities.price_calculator_generic import calculate_item_total_value, \
    calculate_item_price
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import get_prod_by_id
from eProc_Shopping_Cart.models import CartItemDetails, ScHeader, ScItem, ScAccounting, \
    ScAddresses, ScApproval, PurchasingData, ScPotentialApproval
from eProc_User_Settings.Utilities.user_settings_generic import get_object_id_list_user, get_attr_value
from eProc_Catalog.models import *
from eProc_Registration.models import *
import datetime

django_query_instance = DjangoQueries()


# Class to save shopping cart
class SaveShoppingCart:
    cart_guid = []
    eform_item_guid = []

    def __init__(self, request, sc_ui_data, attachments_data, sc_header_guid, save_type):
        self.po_transaction_type = None
        self.save_type = save_type
        self.header_status = ''
        self.cart_item_guid = []
        self.save_sc_data_to_db = SaveSoppingCartDataToDb()
        self.header_guid = sc_header_guid
        self.client = global_variables.GLOBAL_CLIENT
        self.username = global_variables.GLOBAL_LOGIN_USERNAME
        self.login_user_obj_id = global_variables.GLOBAL_LOGIN_USER_OBJ_ID
        self.object_id_list = get_object_id_list_user(self.client, self.login_user_obj_id)
        self.edit_flag = False
        self.supplier_note_existence_data = ''
        self.internal_note_existence_data = ''
        self.attachment_existence_data = ''
        self.accounting_change_type = ''
        self.accounting_change_value = ''
        self.address_change_data = {}

        if 'approver_text' in sc_ui_data:
            self.approver_text = sc_ui_data['approver_text']
        self.doc_number = ''
        self.sc_ui_data = sc_ui_data
        self.attachments_data = attachments_data
        self.requester = self.sc_ui_data['requester']
        if self.requester:
            self.currency = global_variables.GLOBAL_USER_CURRENCY
            self.timezone = global_variables.GLOBAL_USER_TIMEZONE
        self.company_code = get_attr_value(self.client, CONST_CO_CODE, self.object_id_list, self.edit_flag)
        self.invoice_address = get_attr_value(self.client, CONST_INV_ADDR, self.object_id_list, self.edit_flag)
        self.subtype = ''

        if not self.invoice_address:
            self.invoice_address = 0

        if checkKey(sc_ui_data, 'adr_num'):
            if self.sc_ui_data['adr_num']:
                self.ship_addr_num = self.sc_ui_data['adr_num']
            else:
                self.ship_addr_num = 0

    # Method to save header details
    def save_header_details(self, status):
        """
        :return:
        """
        time_diff = None
        if django_query_instance.django_existence_check(TimeZone, {'time_zone': self.timezone, 'del_ind': False}):
            get_tz_difference = django_query_instance.django_get_query(TimeZone, {'time_zone': self.timezone,
                                                                                  'del_ind': False})
            time_diff = get_tz_difference.utc_difference

        if self.login_user_obj_id is None or self.login_user_obj_id == '' or self.login_user_obj_id == 0:
            msgid = 'MSG161'
            error_msg = get_message_desc(msgid)[1]

            error = error_msg
            return False, error

        get_document_number = generate_document_number(CONST_SC_TRANS_TYPE, self.client, self.object_id_list,
                                                       self.edit_flag, CONST_DOC_TYPE_SC)
        if not get_document_number[0]:
            return False, get_document_number[1]
        self.po_transaction_type = get_attr_value(self.client, CONST_PO_TRANS_TYPE, self.object_id_list, self.edit_flag)
        if len(self.po_transaction_type) == 0:
            msgid = 'MSG192'
            error_msg = get_message_desc(msgid)[1]

            return False, error_msg
        self.subtype = get_document_number[2]
        self.doc_number = get_document_number[0]
        if not django_query_instance.django_existence_check(Currency,
                                                            {'currency_id': self.currency,
                                                             'del_ind': False}):
            self.currency = None

        if not django_query_instance.django_existence_check(TimeZone,
                                                            {'time_zone': self.timezone,
                                                             'del_ind': False}):
            self.timezone = None

        header_guid = self.header_guid
        ordered_at = None
        if self.save_type == 'Order':
            ordered_at = datetime.datetime.today()
        self.header_status = status

        sc_header_save_data = {
            'guid': self.header_guid,
            'client': global_variables.GLOBAL_CLIENT,
            'doc_number': get_document_number[0],
            'co_code': self.company_code,
            'description': self.sc_ui_data['cart_name'],
            'currency': self.currency,
            'requester': self.sc_ui_data['requester'],
            'status': status,
            'created_at': datetime.datetime.now(),
            'created_by': self.username,
            'ship_addr_num': self.ship_addr_num,
            'inv_addr_num': self.invoice_address,
            'time_zone': self.timezone,
            'time_zone_difference': time_diff,
            'ordered_at': ordered_at,
            'transaction_type': self.subtype,
            'language_id': global_variables.GLOBAL_USER_LANGUAGE
        }

        self.save_sc_data_to_db.save_header_to_db(header_guid, sc_header_save_data)

        update_number_range = django_query_instance.django_filter_only_query(NumberRanges, {
            'sequence': int(get_document_number[1]), 'client': self.client, 'document_type': CONST_DOC_TYPE_SC
        })

        update_number_range.update(current=self.doc_number, client=self.client)
        acc_type = self.sc_ui_data['acc_assign_cat']
        acc_value = self.sc_ui_data['acc_assign_val']
        gl_acc_value = ' '
        item_flag = False
        self.accounting_change_type = acc_type
        self.accounting_change_value = acc_value
        SaveShoppingCart.save_accounting_data(self, None, self.header_guid, None, acc_type, acc_value, gl_acc_value,
                                              item_flag)
        address_number = self.sc_ui_data['adr_num'].replace(',', '')
        street_output = self.sc_ui_data['street'].replace(',', '')
        area_output = self.sc_ui_data['area'].replace(',', '')
        landmark_output = self.sc_ui_data['landmark'].replace(',', '')
        city_output = self.sc_ui_data['city'].replace(',', '')
        pcode_output = self.sc_ui_data['pcode'].replace(',', '')
        region_output = self.sc_ui_data['region'].replace(',', '')
        self.address_change_data = {'address_number': address_number, 'street_output': street_output,
                                    'area_output': area_output,
                                    'landmark_output': landmark_output, 'city_output': city_output,
                                    'pcode_output': pcode_output,
                                    'region_output': region_output}
        SaveShoppingCart.save_address(self, None, self.header_guid, None, address_number, street_output, area_output,
                                      landmark_output, city_output, pcode_output, region_output, item_flag)

        return self.doc_number, self.sc_ui_data['cart_name'], get_document_number[1]

    def save_item_details(self, request):
        """
        :param request:
        :return:
        """
        global int_prod_id
        pref_supplier = ''
        start_date = None
        end_date = None
        required_on = None
        unit = ''
        overall_limit = None
        expected_value = None
        ir_gr_ind = False
        gr_ind = False
        quantity = None
        catalog_qty = None
        supplier_id = None
        ctr_num = None
        ctr_item_num = None
        order_date = None
        offcatalog = True
        product_guid = None
        supp_prod_num = None
        supplier_name = None
        supplier_contact = None
        supplier_fax_no = None
        supplier_email = None
        blocked_supplier = None
        delivery_days = None
        catalog_id = None
        supplier_type = ''
        int_prod_id = ''
        gross_price = ''

        if self.save_type == 'Order':
            order_date = datetime.datetime.now()

        is_eform = False
        cart_items = django_query_instance.django_filter_query(CartItemDetails,
                                                               {'client': self.client,
                                                                'username': self.username},
                                                               ['item_num'],
                                                               None)

        counter = 0
        for item in cart_items:
            self.cart_item_guid.append(item['guid'])
            cart_item_details = django_query_instance.django_get_query(CartItemDetails, {'guid': item['guid'],
                                                                                         'client': self.client})
            guid = guid_generator()

            # Product category for free text item should be retrieved from mss_freetext_form
            # based on supplier_id and client
            if cart_item_details.call_off != CONST_PR_CALLOFF:
                if django_query_instance.django_existence_check(SupplierMaster, {
                    'supplier_id': cart_item_details.supplier_id, 'client': self.client
                }):
                    get_supplier_detail = django_query_instance.django_get_query(SupplierMaster, {
                        'supplier_id': cart_item_details.supplier_id, 'client': self.client
                    })

                    supplier_name = get_supplier_detail.name1 + ' ' + get_supplier_detail.name2
                    supplier_contact = get_supplier_detail.mobile_num
                    supplier_type = get_supplier_detail.supp_type
                    supplier_fax_no = get_supplier_detail.fax
                    supplier_email = get_supplier_detail.email
                    blocked_supplier = get_supplier_detail.block
                    delivery_days = get_supplier_detail.delivery_days

            if cart_item_details.call_off == CONST_FREETEXT_CALLOFF:
                product_cat_id = django_query_instance.django_get_query(FreeTextDetails, {
                    'freetext_id': cart_item_details.int_product_id, 'del_ind': False, 'client': self.client
                })
                prod_cat = product_cat_id.prod_cat_id
                prod_cat_desc = get_prod_by_id(product_cat_id.prod_cat_id)
                unspsc = product_cat_id.prod_cat_id
            else:
                product_cat_id = cart_item_details.prod_cat_id
                prod_cat = product_cat_id
                prod_cat_desc = get_prod_by_id(cart_item_details.prod_cat_id)
                unspsc = cart_item_details.prod_cat_id

            # Supplier details
            pref_supplier = None
            supplier_id = None

            if cart_item_details.call_off in [CONST_LIMIT_ORDER_CALLOFF, CONST_PR_CALLOFF]:
                pref_supplier = cart_item_details.supplier_id

            if cart_item_details.call_off == CONST_PR_CALLOFF:
                pref_supplier = cart_item_details.pref_supplier

            else:
                supplier_id = cart_item_details.supplier_id

            if cart_item_details.call_off == CONST_CATALOG_CALLOFF:
                offcatalog = False

            int_product_id = None
            # Call_off details
            int_prod_id = item['int_product_id']
            if cart_item_details.call_off == CONST_CATALOG_CALLOFF:
                item_cat = 'Green'
                if django_query_instance.django_existence_check(ProductsDetail, {
                    'product_id': int_prod_id, 'client': self.client, 'del_ind': False
                }):
                    get_product_detail = django_query_instance.django_get_query(ProductsDetail, {
                        'product_id': int_prod_id, 'client': self.client, 'del_ind': False
                    })
                    ctr_num = get_product_detail.ctr_num
                    ctr_item_num = get_product_detail.ctr_item_num
                    supp_prod_num = get_product_detail.supp_product_id
                    product_guid = get_product_detail.catalog_item
                    # catalog_id = get_product_detail.catalog_id

            elif cart_item_details.call_off == CONST_PR_CALLOFF:
                item_cat = 'Red'
            else:
                item_cat = 'Yellow'

            # Product type details
            if cart_item_details.call_off in [CONST_CATALOG_CALLOFF, CONST_FREETEXT_CALLOFF, CONST_PR_CALLOFF]:
                prod_type = '01'
            else:
                prod_type = 'Limi'

            item_del_date = cart_item_details.item_del_date

            if cart_item_details.call_off == CONST_LIMIT_ORDER_CALLOFF:
                start_date = cart_item_details.start_date
                end_date = cart_item_details.end_date
                required_on = cart_item_details.item_del_date

            if cart_item_details.call_off == CONST_CATALOG_CALLOFF:
                # Pre-filled for catalog, price_unit also known as lot size
                price_unit = cart_item_details.price_unit
            else:
                # Hardcoded for other call-off's
                price_unit = '01'

            if not cart_item_details.call_off == CONST_LIMIT_ORDER_CALLOFF:
                unit = cart_item_details.unit

            if cart_item_details.call_off == CONST_LIMIT_ORDER_CALLOFF:
                overall_limit = cart_item_details.overall_limit
                expected_value = cart_item_details.expected_value
                ir_gr_ind = cart_item_details.ir_gr_ind_limi
                gr_ind = cart_item_details.gr_ind

            if cart_item_details.call_off == CONST_FREETEXT_CALLOFF:
                supp_prod_num = product_cat_id.eform_id

            if cart_item_details.call_off in [CONST_CATALOG_CALLOFF, CONST_PR_CALLOFF, CONST_FREETEXT_CALLOFF]:
                lead_time = cart_item_details.lead_time
            else:
                lead_time = None

            if cart_item_details.call_off == CONST_CATALOG_CALLOFF:
                catalog_qty = cart_item_details.quantity

            if cart_item_details.call_off in [CONST_FREETEXT_CALLOFF, CONST_PR_CALLOFF]:
                quantity = cart_item_details.quantity

            requester_currency = get_requester_currency(self.sc_ui_data['requester'])
            item_currency = cart_item_details.currency
            if not item_currency:
                item_currency = requester_currency
            if not cart_item_details.call_off == CONST_LIMIT_ORDER_CALLOFF:
                value = calculate_item_total_value(cart_item_details.call_off, cart_item_details.quantity, catalog_qty,
                                                   cart_item_details.price_unit, cart_item_details.price,
                                                   overall_limit=None)

                value = convert_currency(value, str(item_currency), str(requester_currency))
                gross_price = convert_currency(cart_item_details.gross_price, str(item_currency),
                                               str(global_variables.GLOBAL_USER_CURRENCY))

            else:
                value = cart_item_details.overall_limit
                value = convert_currency(value, str(item_currency), str(requester_currency))
            if cart_item_details.call_off == CONST_FREETEXT_CALLOFF:
                eform_check = check_for_eform(request)
                if cart_item_details.supplier_id not in eform_check:
                    eform = 1
                    is_eform = True
                    SaveShoppingCart.cart_guid.append(cart_item_details.guid)
                    SaveShoppingCart.eform_item_guid.append(guid)
                else:
                    eform = 0
                    is_eform = False
            else:
                eform = None

            check_silent_po = convert_to_boolean(self.sc_ui_data['get_silent_po'])
            if check_silent_po:
                silent_po = True
            else:
                silent_po = False
            item_num = counter + 1
            currency = cart_item_details.currency
            if not currency:
                currency = requester_currency
            acc_type = self.sc_ui_data['change_acc_type' + str(counter + 1)].split(' -')[0]
            acc_value = self.sc_ui_data['change_acc_value' + str(counter + 1)].split(' -')[0]
            address_number = self.sc_ui_data['address_number' + str(counter + 1)].replace(',', '')
            if address_number == '':
                address_number = None
            street_output = self.sc_ui_data['street_output' + str(counter + 1)].replace(',', '')
            area_output = self.sc_ui_data['area_output' + str(counter + 1)].replace(',', '')
            landmark_output = self.sc_ui_data['landmark_output' + str(counter + 1)].replace(',', '')
            city_output = self.sc_ui_data['city_output' + str(counter + 1)].replace(',', '')
            pcode_output = self.sc_ui_data['pcode_output' + str(counter + 1)].replace(',', '')
            region_output = self.sc_ui_data['region_output' + str(counter + 1)].replace(',', '')
            # check item level change in accounting
            if self.accounting_change_type != acc_type or self.accounting_change_value != acc_value:
                accounting_change_flag = True
            else:
                accounting_change_flag = False
            # check item level change in address
            if self.address_change_data['address_number'] != address_number or self.address_change_data[
                'street_output'] != street_output or self.address_change_data['area_output'] != area_output or \
                    self.address_change_data['landmark_output'] != landmark_output or self.address_change_data[
                'city_output'] != city_output or self.address_change_data['pcode_output'] != pcode_output or \
                    self.address_change_data['region_output'] != region_output:
                address_change_flag = True
            else:
                address_change_flag = False
            # check item level internal note present
            if self.sc_ui_data['internal_note' + str(item_num)]:
                internal_note_existence_flag = True
            else:
                internal_note_existence_flag = False

            # check item level supplier note present
            if self.sc_ui_data['supplier_note' + str(item_num)]:
                supplier_note_existence_flag = True
            else:
                supplier_note_existence_flag = False
            try:
                if self.sc_ui_data['attachment_name' + str(item_num)]:
                    attachment_existence_flag = True
                else:
                    attachment_existence_flag = False
            except:
                attachment_existence_flag = False
            if django_query_instance.django_existence_check(CatalogMapping,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'item_id': int_prod_id,
                                                             'del_ind': False}):
                catalog_id = django_query_instance.django_filter_value_list_query(CatalogMapping,
                                                                                  {
                                                                                      'client': global_variables.GLOBAL_CLIENT,
                                                                                      'item_id': int_prod_id,
                                                                                      'del_ind': False},
                                                                                  'catalog_id')[0]
            print(unspsc, cart_item_details.call_off, int_prod_id)
            grouping_ind = get_grouping_detail(self.company_code, unspsc, cart_item_details.call_off, int_prod_id)
            source_relevant_ind = get_source_relevant_ind(self.company_code, unspsc, cart_item_details.call_off,
                                                          int_prod_id)
            print("source_relevant_ind = ", source_relevant_ind)
            sc_item_save_data = {
                'guid': guid,
                'header_guid': django_query_instance.django_get_query(ScHeader,
                                                                      {'guid': self.header_guid, 'client': self.client,
                                                                       'del_ind': False}),
                'po_transaction_type': self.po_transaction_type,
                'item_num': item_num,
                'cust_prod_cat_id': prod_cat,
                'prod_cat_desc': prod_cat_desc,
                'prod_cat_id': unspsc,
                'comp_code': self.company_code,
                'pref_supplier': pref_supplier,
                'supplier_id': supplier_id,
                'process_flow': item_cat,
                'prod_type': prod_type,
                # 'catalog_id': catalog_id,
                'item_del_date': item_del_date,
                'product_info_id': cart_item_details.product_info_id,
                'start_date': start_date,
                'end_date': end_date,
                'catalog_id': catalog_id,
                'required_on': required_on,
                'long_desc': cart_item_details.long_desc,
                'price': cart_item_details.price,
                'base_price': cart_item_details.base_price,
                'additional_price': cart_item_details.additional_price,
                'actual_price': cart_item_details.actual_price,
                'discount_percentage': cart_item_details.discount_percentage,
                'discount_value': cart_item_details.discount_value,
                'cgst': cart_item_details.cgst,
                'sgst': cart_item_details.sgst,
                'vat': cart_item_details.vat,
                'tax_value': cart_item_details.tax_value,
                'gross_price': gross_price,
                'currency': currency,
                'price_unit': price_unit,
                'unit': unit,
                'overall_limit': overall_limit,
                'expected_value': expected_value,
                'ir_gr_ind': ir_gr_ind,
                'gr_ind': gr_ind,
                'call_off': cart_item_details.call_off,
                'bill_to_addr_num': self.invoice_address,
                'ship_to_addr_num': self.ship_addr_num,
                'del_ind': False,
                'created_at': datetime.datetime.now(),
                'created_by': self.username,
                'lead_time': lead_time,
                'catalog_qty': catalog_qty,
                'quantity': cart_item_details.quantity,
                'value': value,
                # 'eform': eform,
                'eform_id': cart_item_details.eform_id,
                'variant_id': cart_item_details.variant_id,
                'client': django_query_instance.django_get_query(OrgClients, {'client': self.client, 'del_ind': False}),
                'description': cart_item_details.description,
                'silent_po': silent_po,
                'goods_recep': self.sc_ui_data['receiver'],
                'int_product_id': int_prod_id,
                'ctr_num': ctr_num,
                'ctr_item_num': ctr_item_num,
                'supp_product_id': supp_prod_num,
                'document_type': CONST_BUS_TYPE_SC,
                'order_date': order_date,
                'offcatalog': offcatalog,
                'source_relevant_ind': source_relevant_ind,
                'grouping_ind': grouping_ind,
                # 'product_guid': product_guid,
                'supplier_username': supplier_name,
                'supp_type': supplier_type,
                'supplier_email': supplier_email,
                'supplier_mobile_num': supplier_contact,
                'supplier_fax_no': supplier_fax_no,
                'blocked_supplier': blocked_supplier,
                'delivery_days': delivery_days,
                'address_change_flag': address_change_flag,
                'accounting_change_flag': accounting_change_flag,
                'attachment_existence_flag': attachment_existence_flag,
                'internal_note_existence_flag': internal_note_existence_flag,
                'supplier_note_existence_flag': supplier_note_existence_flag
            }
            self.save_sc_data_to_db.save_sc_item_details_to_db(guid, sc_item_save_data)

            if cart_item_details.eform_id or cart_item_details.variant_id:
                EformFieldData.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                              cart_guid=item['guid']).update(
                    item_guid=django_query_instance.django_get_query(ScItem,
                                                                     {'client': global_variables.GLOBAL_CLIENT,
                                                                      'guid': guid}))
                # django_query_instance.django_update_or_create_query(EformFieldData,
                #                                                     {'client':global_variables.GLOBAL_CLIENT,
                #                                                      'cart_guid':item.guid},
                #                                                     {'item_guid':django_query_instance.django_get_query(ScItem,
                #                                                                                                         {'client':global_variables.GLOBAL_CLIENT,
                #                                                                                                          'guid':guid})})

            if is_eform:
                if cart_item_details.call_off == CONST_FREETEXT_CALLOFF:
                    eform = zip(SaveShoppingCart.cart_guid, SaveShoppingCart.eform_item_guid)
                    SaveShoppingCart.link_eform(self, eform)
                    is_eform = False

            gl_acc_value = self.sc_ui_data['gl_acc_val' + str(counter + 1)]
            item_flag = True

            SaveShoppingCart.save_accounting_data(self, guid, None, str(counter + 1), acc_type, acc_value, gl_acc_value,
                                                  item_flag)

            SaveShoppingCart.save_address(self, guid, None, str(counter + 1), address_number, street_output,
                                          area_output, landmark_output, city_output, pcode_output, region_output,
                                          item_flag)
            SaveShoppingCart.get_purchasing_data(self, guid, self.company_code, prod_cat, counter + 1, self.header_guid
                                                 , cart_item_details.supplier_id)
            SaveShoppingCart.save_notes_data(self, counter, guid, counter + 1)
            SaveShoppingCart.save_attachments(self, counter, guid, counter + 1, self.doc_number)
            counter = counter + 1
        total_value = self.sc_ui_data['total_value']

        sc_total_value = django_query_instance.django_filter_only_query(ScHeader, {'guid': self.header_guid,
                                                                                   'del_ind': False})
        sc_total_value.update(total_value=total_value, gross_amount=total_value)

    # Method to save accounting data
    def save_accounting_data(self, item_guid, header_guid, item_num, acc_type, acc_value, gl_acc_value, item_flag):
        """
        :param item_flag:
        :param gl_acc_value:
        :param acc_type:
        :param acc_value:
        :param acc_type:
        :param header_guid:
        :param item_guid:
        :param item_num:
        :return:
        """
        cost_center = None
        internal_order = None
        wbs_ele = None
        asset_number = None

        acc_assign_cat_data = acc_type
        acc_assign_cat = acc_assign_cat_data.split(' ')[0]
        acc_assign_val_data = acc_value
        acc_assign_val = acc_assign_val_data.split(' ')[0]
        if acc_assign_cat == 'CC':
            cost_center = acc_assign_val
        elif acc_assign_cat == 'OR':
            internal_order = acc_assign_val
        elif acc_assign_cat == 'WBS':
            wbs_ele = acc_assign_val
        else:
            asset_number = acc_assign_val
        guid = guid_generator()
        if item_flag:

            item_guid = django_query_instance.django_get_query(ScItem, {'guid': item_guid, 'client': self.client,
                                                                        'del_ind': False})
            header_guid = None
        else:
            item_guid = None
            header_guid = django_query_instance.django_get_query(ScHeader, {'guid': header_guid, 'client': self.client,
                                                                            'del_ind': False})
            item_num = 0
        sc_acc_save_data = {
            'guid': guid,
            'client': django_query_instance.django_get_query(OrgClients, {'client': self.client, 'del_ind': False}),
            'item_guid': item_guid,
            'header_guid': header_guid,
            'acc_item_num': item_num,
            'dist_perc': '100',  # Hardcoded
            'gl_acc_num': gl_acc_value,
            'acc_cat': acc_assign_cat,
            'ref_date': datetime.datetime.now(),
            'cost_center': cost_center,
            'internal_order': internal_order,
            'wbs_ele': wbs_ele,
            'asset_number': asset_number
        }

        self.save_sc_data_to_db.save_accounting_data(guid, sc_acc_save_data)

    def save_approval_data(self, manager_detail, button_status, sc_completion_flag):
        """
        save approval data based on managed detail
        :param sc_completion_flag:
        :param button_status:
        :param manager_detail:
        :return:
        """
        if manager_detail:
            if manager_detail[0] != '':
                save_sc_approval(manager_detail, self.header_guid, button_status, sc_completion_flag)

    # Method to save address at item level
    def save_address(self, item_guid, header_guid, item_num, address_number, street_output, area_output,
                     landmark_output, city_output, pcode_output, region_output, item_flag):
        """
        :param item_flag:
        :param region_output:
        :param pcode_output:
        :param city_output:
        :param area_output:
        :param street_output:
        :param address_number:
        :param header_guid:
        :param landmark_output:
        :param item_guid: It stores item guid to save data at item level
        Data like street, area, landmark, city, postal code, region is being split and replaced to get data in required
        format
        :param item_num: Indicates item number
        """
        get_address_detail = None

        save_address_data, guid = self.get_address_dictionary(item_guid, header_guid, item_num, address_number,
                                                              street_output, area_output,
                                                              landmark_output, city_output, pcode_output,
                                                              region_output, item_flag, 'D')
        self.save_sc_data_to_db.save_address_to_db(guid, save_address_data)
        # save invoice address
        default_invoice_addr = \
            OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(self.object_id_list, CONST_INV_ADDR)[1]
        save_address_data, guid = self.get_address_dictionary(item_guid, header_guid, item_num, default_invoice_addr,
                                                              street_output, area_output,
                                                              landmark_output, city_output, pcode_output,
                                                              region_output, item_flag, 'I')
        self.save_sc_data_to_db.save_address_to_db(guid, save_address_data)

    def get_address_dictionary(self, item_guid, header_guid, item_num, address_number, street_output, area_output,
                               landmark_output, city_output, pcode_output, region_output, item_flag, addr_type):
        """

        """
        get_address_detail = None
        print(address_number)
        if not address_number:
            address_number = 0
        if django_query_instance.django_existence_check(OrgAddress,
                                                        {'address_number': address_number, 'client': self.client}):
            get_address_detail = django_query_instance.django_get_query(OrgAddress, {'address_number': address_number,
                                                                                     'client': self.client})

        if item_flag:
            item_guid = django_query_instance.django_get_query(ScItem, {'guid': item_guid, 'client': self.client,
                                                                        'del_ind': False})
            header_guid = None
        else:
            item_guid = None
            header_guid = django_query_instance.django_get_query(ScHeader, {'guid': header_guid, 'client': self.client,
                                                                            'del_ind': False})
            item_num = 0
        guid = guid_generator()
        save_address_data = {
            'guid': guid,
            'header_guid': header_guid,
            'item_guid': item_guid,
            'item_num': item_num,
            'client': django_query_instance.django_get_query(OrgClients, {'client': self.client, 'del_ind': False}),
            'title': None if get_address_detail is None else get_address_detail.title,
            'name1': None if get_address_detail is None else get_address_detail.name1,
            'name2': None if get_address_detail is None else get_address_detail.name2,
            'country_code': None if get_address_detail is None else get_address_detail.country_code,
            'language_id': None if get_address_detail is None else get_address_detail.language_id,
            'mobile_number': None if get_address_detail is None else get_address_detail.mobile_number,
            'telephone_number': None if get_address_detail is None else get_address_detail.telephone_number,
            'fax_number': None if get_address_detail is None else get_address_detail.fax_number,
            'email': None if get_address_detail is None else get_address_detail.email,
            'time_zone': None if get_address_detail is None else get_address_detail.time_zone,
            'address_partner_type': django_query_instance.django_get_query(AddressPartnerType,
                                                                           {'address_partner_type': '01'}),
            'address_type': addr_type
        }
        if addr_type == 'D':
            save_address_data['address_number'] = address_number
            save_address_data['street'] = street_output
            save_address_data['area'] = area_output
            save_address_data['landmark'] = landmark_output
            save_address_data['city'] = city_output
            save_address_data['postal_code'] = pcode_output
            save_address_data['region'] = region_output
        else:
            if get_address_detail:
                save_address_data['address_number'] = get_address_detail.address_number
                save_address_data['street'] = get_address_detail.street
                save_address_data['area'] = get_address_detail.area
                save_address_data['landmark'] = get_address_detail.landmark
                save_address_data['city'] = get_address_detail.city
                save_address_data['postal_code'] = get_address_detail.postal_code
                save_address_data['region'] = get_address_detail.region
            else:
                save_address_data['address_number'] = 0
                save_address_data['street'] = ''
                save_address_data['area'] = ''
                save_address_data['landmark'] = ''
                save_address_data['city'] = ''
                save_address_data['postal_code'] = ''
                save_address_data['region'] = ''

        return save_address_data, guid

    def get_purchasing_data(self, item_guid, co_code, prod_cat_id, item_num, header_guid, supplier_id):
        """
        :param header_guid:
        :param item_guid:
        :param co_code:
        :param prod_cat_id:
        :param item_num: Indicates item number
        :param supplier_id:
        :return:
        """
        org_porg_object_id = django_query_instance.django_filter_value_list_query(OrgModel, {
            'client': global_variables.GLOBAL_CLIENT, 'del_ind': False, 'node_type': CONST_PORG
        }, 'object_id')

        orgattr_porg_object_id = django_query_instance.django_filter_value_list_query(OrgAttributesLevel, {
            'attribute_id': CONST_CO_CODE, 'low': co_code, 'object_id__in': org_porg_object_id,
            'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
        }, 'object_id')

        purch_org_object_id_list = django_query_instance.django_filter_value_list_query(OrgPorg, {
            'object_id__in': orgattr_porg_object_id, 'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
        }, 'object_id')

        purch_org_det = django_query_instance.django_filter_only_query(OrgAttributesLevel, {
            'object_id__in': purch_org_object_id_list, 'client': self.client,
            'attribute_id': CONST_PROD_CAT, 'del_ind': False
        })

        for details in purch_org_det:
            object_id = details.object_id_id
            low = int(details.low)
            high = int(details.high) + 1
            incoterm_desc = ''
            if int(prod_cat_id) in range(int(low), int(high)):
                p_org = django_query_instance.django_get_query(OrgPorg, {
                    'object_id': object_id, 'client': self.client, 'del_ind': False
                })

                purch_group = django_query_instance.django_filter_value_list_query(OrgPGroup, {
                    'porg_id': p_org.porg_id, 'client': self.client, 'del_ind': False
                }, 'object_id')

                p_grp_det = django_query_instance.django_filter_only_query(OrgAttributesLevel, {
                    'object_id__in': purch_group, 'client': self.client,
                    'attribute_id': CONST_RESP_PROD_CAT, 'del_ind': False
                })
                for resp_prod_cat in p_grp_det:
                    p_grp_obj_id = resp_prod_cat.object_id
                    p_grp_low = int(resp_prod_cat.low)
                    p_grp_high = int(resp_prod_cat.high)
                    if int(prod_cat_id) in range(int(p_grp_low), int(p_grp_high) + 1):
                        p_group = django_query_instance.django_get_query(OrgPGroup, {
                            'object_id': p_grp_obj_id, 'client': self.client, 'del_ind': False
                        })
                        if supplier_id is not None:
                            if django_query_instance.django_existence_check(OrgSuppliers, {
                                'supplier_id': supplier_id, 'client': self.client,
                                'porg_id': p_org, 'del_ind': False
                            }):
                                get_supplier_org_info = django_query_instance.django_get_query(OrgSuppliers, {
                                    'supplier_id': supplier_id, 'client': self.client,
                                    'porg_id': p_org, 'del_ind': False
                                })

                                incoterm_key = get_supplier_org_info.incoterm_key
                                if django_query_instance.django_existence_check(Incoterms,
                                                                                {'incoterm_key': incoterm_key,
                                                                                 'del_ind': False}):
                                    incoterm = django_query_instance.django_get_query(Incoterms,
                                                                                      {'incoterm_key': incoterm_key,
                                                                                       'del_ind': False})
                                    incoterm_desc = incoterm.description
                                payment_term_key = get_supplier_org_info.payment_term_key
                                django_query_instance.django_filter_only_query(ScItem,
                                                                               {'guid': item_guid}).update(
                                    incoterm=str(incoterm_key),
                                    incoterm_loc=incoterm_desc,
                                    payment_term=str(payment_term_key),
                                    purch_org=str(p_org))
                        guid = guid_generator()
                        save_purchasing_data = {
                            'purch_guid': guid_generator(),
                            'sc_header_guid': django_query_instance.django_get_query(ScHeader, {'guid': header_guid}),
                            'sc_item_guid': django_query_instance.django_get_query(ScItem, {'guid': item_guid}),
                            'prod_cat': prod_cat_id,
                            'comp_code': co_code,
                            'purch_org': p_org,
                            'purch_grp': p_group,
                            'client': django_query_instance.django_get_query(OrgClients,
                                                                             {'client': self.client, 'del_ind': False}),
                            'item_num': item_num
                        }
                        self.save_sc_data_to_db.save_purchasing_data(guid, save_purchasing_data)

    # Method to save notes data (Approval or internal or supplier notes)
    def save_notes_data(self, counter, item_guid, item_num):
        """
        :param counter: Counter is used to access keys from a query set to extract data
        :param item_guid: Item guid
        :param item_num: Indicates item number
        :return:
        """
        incremented_counter = str(int(counter) + 1)
        supplier_text_id = 'supplier_note' + incremented_counter
        supplier_text_data = self.sc_ui_data[supplier_text_id]
        internal_text_id = 'internal_note' + incremented_counter
        internal_text_data = self.sc_ui_data[internal_text_id]

        if counter == 0:
            approval_note = self.approver_text
            save_approval_note(counter, self.client, self.header_guid, self.doc_number, approval_note)

        # Saving of supplier text
        save_internal_supplier_note(self.client, item_guid, self.doc_number, item_num, CONST_SUPPLIER_NOTE,
                                    supplier_text_data)

        # Saving of internal note

        save_internal_supplier_note(self.client, item_guid, self.doc_number, item_num, CONST_INTERNAL_NOTE,
                                    internal_text_data)

    # Method to save attachment data for items in the cart
    def save_attachments(self, counter, item_guid, item_num, doc_number):
        """
        :param doc_number:
        :param counter: Counter is used to access keys from a query set to extract data
        :param item_guid: Item guid
        :param item_num:
        :return:
        """
        incremented_counter = str(int(counter) + 1)
        if 'no_attachments' + incremented_counter in self.sc_ui_data:
            last_available_attachment = int(self.sc_ui_data['last_index_attachments' + incremented_counter])
            no_attachments_available = int(self.sc_ui_data['no_attachments' + incremented_counter])
            if no_attachments_available > 0:
                c = 1
                while c <= last_available_attachment:
                    attachment_id = 'attachment' + incremented_counter + '_' + str(c)
                    try:
                        attachment_data = self.attachments_data[attachment_id]
                    except MultiValueDictKeyError:
                        attachment_data = 'No attachments available'

                    if attachment_data != 'No attachments available':
                        doc_format = self.sc_ui_data['file_extension' + incremented_counter + '_' + str(c)]
                        attachment_name = self.sc_ui_data['attachment_name' + incremented_counter]
                        attach_type = self.sc_ui_data['attachment_type' + incremented_counter]
                        if attach_type == 'Internal Use':
                            attachment_type = 'I'
                        else:
                            attachment_type = 'E'

                        save_attachment_data(self.header_guid, doc_number, attachment_name,
                                             attachment_data, attachment_type, doc_format, item_guid, item_num)
                    c += 1
                    if c > last_available_attachment:
                        break


class EditShoppingCart(SaveShoppingCart):
    def __init__(self, request):
        self.save_sc_data_to_db = SaveSoppingCartDataToDb()
        SaveShoppingCart.__init__(self, request, sc_header_guid='',
                                  sc_ui_data={'acc_assign_cat': '', 'acc_assign_val': '', 'approver_text': '',
                                              'requester': ''},
                                  attachments_data='', save_type='Edit')

    def add_item_to_saved_cart(self, header_guid, item_data):
        supplier_id = None
        gl_acc_num_detail = None
        if supplier_id in item_data:
            supplier_id = item_data['supplier_id']

        sc_instance = django_query_instance.django_get_query(ScHeader, {'guid': header_guid, 'client': self.client})

        document_number = sc_instance.doc_number
        requester = sc_instance.requester
        eform_guid = None
        eform = False
        if item_data['call_off'] == CONST_FREETEXT_CALLOFF:
            eform_guid = item_data.get("guid")
            eform = item_data.get('eform')
        value = item_data.get('value')
        sc_instance.total_value = float(sc_instance.total_value) + float(value)
        sc_instance.save()

        item_details = django_query_instance.django_filter_only_query(ScItem, {'header_guid': header_guid,
                                                                               'client': self.client,
                                                                               'del_ind': False})
        get_item_num = item_details.aggregate(Max('item_num'))
        item_num = list(get_item_num.values())[0] + 1
        get_item_guid = item_details.values_list('guid', flat=True)
        get_silent_po = item_details.values_list('silent_po', flat=True)
        item_guid = get_item_guid[0]
        new_item_guid = guid_generator()
        item_data['guid'] = new_item_guid
        item_data['item_num'] = item_num
        save_sc_data_to_db = SaveSoppingCartDataToDb()
        prod_cat_id = item_data['prod_cat_id']
        item_data['prod_cat_desc'] = get_prod_by_id(prod_cat_id)
        item_data['comp_code'] = self.company_code
        item_data['bill_to_addr_num'] = self.invoice_address
        item_data['ship_to_addr_num'] = self.ship_addr_num
        item_data['created_by'] = self.username
        item_data['goods_recep'] = self.username
        item_data['silent_po'] = get_silent_po[0]
        save_sc_data_to_db.save_sc_item_details_to_db(new_item_guid, item_data)

        get_address_data = django_query_instance.django_get_query(ScAddresses,
                                                                  {'header_guid': header_guid,
                                                                   'client': self.client,
                                                                   'del_ind': False,
                                                                   'address_type': 'D'})
        get_accounting_data = django_query_instance.django_get_query(ScAccounting,
                                                                     {'header_guid': header_guid,
                                                                      'client': self.client,
                                                                      'del_ind': False})
        address_guid = guid_generator()
        accounting_guid = guid_generator()

        address_data = {
            'guid': address_guid,
            'item_guid': django_query_instance.django_get_query(ScItem, {'guid': new_item_guid, 'del_ind': False}),
            'item_num': item_num,
            'address_number': get_address_data.address_number,
            'street': get_address_data.street,
            'area': get_address_data.area,
            'landmark': get_address_data.landmark,
            'city': get_address_data.city,
            'postal_code': get_address_data.postal_code,
            'region': get_address_data.region,
            'client': get_address_data.client,
            'address_type': 'D'
        }
        det_default_gl_acc_filter_dict = {
            'client': global_variables.GLOBAL_CLIENT,
            'prod_cat_id': prod_cat_id,
            'account_assign_cat': get_accounting_data.acc_cat,
            'item_from_value__lt': int(value),
            'item_to_value__gt': int(value),
            'company_id': self.company_code,
            'currency_id': global_variables.GLOBAL_USER_CURRENCY,
            'gl_acc_default': True,
            'del_ind': False
        }
        if DjangoQueries.django_existence_check(DetermineGLAccount, det_default_gl_acc_filter_dict):
            gl_acc_num_detail = DjangoQueries.django_filter_value_list_query(DetermineGLAccount,
                                                                             det_default_gl_acc_filter_dict,
                                                                             'gl_acc_num')[0]
        accounting_data = {
            'guid': accounting_guid,
            'client': django_query_instance.django_get_query(OrgClients, {'client': self.client, 'del_ind': False}),
            'item_guid': django_query_instance.django_get_query(ScItem,
                                                                {'guid': new_item_guid, 'client': self.client,
                                                                 'del_ind': False}),
            'acc_item_num': item_num,
            'dist_perc': '100',  # Hardcoded
            'gl_acc_num': gl_acc_num_detail,
            'acc_cat': get_accounting_data.acc_cat,
            'ref_date': get_accounting_data.ref_date,
            'cost_center': get_accounting_data.cost_center,
            'internal_order': get_accounting_data.internal_order,
            'wbs_ele': get_accounting_data.wbs_ele,
            'asset_number': get_accounting_data.asset_number
        }

        # Saving of supplier text
        save_internal_supplier_note(self.client, new_item_guid, document_number, item_num, CONST_SUPPLIER_NOTE,
                                    '')

        # Saving of internal note
        save_internal_supplier_note(self.client, new_item_guid, document_number, item_num, CONST_INTERNAL_NOTE,
                                    '')

        if eform:
            update_eform = django_query_instance.django_filter_only_query(EformFieldData, {'cart_guid': eform_guid})
            update_eform.update(item_guid=django_query_instance.django_get_query(ScItem, {'guid': new_item_guid,
                                                                                          'item_num': item_num}))
        self.save_sc_data_to_db.save_address_to_db(guid=address_guid, save_address_data=address_data)
        invoice_address_data = {
            'guid': guid_generator(),
            'item_guid': django_query_instance.django_get_query(ScItem, {'guid': new_item_guid, 'del_ind': False}),
            'item_num': item_num,
            'address_number': get_address_data.address_number,
            'street': get_address_data.street,
            'area': get_address_data.area,
            'landmark': get_address_data.landmark,
            'city': get_address_data.city,
            'postal_code': get_address_data.postal_code,
            'region': get_address_data.region,
            'client': get_address_data.client,
            'address_type': 'I'
        }
        self.save_sc_data_to_db.save_address_to_db(guid=address_guid, save_address_data=invoice_address_data)
        self.save_sc_data_to_db.save_accounting_data(guid=accounting_guid, sc_acc_save_data=accounting_data)
        SaveShoppingCart.get_purchasing_data(self, item_guid=new_item_guid, co_code=self.company_code,
                                             prod_cat_id=prod_cat_id, item_num=item_num, header_guid=header_guid,
                                             supplier_id=supplier_id)

        value_of_sc = django_query_instance.django_filter_value_list_without_query(ScItem, {'header_guid': header_guid,
                                                                                            'del_ind': False}, 'value')
        total_value = sum(value_of_sc)
        django_query_instance.django_filter_only_query(ScHeader, {
            'guid': header_guid}).update(total_value=sc_instance.total_value, gross_amount=sc_instance.total_value)

        account_assignment_category, account_assignment_value = get_highest_acc_detail(header_guid)
        approval_data = get_manger_detail(self.client, requester,
                                          account_assignment_category, sc_instance.total_value, sc_instance.co_code,
                                          account_assignment_value,
                                          global_variables.GLOBAL_USER_CURRENCY)
        # Save Approver detail
        delete_approver_detail(header_guid)
        sc_completion_flag = False
        if django_query_instance.django_existence_check(ScItem, {'client': global_variables.GLOBAL_CLIENT,
                                                                 'del_ind': False,
                                                                 'header_guid': header_guid,
                                                                 'call_off': CONST_PR_CALLOFF}):
            sc_completion_flag = True
        save_sc_approval(approval_data[0], header_guid, CONST_SC_HEADER_SAVED, sc_completion_flag)
        # end of save Approver detail
        # purch_worklist_flag = False
        # if item_data['call_off'] == CONST_PR_CALLOFF:
        #     purch_worklist_flag = True
        # save_sc_approval(approval_data[0], header_guid, CONST_SC_HEADER_SAVED, purch_worklist_flag)
        return True, new_item_guid

    def delete_item_from_sc(self, del_item_guid, total_value, header_guid):
        django_query_instance.django_filter_delete_query(EformFieldData,
                                                         {'item_guid': del_item_guid,
                                                          'client': self.client})
        django_query_instance.django_filter_delete_query(PurchasingData,
                                                         {'sc_item_guid': del_item_guid,
                                                          'client': self.client})
        django_query_instance.django_filter_delete_query(Attachments, {'item_guid': del_item_guid,
                                                                       'client': self.client})
        django_query_instance.django_filter_delete_query(Notes, {'item_guid': del_item_guid,
                                                                 'client': self.client})
        django_query_instance.django_filter_delete_query(ScAccounting, {'item_guid': del_item_guid,
                                                                        'client': self.client})
        django_query_instance.django_filter_delete_query(ScAddresses, {'item_guid': del_item_guid,
                                                                       'client': self.client})
        django_query_instance.django_filter_delete_query(ScItem, {'guid': del_item_guid,
                                                                  'client': self.client})
        #
        #
        #
        # django_query_instance.django_filter_only_query(EformData, {'item_guid': del_item_guid,
        #                                                            'client': self.client})
        # django_query_instance.django_filter_only_query(EformFieldData, {'item_guid': del_item_guid,
        #                                                            'client': self.client})
        #
        #
        # django_query_instance.django_filter_only_query(PurchasingData, {'sc_item_guid': del_item_guid,
        #                                                                 'client': self.client}).update(del_ind=True)
        #
        # django_query_instance.django_filter_only_query(Attachments, {'item_guid': del_item_guid,
        #                                                              'client': self.client}).update(del_ind=True)
        #
        # django_query_instance.django_filter_only_query(Notes, {'item_guid': del_item_guid,
        #                                                        'client': self.client}).update(del_ind=True)
        #
        # django_query_instance.django_filter_only_query(ScAccounting, {'item_guid': del_item_guid,
        #                                                               'client': self.client}).update(del_ind=True)
        #
        # django_query_instance.django_filter_only_query(ScAddresses, {'item_guid': del_item_guid,
        #                                                              'client': self.client}).update(del_ind=True)
        #
        # django_query_instance.django_filter_only_query(EformData, {'item_guid': del_item_guid,
        #                                                            'client': self.client}).update(del_ind=True)
        sc_item_price = django_query_instance.django_filter_value_list_ordered_by_distinct_query(ScItem,
                                                                                                 {
                                                                                                     'header_guid': header_guid,
                                                                                                     'client': self.client,
                                                                                                     'del_ind': False},
                                                                                                 'value',
                                                                                                 None)
        # sc_item = django_query_instance.django_filter_only_query(ScItem, {
        #     'guid': del_item_guid, 'client': self.client, 'del_ind': False
        # })
        # item_value = list(sc_item.values_list('value', flat=True))[0]
        # sc_item.update(del_ind=True)
        # updated_total_value = float(total_value) - float(item_value)
        sc_total = sum(sc_item_price)
        django_query_instance.django_filter_only_query(ScHeader, {
            'guid': header_guid, 'client': self.client
        }).update(total_value=sc_total, gross_amount=sc_total)

        count = django_query_instance.django_filter_count_query(ScItem, {'header_guid': header_guid, 'del_ind': False})
        if count == 0:
            django_query_instance.django_filter_delete_query(PurchasingData,
                                                             {'sc_header_guid': header_guid,
                                                              'client': self.client,
                                                              'del_ind': False})
            django_query_instance.django_filter_delete_query(ChatContent,
                                                             {'sc_header_guid': header_guid,
                                                              'client': self.client,
                                                              'del_ind': False})
            django_query_instance.django_update_query(ScHeader,
                                                      {'guid': header_guid,
                                                       'client': self.client,
                                                       'del_ind': False}, {'status': CONST_SC_HEADER_DELETED})
            # django_query_instance.django_filter_only_query(ScApproval, {
            #     'header_guid': header_guid, 'client': self.client
            # }).update(del_ind=True)
            #
            # django_query_instance.django_filter_only_query(ScAccounting, {
            #     'header_guid': header_guid, 'client': self.client
            # }).update(del_ind=True)
            #
            # django_query_instance.django_filter_only_query(ScAddresses, {
            #     'header_guid': header_guid, 'client': self.client
            # }).update(del_ind=True)
            #
            # django_query_instance.django_filter_only_query(ScHeader, {
            #     'guid': header_guid, 'client': self.client
            # }).update(del_ind=True)

        return sc_total, count

    def delete_sc(self, header_guid):
        item_guid = django_query_instance.django_filter_only_query(ScItem, {
            'header_guid': header_guid, 'client': self.client, 'del_ind': False
        })
        for data in item_guid:
            django_query_instance.django_filter_only_query(PurchasingData, {
                'sc_item_guid': data.guid, 'client': self.client
            }).update(del_ind=True)

            django_query_instance.django_filter_only_query(Attachments, {
                'item_guid': data.guid, 'client': self.client
            }).update(del_ind=True)

            django_query_instance.django_filter_only_query(Notes, {
                'item_guid': data.guid, 'client': self.client
            }).update(del_ind=True)

            django_query_instance.django_filter_only_query(ScAccounting, {
                'item_guid': data.guid, 'client': self.client
            }).update(del_ind=True)

            django_query_instance.django_filter_only_query(ScAddresses, {
                'item_guid': data.guid, 'client': self.client
            }).update(del_ind=True)

            django_query_instance.django_filter_only_query(EformFieldData, {
                'item_guid': data.guid, 'client': self.client
            }).update(del_ind=True)

            django_query_instance.django_filter_only_query(ScItem, {
                'guid': data.guid, 'client': self.client
            }).update(del_ind=True)

        hdr_guid = django_query_instance.django_filter_only_query(ScApproval, {
            'header_guid': header_guid, 'client': self.client, 'del_ind': False
        })
        for approval in hdr_guid:
            django_query_instance.django_filter_only_query(ScApproval, {
                'header_guid': approval.guid, 'client': self.client
            }).update(del_ind=True)

        django_query_instance.django_filter_only_query(ScHeader, {'guid': header_guid,
                                                                  'client': self.client}).update(del_ind=True)

        return '', ''


class SaveSoppingCartDataToDb:
    @staticmethod
    def save_header_to_db(header_guid, sc_header_save_data):
        django_query_instance.django_update_or_create_query(ScHeader, {'guid': header_guid}, sc_header_save_data)

    @staticmethod
    def save_sc_item_details_to_db(item_guid, sc_item_details):
        django_query_instance.django_update_or_create_query(ScItem, {'guid': item_guid}, sc_item_details)

    @staticmethod
    def save_accounting_data(guid, sc_acc_save_data):
        django_query_instance.django_update_or_create_query(ScAccounting, {'guid': guid}, sc_acc_save_data)

    @staticmethod
    def save_address_to_db(guid, save_address_data):
        django_query_instance.django_update_or_create_query(ScAddresses, {'guid': guid}, save_address_data)

    @staticmethod
    def save_purchasing_data(guid, save_purchasing_data):
        django_query_instance.django_update_or_create_query(PurchasingData, {'purch_guid': guid}, save_purchasing_data)


class CheckForScErrors:
    def __init__(self, client, username):
        self.client = client
        self.data = []
        self.addr_error = []
        self.info = []
        self.sc_check_data = {}
        self.username = username
        self.error_message_info = []

    def invoice_address_check(self, address_number, company_code):
        """

        """
        error_msg = ''
        if address_number == 'None' or address_number is None or address_number == '':
            error_msg = 'Default invoice address is not maintained please contact your admin'
            self.error_message_info.append(error_msg)
            return error_msg
        check_for_address_number_map = django_query_instance.django_existence_check(OrgAddressMap,
                                                                                    {'client': self.client,
                                                                                     'del_ind': False,
                                                                                     'address_type': 'I',
                                                                                     'address_number': address_number,
                                                                                     'company_id': company_code})
        check_for_address_number = django_query_instance.django_existence_check(OrgAddress, {
            'client': self.client, 'del_ind': False, 'address_number': address_number
        })

        if not check_for_address_number and check_for_address_number_map:
            error_msg = 'Invoice address is not valid'
            self.error_message_info.append(error_msg)
            return error_msg
        else:
            return error_msg

    def header_level_delivery_address_check(self, address_number, company_code, address_number_list, check_flag):
        error_msg = None
        if check_flag:
            if len(address_number_list) == 0:
                error_msg = get_message_desc('MSG203')[1]
                self.error_message_info.append(error_msg)
                return error_msg
        if address_number == 'None' or address_number is None or address_number == '':
            error_msg = get_message_desc('MSG163')[1]
            self.error_message_info.append(error_msg)
            return error_msg
        check_for_address_number_map = django_query_instance.django_existence_check(OrgAddressMap,
                                                                                    {'client': self.client,
                                                                                     'del_ind': False,
                                                                                     'address_type': 'D',
                                                                                     'address_number': address_number,
                                                                                     'company_id': company_code})
        check_for_address_number = django_query_instance.django_existence_check(OrgAddress, {
            'client': self.client, 'del_ind': False, 'address_number': address_number
        })

        if not check_for_address_number and check_for_address_number_map:
            error_msg = get_message_desc('MSG162')[1]
            self.error_message_info.append(error_msg)
            return error_msg
        else:
            return error_msg

    def item_level_delivery_address_check(self, address_number, item_num):
        error_msg = None
        address_error = {}
        if address_number == 'None' or address_number is None or address_number == '':
            error_msg = get_message_desc('MSG204')[1]
            address_error[item_num] = error_msg
            self.data.append(address_error)
            return error_msg

        check_for_address_number = django_query_instance.django_existence_check(OrgAddress, {
            'client': self.client, 'del_ind': False, 'address_number': address_number
        })

        if not check_for_address_number:
            error_msg = get_message_desc('MSG162')[1]
            address_error[item_num] = error_msg
            self.data.append(address_error)
            return error_msg
        else:
            return error_msg

    def item_level_delivery_address_first_check(self, cart_items_count, error_msg):
        """

        """
        address_error = {}
        item_num = 1
        cart_count = cart_items_count
        while item_num <= cart_count:
            address_error[item_num] = error_msg
            item_num = item_num + 1
        self.data.append(address_error)

    def delivery_address_check(self, address_number, item_num):
        address_error = {}

        if address_number == 'None' or address_number is None or address_number == '':
            msgid = 'MSG162'
            error_msg = get_message_desc(msgid)[1]
            address_error[item_num] = error_msg
            self.data.append(address_error)
            return False, self.data
        msgid = 'MSG163'
        error_msg = get_message_desc(msgid)[1]

        if len(address_number) == 0:
            address_error[item_num] = error_msg
            self.data.append(address_error)
            return False, self.data

        check_for_address_number = django_query_instance.django_existence_check(OrgAddress, {
            'client': self.client, 'del_ind': False, 'address_number': address_number
        })
        msgid = 'MSG162'
        error_msg = get_message_desc(msgid)[1]

        if not check_for_address_number:
            address_error[item_num] = error_msg
            self.data.append(address_error)
            return False, self.data
        else:
            return True, ''

    def header_acc_check(self, acc, acc_val, acc_desc_list, company_code):
        """"
        """
        if len(acc_desc_list) == 0:
            error_msg = "Account assignment category is not maintained. Please contact admin"
            self.error_message_info.append(error_msg)
        if not acc:
            error_msg = "Please select relevant account assignment category"
            self.error_message_info.append(error_msg)
        else:
            if not django_query_instance.django_existence_check(AccountingData,
                                                                {'account_assign_cat': acc,
                                                                 'account_assign_value': acc_val,
                                                                 'client': self.client,
                                                                 'del_ind': False,
                                                                 'company_id': company_code}):
                msgid = 'MSG165'
                errormsg = get_message_desc(msgid)[1]
                self.error_message_info.append(errormsg)
            if not django_query_instance.django_existence_check(AccountAssignmentCategory,
                                                                {'account_assign_cat': acc,
                                                                 'del_ind': False}):
                msgid = 'MSG166'
                errormsg = get_message_desc(msgid)[1]
                self.error_message_info.append(errormsg)
        if not acc_val:
            error_msg = "Please select relevant account assignment category value"
            self.error_message_info.append(error_msg)

    def item_level_acc_check(self, acc, acc_val, acc_desc_list, gl_acc_num, company_code, item_num):
        """

        """
        account_assignment_errors = {}
        if len(acc_desc_list) == 0:
            account_assignment_errors = {}
            error_msg = "Account assignment category is not maintained. Please contact admin"
            account_assignment_errors[item_num] = error_msg
            self.data.append(account_assignment_errors)
        if not acc:
            account_assignment_errors = {}
            error_msg = "Please select relevant account assignment category"
            account_assignment_errors[item_num] = error_msg
            self.data.append(account_assignment_errors)
        else:
            if not django_query_instance.django_existence_check(AccountingData,
                                                                {'account_assign_cat': acc,
                                                                 'account_assign_value': acc_val,
                                                                 'client': self.client,
                                                                 'del_ind': False,
                                                                 'company_id': company_code}):
                account_assignment_errors = {}
                msgid = 'MSG165'
                error_msg = get_message_desc(msgid)[1]
                account_assignment_errors[item_num] = error_msg
                self.data.append(account_assignment_errors)
            if not django_query_instance.django_existence_check(AccountAssignmentCategory,
                                                                {'account_assign_cat': acc,
                                                                 'del_ind': False}):
                account_assignment_errors = {}
                msgid = 'MSG166'
                error_msg = get_message_desc(msgid)[1]
                account_assignment_errors[item_num] = error_msg
                self.data.append(account_assignment_errors)
        if not acc_val:
            account_assignment_errors = {}
            error_msg = "Please select relevant account assignment category value"
            account_assignment_errors[item_num] = error_msg
            self.data.append(account_assignment_errors)
        if not django_query_instance.django_existence_check(DetermineGLAccount,
                                                            {'account_assign_cat': acc,
                                                             'gl_acc_num': gl_acc_num,
                                                             'del_ind': False,
                                                             'client': self.client}):
            account_assignment_errors = {}
            error_msg = get_message_desc('MSG164')[1]
            account_assignment_errors[item_num] = error_msg
            self.data.append(account_assignment_errors)

    def header_level_acc_check(self, acc_list, default_acc, acc_value_list, default_acc_value, company_code):
        """

        """
        if default_acc:
            if not django_query_instance.django_existence_check(AccountAssignmentCategory,
                                                                {'account_assign_cat': default_acc,
                                                                 'del_ind': False}):
                msgid = 'MSG166'
                errormsg = get_message_desc(msgid)[1]
                self.error_message_info.append(errormsg)

        else:
            error_msg = "No default Account assignment category maintained.Please maintain defaults in Purchase settings"
            self.error_message_info.append(error_msg)
        if default_acc_value:
            if not django_query_instance.django_existence_check(AccountingData,
                                                                {'account_assign_cat': default_acc,
                                                                 'account_assign_value': default_acc_value,
                                                                 'client': self.client,
                                                                 'del_ind': False,
                                                                 'company_id': company_code}):
                msgid = 'MSG165'
                errormsg = get_message_desc(msgid)[1]
                self.error_message_info.append(errormsg)
        else:
            error_msg = "No default Account assignment category value maintained.Please maintain defaults in Purchase " \
                        "settings "
            self.error_message_info.append(error_msg)
        if len(acc_list) == 0:
            error_msg = "Account assignment category is not maintained. Please contact admin"
            self.error_message_info.append(error_msg)
        if len(acc_value_list) == 0:
            error_msg = "Account assignment category value is not maintained. Please contact admin"
            self.error_message_info.append(error_msg)

    def account_assignment_check(self, acc_assign_cat, acc_assign_value, gl_acc_num, item_num):
        account_assignment_errors = {}
        check_for_acc_assign_cat = django_query_instance.django_existence_check(AccountAssignmentCategory, {
            'account_assign_cat': acc_assign_cat, 'del_ind': False
        })

        if check_for_acc_assign_cat:
            check_for_acc_assign_val = django_query_instance.django_existence_check(AccountingDataDesc, {
                'account_assign_cat': acc_assign_cat, 'account_assign_value': acc_assign_value,
                'client': self.client, 'del_ind': False
            })

            check_for_gl_acc_num = django_query_instance.django_existence_check(DetermineGLAccount, {
                'account_assign_cat': acc_assign_cat, 'gl_acc_num': gl_acc_num,
                'del_ind': False, 'client': self.client
            })

            msgid = 'MSG164'
            error_msg = get_message_desc(msgid)[1]

            msgid = 'MSG165'
            error_msg1 = get_message_desc(msgid)[1]

            if not check_for_gl_acc_num:
                account_assignment_errors[item_num] = error_msg
                self.data.append(account_assignment_errors)
                return False, self.data

            elif not check_for_acc_assign_val:
                account_assignment_errors[item_num] = error_msg1
                self.data.append(account_assignment_errors)
                return False, self.data

            else:
                return True, ''

        else:
            msgid = 'MSG166'
            errormsg = get_message_desc(msgid)[1]

            account_assignment_errors[item_num] = errormsg
            self.data.append(account_assignment_errors)
            return False, self.data

    def check_for_prod_cat(self, prod_id, co_code, item_num):
        is_purchase_organisation = False
        is_purchase_group = False
        prod_cat_errors = {}
        co_code_list = ['ALL', co_code]

        org_porg_object_id = django_query_instance.django_filter_value_list_query(OrgModel, {
            'client': global_variables.GLOBAL_CLIENT, 'del_ind': False, 'node_type': CONST_PORG
        }, 'object_id')

        purch_org_object_id_list = django_query_instance.django_filter_value_list_query(OrgPorgMapping,
                                                                                        {'company_id': co_code,
                                                                                         'client': global_variables.GLOBAL_CLIENT,
                                                                                         'del_ind': False},
                                                                                        'object_id')
        # orgattr_porg_object_id = django_query_instance.django_filter_value_list_query(OrgAttributesLevel, {
        #     'attribute_id': CONST_CO_CODE, 'low': co_code, 'object_id__in': org_porg_object_id,
        #     'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
        # }, 'object_id')
        #
        # purch_org_object_id_list = django_query_instance.django_filter_value_list_query(OrgPorg, {
        #     'object_id__in': orgattr_porg_object_id, 'client': global_variables.GLOBAL_CLIENT,
        #     'del_ind': False
        # }, 'object_id')

        purch_org_det = django_query_instance.django_filter_only_query(OrgAttributesLevel, {
            'object_id__in': purch_org_object_id_list, 'extended_value__in': co_code_list,
            'client': self.client, 'attribute_id': CONST_PROD_CAT, 'del_ind': False
        })

        if purch_org_det.count() > 0:
            for low_high in purch_org_det:
                if int(prod_id) in range(int(low_high.low), int(low_high.high) + 1):
                    is_purchase_organisation = True

        if is_purchase_organisation:
            get_purchase_org_id = django_query_instance.django_filter_value_list_query(OrgPorg, {
                'object_id__in': purch_org_object_id_list, 'client': global_variables.GLOBAL_CLIENT,
                'del_ind': False
            }, 'porg_id')

            purchase_grp_obj_id_list = django_query_instance.django_filter_value_list_query(OrgPGroup, {
                'client': self.client, 'porg_id__in': get_purchase_org_id, 'del_ind': False
            }, 'object_id')

            get_pgrp_prod_cat_det = django_query_instance.django_filter_only_query(OrgAttributesLevel, {
                'object_id__in': purchase_grp_obj_id_list, 'client': self.client,
                'extended_value__in': co_code_list, 'attribute_id': CONST_RESP_PROD_CAT, 'del_ind': False
            })

            for product_categories in get_pgrp_prod_cat_det:
                if int(prod_id) in range(int(product_categories.low), int(product_categories.high) + 1):
                    return True, ''

        if not is_purchase_group:
            prod_cat_errors[item_num] = f'Product category {prod_id} is not assigned to any purchasing group'
            self.data.append(prod_cat_errors)
            return False, self.data

        prod_cat_errors[item_num] = f'Product category {prod_id} is not assigned to any purchase organisation'
        self.data.append(prod_cat_errors)
        return False, self.data

    def check_for_supplier(self, supplier_id, product_category, company_code, item_num):
        """
        :param supplier_id:
        :param product_category:
        :param company_code:
        :param item_num:
        :return:
        """
        check_supplier_error = {}
        filter_supplier_query = django_query_instance.django_filter_only_query(OrgSuppliers, {
            'client': self.client, 'del_ind': False, 'supplier_id': supplier_id
        })

        if not filter_supplier_query.exists():
            if supplier_id != 'None':
                check_supplier_error[item_num] = f'Supplier {supplier_id} is not assigned to any organisations'
                self.data.append(check_supplier_error)
                return False, self.data

        check_supplier_org_info = filter_supplier_query.values_list('porg_id', flat=True)

        for porgs in check_supplier_org_info:
            supplier_filter_porg = django_query_instance.django_filter_only_query(OrgSuppliers, {
                'client': self.client, 'del_ind': False, 'supplier_id': supplier_id, 'porg_id': porgs
            })[0]

            incoterm = supplier_filter_porg.incoterm_key
            payterm = supplier_filter_porg.payment_term_key

            if incoterm is None or incoterm == '' or payterm is None or payterm == '':
                check_supplier_error[item_num] = f'Please maintain incoterm and payterms for supplier {supplier_id}'
                self.data.append(check_supplier_error)
                return False, self.data

            if porgs == '' and porgs is None:
                check_supplier_error[item_num] = f'Supplier {supplier_id} is not assigned to any purchase organisations'
                self.data.append(check_supplier_error)
                return False, self.data

        return True, ''

    def approval_check(self, acc_default, acc_default_val, total_val, company_code):
        """
        :param acc_default:
        :param acc_default_val:
        :param total_val:
        :param company_code:
        :return:
        """
        manager_detail, error_message = get_manger_detail(self.client, self.username, acc_default, total_val,
                                                          company_code, acc_default_val,
                                                          global_variables.GLOBAL_USER_CURRENCY)
        manager_details, approver_id = get_users_first_name(manager_detail)
        self.sc_check_data['total_value'] = total_val
        self.sc_check_data['manager_detail'] = manager_details
        self.sc_check_data['approver_id'] = approver_id
        if error_message:
            self.sc_check_data['msg_info'] = error_message

    def update_approval_check(self, manager_details, approver_id, total_value,
                              msg_info):
        """
        :param acc_default:
        :param acc_default_val:
        :param total_val:
        :param company_code:
        :return:
        """
        self.sc_check_data['total_value'] = total_value
        self.sc_check_data['manager_detail'] = manager_details
        self.sc_check_data['approver_id'] = approver_id
        if msg_info:
            self.sc_check_data['msg_info'] = msg_info

    def catalog_item_check(self, product_id, price, lead_time, item_num, item_guid, quantity):
        check_catalog_errors = {}

        get_product_detail = django_query_instance.django_get_query(ProductsDetail, {
            'product_id': product_id, 'client': self.client, 'del_ind': False
        })
        if get_product_detail.variant_id:
            pricing_list = [CONST_VARIANT_BASE_PRICING, CONST_VARIANT_ADDITIONAL_PRICING, CONST_QUANTITY_BASED_DISCOUNT]
            if django_query_instance.django_existence_check(VariantConfig,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'del_ind': False,
                                                             'variant_id': get_product_detail.variant_id,
                                                             'dropdown_pricetype__in': pricing_list}):
                current_price, discount_percentage, base_price, additional_pricing = calculate_item_price(item_guid,
                                                                                                          quantity)
            else:
                current_price = get_product_detail.price
        else:
            current_price = get_product_detail.price
        current_lead_time = get_product_detail.lead_time
        if int(current_lead_time) != int(lead_time):
            check_catalog_errors[item_num] = f'Lead time of an item has changed since the last time you added'
            self.data.append(check_catalog_errors)
            return False, self.data

        if float(current_price) != float(price):
            check_catalog_errors[item_num] = f'Price of an item has changed since the last time you added'
            self.data.append(check_catalog_errors)
            return False, self.data

    def document_sc_transaction_check(self, object_id_list):
        document_number_errors = {}
        document_number = generate_document_number(CONST_SC_TRANS_TYPE, self.client, object_id_list, False,
                                                   CONST_DOC_TYPE_SC)
        if not document_number[0]:
            document_number_errors['0'] = document_number[1]
            self.data.append(document_number_errors)
            return False, self.data

    def po_transaction_check(self, object_id_list):
        document_number_errors = {}
        po_transaction_type = get_attr_value(self.client, CONST_PO_TRANS_TYPE, object_id_list, False)
        if len(po_transaction_type) == 0:
            msgid = 'MSG192'
            error_msg = get_message_desc(msgid)[1]

            document_number_errors['0'] = error_msg
            self.data.append(document_number_errors)
            return False, self.data

    def calender_id_check(self, calendar_id):
        calendar_error = {}
        msgid = 'MSG167'
        errormsg = get_message_desc(msgid)[1]

        if calendar_id == '' or calendar_id is None:
            calendar_error['0'] = errormsg
            self.data.append(calendar_error)
            return False, self.data

    def delivery_date_check(self, delivery_date, item_number, holiday_list, calendar_id):
        delivery_date_error = {}
        delivery_date_info = {}

        if len(holiday_list) == 0:
            if item_number == 1:
                delivery_date_error[
                    '0'] = f'Holidays has not configured for the calendar {calendar_id}. Please Contact Your Admin'
                self.data.append(delivery_date_error)
                return False, self.data
        msgid = 'MSG168'
        error_msg = get_message_desc(msgid)[1]

        if delivery_date is None:
            delivery_date_error[item_number] = error_msg
            self.data.append(delivery_date_error)
            return False, self.data
            msgid = 'MSG160'
            error_msg = get_message_desc(msgid)[1]

        if delivery_date in holiday_list:
            delivery_date_info[item_number] = error_msg
            self.info.append(delivery_date_info)
        msgid = 'MSG170'
        error_msg = get_message_desc(msgid)[1]

        if delivery_date is None:
            delivery_date_error[item_number] = error_msg
            self.data.append(delivery_date_error)
            return False, self.data

        else:
            current_date = datetime.date.today()
            msgid = 'MSG171'
            error_msg = get_message_desc(msgid)[1]

            if delivery_date < current_date:
                delivery_date_error[item_number] = error_msg
                self.data.append(delivery_date_error)
                return False, self.data

    def check_for_currency(self, item_number, is_converted, currency):
        currency_error = {}
        if not is_converted:
            currency_error[item_number] = f'{currency} is not a valid currency'
            self.data.append(currency_error)
            return False, self.data

    def get_shopping_cart_errors(self):
        self.sc_check_data['sc_error'] = self.data
        self.sc_check_data['error_msg_info'] = self.error_message_info
        self.sc_check_data['sc_info'] = self.info
        self.sc_check_data['address_error'] = self.addr_error
        return self.sc_check_data


def check_sc_second_step_shopping_cart(sc_check_instance, object_id_list, default_calendar_id, default_invoice_adr,
                                       company_code,
                                       default_address_number, address_number_list, accounting_data, manager_details,
                                       approver_id, total_value,
                                       msg_info,
                                       cart_items):
    """

    """
    holiday_list = []
    cart_items_count = len(cart_items)
    sc_check_instance.document_sc_transaction_check(object_id_list)
    sc_check_instance.po_transaction_check(object_id_list)
    sc_check_instance.calender_id_check(default_calendar_id)
    error_msg = sc_check_instance.header_level_delivery_address_check(default_address_number, company_code,
                                                                      address_number_list, True)
    sc_check_instance.update_approval_check(manager_details, approver_id, total_value,
                                            msg_info)
    sc_check_instance.header_level_acc_check(accounting_data['acc_list'], accounting_data['default_acc_ass_cat'],
                                             accounting_data['acc_value_list'], accounting_data['default_acc'],
                                             company_code)
    sc_check_instance.invoice_address_check(default_invoice_adr, company_code)

    # if error_msg:
    #     sc_check_instance.item_level_delivery_address_check(cart_items_count, error_msg)
    if default_calendar_id is not None or default_calendar_id != '':
        holiday_list = get_list_of_holidays(default_calendar_id, global_variables.GLOBAL_CLIENT)

    for loop_count, items in enumerate(cart_items):
        item_number = loop_count + 1
        sc_check_instance.check_for_prod_cat(items['prod_cat_id'], company_code, item_number)
        if items['call_off'] != CONST_PR_CALLOFF:
            sc_check_instance.check_for_supplier(items['supplier_id'], items['prod_cat_id'], company_code, item_number)
        if items['call_off'] == CONST_CATALOG_CALLOFF:
            sc_check_instance.catalog_item_check(items['int_product_id'], items['price'], items['lead_time'],
                                                 item_number, items['guid'],
                                                 items['quantity'])
        if items['call_off'] not in [CONST_FREETEXT_CALLOFF, CONST_LIMIT_ORDER_CALLOFF]:
            if len(holiday_list) == 0:
                item_delivery_date = None
            else:
                item_delivery_date = calculate_delivery_date(items['guid'],
                                                             items['lead_time'],
                                                             items['supplier_id'],
                                                             default_calendar_id,
                                                             global_variables.GLOBAL_CLIENT,
                                                             CartItemDetails)
        elif items['call_off'] == CONST_FREETEXT_CALLOFF:
            item_delivery_date = calculate_delivery_date_base_on_lead_time(items['lead_time'],
                                                                           items['supplier_id'],
                                                                           default_calendar_id)
            if items['item_del_date'] < item_delivery_date:
                django_query_instance.django_update_query(CartItemDetails,
                                                          {'guid': items['guid'],
                                                           'client': global_variables.GLOBAL_CLIENT},
                                                          {'item_del_date': item_delivery_date})
            else:
                item_delivery_date = items['item_del_date']

        else:
            if items['start_date'] is None:
                item_delivery_date = items['item_del_date']

            else:
                item_delivery_date = items['start_date']
        sc_check_instance.delivery_date_check(item_delivery_date, item_number, holiday_list, default_calendar_id)
        items['item_del_date'] = item_delivery_date

    shopping_cart_errors = sc_check_instance.get_shopping_cart_errors()
    return cart_items, shopping_cart_errors


def get_grouping_detail(company_id, prod_cat_id, call_off, product_id):
    """

    """
    if django_query_instance.django_existence_check(SourcingMapping,
                                                    {'product_id': product_id,
                                                     'prod_cat_id': prod_cat_id,
                                                     'company_id': company_id,
                                                     'client': global_variables.GLOBAL_CLIENT,
                                                     'del_ind': False}):
        return True
    elif django_query_instance.django_existence_check(SourcingRule,
                                                      {'call_off': call_off,
                                                       'prod_cat_id_from__gte': prod_cat_id,
                                                       'prod_cat_id_to__lte': prod_cat_id,
                                                       'client': global_variables.GLOBAL_CLIENT,
                                                       'del_ind': False}):
        return True
    return False


def get_source_relevant_ind(company_code, prod_cat_id, call_off, product_id):
    srcing_flag = False

    if django_query_instance.django_existence_check(PurchaseControl,
                                                    {'call_off': call_off,
                                                     'company_code_id': company_code,
                                                     'purchase_ctrl_flag': True,
                                                     'prod_cat_id': prod_cat_id,
                                                     'client': global_variables.GLOBAL_CLIENT,
                                                     'del_ind': False}):
        # return True
        srcing_flag = False
    else:
        if django_query_instance.django_existence_check(SourcingRule,
                                                        {'call_off': call_off,
                                                         'prod_cat_id_from__lte': prod_cat_id,
                                                         'prod_cat_id_to__gte': prod_cat_id,
                                                         'client': global_variables.GLOBAL_CLIENT,
                                                         'del_ind': False}):
            if not django_query_instance.django_existence_check(SourcingMapping,
                                                                {'product_id': product_id,
                                                                 'prod_cat_id': prod_cat_id,
                                                                 'company_id': company_code,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'del_ind': False}) or django_query_instance.django_existence_check(
                SourcingMapping,
                {'product_id': product_id,
                 'prod_cat_id': prod_cat_id,
                 'company_id': company_code,
                 'client': global_variables.GLOBAL_CLIENT,
                 'del_ind': False}):
                srcing_flag = True
        else:
            srcing_flag = False

    return srcing_flag
