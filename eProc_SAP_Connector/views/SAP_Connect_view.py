from django.http import JsonResponse
from django.shortcuts import render
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Configuration.models import SapConnector
from eProc_SAP_Connector.Utilites.SAP_Connect_Specific import save_connection

django_query_instance = DjangoQueries()


def get_sap_connect(request):
    res = django_query_instance.django_filter_only_query(SapConnector, {'client': getClients(request)}).values()
    context = {
        'inc_nav': True,
        'inc_footer': True,
        # 'sap_connector': res
    }
    return render(request, 'SAP_Connect.html', context)


def create_connection(request):
    """
    saving the catalog which is newly created
    :param request: POST
    :return: Success or failure response
    """
    res = save_connection(request)
    json_obj = JsonParser()
    return json_obj.get_json_from_obj(res)


def get_connection(request):
    res = django_query_instance.django_filter_only_query(SapConnector, {'client': getClients(request)})
    json_obj = JsonParser()
    return json_obj.get_json_from_obj(res)


def delete_connections(request):
    """
    :param request: POST
    :return: result
    """
    get_item = request.POST.get('delete_item')
    django_query_instance.django_get_query(SapConnector, {
        'client': getClients(request), 'pk': get_item, 'del_ind': False
    }).delete()
    res = django_query_instance.django_filter_only_query(SapConnector, {})
    json_obj = JsonParser()
    return json_obj.get_json_from_obj(res)


def Connections(request):
    connections = django_query_instance.django_filter_value_list_query(SapConnector, {'client': getClients(request)},
                                                                       'sys_id')
    return JsonResponse(connections, safe=False)
