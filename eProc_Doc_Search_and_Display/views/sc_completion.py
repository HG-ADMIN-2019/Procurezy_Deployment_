from django.shortcuts import render

from eProc_Basic.Utilities.constants.constants import CONST_DOC_TYPE_SC
from eProc_Basic.Utilities.functions.encryption_util import encrypt
from eProc_Basic.Utilities.functions.get_db_query import requester_field_info
from eProc_Doc_Search_and_Display.Utilities.search_display_specific import get_header_based_on_calloff, DocumentSearch
from eProc_Shopping_Cart.context_processors import update_user_info
import datetime
from datetime import date, timedelta


def sc_completion_doc_search(request):
    document_search_instance = DocumentSearch('', '')
    update_user_info(request)
    context = {
        'inc_nav': True,
        'shopping': True,
        'is_slide_menu': True,
        'is_purchase_active': True,
    }

    if request.method == 'GET':
        encrypted_header_guid = []
        search_fields = {}
        from_date = date.today() - timedelta(days=0)
        # from_date = date.today()
        timeframe = 'Today'
        search_fields['timeframe'] = timeframe
        search_fields['document_number'] = ''
        search_fields['sc_name'] = ''
        search_fields['document_type'] = CONST_DOC_TYPE_SC

        search_criteria = document_search_instance.define_search_criteria(search_fields, 'sc_completion')
        sc_header_details = get_header_based_on_calloff(search_criteria)
        # sc_header_details = get_header_based_on_calloff(search_fields)
        print(sc_header_details)

        for header_guid in sc_header_details:
            created_at_date = header_guid['created_at']
            header_guid['created_at'] = created_at_date.strftime("%d %B %Y ")
            header_guid['first_name'] = requester_field_info(header_guid['created_by'], 'first_name')
            encrypted_header_guid.append(encrypt(header_guid['guid']))
        doc_type = 'SC'
        sc_completion_flag = True
        count = len(sc_header_details)
        sc_header_details = zip(sc_header_details, encrypted_header_guid)

        context['sc_header_details'] = sc_header_details
        context['doc_type'] = doc_type
        context['sc_completion_flag'] = sc_completion_flag
        context['count'] = count
        return render(request, 'Doc Search and Display/sc_completion.html', context)

    if request.method == 'POST':
        search_fields = {}
        document_name = request.POST.get('description')
        document_number = request.POST.get('doc_number')
        created_by = request.POST.get('changed_by')
        timeframe = request.POST.get('created_at')
        search_fields['sc_name'] = document_name
        search_fields['document_number'] = document_number
        search_fields['created_by'] = created_by
        search_fields['timeframe'] = timeframe
        search_fields['document_type'] = CONST_DOC_TYPE_SC
        encrypted_header_guid = []
        # get header detail which has PR, limit order, free text
        search_criteria = document_search_instance.define_search_criteria(search_fields, 'sc_completion')
        sc_header_details = get_header_based_on_calloff(search_criteria)

        for header_guid in sc_header_details:
            created_at_date = header_guid['created_at']
            createdby = header_guid['created_by']
            header_guid['created_at'] = created_at_date.strftime("%d %B %Y")
            header_guid['created_by'] = createdby
            encrypted_header_guid.append(encrypt(header_guid['guid']))
        doc_type = 'SC'
        sc_completion_flag = True
        count = len(sc_header_details)
        sc_header_details = zip(sc_header_details, encrypted_header_guid)

        context['sc_header_details'] = sc_header_details
        context['doc_type'] = doc_type
        context['sc_completion_flag'] = sc_completion_flag
        context['count'] = count
        context['form_method'] = 'POST'

        return render(request, 'Doc Search and Display/sc_completion.html', context)
