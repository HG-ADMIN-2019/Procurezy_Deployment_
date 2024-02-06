"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    number_ranges.py
Usage:
     get_transaction_type           - Renders number ranges html to edit or create transaction type
     edit_create_transaction_types  - Function to update or create transaction type
Author:
    Sanjay
"""

from itertools import chain
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.messages.messages import MSG127
from eProc_Configuration.models import NumberRanges
from eProc_Configuration.models.development_data import *
from eProc_Basic.Utilities.constants.constants import CONST_DOC_TYPE_SC
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.guid_generator import guid_generator


# Function to get transaction type from DB
def get_transaction_type(request):
    """
    :param request: Gets POST data from UI
    :return: Combined and serialized queryset
    """
    client = getClients(request)
    number_ranges = NumberRanges.objects.filter(document_type=CONST_DOC_TYPE_SC, client=client)
    transaction_types = TransactionTypes.objects.filter(document_type=CONST_DOC_TYPE_SC, client=client)
    get_data = list(chain(number_ranges, transaction_types))
    serialized_qs = serializers.serialize('json', get_data)
    return HttpResponse(serialized_qs, content_type='application/json')


# Function to edit or create transaction types
def edit_create_transaction_types(request):
    """
    :param request:  Gets POST data from UI
    :return: Returns a success message on successful updating or creating
    """
    sc_trans_type = JsonParser().get_json_from_req(request)

    transtype_not_exist: object = TransactionTypes.objects.filter(del_ind=False).exclude(
        transaction_type__in=[transtype['transaction_type'] for transtype in sc_trans_type])
    # print(sc_trans_type)
    for set_del_int in transtype_not_exist:
        set_del_int.del_ind = True
        set_del_int.save()

    for transaction_type in sc_trans_type:
        guid = transaction_type['guid']
        if guid == '':
            guid = guid_generator()
        status = False

        print(status)
        if transaction_type['status'] == 'Active':
            status = True
        elif transaction_type['status'] == 'Inactive':
            status = False

        TransactionTypes.objects.update_or_create(guid=guid, defaults={
            'guid': guid,
            'document_type': DocumentType.objects.get(document_type=CONST_DOC_TYPE_SC),
            'transaction_type': transaction_type['transaction_type'],
            'description': transaction_type['description'],
            'sequence': transaction_type['sequence'],
            'active_inactive': status,
            'del_ind': False,
            'client_id': OrgClients.objects.get(client=getClients(request))
        }, )

    msgid = 'MSG127'
    error_msg = get_message_desc(msgid)[1]
    # msg = error_msg['message_desc'][0]
    # error_msg = msg
    return JsonResponse({'message': error_msg})
