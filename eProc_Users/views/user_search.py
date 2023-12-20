from django.http import JsonResponse
from django.shortcuts import render
from pymysql import NULL

from eProc_Attributes.models.org_attribute_models import OrgAttributesLevel
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import encrypt
from eProc_Basic.Utilities.functions.get_db_query import get_country_id
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import FieldTypeDesc
from eProc_Org_Model.models import OrgModel
from eProc_Registration.models import UserData
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Users.Utilities.user_generic import user_detail_search

django_query_instance = DjangoQueries()
JsonParser_obj = JsonParser()


def delete_user(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    user_data = JsonParser_obj.get_json_from_req(request)
    if django_query_instance.django_existence_check(UserData,
                                                        {'email': user_data['data'],
                                                         'del_ind': False}):
        if django_query_instance.django_existence_check(OrgAttributesLevel,
                                                        {'object_id': user_data['object_id_id'] and user_data[
                                                            'object_id_id'] is not NULL,
                                                         'del_ind': False}):
            django_query_instance.django_filter_delete_query(OrgAttributesLevel, {'object_id': user_data['object_id_id'],
                                                                                  'client': global_variables.GLOBAL_CLIENT})
        if django_query_instance.django_existence_check(OrgModel,
                                                        {'object_id': user_data['object_id_id'] and user_data[
                                                            'object_id_id'] is not NULL,
                                                         'del_ind': False}):
            django_query_instance.django_filter_delete_query(OrgModel, {'object_id': user_data['object_id_id'],
                                                                        'client': global_variables.GLOBAL_CLIENT})
        django_query_instance.django_filter_delete_query(UserData, {'email': user_data['email'],
                                                                    'client': global_variables.GLOBAL_CLIENT})

    employee_results = django_query_instance.django_filter_only_query(UserData, {
            'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
        })
    response = {'employee_results': employee_results,'success_message': "User deleted"}
    return JsonResponse(response, safe=False)
