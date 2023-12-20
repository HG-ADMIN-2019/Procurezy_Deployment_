"""Copyright (c) 2020 Hiranya Garbha, Inc.
    Name:
        attachments.py
    Usage:
        The file consists of various functions that handles the attachments like adding, download, getting the attachments, etc.
    Author:
        Shilpa Ellur
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Doc_Details.Utilities.details_generic import GetAttachments
from eProc_Notes_Attachments.Notes_Attachments.Attachment_Form import CreateAttachForm, CreateAttachlistForm
from eProc_Notes_Attachments.Utilities.notes_attachments_generic import download
from eProc_Notes_Attachments.Utilities.notes_attachments_specific import attach_instance_save
from eProc_Notes_Attachments.models import Attachments
from eProc_Basic.Utilities.messages.messages import *
import os

django_query_instance = DjangoQueries()


def attach_list(request):
    """
    Function gets the list of attachments based on the document number
    :param request: POST method with the input as document number
    :return: list of attachments to the respective document number
    """

    if request.method == 'POST':
        attach_list_form = CreateAttachlistForm(request.POST)
        if attach_list_form.is_valid():
            doc_num = attach_list_form.cleaned_data['doc_num']
            data = django_query_instance.django_filter_only_query(Attachments,
                                                                  {'doc_num': doc_num, 'client': getClients(request)})

            return render(request, 'Notes_Attachments/attach_list.html', {'data': data, 'form': attach_list_form})
    else:
        attach_list_form = CreateAttachlistForm()
    return render(request, 'Notes_Attachments/attach_list.html', {
        'attach_list_form': attach_list_form,
        'inc_nav': True,
        'inc_footer': True

    })


def upload_attach(request):
    """
    Function used to add the attachment to the particular document number along with the type of document
    :param request: POST request which gets the document number, type of document and the attachment
    :return: a success message if the attachment is added successfully
    """
    if request.method == 'POST':
        upload_attach_form = CreateAttachForm(request.POST, request.FILES)

        if upload_attach_form.is_valid():
            client = getClients(request)
            instance = upload_attach_form.save(commit=False)
            attach_instance_save(client, instance)
            error_msg = get_message_desc(MSG035)[1]
            # msgid = 'MSG035'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            return JsonResponse({'message': error_msg})
            # return JsonResponse({'message': MSG035})
    else:
        upload_attach_form = CreateAttachForm()
    return render(request, 'eProc_Shopping_Cart/Shopping_Cart/sc_second_step/sc_second_step.html', {
        'form': upload_attach_form,
    })


""" Functions relating to the search tool - download the attachments based on the selected PO """


# Documents page function
@login_required
def attachmentspage(req, guid):
    obj = GetAttachments()
    attachments_list = obj.get_attachments(req, guid)
    popdf_list = obj.get_popdf(req, guid)
    return render(req, 'Doc_Details/attachments.html', {'inc_nav': True,
                                                        'inc_footer': True,
                                                        'attachments': attachments_list,
                                                        'popdf': popdf_list})


# Documents handler
def attach(req):
    if req.method == 'POST':
        path = req.POST.get('file_path')
        if os.path.exists(path):
            if os.path.isfile(path):
                return download(path)
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


@login_required
def downloadpdf(req, type, fname):
    path = 'Files/POPDF/' + fname
    return download(path)


# To download attachments
@login_required
def downloadattach(req):
    path = req.GET['path']
    return download(path)
