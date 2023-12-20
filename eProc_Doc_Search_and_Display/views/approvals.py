from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import encrypt
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.decorators import authorize_view
from eProc_Doc_Search_and_Display.Utilities.search_display_specific import get_sc_header_app_wf, DocumentSearch
from eProc_Notes_Attachments.models import Notes
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Shopping_Cart.models import ScApproval, ScPotentialApproval
from eProc_Workflow.Workflow_Forms.search_manager_approvals import SearchManagerApprovalsForm
import datetime

django_query_instance = DjangoQueries()


@login_required
@authorize_view(CONST_APPROVALS)
def get_sc_for_approval(request):
    sc_header_app_detail1 = ''
    update_user_info(request)
    document_search_instance = DocumentSearch('', '')
    encrypted_guid = []
    zipped_content = []
    if request.is_ajax():
        header_guid = request.POST.get('header_guid')
        approver_note = django_query_instance.django_filter_value_list_query(Notes, {'header_guid': header_guid,
                                                                                     'note_type': 'Approver Note'},
                                                                             'note_text')[0]
        return JsonResponse({'approver_note': approver_note})

    sc_completion_flag = False
    inp_doc_type = 'SC'
    update_user_info(request)

    sc_approval_header = django_query_instance.django_filter_value_list_query(ScPotentialApproval, {
        'app_id': global_variables.GLOBAL_LOGIN_USERNAME,
        # 'proc_lvl_sts': CONST_ACTIVE,
        'client': global_variables.GLOBAL_CLIENT
    }, 'sc_header_guid')

    sc_header_detail = document_search_instance.get_header_details({
        'guid__in': sc_approval_header, 'created_at__date': datetime.date.today()
    })

    sc_header_app_detail = get_sc_header_app_wf(sc_header_detail, global_variables.GLOBAL_CLIENT)

    search_approval = SearchManagerApprovalsForm()
    context = {
        'form_method': ''
    }

    if request.method == 'GET':
        search_criteria = {
            'guid__in': sc_approval_header,
            'created_at': datetime.datetime.today()
        }
        sc_header_detail = document_search_instance.get_header_details(search_criteria)

        sc_header_app_detail = get_sc_header_app_wf(sc_header_detail, global_variables.GLOBAL_CLIENT)

        context['count'] = len(sc_header_app_detail)
        for header_guid in sc_header_app_detail:
            header_guid.append(encrypt(header_guid[0]))

        form_method = ''

    if request.method == 'POST':
        search_criteria = {}
        search_approval = SearchManagerApprovalsForm(request.POST or None)
        timeframe = request.POST.get('time_frame')
        document_number = request.POST.get('document_number')
        document_name = request.POST.get('cart_name')
        status = request.POST.getlist('status', default=None)
        search_criteria['document_number'] = document_number
        search_criteria['sc_name'] = document_name
        search_criteria['timeframe'] = timeframe
        search_criteria['status'] = status
        search_criteria['guid__in'] = sc_approval_header
        search_criteria['document_type'] = request.POST.get('document_type')
        defined_criteria = document_search_instance.define_search_criteria(search_criteria, 'approvals')
        search_criteria = defined_criteria
        sc_header_detail = document_search_instance.get_header_details(search_criteria)

        sc_header_app_detail = get_sc_header_app_wf(sc_header_detail, global_variables.GLOBAL_CLIENT)

        context['count'] = len(sc_header_app_detail)
        for header_guid in sc_header_app_detail:
            # encrypted_guid.append(encrypt(header_guid[0]))
            header_guid.append(encrypt(header_guid[0]))
        # zipped_content = zip(sc_header_app_detail, encrypted_guid)
        print('sc_header_app_detail ', sc_header_app_detail)
        form_method = 'POST'

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_approvals_active': True,
        'sc_completion_flag': sc_completion_flag,
        'sc_header_app_detail': sc_header_app_detail,
        'inp_doc_type': inp_doc_type,
        'search_approval': search_approval,
        'zipped_content': zipped_content,
        'form_method': form_method
    }
    return render(request, 'Doc Search and Display/get_sc_for_approval_rejection.html', context)
