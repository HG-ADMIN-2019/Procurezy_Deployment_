import datetime
import os

from django.core.files.storage import FileSystemStorage
from django.http.response import JsonResponse
from django.shortcuts import render
from pypdf._reader import PdfReader
import tabula
from Majjaka_eProcure import settings
from eProc_Basic.Utilities.functions.distinct_list import distinct_list
from eProc_Basic.Utilities.functions.encryption_util import encrypt, decrypt
from eProc_Basic.Utilities.functions.file_system_related_function import file_existence_check
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Supplier_Order_Management.Utilities.supplier_order_management_specific import *
from eProc_Suppliers.Utilities.supplier_generic import supplier_detail_search, som_po_search


def po_extract(request):
    """

    """
    som_po_data = []
    update_user_info(request)
    text = []
    header_detail = []
    supplier_address = []
    search_fields = {}
    if not request.POST:
        som_po_data = get_som_po_header_data_from_db()
        som_po_data = encrypt_som_po(som_po_data)
    if 'som_po_search' in request.POST:
        search_fields['po_number'] = request.POST.get('po_number')
        search_fields['company_name'] = request.POST.get('company_name')
        search_fields['received_date'] = request.POST.get('received_date')
        search_fields['buyer_name'] = request.POST.get('buyer_name')
        search_fields['buyer_email_id'] = request.POST.get('buyer_email_id')
        search_fields['buyer_phone_num'] = request.POST.get('buyer_phone_num')
        som_po_data = som_po_search(**search_fields)
        som_po_data = encrypt_som_po(som_po_data)
    # elif 'extract_po' in request.POST:
    #     po_pdf_reader()

    context = {'inc_nav': True,
               'inc_footer': True,
               'is_slide_menu': True,
               'text': text,
               'header_detail': header_detail,
               'supplier_address': supplier_address,
               'som_po_data': som_po_data
               }
    return render(request, 'Supplier_Order_Management/som_po_data.html', context)


def som_po_detail(request, encrypted_guid):
    """
    
    """
    update_user_info(request)
    po_doc_num = decrypt(encrypted_guid)
    po_detail = get_som_po_detail(po_doc_num)
    context = po_detail
    return render(request, 'Supplier_Order_Management/som_po_detail.html', context)


def upload_som(request):
    """

    """
    update_user_info(request)
    upload_files = request.FILES
    fs = FileSystemStorage()
    list_file = []
    for key, value in upload_files.items():
        print(key)
        path = 'temp/'+value.name
        filename = fs.save(path, value)
        po_num = get_po_num(value.name)
        file_name = po_num+'.pdf'
        new_filename = 'pdf_read/' + file_name
        absolute_path = os.path.join(str(settings.BASE_DIR), 'media', 'pdf_read', file_name)
        if not file_existence_check(absolute_path):
            os.rename(fs.path(path), fs.path(new_filename))
            list_file.append(file_name)
    temp_folder_path = os.path.join(str(settings.BASE_DIR), 'media', 'temp')
    delete_all_files(temp_folder_path)
    display_data = {}
    po_pdf_reader(list_file)
    return JsonResponse(display_data, safe=False)
