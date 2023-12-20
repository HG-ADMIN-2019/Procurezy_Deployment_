import csv
import datetime
import io
import json
import zipfile
from pathlib import Path
import os

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from Majjaka_eProcure import settings
from Majjaka_eProcure.settings import BASE_DIR
from eProc_Basic.Utilities.constants.constants import CONST_FT_ITEM_EFORM, CONST_QUANTITY_BASED_DISCOUNT, \
    CONST_CATALOG_IMAGE_TYPE
from eProc_Basic.Utilities.functions.dict_check_key import checkKey
from eProc_Basic.Utilities.functions.dictionary_key_to_list import dictionary_key_to_list
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import decrypt, encrypt
from eProc_Basic.Utilities.functions.guid_generator import dynamic_guid_generator, guid_generator
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.functions.query_append_id_desc import AppendIdDesc
from eProc_Basic.Utilities.functions.query_basic_data_append_desc import get_unspsc_append_desc_data, \
    get_supplier_append_desc_data, get_uom_append_desc_data, get_currency_append_desc_data, \
    get_country_append_desc_data, get_language_append_desc_data, catalog_append_desc_data, get_basic_data
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.global_defination.global_variables import GLOBAL_FILENAME_COUNT
from eProc_Basic.Utilities.messages.messages import MSG129, MSG130, MSG048
from eProc_Catalog.Utilities.catalog_specific import save_image_to_db, save_product_images
from eProc_Configuration.models import ProductsDetail, Country, Currency, SupplierMaster, UnitOfMeasures, Languages, \
    Catalogs, ImagesUpload, UnspscCategories, FreeTextDetails, EformFieldConfig
from eProc_Configuration_Check.Utilities.configuration_check_generic import check_unspsc_category_desc_data, \
    check_product_detail_data
from eProc_Form_Builder.Utilities.form_builder_generic import FormBuilder
from eProc_Form_Builder.models import EformFieldData
from eProc_Manage_Content.Utilities.manage_content_generic import get_product_details_image_eform, get_eform_details, \
    get_discount_data
from eProc_Manage_Content.Utilities.manage_content_specific import save_product_details_eform, \
    save_product_specification, save_catalog_to_db, get_assigned_unssigned_product_id_list, save_catalog_mapping, \
    CatalogMappingAction, save_product_detail_images, update_boolean, value_type_caste, save_products_specifications, \
    save_discount_data
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import get_prod_cat, get_supplier_first_second_name
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Upload.Utilities.upload_data.upload_pk_tables import CompareTableHeader

JsonParser_obj = JsonParser()
django_query_instance = DjangoQueries()


def get_product_details(request, product_id):
    """

    """
    update_user_info(request)

    product_details = []
    country_of_origin_id = ''
    unit_id = ''
    new_product_id = ''
    language_id = ''
    supplier_id = ''
    catalog_id = ''
    prod_cat_id = ''
    currency_id = ''
    encrypt_new_product_id = ''
    prod_img_detail = []
    eform_configured = []
    eform_edit_flag = 0
    product_existence_flag = False
    product_specification = []
    if product_id != 'None':
        product_existence_flag = True
        template = 'ManageContentDetail/display_edit_product_detail.html'
        product_id = decrypt(product_id)
        # get product details and image information
        product_details, prod_img_detail, eform_configured, product_specification, eform_edit_flag = get_product_details_image_eform(
            product_id)

        # if product_id exist then update default basic data
        if product_details:
            country_of_origin_id = product_details.country_of_origin_id
            currency_id = product_details.currency_id
            unit_id = product_details.unit_id
            language_id = product_details.language_id
            supplier_id = product_details.supplier_id
            prod_cat_id = product_details.prod_cat_id
    else:
        new_product_id = dynamic_guid_generator(16)
        encrypt_new_product_id = encrypt(new_product_id)
        template = 'ManageContentDetail/display_edit_new_product_detail.html'
    # get basic details
    country_desc, currency_desc, unit_desc, \
    language_desc, supplier_desc, unspsc_desc = get_basic_data(
        country_of_origin_id, currency_id, unit_id, language_id, supplier_id, prod_cat_id,
        global_variables.GLOBAL_USER_LANGUAGE)

    client = global_variables.GLOBAL_CLIENT
    product_category = get_prod_cat()
    supplier_details = get_supplier_first_second_name(client)

    # print(eform_configured)
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'product_details': product_details,
        'country_desc': country_desc,
        'unit_desc': unit_desc,
        'language_desc': language_desc,
        'supplier_desc': supplier_desc,
        'unspsc_desc': unspsc_desc,
        'currency_desc': currency_desc,
        'prod_img_detail': prod_img_detail,
        'eform_configured': eform_configured,
        'eform_edit_flag': eform_edit_flag,
        'product_specification': product_specification,
        'new_product_id': new_product_id,
        'product_existence_flag': product_existence_flag,
        'encrypt_new_product_id': encrypt_new_product_id,
        'product_category': product_category,
        'supplier_details': supplier_details
    }

    return render(request, template, context)


def save_product_details_spec_images_eform(request):
    """

    """
    update_user_info(request)
    product_not_exist = ''
    eform_configured = {}
    product_info_id = None
    discount_id = None
    tiered_pricing = False
    ui_data = request.POST
    attached_file = request.FILES
    converted_dict = dict(ui_data.lists())
    data = json.loads(request.POST['update'])
    eform_configured = json.loads(request.POST['eform_configured'])
    product_existence_flag = json.loads(request.POST['product_existence_flag'])
    product_specification_data = json.loads(request.POST['product_specification_data'])
    create_flag = json.loads(request.POST['create_flag'])
    edit_variant_flag = json.loads(request.POST['edit_variant_flag'])
    form_id = ''
    discount_dic_list = []
    eform_configured_dic_list = []
    if eform_configured:
        for eform in eform_configured:
            if eform['field_type'] == CONST_QUANTITY_BASED_DISCOUNT:
                discount_dic_list.append(eform)
            else:
                eform_configured_dic_list.append(eform)
        form_id = save_product_details_eform(eform_configured_dic_list)
        discount_id = save_discount_data(discount_dic_list)
    if product_specification_data:
        product_info_id = save_product_specification(product_specification_data, data['product_id'])
    save_product_images(attached_file, data['product_id'])
    # save images
    # if checkKey(converted_dict, 'Prod_cat'):
    #     prod_cat = converted_dict['Prod_cat']
    #     file_name = converted_dict['file_name']
    #     default_image = [True if img_flag else False for img_flag in converted_dict['default_image_value']]
    #     save_image_to_db(prod_cat, file_name, attached_file, default_image)
    # if ProductsDetail.objects.filter(product_id=data['product_id']).exists():
    # check for discount

    if django_query_instance.django_existence_check(ProductsDetail, {'client': global_variables.GLOBAL_CLIENT,
                                                                     'product_id': data['product_id']}):
        django_query_instance.django_update_query(ProductsDetail,
                                                  {'client': global_variables.GLOBAL_CLIENT,
                                                   'product_id': data['product_id']},
                                                  {'short_desc': data["short_desc"],
                                                   'long_desc': data['long_desc'],
                                                   'supplier_id': data['supplier_id'],
                                                   'cust_prod_cat_id': data['prod_cat_id'],
                                                   'prod_type': data['product_type'],
                                                   'value_min': data['value_min'],
                                                   'price_on_request': False,
                                                   'unit': UnitOfMeasures.objects.get(
                                                       uom_id=data['unit']),
                                                   'price_unit': data['price_unit'],
                                                   'currency': Currency.objects.get(
                                                       currency_id=data['currency']),
                                                   'price': data['price'],
                                                   'manufacturer': data['manufacturer'],
                                                   'manu_part_num': data['manu_prod'],
                                                   'prod_cat_id': UnspscCategories.objects.get(
                                                       prod_cat_id=data['unspsc']),
                                                   'brand': data['brand'],
                                                   'lead_time': data['lead_time'],
                                                   'quantity_avail': data[
                                                       'quantity_avail'],
                                                   'quantity_min': data['quantity_min'],
                                                   'offer_key': data['offer_key'],
                                                   'country_of_origin': Country.objects.get(
                                                       country_code=data[
                                                           'country_of_origin']),
                                                   'language': Languages.objects.get(
                                                       language_id=data['language']),
                                                   'search_term1': data['search_term1'],
                                                   'search_term2': data['search_term2'],
                                                   'variant_id': form_id,
                                                   'discount_id':discount_id,
                                                   'product_info_id': product_info_id,
                                                   'changed_at': datetime.date.today(),
                                                   'changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                   'supp_product_id': data['supplier_product_number'],
                                                   'external_link': data['product_webpage_link'],
                                                   'ctr_num': data['product_contract_num'],
                                                   'ctr_item_num': data['ctr_item_num'],
                                                   'ctr_name': data['product_contract_name'],
                                                   'manu_code_num': data['prd_manu_code_no'],
                                                   'quantity_max': data['quantity_max'],
                                                   'products_detail_source_system': data['product_source_system']
                                                   })
    else:
        django_query_instance.django_create_query(ProductsDetail,
                                                  {'client': global_variables.GLOBAL_CLIENT,
                                                   'catalog_item': guid_generator(),
                                                   'product_id': data['product_id'],
                                                   'short_desc': data["short_desc"],
                                                   'long_desc': data['long_desc'],
                                                   'value_min': data['value_min'],
                                                   'supplier_id': data['supplier_id'],
                                                   'cust_prod_cat_id': data['prod_cat_id'],
                                                   'prod_type': data['product_type'],
                                                   'price_on_request': False,
                                                   'unit': UnitOfMeasures.objects.get(
                                                       uom_id=data['unit']),
                                                   'price_unit': data['price_unit'],
                                                   'currency': Currency.objects.get(
                                                       currency_id=data['currency']),
                                                   'price': data['price'],
                                                   'manufacturer': data['manufacturer'],
                                                   'manu_part_num': data['manu_prod'],
                                                   'prod_cat_id': UnspscCategories.objects.get(
                                                       prod_cat_id=data['unspsc']),
                                                   'brand': data['brand'],
                                                   'lead_time': data['lead_time'],
                                                   'quantity_avail': data[
                                                       'quantity_avail'],
                                                   'quantity_min': data['quantity_min'],
                                                   'offer_key': data['offer_key'],
                                                   'country_of_origin': Country.objects.get(
                                                       country_code=data[
                                                           'country_of_origin']),
                                                   'language': Languages.objects.get(
                                                       language_id=data['language']),
                                                   'search_term1': data['search_term1'],
                                                   'search_term2': data['search_term2'],
                                                   'variant_id': form_id,
                                                   'discount_id':discount_id,
                                                   'product_info_id': product_info_id,
                                                   'created_at': datetime.date.today(),
                                                   'created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                   'changed_at': datetime.date.today(),
                                                   'changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                   'supp_product_id': data['supplier_product_number'],
                                                   'external_link': data['product_webpage_link'],
                                                   'ctr_num': data['product_contract_num'],
                                                   'ctr_item_num': data['ctr_item_num'],
                                                   'ctr_name': data['product_contract_name'],
                                                   'manu_code_num': data['prd_manu_code_no'],
                                                   'quantity_max': data['quantity_max'],
                                                   'products_detail_source_system': data['product_source_system']

                                                   })
    eform_configured, eform_edit_flag = get_eform_details(form_id)
    discount_data = get_discount_data(discount_id)
    if discount_data:
        eform_configured.append(discount_data)
    return JsonResponse(eform_configured, safe=False)


def save_catalog_db(request):
    """

    :param request:
    :return:
    """
    update_user_info(request)
    catalog_data = JsonParser_obj.get_json_from_req(request)
    catalog_data_response = save_catalog_to_db(catalog_data)
    return JsonResponse(catalog_data_response, safe=False)


def generate_guid(request):
    """

    """
    catalog = {}
    catalog['catalog_id'] = dynamic_guid_generator(4)
    return JsonResponse(catalog, safe=False)


def get_assign_unassign_product(request):
    """

    """
    update_user_info(request)
    assign_unassign_data = JsonParser_obj.get_json_from_req(request)
    catalog_mapping_instance = CatalogMappingAction(assign_unassign_data['catalog_id'])
    product_id_list, freetext_id_list = catalog_mapping_instance.get_assigned_unssigned_product_id_list(
        assign_unassign_data)
    catalog_mapping_product_details = {'product_id_list': product_id_list, 'freetext_id_list': freetext_id_list}
    return JsonResponse(catalog_mapping_product_details, safe=False)


def assign_unassign_product_data(request):
    """

    """
    update_user_info(request)
    catalog_mapping_info = JsonParser_obj.get_json_from_req(request)
    catalog_mapping_instance = CatalogMappingAction(catalog_mapping_info['catalog_id'])
    catalog_mapping_instance.save_catalog_mapping(catalog_mapping_info)
    response = {}
    return JsonResponse(response, safe=False)


def activate_deactivate_catalog(request):
    """

    """
    catalog_active_flag_detail = JsonParser_obj.get_json_from_req(request)
    django_query_instance.django_update_query(Catalogs,
                                              {'client': global_variables.GLOBAL_CLIENT,
                                               'catalog_id': catalog_active_flag_detail['catalog_id'],
                                               'del_ind': False},
                                              {'is_active_flag': catalog_active_flag_detail['flag']})
    response = {}
    return JsonResponse(response, safe=False)


def save_data_upload(request):
    """

    """
    update_user_info(request)
    data = JsonParser_obj.get_json_from_req(request)

    for val in data['product_list']:
        path = val['image_path']
        del val['image_path']
        val = value_type_caste(val)
        val = update_boolean(val)
        val['client'] = global_variables.GLOBAL_CLIENT
        val['unit'] = django_query_instance.django_get_query(UnitOfMeasures, {'uom_id': val['unit']})
        val['country_of_origin'] = django_query_instance.django_get_query(Country,
                                                                          {'country_code': val['country_of_origin']})
        val['currency'] = django_query_instance.django_get_query(Currency, {'currency_id': val['currency']})
        val['language'] = django_query_instance.django_get_query(Languages, {'language_id': val['language']})
        val['prod_cat_id'] = django_query_instance.django_get_query(UnspscCategories,
                                                                    {'prod_cat_id': val['prod_cat_id']})
        if django_query_instance.django_existence_check(ProductsDetail, {'client': global_variables.GLOBAL_CLIENT,
                                                                         'product_id': val['product_id']}):
            # print(val['product_id'])

            django_query_instance.django_update_query(ProductsDetail,
                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                       'product_id': val['product_id']},
                                                      val)
            response = 0
        else:
            val['catalog_item'] = guid_generator()
            # save_product_detail_images(path, val['product_id'])
            django_query_instance.django_create_query(ProductsDetail,
                                                      val)
            response = 1

        product_info_id = save_products_specifications(data['product_spec'])
        if django_query_instance.django_existence_check(ProductsDetail, {'client': global_variables.GLOBAL_CLIENT,
                                                                         'product_id': val['product_id']}):
            # print(val['product_id'])

            django_query_instance.django_update_query(ProductsDetail,
                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                       'product_id': val['product_id']},
                                                      {'product_info_id':product_info_id})
        # Save Images from image path
        if path:
            if os.path.exists(path):
                save_product_detail_images(path, val['product_id'])
    return JsonResponse(response, safe=False)


# def get_image_details1(request):
#     """
#
#     """
#     client = global_variables.GLOBAL_CLIENT
#     count = global_variables.GLOBAL_FILENAME_COUNT + 1
#     image_details = list(
#         ImagesUpload.objects.filter(client=client, del_ind=False).values(
#             'image_id', 'image_number',
#             'image_url', 'image_name', 'image_default', 'image_type', 'images_upload_source_system',
#             'images_upload_destination_system', 'client'))
#     imgtype = []
#     img_client = []
#     imgId = []
#     imgName = []
#     # imgarray = []
#     imgarray2 = []
#
#     print(image_details)
#     for data in image_details:
#         imgtype.append(data['image_type'])
#         img_client.append(data['client'])
#         imgId.append(data['image_id'])
#         imgName.append(data['image_name'])
#
#         imgarray = []
#         imgarray.append(data['image_type'])
#         imgarray.append(data['client'])
#         imgarray.append(data['image_id'])
#
#         imgPath = '/'.join(imgarray)
#         print(imgPath)
#         dir_check = "C:/Users/deepi/Downloads" + imgPath
#
#         if os.path.isdir(dir_check):
#             new_folder = imgarray[0] + '(' + str(count + 1) + ')'
#             imgarray2.append(new_folder)
#             imgarray2.append(img_client[0])
#             imgarray2.append(imgId[0])
#             imgPath2 = '/'.join(imgarray2)
#             final_path = "C:/Users/Lenovo/Downloads/" + imgPath2
#             global_variables.GLOBAL_FILENAME_COUNT = modify_count(count)
#         else:
#             final_path = "C:/Users/Lenovo/Downloads/" + imgPath
#
#         os.makedirs(final_path, mode=0o666)
#         filename = data['image_name']
#         path = r'media/' + imgPath + '/' + filename
#         # img = cv2.imread(path)
#         os.chdir(final_path)
#         # cv2.imwrite(filename, img)
#         os.chdir(final_path)
#         imgPath = ''
#
#     res = 1
#
#     context = {
#         'image_details': image_details,
#         'res': res,
#     }
#
#     return JsonResponse(context, safe=False)


def get_image_details(request):
    update_user_info(request)
    destination = os.path.join(Path.home(), 'Downloads','image.zip')
    source = os.path.join(str(settings.BASE_DIR), 'media', 'catalog', str(global_variables.GLOBAL_CLIENT))
    # shutil.make_archive('zip_file', 'zip', source, destination)
    make_archive(source, destination)
    return JsonResponse({}, safe=False)


def make_archive(source, destination, format='zip'):
    import os
    import shutil
    from shutil import make_archive
    base, name = os.path.split(destination)
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(source.strip(os.sep))
    print(f'Source: {source}\nDestination: {destination}\nArchive From: {archive_from}\nArchive To: {archive_to}\n')
    shutil.make_archive(name, format, archive_from, archive_to)
    shutil.move('%s.%s' % (name, format), destination)


# def get_image_details2(request):
#     # Files (local path) to put in the .zip
#     # FIXME: Change this (get paths from DB etc)
#     # filenames = django_query_instance.django_filter_value_list_query(ImagesUpload,
#     #                                                                  {'client':global_variables.GLOBAL_CLIENT,
#     #                                                                   'del_ind':False,
#     #                                                                   'image_type':CONST_CATALOG_IMAGE_TYPE},
#     #                                                                 'image_url' )
#     # for index,filename in enumerate(filenames):
#     #     filename[index] = os.path.join(str(settings.BASE_DIR), filename)
#     filenames = ['/media/catalog/700/5A22E8CAE8B444DC/desk1.jpg']
#
#     # Folder name in ZIP archive which contains the above files
#     # E.g [thearchive.zip]/somefiles/file2.txt
#     # FIXME: Set this to something better
#     zip_subdir = " C:/Users/deepi/Downloads/image"
#     zip_filename = "%s.zip" % zip_subdir
#
#     # Open StringIO to grab in-memory ZIP contents
#     s = io.BytesIO()
#
#     # The zip compressor
#     zf = zipfile.ZipFile(s, "w")
#
#     for fpath in filenames:
#         # Calculate path for file in zip
#         fdir, fname = os.path.split(fpath)
#         zip_path = os.path.join(zip_subdir, fname)
#         fpath = 'D:/Majjaka/majjaka_shop_22_04_2022/Majjaka-Shop/media/catalog/700/5A22E8CAE8B444DC/desk1.jpg'
#         # Add file, at correct path
#         zf.write(fpath, zip_path)
#
#     # Must close zip for all contents to be written
#     zf.close()
#
#     # Grab ZIP file from in-memory, make response with correct MIME-type
#     resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
#     # ..and correct content-disposition
#     resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
#
#     return resp


def modify_count(count):
    global_variables.GLOBAL_FILENAME_COUNT = count + 1
    print("count = ", global_variables.GLOBAL_FILENAME_COUNT)
    return global_variables.GLOBAL_FILENAME_COUNT


@login_required
@transaction.atomic
def delete_freetext_form(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    freetext_id_list = JsonParser_obj.get_json_from_req(request)
    freetext_info = FormBuilder().delete_freetext(freetext_id_list['data'])
    msgid = 'MSG130'
    error_msg = get_message_desc(msgid)[1]

    response = {'freetext_info': freetext_info,
                'success_message': error_msg}
    return JsonResponse(response, safe=False)


def delete_product(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    product_id_list = JsonParser_obj.get_json_from_req(request)
    product_info = FormBuilder().delete_product_item(product_id_list['data'])
    msgid = 'MSG130'
    error_msg = get_message_desc(msgid)[1]

    response = {'product_info': product_info,
                'success_message': error_msg}
    return JsonResponse(response, safe=False)


def upload_product_data(request):
    """

    """
    product_detail_data = []
    product_specification_data = []
    db_header = request.POST.get('db_header_data')
    csv_file = request.FILES['file_attach']
    data_set_val = csv_file.read().decode('ISO-8859-1')
    fin_data_upload_header = io.StringIO(data_set_val)
    next(fin_data_upload_header)
    next(fin_data_upload_header)

    for header in csv.reader(fin_data_upload_header, delimiter=',', quotechar='"'):
        if header[0] == 'ProductsDetail':
            del header[0]
            product_detail_data.append(header)
        elif header[0] == 'ProductSpecification':
            del header[0]
            product_specification_data.append(header)
    data = {'products_detail': product_detail_data,
            'product_specification': product_specification_data}

    return JsonResponse(data, safe=False)


def check_product_detail(request):
    """

    """
    update_user_info(request)
    ui_data_dictionary = JsonParser_obj.get_json_from_req(request)
    ui_data = ui_data_dictionary['data_list']
    messages = check_product_detail_data(ui_data,'UPLOAD')
    return JsonResponse({'messages': messages}, safe=False)
