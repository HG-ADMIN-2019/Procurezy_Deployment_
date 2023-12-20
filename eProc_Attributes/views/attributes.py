"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    attributes.py
Usage:
    on click of Attributes in nav bar dropdown
    attributes - This function handle getting attribute level data and render attributes.html
Author:
    Deepika K
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from Majjaka_eProcure import settings
from eProc_Attributes.Utilities.attributes_specific import get_attr_value_list, get_dropdown_value, get_parents_obj_id, \
    get_dropdown_attr_id_list, append_dropdown_attr_id_list, save_attr_id_data_into_db, get_comp_code_drop_down, \
    get_attr_values_company_Code_list, delete_org_attributes_based_on_object_id, get_org_attribute_id_list
from eProc_Attributes.models.org_attribute_models import OrgAttributesLevel
from eProc_Basic.Utilities.constants.constants import CONST_US_ROLE
from eProc_Basic.Utilities.functions.dict_check_key import checkKey
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.global_defination import global_variables
from django.http import JsonResponse

# from itertools import chain - required
from eProc_Org_Model.models import OrgModel
from eProc_Shopping_Cart.context_processors import update_user_info

JsonParser_obj = JsonParser()


@login_required
def org_attributes(request):
    """
    get object id, attributed value to UI
    :param request: UI data into views
    :return: render attributes.html
    """
    attr_value_list = []
    client = getClients(request)
    attr_detail = {}
    update_user_info(request)

    if request.POST:
        data = JsonParser_obj.get_json_from_req(request)
        # get requested object id from UI
        attr_object_id = data['obj_id']
        #  get attribute level values for specified object id
        attr_detail = get_attr_values_company_Code_list(client, attr_object_id)

    return JsonResponse(attr_detail,safe=False)


def delete_popup(request, pk):
    """

    :param request:
    :param pk:
    :return:
    """
    update_user_info(request)
    attr_id_list = []
    if DjangoQueries.django_existence_check(OrgAttributesLevel,{'id':pk}):
        obj = DjangoQueries.django_get_query(OrgAttributesLevel,{'id':pk})
        client = global_variables.GLOBAL_CLIENT
        object_id_list = get_parents_obj_id(client, obj.object_id)
        attr_id_list = OrgAttributesLevel.objects.filter(attribute_id=obj.attribute_id, object_id__in=object_id_list)
    context = {
        'inc_nav': True,
        'inc_shop_nav': True,
        'attr_id_list': attr_id_list
    }
    return render(request, 'Attributes/delete_popup.html', context)


def dropdown_list(request):
    """
    on click od add attribute send respective drop down value to UI
    :param request:
    :return: json response of dropdown value list
    """
    update_user_info(request)
    data       = {}
    attr_value = ''

    if request.is_ajax():
        attr_value = request.POST.get('value')
    client = global_variables.GLOBAL_CLIENT
    dropdown_value = get_dropdown_value(client, attr_value)
    data['attr_id'] = attr_value
    data['attr_value'] = dropdown_value

    return JsonResponse(data)


def update_popup(request):

    """
    on click of  delete button, get all attribute list based in attribute id
    :param request:
    :return:
    """
    attr_value_list = {}
    attribute_id = request.POST.get('value')
    obj_id_user = request.POST.get('obj_id')
    client = getClients(request)

    drop_down, attr_id_list = get_dropdown_attr_id_list(client, attribute_id, obj_id_user)
    dropdown_attr_list = append_dropdown_attr_id_list(drop_down, attr_id_list)
    attr_value_list['attr_values'] = drop_down
    attr_value_list['attr_value_list'] = attr_id_list
    return JsonResponse(attr_value_list, safe=False)


def save_table(request):
    """
    Save newly added attributes into attributelevel table
    :param request:
    :return: send saved response to UI via Json
    """
    response = {}
    data = ''
    update_user_info(request)
    attr_id_data = JsonParser_obj.get_json_from_req(request)
    attr_object_id = attr_id_data['object_id']
    save_data = attr_id_data['attr_details']

    attr_object_id = save_attr_id_data_into_db(save_data,attr_object_id,global_variables.GLOBAL_CLIENT)
    attr_value_list = get_attr_values_company_Code_list(global_variables.GLOBAL_CLIENT, attr_object_id)

    return JsonResponse(attr_value_list,safe=False)


def save_deleted_attr(request):
    """

    :param request:
    :return: send json response of attr list
    """
    update_user_info(request)
    save_details = JsonParser_obj.get_json_from_req(request)
    save_data = save_details['attr_details']
    attr_object_id = save_details['object_id']
    attribute_id = save_data[0]['attribute_id']

    # delete node in OrgAttributesLevel db table
    delete_org_attributes_based_on_object_id(attribute_id,attr_object_id)

    #  check save data attribute list
    key_exit = checkKey(save_data, 'value')

    # attribute list exist then save attribute list into db(attribute level table)
    if key_exit:
        attr_object_id = save_attr_id_data_into_db( save_data,attr_object_id,global_variables.GLOBAL_CLIENT)

    elif save_data[0]['attribute_id'] == CONST_US_ROLE:
        global_variables.GLOBAL_SUB_MENU = {}
        global_variables.GLOBAL_SLIDE_MENU = {}

    #  get attr value list of selected node and its parent
    attr_value_list = get_attr_values_company_Code_list(global_variables.GLOBAL_CLIENT, attr_object_id)
    drop_down = get_dropdown_value(global_variables.GLOBAL_CLIENT, save_data[0]['attribute_id'])
    attr_value_list['attr_values'] = drop_down
    dropdown_attr_list = append_dropdown_attr_id_list(drop_down, attr_value_list)
    return JsonResponse(attr_value_list,safe=False)


def attr_id_list(request):
    update_user_info(request)
    select_node_detail = JsonParser_obj.get_json_from_req(request)
    # get org attribute id list based on node type
    attr_id = get_org_attribute_id_list(select_node_detail)

    return JsonResponse(attr_id,safe=False)
