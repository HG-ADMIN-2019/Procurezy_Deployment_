"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    sc_upload.py
Usage:
    on click of Upload SC in data upload page
    This file handle upload_sc views functionality and render upload_csv_attachment.html

Author:
    Deepika K/Shreyas
"""
from django.contrib import messages
from django.shortcuts import render
import io

from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.messages.messages import *
from eProc_Upload.Utilities.upload_specific.upload_SC import upload_SC
from eProc_Upload.Utilities.upload_specific.upload_PO import upload_PO
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required


@login_required
def upload_sc(request):
    """
    on click of Upload SC Map(Data Upload->Upload SC Map)button in data_upload.html page, upload_SC funtion is called
    this function allow user to attach .csv file
    :param request:request data from UI
    :return:render upload_csv_attachment.html and context
    """
    template = "Upload/upload_csv_attachment.html"
    error_msg = get_message_desc(MSG044)[1]
    # msgid = 'MSG044'
    # error_msg = get_msg_desc(msgid)
    # msg = error_msg['message_desc'][0]
    # error_msg = msg

    prompt = {

        # 'order': MSG044

        'order': error_msg
        # Display message MSG045 = 'Please upload SC data in CSV format'
    }
    if request.method == "GET":
        return render(request, template, prompt)
    if request.method == 'POST':
        Test_mode = request.POST.get('test')

        try:
            csv_file = request.FILES['file']
            error_msg = get_message_desc(MSG044)[1]
            # msgid = 'MSG044'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            if not csv_file.name.endswith('.csv'):

                messages.error(request, error_msg)
                # messages.error(request, MSG044)
                return render(request, template, prompt)

            data_set = csv_file.read().decode('utf8')

            fin_SC_upld_data = io.StringIO(data_set)
            next(fin_SC_upld_data)

            is_saved = upload_SC(request, fin_SC_upld_data, Test_mode)

            if (is_saved):
                return render(request, template, prompt)
            else:
                return render(request, template, prompt)

        except MultiValueDictKeyError:
            csv_file = False
            error_msg = get_message_desc(MSG045)[1]

            # msgid = 'MSG045'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            messages.error(request, error_msg)
            # messages.error(request, MSG045)

            return render(request, template, prompt)
    context = {
    }
    return render(request, template, prompt)


def upload_po(request):
    """
    on click of Upload PO Map(Data Upload->Upload PO Map)button in data_upload.html page, upload_PO funtion is called
    this function allow user to attach .csv file
    :param request:request data from UI
    :return:render upload_csv_attachment.html and context
    """
    template = "Upload/upload_csv_attachment.html"
    error_msg = get_message_desc(MSG046)[1]
    # msgid = 'MSG046'
    # error_msg = get_msg_desc(msgid)
    # msg = error_msg['message_desc'][0]
    # error_msg = msg
    messages.error(request, error_msg)

    prompt = {
        # 'order': MSG046
        'order': error_msg
        # Display message MSG046 = 'Please upload PO data in CSV format'
    }
    if request.method == "GET":
        return render(request, template, prompt)
    if request.method == 'POST':
        Test_mode = request.POST.get('test')

        try:
            csv_file = request.FILES['file']
            error_msg = get_message_desc(MSG044)[1]
            # msgid = 'MSG044'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            if not csv_file.name.endswith('.csv'):

                messages.error(request, error_msg)
                # messages.error(request, MSG044)
                return render(request, template, prompt)

            data_set = csv_file.read().decode('utf8')

            fin_PO_upld_data = io.StringIO(data_set)
            next(fin_PO_upld_data)

            is_saved = upload_PO(request, fin_PO_upld_data, Test_mode)

            if (is_saved):
                return render(request, template, prompt)
            else:
                return render(request, template, prompt)

        except MultiValueDictKeyError:
            csv_file = False
            error_msg = get_message_desc(MSG046)[1]
            # msgid = 'MSG046'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg

            messages.error(request, error_msg)
            # messages.error(request, MSG046)

            return render(request, template, prompt)
    context = {
    }
    return render(request, template, prompt)
