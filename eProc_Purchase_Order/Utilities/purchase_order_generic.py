import datetime
import time

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from eProc_Attributes.Utilities.attributes_generic import OrgAttributeValues
from eProc_Basic.Utilities.constants.constants import CONST_PO_SPLIT_SUPPLIER, CONST_PO_SPLIT_CURRENCY, \
    CONST_ERROR_SPLIT_CRITERIA, CONST_SC_TRANS_TYPE, CONST_PO_TRANS_TYPE, CONST_DOC_TYPE_PO, \
    CONST_ERROR_TRANSACTION_TYPE, CONST_PO_STATUS_ORDERED, CONST_SYSTEM_USER, CONST_CALENDAR_ID, CONST_MULTIPLE, \
    CONST_DOC_TYPE_SC, CONST_SUPPLIER_NOTE, CONST_INTERNAL_NOTE, CONST_AUTO, CONST_FREETEXT_CALLOFF, \
    CONST_FT_ITEM_EFORM, CONST_CATALOG_CALLOFF, CONST_ALL, CONST_CATALOG_ITEM_VARIANT, CONST_VALIDATION_ERROR, \
    CONST_NOT_FOUND_ERROR
from eProc_Basic.Utilities.functions.dictionary_key_to_list import dictionary_key_to_list
from eProc_Basic.Utilities.functions.distinct_list import distinct_list
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.generate_document_number import generate_document_number
from eProc_Basic.Utilities.functions.get_db_query import requester_field_info
from eProc_Basic.Utilities.functions.get_description import get_description_uom, get_accounting_description, \
    get_acc_value_desc_update, get_gl_acc_description
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.remove_element_from_list import remove_element_from_list
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG001, MSG0120
from eProc_Calendar_Settings.Utilities.calender_settings_generic import calculate_delivery_date
from eProc_Configuration.models import PoSplitCriteria, NumberRanges, OrgAddress, SupplierMaster, OrgPorg, OrgPGroup, \
    DocumentType, UnitOfMeasures, PoGroupCriteria
from eProc_Doc_Details.Utilities.details_generic import GetAttachments
from eProc_Doc_Search_and_Display.Utilities.search_display_specific import get_po_header_app
from eProc_Emails.Utilities.email_notif_generic import send_po_attachment_email
from eProc_Exchange_Rates.Utilities.exchange_rates_generic import convert_currency
from eProc_Form_Builder.models import EformFieldData
from eProc_Generate_PDF.Utilities.generate_pdf_generic import save_pdf
# from eProc_Generate_PDF.Utilities.generate_pdf_generic import save_pdf
# from eProc_Generate_PDF.Utilities.generate_pdf_generic import save_pdf
# from eProc_Generate_PDF.Utilities.generate_pdf_generic import save_pdf
# from eProc_Generate_PDF.Utilities.generate_pdf_generic import save_pdf
# from eProc_Generate_PDF.Utilities.generate_pdf_generic import save_pdf
from eProc_Generate_PDF.Utilities.generate_pdf_generic import save_pdf
from eProc_Generate_PDF.views import render_pdf_view
from eProc_Notes_Attachments.models import Notes, Attachments
from eProc_Price_Calculator.Utilities.price_calculator_generic import calculate_item_total_value
from eProc_Purchase_Order.models import PoHeader, PoItem, PoAccounting, PoApproval, PoPotentialApproval, PoAddresses
from eProc_Registration.models import UserData
from eProc_Related_Documents.Utilities.related_documents_generic import get_item_level_related_documents
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import get_total_value, get_image_url
from eProc_Shopping_Cart.models import ScHeader, ScItem, ScAccounting, ScApproval, ScPotentialApproval, ScAddresses, \
    PurchasingData, PurchasingUser
from eProc_Suppliers.Utilities.supplier_generic import get_supplier_email
from eProc_User_Settings.Utilities.user_settings_generic import get_object_id_list_user

django_query_instance = DjangoQueries()


def get_po_split_type(company_code):
    """

    """
    po_split_active_list_cocode = []
    po_split_list = django_query_instance.django_filter_value_list_query(PoSplitCriteria,
                                                                         {'client': global_variables.GLOBAL_CLIENT,
                                                                          'del_ind': False,
                                                                          'company_code_id': '*',
                                                                          'activate': True}, 'po_split_type')

    if django_query_instance.django_existence_check(PoSplitCriteria,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'del_ind': False,
                                                     'company_code_id': company_code,
                                                     'activate': False}):
        po_split_inactive_list_cocode = django_query_instance.django_filter_value_list_query(PoSplitCriteria,
                                                                                             {
                                                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                                                 'del_ind': False,
                                                                                                 'company_code_id': company_code,
                                                                                                 'activate': False},
                                                                                             'po_split_type')
        po_split_list = remove_element_from_list(po_split_list, po_split_inactive_list_cocode)
    if django_query_instance.django_existence_check(PoSplitCriteria,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'del_ind': False,
                                                     'company_code_id': company_code,
                                                     'activate': True}):
        po_split_active_list_cocode = django_query_instance.django_filter_value_list_query(PoSplitCriteria,
                                                                                           {
                                                                                               'client': global_variables.GLOBAL_CLIENT,
                                                                                               'del_ind': False,
                                                                                               'company_code_id': company_code,
                                                                                               'activate': True},
                                                                                           'po_split_type')
    po_split_list = list(set(po_split_list + po_split_active_list_cocode))
    return po_split_list


class CreatePurchaseOrder:
    def __init__(self, sc_header_instance):
        self.supplier_name = ''
        self.sc_header_instance = sc_header_instance
        self.po_document_number = ''
        self.sequence = ''
        self.po_transaction_type = ''
        self.po_header_guid = ''
        self.po_doc_list = []
        self.po_header_guid_generator = ''
        self.supplier_id = ''
        self.sc_item_guid = []
        self.error_message = ''
        self.output = ''
        self.sc_item_instance = django_query_instance.django_filter_query(ScItem,
                                                                          {'header_guid': sc_header_instance.guid,
                                                                           'client': global_variables.GLOBAL_CLIENT,
                                                                           'del_ind': False}, ['item_num'], None)
        for sc_item_details in self.sc_item_instance:
            self.sc_item_guid.append(sc_item_details['guid'])
        self.requester_obj_id = requester_field_info(sc_header_instance.requester, 'object_id')
        self.object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT, self.requester_obj_id)

    # @transaction.atomic
    def create_po(self):
        """

        """
        po_creation_flag = False
        # get split type for the sc company code
        po_split_list = get_po_split_type(self.sc_header_instance.co_code)
        # po_split_list = get_po_split_group_type(self.sc_header_instance.co_code)
        print("splitting type:", po_split_list)
        if po_split_list:
            if CONST_PO_SPLIT_SUPPLIER in po_split_list:
                supplier_list = django_query_instance.django_filter_value_list_query(ScItem,
                                                                                     {
                                                                                         'client': global_variables.GLOBAL_CLIENT,
                                                                                         'header_guid': self.sc_header_instance.guid,
                                                                                         'source_relevant_ind': 0},
                                                                                     'supplier_id')
                print("supplier list", supplier_list)
                # supplier level split
                for supplier in supplier_list:
                    print("supplier based split:", supplier)
                    sc_item_details = django_query_instance.django_filter_query(ScItem,
                                                                                {
                                                                                    'client': global_variables.GLOBAL_CLIENT,
                                                                                    'header_guid': self.sc_header_instance.guid,
                                                                                    'supplier_id': supplier
                                                                                }, ['item_num'], None)
                    if sc_item_details:
                        po_creation_flag = check_for_po_creation(sc_item_details[0])
                    # if currency level split is enabled
                    if CONST_PO_SPLIT_CURRENCY in po_split_list:
                        currency_list = django_query_instance.django_filter_value_list_query(ScItem,
                                                                                             {
                                                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                                                 'header_guid': self.sc_header_instance.guid,
                                                                                                 'supplier_id': supplier},
                                                                                             'currency')
                        # if items has different currency
                        if len(currency_list) != 1:
                            print("currency List: ", currency_list)
                            for currency in currency_list:
                                print("currency based split: ", currency)
                                sc_item_details = django_query_instance.django_filter_query(ScItem,
                                                                                            {
                                                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                                                'header_guid': self.sc_header_instance.guid,
                                                                                                'supplier_id': supplier,
                                                                                                'currency': currency
                                                                                            }, None, None)
                                print("no. of PO Item for currency split:", len(sc_item_details))
                                if sc_item_details:
                                    po_creation_flag = check_for_po_creation(sc_item_details[0])
                                if po_creation_flag:
                                    status = self.create_purchaser_order(sc_item_details, supplier)
                                    if not status:
                                        return False, self.error_message, self.output, self.po_doc_list
                        # items has same currency
                        else:
                            print("No currency split for same currency:", len(sc_item_details))
                            print("Item Count", len(sc_item_details))
                            if sc_item_details:
                                po_creation_flag = check_for_po_creation(sc_item_details[0])
                            if po_creation_flag:
                                status = self.create_purchaser_order(sc_item_details, supplier)
                                if not status:
                                    return False, self.error_message, self.output, self.po_doc_list
                    # only supplier split is enabled
                    else:
                        print("supplier split", sc_item_details)
                        print("Item Count", len(sc_item_details))
                        if sc_item_details:
                            po_creation_flag = check_for_po_creation(sc_item_details[0])
                        if po_creation_flag:
                            status = self.create_purchaser_order(sc_item_details, supplier)
                            if not status:
                                return False, self.error_message, self.output, self.po_doc_list
            else:
                update_po_error_status(self.sc_header_instance.guid, CONST_ERROR_SPLIT_CRITERIA)
        else:
            update_po_error_status(self.sc_header_instance.guid, CONST_ERROR_SPLIT_CRITERIA)
        return True, self.error_message, self.output, self.po_doc_list

    @transaction.atomic
    def create_purchaser_order(self, sc_item_details, supplier_id):
        """

        """
        self.supplier_id = supplier_id
        send_to_list = []
        try:
            status = self.create_po_header(sc_item_details)

            if not status:
                print("error")
                return "Error"
            else:
                item_status = self.create_po_item(sc_item_details)
                if item_status:
                    print("po item created successfully")
                    accounting_status = self.create_po_accounting(sc_item_details)
                    if accounting_status:
                        print("po accounting created successfully")
                        approval_status = self.create_po_approval()
                        if approval_status:
                            address_status = self.create_po_address(sc_item_details)
                            if address_status:
                                purchase_status = self.update_purchase_status(sc_item_details)
                                if purchase_status:
                                    self.update_document_number_sc_item(sc_item_details)
            print("PO created")
            context = get_po_details(self.po_header_guid)
            context['po_header_delivery_address'] = django_query_instance.django_get_query(PoAddresses, {
                'po_header_guid': self.po_header_guid,
                'address_type': 'D',
                'del_ind': False})
            context['po_header_invoice_address'] = django_query_instance.django_get_query(PoAddresses,
                                                                                          {
                                                                                              'po_header_guid': self.po_header_guid,
                                                                                              'address_type': 'I',
                                                                                              'del_ind': False})
            context = get_po_details(self.po_header_guid)
            context['doc_number'] = self.po_document_number
            context['po_header_delivery_address'] = django_query_instance.django_get_query(PoAddresses, {
                'po_header_guid': self.po_header_guid,
                'address_type': 'D',
                'del_ind': False})
            context['po_header_invoice_address'] = django_query_instance.django_get_query(PoAddresses, {
                'po_header_guid': self.po_header_guid,
                'address_type': 'I',
                'del_ind': False})
            file_name, status, self.output = save_pdf(context)
            self.sc_header_instance.follow_on_doc_type = CONST_DOC_TYPE_PO
            self.sc_header_instance.save()
            # django_query_instance.django_update_query(PoHeader,
            #                                           {'client':global_variables.GLOBAL_CLIENT})
            # subject = 'Purchase Order Detail ' + str(self.po_document_number)
            # content = 'Dear ' + str(
            #     self.supplier_name) + ',\n Please find attached purchase order.\n\nRegards,\nMajjaka'
            # send_to_list.append(get_supplier_email(supplier_id))
            email_supp_monitoring_guid = ''
            send_po_attachment_email(self.output, self.po_document_number, email_supp_monitoring_guid)

            return True
        # except ValidationError:
        except Exception as error_message:
            print(str(error_message))
            self.error_message = str(error_message)
            update_po_error_status(self.sc_header_instance.guid, CONST_VALIDATION_ERROR)
            return False

    def create_po_header(self, sc_item_details):
        """

        """
        self.po_document_number, self.sequence, self.po_transaction_type = generate_document_number(CONST_PO_TRANS_TYPE,
                                                                                                    global_variables.GLOBAL_CLIENT,
                                                                                                    self.object_id_list,
                                                                                                    False,
                                                                                                    CONST_DOC_TYPE_PO)

        if not self.po_document_number:
            update_po_error_status(self.sc_header_instance.guid, CONST_ERROR_TRANSACTION_TYPE)
            return False
        else:
            print(self.po_document_number)
            print("sc_item_details ", sc_item_details)
            sgst_data = sum(dictionary_key_to_list(sc_item_details, 'sgst'))
            cgst_data = sum(dictionary_key_to_list(sc_item_details, 'cgst'))
            vat_data = sum(dictionary_key_to_list(sc_item_details, 'vat'))
            # sgst_data = 0.00
            # cgst_data = 0.00
            # vat_data = 0.00
            self.po_header_guid_generator = guid_generator()
            self.po_header_guid = self.po_header_guid_generator
            supplier_details = django_query_instance.django_get_query(SupplierMaster,
                                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                                       'supplier_id': self.supplier_id})
            self.supplier_name = supplier_details.name1
            total_value = get_total_value(sc_item_details, self.sc_header_instance.currency)
            po_header_details = {
                'po_header_guid': self.po_header_guid,
                'doc_number': self.po_document_number,
                'transaction_type': self.po_transaction_type,
                'posting_date': datetime.datetime.now(),
                'version_type': 'A',
                'version_num': 1,
                'description': self.sc_header_instance.description,
                'language_id': self.sc_header_instance.language_id,
                'currency': supplier_details.currency_id,
                'payment_term': sc_item_details[0]['payment_term'],
                'incoterm': sc_item_details[0]['incoterm'],
                'incoterm_loc': sc_item_details[0]['incoterm_loc'],
                'requester': self.sc_header_instance.requester,
                'status': CONST_PO_STATUS_ORDERED,
                'po_header_created_at': datetime.datetime.now(),
                'po_header_created_by': CONST_SYSTEM_USER,
                'po_header_changed_at': datetime.datetime.now(),
                'po_header_changed_by': CONST_SYSTEM_USER,
                'document_type': CONST_DOC_TYPE_PO,
                'ordered_at': datetime.datetime.now(),
                'time_zone': self.sc_header_instance.time_zone,
                'company_code_id': self.sc_header_instance.co_code,
                'inv_addr_num': self.sc_header_instance.inv_addr_num,
                'ship_addr_num': self.sc_header_instance.ship_addr_num,
                'supplier_id': sc_item_details[0]['supplier_id'],
                'supplier_username': sc_item_details[0]['supplier_username'],
                'supplier_mobile_num': sc_item_details[0]['supplier_mobile_num'],
                'supplier_fax_no': sc_item_details[0]['supplier_fax_no'],
                'supplier_email': sc_item_details[0]['supplier_email'],
                'pref_supplier': sc_item_details[0]['pref_supplier'],
                'supp_type': sc_item_details[0]['supp_type'],
                'delivery_days': sc_item_details[0]['delivery_days'],
                'sgst': sgst_data,
                'cgst': cgst_data,
                'vat': vat_data,
                'total_value': total_value,
                'client': global_variables.GLOBAL_CLIENT
            }

        django_query_instance.django_create_query(PoHeader, po_header_details)
        self.po_doc_list.append(self.po_document_number)
        # save header level note
        save_po_header_level_notes(self.sc_header_instance.guid, self.po_header_guid)

        # update current document number in number range table
        django_query_instance.django_update_query(NumberRanges,
                                                  {'client': global_variables.GLOBAL_CLIENT,
                                                   'del_ind': False,
                                                   'sequence': self.sequence,
                                                   'document_type': CONST_DOC_TYPE_PO},
                                                  {'current': self.po_document_number})
        print("PO Header Created Successfully")
        return True

    def create_po_item(self, sc_item_details):
        """

        """
        po_item_list = []
        org_attr_value_instance = OrgAttributeValues()
        default_calendar_id = org_attr_value_instance.get_user_default_attr_value_list_by_attr_id(self.object_id_list,
                                                                                                  CONST_CALENDAR_ID)[1]

        self.po_header_guid = django_query_instance.django_get_query(PoHeader,
                                                                     {'client': global_variables.GLOBAL_CLIENT,
                                                                      'del_ind': False,
                                                                      'po_header_guid': self.po_header_guid})

        for loop_counter, sc_item_detail in enumerate(sc_item_details):
            print("po item", loop_counter)
            desc = sc_item_details[loop_counter]['description']
            po_item_num = loop_counter + 1
            delivery_date = calculate_delivery_date(sc_item_detail['guid'], int(sc_item_detail['lead_time']),
                                                    sc_item_detail['supplier_id'],
                                                    default_calendar_id, global_variables.GLOBAL_CLIENT,
                                                    ScItem)
            if sc_item_detail['currency'] != self.po_header_guid.currency:
                item_value = calculate_item_total_value(sc_item_detail['call_off'], sc_item_detail['quantity'],
                                                        sc_item_detail['quantity'], sc_item_detail['price_unit'],
                                                        sc_item_detail['price'], None)
                sc_item_detail['value'] = convert_currency(item_value,
                                                           str(sc_item_detail['currency']),
                                                           str(self.po_header_guid.currency))
            # if sc_item_detail['description'] == desc:
                # sc_item_detail['quantity'] += 1
            po_item_guid = guid_generator()
            po_item_dictionary = {
                'po_item_guid': po_item_guid, 'po_item_num': po_item_num,
                'sc_doc_num': self.sc_header_instance.doc_number,
                'sc_item_num': sc_item_detail['item_num'], 'int_product_id': sc_item_detail['int_product_id'],
                'supp_product_id': sc_item_detail['supp_product_id'], 'description': sc_item_detail['description'],
                'long_desc': sc_item_detail['long_desc'], 'stock_keeping_unit': sc_item_detail['stock_keeping_unit'],
                'univeral_product_code': sc_item_detail['univeral_product_code'], 'barcode': sc_item_detail['barcode'],
                'itm_language_id': sc_item_detail['itm_language_id'], 'order_date': datetime.datetime.now(),
                'grp_ind': sc_item_detail['grp_ind'], 'company_code_id': self.sc_header_instance.co_code,
                'del_datcat': sc_item_detail['del_datcat'], 'item_del_date': delivery_date,
                'prod_cat_id': sc_item_detail['prod_cat_id'], 'prod_cat_desc': sc_item_detail['prod_cat_desc'],
                'cust_prod_cat_id': sc_item_detail['cust_prod_cat_id'], 'lead_time': sc_item_detail['lead_time'],
                'final_inv': sc_item_detail['final_inv'], 'overall_limit': sc_item_detail['overall_limit'],
                'expected_value': sc_item_detail['expected_value'], 'start_date': sc_item_detail['start_date'],
                'end_date': sc_item_detail['end_date'], 'required_on': sc_item_detail['required_on'],
                'undef_limit': sc_item_detail['undef_limit'], 'ir_gr_ind_limi': sc_item_detail['ir_gr_ind_limi'],
                'gr_ind_limi': sc_item_detail['gr_ind_limi'], 'val_iv_e': sc_item_detail['val_iv_e'],
                'val_iv': sc_item_detail['val_iv'], 'val_po_e': sc_item_detail['val_po_e'],
                'val_po_e_agg': sc_item_detail['val_po_e_agg'], 'quan_po_e': sc_item_detail['quan_po_e'],
                'source_relevant_ind': sc_item_detail['source_relevant_ind'], 'ext_demid': sc_item_detail['ext_demid'],
                'ext_dem_posid': sc_item_detail['ext_dem_posid'], 'offcatalog': sc_item_detail['offcatalog'],
                'process_flow': sc_item_detail['process_flow'], 'quantity_min': sc_item_detail['quantity_min'],
                'quantity_max': sc_item_detail['quantity_max'], 'tiered_flag': sc_item_detail['tiered_flag'],
                'bundle_flag': sc_item_detail['bundle_flag'], 'material_no': sc_item_detail['material_no'],
                'sgst': sc_item_detail['sgst'], 'cgst': sc_item_detail['cgst'], 'vat': sc_item_detail['vat'],
                'prod_type': sc_item_detail['prod_type'], 'catalog_id': sc_item_detail['catalog_id'],
                'catalog_name': sc_item_detail['catalog_name'], 'fin_entry_ind': sc_item_detail['fin_entry_ind'],
                'price_origin': sc_item_detail['price_origin'], 'quantity': sc_item_detail['quantity'],
                'base_price': sc_item_detail['base_price'], 'additional_price': sc_item_detail['additional_price'],
                'actual_price': sc_item_detail['actual_price'],
                'discount_percentage': sc_item_detail['discount_percentage'],
                'discount_value': sc_item_detail['discount_value'], 'price': sc_item_detail['price'],
                'tax_value': sc_item_detail['tax_value'], 'price_unit': sc_item_detail['price_unit'],
                'unit': sc_item_detail['unit'], 'gross_price': sc_item_detail['gross_price'],
                'value': sc_item_detail['value'], 'value_min': sc_item_detail['value_min'],
                'currency': sc_item_detail['currency'], 'tax_code': sc_item_detail['tax_code'],
                'gr_ind': sc_item_detail['gr_ind'], 'ir_gr_ind': sc_item_detail['ir_gr_ind'],
                'ir_ind': sc_item_detail['ir_ind'], 'po_resp': sc_item_detail['po_resp'],
                'asn_ind': sc_item_detail['asn_ind'], 'eform_id': sc_item_detail['eform_id'],
                'dis_rej_ind': sc_item_detail['dis_rej_ind'], 'goods_marking': sc_item_detail['goods_marking'],
                'ctr_name': sc_item_detail['ctr_name'], 'ctr_num': sc_item_detail['ctr_num'],
                'ctr_item_num': sc_item_detail['ctr_item_num'], 'pref_supplier': sc_item_detail['pref_supplier'],
                'approved_by': sc_item_detail['approved_by'], 'call_off': sc_item_detail['call_off'],
                'manu_part_num': sc_item_detail['manu_part_num'], 'manu_code_num': sc_item_detail['manu_code_num'],
                'ship_from_addr_num': sc_item_detail['ship_from_addr_num'], 'status': sc_item_detail['status'],
                'bill_to_addr_num': sc_item_detail['bill_to_addr_num'],
                'ship_to_addr_num': sc_item_detail['ship_to_addr_num'],
                'cash_disc1': sc_item_detail['cash_disc1'], 'cash_disc2': sc_item_detail['cash_disc2'],
                'goods_recep': sc_item_detail['goods_recep'], 'manufacturer': sc_item_detail['manufacturer'],
                'delivery_days': sc_item_detail['delivery_days'],
                'supplier_note_existence_flag': sc_item_detail['supplier_note_existence_flag'],
                'internal_note_existence_flag': sc_item_detail['internal_note_existence_flag'],
                'attachment_existence_flag': sc_item_detail['attachment_existence_flag'],
                'accounting_change_flag': sc_item_detail['accounting_change_flag'],
                'address_change_flag': sc_item_detail['address_change_flag'],
                'po_item_created_at': datetime.datetime.now(), 'po_item_created_by': CONST_SYSTEM_USER,
                'po_item_changed_at': datetime.datetime.now(), 'po_item_changed_by': CONST_SYSTEM_USER,
                'po_header_guid': self.po_header_guid,
                'client': global_variables.GLOBAL_CLIENT,
                'sc_header_guid': self.sc_header_instance,
                'sc_item_guid': django_query_instance.django_get_query(ScItem,
                                                                       {'client': global_variables.GLOBAL_CLIENT,
                                                                        'guid': sc_item_detail['guid'],
                                                                        'del_ind': False})
            }
            po_item_list.append(po_item_dictionary)
            # create entry in po item table
            django_query_instance.django_create_query(PoItem, po_item_dictionary)
            if sc_item_detail['eform_id']:
                update_po_item_guid_eform(po_item_guid, sc_item_detail['guid'])

            # save item level note
            save_po_item_level_supp_int_note(sc_item_detail['guid'], po_item_guid, loop_counter)

            save_attachments(sc_item_detail['guid'], self.sc_header_instance.guid, po_item_guid, self.po_header_guid,
                             loop_counter, self.po_document_number)
            django_query_instance.django_update_query(ScItem,
                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                       'guid': sc_item_detail['guid'],
                                                       'del_ind': False},
                                                      {'po_doc_num': self.po_document_number,
                                                       'po_item_num': po_item_num,
                                                       'po_item_guid': po_item_guid,
                                                       'po_header_guid': self.po_header_guid_generator})

        # django_query_instance.django_bulk_create_query(PoItem, po_item_list)
        return True

    def create_po_accounting(self, sc_item_details):
        """

        """
        sc_item_guid_list = dictionary_key_to_list(sc_item_details, 'guid')
        filter_queue = Q(item_guid__in=sc_item_guid_list) | Q(header_guid=self.sc_header_instance.guid)
        accounting_details = django_query_instance.django_queue_query(ScAccounting,
                                                                      {'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue, None, None)
        for count, accounting_detail in enumerate(accounting_details):
            if accounting_detail['header_guid_id']:
                accounting_detail['po_header_guid'] = self.po_header_guid
                accounting_detail['acc_item_num'] = 0
            else:
                po_item_guid = django_query_instance.django_filter_value_list_query(PoItem,
                                                                                    {
                                                                                        'client': global_variables.GLOBAL_CLIENT,
                                                                                        'del_ind': False,
                                                                                        'sc_item_guid':
                                                                                            accounting_detail[
                                                                                                'item_guid_id']},
                                                                                    'po_item_guid')[0]
                po_item_instance = django_query_instance.django_get_query(PoItem,
                                                                          {
                                                                              'client': global_variables.GLOBAL_CLIENT,
                                                                              'del_ind': False,
                                                                              'po_item_guid': po_item_guid})

                accounting_detail['po_item_guid'] = po_item_instance
                accounting_detail['acc_item_num'] = po_item_instance.po_item_num
            del accounting_detail['guid']
            del accounting_detail['sc_accounting_created_at']
            del accounting_detail['sc_accounting_created_by']
            del accounting_detail['sc_accounting_changed_at']
            del accounting_detail['sc_accounting_changed_by']
            del accounting_detail['sc_accounting_source_system']
            del accounting_detail['sc_accounting_destination_system']
            del accounting_detail['header_guid_id']
            del accounting_detail['item_guid_id']
            accounting_detail['po_accounting_guid'] = guid_generator()
            accounting_detail['po_accounting_created_at'] = datetime.datetime.now()
            accounting_detail['po_accounting_created_by'] = CONST_SYSTEM_USER
            accounting_detail['po_accounting_changed_at'] = datetime.datetime.now()
            accounting_detail['po_accounting_changed_by'] = CONST_SYSTEM_USER
            accounting_detail['client'] = global_variables.GLOBAL_CLIENT
            django_query_instance.django_create_query(PoAccounting, accounting_detail)
        return True
        # django_query_instance.django_bulk_create_query(PoAccounting,accounting_details)

    def create_po_approval(self):
        """

        """
        sc_approval_details = django_query_instance.django_filter_query(ScApproval,
                                                                        {'header_guid': self.sc_header_instance.guid},
                                                                        None,
                                                                        None)
        sc_potential_approval_details = django_query_instance.django_filter_query(ScPotentialApproval,
                                                                                  {
                                                                                      'sc_header_guid': self.sc_header_instance.guid},
                                                                                  None,
                                                                                  None)
        if not django_query_instance.django_existence_check(PoApproval,
                                                            {'po_header_guid': self.po_header_guid}):
            for sc_approval_detail in sc_approval_details:
                sc_approval_detail['po_header_guid'] = self.po_header_guid
                sc_approval_detail['po_approval_guid'] = guid_generator()
                sc_approval_detail['client'] = global_variables.GLOBAL_CLIENT
                del sc_approval_detail['guid']
                del sc_approval_detail['sc_approval_created_at']
                del sc_approval_detail['sc_approval_created_by']
                del sc_approval_detail['sc_approval_changed_at']
                del sc_approval_detail['sc_approval_changed_by']
                del sc_approval_detail['header_guid_id']
                del sc_approval_detail['item_guid_id']
                django_query_instance.django_create_query(PoApproval, sc_approval_detail)
        if not django_query_instance.django_existence_check(PoPotentialApproval,
                                                            {'po_header_guid': self.po_header_guid}):
            for sc_potential_approval_detail in sc_potential_approval_details:
                sc_potential_approval_detail['po_header_guid'] = self.po_header_guid
                if sc_potential_approval_detail['app_id'] == CONST_AUTO:
                    sc_potential = {'client': global_variables.GLOBAL_CLIENT,
                                    'po_header_guid': self.po_header_guid,
                                    'step_num': sc_potential_approval_detail['step_num']}
                else:
                    sc_potential = {'client': global_variables.GLOBAL_CLIENT,
                                    'po_header_guid': self.po_header_guid,
                                    'step_num': sc_potential_approval_detail['step_num'],
                                    'app_id': sc_potential_approval_detail['app_id']}
                sc_potential_approval_detail['po_approval_guid'] = django_query_instance.django_get_query(PoApproval,
                                                                                                          sc_potential)
                sc_potential_approval_detail['po_potential_approval_guid'] = guid_generator()
                sc_potential_approval_detail['client'] = global_variables.GLOBAL_CLIENT
                del sc_potential_approval_detail['sc_potential_approval_guid']
                del sc_potential_approval_detail['sc_approval_guid_id']
                del sc_potential_approval_detail['sc_header_guid_id']
                django_query_instance.django_create_query(PoPotentialApproval, sc_potential_approval_detail)
        return True

    def create_po_address(self, sc_item_details):
        """

        """
        sc_item_guid_list = dictionary_key_to_list(sc_item_details, 'guid')
        filter_queue = Q(item_guid__in=sc_item_guid_list) | Q(header_guid=self.sc_header_instance.guid)
        sc_address_details = django_query_instance.django_queue_query(ScAddresses,
                                                                      {'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue, ['item_num'], None)
        for sc_address_detail in sc_address_details:

            if sc_address_detail['header_guid_id']:
                print('creating header level po address')
                sc_address_detail['po_header_guid'] = self.po_header_guid
            else:
                print('creating item level po address')
                po_item_guid = django_query_instance.django_filter_value_list_query(PoItem,
                                                                                    {
                                                                                        'client': global_variables.GLOBAL_CLIENT,
                                                                                        'del_ind': False,
                                                                                        'sc_item_guid':
                                                                                            sc_address_detail[
                                                                                                'item_guid_id']},
                                                                                    'po_item_guid')[0]
                po_item_guid_detail = django_query_instance.django_get_query(PoItem,
                                                                             {
                                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                                 'del_ind': False,
                                                                                 'po_item_guid': po_item_guid})
                sc_address_detail['po_item_guid'] = po_item_guid_detail
                sc_address_detail['item_num'] = po_item_guid_detail.po_item_num

            del sc_address_detail['guid']
            del sc_address_detail['sc_addr_created_at']
            del sc_address_detail['sc_addr_created_by']
            del sc_address_detail['sc_addr_changed_at']
            del sc_address_detail['sc_addr_changed_by']
            del sc_address_detail['sc_addresses_source_system']
            del sc_address_detail['sc_addresses_destination_system']
            del sc_address_detail['header_guid_id']
            del sc_address_detail['item_guid_id']
            sc_address_detail['po_addresses_guid'] = guid_generator()
            sc_address_detail['po_addr_created_at'] = datetime.datetime.now()
            sc_address_detail['po_addr_created_by'] = CONST_SYSTEM_USER
            sc_address_detail['po_addr_changed_at'] = datetime.datetime.now()
            sc_address_detail['po_addr_changed_by'] = CONST_SYSTEM_USER
            sc_address_detail['client'] = global_variables.GLOBAL_CLIENT
            django_query_instance.django_create_query(PoAddresses, sc_address_detail)
        return True

    def update_purchase_status(self, sc_item_details):
        """

        """
        print("update purchasing data")
        for sc_item_detail in sc_item_details:
            po_item_guid = django_query_instance.django_filter_value_list_query(PoItem,
                                                                                {'sc_item_guid': sc_item_detail['guid'],
                                                                                 'sc_header_guid': self.sc_header_instance.guid},
                                                                                'po_item_guid')[0]
            print("purchasing po item guid", po_item_guid)
            po_item_guid = django_query_instance.django_get_query(PoItem, {'po_item_guid': po_item_guid})
            if django_query_instance.django_existence_check(PurchasingData,
                                                            {'sc_item_guid': sc_item_detail['guid'],
                                                             'sc_header_guid': self.sc_header_instance.guid}):
                django_query_instance.django_update_query(PurchasingData,
                                                          {'sc_item_guid': sc_item_detail['guid'],
                                                           'sc_header_guid': self.sc_header_instance.guid},
                                                          {'po_item_guid': po_item_guid,
                                                           'po_header_guid': self.po_header_guid})
            if django_query_instance.django_existence_check(PurchasingUser,
                                                            {'sc_item_guid': sc_item_detail['guid'],
                                                             'sc_header_guid': self.sc_header_instance.guid}):
                django_query_instance.django_update_query(PurchasingUser,
                                                          {'sc_item_guid': sc_item_detail['guid'],
                                                           'sc_header_guid': self.sc_header_instance.guid},
                                                          {'po_item_guid': po_item_guid,
                                                           'po_header_guid': self.po_header_guid})
        return True

    def update_document_number_sc_item(self, sc_item_details):
        """

        """
        for sc_item_detail in sc_item_details:
            django_query_instance.django_update_query(ScItem,
                                                      {'guid': sc_item_detail['guid'],
                                                       'client': global_variables.GLOBAL_CLIENT,
                                                       'del_ind': False},
                                                      {'po_doc_num': self.po_document_number})


def update_po_error_status(header_guid, error_type):
    """

    """
    django_query_instance.django_update_query(ScHeader,
                                              {'client': global_variables.GLOBAL_CLIENT,
                                               'del_ind': False,
                                               'guid': header_guid},
                                              {'transmission_error': True,
                                               'transmission_error_type': error_type})


def create_po_pdf(doc_number):
    """

    """
    context = {}
    po_details = django_query_instance.django_get_query(PoHeader,
                                                        {'doc_number': doc_number,
                                                         'client': global_variables.GLOBAL_CLIENT,
                                                         'del_ind': False})
    guid = po_details.po_header_guid
    address_details = django_query_instance.django_get_query(PoAddresses,
                                                             {'po_header_guid': guid,
                                                              'del_ind': False,
                                                              'address_type': 'D'})
    inv_add_number = po_details.inv_addr_num

    invoice_address = django_query_instance.django_filter_only_query(OrgAddress, {
        'address_number': inv_add_number, 'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
    })

    item_details = django_query_instance.django_filter_only_query(PoItem, {
        'po_header_guid': guid, 'del_ind': False
    })

    accounting_data = django_query_instance.django_filter_only_query(PoAccounting, {
        'po_header_guid': guid, 'del_ind': False, 'client': global_variables.GLOBAL_CLIENT
    })

    requester_details = django_query_instance.django_filter_only_query(UserData, {'username': po_details.requester,
                                                                                  'client': global_variables.GLOBAL_CLIENT})

    context = {
        'po_header_details': po_details,
        'address_details': address_details,
        'invoice_address': invoice_address,
        'po_item_details': item_details,
        'po_accounting_details': accounting_data,
        'requester_details': requester_details,
        'doc_number': doc_number
    }
    return context


def get_po_details(po_header_guid):
    """

    """
    supplier_currency = ''
    actual_price_list = []
    discount_value_list = []
    tax_value_list = []
    company_code = CONST_ALL
    po_header_level_address = ''
    po_header_details = django_query_instance.django_filter_query(PoHeader,
                                                                  {'po_header_guid': po_header_guid,
                                                                   'client': global_variables.GLOBAL_CLIENT},
                                                                  None,
                                                                  None)
    for po_header_detail in po_header_details:
        supplier_details = django_query_instance.django_filter_query(SupplierMaster,
                                                                     {
                                                                         'client': global_variables.GLOBAL_CLIENT,
                                                                         'supplier_id':
                                                                             po_header_detail[
                                                                                 'supplier_id']},
                                                                     None,
                                                                     None)[0]
        po_header_detail['supplier_address'] = supplier_details
        po_header_detail['supplier_description'] = supplier_details['name1']
        company_code = po_header_detail['company_code_id']
        supplier_currency = po_header_detail['currency']
        po_header_detail = get_purchasing_info(po_header_detail, 'po_header_guid')
        if django_query_instance.django_existence_check(UserData,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'username': po_header_detail['requester']}):
            user_details = django_query_instance.django_filter_query(UserData,
                                                                     {'client': global_variables.GLOBAL_CLIENT,
                                                                      'username': po_header_detail['requester']},
                                                                     None,
                                                                     None)[0]
            po_header_detail['requester'] = user_details['first_name'] + ' ' + user_details['last_name']
            po_header_detail['email_id'] = user_details['email']
            po_header_detail['phone_num'] = user_details['phone_num']

    po_item_details = django_query_instance.django_filter_query(PoItem,
                                                                {'po_header_guid': po_header_guid,
                                                                 'client': global_variables.GLOBAL_CLIENT},
                                                                ['po_item_num'],
                                                                None)
    for po_item_detail in po_item_details:
        item_currency = po_item_detail['currency']
        po_item_detail['unit'] = get_description_uom(po_item_detail['unit'])

        if supplier_currency != po_item_detail['currency']:
            # po_item_detail['value'] = convert_currency(po_item_detail['value'], po_item_detail['currency'],
            #                                            supplier_currency)
            actual_price_list.append(
                convert_currency(float(po_item_detail['actual_price']) * po_item_detail['quantity'], str(item_currency),
                                 str(supplier_currency)))
            discount_value_list.append(
                convert_currency(float(po_item_detail['discount_value']), str(item_currency), str(supplier_currency)))
            tax_value_list.append(
                convert_currency(float(po_item_detail['tax_value']), str(item_currency), str(supplier_currency)))

        else:
            actual_price_list.append(float(po_item_detail['actual_price']) * po_item_detail['quantity'])
            discount_value_list.append(float(po_item_detail['discount_value']))
            tax_value_list.append(float(po_item_detail['tax_value']))
        po_item_detail['related_documents'] = get_item_level_related_documents(po_item_detail,
                                                                               CONST_DOC_TYPE_PO,
                                                                               po_item_detail['sc_doc_num'])
        if po_item_detail['call_off'] == CONST_CATALOG_CALLOFF:
            po_item_detail['image_url'] = get_image_url(po_item_detail['int_product_id'])
        else:
            po_item_detail['image_url'] = ''
        if po_item_detail['eform_id']:
            if po_item_detail['call_off'] == CONST_FREETEXT_CALLOFF:
                po_item_detail['eform_data'] = django_query_instance.django_filter_query(EformFieldData,
                                                                                         {
                                                                                             'client': global_variables.GLOBAL_CLIENT,
                                                                                             'del_ind': False,
                                                                                             'eform_type': CONST_FT_ITEM_EFORM,
                                                                                             'po_item_guid':
                                                                                                 po_item_detail[
                                                                                                     'po_item_guid']},
                                                                                         None,
                                                                                         None)
            elif po_item_detail['call_off'] == CONST_CATALOG_CALLOFF:
                po_item_detail['eform_data'] = django_query_instance.django_filter_query(EformFieldData,
                                                                                         {
                                                                                             'client': global_variables.GLOBAL_CLIENT,
                                                                                             'del_ind': False,
                                                                                             'eform_type': CONST_CATALOG_ITEM_VARIANT,
                                                                                             'po_item_guid':
                                                                                                 po_item_detail[
                                                                                                     'po_item_guid']},
                                                                                         None,
                                                                                         None)
        print(po_item_detail['related_documents'])
        po_item_detail = get_purchasing_info(po_item_detail, 'po_item_guid')
    po_item_guid_list = dictionary_key_to_list(po_item_details, 'po_item_guid')
    supplier_note = django_query_instance.django_filter_query(Notes,
                                                              {'client': global_variables.GLOBAL_CLIENT,
                                                               'del_ind': False,
                                                               'note_type': CONST_SUPPLIER_NOTE,
                                                               'item_guid__in': po_item_guid_list},
                                                              ['item_num'],
                                                              None)
    internal_note = django_query_instance.django_filter_query(Notes,
                                                              {'client': global_variables.GLOBAL_CLIENT,
                                                               'del_ind': False,
                                                               'note_type': CONST_INTERNAL_NOTE,
                                                               'item_guid__in': po_item_guid_list},
                                                              ['item_num'],
                                                              None)
    po_attachments = get_po_item_attachments(po_item_guid_list)
    po_accounting_details = django_query_instance.django_filter_query(PoAccounting,
                                                                      {'po_item_guid__in': po_item_guid_list,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      ['acc_item_num'],
                                                                      None)
    for po_accounting_detail in po_accounting_details:
        get_acc_value_desc_update(po_accounting_detail, company_code)
        po_accounting_detail['acc_cat'] = get_accounting_description(po_accounting_detail['acc_cat'])
        po_accounting_detail['gl_acc_num'] = get_gl_acc_description(po_accounting_detail['gl_acc_num'], company_code)
    for po_header_detail in po_header_details:
        po_header_detail['guid'] = po_header_detail['po_header_guid']
        del po_header_detail['po_header_guid']
        po_header_detail['created_at'] = po_header_detail['po_header_created_at']
        del po_header_detail['po_header_created_at']
        po_header_detail['created_by'] = po_header_detail['po_header_created_by']
        del po_header_detail['po_header_created_by']
    sc_header, sc_appr, sc_completion, requester_first_name = get_po_header_app(po_header_details,
                                                                                global_variables.GLOBAL_CLIENT)
    for sc_appr_detail in sc_appr:
        sc_appr_detail['header_guid_id'] = sc_appr_detail['po_header_guid_id']
        del sc_appr_detail['po_header_guid_id']
    if django_query_instance.django_existence_check(PoAddresses,
                                                    {'po_header_guid': po_header_guid,
                                                     'client': global_variables.GLOBAL_CLIENT,
                                                     'address_type': 'D'}):
        po_header_level_address = django_query_instance.django_filter_query(PoAddresses,
                                                                            {'po_header_guid': po_header_guid,
                                                                             'client': global_variables.GLOBAL_CLIENT,
                                                                             'address_type': 'D'},
                                                                            None,
                                                                            None)[0]

    po_item_level_address = django_query_instance.django_filter_query(PoAddresses,
                                                                      {'po_item_guid__in': po_item_guid_list,
                                                                       'client': global_variables.GLOBAL_CLIENT,
                                                                       'address_type': 'D'
                                                                       },
                                                                      ['item_num'],
                                                                      None)
    actual_price = sum(actual_price_list)
    discount_value = sum(discount_value_list)
    tax_value = sum(tax_value_list)
    context = {'po_header_details': po_header_details,
               'po_item_details': po_item_details,
               'actual_price': actual_price,
               'discount_value': discount_value,
               'tax_value': tax_value,
               'po_accounting_details': po_accounting_details,
               'sc_appr': sc_appr,
               'sc_head': sc_header[0],
               'sc_completion': sc_completion,
               'requester_first_name': requester_first_name,
               'po_header_level_address': po_header_level_address,
               'po_item_level_address': po_item_level_address,
               'supplier_notes': supplier_note,
               'internal_notes': internal_note,
               'po_attachments': po_attachments,
               }
    return context


def get_purchasing_info(doc_detail, field_name):
    """

    """

    porg_data = django_query_instance.django_filter_value_list_query(PurchasingData,
                                                                     {'client': global_variables.GLOBAL_CLIENT,
                                                                      field_name: doc_detail[field_name]}, 'purch_org')
    porg_data = distinct_list(porg_data)
    if len(porg_data) > 1:
        doc_detail['porg_description'] = CONST_MULTIPLE
        doc_detail['pgrp_description'] = CONST_MULTIPLE
    elif django_query_instance.django_existence_check(PurchasingData,
                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                       field_name: doc_detail[field_name]}):
        purchaser_detail = django_query_instance.django_filter_query(PurchasingData,
                                                                     {'client': global_variables.GLOBAL_CLIENT,
                                                                      field_name: doc_detail[
                                                                          field_name]},
                                                                     None,
                                                                     None)[0]
        if django_query_instance.django_existence_check(OrgPorg,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'porg_id': purchaser_detail['purch_org']}):
            porg_description = django_query_instance.django_filter_value_list_query(OrgPorg,
                                                                                    {
                                                                                        'client': global_variables.GLOBAL_CLIENT,
                                                                                        'porg_id': purchaser_detail[
                                                                                            'purch_org']},
                                                                                    'description')[0]

            doc_detail['porg_description'] = purchaser_detail['purch_org'] + ' - ' + porg_description
        else:
            doc_detail['porg_description'] = purchaser_detail['purch_org']

        if django_query_instance.django_existence_check(OrgPGroup,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'pgroup_id': purchaser_detail['purch_grp']}):
            pgrp_description = django_query_instance.django_filter_value_list_query(OrgPGroup,
                                                                                    {
                                                                                        'client': global_variables.GLOBAL_CLIENT,
                                                                                        'pgroup_id': purchaser_detail[
                                                                                            'purch_grp']},
                                                                                    'description')[0]

            doc_detail['pgrp_description'] = purchaser_detail['purch_grp'] + ' - ' + pgrp_description
        else:
            doc_detail['pgrp_description'] = purchaser_detail['purch_grp']
    return doc_detail


def save_po_item_level_supp_int_note(item_guid, po_item_guid, loop_counter):
    """

    """
    if django_query_instance.django_existence_check(Notes,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'document_type': CONST_DOC_TYPE_SC,
                                                     'item_guid': item_guid}):
        notes_details = django_query_instance.django_filter_query(Notes,
                                                                  {'client': global_variables.GLOBAL_CLIENT,
                                                                   'document_type': CONST_DOC_TYPE_SC,
                                                                   'item_guid': item_guid}, None,
                                                                  None)
        for notes_detail in notes_details:
            notes_detail['guid'] = guid_generator()
            notes_detail['item_guid'] = po_item_guid
            notes_detail['item_num'] = loop_counter + 1
            del notes_detail['document_type_id']
            notes_detail['document_type'] = django_query_instance.django_get_query(DocumentType,
                                                                                   {'document_type': CONST_DOC_TYPE_PO})
            django_query_instance.django_create_query(Notes, notes_detail)


def save_po_header_level_notes(guid, po_header_guid):
    """

    """
    if django_query_instance.django_existence_check(Notes,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'document_type': CONST_DOC_TYPE_SC,
                                                     'header_guid': guid}):
        notes_details = django_query_instance.django_filter_query(Notes,
                                                                  {'client': global_variables.GLOBAL_CLIENT,
                                                                   'document_type': CONST_DOC_TYPE_SC,
                                                                   'header_guid': guid},
                                                                  None,
                                                                  None)
        for notes_detail in notes_details:
            notes_detail['guid'] = guid_generator()
            notes_detail['header_guid'] = po_header_guid
            notes_detail['item_num'] = 0
            del notes_detail['document_type_id']
            notes_detail['document_type'] = django_query_instance.django_get_query(DocumentType,
                                                                                   {'document_type': CONST_DOC_TYPE_PO})
            django_query_instance.django_create_query(Notes, notes_detail)


def save_attachments(sc_item_guid, sc_header_guid, po_item_guid, po_header_guid, loop_counter, po_document_number):
    """

    """
    if django_query_instance.django_existence_check(Attachments,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'item_guid': sc_item_guid,
                                                     'header_guid': sc_header_guid}):
        attachment_details = django_query_instance.django_filter_query(Attachments,
                                                                       {'client': global_variables.GLOBAL_CLIENT,
                                                                        'item_guid': sc_item_guid,
                                                                        'header_guid': sc_header_guid},
                                                                       None, None)
        for attachment_detail in attachment_details:
            attachment_detail['guid'] = guid_generator()
            attachment_detail['item_num'] = loop_counter
            attachment_detail['doc_num'] = po_document_number
            print("attachment guid: ", attachment_detail['guid'])
            del attachment_detail['document_type_id']
            attachment_detail['document_type'] = django_query_instance.django_get_query(DocumentType,
                                                                                        {
                                                                                            'document_type': CONST_DOC_TYPE_PO})
            attachment_detail['item_guid'] = po_item_guid
            attachment_detail['header_guid'] = po_header_guid
            django_query_instance.django_create_query(Attachments, attachment_detail)


def get_po_item_attachments(item_guid_list):
    available_attachments = django_query_instance.django_filter_query(Attachments,
                                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                                       'item_guid__in': item_guid_list,
                                                                       'del_ind': False}, ['item_num'], None)
    attachment_data = []
    if available_attachments:
        attachment_file_path = available_attachments
        for attachments in attachment_file_path:
            item_guid = attachments['item_guid']
            file_path = str(attachments['doc_file'])
            split_file_path = file_path.split('/')
            file_path = '/'.join(split_file_path[:-1])
            file_path = 'media/' + file_path
            GetAttachments.get_all_files(file_path, item_guid)
            file_name = split_file_path[6]
            attachment_dict = {
                'attachment_guid': attachments['guid'],
                'item_guid': attachments['item_guid'],
                'file_name': file_name,
                'file_path': file_path + '/' + file_name,
                'attachment_name': attachments['title'],
                'type': attachments['attach_type_flag'],
                'item_num': attachments['item_num'],
            }
            attachment_data.append(attachment_dict)
    return attachment_data


def update_po_item_guid_eform(po_item_guid, sc_item_guid):
    """

    """

    django_query_instance.django_update_query(EformFieldData,
                                              {'client': global_variables.GLOBAL_CLIENT,
                                               'item_guid': sc_item_guid},
                                              {'po_item_guid': django_query_instance.django_get_query(PoItem,
                                                                                                      {
                                                                                                          'po_item_guid': po_item_guid})})


def retrigger_po(doc_list):
    """

    """
    reprocessing_list = []
    invalid_list = []
    for document in doc_list:
        sc_header_instance = django_query_instance.django_get_query(ScHeader,
                                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                                     'doc_number': document['doc_number']})
        if sc_header_instance:
            create_purchase_order = CreatePurchaseOrder(sc_header_instance)
            status, error_message, output, po_doc_list = create_purchase_order.create_po()
            for po_document_number in po_doc_list:
                email_supp_monitoring_guid = ''
                send_po_attachment_email(output, po_document_number, email_supp_monitoring_guid)
            if error_message:
                document['error_message'] = error_message
                document['error_type'] = CONST_VALIDATION_ERROR
                invalid_list.append(document)
            else:

                sc_header_instance.transmission_error = False
                sc_header_instance.transmission_error_type = None
                sc_header_instance.save()
        else:
            reprocessing_list.append({'doc_number': sc_header_instance['doc_number'],
                                      'error_type': CONST_NOT_FOUND_ERROR})
    reprocessing_list = reprocessing_list + invalid_list
    return reprocessing_list


def check_po(sc_header_details):
    """

    """
    valid_list = []
    invalid_list = []
    for sc_header_instance in sc_header_details:
        po_split_list = get_po_split_type(sc_header_instance['co_code'])
        if CONST_PO_SPLIT_SUPPLIER not in po_split_list:
            invalid_list.append({'doc_number': sc_header_instance['doc_number'],
                                 'error_type': CONST_ERROR_SPLIT_CRITERIA,
                                 'company_code_id': sc_header_instance['co_code']})
        else:
            valid_list.append({'doc_number': sc_header_instance['doc_number'],
                               'company_code_id': sc_header_instance['co_code'],
                               'error_type': 'Read to Process'})
        invalid_doc_list = dictionary_key_to_list(invalid_list, 'doc_number')
        if sc_header_instance['doc_number'] not in invalid_doc_list:
            # Transaction type validation
            requester_obj_id = requester_field_info(sc_header_instance['requester'], 'object_id')
            object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT, requester_obj_id)
            po_document_number, sequence, po_transaction_type = generate_document_number(CONST_PO_TRANS_TYPE,
                                                                                         global_variables.GLOBAL_CLIENT,
                                                                                         object_id_list,
                                                                                         False,
                                                                                         CONST_DOC_TYPE_PO)

            if not po_document_number:
                if sc_header_instance['doc_number'] not in invalid_doc_list:
                    invalid_list.append({'doc_number': sc_header_instance['doc_number'],
                                         'error_type': CONST_ERROR_TRANSACTION_TYPE,
                                         'error_description': MSG0120,
                                         'company_code_id': sc_header_instance['co_code']})
            else:
                doc_list = dictionary_key_to_list(valid_list, 'doc_number')
                if sc_header_instance['doc_number'] not in doc_list:
                    valid_list.append({'doc_number': sc_header_instance['doc_number'],
                                       'company_code_id': sc_header_instance['co_code'],
                                       'error_type': 'Read to Process'})
    processing_list = {'invalid_list': invalid_list,
                       'valid_list': valid_list}
    reprocess_invalid_list = retrigger_po(valid_list)
    processing_list['invalid_list'] = reprocess_invalid_list + invalid_list
    return processing_list


def check_for_po_creation(sc_item_detail):
    """

    """
    po_creation_flag = True
    if sc_item_detail['po_doc_num']:
        po_creation_flag = False
    return po_creation_flag
