"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    personal_settings_forms.py
Usage:
    get personal settings forms
    PersonalSettingsForm - create PersonalSettingsForm in editable mode
    PersonalSettingsDisplayForm - create PersonalSettingsForm in non editable mode

Author:
    Deepika K
"""
from django import forms

from eProc_Basic.Utilities.functions.get_db_query import django_query_instance
from eProc_Basic.Utilities.messages.messages import MSG020, MSG026
from eProc_Basic.models import *
from eProc_Configuration.models import *
from eProc_Configuration.models.basic_data import Languages
from eProc_Registration.models import UserData


class PersonalSettingsForm(forms.ModelForm):
    language_id = forms.ModelChoiceField(queryset=Languages.objects.filter(del_ind=False), label='Language')
    currency_id = forms.ModelChoiceField(queryset=Currency.objects.filter(del_ind=False), label='Currency')
    time_zone = forms.ModelChoiceField(queryset=TimeZone.objects.filter(del_ind=False))

    # def clean(self):
    #     cleaned_data = super().clean()
    #     first_name = cleaned_data.get('first_name')
    #     last_name = cleaned_data.get('last_name')
    #
    #     regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    #     # To restrict the wildcard search to 3 characters and form fields validations
    #
    #     if regex.search(first_name):
    #         raise forms.ValidationError('Name cannot contain special characters')
    #
    #     if regex.search(last_name):
    #         raise forms.ValidationError('Name cannot contain special characters')

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if '@' in first_name or '-' in first_name or '|' in first_name:
            raise forms.ValidationError("Name cannot contain special characters")
        return first_name

    class Meta:
        model = UserData
        fields = ('username', 'first_name', 'last_name', 'email', 'language_id', 'time_zone', 'date_format',
                  'employee_id', 'decimal_notation', 'currency_id')
        labels = {
            "username": "User Name",
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email ID",
            "time_zone": "Time Zone",
            "date_format": "Date Format",
            "employee_id": "Employee ID",
            "decimal_notation": "Decimal Notation",
            "currency_id": "Currency",
        }

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
        widgets = {
            'username': forms.TextInput(attrs={'class': 'hg_edit_mode', 'readonly': 'readonly'}),
            'first_name': forms.TextInput(attrs={'class': 'form-group col-sm'}),
            'date_format': forms.Select(choices=DATE_FORMAT_CHOICES),
            'decimal_notation': forms.Select(choices=DECIMAL_NOTATION_CHOICES),
            'employee_id': forms.TextInput(attrs={'class': 'hg_display_mode', 'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'class': 'hg_edit_mode', 'readonly': 'readonly'}),

        }

    def __init__(self, *args, **kwargs):
        super(PersonalSettingsForm, self).__init__(*args, **kwargs)
        for personal_setting_data in self.fields:
            self.fields[personal_setting_data].widget.attrs.update({'class': 'form-control'})
            self.fields['employee_id'].widget.attrs.update({'class': 'form-control'})
            self.fields['email'].widget.attrs.update({'class': 'form-control'})
            self.fields['employee_id'].required = False
            self.fields['email'].required = False


class PersonalSettingsDisplayForm(forms.ModelForm):
    language_id= forms.ModelChoiceField(queryset=Languages.objects.all(),label='Language',widget=forms.Select(attrs={'style':'width:100%;'}))
    currency_id = forms.ModelChoiceField(queryset=Currency.objects.all(),label='Currency',widget=forms.Select(attrs={'style':'width:100%;'}))
    time_zone = forms.ModelChoiceField(queryset=TimeZone.objects.all(),widget=forms.Select(attrs={'style':'width:100%;'}))

    class Meta:
        model = UserData
        fields = ('username', 'first_name', 'last_name', 'email', 'language_id','time_zone','date_format','employee_id',
                  'decimal_notation', 'currency_id')
        labels = {
            "username":"User Name",
            "first_name": "First Name",
            "last_name":"Last Name",
            "email":"Email ID",
            "time_zone":"Time Zone",
            "date_format":"Date Format",
            "employee_id":"Employee ID",
            "decimal_notation":"Decimal Notation",
            "currency_id":"Currency",
        }

    def __init__(self, *args, **kwargs):
        from django.forms.widgets import Select
        super(PersonalSettingsDisplayForm, self).__init__(*args, **kwargs)
        for personal_setting_data in self.fields:
            self.fields[personal_setting_data].widget.attrs.update({'class': 'form-control'})
            if isinstance(self.fields[personal_setting_data].widget, Select):
                self.fields['employee_id'].required = False
                self.fields['email'].required = False
                self.fields['username'].required = False
                self.fields[personal_setting_data].widget.attrs['disabled'] = 'disabled'
            else:
                self.fields[personal_setting_data].widget.attrs['readonly'] = 'readonly'
