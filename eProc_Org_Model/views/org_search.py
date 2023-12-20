from django.http import JsonResponse

# Create your views here.
from eProc_Basic.Utilities.constants.constants import CONST_COMPANY_CODE, CONST_PORG, CONST_PGROUP, CONST_USER
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Org_Model.Utilities.org_specific import OrgNodesSearch
from eProc_Org_Model.models import OrgModel
from eProc_Shopping_Cart.context_processors import update_user_info


def org_nodes_filter_fun(request):
    """
    Organization node search feature based on the node type
    :param request: POST
    :return: Searched nodes
    """

    """Reading Data"""
    update_user_info(request)
    json_obj = JsonParser()
    input = json_obj.get_json_from_req(request)
    node_type = input['node_type']
    search_id = input['search_id']

    org_specific_obg = OrgNodesSearch()
    if node_type == CONST_COMPANY_CODE:
        result = org_specific_obg.company_search(search_id)
    elif node_type == CONST_PORG:
        result = org_specific_obg.purchase_org_search(search_id)
    elif node_type == CONST_PGROUP:
        result = org_specific_obg.purchase_grp_search(search_id)
    elif node_type == CONST_USER:
        result = org_specific_obg.org_user_search(search_id)

    if len(result) > 0:
        data = OrgModel.objects.filter(client=global_variables.GLOBAL_CLIENT, object_id__in=result).distinct()
    else:
        data = ['{"error": "No matching data found"}']

    return json_obj.get_json_from_obj(data)


def get_node_tree_strcture(request):
    """
    Get the tree structure that is immediate parents chain until root node
    :param request: POST
    :return: tree structure that is immediate parents chain until root node
    """
    json_obj = JsonParser()
    input = json_obj.get_json_from_req(request)
    node_id = input['node_id']
    org_specific_obj = OrgNodesSearch()
    org_specific_obj.dict_nodes = {}
    org_specific_obj.counter = 0
    org_specific_obj.get_node(node_id)
    return JsonResponse(org_specific_obj.dict_nodes)
