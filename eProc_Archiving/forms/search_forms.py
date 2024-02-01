# The purpose of a form is to give users a chance to enter data and submit it to a server. Form for searching SC and
# PO documents based on Document types, Document number, Date range, Supplier, Creator and Requester

# Importing the Django standard libraries
from django import forms
from django.utils.safestring import mark_safe
from datetime import date


# Form fields are created as attributes of the class
class SearchForm1(forms.Form):
    doc_types = (
        ('SC', 'Shopping Cart'),
        ('PO', 'Purchase Order'),
        ('CONF', 'Confirmation'),
    )
    doc_type = forms.ChoiceField(
        label='Select Document Type',
        choices=doc_types,
        widget=forms.Select(
            attrs={"onchange": 'docchanged(this.value)', "class": "form-control", "style": "width:101%"}),
    )
    doc_num = forms.IntegerField(
        label=mark_safe('Enter Document Number'),
        initial=None,
        min_value=10000,
        max_value=9999999999,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", }),
    )
    from_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'style': 'width:15%'}),
        label=mark_safe('From Date'),
        required=False,
        initial=date.today().replace(day=1, month=1, year=2018),
    )
    to_date = forms.DateField(

        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'style': 'margin-left:8px'}),
        label='To Date',
        required=False,
        initial=date.today()
    )
    supplier = forms.CharField(
        label='Enter supplier ID',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", 'style': 'width:37.8%; padding-right:5px;'}),
    )
    po_number = forms.CharField(
        label='PO Number',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", 'style': 'width:37.8%'}),
    )

    # Form field validation
    def clean_doc_num1(self):
        doc_num = self.cleaned_data.get('doc_num')
        if not 0 < len(str(doc_num)) <= 10:
            raise forms.ValidationError("Please enter a valid number")
        return doc_num

    def clean_po_number1(self):
        po_number = self.cleaned_data.get('po_number')
        if po_number != '':
            if len(str(po_number)) <= 10:
                raise forms.ValidationError("Please enter a valid po number")
            return po_number

    def clean1(self):
        cleaned_data = super(SearchForm1, self).clean()
        m_doc_typ = cleaned_data.get('doc_type')
        m_doc_num = cleaned_data.get('doc_num')
        m_frm_date = cleaned_data.get('from_date')
        m_to_date = cleaned_data.get('to_date')
        m_supp = cleaned_data.get('supplier')
        m_created_by = cleaned_data.get('created_by')
        m_requester = cleaned_data.get('requester')

        # To restrict the wildcard search to 3 characters and form fields validations
        # Created by field validation
        if m_created_by is not None:
            if '*' in m_created_by:
                m_created_by = m_created_by.replace('*', '')
                if len(str(m_created_by)) <= 2:
                    raise forms.ValidationError('Please enter at least three characters for creator search')
                if not m_created_by.isalnum():
                    raise forms.ValidationError('Please enter a valid creator user id/name')
        else:
            # Handle the case when m_created_by is None (optional)
            raise forms.ValidationError('Please provide a value for creator search')

        # Requester field validation
        if '*' in m_requester:
            m_requester = m_requester.replace('*', '')
            if len(str(m_requester)) <= 2:
                raise forms.ValidationError(' Please enter atleast three characters for requester search ')
            if not m_requester.isalnum():
                raise forms.ValidationError(' Please enter a valid requester user id/name')

        # Supplier field validation
        if '*' in m_supp:
            m_supp = m_supp.replace('*', '')
            if len(str(m_supp)) <= 2:
                raise forms.ValidationError(' Please enter atleast three characters for supplier search ')
            if not m_supp.isalnum():
                raise forms.ValidationError(' Please enter a valid supplier user id/name')

        # Form fields validation
        if (m_doc_num is None or m_doc_num == '') and (m_frm_date is None or m_frm_date == '') and \
                (m_to_date is None or m_to_date == '') and (m_supp is None or m_supp == '') \
                and (m_created_by is None or m_created_by == '') and (m_requester is None or m_requester == ''):
            raise forms.ValidationError(' Please enter any one search criteria')

        # Date range validation
        if (m_frm_date is not None and m_to_date is None) or (m_frm_date is None and m_to_date is not None):
            raise forms.ValidationError(' Please enter From and To date')

        if m_frm_date is not None and m_to_date is not None:
            if m_frm_date > m_to_date:
                raise forms.ValidationError('\'From Date\' cannot be greater than \'To Date\'')


# Code for requester and creator based search (enabled using settings.py)
class ExtSearch1(SearchForm1):
    created_by = forms.CharField(
        label='Creator',
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    requester = forms.CharField(
        label='Requester',
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
