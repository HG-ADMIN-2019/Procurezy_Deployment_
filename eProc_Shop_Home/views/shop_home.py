"""Copyright (c) 2021 Hiranya Garbha, Inc.
Name:
    call_off_form_templates.py
Usage:
     shopping_cart_home - Renders shopping cart home page
Author:
    Siddarth
"""
import json
import operator
from datetime import timedelta
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from eProc_Basic.Utilities.functions.distinct_list import distinct_list
from eProc_Basic.Utilities.functions.encryption_util import encrypt
from eProc_Basic.Utilities.functions.generate_document_number import generate_document_number
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.functions.sort_dictionary import sort_list_dictionary_key_values
from eProc_Basic.Utilities.messages.messages import MSG112
from eProc_Catalog.Utilities import catalog_global_variables
from eProc_Catalog.Utilities.catalog_generic import append_image_into_catalog_list
from eProc_Catalog.Utilities.catalog_specific import update_product_pricing
from eProc_Form_Builder.models import EformFieldData
from eProc_Org_Support.models import OrgSupport
from eProc_Shop_Home.Utilities.shop_home_specific import ShopHome
from eProc_Shop_Home.models import FavouriteCart, RecentlyViewedProducts
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import *
from eProc_Basic.Utilities.functions.get_db_query import *
from eProc_Shopping_Cart.context_processors import update_user_info
from collections import Counter
from itertools import islice
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries, bulk_create_entry_db
import datetime
from eProc_Shopping_Cart.models import ScItem, ScHeader
from eProc_System_Settings.Utilities.system_settings_generic import sys_attributes

django_query_instance = DjangoQueries()

import logging

logger = logging.getLogger('django')


@login_required
def shopping_cart_home(request):
    """
    :param request: Takes request from the user and returns home page of shopping cart application
    :return: Renders home.html after processing the request from user
    """
    # logger.info('Login to home page')
    # logger.debug('debug Login to home page')
    update_user_info(request)
    shop_home_instance = ShopHome()
    prod_id_list = []
    fav_cart_product_id = []
    freetext_prodcat = []
    freetext_supp_id = []
    freetext_item_flag = ''
    freetext_price = []
    # delete_all_shopping_carts({'client':global_variables.GLOBAL_CLIENT}, global_variables.GLOBAL_CLIENT)
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_home_active': True
    }

    client = global_variables.GLOBAL_CLIENT
    username = global_variables.GLOBAL_LOGIN_USERNAME
    search_fields = {}
    from_date = datetime.date.today() - timedelta(days=30)
    min_date = datetime.datetime.combine(from_date, datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    search_fields['created_at__gte'] = min_date
    search_fields['created_at__lte'] = today_max

    obj_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT, global_variables.GLOBAL_LOGIN_USER_OBJ_ID)

    # get user's default company code value
    company_code_list, default_company_code = OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(
        obj_id_list, CONST_CO_CODE)

    catalog_id_list = django_query_instance.django_filter_value_list_query(
        OrgAttributesLevel, {
            'client': client, 'object_id__in': obj_id_list, 'attribute_id': CONST_CAT_ID, 'del_ind': False
        }, 'low')
    catalog_global_variables.USER_ASSIGNED_CATALOGS_LIST = django_query_instance.django_filter_value_list_query(
        Catalogs,
        {'client': global_variables.GLOBAL_CLIENT,
         'catalog_id__in': catalog_id_list,
         'del_ind': False,
         'is_active_flag': True}, 'catalog_id')
    assigned_catalog_id_list = catalog_global_variables.USER_ASSIGNED_CATALOGS_LIST

    search_fields['client'] = client
    search_fields['co_code'] = default_company_code
    search_fields['status'] = CONST_SC_HEADER_APPROVED
    search_fields['del_ind'] = False

    get_sc_header_guid = django_query_instance.django_filter_value_list_query(ScHeader, search_fields, 'guid')

    product_id = django_query_instance.django_filter_value_list_query(ScItem, {
        'client': client, 'comp_code': default_company_code, 'header_guid__in': get_sc_header_guid,
        'call_off': CONST_CATALOG_CALLOFF, 'del_ind': False
    }, 'int_product_id')
    product_id_list = []
    product_id_data = distinct_list(product_id)
    for product in product_id_data:
        if django_query_instance.django_existence_check(CatalogMapping,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'catalog_id__in': assigned_catalog_id_list,
                                                         'item_id': product}):
            product_id_list.append(product)

    # Counts repeated elements
    get_product_count = dict(Counter(product_id_list))

    # Sort product id count in descending order
    sort_get_product_count = dict(sorted(get_product_count.items(), key=operator.itemgetter(1), reverse=True))
    product_id_number = list(sort_get_product_count.keys())

    # Get top 10 values of product id
    popular_product_id = list(islice(product_id_number, CONST_POPULAR_ITEMS_LIMIT))

    product_details_value = django_query_instance.django_filter_only_query(ProductsDetail, {
        'product_id__in': popular_product_id, 'client': client, 'del_ind': False
    }).values()
    # print(product_details_value)
    # Get image data
    image_info = django_query_instance.django_filter_only_query(ImagesUpload, {
        'image_default': True, 'client': client, 'del_ind': False,
        'image_id__in': popular_product_id, 'image_type': CONST_CATALOG_IMAGE_TYPE
    }).values('image_id', 'image_url')
    product_details_value = update_product_pricing(product_details_value)
    popular_product_array = append_image_into_catalog_list(product_details_value, image_info)
    if popular_product_array:
        for product in popular_product_array:
            product['encrypt_product_id'] = encrypt(product['product_id'])
            product = update_supplier_desc(product)
    context['popular_product_array'] = popular_product_array
    sys_attributes_instance = sys_attributes(client)
    context['frequently_purchased_flag'] = sys_attributes_instance.get_frequently_purchased()
    context['recently_viewed_flag'] = sys_attributes_instance.get_recently_viewed()

    # Renders favourite shopping carts
    if django_query_instance.django_existence_check(FavouriteCart, {'client': client, 'username': username}):
        fav_cart_num_list = list(django_query_instance.django_filter_only_query(FavouriteCart, {'client': client,
                                                                                                'username': username}).values(
            'favourite_cart_number',
            'favourite_cart_name',
            'fc_total_value',
            'fc_total_currency').order_by('favourite_cart_number').distinct())

        for cart_num in fav_cart_num_list:
            cart_num['fc_count'] = django_query_instance.django_filter_count_query(FavouriteCart,
                                                                                   {'client': client,
                                                                                    'favourite_cart_number': cart_num[
                                                                                        'favourite_cart_number']
                                                                                    })

        context['fav_cart_num_list'] = fav_cart_num_list

        fav_cart_detail = django_query_instance.django_filter_only_query(FavouriteCart,
                                                                         {'client': client,
                                                                          'username': username}).values().order_by(
            'favourite_cart_number')

        for cart_items_data in fav_cart_detail:
            prod_id_list.append(cart_items_data['int_product_id'])

        # Get image data
        item_image_info = django_query_instance.django_filter_only_query(ImagesUpload, {
            'client': client, 'image_default': True, 'image_id__in': prod_id_list,
            'image_type': CONST_CATALOG_IMAGE_TYPE, 'del_ind': False
        }).values('image_id', 'image_url')

        # Checking whether the product exists in catalog

        for cart_items_prod_id in fav_cart_detail:
            freetext_price.append(cart_items_prod_id['price'])
            fav_cart_product_id.append(cart_items_prod_id['int_product_id'])
            freetext_prodcat.append(cart_items_prod_id['prod_cat_id'])
            freetext_supp_id.append(cart_items_prod_id['supplier_id'])

            catalog_product_flag = django_query_instance.django_existence_check(ProductsDetail, {
                'product_id': cart_items_prod_id['int_product_id'], 'client': client, 'del_ind': False})
            freetext_formid = django_query_instance.django_filter_value_list_query(FreeTextForm, {
                'prod_cat_id': cart_items_prod_id['prod_cat_id'], 'client': client, 'del_ind': False}, 'form_id')
            # print(freetext_formid)
            freetext_item_flag = django_query_instance.django_existence_check(FreeTextForm, {
                'form_id__in': freetext_formid, 'client': client, 'del_ind': False})
            if freetext_item_flag:
                freetext_item_flag = 1
            else:
                freetext_item_flag = 0
            # if catalog_product_flag:

        context['fav_cart_detail'] = fav_cart_detail
        context['item_image_info'] = item_image_info
        context['fav_cart_product_id'] = fav_cart_product_id
        context['freetext_item_flag'] = freetext_item_flag
        context['freetext_prodcat'] = freetext_prodcat
        context['freetext_supp_id'] = freetext_supp_id
        context['freetext_price'] = freetext_price

    # Display recently viewed products
    # django_query_instance.django_filter_only_query(RecentlyViewedProducts, {'username': username,
    #                                                                         'client': client,
    #                                                                         'del_ind': False}).exclude(
    #     catalog_id__in=assigned_catalog_id_list).delete()

    recently_viewed_product_id = list(django_query_instance.django_filter_only_query(RecentlyViewedProducts, {
        'username': username, 'client': client, 'del_ind': False
    }).order_by('-recently_viewed_prod_changed_at').values_list('product_id', flat=True))

    print(recently_viewed_product_id)
    recently_viewed_product_details_value = django_query_instance.django_filter_only_query(ProductsDetail, {
        'product_id__in': recently_viewed_product_id, 'client': client, 'del_ind': False
    }).values()

    # Get image data
    recently_viewed_product_image_info = django_query_instance.django_filter_only_query(ImagesUpload, {
        'client': client, 'image_default': True, 'image_id__in': recently_viewed_product_id,
        'image_type': CONST_CATALOG_IMAGE_TYPE, 'del_ind': False
    }).values('image_id', 'image_url')
    recently_viewed_product_details_value = update_product_pricing(recently_viewed_product_details_value)
    product_data_and_image_array = append_image_into_catalog_list(recently_viewed_product_details_value,
                                                                  recently_viewed_product_image_info)

    recently_viewed_product_array = sort_list_dictionary_key_values(recently_viewed_product_id,
                                                                    product_data_and_image_array, 'product_id')
    if recently_viewed_product_array:
        for recently_viewed_product in recently_viewed_product_array:
            recently_viewed_product['encrypt_product_id'] = encrypt(recently_viewed_product['product_id'])
            recently_viewed_product = update_supplier_desc(recently_viewed_product)

    context['recently_viewed_product_array'] = recently_viewed_product_array

    # Organizational Announcements
    context['org_announcements_data'] = shop_home_instance.get_org_announcements()
    # print(context['org_announcements_data'])

    # org support email

    support_chat_array = []
    support_email_array = []
    support_phone_array = []
    support_call = ''
    support_email_data = ''
    support_uname = ''

    support_email = django_query_instance.django_filter_only_query(OrgSupport, {
        'org_support_types': 'EMAIL', 'client': client, 'del_ind': False
    })
    for email in support_email:
        if support_email is not None and len(support_email) > 1:
            support_email_array.append(email.org_support_email)
            support_email_data = json.dumps(support_email_array)
        else:
            # support_email_array.append(email.org_support_email)
            support_email_data = [email.org_support_email]

    support_phone = django_query_instance.django_filter_only_query(OrgSupport, {
        'org_support_types': 'CALL', 'client': client, 'del_ind': False
    })

    for phone in support_phone:
        if support_phone is not None and len(support_phone) > 1:
            support_phone_array.append(phone.org_support_number)
            support_call = json.dumps(support_phone_array)
        else:
            # support_phone_array.append(phone.org_support_number)
            support_call = [phone.org_support_number]

    support_chat = django_query_instance.django_filter_only_query(OrgSupport, {
        'org_support_types': 'CHAT', 'client': client, 'del_ind': False
    })

    support_uname = []  # Initialize the list outside the loop

    if support_chat is not None and len(support_chat) > 1:
        for chat in support_chat:
            support_uname.append(chat.username.strip("[]'"))
    else:
        if len(support_chat) == 1:
            support_uname = [support_chat[0].username.strip("[]'")]

    context['support_email'] = support_email_data
    context['support_phone'] = support_call
    context['support_chat'] = support_uname

    return render(request, 'Shop_Home/home.html', context)


def add_favourite_shopping_cart(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    username = global_variables.GLOBAL_LOGIN_USERNAME

    if request.method == 'POST':
        favourite_cart_name = request.POST.get('favourite_cart_name')
        total_cart_value = request.POST.get('total_cart_value')
        total_cart_currency = request.POST.get('total_cart_currency')

        fav_cart_list_count = list(django_query_instance.django_filter_only_query(FavouriteCart, {
            'client': client, 'username': username
        }).values('favourite_cart_number').distinct())

        if len(fav_cart_list_count) == CONST_FAVOURITE_SC_LIMIT:
            msgid = 'MSG158'
            error_msg = get_message_desc(msgid)[1]

            return JsonResponse({'error_message': error_msg}, status=201)
        else:
            # check if favourite cart name already exists
            if django_query_instance.django_existence_check(FavouriteCart, {
                'client': client, 'username': username, 'favourite_cart_name': favourite_cart_name, 'del_ind': False
            }):
                msgid = 'MSG159'
                error_msg = get_message_desc(msgid)[1]

                return JsonResponse({'error_message': error_msg}, status=201)

            object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT,
                                                     global_variables.GLOBAL_LOGIN_USER_OBJ_ID)
            generated_doc_detail = generate_document_number(CONST_FC_TRANS_TYPE, global_variables.GLOBAL_CLIENT,
                                                            object_id_list,
                                                            False, CONST_DOC_TYPE_FC)
            fav_cart_number = generated_doc_detail[0]

            if fav_cart_number:
                update_number_range = django_query_instance.django_filter_only_query(NumberRanges, {
                    'sequence': int(generated_doc_detail[1]), 'document_type': CONST_DOC_TYPE_FC, 'client': client
                })

                update_number_range.update(current=fav_cart_number, client=client)

                cart_item_data = django_query_instance.django_filter_only_query(CartItemDetails, {
                    'client': client, 'username': username
                }).values()

                for items_details in cart_item_data:
                    guid = guid_generator()
                    defaults = {
                        'item_num': items_details['item_num'],
                        'description': items_details['description'],
                        'prod_cat_desc': items_details['prod_cat_desc'],
                        'prod_cat_id': items_details['prod_cat_id'],
                        'int_product_id': items_details['int_product_id'],
                        'supp_product_id': items_details['supp_product_id'],
                        'quantity': items_details['quantity'],
                        'unit': items_details['unit'],
                        'price': items_details['price'],
                        'base_price': items_details['base_price'],
                        'additional_price': items_details['additional_price'],
                        'actual_price': items_details['actual_price'],
                        'discount_percentage': items_details['discount_percentage'],
                        'discount_value': items_details['discount_value'],
                        'sgst': items_details['sgst'],
                        'cgst': items_details['cgst'],
                        'vat': items_details['vat'],
                        'tax_value': items_details['tax_value'],
                        'gross_price': items_details['gross_price'],
                        'price_unit': items_details['price_unit'],
                        'currency': items_details['currency'],
                        'supplier_id': items_details['supplier_id'],
                        'pref_supplier': items_details['pref_supplier'],
                        'lead_time': items_details['lead_time'],
                        'value': items_details['value'],
                        'manu_part_num': items_details['manu_part_num'],
                        'manu_code_num': items_details['manu_code_num'],
                        'call_off': items_details['call_off'],
                        'supplier_mobile_num': items_details['supplier_mobile_num'],
                        'supplier_fax_no': items_details['supplier_fax_no'],
                        'supplier_email': items_details['supplier_email'],
                        'quantity_min': items_details['quantity_min'],
                        'value_min': items_details['value_min'],
                        'tiered_flag': items_details['tiered_flag'],
                        'bundle_flag': items_details['bundle_flag'],
                        'tax_code': items_details['tax_code'],
                        'delivery_days': items_details['delivery_days'],
                        'catalog_id': items_details['catalog_id'],
                        'catalog_item': items_details['catalog_item'],
                        'ctr_num': items_details['ctr_num'],
                        'ctr_name': items_details['ctr_name'],
                        'prod_type': items_details['prod_type'],
                        'item_del_date': items_details['item_del_date'],
                        'process_type': items_details['process_type'],
                        'start_date': items_details['start_date'],
                        'end_date': items_details['end_date'],
                        'ir_gr_ind_limi': items_details['ir_gr_ind_limi'],
                        'gr_ind_limi': items_details['gr_ind_limi'],
                        'overall_limit': items_details['overall_limit'],
                        'expected_value': items_details['expected_value'],
                        'username': items_details['username'],
                        'eform_id': items_details['eform_id'],
                        'client_id': client
                    }

                    django_query_instance.django_update_or_create_query(FavouriteCart, {
                        'favourite_cart_guid': guid, 'favourite_cart_number': fav_cart_number,
                        'favourite_cart_name': favourite_cart_name, 'fc_total_value': total_cart_value,
                        'fc_total_currency': total_cart_currency
                    }, defaults)
                    if items_details['eform_id']:
                        eform_transaction_data = django_query_instance.django_filter_query(EformFieldData,
                                                                                           {'eform_id': items_details[
                                                                                               'eform_id'],
                                                                                            'cart_guid': items_details[
                                                                                                'guid'],
                                                                                            'client': global_variables.GLOBAL_CLIENT},
                                                                                           None, None)
                        dictionary_list = []
                        for eform_transaction in eform_transaction_data:
                            if eform_transaction['product_eform_pricing_guid_id']:
                                product_eform_pricing_guid = django_query_instance.django_get_query(ProductEformPricing,
                                                                                                    {
                                                                                                        'product_eform_pricing_guid':
                                                                                                            eform_transaction[
                                                                                                                'product_eform_pricing_guid_id']})
                            else:
                                product_eform_pricing_guid = None
                            eform_dictionary = {'eform_field_data_guid': guid_generator(),
                                                'eform_id': eform_transaction['eform_id'],
                                                'favourite_cart_guid': guid,
                                                'product_eform_pricing_guid': product_eform_pricing_guid,
                                                'eform_type': CONST_CATALOG_ITEM_VARIANT,
                                                'eform_field_count': int(eform_transaction['eform_field_count']),
                                                'eform_field_name': eform_transaction['eform_field_name'],
                                                'client': global_variables.GLOBAL_CLIENT,
                                                'eform_field_data': eform_transaction['eform_field_data']}
                            dictionary_list.append(eform_dictionary)
                        bulk_create_entry_db(EformFieldData, dictionary_list)
                msgid = 'MSG160'
                error_msg = get_message_desc(msgid)[1]

                return JsonResponse({'success_message': error_msg}, status=201)
            else:
                return JsonResponse({'error_message': generated_doc_detail[1]}, status=201)


def sort_product_list_based_on_product_id(recently_viewed_product_id, recently_viewed_product_array):
    viewed_products_list = []
    for product_id in recently_viewed_product_id:
        for sort_product_array in recently_viewed_product_array:
            if sort_product_array['product_id'] == product_id:
                viewed_products_list.append(sort_product_array)
    return viewed_products_list


def delete_recently_viewed_item(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    username = global_variables.GLOBAL_LOGIN_USERNAME

    if request.method == 'POST':
        item_prod_id = request.POST.get('item_prod_id')

        django_query_instance.django_filter_delete_query(RecentlyViewedProducts, {
            'username': username, 'product_id': item_prod_id, 'client': client, 'del_ind': False
        })
        recently_viewed_count = django_query_instance.django_filter_count_query(RecentlyViewedProducts,
                                                                                {'username': username,
                                                                                 'client': client,
                                                                                 'del_ind': False})
        msgid = 'MSG113'
        error_msg = get_message_desc(msgid)[1]
        return JsonResponse({'success': error_msg, 'recently_viewed_count': recently_viewed_count}, status=201)


def delete_favourite_shopping_cart(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    username = global_variables.GLOBAL_LOGIN_USERNAME

    if request.method == 'POST':
        fav_cart_num = request.POST.get('fav_cart_num')

        django_query_instance.django_filter_delete_query(FavouriteCart, {
            'favourite_cart_number': fav_cart_num, 'username': username, 'client': client, 'del_ind': False
        })

        msgid = 'MSG113'
        error_msg = get_message_desc(msgid)[1]

        return JsonResponse({'success': error_msg}, status=201)


def add_fav_sc_to_cart(request):
    """

    """
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    username = global_variables.GLOBAL_LOGIN_USERNAME
    response = {}
    if request.method == 'POST':
        fav_cart_num = request.POST.get('fav_cart_num')
        django_query_instance.django_filter_delete_query(CartItemDetails,
                                                         {'username': global_variables.GLOBAL_LOGIN_USERNAME,
                                                          'client': global_variables.GLOBAL_CLIENT})
        fav_cart_detail = django_query_instance.django_filter_query(FavouriteCart,
                                                                    {'favourite_cart_number': fav_cart_num,
                                                                     'username': username, 'client': client,
                                                                     'del_ind': False},
                                                                    None,
                                                                    None)
        cart_list = []
        for items_details in fav_cart_detail:
            guid = guid_generator()
            defaults = {
                'guid': guid,
                'item_num': items_details['item_num'],
                'description': items_details['description'],
                'prod_cat_desc': items_details['prod_cat_desc'],
                'prod_cat_id': items_details['prod_cat_id'],
                'int_product_id': items_details['int_product_id'],
                'quantity': items_details['quantity'],
                'unit': items_details['unit'],
                'price': items_details['price'],
                'base_price': items_details['base_price'],
                'additional_price': items_details['additional_price'],
                'actual_price': items_details['actual_price'],
                'discount_percentage': items_details['discount_percentage'],
                'discount_value': items_details['discount_value'],
                'sgst': items_details['sgst'],
                'cgst': items_details['cgst'],
                'vat': items_details['vat'],
                'tax_value': items_details['tax_value'],
                'gross_price': items_details['gross_price'],
                'price_unit': items_details['price_unit'],
                'currency': items_details['currency'],
                'supplier_id': items_details['supplier_id'],
                'pref_supplier': items_details['pref_supplier'],
                'lead_time': items_details['lead_time'],
                'value': items_details['value'],
                'manu_part_num': items_details['manu_part_num'],
                'manu_code_num': items_details['manu_code_num'],
                'supp_product_id': items_details['supp_product_id'],
                'call_off': items_details['call_off'],
                'supplier_mobile_num': items_details['supplier_mobile_num'],
                'supplier_fax_no': items_details['supplier_fax_no'],
                'supplier_email': items_details['supplier_email'],
                'quantity_min': items_details['quantity_min'],
                'value_min': items_details['value_min'],
                'tiered_flag': items_details['tiered_flag'],
                'bundle_flag': items_details['bundle_flag'],
                'tax_code': items_details['tax_code'],
                'delivery_days': items_details['delivery_days'],
                'catalog_id': items_details['catalog_id'],
                'catalog_item': items_details['catalog_item'],
                'ctr_num': items_details['ctr_num'],
                'prod_type': items_details['prod_type'],
                'item_del_date': items_details['item_del_date'],
                'process_type': items_details['process_type'],
                'start_date': items_details['start_date'],
                'end_date': items_details['end_date'],
                'ir_gr_ind_limi': items_details['ir_gr_ind_limi'],
                'gr_ind_limi': items_details['gr_ind_limi'],
                'overall_limit': items_details['overall_limit'],
                'expected_value': items_details['expected_value'],
                'username': items_details['username'],
                'eform_id': items_details['eform_id'],
                'client_id': client
            }
            cart_list.append(defaults)
            if items_details['eform_id']:
                eform_transaction_data = django_query_instance.django_filter_query(EformFieldData,
                                                                                   {'eform_id': items_details[
                                                                                       'eform_id'],
                                                                                    'favourite_cart_guid':
                                                                                        items_details[
                                                                                            'favourite_cart_guid'],
                                                                                    'client': global_variables.GLOBAL_CLIENT},
                                                                                   None, None)
                print(guid)
                filter = django_query_instance.django_filter_query(EformFieldData,
                                                                   {'eform_id': items_details[
                                                                       'eform_id'],
                                                                    'favourite_cart_guid': items_details[
                                                                        'favourite_cart_guid'],
                                                                    'client': global_variables.GLOBAL_CLIENT}, None,
                                                                   None
                                                                   )
                django_query_instance.django_update_query(EformFieldData,
                                                          {'eform_id': items_details[
                                                              'eform_id'],
                                                           'favourite_cart_guid': items_details[
                                                               'favourite_cart_guid'],
                                                           'client': global_variables.GLOBAL_CLIENT},
                                                          {'cart_guid': guid}
                                                          )
        bulk_create_entry_db(CartItemDetails, cart_list)
    global_variables.GLOBAL_CART_COUNTER = display_cart_counter(global_variables.GLOBAL_LOGIN_USERNAME)
    response['cart_count'] = global_variables.GLOBAL_CART_COUNTER
    # msgid = 'MSG112'
    error_msg = get_message_desc(MSG112)[1]
    response['success'] = error_msg
    return JsonResponse(response, safe=False)
