"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    password_change_form.py
Usage:
     class PasswordChangeCustomForm - Custom form for password change

Author:
    Babu / Siddarth
"""
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import CharField, PasswordInput


# Custom form for password change
class PasswordChangeCustomForm(PasswordChangeForm):
    error_messages = {
        'password_incorrect': "Please enter a valid old password",
        'password_mismatch': "Passwords do not match"
    }
    error_css_class = 'has-error'
    old_password = CharField(required=True, label='Old Password',
                             widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}))
    new_password1 = CharField(required=True, label='New Password',
                              widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    new_password2 = CharField(required=True, label='Confirm New Password',
                              widget=PasswordInput(
                                  attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}))
