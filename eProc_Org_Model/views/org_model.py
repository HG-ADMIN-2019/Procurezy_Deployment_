from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from eProc_Basic.Utilities.constants.constants import CONST_RNODE
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.messages.messages import MSG134
from eProc_Org_Model.Utilities.org_specific import get_org_model_detail, update_node_details
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Org_Model.Utilities.org_tree_specific import get_org_model_attr_detail
from eProc_Org_Model.models import OrgModel, OrgNames


@login_required
def org_model_ui(request):
    filter_dictionary = {}
    root_node_name = ''
    org_model_detail = []

    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    if not OrgModel.objects.filter(object_id=global_variables.GLOBAL_LOGIN_USER_OBJ_ID, client=client).exists():
        global_variables.GLOBAL_ORG_TREE_STRUCTURE_FLAG = False
    if global_variables.GLOBAL_ORG_TREE_STRUCTURE_FLAG:
        org_model_detail, object_id_list, root_node_name = get_org_model_detail(global_variables.GLOBAL_LOGIN_USER_OBJ_ID)
    context = {
        'org_model_detail': org_model_detail,
        'root_node_name': root_node_name,
        'org_tree_flag': global_variables.GLOBAL_ORG_TREE_STRUCTURE_FLAG
    }
    return render(request, 'org_model.html', context)


from django.http import HttpResponse, JsonResponse
from django.views import View

from eProc_Org_Model.Utilities.apiHandler import ApiHandler
from eProc_Shopping_Cart.context_processors import update_user_info


class HandleOrg(View, JsonParser):
    """
    Handle Organization related API calls
    """

    def post(self, req, action):
        """
        Handles POST request
        :param req: Http request object
        :param action: Action to be performed on org
        :return: Http response
        """
        # Get JSON data from request's body
        data = self.get_json_from_req(req)
        if action == "create":
            # Create new organization
            res = ApiHandler.create_org(data, req)
            return self.get_json_from_obj(res)
        elif action == "getall":
            res = ApiHandler.get_all_org(data, req)
            return self.get_json_from_obj(res)
        return HttpResponse("Invalid request")


class HandleNode(View, JsonParser):
    """
    Handle Node related API calls
    """

    def post(self, req, action):
        """
        Handles POST request
        :param req: Http request object
        :param action: Action to be performed on node
        :return: Http response
        """
        # Get JSON data from request's body
        data = self.get_json_from_req(req)
        if action == "create":
            # Create new node
            res,error_msg = ApiHandler.create_node(data, req)
            if error_msg:
                return JsonResponse(error_msg, safe=False)
            return self.get_json_from_obj(res)
        elif action == "edit":
            res = ApiHandler.edit_node(data)
            return self.get_json_from_obj(res)
        elif action == "delete":
            res = ApiHandler.delete_node(data, req)
            return self.get_json_from_obj(res)
        elif action == "get":
            res = ApiHandler.get_node(data, req)
            return self.get_json_from_obj(res)
        elif action == "getchilds":
            res = ApiHandler.get_children(data, req)
            return self.get_json_from_obj(res)
        msgid = 'MSG134'
        error_msg = get_msg_desc(msgid)
        msg = error_msg['message_desc'][0]
        error_msg = msg
        return HttpResponse(error_msg)


class HandleUsers(View, JsonParser):
    """
    Handle user related API calls
    """

    def post(self, req, action):
        """
        Handles POST request
        :param req: Http request object
        :param action: Action to be performed on users
        :return: Http response
        """
        update_user_info(req)
        data = self.get_json_from_req(req)
        if action == 'assign':
            resp = ApiHandler.assign_users(data, req)
            return self.get_json_from_obj(resp)
        elif action == "get_users":
            resp = ApiHandler.get_users(data, req)
            return self.get_json_from_obj(resp)
        elif action == "assign_users":
            resp = ApiHandler.assign_group_of_users(data, req)
            return self.get_json_from_obj(resp)
        elif action == 'assigned_unassigned_users':
            resp = ApiHandler.get_assign_unassigned_user(data)
            return self.get_json_from_obj(resp)
        elif action == 'save_assign_unassign_user':
            resp = ApiHandler.save_assign_unassigned_user(data)
            return self.get_json_from_obj(resp)
        msgid = 'MSG131'
        error_msg = get_message_desc(msgid)[1]


        return HttpResponse(error_msg)


class HandleNodeTypes(View, JsonParser):
    """
    Handle node-types related API calls
    """

    def post(self, req):
        """
        Handles POST request
        :param req: Http request object
        :return: Http response
        """
        data = self.get_json_from_req(req)
        res = ApiHandler.get_node_types(data, req)
        return self.get_json_from_obj(res)


class HandleDetails(View, JsonParser):
    """
    Handle details tab related API calls
    """

    def post(self, req, action):
        """
        Handles POST request
        :param req: Http request object
        :param action: Action to be performed on details
        :return: Http response
        """
        data = self.get_json_from_req(req)
        if action == "get":
            res = ApiHandler.get_node_details(data, req)
            return self.get_json_from_obj(res)
        elif action == "edit":
            res = ApiHandler.modify_node_details(data, req)
            return self.get_json_from_obj(res)
        elif action == "save":
            res = ApiHandler.save_node_details(data, req)
            return self.get_json_from_obj(res)
        msgid = 'MSG134'
        error_msg = get_msg_desc(msgid)
        msg = error_msg['message_desc'][0]
        error_msg = msg
        return HttpResponse(error_msg)


class HandleBasicData(View, JsonParser):
    """
    Handle basic data tab related API calls
    """

    def post(self, req, action):
        """
        Handles POST request
        :param req: Http request object
        :param action: Action to be performed on basic data tab
        :return: Http response
        """
        data = self.get_json_from_req(req)
        if action == "get":
            res = ApiHandler.get_node_basic_data(data, req)
            return self.get_json_from_obj(res)
        elif action == "edit":
            res = ApiHandler.edit_node_basic_data(data, req)
            return self.get_json_from_obj(res)
        msgid = 'MSG134'
        error_msg = get_msg_desc(msgid)
        msg = error_msg['message_desc'][0]
        error_msg = msg
        return HttpResponse(error_msg)


def get_all_organisations(request):
    response = ApiHandler.get_all_org(None, request)
    return JsonParser().get_json_from_obj(response)


def get_children(request):
    if request.method == 'POST':
        data = JsonParser().get_json_from_req(request)
        res = ApiHandler.get_children(data, request)
        return JsonParser().get_json_from_obj(res)
    msgid = 'MSG131'
    error_msg = get_message_desc(msgid)[1]

    return HttpResponse(error_msg)


def get_node_types(request):
    res = ApiHandler.get_node_types(None, request)
    return JsonParser().get_json_from_obj(res)


def org_node_detail(request):
    """

    """
    update_user_info(request)
    json_obj = JsonParser()
    json_data = json_obj.get_json_from_req(request)
    org_model_attr_detail = get_org_model_attr_detail(json_data['object_id'])

    return JsonResponse(org_model_attr_detail, safe=False)


def save_basic_details_ajax_call(request):
    update_user_info(request)
    json_obj = JsonParser()
    json_data = json_obj.get_json_from_req(request)
    print(json_data)
    org_model_obj = ''
    if not DjangoQueries().django_existence_check(OrgModel,
                                                  {'client': global_variables.GLOBAL_CLIENT,
                                                   'object_id': json_data['object_id'],
                                                   'name': json_data['node_name']}):
        org_model_obj = DjangoQueries().django_update_or_create_query(OrgModel,
                                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                                       'object_id': json_data['object_id']},
                                                                      {'name': json_data['node_name']})
    if json_data['node_type'] == CONST_RNODE:
        if DjangoQueries.django_existence_check(OrgNames, {'client': global_variables.GLOBAL_CLIENT,
                                                            'object_id': json_data['object_id']}):
            DjangoQueries.django_update_or_create_query(OrgNames,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'object_id': json_data['object_id']},
                                                        {'name': json_data['node_name']})
    # update company,porg,pgrp in its respective table based on node type
    update_node_details(json_data)
    org_model_obj = DjangoQueries.django_filter_value_list_query(OrgModel,
                                                                 {'client': global_variables.GLOBAL_CLIENT,
                                                                  'object_id': json_data['object_id']},
                                                                 'name'
                                                                 )
    org_node_details = {'org_model_name': org_model_obj}

    return JsonResponse(org_node_details, safe=False)


def org_model_information(request):
    """

    """
    root_node_object_id = 0
    update_user_info(request)
    json_obj = JsonParser()
    json_data = json_obj.get_json_from_req(request)
    org_model_detail, object_id_list, root_node_name = get_org_model_detail(json_data['object_id'])
    if object_id_list:
        root_node_object_id = object_id_list[0]
    dictionary_list = {
        'org_model_detail':org_model_detail,
        'object_id_list':object_id_list,
        'root_node_name':root_node_name,
        'root_node_object_id':root_node_object_id
    }
    return JsonResponse(dictionary_list, safe=False)
