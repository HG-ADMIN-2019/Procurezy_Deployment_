"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    registration_model.py
Usage:
     Saves the data for new user registration
     supplier_registration_form : Get the form and the data from UI which supplier has entered  and saves the data to DB,returning the supplier_register.html page.
Author:
    Siddarth Menon
"""
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG177, MSG179
from eProc_Configuration.models import *
from eProc_Registration.Utilities.registration_generic import save_supplier_image
from eProc_Registration.Utilities.registration_specific import save_supplier_registration
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Suppliers.SupplierForms.supplier_registration_form import SupplierRegForm
from eProc_Suppliers.models.suppliers_model import OrgSuppliers

django_query_instance = DjangoQueries()


@login_required
@transaction.atomic
def supplier_registration_form(request):
    """

    :param request: Request data from UI
    :return: render supplier_register.html
    """

    update_user_info(request)
    supplier_form = SupplierRegForm()
    purch_org_list = []
    currency_list = []
    payterm_list = []
    incoterm_list = []

    purch_org = django_query_instance.django_filter_only_query(OrgPorg, {
        'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
    }).values('porg_id')

    for porg_data in purch_org:
        purch_org_list.append(porg_data['porg_id'])

    currency_id = Currency.objects.values('currency_id')
    for currency_data in currency_id:
        currency_list.append(currency_data['currency_id'])

    payterm = django_query_instance.django_filter_only_query(Payterms, {
        'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
    }).values('payment_term_key')

    for payterm_data in payterm:
        payterm_list.append(payterm_data['payment_term_key'])

    incoterms = Incoterms.objects.values('incoterm_key')
    for incoterm_data in incoterms:
        incoterm_list.append(incoterm_data['incoterm_key'])

    if request.method == 'POST':
        supplier_form = SupplierRegForm(request.POST or None)

        # if supplier_form.is_valid():
        save_supplier_registration(request)
        if 'supplier_image' in request.FILES:
            supplier_file = request.FILES['supplier_image']
            supplier_id = request.POST['supplier_id']
            supplier_image_name = request.FILES['supplier_image'].name
            save_supplier_image(supplier_file, supplier_id, supplier_image_name)
            msgid = 'MSG177'
            error_msg = get_message_desc(msgid)[1]

        messages.success(request, error_msg)
        # else:
        print(supplier_form.errors)

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'purch_org': purch_org_list,
        'currency_id': currency_list,
        'payterm_list': payterm_list,
        'incoterm_list': incoterm_list,
        'supplier_form': supplier_form,
    }

    return render(request, 'Supplier Registration/supplier_register.html', context)


@transaction.atomic
def supplier_registration_second_step(request):
    client = getClients(request)
    supplier_org_data = JsonParser().get_json_from_req(request)
    for supplier_data in supplier_org_data:
        guid = guid_generator()
        defaults = {
            'guid': guid,
            'supplier_id': supplier_data['supp_id'],
            'porg_id': supplier_data['porg_id'],
            'currency_id': django_query_instance.django_get_query(Currency, {
                'currency_id': supplier_data['currency_id'], 'del_ind': False
            }),

            'payment_term_key': django_query_instance.django_get_query(Payterms, {
                'payment_term_key': supplier_data['payment_term'], 'del_ind': False, 'client': client
            }),

            'incoterm_key': django_query_instance.django_get_query(Incoterms,
                                                                   {'incoterm_key': supplier_data['incoterm1'],
                                                                    'del_ind': False}),
            'gr_inv_vrf': supplier_data['gr_inv_vrf'],
            'inv_conf_exp': supplier_data['inv_conf_exp'],
            'gr_conf_exp': supplier_data['gr_conf_exp'],
            'po_resp': supplier_data['po_resp'],
            'ship_notif_exp': supplier_data['ship_notif_exp'],
            'purch_block': supplier_data['purch_block'],
            'del_ind': False,
            'client_id': django_query_instance.django_get_query(OrgClients, {'client': client})
        }
        django_query_instance.django_update_or_create_query(OrgSuppliers, {'guid': guid}, defaults)
        msgid = 'MSG179'
        error_msg = get_message_desc(msgid)[1]

    return JsonResponse({'message': error_msg})
