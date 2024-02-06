from eProc_Account_Assignment.Utilities.account_assignment_specific import remove_insert
from eProc_Basic.Utilities.constants.constants import CONST_DEL_ADDR
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.str_concatenate import concatenate_str, concatenate_array_str
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import OrgAddressMap, OrgAddress

django_query_instance = DjangoQueries()


class Address_desc:

    @staticmethod
    def get_addr_description(client, attr_value_list, attr_id, addr_type):
        addr_detail = []

        if django_query_instance.django_existence_check(OrgAddressMap, {'address_number__in': attr_value_list,
                                                                        'del_ind': False}):

            addr_values = django_query_instance.django_filter_value_list_query(OrgAddressMap, {
                'address_number__in': attr_value_list,
                'del_ind': False,
                'address_type': addr_type,
                'client': client
            }, 'address_number')

            addr_detail = django_query_instance.django_filter_only_query(OrgAddress, {
                'address_number__in': addr_values, 'client': client,'del_ind':False
            }).values()

        return addr_detail

    @staticmethod
    def append_addr_desc(addr_details, addr_default_value):
        attr_val = []
        attr_desc = []
        addr_append_default_val_desc = None
        addr_append_val_desc = ''
        if addr_details:
            for addr_detail in addr_details:
                desc_value = addr_detail['street'] + ' \n ' + addr_detail['area'] + ' / ' + addr_detail[
                    'landmark'] + ' / ' + addr_detail['city'] + ' / ' + addr_detail['postal_code'] + ' / ' + \
                             addr_detail['region']
                if addr_default_value:
                    if int(addr_default_value) == addr_detail['address_number']:
                        addr_append_default_val_desc = concatenate_str(str(addr_detail['address_number']),
                                                                       str(desc_value))

                attr_val.append(str(addr_detail['address_number']))
                attr_desc.append(desc_value)
            addr_append_val_desc = concatenate_array_str(attr_val, attr_desc)
            if addr_append_default_val_desc:
                addr_append_val_desc = remove_insert(addr_append_val_desc, addr_append_default_val_desc)

        return addr_append_val_desc, [addr_append_default_val_desc]


def get_shipping_drop_down(addr_value, addr_default_value):
    """
    get_shipping_drop_down
    :return: delivery_addr_list,addr_default,addr_val_desc
    """
    delivery_addr_list = ''
    addr_default = ''
    addr_val_desc = ''

    if addr_value:
        if addr_default_value:
            add_default_address_value = [addr_default_value]
            addr_val_desc = Address_desc.get_addr_description(global_variables.GLOBAL_CLIENT, add_default_address_value,
                                                              CONST_DEL_ADDR, 'D')
        delivery_addr_desc = Address_desc.get_addr_description(global_variables.GLOBAL_CLIENT, addr_value,
                                                               CONST_DEL_ADDR, 'D')
        delivery_addr_list, addr_default = Address_desc.append_addr_desc(delivery_addr_desc, addr_default_value)

    return delivery_addr_list, addr_default, addr_val_desc
