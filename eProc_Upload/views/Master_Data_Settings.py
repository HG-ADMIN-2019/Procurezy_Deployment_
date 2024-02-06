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
from eProc_Upload.Utilities.upload_specific.upload_address import upload_address
from eProc_Upload.Utilities.upload_specific.upload_addressmap import upload_addressmap
from eProc_Upload.Utilities.upload_specific.upload_productcustcatg import upload_productcustcatg
from eProc_Upload.Utilities.upload_specific.upload_wfacc import upload_wfacc
from eProc_Upload.Utilities.upload_specific.upload_suppliers import upload_suppliermaster
from eProc_Upload.Utilities.upload_specific.upload_user import upload_user
from eProc_Basic.Utilities.messages.messages import *
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required


@login_required
def data_upload(req):
    """
    on click of Data upload in nav bar liked to data upload page
    :param req: request data from UI
    :return: render data_upload.html and context
    """
    context = {'inc_nav': True, 'nav_title': 'Upload data'}
    return render(req, 'Upload/data_upload.html', context)


@login_required
def upload_acc_asscat_master(request):
    """
    on click of Upload Account assign cat Map(Data Upload->Upload Account assign cat Map)button in data_upload.html page, upload_accasscat funtion is called
    this function allow user to attach .csv file
    :param request:request data from UI
    :return:render upload_csv_attachment.html and context
    """
    template = "Upload/upload_csv_attachment.html"
    msgid = 'MSG061'
    error_msg = get_message_desc(msgid)[0]
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

            fin_accasscat_upld_data = io.StringIO(data_set)
            next(fin_accasscat_upld_data)

            is_saved = upload_accasscat(request, fin_accasscat_upld_data, Test_mode)

            if (is_saved):
                return render(request, template, prompt)
            else:
                return render(request, template, prompt)
                msgid = 'MSG061'
                error_msg = get_message_desc(msgid)[0]
        except MultiValueDictKeyError:
            csv_file = False
            messages.error(request, error_msg)

            return render(request, template, prompt)
    context = {
    }
    return render(request, template, prompt)


def upload_address_master(request):
    """
    on click of Upload Address(Data Upload->Upload Address)button in data_upload.html page, upload_prodcatg funtion is called
    this function allow user to attach .csv file
    :param request:request data from UI
    :return:render upload_csv_attachment.html and context
    """
    template = "Upload/upload_csv_attachment.html"
    error_msg = get_message_desc(MSG063)[1]
    # msgid = 'MSG063'
    # error_msg = get_msg_desc(msgid)
    # msg = error_msg['message_desc'][0]
    # error_msg = msg
    prompt = {
        'order': error_msg
        # 'order': MSG063
        # Display message MSG063 = 'Please upload Address  data in CSV format'
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

                messages.error(request, error_msg)

                # messages.error(request, MSG044)


                return render(request, template, prompt)

            data_set = csv_file.read().decode('utf8')

            fin_address_upld_data = io.StringIO(data_set)
            next(fin_address_upld_data)

            is_saved = upload_address(request, fin_address_upld_data, Test_mode)

            if (is_saved):
                return render(request, template, prompt)
            else:
                return render(request, template, prompt)


        except MultiValueDictKeyError:
            csv_file = False
            # messages.error(request, MSG063)

            return render(request, template, prompt)
    context = {
    }
    return render(request, template, prompt)


def upload_addressmap_master(request):
    """
    on click of Upload Address Map(Data Upload->Upload Address Map)button in data_upload.html page, upload_addressmap funtion is called
    this function allow user to attach .csv file
    :param request:request data from UI
    :return:render upload_csv_attachment.html and context
    """
    template = "Upload/upload_csv_attachment.html"
    error_msg = get_message_desc(MSG063)[1]
    # msgid = 'MSG063'
    # error_msg = get_msg_desc(msgid)
    # msg = error_msg['message_desc'][0]
    # error_msg = msg
    prompt = {
        'order': error_msg
        # 'order': MSG064
        # Display message MSG064 = 'Please upload Address Map data in CSV format'
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

                messages.error(request, error_msg)

                # messages.error(request, MSG044)

                return render(request, template, prompt)

            data_set = csv_file.read().decode('utf8')

            fin_address_upld_data = io.StringIO(data_set)
            next(fin_address_upld_data)

            is_saved = upload_addressmap(request, fin_address_upld_data, Test_mode)

            if (is_saved):
                return render(request, template, prompt)
            else:
                return render(request, template, prompt)

        except MultiValueDictKeyError:
            csv_file = False
            error_msg = get_message_desc(MSG063)[1]
            # msgid = 'MSG063'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            messages.error(request, error_msg)

            return render(request, template, prompt)
    context = {
    }
    return render(request, template, prompt)


def upload_productcustcatg_master(request):
    """
    on click of Upload productcustcatg Map(Data Upload->Upload productcustcatg Map)button in data_upload.html page, upload_productcustcatg funtion is called
    this function allow user to attach .csv file
    :param request:request data from UI
    :return:render upload_csv_attachment.html and context
    """
    template = "Upload/upload_csv_attachment.html"
    msgid = 'MSG059'
    error_msg = get_message_desc(msgid)[1]
    prompt = {
        'order': error_msg
        # 'order': MSG059
        # Display message MSG059 = 'Please upload Product Category Cust data in CSV format'
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
                messages.error(request, error_msg)
                # messages.error(request, MSG044)
                return render(request, template, prompt)

            data_set = csv_file.read().decode('utf8')

            fin_productcustcatg_upld_data = io.StringIO(data_set)
            next(fin_productcustcatg_upld_data)

            is_saved = upload_productcustcatg(request, fin_productcustcatg_upld_data, Test_mode)

            if (is_saved):
                return render(request, template, prompt)
            else:
                return render(request, template, prompt)

        except MultiValueDictKeyError:
            csv_file = False
            msgid = 'MSG059'
            error_msg = get_message_desc(msgid)[1]
            messages.error(request, error_msg)
            # messages.error(request, MSG059)

            return render(request, template, prompt)
    context = {
    }
    return render(request, template, prompt)


def upload_supplier_master(request):
    """
    on click of Upload suppliermaster(Data Upload->Upload suppliermaster)button in data_upload.html page, upload_prodcatg funtion is called
    this function allow user to attach .csv file
    :param request:request data from UI
    :return:render upload_csv_attachment.html and context
    """
    template = "Upload/upload_csv_attachment.html"
    error_msg = get_message_desc(MSG047)[1]
    # msgid = 'MSG047'
    # error_msg = get_msg_desc(msgid)
    # msg = error_msg['message_desc'][0]
    # error_msg = msg

    prompt = {
        # 'order': MSG047
        'order': error_msg
        # Display message MSG047 = 'Please upload User data in CSV format'
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
                messages.error(request, error_msg)
                # messages.error(request, MSG044)

                return render(request, template, prompt)

            data_set = csv_file.read().decode('utf8')

            fin_supplier_upld_data = io.StringIO(data_set)
            next(fin_supplier_upld_data)

            is_saved = upload_suppliermaster(request, fin_supplier_upld_data, Test_mode)

            if (is_saved):
                return render(request, template, prompt)
            else:
                return render(request, template, prompt)

        except MultiValueDictKeyError:
            csv_file = False
            error_msg = get_message_desc(MSG047)[1]
            # msgid = 'MSG047'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            messages.error(request, error_msg)
            # messages.error(request, MSG047)

            return render(request, template, prompt)

    return render(request, template, prompt)


def upload_user_master(request):
    """
    on click of Upload user Data(Data Upload->Upload user )button in data_upload.html page, upload_user function is called
    this function allow user to attach .csv file
    :param request:request data from UI
    :return:render upload_csv_attachment.html and context
    """
    template = "Upload/upload_csv_attachment.html"
    error_msg = get_message_desc(MSG047)[1]
    # msgid = 'MSG047'
    # error_msg = get_msg_desc(msgid)
    # msg = error_msg['message_desc'][0]
    # error_msg = msg
    prompt = {
        'order': error_msg
        # 'order': MSG047
        # Display message MSG047 = 'Please upload User data in CSV format'
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
                messages.error(request, error_msg)
                # messages.error(request, MSG044)

                return render(request, template, prompt)

            data_set = csv_file.read().decode('utf8')

            fin_user_upld_data = io.StringIO(data_set)
            next(fin_user_upld_data)

            is_saved = upload_user(request, fin_user_upld_data, Test_mode)

            if (is_saved):
                return render(request, template, prompt)
            else:
                return render(request, template, prompt)

        except MultiValueDictKeyError:
            csv_file = False
            error_msg = get_message_desc(MSG047)[1]
            # msgid = 'MSG047'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            messages.error(request, error_msg)
            # messages.error(request, MSG047)

            return render(request, template, prompt)

    return render(request, template, prompt)


def upload_Wfacc_master(request):
    """
    on click of Upload Wfacc(Data Upload->Upload Wfacc)button in data_upload.html page, upload_prodcatg funtion is called
    this function allow user to attach .csv file
    :param request:request data from UI
    :return:render upload_csv_attachment.html and context
    """
    template = "Upload/upload_csv_attachment.html"
    msgid = 'MSG181'
    error_msg = get_message_desc(msgid)[1]

    prompt = {
        'order': error_msg
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
                messages.error(request, error_msg)
                # messages.error(request, MSG044)

                return render(request, template, prompt)

            data_set = csv_file.read().decode('utf8')

            fin_Wfacc_upld_data = io.StringIO(data_set)
            next(fin_Wfacc_upld_data)

            is_saved = upload_wfacc(request, fin_Wfacc_upld_data, Test_mode)

            if (is_saved):
                error_msg = get_message_desc(MSG037)[1]
                messages.success(request,error_msg)
                return render(request, template, prompt)
            else:
                return render(request, template, prompt)

        except MultiValueDictKeyError:
            csv_file = False
            # error_msg = get_message_desc(MSG063)[1]
            # messages.error(request, error_msg)

            return render(request, template, prompt)
    context = {
    }
    return render(request, template, prompt)
