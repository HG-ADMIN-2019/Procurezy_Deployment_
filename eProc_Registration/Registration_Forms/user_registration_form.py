"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    user_registration_form.py
Usage:
   User register form fields
    Regform : This class is used to build the form for user registration page.
Author:
    Soni Vydyula
"""
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import forms
from django.forms import ModelForm
from django import forms
import re

from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import *
from eProc_Registration.models import UserData


class RegForm(ModelForm):
    username = forms.CharField(label='User Name',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control check_special_char mandatory_fields'}),
                               )
    first_name = forms.CharField(label='First Name',
                                 widget=forms.TextInput(attrs={'class': 'form-control check_special_char '
                                                                        'mandatory_fields'}),
                                 )
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control '
                                                                                          'check_special_char'}),
                                required=False)
    phone_num = forms.CharField(label='Phone Number',
                                widget=forms.TextInput(attrs={'class': 'form-control check_phone_number '
                                                                       'mandatory_fields'}),
                                required=False)
    language_id = forms.ModelChoiceField(queryset=Languages.objects.all(), empty_label="None", widget=forms.Select(
        attrs={'class': 'form-control mandatory_fields'}), label='Language')
    currency_id = forms.ModelChoiceField(queryset=Currency.objects.all(), empty_label="None", widget=forms.Select(
        attrs={'class': 'form-control mandatory_fields'}), label='Currency')
    time_zone = forms.ModelChoiceField(queryset=TimeZone.objects.all(), empty_label="None", widget=forms.Select(
        attrs={'class': 'form-control mandatory_fields'}), label='TimeZone')
    email = forms.EmailField(label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control mandatory_fields'}))
    is_superuser = forms.BooleanField(
        label='Super user',
        required=False,
        disabled=False,
        widget=forms.widgets.CheckboxInput(
            attrs={'class': 'form-control mandatory_fields'}),
        help_text="Super user",
    )

    # Meta data for UserData model
    class Meta:
        model = UserData
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_num', 'employee_id', 'language_id',
                  'time_zone',
                  'date_format', 'decimal_notation', 'currency_id', 'user_type', 'is_superuser']

        DATE_FORMAT_CHOICES = (
            ('DD.MM.YYYY', 'DD.MM.YYYY'),
            ('MM/DD/YYYY', 'MM/DD/YYYY'),
            ('MM-DD-YYYY', 'MM-DD-YYYY'),
            ('YYYY.MM.DD', 'YYYY.MM.DD'),
            ('YYYY/MM/DD', 'YYYY/MM/DD'),
            ('YYYY-MM-DD', 'YYYY-MM-DD'))
        DECIMAL_NOTATION_CHOICES = (
            ('1.234.567,89', '1.234.567,89'),
            ('1,234,567.89', '1,234,567.89'),
            ('1 234 567,89', '1 234 567,89')
        )
        USER_TYPE = (
            ('Buyer', 'Buyer'),
            ('Supplier', 'Supplier'),
            ('Support', 'Support')
        )
        widgets = {
            'date_format': forms.Select(choices=DATE_FORMAT_CHOICES, attrs={'class': 'form-control'}),
            'decimal_notation': forms.Select(choices=DECIMAL_NOTATION_CHOICES,
                                             attrs={'class': 'form-control'}),
            'user_type': forms.Select(choices=USER_TYPE, attrs={'class': 'form-control'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control check_special_char mandatory_fields'}),
        }

    # def clean(self):
    #     data = self.cleaned_data['is_superuser']
    #     return data


class UserRegForm(ModelForm):
    username = forms.CharField(label='User Name',
                               widget=forms.TextInput(attrs={'class': 'form-control mandatory_fields'}),
                               )
    first_name = forms.CharField(label='First Name',
                                 widget=forms.TextInput(attrs={'class': 'form-control mandatory_fields'}),
                                 )
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                required=False)
    phone_num = forms.CharField(label='Phone Number',
                                widget=forms.TextInput(attrs={'class': 'form-control mandatory_fields'}),
                                )
    language_id = forms.ModelChoiceField(queryset=Languages.objects.all(), empty_label="None", widget=forms.Select(
        attrs={'class': 'form-control mandatory_fields'}), label='Language', )
    currency_id = forms.ModelChoiceField(queryset=Currency.objects.all(), empty_label="None", widget=forms.Select(
        attrs={'class': 'form-control mandatory_fields'}), label='Currency', )
    time_zone = forms.ModelChoiceField(queryset=TimeZone.objects.all(), empty_label="None", widget=forms.Select(
        attrs={'class': 'form-control mandatory_fields'}), label='TimeZone', )
    email = forms.EmailField(label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control mandatory_fields'}))

    # Meta data for UserData model
    class Meta:
        model = UserData
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_num', 'employee_id', 'language_id',
                  'time_zone',
                  'date_format', 'decimal_notation', 'currency_id', 'user_type', 'is_superuser']

        DATE_FORMAT_CHOICES = (
            ('DD.MM.YYYY', 'DD.MM.YYYY'),
            ('MM/DD/YYYY', 'MM/DD/YYYY'),
            ('MM-DD-YYYY', 'MM-DD-YYYY'),
            ('YYYY.MM.DD', 'YYYY.MM.DD'),
            ('YYYY/MM/DD', 'YYYY/MM/DD'),
            ('YYYY-MM-DD', 'YYYY-MM-DD'))
        DECIMAL_NOTATION_CHOICES = (
            ('1.234.567,89', '1.234.567,89'),
            ('1,234,567.89', '1,234,567.89'),
            ('1 234 567,89', '1 234 567,89')
        )
        USER_TYPE = (
            ('Buyer', 'Buyer'),
            ('Supplier', 'Supplier'),
            ('Support', 'Support')
        )
        widgets = {
            'date_format': forms.Select(choices=DATE_FORMAT_CHOICES, attrs={'class': 'form-control'}),
            'decimal_notation': forms.Select(choices=DECIMAL_NOTATION_CHOICES,
                                             attrs={'class': 'form-control'}),
            'user_type': forms.Select(choices=USER_TYPE, attrs={'class': 'form-control'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control mandatory_fields'}),
        }
