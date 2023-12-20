"""Copyright (c) 2020 Hiranya Garbha, Inc.
    Name:
        notes.py
    Usage:
        file consists of function dealing with the notes.
    Author:
        Shilpa Ellur

"""
from django.http import JsonResponse
from django.shortcuts import render

from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Notes_Attachments.Notes_Attachments.Notes_Form import *
from eProc_Notes_Attachments.Utilities.notes_attachments_specific import notes_instance_save
from eProc_Basic.Utilities.messages.messages import *


def add_notes(req):
    """
    Adding notes to the document at header level and item level along with the note type
    :param req: Gets the request with document number, type of note and note
    :return: success message if the note is added successfully
    """
    if req.method == 'POST':
        add_note_form = NotesForm(req.POST)
        if add_note_form.is_valid():
            client = req.user.client_id
            frmst = add_note_form.save(commit=False)
            notes_instance_save(frmst, client)
            error_msg = get_message_desc(MSG034)[1]
            # msgid = 'MSG034'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            return JsonResponse({'message': error_msg})
            # return JsonResponse({'message': MSG034})
    else:
        add_note_form = NotesForm()
    return render(req, 'Shopping_Cart/sc_second_step/sc_second_step.html', {
        'add_note_form': add_note_form,
    })
