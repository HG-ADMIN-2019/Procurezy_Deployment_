"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    system_setting_form.py
Usage:
   system settings form fields
     SystemSettingsForm: This class is used to build the form for system settings page.
Author:
    Soni Vydyula
"""

from django import forms

from eProc_Configuration.models import SystemSettings


class SystemSettingsForm(forms.ModelForm):
    pwd_policy = forms.ChoiceField(label='Password Policy', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                   required=False)
    login_attempts = forms.CharField(label='Login Attempts', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                     required=False)
    session_timeout = forms.CharField(label='Session Timeout', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                      required=False)
    msg_display = forms.CharField(label='Message Display time', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  required=False)
    theme_color = forms.CharField(label='Theme Colour', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  required=False)
    pagination_count = forms.CharField(label='Pagination Count',
                                       widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    attachment_size = forms.CharField(label='Size of an Attachment',
                                      widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    attachment_extension = forms.CharField(label='Attachment Extension',
                                           widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    attribute_09 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    attribute_10 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    attribute_11 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    attribute_12 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    attribute_13 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    attribute_14 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = SystemSettings
        fields = ['pwd_policy', 'login_attempts', 'session_timeout', 'msg_display', 'theme_color', 'pagination_count',
                  'attachment_size',
                  'attachment_extension', 'attribute_09', 'attribute_10', 'attribute_11', 'attribute_12',
                  'attribute_13', 'attribute_14']
