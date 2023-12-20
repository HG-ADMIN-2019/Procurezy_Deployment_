"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    Master_Data_Settings_upload.py
Usage:
    on click of Upload country Map in data upload page
    This file handle upload_country view functionality and render upload_csv_attachment.html

    SP11-13 - Add Upload Functionality

Author:
    Shankar Bhat - Eprocurement-6 - Add Upload Functionality
"""
import csv
import io

from django.shortcuts import render
from django.contrib import messages

from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Upload.Utilities.upload_specific.upload_accasscat import upload_accasscat
from eProc_Upload.Utilities.upload_specific.upload_orgmodel import upload_orgmodel

from eProc_Basic.Utilities.messages.messages import *
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required


@login_required
def upload_orgmodel_master(request):
    """
    on click of Upload OrgModel  Map(Data Upload->Upload OrgModel  Map)button in data_upload.html page, upload_accasscat funtion is called
    this function allow user to attach .csv file
    :param request:request data from UI
    :return:render upload_csv_attachment.html and context
    """
    template = "Upload/upload_csv_attachment.html"
    msgid = 'MSG182'
    error_msg = get_message_desc(msgid)[1]

    prompt = {
        'order': error_msg
        # Display message MSG061 = 'Please upload Account Assignment Category data in CSV format'
    }
    if request.method == "GET":
        return render(request, template, prompt)
    if request.method == 'POST':
        Test_mode = request.POST.get('test')
        try:
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                error_msg = get_message_desc(MSG044)[1]
                # msgid = 'MSG044'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg
                messages.error(request, error_msg, prompt)
                # messages.error(request, MSG044, prompt)

                return render(request, template, prompt)

            data_set = csv_file.read().decode('utf8')

            fin_orgmodel_upld_data = io.StringIO(data_set)
            next(fin_orgmodel_upld_data)

            is_saved = upload_orgmodel(request, fin_orgmodel_upld_data, Test_mode)

            if (is_saved):
                return render(request, template, prompt)
            else:
                return render(request, template, prompt)
                msgid = 'MSG061'
                error_msg = get_msg_desc(msgid)
                msg = error_msg['message_desc'][0]
                error_msg = msg
        except MultiValueDictKeyError:
            csv_file = False
            messages.error(request, error_msg)

            return render(request, template, prompt)
    context = {
    }
    return render(request, template, prompt)
