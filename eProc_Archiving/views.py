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

from django.http import JsonResponse
from django.shortcuts import render

from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.db_queries import getClients
from eProc_Archiving.models import arch_Country, arch_CompanyCode, arch_OrgClients
from eProc_Archiving.models import arch_CountryCompCode
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
import io
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from eProc_Archiving.Utilites.upload_specific import UploadScPO


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
                paginator = Paginator(result, total_number_results)

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


# data upload logic

@login_required
def data_upload(request):
    # context = {
    #     'inc_nav': True,
    #     'inc_footer': True,
    #     'nav_title': 'Upload data',
    #     'inc_side_panel': True
    # }


    return render(request, 'data_upload.html', {'inc_nav': True,
                                                'inc_footer': True,
                                                'is_slide_menu': True,
                                                'is_home_active': False,
                                                'is_Archiving_active': True,

                                                })


@login_required
def upload_sc(request):
    template = "upload_csv_attachment.html"
    prompt = {
        'order': 'Please upload SC data in CSV format',
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_home_active': False,
        'is_Archiving_active': True
    }
    if request.method == "GET":
        return render(request, template, prompt)
    if request.method == 'POST':
        try:
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                message = {
                    'error': 'Please attach CSV file',
                    'order': 'Please upload SC data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, message)
            data_set = csv_file.read().decode('utf8')
            final_upload_data = io.StringIO(data_set)
            Upload_SC = UploadScPO()
            is_saved = Upload_SC.upload_SC(request, final_upload_data)
            if is_saved:
                response1 = "Data saved successfully"
                context = {
                    'response1': response1,
                    'order': 'Please upload SC data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, context)
            else:
                response = "Data is not saved successfully"
                context = {
                    'response': response,
                    'order': 'Please upload SC data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, context)
        except MultiValueDictKeyError:
            csv_file = False
            context = {
                'order': 'Please upload SC data in CSV format',
                'inc_nav': True,
                'inc_footer': True,
                'is_slide_menu': True,
                'is_home_active': False,
                'is_Archiving_active': True
            }
            return render(request, template, context)
    context = {
        'order': 'Please upload SC data in CSV format',
        'inc_side_panel': True,
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_home_active': False,
        'is_Archiving_active': True
    }
    return render(request, template, context)


@login_required
def upload_po(request):
    template = "upload_csv_attachment.html"
    prompt = {
        'order': 'Please upload PO data in CSV format',
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_home_active': False,
        'is_Archiving_active': True
    }
    if request.method == "GET":
        return render(request, template, prompt)
    if request.method == 'POST':
        try:
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                message = {
                    'error': 'Please attach CSV file',
                    'order': 'Please upload PO data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, message)
            data_set = csv_file.read().decode('utf8')
            final_upload_data = io.StringIO(data_set)
            Upload_PO = UploadScPO()
            is_saved = Upload_PO.upload_PO(request, final_upload_data)
            if (is_saved):
                response1 = "Data saved successfully"
                context = {
                    'response1': response1,
                    'order': 'Please upload PO data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, context)
            else:
                response = "Data is not saved successfully"
                context = {
                    'response': response,
                    'order': 'Please upload PO data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, context)
        except MultiValueDictKeyError:
            csv_file = False
            context = {
                'order': 'Please upload PO data in CSV format',
                'inc_nav': True,
                'inc_footer': True,
                'is_slide_menu': True,
                'is_home_active': False,
                'is_Archiving_active': True
            }
            return render(request, template, context)
    context = {
        'order': 'Please upload PO data in CSV format',
        'inc_side_panel': True,
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_home_active': False,
        'is_Archiving_active': True
    }
    return render(request, template, context)


@login_required
def upload_confirmation(request):
    template = "upload_csv_attachment.html"
    prompt = {
        'order': 'Please upload Confirmation data in CSV format',
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_home_active': False,
        'is_Archiving_active': True
    }
    if request.method == "GET":
        return render(request, template, prompt)
    if request.method == 'POST':
        try:
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                message = {
                    'error': 'Please attach CSV file',
                    'order': 'Please upload Confirmation data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, message)
            data_set = csv_file.read().decode('utf8')
            final_upload_data = io.StringIO(data_set)
            upload_conf = UploadScPO()
            is_saved = upload_conf.upload_confirmation(request, final_upload_data)
            if (is_saved):
                response1 = "Data saved successfully"
                context = {
                    'response1': response1,
                    'order': 'Please upload Confirmation data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, context)
            else:
                response = "Data is not saved successfully"
                context = {
                    'response': response,
                    'order': 'Please upload Confirmation data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, context)
        except MultiValueDictKeyError:
            csv_file = False
            context = {
                'order': 'Please upload Confirmation data in CSV format',
                'inc_nav': True,
                'inc_footer': True,
                'is_slide_menu': True,
                'is_home_active': False,
                'is_Archiving_active': True
            }
            return render(request, template, context)
    context = {
        'order': 'Please upload Confirmation data in CSV format',
        'inc_side_panel': True,
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_home_active': False,
        'is_Archiving_active': True
    }
    return render(request, template, context)


@login_required
def upload_user(request):
    template = "upload_csv_attachment.html"
    prompt = {
        'order': 'Please upload User data in CSV format',
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_home_active': False,
        'is_Archiving_active': True
    }
    if request.method == "GET":
        return render(request, template, prompt)
    if request.method == 'POST':
        try:
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                message = {
                    'error': 'Please attach CSV file',
                    'order': 'Please upload User data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, message)
            data_set = csv_file.read().decode('utf8')
            final_upload_data = io.StringIO(data_set)
            next(final_upload_data)
            Upload = UploadScPO()
            is_saved = Upload.upload_user(request, final_upload_data)
            if is_saved:
                response1 = "Data saved successfully"
                context = {
                    'response1': response1,
                    'order': 'Please upload User data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, context)
            else:
                response = "Data is not saved successfully"
                context = {
                    'response': response,
                    'order': 'Please upload User data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, context)
        except MultiValueDictKeyError:
            csv_file = False
            context = {
                'order': 'Please upload User data in CSV format',
                'inc_nav': True,
                'inc_footer': True,
                'is_slide_menu': True,
                'is_home_active': False,
                'is_Archiving_active': True
            }
            return render(request, template, context)
    context = {
        'order': 'Please upload User data in CSV format',
        'inc_side_panel': True,
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_home_active': False,
        'is_Archiving_active': True
    }
    return render(request, template, context)


@login_required
def upload_supplier_master(request):
    template = "upload_csv_attachment.html"
    prompt = {
        'order': 'Please upload Supplier master data in CSV format',
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_home_active': False,
        'is_Archiving_active': True
    }
    if request.method == "GET":
        return render(request, template, prompt)
    if request.method == 'POST':
        try:
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                message = {
                    'error': 'Please attach CSV file',
                    'order': 'Please upload Supplier master data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, message)
            data_set = csv_file.read().decode('utf8')
            final_upload_data = io.StringIO(data_set)
            next(final_upload_data)
            Upload = UploadScPO()
            is_saved = Upload.upload_supplier(request, final_upload_data)
            if is_saved:
                response1 = "Data saved successfully"
                context = {
                    'response1': response1,
                    'order': 'Please upload Supplier master data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, context)
            else:
                response = "Data is not saved successfully"
                context = {
                    'response': response,
                    'order': 'Please upload Supplier master data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, context)
        except MultiValueDictKeyError:
            csv_file = False
            context = {
                'order': 'Please upload Supplier master data in CSV format',
                'inc_nav': True,
                'inc_footer': True,
                'is_slide_menu': True,
                'is_home_active': False,
                'is_Archiving_active': True
            }
            return render(request, template, context)
    context = {
        'order': 'Please upload Supplier master data in CSV format',
        'inc_side_panel': True,
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_home_active': False,
        'is_Archiving_active': True

    }
    return render(request, template, context)


@login_required
def upload_country_cocode(request):
    template = "upload_csv_attachment.html"
    prompt = {
        'order': 'Please upload Country and Company code data in CSV format',
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_home_active': False,
        'is_Archiving_active': True
    }
    if request.method == "GET":
        return render(request, template, prompt)
    if request.method == 'POST':
        try:
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                message = {
                    'error': 'Please attach CSV file',
                    'order': 'Please upload Country and Company code data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, message)
            data_set = csv_file.read().decode('utf8')
            final_upload_data = io.StringIO(data_set)
            next(final_upload_data)
            Upload_SC = UploadScPO()
            is_saved = Upload_SC.upload_country_ccode(request, final_upload_data)
            if is_saved:
                response1 = "Data saved successfully"
                context = {
                    'response1': response1,
                    'order': 'Please upload Country and Company code data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, context)
            else:
                response = "Data is not saved successfully"
                context = {
                    'response': response,
                    'order': 'Please upload Country and Company code data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, context)
        except MultiValueDictKeyError:
            csv_file = False
            context = {
                'order': 'Please upload Country and Company code data in CSV format',
                'inc_nav': True,
                'inc_footer': True,
                'is_slide_menu': True,
                'is_home_active': False,
                'is_Archiving_active': True
            }
            return render(request, template, context)
    context = {
        'order': 'Please upload Country and Company code data in CSV format',
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_home_active': False,
        'is_Archiving_active': True
    }
    return render(request, template, context)


@login_required
def upload_country(request):
    template = "upload_csv_attachment.html"
    prompt = {
        'order': 'Please upload Country data in CSV format',
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_home_active': False,
        'is_Archiving_active': True
    }
    if request.method == "GET":
        return render(request, template, prompt)
    if request.method == 'POST':
        try:
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                message = {
                    'error': 'Please attach CSV file',
                    'order': 'Please upload Country data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, message)
            data_set = csv_file.read().decode('utf8')
            final_upload_data = io.StringIO(data_set)
            next(final_upload_data)
            Upload_SC = UploadScPO()
            is_saved = Upload_SC.Upload_country(request, final_upload_data)
            if is_saved:
                response1 = "Data saved successfully"
                context = {
                    'response1': response1,
                    'order': 'Please upload Country data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, context)
            else:
                response = "Data is not saved successfully"
                context = {
                    'response': response,
                    'order': 'Please upload Country data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, context)
        except MultiValueDictKeyError:
            csv_file = False
            context = {
                'order': 'Please upload Country data in CSV format',
                'inc_nav': True,
                'inc_footer': True,
                'is_slide_menu': True,
                'is_home_active': False,
                'is_Archiving_active': True
            }
            return render(request, template, context)
    context = {
        'order': 'Please upload Country data in CSV format',
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_home_active': False,
        'is_Archiving_active': True
    }
    return render(request, template, context)


@login_required
def upload_cocode(request):
    template = "upload_csv_attachment.html"
    prompt = {
        'order': 'Please Company code data in CSV format',
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_home_active': False,
        'is_Archiving_active': True
    }
    if request.method == "GET":
        return render(request, template, prompt)
    if request.method == 'POST':
        try:
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                message = {
                    'error': 'Please attach CSV file',
                    'order': 'Please upload Company code data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, message)
            data_set = csv_file.read().decode('utf8')
            final_upload_data = io.StringIO(data_set)
            next(final_upload_data)
            Upload_SC = UploadScPO()
            is_saved = Upload_SC.Upload_cocode(request, final_upload_data)
            if is_saved:
                response1 = "Data saved successfully"
                context = {
                    'response1': response1,
                    'order': 'Please upload Company code data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, context)
            else:
                response = "Data is not saved successfully"
                context = {
                    'response': response,
                    'order': 'Please upload Company code data in CSV format',
                    'inc_nav': True,
                    'inc_footer': True,
                    'is_slide_menu': True,
                    'is_home_active': False,
                    'is_Archiving_active': True
                }
                return render(request, template, context)
        except MultiValueDictKeyError:
            csv_file = False
            context = {
                'order': 'Please upload Company code data in CSV format',
                'inc_nav': True,
                'inc_footer': True,
                'is_slide_menu': True,
                'is_home_active': False,
                'is_Archiving_active': True
            }
            return render(request, template, context)
    context = {
        'order': 'Please upload Company code data in CSV format',
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_home_active': False,
        'is_Archiving_active': True
    }
    return render(request, template, context)


# countrycompcode

def get_country_ccode(request):
    """
    :param request:
    :return:
    """

    country_ccode = list(
        arch_CountryCompCode.objects.filter(client=getClients(request), del_ind=0).values('country', 'company_code_id',
                                                                                          'country_comp_code_guid'))
    country_data = list(arch_Country.objects.filter(del_ind=0).values_list('country_code', flat=True))
    ccode_data = list(arch_CompanyCode.objects.filter(del_ind=0).values_list('company_code_id', flat=True))
    context = {'inc_nav': True,
               'inc_footer': True,
               'inc_side_panel': True,
               'country_ccode': country_ccode,
               'country_data': country_data,
               'ccode_data': ccode_data
               }
    return render(request, 'config_comp_code.html', context)
    # return render(request,context)


JsonParser_obj = JsonParser()


@csrf_exempt
def save_cccode(request):
    cccode_data = JsonParser_obj.get_json_from_req(request)
    Success_message = "Data Saved Successfully"

    client = getClients(request)

    CtryCmpCd_not_exist: object = arch_CountryCompCode.objects.filter(del_ind=False).exclude \
        (country_comp_code_guid=[CtryCmpCd['country_comp_code_guid'] for CtryCmpCd in cccode_data])

    for set_del_int in CtryCmpCd_not_exist:
        set_del_int.del_ind = True
        set_del_int.save()

    for save_CtryCmpCd in cccode_data:
        guid = save_CtryCmpCd['country_comp_code_guid']
        if guid == 'GUID':
            guid = guid_generator()

        # print( save_CtryCmpCd['company_code_id'], save_CtryCmpCd['country_comp_code_guid'], save_CtryCmpCd['country'])
        # Below logic is for existing records changed.
        if arch_CountryCompCode.objects.filter(country_comp_code_guid=guid,
                                               company_code_id=save_CtryCmpCd['company_code_id'],
                                               client=client, del_ind=0).exists():
            continue
        elif arch_CountryCompCode.objects.filter(company_code_id=save_CtryCmpCd['company_code_id'],
                                                 client=client, del_ind=1).exists():
            arch_CountryCompCode.objects.filter(company_code_id=save_CtryCmpCd['company_code_id'],
                                                client=client, del_ind=1).update(
                country=arch_Country.objects.get(country_code=save_CtryCmpCd['country']),
                del_ind=0)
        else:
            # Check if there is any change in the record if no then skip the record
            arch_CountryCompCode.objects.update_or_create(country_comp_code_guid=guid, defaults={
                'country_comp_code_guid': guid,
                'company_code_id': save_CtryCmpCd['company_code_id'],
                'del_ind': False,
                'country': arch_Country.objects.get(country_code=save_CtryCmpCd['country']),
                'client_id': arch_OrgClients.objects.get(client=client)
            }, )

    country_ccode = list(arch_CountryCompCode.objects.filter(client=getClients(request), del_ind=0).values('country',
                                                                                                           'company_code_id',
                                                                                                           'country_comp_code_guid'))
    # Upload_response = list (chain( country_ccode) )
    # return JsonParser_obj.get_json_from_obj ( Upload_response )

    return JsonResponse({'country_ccode': country_ccode, 'message': 'Data updated successfully'})
