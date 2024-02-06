"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    supplier_registration_form.py
Usage:
    Supplier register form fields
    SupplierRegForm : This class is used to build the form for supplier registration page.
Author:
    Siddarth Menon
"""

from django import forms
import re

from django.core.validators import RegexValidator

from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import *
from eProc_Configuration.models import Currency, Languages, Country, SupplierMaster
import datetime


class SupplierRegForm(forms.Form):
    supplier_id = forms.CharField(label='Supplier id', required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control check_special_char'}),
                                  # validators=[RegexValidator('[+-/%]', inverse_match=True)]
                                  )

    supplier_types = (
        ('E-mail Supplier', 'E-mail Supplier'),
        ('Mail Supplier', 'Mail Supplier'),
        ('Integrated Supplier', 'Integrated Supplier'),
    )
    working_days_choices = (
        ('1', 'Sunday'),
        ('2', 'Monday'),
        ('3', 'Tuesday'),
        ('4', 'Wednesday'),
        ('5', 'Thursday'),
        ('6', 'Friday'),
        ('7', 'Saturday')
    )
    supp_type = forms.CharField(label='Communication Type', required=False,
                                widget=forms.Select(choices=supplier_types, attrs={'class': 'form-control'}))
    name1 = forms.CharField(label='Name 1', required=False, widget=forms.TextInput(attrs={'class': 'form-control '
                                                                                                   'check_special_char',
                                                                                          }))
    name2 = forms.CharField(label='Name 2', required=False, widget=forms.TextInput(attrs={'class': 'form-control '
                                                                                                   'check_special_char'}))
    email = forms.CharField(label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # email1 = forms.EmailField(label='E-mail 1', required=False, widget=forms.TextInput(attrs={'class':
    # 'form-control'})) email2 = forms.EmailField(label='E-mail 2', required=False, widget=forms.TextInput(attrs={
    # 'class': 'form-control'})) email3 = forms.EmailField(label='E-mail 3', required=False, widget=forms.TextInput(
    # attrs={'class': 'form-control'})) email4 = forms.EmailField(label='E-mail 4', required=False,
    # widget=forms.TextInput(attrs={'class': 'form-control'})) email5 = forms.EmailField(label='E-mail 5',
    # required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    landline = forms.CharField(label='Landline', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile_num = forms.CharField(label='Mobile', required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    fax = forms.CharField(label='Fax', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    street = forms.CharField(label='Street', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    postal_code = forms.CharField(label='Postal code', required=True,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(label='City', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country_code = forms.ModelChoiceField(queryset=Country.objects.all(), label='Country',
                                          empty_label=" Please select country from drop-down ", required=False,
                                          widget=forms.Select(
                                              attrs={'class': 'form-control'}))
    language_id = forms.ModelChoiceField(queryset=Languages.objects.all(), required=False, label='Language',
                                         empty_label=" Please select language from drop-down ", widget=forms.Select(
            attrs={'class': 'form-control'}))
    currency_id = forms.ModelChoiceField(queryset=Currency.objects.all(), required=False, label='Currency',
                                         empty_label=" Please select currency in drop-down ", widget=forms.Select(
            attrs={'class': 'form-control'}))
    registration_number = forms.CharField(label='Registration number', required=False,
                                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    search_term1 = forms.CharField(label='Search Term 1', required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    search_term2 = forms.CharField(label='Search Term 2', required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    working_days = forms.CharField(widget=forms.Select(choices=working_days_choices, attrs={'class': 'form-control'}),
                                   required=False)
    duns_number = forms.CharField(label='Duns Number', required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    lockdate = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control', 'min': datetime.date.today(), 'max': '9999-12-12'}),
        label='Lock Date',
        required=False,
    )
    output_medium_types = (
        ('Print', 'Print'),
        ('Mail', 'Mail'),
        ('Fax', 'Fax'),
        ('XML / XI', 'XML / XI'),
    )
    output_medium = forms.CharField(widget=forms.Select(choices=output_medium_types, attrs={'class': 'form-control'}),
                                    required=False)
    supplier_image = forms.FileField(label='sample photo', widget=forms.FileInput, required=False)
