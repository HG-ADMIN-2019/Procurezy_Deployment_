"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    number_ranges.py
Usage:
     get_number_ranges          - Renders number ranges html to edit or create number ranges
     edit_create_number_ranges  - Function to update or create number ranges
Author:
    Sanjay
"""

from itertools import chain
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.messages.messages import MSG126
from eProc_Configuration.models import NumberRanges
from eProc_Configuration.models.development_data import *
from eProc_Basic.Utilities.constants.constants import CONST_DOC_TYPE_SC
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.guid_generator import guid_generator


# Function to get number ranges and transaction type data from DB
def get_number_ranges(request):
    """
    :param request: Gets data from UI
    :return: Returns combined and serialized queryset
    """
    client = getClients(request)
    number_ranges = NumberRanges.objects.filter(document_type=CONST_DOC_TYPE_SC, client=client)
    transaction_types = TransactionTypes.objects.filter(document_type=CONST_DOC_TYPE_SC, client=client)
    get_data = list(chain(number_ranges, transaction_types))
    serialized_data = serializers.serialize('json', get_data)
    return HttpResponse(serialized_data, content_type='application/json')


# Function to edit or create number ranges
def edit_create_number_ranges(request):
    """
    :param request: Gets the number range data to create or update
    :return: Updated data
    """

    client = getClients(request)
    sc_number_ranges = JsonParser().get_json_from_req(request)
    # If condition to check if all number ranges are deleted in UI
    if sc_number_ranges == 'Delete all number ranges':
        NumberRanges.objects.filter(client=client).delete()
    else:
        for number_ranges in sc_number_ranges:
            for sequence in number_ranges['sequence_delete']:
                # if condition to delete number ranges
                if sequence is not None and sequence != '':
                    NumberRanges.objects.filter(sequence=sequence, client=client).delete()

            guid = number_ranges['guid']
            #  If guid is empty create number range or update existing number range
            if guid == '':
                guid = guid_generator()

            NumberRanges.objects.update_or_create(guid=guid, defaults={
                'guid': guid,
                'document_type': DocumentType.objects.get(document_type=CONST_DOC_TYPE_SC),
                'sequence': number_ranges['sequence'],
                'starting': number_ranges['starting'],
                'ending': number_ranges['ending'],
                'current': number_ranges['current'],
                'client_id': OrgClients.objects.get(client=client)
            }, )
            msgid = 'MSG126'
            error_msg = get_message_desc(msgid)[1]
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            return JsonResponse({'message': error_msg})
