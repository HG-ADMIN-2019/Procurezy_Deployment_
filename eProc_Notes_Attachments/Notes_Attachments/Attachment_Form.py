"""Copyright (c) 2020 Hiranya Garbha, Inc.
    Name:
        Attachments_Forms.py
    Usage:
        Consists of form to upload and retrieve attachments
    Author:
        Shilpa Ellur
"""
from django import forms

# Form for searching the Attachments based on SC or PO number
from eProc_Notes_Attachments.models.notes_attachements_model import Attachments


class CreateAttachlistForm(forms.Form):
    doc_num = forms.CharField(
        required=True,
        label='Document Number',
        widget=forms.NumberInput(attrs={'style': 'width:469px;'})
    )


# Form for uploading the Attachments based on SC or PO number
class CreateAttachForm(forms.ModelForm):
    doc_num = forms.CharField(initial=12344)

    class Meta:
        model = Attachments
        fields = ('doc_num', 'title', 'doc_file')
