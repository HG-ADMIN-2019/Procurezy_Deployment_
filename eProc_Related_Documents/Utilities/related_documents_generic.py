from eProc_Basic.Utilities.constants.constants import CONST_DOC_TYPE_PO, CONST_DOC_TYPE_SC
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import encrypt
from eProc_Basic.Utilities.functions.get_description import get_description_uom
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Purchase_Order.models import PoItem, PoHeader
from eProc_Shopping_Cart.models import ScItem, ScHeader

django_query_instance = DjangoQueries()


def get_item_level_related_documents(item_detail, document_types, document_number):
    """

    """
    item_details = []
    if document_types == CONST_DOC_TYPE_PO:
        item_details = django_query_instance.django_filter_query(ScItem,
                                                                 {'client': global_variables.GLOBAL_CLIENT,
                                                                  'po_item_guid': item_detail['po_item_guid']},
                                                                 None,
                                                                 None)
        for item_detail in item_details:
            item_detail['document_number'] = document_number
            item_detail['document'] = 'Shopping Cart'
            item_detail['encrypt_header_guid'] = encrypt(item_detail['header_guid_id'])
            sc_header_instance = django_query_instance.django_get_query(ScHeader,
                                                                        {'guid': item_detail[
                                                                            'header_guid_id'],
                                                                         'client': global_variables.GLOBAL_CLIENT})
            item_detail['status'] = sc_header_instance.status
            item_detail['created_at'] = sc_header_instance.created_at
            item_detail['sc_name'] = sc_header_instance.description
            item_detail['unit'] = get_description_uom(item_detail['unit'])
    if document_types == CONST_DOC_TYPE_SC:
        item_details = django_query_instance.django_filter_query(PoItem,
                                                                 {'client': global_variables.GLOBAL_CLIENT,
                                                                  'sc_item_guid': item_detail['guid']},
                                                                 None,
                                                                 None)
        for item_detail in item_details:
            item_detail['document_number'] = document_number
            item_detail['document'] = 'Purchase Order'
            item_detail['encrypt_header_guid'] = encrypt(item_detail['po_header_guid_id'])
            po_header_instance = django_query_instance.django_get_query(PoHeader,
                                                                        {'po_header_guid': item_detail[
                                                                            'po_header_guid_id'],
                                                                         'client': global_variables.GLOBAL_CLIENT})
            item_detail['status'] = po_header_instance.status
            item_detail['created_at'] = po_header_instance.po_header_created_at
            item_detail['po_name'] = po_header_instance.description
            item_detail['unit'] = get_description_uom(item_detail['unit'])
    return item_details
