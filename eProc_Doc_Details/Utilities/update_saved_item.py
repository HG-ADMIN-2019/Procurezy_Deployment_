from eProc_Add_Item.views import save_eform_data
from eProc_Attributes.Utilities.attributes_generic import OrgAttributeValues
from eProc_Basic.Utilities.constants.constants import CONST_CALENDAR_ID, CONST_PR_CALLOFF, CONST_SC_HEADER_SAVED
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import get_requester_currency, get_object_id_from_username
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG124
from eProc_Calendar_Settings.Utilities.calender_settings_generic import calculate_delivery_date
from eProc_Doc_Details.Utilities.details_specific import get_approver_list
from eProc_Exchange_Rates.Utilities.exchange_rates_generic import convert_currency
from eProc_Price_Calculator.Utilities.price_calculator_generic import calculate_item_total_value, calculate_item_price
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import get_prod_by_id, \
     get_price_discount_tax
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import get_manger_detail, get_highest_acc_detail, \
    delete_approver_detail
from eProc_Shopping_Cart.context_processors import update_user_obj_id_list_info
from eProc_Shopping_Cart.models import ScItem, ScHeader
from eProc_User_Settings.Utilities.user_settings_generic import get_object_id_list_user
from eProc_Workflow.Utilities.work_flow_generic import save_sc_approval

django_query_instance = DjangoQueries()


class UpdateSavedItem:
    def __init__(self, sc_header_guid, item_guid):
        self.sc_header_guid = sc_header_guid
        self.sc_header_instance = django_query_instance.django_get_query(ScHeader, {'pk': sc_header_guid})
        self.requester = self.sc_header_instance.requester if self.sc_header_instance is not None else None
        self.requester_currency = get_requester_currency(self.requester)
        self.item_guid = item_guid
        self.get_item_instance = django_query_instance.django_get_query(ScItem, {'guid': self.item_guid})
        self.company_code = self.get_item_instance.comp_code if self.get_item_instance is not None else None
        self.requester_object_id = get_object_id_from_username(self.requester)
        self.org_attr_value_instance = OrgAttributeValues()

    def update_limit_item(self, update_item_detail):
        item_details = {}
        overall_limit = update_item_detail['overall_limit']
        expected_value = update_item_detail['expected_value']
        description = update_item_detail['description']
        prod_cat = update_item_detail['prod_cat']
        currency = update_item_detail['currency']
        supplier_id = update_item_detail['supplier_id']
        follow_up_action = update_item_detail['follow_up_action']

        item_details['cmp_code'] = self.company_code
        prod_cat_desc = get_prod_by_id(prod_cat)

        item_details['overall_limit'] = overall_limit
        item_details['expected_value'] = expected_value
        item_details['description'] = description
        item_details['prod_cat'] = prod_cat
        item_details['prod_cat_desc'] = prod_cat_desc
        item_details['supplier_id'] = supplier_id
        item_details['currency'] = currency

        if follow_up_action == 'Invoice & Confirmation Only':
            item_details['ir_gr_ind_limi'] = True
            item_details['gr_ind_limi'] = False
        else:
            item_details['ir_gr_ind_limi'] = False
            item_details['gr_ind_limi'] = True

        required = update_item_detail['required']
        start_date = update_item_detail['start_date']
        end_date = update_item_detail['end_date']
        item_del_date = update_item_detail['item_del_date']

        if required == 'On':
            item_details['start_date'] = None
            item_details['end_date'] = None
            item_details['item_del_date'] = item_del_date

        if required == 'From':
            item_details['item_del_date'] = None
            item_details['end_date'] = None
            item_details['start_date'] = start_date

        if required == 'Between':
            item_details['item_del_date'] = None
            item_details['end_date'] = end_date
            item_details['start_date'] = start_date

        item_value_converted = convert_currency(overall_limit, currency, self.requester_currency)

        item_details['value'] = item_value_converted
        item_details['acc_type'] = update_item_detail['account_assignment_category']
        item_details['acc_value'] = update_item_detail['account_assignment_value']
        item_details['total_sc_value'] = item_value_converted
        item_details['follow_up_action'] = follow_up_action
        manager_detail = get_approver_list(item_details)

        return item_details, manager_detail, item_value_converted

    def update_pr_item(self, update_item_detail):
        item_details = {}
        item_value_object = update_item_detail['item_value_object']
        call_off = update_item_detail['call_off']
        description = update_item_detail['description']
        int_product_id = update_item_detail['int_product_id']
        update_user_obj_id_list_info()
        object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT, self.requester_object_id)

        default_calendar_id = self.org_attr_value_instance.get_user_default_attr_value_list_by_attr_id(object_id_list,
                                                                                                       CONST_CALENDAR_ID)[
            1]

        if not int_product_id:
            ext_product_id = None

        price = update_item_detail['price']
        prod_cat = update_item_detail['prod_cat_id']
        prod_cat_desc = get_prod_by_id(prod_cat)
        currency = update_item_detail['currency']
        unit = update_item_detail['unit']
        lead_time = update_item_detail['lead_time']
        quantity = update_item_detail['quantity']
        account_assignment_category = update_item_detail['account_assignment_category']
        account_assignment_value = update_item_detail['account_assignment_value']

        item_total_value = calculate_item_total_value(call_off, quantity, None, 1, price, None)
        if currency != self.requester_currency:
            item_total_value = convert_currency(item_total_value, currency, self.requester_currency)
        if item_total_value:
            item_value_object[self.item_guid] = item_total_value

            for key in item_value_object.keys():
                item_value_object[key] = float(item_value_object[key])

            item_value = list(item_value_object.values())
            total_sc_value = sum(item_value)

            item_details['description'] = description
            item_details['int_product_id'] = int_product_id
            item_details['value'] = item_total_value
            item_details['prod_cat_desc'] = prod_cat_desc
            item_details['unit'] = unit
            item_details['lead_time'] = lead_time
            item_details['cmp_code'] = self.company_code
            item_details['acc_type'] = account_assignment_category
            item_details['acc_value'] = account_assignment_value
            item_details['total_sc_value'] = total_sc_value
            item_details['price'] = price
            item_details['quantity'] = quantity
            item_details['currency'] = currency

            item_delivery_date = calculate_delivery_date(self.item_guid,
                                                         int(lead_time),
                                                         None,
                                                         default_calendar_id,
                                                         global_variables.GLOBAL_CLIENT,
                                                         ScItem)

            item_with_highest_value = max(item_value_object, key=item_value_object.get)
            django_query_instance.django_update_query(ScItem,
                                                      {'guid': update_item_detail['guid'],
                                                       'client': global_variables.GLOBAL_CLIENT,
                                                       'del_ind': False},
                                                      {'price': price,
                                                       'base_price':price,
                                                       'actual_price':price,
                                                       'int_product_id':int_product_id,
                                                       'quantity': quantity,
                                                       'value': item_total_value,
                                                       'description': description,
                                                       'prod_cat_id': update_item_detail['prod_cat_id'],
                                                       'currency': update_item_detail['currency'],
                                                       'unit': update_item_detail['unit'],
                                                       'lead_time': update_item_detail['lead_time']})
            django_query_instance.django_update_query(ScHeader,
                                                      {'guid': update_item_detail['sc_header_guid'],
                                                       'client': global_variables.GLOBAL_CLIENT},
                                                      {'total_value': total_sc_value})
            return item_details, total_sc_value, item_with_highest_value, item_delivery_date

        else:
            msgid = 'MSG124'
            error_msg = get_message_desc(msgid)[1]

        return False, error_msg, None, None

    def update_saved_freetext_item(self, update_item_detail):
        item_details = {}
        eform_details = {}
        item_ui_data = update_item_detail['cart_item_data']
        quantity = item_ui_data['quantity']
        price = item_ui_data['price']
        call_off = update_item_detail['call_off']
        guid = item_ui_data['guid']
        currency = self.get_item_instance.currency
        item_value_object = update_item_detail['item_value_object']

        item_total_value = calculate_item_total_value(call_off, quantity, None, 1, price, None)
        if currency != self.requester_currency:
            item_total_value = convert_currency(item_total_value, currency, self.requester_currency)
        item_ui_data['value'] = item_total_value
        django_query_instance.django_update_query(ScItem, {'guid': guid}, item_ui_data)
        if item_total_value:
            item_value_object[self.item_guid] = item_total_value

            for key in item_value_object.keys():
                item_value_object[key] = float(item_value_object[key])

            item_value = list(item_value_object.values())
            total_sc_value = sum(item_value)

            item_with_highest_value = max(item_value_object, key=item_value_object.get)
            save_eform_data(update_item_detail['eform_data'])
            item_details['total_sc_value'] = total_sc_value
            item_details['quantity'] = quantity
            item_details['value'] = item_total_value
            item_details['price'] = price
            django_query_instance.django_update_query(ScHeader,
                                                      {'client':global_variables.GLOBAL_CLIENT,
                                                       'guid':update_item_detail['sc_header_guid']},
                                                      {'total_value':total_sc_value,
                                                       'gross_amount':total_sc_value})
            return item_details, eform_details, item_value, item_with_highest_value, total_sc_value

        else:
            msgid = 'MSG124'
            error_msg = get_message_desc(msgid)[1]

        return False, error_msg, None, None

    def update_saved_catalog_item(self, update_item_detail):
        item_details = {}
        quantity = update_item_detail['quantity']
        price = update_item_detail['price']
        call_off = update_item_detail['call_off']
        guid = update_item_detail['guid']

        sc_item_instance = django_query_instance.django_get_query(ScItem, {'guid': guid})
        currency = sc_item_instance.currency
        item_value_object = update_item_detail['item_value_object']
        if sc_item_instance.variant_id:
            price, discount_percentage, base_price, additional_pricing = calculate_item_price(guid, quantity)
        else:
            discount_percentage = 0
            base_price = price
            additional_pricing = 0

        actual_price, discount_value, tax_value, gross_price = get_price_discount_tax(price,
                                                                                      base_price,
                                                                                      additional_pricing,
                                                                                      None,
                                                                                      discount_percentage,
                                                                                      quantity)
        item_total_value = calculate_item_total_value(call_off, quantity, None, 1, price, None)
        if currency != self.requester_currency:
            item_total_value = convert_currency(item_total_value, currency, self.requester_currency)
        if item_total_value:
            item_value_object[self.item_guid] = item_total_value

        for key in item_value_object.keys():
            item_value_object[key] = float(item_value_object[key])

        item_value = list(item_value_object.values())
        total_sc_value = sum(item_value)
        item_with_highest_value = max(item_value_object, key=item_value_object.get)

        item_details['total_sc_value'] = total_sc_value
        item_details['catalog_qty'] = quantity
        item_details['value'] = item_total_value
        item_details['acc_type'] = ''
        item_details['acc_value'] = ''
        item_details['total_sc_value'] = ''
        item_details['price'] = price
        item_details['discount_percentage'] = discount_percentage
        item_details['discount_value'] = discount_value
        item_details['gross_price'] = gross_price
        sc_item_instance.price = price
        sc_item_instance.discount_percentage = discount_percentage
        sc_item_instance.discount_value = discount_value
        sc_item_instance.gross_price = gross_price
        sc_item_instance.base_price = base_price
        sc_item_instance.actual_price = actual_price
        sc_item_instance.catalog_qty = quantity
        sc_item_instance.quantity = quantity
        sc_item_instance.value = item_total_value
        sc_item_instance.save()
        django_query_instance.django_update_query(ScHeader,
                                                  {'guid': sc_item_instance.header_guid,
                                                   'client': global_variables.GLOBAL_CLIENT},
                                                  {'total_value': total_sc_value})
        # save ScApproval data
        account_assignment_category, account_assignment_value = get_highest_acc_detail(self.sc_header_guid)
        approval_data = get_manger_detail(global_variables.GLOBAL_CLIENT, self.sc_header_instance.requester,
                                          account_assignment_category, self.sc_header_instance.total_value,
                                          self.sc_header_instance.co_code,
                                          account_assignment_value,
                                          global_variables.GLOBAL_USER_CURRENCY)
        # Save Approver detail
        delete_approver_detail(self.sc_header_guid)
        sc_completion_flag = False
        if django_query_instance.django_existence_check(ScItem, {'client': global_variables.GLOBAL_CLIENT,
                                                                 'del_ind': False,
                                                                 'header_guid': self.sc_header_guid,
                                                                 'call_off': CONST_PR_CALLOFF}):
            sc_completion_flag = True
        save_sc_approval(approval_data[0], self.sc_header_guid, CONST_SC_HEADER_SAVED, sc_completion_flag)
        return item_details, item_total_value, total_sc_value, item_with_highest_value

    def save_to_db_onclick(self, item_details):
        django_query_instance.django_update_query(ScItem, {'guid': self.item_guid}, item_details)
