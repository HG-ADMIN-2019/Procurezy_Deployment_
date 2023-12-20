from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

from eProc_Basic.Utilities.functions.encryption_util import encrypt, decrypt
from eProc_Basic.Utilities.functions.guid_generator import dynamic_guid_generator
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.messages.messages import MSG129, MSG130
from eProc_Content_Search.Utilities.content_search_generic import freetext_search
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import get_prod_cat, get_supplier_first_second_name
from eProc_Basic.Utilities.functions.get_db_query import *
from eProc_Form_Builder.Utilities.form_builder_generic import *
from eProc_Form_Builder.models import *
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Shopping_Cart.context_processors import update_user_info

JsonParser_obj = JsonParser()
django_query_instance = DjangoQueries()


@login_required
@transaction.atomic
def create_or_update_freetext_form(request, freetext_id):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    client = getClients(request)
    freetext_details = {}
    eform_configured = []
    supplier_details = get_supplier_first_second_name(client)
    if request.method == 'GET':
        if freetext_id != 'None':
            freetext_action = 'UPDATE'
            freetext_id = decrypt(freetext_id)
            if django_query_instance.django_existence_check(FreeTextDetails,
                                                            {'client': client,
                                                             'freetext_id': freetext_id,
                                                             'del_ind': False}):
                freetext_details = django_query_instance.django_filter_query(FreeTextDetails,
                                                                             {'client': client,
                                                                              'freetext_id': freetext_id,
                                                                              'del_ind': False},
                                                                             None,
                                                                             None)[0]
                eform_configured = get_freetext_eform_detail(freetext_details['eform_id'])
        else:
            freetext_action = 'CREATE'
            freetext_id = dynamic_guid_generator(16)
    encrypt_freetext_id = encrypt(freetext_id)
    context = {
        'inc_nav': True,
        'product_category': get_prod_cat(),
        'supplier_details': supplier_details,
        'freetext_id': freetext_id,
        'freetext_details': freetext_details,
        'eform_configured': eform_configured,
        'currency_list': get_currency_data(),
        'country_list': get_country_data(),
        'encrypt_freetext_id': encrypt_freetext_id,
        'freetext_action': freetext_action
    }

    return render(request, 'Form_Builder/create_freetext_form.html', context)


@login_required
def display_freetext_forms(request):
    update_user_info(request)
    client = getClients(request)
    freetext_details = []
    if request.method == 'GET':
        freetext_details = get_ft_data()

    elif request.is_ajax():
        item_details = JsonParser().get_json_from_req(request)
        freetext_query = freetext_search(**item_details)
        freetext_query = update_ft(freetext_query)
        return JsonResponse(freetext_query, safe=False)
    # used_forms = django_query_instance.django_filter_value_list_query(EformData, {'client': client}, 'form_id')
    context = {
        'inc_nav': True,
        'is_slide_menu': True,
        'is_content_mgmnt_active': True,
        'encrypted_freetext_id': None,
        'display_available_forms': freetext_details,
        'supplier_details': get_supplier_first_second_name(client),
        'product_category': get_prod_cat(),
        'catalogs': django_query_instance.django_filter_only_query(Catalogs, {'client': client, 'del_ind': False,
                                                                              'is_active_flag': True}),
        'currency_list': get_currency_data(),
        'country_list': get_country_data(),
        # 'used_forms': used_forms
    }
    return render(request, 'Form_Builder/display_available_forms.html', context)


# This function is used to delete freetext form (not freetext item)
# @login_required
# def display_fields_to_update(request):
#     client = getClients(request)
#     form_id = request.POST.get('form_id')
#     form_instance = django_query_instance.django_get_query(FreeTextDetails, {'client': client,
#                                                                           'form_id': form_id, 'del_ind': False})
#     print(form_instance)
#     supplier_id = form_instance.supplier_id
#     product_category = form_instance.prod_cat_id
#     update_form_instance = FormBuilder().get_freetext_form(supplier_id, product_category, client)
#     return JsonResponse({'update_form_instance': update_form_instance})


def create_update_freetext_form(request):
    """

    """
    update_user_info(request)
    data_dictionary = JsonParser_obj.get_json_from_req(request)
    # Save FT and its eform into DB
    create_freetext = FormBuilder().save_freetext_form(data_dictionary)
    if create_freetext[0]:
        return JsonResponse({'success_message': create_freetext[1]}, status=201)

    else:
        return JsonResponse({'error_message': create_freetext[1]}, status=400)
