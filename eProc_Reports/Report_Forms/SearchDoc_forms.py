# The purpose of a form is to give users a chance to enter data and submit it to a server.
# Form for searching SC and PO documents based on Document types, Date range

# Importing the Django standard libraries
from django import forms
from django.utils.safestring import mark_safe
from datetime import date

# Form fields are created as attributes of the class
from eProc_Basic.Utilities.constants.constants import CONST_ERROR_SPLIT_CRITERIA, CONST_ERROR_TRANSACTION_TYPE, \
    CONST_VALIDATION_ERROR
from eProc_Configuration.models import OrgCompanies


class DocumentSearchForm(forms.Form):
    doc_types = (('SC', 'Shopping Cart'), ('PO', 'Purchase Order'))

    doc_type = forms.ChoiceField(
        label='Select Document Type',
        choices=doc_types,
        widget=forms.Select(attrs={'class': "form-control", "onchange": 'docchanged(this.value)'}),
    )

    # Override label_from_instance to customize the display value for each item
    company_code = forms.ModelChoiceField(
        label='Company Code',
        required=False,
        empty_label=None,
        queryset=OrgCompanies.objects.filter(del_ind=False),
        widget=forms.Select(attrs={'class': "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_code'].label_from_instance = self.label_from_instance

    def label_from_instance(self, obj):
        return f'{obj.company_id} - {obj.name1}'

    from_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': "form-control"}),
        label=mark_safe('From Date'),
        required=False,
        initial=date.today()
    )
    to_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='To Date',
        required=False,
        initial=date.today()
    )
    doc_num = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control check_number_search'}),
        label=mark_safe('Enter Document Number'),
        required=False
    )
    created_by = forms.CharField(
        label='Created By',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    requester = forms.CharField(
        label='Requester',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # hide the supplier field as we are not supporting PO currently supplier = forms.CharField(label='Supplier',
    # required=False, widget=forms.TextInput(attrs={'style':'height:26px; width:100%; border:solid 1px
    # #cac6c6;border-radius: 2px;'}))
    def clean(self):
        cleaned_data = super(DocumentSearchForm, self).clean()
        frm_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        comp_cde = cleaned_data.get('company_code')

        # Form fields validation
        if (frm_date is None or frm_date == '') and (to_date is None or to_date == ''):
            raise forms.ValidationError(' Please enter any one search criteria')

        # Date range validation
        if (frm_date is not None and to_date is None) or (frm_date is None and to_date is not None):
            raise forms.ValidationError(' Please enter From and To date')

        if frm_date is not None and to_date is not None:
            if frm_date > to_date:
                raise forms.ValidationError('\'From Date\' cannot be greater than \'To Date\'')

        if (comp_cde == 'Select') or comp_cde is None:
            raise forms.ValidationError(' Please Select Company Code')


class ApplicationMonitoringForm(DocumentSearchForm):
    error_type = ((CONST_ERROR_SPLIT_CRITERIA, 'Shopping Cart Split'),
                  (CONST_ERROR_TRANSACTION_TYPE, 'Transaction Type'),
                  (CONST_VALIDATION_ERROR,'Data Validation'),
                  ('OTHERS', 'Others'))
    doc_types = forms.ChoiceField(label='Select Document Type', choices=error_type,
                                  widget=forms.Select(
                                      attrs={'class': "form-control", "onchange": 'docchanged(this.value)'}))


class EmailUserMonitoringForm(DocumentSearchForm):
    email_types = (
    ('REGISTRATION', 'User Registration'), ('SC_APPROVAL', 'Shopping Cart Approval'), ('PASSWORD_LOCK', 'User Password '
                                                                                                        'Locked'),
    ('ACCT_DEACTIVATED', 'User Account Deactivated'), ('RESET_PASSWORD', 'Reset Password'),
    ('SC_REJECTED', 'Shopping Cart Rejected'), ('APPROVED_SC', 'Approved Shopping Cart'))

    email_types_ext = (('PO_SUPPLIER', 'Supplier Order'), ('RFQ', 'Request For Quotation'))

    email_types = forms.ChoiceField(label='Select Email Type', choices=email_types,
                                    widget=forms.Select(
                                        attrs={'class': "form-control"}))

    email_types_ext = forms.ChoiceField(label='Select Email Type', choices=email_types_ext,
                                        widget=forms.Select(attrs={'class': "form-control"}))

    status = (
        (1, 'SENT'), (2, 'FAILED'), (3, 'PROCESSING'))
    email_status = forms.ChoiceField(label='Select Email Status', choices=status,
                                     widget=forms.Select(
                                         attrs={'class': "form-control"}))
