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
from eProc_Upload.Utilities.upload_specific.upload_apptypes import upload_apptypes
from eProc_Upload.Utilities.upload_specific.upload_doctype import upload_doctype
from eProc_Upload.Utilities.upload_specific.upload_notifkeywords import upload_notifkeywords
from eProc_Upload.Utilities.upload_specific.upload_notifsettings import upload_notifsettings
from eProc_Upload.Utilities.upload_specific.upload_detglacc import upload_detglacc

from eProc_Basic.Utilities.messages.messages import *
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required


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
          # 'order': MSG061
        # Display message MSG061 = 'Please upload Account Assignment Category data in CSV format'
    }
    if request.method == "GET":
         return render(request, template, prompt)
    if request.method == 'POST':
        Test_mode = request.POST.get ( 'test' )

        try:
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                error_msg = get_message_desc(MSG044)[1]
                # msgid = 'MSG044'
                # error_msg = get_msg_desc(msgid)

                messages.error(request, error_msg, prompt)
                # messages.error(request, MSG044, prompt)

                return render(request,template, prompt)

            data_set = csv_file.read().decode('utf8')

            fin_accasscat_upld_data = io.StringIO(data_set)
            next(fin_accasscat_upld_data)

            is_saved=upload_accasscat(request, fin_accasscat_upld_data,Test_mode)

            if (is_saved):
                return render(request, template, prompt)
            else:
                return render(request, template ,prompt)

        except MultiValueDictKeyError:
            csv_file = False
            msgid = 'MSG061'
            error_msg = get_message_desc(msgid)[0]
            messages.error(request, error_msg)
            # messages.error(request, MSG061)

            return render(request, template, prompt)
    context = {
           }
    return render(request, template, prompt)





def upload_documenttype_master(request):
    """
    on click of Upload doctype Map(Data Upload->Upload doctype Map)button in data_upload.html page, upload_doctype funtion is called
    this function allow user to attach .csv file
    :param request:request data from UI
    :return:render upload_csv_attachment.html and context
    """
    template = "Upload/upload_csv_attachment.html"
    msgid = 'MSG060'
    error_msg = get_message_desc(msgid)[0]
    prompt = {
          'order': error_msg
          # 'order': MSG060
        # Display message MSG060 = 'Please upload Document Type data in CSV format'
    }
    if request.method == "GET":
         return render(request, template, prompt)
    if request.method == 'POST':
        Test_mode = request.POST.get ( 'test' )

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
                return render(request,template, prompt)

            data_set = csv_file.read().decode('utf8')

            fin_doctype_upld_data = io.StringIO(data_set)
            next(fin_doctype_upld_data)

            is_saved=upload_doctype(request, fin_doctype_upld_data, Test_mode)

            if (is_saved):
                return render(request, template, prompt)
            else:
                return render(request, template ,prompt)

        except MultiValueDictKeyError:
            csv_file = False
            msgid = 'MSG060'
            error_msg = get_message_desc(msgid)[0]
            messages.error(request, error_msg)
            # messages.error(request, MSG060)

            return render(request, template, prompt)
    context = {
           }
    return render(request, template, prompt)



def upload_notifkeywords_master(request):
    """
    on click of Upload notifkeywords(Data Upload->Upload notifkeywords)button in data_upload.html page, upload_prodcatg funtion is called
    this function allow user to attach .csv file
    :param request:request data from UI
    :return:render upload_csv_attachment.html and context
    """
    template = "Upload/upload_csv_attachment.html"
    error_msg = get_message_desc(MSG075)[1]
    # msgid = 'MSG075'
    # error_msg = get_msg_desc(msgid)
    # msg = error_msg['message_desc'][0]
    # error_msg = msg
    prompt= {
          'order': error_msg
          # 'order': MSG075
          # Display message MSG063 = 'Please upload notifkeywords  data in CSV format'
      }

    if request.method == "GET":
         return render(request, template, prompt)
    if request.method == 'POST':
        Test_mode = request.POST.get ( 'test' )

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

            fin_notifkeywords_upld_data = io.StringIO(data_set)
            next(fin_notifkeywords_upld_data)

            is_saved=upload_notifkeywords(request, fin_notifkeywords_upld_data, Test_mode)

            if (is_saved ):
                return render(request, template, prompt)
            else:
                return render(request, template ,prompt)

        except MultiValueDictKeyError:
            csv_file = False
            # messages.error(request, MSG063)

            return render(request, template, prompt)
    context = {
           }
    return render(request, template, prompt)



def upload_notifsettings_master(request):
    """
    on click of Upload notifsettings(Data Upload->Upload notifsettings)button in data_upload.html page, upload_prodcatg funtion is called
    this function allow user to attach .csv file
    :param request:request data from UI
    :return:render upload_csv_attachment.html and context
    """
    template = "Upload/upload_csv_attachment.html"
    error_msg = get_message_desc(MSG076)[1]
    # msgid = 'MSG076'
    # error_msg = get_msg_desc(msgid)
    # msg = error_msg['message_desc'][0]
    # error_msg = msg
    prompt= {
          'order': error_msg
          # 'order': MSG076
          # Display message MSG063 = 'Please upload notifsettings  data in CSV format'
      }

    if request.method == "GET":
         return render(request, template, prompt)
    if request.method == 'POST':
        Test_mode = request.POST.get ( 'test' )

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

            fin_notifsettings_upld_data = io.StringIO(data_set)
            next(fin_notifsettings_upld_data)

            is_saved=upload_notifsettings(request, fin_notifsettings_upld_data, Test_mode)

            if (is_saved ):
                return render(request, template, prompt)
            else:
                return render(request, template ,prompt)

        except MultiValueDictKeyError:
            csv_file = False
            # messages.error(request, MSG063)

            return render(request, template, prompt)
    context = {
           }
    return render(request, template, prompt)



def upload_detglacc_master(request):
    """
    on click of Upload orgnodetypes(Data Upload->Upload orgnodetypes)button in data_upload.html page, upload_accountingdata
    funtion is called this function allow user to attach .csv file
    :param request:request data from UI
    :return:render upload_csv_attachment.html and context
    """
    template = "Upload/upload_csv_attachment.html"

    prompt = {
          'order': 'Please upload Det GL Account data in CSV format'
        # Display message MSG069 = 'Please upload OrgNodeTypes data in CSV format'
      }
    if request.method == "GET":
         return render(request, template, prompt)
    if request.method == 'POST':
        Test_mode = request.POST.get ( 'test' )

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

            fin_detglacc_upld_data = io.StringIO(data_set)
            next(fin_detglacc_upld_data)

            is_saved=upload_detglacc(request, fin_detglacc_upld_data, Test_mode)

            if is_saved:
                error_msg = get_message_desc(MSG037)[1]
                messages.success(request,error_msg
                                 )
                return render(request, template, prompt)
            else:
                return render(request, template ,prompt)

        except MultiValueDictKeyError:
            csv_file = False
            error_msg = get_message_desc(MSG069)[1]
            # msgid = 'MSG069'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            messages.error(request, error_msg)
            # messages.error(request, MSG069)

            return render(request, template, prompt)
    context = {
           }
    return render(request, template, prompt)



def upload_apptypes_master(request):
    """
    on click of Upload orgnodetypes(Data Upload->Upload orgnodetypes)button in data_upload.html page, upload_accountingdata
    funtion is called this function allow user to attach .csv file
    :param request:request data from UI
    :return:render upload_csv_attachment.html and context
    """
    template = "Upload/upload_csv_attachment.html"

    prompt = {
          'order': 'Please upload Approval Types data in CSV format'
        # Display message MSG069 = 'Please upload OrgNodeTypes data in CSV format'
      }
    if request.method == "GET":
         return render(request, template, prompt)
    if request.method == 'POST':
        Test_mode = request.POST.get ( 'test' )

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

            fin_Apptypes_upld_data = io.StringIO(data_set)
            next(fin_Apptypes_upld_data)

            is_saved=upload_apptypes(request, fin_Apptypes_upld_data, Test_mode)

            if (is_saved):
                error_msg = get_message_desc(MSG037)[1]
                # messages.success(request,MSG037)
                return render(request, template, prompt)
            else:
                return render(request, template ,prompt)

        except MultiValueDictKeyError:
            csv_file = False
            error_msg = get_message_desc(MSG069)[1]
            # msgid = 'MSG069'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            messages.error(request, error_msg)
            # messages.error(request, MSG069)

            return render(request, template, prompt)
    context = {
           }
    return render(request, template, prompt)







def upload_systemsettings_master(request):
    """
    on click of Upload orgnodetypes(Data Upload->Upload orgnodetypes)button in data_upload.html page, upload_accountingdata
    funtion is called this function allow user to attach .csv file
    :param request:request data from UI
    :return:render upload_csv_attachment.html and context
    """
    template = "Upload/upload_csv_attachment.html"

    prompt = {
          'order': 'Please upload System Settings Data in CSV format'
        # Display message MSG069 = 'Please upload OrgNodeTypes data in CSV format'
      }
    if request.method == "GET":
         return render(request, template, prompt)
    if request.method == 'POST':
        Test_mode = request.POST.get ( 'test' )

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

            fin_systemsettings_upld_data = io.StringIO(data_set)
            next(fin_systemsettings_upld_data)

            is_saved=upload_systemsettings(request, fin_systemsettings_upld_data, Test_mode)

            if (is_saved):
                error_msg = get_message_desc(MSG037)[1]
                messages.success(request,error_msg)
                return render(request, template, prompt)
            else:
                return render(request, template ,prompt)

        except MultiValueDictKeyError:
            csv_file = False
            error_msg = get_message_desc(MSG069)[1]
            # msgid = 'MSG069'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            messages.error(request, error_msg)
            # messages.error(request, MSG069)

            return render(request, template, prompt)
    context = {
           }
    return render(request, template, prompt)
