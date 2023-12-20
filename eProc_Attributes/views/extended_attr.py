from datetime import datetime

from django.http.response import JsonResponse

from eProc_Attributes.Utilities.attributes_specific import get_attr_value_list, get_extended_att_list, \
    save_extended_responsibility
from eProc_Basic.Utilities.constants.constants import CONST_PROD_CAT
from eProc_Basic.Utilities.functions.dict_check_key import checkKey
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries, bulk_create_entry_db
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models.master_data import OrgPorgMapping
from eProc_Org_Model.models.org_model import OrgModel
from eProc_Shopping_Cart.context_processors import update_user_info

JsonParser_obj = JsonParser()
django_query_instance = DjangoQueries()


def extended_attr(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    # get requested object id from UI
    object_id = request.POST.get('obj_id')
    attr_value_list = get_extended_att_list(client, object_id, CONST_PROD_CAT)
    return JsonParser_obj.get_json_from_obj(attr_value_list)


def save_ext_attr(request):
    """

    :param request:
    :return:
    """
    update_user_info(request)
    save_ext_data = JsonParser_obj.get_json_from_req(request)
    client = global_variables.GLOBAL_CLIENT
    attr_object_id = save_ext_data[0]['obj_id']
    # save extend attributes to OrgAttributesLevel db table
    save_extended_responsibility(save_ext_data)
    attr_value_list = get_attr_value_list(client, attr_object_id)
    # return JsonParser_obj.get_json_from_obj(attr_value_list)
    return JsonResponse(attr_value_list, safe=False)


def save_porg_company_id(request):
    """

    """
    update_user_info(request)
    porg_data = JsonParser_obj.get_json_from_req(request)
    porg_mapping_list = []
    object_id = None
    save_porg_data = porg_data['save_porg_mapping_attributes']

    django_query_instance.django_filter_delete_query(OrgPorgMapping,
                                                     {'client': global_variables.GLOBAL_CLIENT,
                                                      'object_id': porg_data['object_id']})
    if save_porg_data:
        object_id = django_query_instance.django_get_query(OrgModel,
                                                           {'client': global_variables.GLOBAL_CLIENT,
                                                            'object_id': porg_data['object_id']})
    for save_porg in save_porg_data:
        org_porg_mapping_guid = guid_generator()
        porg_mapping_list.append({'org_porg_mapping_guid': org_porg_mapping_guid,
                                  'porg_id': save_porg['porg_id'],
                                  'company_id': save_porg['company_id'],
                                  'org_porg_mapping_changed_at': datetime.today(),
                                  'org_porg_mapping_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                  'org_porg_mapping_created_at': datetime.today(),
                                  'org_porg_mapping_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                  'object_id': object_id,
                                  'client_id':global_variables.GLOBAL_CLIENT
                                  })
    bulk_create_entry_db(OrgPorgMapping,
                         porg_mapping_list)
    context = {'message': 'Data Saved Successfully'}
    return JsonResponse(context, safe=False)
