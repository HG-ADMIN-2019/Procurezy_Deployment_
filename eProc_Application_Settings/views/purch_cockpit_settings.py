import json
from django.http import JsonResponse

from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Configuration.models import purch_cockpit, UnitOfMeasures, Currency, Languages, Country, UnspscCategories, \
    OrgClients, ProductsDetail
from eProc_Basic.Utilities.functions.dict_check_key import checkKey

from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Catalog.Utilities.catalog_specific import save_image_to_db
from eProc_Shopping_Cart.context_processors import update_user_info

JsonParser_obj = JsonParser()


def purch_cockpit_display(request):
    """

    :param request:
    :return:
    """
    purch_info = request.POST.get('purch_cockpit')
    if purch_info == 'purch_cockpit':
        purch_data_response = purch_cockpit.objects.filter(del_ind=False)
        return JsonParser_obj.get_json_from_obj(purch_data_response)


def save_purch_cockpit_data(request):
    """

    :param request:
    :return:
    """

    purch_cockpit_data = JsonParser_obj.get_json_from_req(request)

    purchcockpit_not_exist: object = purch_cockpit.objects.filter(del_ind=False).exclude(
        from_prod_cat__in=[purch['from_prod_cat'] for purch in purch_cockpit_data])

    for set_del_int in purchcockpit_not_exist:
        set_del_int.del_ind = True
        set_del_int.save()

    for data in purch_cockpit_data:

        if not (
        purch_cockpit.objects.filter(from_prod_cat=data['from_prod_cat'], to_prod_cat=data['to_prod_cat']).exists()):
            obj, created = purch_cockpit.objects.update_or_create(
                client=OrgClients.objects.get(client=getClients(request)),
                guid=guid_generator(),
                from_prod_cat=data['from_prod_cat'],
                to_prod_cat=data['to_prod_cat'])
    purch_data_response = purch_cockpit.objects.filter(del_ind=False)
    return JsonParser_obj.get_json_from_obj(purch_data_response)


def save_product_details_images(request):
    """

    :param request:
    :return:
    """
    update_user_info(request)
    product_not_exist = ''
    ui_data = request.POST
    attached_file = request.FILES
    converted_dict = dict(ui_data.lists())
    product_data = json.loads(request.POST['update'])
    # save images
    if checkKey(converted_dict, 'Prod_cat'):
        prod_cat = converted_dict['Prod_cat']
        file_name = converted_dict['file_name']
        default_image = [True if img_flag else False for img_flag in converted_dict['default_image_value']]
        save_image_to_db(prod_cat, file_name, attached_file, default_image)

    product_not_exist: object = ProductsDetail.objects.filter(del_ind=False).exclude(
        product_id__in=[product['product_id'] for product in product_data])
    for set_del_int in product_not_exist:
        set_del_int.del_ind = True
        set_del_int.save()
    for data in product_data:
        if not (ProductsDetail.objects.filter(product_id=data['product_id']).exists()):
            obj, created = ProductsDetail.objects.create(
                client=OrgClients.objects.get(client=global_variables.GLOBAL_CLIENT),
                catalog_item=guid_generator(),
                product_id=int(data['product_id']),
                short_desc=data['short_desc'],
                long_desc=data['long_desc'],
                supplier_id=data['supplier_id'],
                prod_cat_id=data['prod_cat_id'],
                catalog_id=data['catalog_id'],
                product_type=data['product_type'],
                price_on_request=False,
                unit=UnitOfMeasures.objects.get(uom_id=data['unit']),
                price_unit=data['price_unit'],
                currency=Currency.objects.get(currency_id=data['currency']),
                price=data['price'],
                manufacturer=data['manufacturer'],
                manu_part_num=data['manu_prod'],
                unspsc=UnspscCategories.objects.get(prod_cat_id=data['unspsc']),
                brand=data['brand'],
                lead_time=data['lead_time'],
                quantity_avail=data['quantity_avail'],
                quantity_min=data['quantity_min'],
                offer_key=data['offer_key'],
                country_of_origin=Country.objects.get(country_code=data['country_of_origin']),
                language=Languages.objects.get(language_id=data['language']),
                search_term1=data['search_term1'],
                search_term2=data['search_term2'])

        else:
            ProductsDetail.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                          product_id=int(data['product_id'])).update(short_desc=data['short_desc'],
                                                                                     long_desc=data['long_desc'],
                                                                                     supplier_id=data['supplier_id'],
                                                                                     prod_cat_id=data['prod_cat_id'],
                                                                                     catalog_id=data['catalog_id'],
                                                                                     product_type=data['product_type'],
                                                                                     price_on_request=False,
                                                                                     unit=UnitOfMeasures.objects.get(
                                                                                         uom_id=data['unit']),
                                                                                     price_unit=data['price_unit'],
                                                                                     currency=Currency.objects.get(
                                                                                         currency_id=data['currency']),
                                                                                     price=data['price'],
                                                                                     manufacturer=data['manufacturer'],
                                                                                     manu_part_num=data['manu_prod'],
                                                                                     unspsc=UnspscCategories.objects.get(
                                                                                         prod_cat_id=data['unspsc']),
                                                                                     brand=data['brand'],
                                                                                     lead_time=data['lead_time'],
                                                                                     quantity_avail=data[
                                                                                         'quantity_avail'],
                                                                                     quantity_min=data['quantity_min'],
                                                                                     offer_key=data['offer_key'],
                                                                                     country_of_origin=Country.objects.get(
                                                                                         country_code=data[
                                                                                             'country_of_origin']),
                                                                                     language=Languages.objects.get(
                                                                                         language_id=data['language']),
                                                                                     search_term1=data['search_term1'],
                                                                                     search_term2=data['search_term2'])
    catalog_data_response = ProductsDetail.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False)
    return JsonParser_obj.get_json_from_obj(catalog_data_response)
