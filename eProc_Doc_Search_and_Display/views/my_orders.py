from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from Majjaka_eProcure import settings
from eProc_Basic.Utilities.constants.constants import CONST_MY_ORDER, CONST_DOC_TYPE_SC, CONST_DOC_TYPE_PO
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import encrypt
from eProc_Basic.Utilities.functions.get_db_query import getClients, get_login_obj_id
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.decorators import authorize_view
from eProc_Doc_Search_and_Display.Doc_Search_Forms.search_forms import *
from eProc_Doc_Search_and_Display.Utilities.search_display_specific import get_my_order_default, \
    get_sc_header_app, DocumentSearch, get_po_header_app
from eProc_Purchase_Order.models import PoApproval, PoPotentialApproval
from eProc_Shopping_Cart.context_processors import update_user_info

django_query_instance = DjangoQueries()


@login_required
@authorize_view(CONST_MY_ORDER)
def sc_po_hdr_search(request):
    """
    :param request:
    :return:
    """

    inp_doc_type = ''
    result = ''
    page_range = 0
    approver_details = []
    doc_header_details = []
    doc_approver_details = []
    sc_completion = []
    encrypted_header_guid = []
    requester_first_name = ''
    sc_completion_flag = False
    client = getClients(request)
    login_user_obj_id = get_login_obj_id(request)
    update_user_info(request)
    username = global_variables.GLOBAL_LOGIN_USERNAME
    document_type = ''
    document_type = request.POST.get('doc_type')
    if document_type == CONST_DOC_TYPE_SC:
        inp_status = request.POST.getlist('status', default=None)
    else:
        inp_status = request.POST.getlist('po_status', default=None)
    # inp_status = request.POST.getlist('status', default=None)
    if not request.method == 'POST':
        if 'results' in request.session:
            request.POST = request.session['results']
            request.method = 'POST'

    if request.method == 'POST':
        request.session['results'] = request.POST

    # If method is post get the form values and get header details accordingly
    if request.method == 'POST':
        requester = global_variables.GLOBAL_LOGIN_USERNAME
        created_by = global_variables.GLOBAL_LOGIN_USERNAME
        document_search_instance = DocumentSearch(requester, created_by)
        if settings.SEARCH_FORM == 'X':
            search_form = ExtSearch(request.POST)
        else:
            search_form = SearchForm(request.POST)
        # if search_form.is_valid():
        document_type = request.POST.get('doc_type')
        ui_search_data = {'document_number': request.POST.get('doc_num'),
                          'document_type': document_type,
                          'supplier': request.POST.get('supplier'),
                          'timeframe': request.POST.get('time_frame'),
                          'sc_name': request.POST.get('SCName'),
                          'status': inp_status,
                          'requester': username}
        search_criteria = document_search_instance.define_search_criteria(ui_search_data, 'my_order')
        if document_type == CONST_DOC_TYPE_SC:
            result = document_search_instance.get_header_details(search_criteria)
        elif document_type == CONST_DOC_TYPE_PO:
            doc_header_details = document_search_instance.get_po_header_details(search_criteria)
            result = doc_header_details
    else:
        if settings.SEARCH_FORM == 'X':
            search_form = ExtSearch()
        else:
            search_form = SearchForm()

    t_count = len(result)
    my_order_default = get_my_order_default(client, login_user_obj_id)

    if document_type == CONST_DOC_TYPE_SC:
        # Appending SCHeader fields and its respective SCApproval
        doc_header_details, doc_approver_details, sc_completion, requester_first_name = get_sc_header_app(result,
                                                                                                          client)
    elif document_type == CONST_DOC_TYPE_PO:
        for po_header_guid in doc_header_details:
            po_header_guid['guid'] = po_header_guid['po_header_guid']
            del po_header_guid['po_header_guid']
            po_header_guid['created_at'] = po_header_guid['po_header_created_at']
            del po_header_guid['po_header_created_at']
            po_header_guid['created_by'] = po_header_guid['po_header_created_by']
            del po_header_guid['po_header_created_by']
        doc_header_details, doc_approver_details, sc_completion, requester_first_name = get_po_header_app(result,
                                                                                                          client)
        for doc_approver_detail in doc_approver_details:
            doc_approver_detail['header_guid_id'] = doc_approver_detail['po_header_guid_id']
            del doc_approver_detail['po_header_guid_id']

    # Paginating search results and restricting the results to 50 per page
    page = request.GET.get('page', 1)
    paginator = Paginator(approver_details, 5)
    try:
        approver_details = paginator.page(page)
    except PageNotAnInteger:
        approver_details = paginator.page(1)
    except EmptyPage:
        approver_details = paginator.page(paginator.num_pages)

    for header_guid in doc_header_details:
        encrypted_header_guid.append(encrypt(header_guid['guid']))

    doc_header_details = zip(doc_header_details, encrypted_header_guid)

    # Context to display in search.html
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'doc_approver_details': doc_approver_details,
        'sc_appr': doc_approver_details,
        'doc_header_details': doc_header_details,
        'sc_completion': sc_completion,
        'requester_first_name': requester_first_name,
        'sform': search_form,
        'results': result,
        'my_order_default': my_order_default,
        'approver_details': approver_details,
        'page_range': page_range,
        't_count': t_count,
        'inp_doc_type': document_type,
        'sc_completion_flag': sc_completion_flag,
        'inp_status': inp_status,
        'is_slide_menu': True,
        'is_shop_active': True
    }

    return render(request, 'Doc Search and Display/search.html', context)
