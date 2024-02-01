import os

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import Http404, HttpResponse, FileResponse
from django.shortcuts import render
from django.utils.encoding import smart_str

from eProc_Archiving.Utilites.doc_search_specific import arch_get_hdr_data, get_cocode_filter, \
    get_doc_details, arch_GetAttachments
from eProc_Archiving.forms.search_forms import ExtSearch1, SearchForm1, ExtSearch1, SearchForm1
from eProc_Archiving.models import ConfHeader, ConfAccounting, arch_ScItem, arch_ScAccounting, arch_ScApproval, \
    arch_PoHeader, arch_PoItem, arch_PoAccounting, arch_PoApproval, ConfItem, arch_ScHeader
from eProc_Basic.Utilities.functions.get_db_query import getUsername, getClients


@login_required
def docsearch(request):
    result = ''
    page_range = 0
    t_count = 0
    inp_doc_type = ''
    total_number_results = 0
    login_username = getUsername(request)
    client = getClients(request)
    if not request.method == 'POST':
        if 'search-persons-post' in request.session:
            request.POST = request.session['search-persons-post']
            request.method = 'POST'
    if request.method == 'POST':
        request.session['search-persons-post'] = request.POST
    if request.method == 'POST':
        if settings.SEARCH_FORM1 == 'X':
            search_form = ExtSearch1(request.POST)
        else:
            search_form = SearchForm1(request.POST)
        if search_form.is_valid():
            inp_doc_type = request.POST.get('doc_type')
            inp_doc_num = request.POST.get('doc_num')
            inp_from_date = request.POST.get('from_date')
            inp_to_date = request.POST.get('to_date')
            inp_supl = request.POST.get('supplier')
            inp_created_by = request.POST.get('created_by')
            inp_requester = request.POST.get('requester')
            po_number = request.POST.get('po_number')
            filter_result, header_guid = arch_get_hdr_data(request,
                                                           inp_doc_type,
                                                           inp_doc_num,
                                                           inp_from_date,
                                                           inp_to_date,
                                                           inp_supl,
                                                           inp_created_by,
                                                           inp_requester,
                                                           po_number
                                                           )
            result = get_cocode_filter(client, login_username, header_guid, inp_doc_type)

            total_number_results = len(result)

            if result:
                page = request.GET.get('page', 1)

                # Pagination for search results
                paginator = Paginator(result, 10)

                if paginator.count > 0:
                    try:
                        result = paginator.page(page)
                    except PageNotAnInteger:
                        result = paginator.page(1)
                    except EmptyPage:
                        result = paginator.page(paginator.num_pages)
                        # Handling the Number of Page Numbers to be displayed
                        index = paginator.page_range.index(result.number)
                        max_index = len(paginator.page_range)
                        start_index = index - 3 if index >= 3 else 0
                        end_index = index + 3 if index <= max_index - 3 else max_index
                        page_range = paginator.page_range[start_index:end_index]

                t_count = len(result)

            else:
                result = 'No results found'
    else:
        if settings.SEARCH_FORM1 == 'X':
            search_form = ExtSearch1()
        else:
            search_form = SearchForm1()

    return render(request, 'search.html', {'inc_nav': True,
                                           'inc_footer': True,
                                           'is_slide_menu': True,
                                           'is_home_active': False,
                                           'nav_title': 'Search for document',
                                           'sform': search_form,
                                           'results': result,
                                           'total_count': t_count,
                                           'page_range': page_range,
                                           'inp_doc_type': inp_doc_type,
                                           'total_number_results': total_number_results,
                                           'inc_side_panel': True,
                                           'is_Archiving_active': True
                                           })


def get_sc_po_data(request):
    return render(request, '')


@login_required
def m_det_meth(request, type, guid):
    print(f"Type: {type}, GUID: {guid}")
    appr_data = {}
    doc_data = get_doc_details(type, guid)
    hdr_data = doc_data.get('hdr_data', None)
    itm_data = doc_data.get('itm_data', None)
    acc_data = doc_data.get('acc_data', None)
    if type == 'CONF':
        show_appr = False
        print(f"GUID: {guid}")
    else:
        appr_data = doc_data.get('appr_data', None)

        if appr_data.count() > 0:
            show_appr = True
        else:
            show_appr = False
    return render(request, 'doc_detail.html', {'type': type,
                                               'guid': guid,
                                               'show_appr': show_appr,
                                               'header_details': hdr_data,
                                               'item_details': itm_data,
                                               'accounting_details': acc_data,
                                               'approval_details': appr_data,
                                               'inc_nav': True,
                                               'inc_footer': True,
                                               'inc_side_panel': True})


# To download pdf
@login_required
def downloadpdf(request, type, fname):
    path = 'Files/POPDF/' + fname
    return download(path)


# To download attachments
@login_required
def arch_downloadattach(request):
    path = request.GET['path']
    print("File path:", path)
    try:
        return download(path)
    except Exception as e:
        print("Error:", e)
        raise



def download(path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    print("Full file path:", file_path)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={smart_str(os.path.basename(file_path))}'
            return response

    raise Http404


# Documents page function
@login_required
def attachmentspage(request, guid):
    obj = arch_GetAttachments()
    attachments_list = obj.get_attachments(request, guid)
    popdf_list = obj.get_popdf(request, guid)
    # Add these print statements
    print("Attachments List:", attachments_list)
    print("POPDF List:", popdf_list)

    return render(request, 'attachments.html', {'inc_nav': True,
                                                'inc_footer': True,
                                                'attachments': attachments_list,
                                                'popdf': popdf_list})


# Documents handler
def attach(request):
    if request.method == 'POST':
        path = request.POST.get('file_path')
        if os.path.exists(path):
            if os.path.isfile(path):
                return download(path, '')
            else:
                res = ''
                list = os.listdir(path)
                for file in list:
                    pdf = path + '/' + file
                    if os.path.isfile(pdf):
                        pdf = pdf.replace('&', '%26')
                        line = "<img src=\"/static/img/file.png\"  style=\"border:none; width:15px; height:15px; \"  > "
                        line += "<a href=\"attachments/download?path=" + pdf + "\">" + os.path.basename(
                            pdf) + "</a><br/>"
                    else:
                        line = "<img src=\"/static/img/folder.png\"  style=\"border:none; width:15px; height:15px; \"  > "
                        line += "<a onclick=\"get_pdf('" + pdf + "')\" href=\"javascript:void(0);\">" + os.path.basename(
                            pdf) + "</a><br/>"
                    res += line
                return HttpResponse(res)
        else:
            raise Http404
    else:
        raise Http404


def get_doc_det_by_doc_num(request, doc_type, doc_number):
    """
    :param request:
    :param doc_type: Based on document type header details are being fetched
    :param doc_number: Referred to document number in the document
    :return:
    """
    if doc_type == 'SC':
        header_instance = arch_ScHeader
        itm_obj = arch_ScItem()
        acc_obj = arch_ScAccounting()
        appr_obj = arch_ScApproval()
    elif doc_type == 'PO':
        header_instance = arch_PoHeader
        itm_obj = arch_PoItem()
        acc_obj = arch_PoAccounting()
        appr_obj = arch_PoApproval()
    else:
        header_instance = ConfHeader
        itm_obj = ConfItem()
        acc_obj = ConfAccounting()
    client = getClients(request)
    header_details = header_instance.objects.filter(doc_number=doc_number, client=client)
    if len(header_details) > 0:
        header_guid = header_details.values_list('guid', flat=True)[0]
        item_details = itm_obj.get_itms_by_guid(header_guid)
        item_guid = list(item_details.values_list('guid', flat=True))
        accounting_details = acc_obj.get_acc_data_by_guid(item_guid)
        approval_details = appr_obj.get_apprs_by_guid(header_guid)
        show_approval_details = False
        if len(approval_details) > 0:
            show_approval_details = True
        context = {
            'header_details': header_details,
            'item_details': item_details,
            'accounting_details': accounting_details,
            'approval_details': approval_details,
            'show_approval_details': show_approval_details,
            'type': doc_type,
            'guid': header_guid,
            'inc_side_panel': True,
            'inc_nav': True,
        }
        return render(request, 'document_number_details.html', context)
    else:
        context = {
            'inc_side_panel': True,
            'inc_nav': True,
        }
        return render(request, 'document_number_details.html', context)


# @login_required
# def downloadattach(request):
#     path = request.GET['path']
#     return download(path)


# Documents page function
@login_required
def arch_attachmentspage(request, guid):
    obj = arch_GetAttachments()
    attachments_list = obj.get_attachments(request, guid)
    popdf_list = obj.arch_get_popdf(request, guid)

    # Add these print statements
    print("Attachments List:", attachments_list)
    print("POPDF List:", popdf_list)

    return render(request, 'attachments.html', {'inc_nav': True,
                                                'inc_footer': True,
                                                'is_slide_menu': True,
                                                'is_home_active': False,
                                                'attachments': attachments_list,
                                                'popdf': popdf_list})
