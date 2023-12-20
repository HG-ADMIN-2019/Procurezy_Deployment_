"""Copyright (c) 2020 Hiranya Garbha, Inc.
    Name:
        Notes_Forms.py
    Usage:
        Consists of form to add notes
    Author:
        Shilpa Ellur
"""
from eProc_Basic.Utilities.functions.mathematical_symbols import validationMathSymbols
from django import forms

from eProc_Notes_Attachments.models.notes_attachements_model import Notes


class NotesForm(forms.ModelForm):
    doc_num = forms.CharField(initial=12344)

    class Meta:
        model = Notes
        fields = ('doc_num', 'note_text')

    def __init__(self, *args, **kwargs):
        super(NotesForm, self).__init__(*args, **kwargs)
        for data in self.fields:
            self.fields[data].widget.attrs.update({'class': 'hg_edit_mode'})


# varification code for note text

    def clean(self):
        cleaned_data = super(NotesForm, self).clean()
        m_doc_num = cleaned_data.get('doc_num')
        ntype = cleaned_data.get('note_type')
        ntext = cleaned_data.get('note_text')

        if len(str(m_doc_num)) <= 5:
            raise forms.ValidationError(' Please enter the correct num ')

        if not m_doc_num.isnumeric():
            raise forms.ValidationError('Accepts only numbers')

        check_mathematical_symbols = validationMathSymbols(ntext)
        if check_mathematical_symbols:
            raise forms.ValidationError("Do not use Mathematical symbols")



