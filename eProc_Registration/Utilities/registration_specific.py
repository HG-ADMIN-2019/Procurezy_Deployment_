"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    registration_specific.py
Usage:
    creates the new user and  stores it to DB
    create_user: This function stores the new user details to DB and returns true or false.
Author:
    Soni Vydyula, Siddarth Menon
"""
import datetime

from django.forms import ModelForm
from eProc_Basic.Utilities.constants.constants import CONST_USER_REG
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import Languages, Country, Currency, SupplierMaster
from eProc_Emails.Utilities.email_notif_generic import email_notify
from eProc_System_Settings.Utilities.system_settings_generic import sys_attributes

django_query_instance = DjangoQueries()


class RegFncts(ModelForm):
    @staticmethod
    def create_user(request, new_user, client, password):
        """
        creates the new user and  stores it to DB
        :param request: request data from UI
        :param new_user: takes the input from UI while new user is created
        :return: returns true or false upon saving data to DB.
        """
        new_user.client = client
        # new_user.date_joined = datetime.datetime.now()
        new_user.save()
        variant_name = CONST_USER_REG
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        email_data = {
            'username': username,
            'email': email,
            'first_name': first_name,
            'email_user_monitoring_guid': '',
            'password': password
        }
        email_notify(email_data, variant_name, client)
        return True


def save_supplier_registration(request):
    django_query_instance.django_create_query(SupplierMaster, {
        'supp_guid': guid_generator(),
        'client': global_variables.GLOBAL_CLIENT,
        'supplier_id': request.POST['supplier_id'],
        'supp_type': request.POST['supp_type'],
        'name1': request.POST['name1'],
        'name2': request.POST['name2'],
        'city': request.POST['city'],
        'postal_code': request.POST['postal_code'],
        'street': request.POST['street'],
        'landline': request.POST['landline'],
        'mobile_num': request.POST['mobile_num'],
        'fax': request.POST['fax'],
        'email': request.POST['email'],
        'email1': request.POST['email1'],
        'email2': request.POST['email2'],
        'email3': request.POST['email3'],
        'email4': request.POST['email4'],
        'email5': request.POST['email5'],
        'output_medium': request.POST['output_medium'],
        'search_term1': request.POST['search_term1'],
        'search_term2': request.POST['search_term2'],
        'duns_number': request.POST['duns_number'],
        'delivery_days': request.POST['working_days'],
        'registration_number': request.POST['registration_number'],
        'language_id': django_query_instance.django_get_query(Languages, {'language_id': request.POST['language_id']}),
        'country_code': django_query_instance.django_get_query(Country, {'country_code': request.POST['country_code']}),
        'currency_id': django_query_instance.django_get_query(Currency, {'currency_id': request.POST['currency_id']})
    })

