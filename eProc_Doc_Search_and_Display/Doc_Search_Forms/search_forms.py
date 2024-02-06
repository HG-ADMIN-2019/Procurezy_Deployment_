from django import forms
from django.utils.safestring import mark_safe

from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.messages.messages import *


class SearchForm(forms.Form):
    doc_types = (
        ('DOC01', 'Shopping Cart'),
        ('DOC02', 'Purchase Order')
    )
    doc_type = forms.ChoiceField(
        label='Select Document Type',
        choices=doc_types,
        widget=forms.Select(attrs={"onchange": 'docchanged(this.value)', 'class': 'form-control'}),
    )
    doc_num = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control check_number_search'}),
        label=mark_safe('Enter Document Number'),
        initial=None,
        required=False
    )
    # from_date      = forms.DateField( widget     = forms.DateInput(attrs={'type': 'date', 'style':'width:220px;
    # height:21px; border: solid 1px #cac6c6; border-radius: 2px;' }), label      = mark_safe('From Date'),
    # required   = False, initial    = date.today().replace(day=1, month=1, year=2018) ) to_date        =
    # forms.DateField( widget     = forms.DateInput(attrs={'type': 'date', 'style':'width:220px; height:21px;
    # border:solid 1px #cac6c6; border-radius: 2px;' }), label      = 'To Date', required   = False, initial    =
    # date.today() )
    supplier = forms.CharField(
        label='Enter supplier ID',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control check_special_char'})
    )
    # Start of MEP:19
    timeframe = (
        ('Today', 'Today'),
        ('7', 'Last 7 Days'),
        ('30', 'Last 30 Days'),
        ('90', 'Last 90 Days')
    )
    time_frame = forms.ChoiceField(
        label='Select Time Frame',
        choices=timeframe,
        required=False,
        widget=forms.Select(attrs={"onchange": 'docchanged(this.value)',
                                   'class': 'form-control'}),
    )

    SCName = forms.CharField(
        label='SC Name',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control check_for_search'})
    )

    # buy_on_behalf = forms.BooleanField(
    #     label='Buy On Behalf',
    #     required=False,
    #     widget=forms.CheckboxInput(attrs={'class':'check_box_inp'})
    # )
    # end of MEP:19
    # Form field validation
    def clean_doc_num(self):
        doc_num = self.cleaned_data.get('doc_num')
        if not 0 < len(str(doc_num)) <= 10:
            error_msg = get_message_desc(MSG008)[1]
            # msgid = 'MSG008'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG008)

        return doc_num

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        doc_typ = cleaned_data.get('doc_type')
        doc_num = cleaned_data.get('doc_num')
        # frm_date   = cleaned_data.get('from_date')
        # to_date    = cleaned_data.get('to_date')
        supp = cleaned_data.get('supplier')
        # created_by = cleaned_data.get('created_by')
        # requester  = cleaned_data.get('requester')
        SCName = cleaned_data.get('SCName')

        # To restrict the wildcard search to 3 characters and form fields validations
        # Created by field validation
        #         if '*' in created_by:
        #             created_by = created_by.replace('*', '')
        #             if len(str(created_by)) <= 2:
        #                 raise forms.ValidationError(MSG006)
        #             if not created_by.isalnum():
        #                 raise forms.ValidationError(MSG007)
        #
        # # Requester field validation
        #         if '*' in requester:
        #             requester = requester.replace('*', '')
        #             if len(str(requester)) <= 2:
        #                 raise forms.ValidationError(MSG009)
        #             if not requester.isalnum():
        #                 raise forms.ValidationError(MSG010)

        # Supplier field validation
        if '*' in supp:
            supp = supp.replace('*', '')
            if len(str(supp)) <= 2:
                error_msg = get_message_desc(MSG011)[1]
                # msgid = 'MSG011'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg
                raise forms.ValidationError(error_msg)
                # raise forms.ValidationError(MSG011)
            if not supp.isalnum():
                error_msg = get_message_desc(MSG012)[1]
                # msgid = 'MSG012'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg
                raise forms.ValidationError(error_msg)
                # raise forms.ValidationError(MSG012)
            # Start of MEP:19
        # SC NAme field validation
        if '*' in SCName:
            SCName = SCName.replace('*', '')
            if len(str(SCName)) <= 2:
                error_msg = get_message_desc(MSG110)[1]
                # msgid = 'MSG110'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg
                raise forms.ValidationError(error_msg)
            if not SCName.isalnum():
                error_msg = get_message_desc(MSG111)[1]
                # msgid = 'MSG111'
                # error_msg = get_msg_desc(msgid)
                raise forms.ValidationError(error_msg)


# End of MEP:19
# Form fields validation
#         if (doc_num is None or doc_num == '') and (frm_date is None or frm_date == '') and \
#                 (to_date is None or to_date == '') and (supp is None or supp == '') \
#                 and (created_by is None or created_by == '') and (requester is None or requester == ''):
#             raise forms.ValidationError(MSG013)

# Date range validation
#         if (frm_date is not None and to_date is None) or (frm_date is None and to_date is not None):
#             raise forms.ValidationError(MSG014)
#
#         if frm_date is not None and to_date is not None:
#             if frm_date > to_date:
#                 raise forms.ValidationError(MSG015)


# Code for requester and creator based search (enabled using settings.py)
class ExtSearch(SearchForm):
    created_by = forms.CharField(
        label='Creator',
        required=False,
        max_length=20,
        widget=forms.TextInput(
            attrs={'style': 'width:457px; height:21px; border:solid 1px #cac6c6; border-radius: 2px;'})
    )
    requester = forms.CharField(
        label='Requester',
        required=False,
        max_length=20,
        widget=forms.TextInput(
            attrs={'style': 'width:457px; height:21px; border:solid 1px #cac6c6; border-radius: 2px;'})
    )
