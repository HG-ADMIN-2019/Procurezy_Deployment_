import json
import random

from django.shortcuts import get_object_or_404

from eProc_Attributes.models.org_attribute_models import OrgAttributesLevel
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Configuration.models.development_data import OrgNodeTypes, OrgAttributes
from eProc_Org_Model.Utilities.orgUsers import OrgUser
from eProc_Basic.Utilities.constants.constants import CONST_RNODE, CONST_NODE, CONST_COMPANY_CODE, CONST_PORG, \
    CONST_PGROUP, CONST_USER, CONST_ASSIGN, CONST_UNASSIGN
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import OrgClients, OrgCompanies, OrgPorg, OrgPGroup
from eProc_Org_Model.models import *

from eProc_Org_Model.Utilities.client import OrgClient
from eProc_Org_Model.Utilities.node import Node

from eProc_Org_Model.Utilities.organization import Organization
from eProc_Org_Model.models.org_model import OrgModel

from eProc_Registration.models import UserData
from eProc_Shopping_Cart.context_processors import update_user_info

django_query_instance = DjangoQueries()


class ApiHandler:
    """
    Contains methods for handling all APIs
    """

    @staticmethod
    def create_org(data, request):
        """
        Creates new organization for client
        :param data: Organization data (should contain client and org_name)
        :return: Response object/message
        """

        # Get client and org_name from data
        client = getClients(request)
        org_name = data['org_name']
        return ApiHandler.create_organization(client, org_name)

    @staticmethod
    def create_organization(client, org_name):
        try:
            org_obj = Organization(client, None)
            org_obj.update_org(name=org_name)
            if not org_obj.error:
                root_node = Node(client, None)
                root_node.update_node(name=org_name, node_type=None, parent_node_guid=None, object_id=None,
                                      node_guid=None, root_node_object_id=None)
                if root_node.save_node():
                    org_obj.update_org(root_node=root_node.base.node_guid, object_id=root_node.base.object_id)
                    if org_obj.save_org():
                        return [org_obj.base]
                    return [org_obj.message]
                return [root_node.message]
            return [org_obj.message]
        except KeyError:
            # Raised when client or org_name not found
            return ['{"error": "No valid inputs found"}']

    # @staticmethod
    # def edit_org(data):
    #     """
    #     Edit existing organization
    #     :param data: Organization data
    #     :return: Response data
    #     """
    #     try:
    #         client = data['client']
    #         org_name = data['org_name']
    #         pk = data['pk']
    #         org_obj = Organization(client, pk)
    #         org_obj.update_org(name=org_name)
    #         if not org_obj.error:
    #             if org_obj.save_org():
    #                 return [org_obj.base]
    #             return [org_obj.message]
    #         return [org_obj.message]
    #     except KeyError:
    #         return [{'error': 'No valid inputs found'}]

    # To get all organizations
    @staticmethod
    def get_all_org(data, request):
        """
        Get all the organizations
        :param data: Organization data(should contain client)
        :return: Response object/message
        """
        try:
            client = getClients(request)
            return Organization.get_all_org(client)
        except KeyError:
            return ['{"error": "No valid inputs found"}']

    @staticmethod
    def create_node(data, request):
        """
        Create new node
        :param data: Node data
        :return: Response object/message
        """

        client = getClients(request)
        name = data['name']
        node_type = data['node_type']
        parent_node = data['parent_node']
        root_node_object_id = data['root_node_object_id']
        return ApiHandler.save_node(client, name, node_type, parent_node, root_node_object_id)

    @staticmethod
    def save_node(client, name, node_type, parent_node, root_node_object_id):
        error_msg = None
        try:
            org_name_count = django_query_instance.django_filter_count_query(OrgModel,
                                                                             {'client':client,
                                                                              'name':name,
                                                                              'del_ind':False})
            # if OrgModel.objects.filter(client=client, name=name, del_ind = None).exists():
            if org_name_count > 0:
                error_msg = {'error':"Node already exists"}
                return None,error_msg
            else:
                new_node = Node(client, None)
                new_node.update_node(name=name,
                                     node_type=node_type,
                                     parent_node_guid=parent_node,
                                     object_id=None,
                                     node_guid=None,
                                     root_node_object_id=root_node_object_id)
                res = new_node.save_node()
                if res:
                    return [new_node.base],error_msg
                else:
                    return [new_node.message],error_msg
        except KeyError:
            return None,['{"error": "No valid inputs found"}']

    @staticmethod
    def edit_node_basic_data(data, request):
        """
        Edit node
        :param data: Node data
        :return: Response object/message
        """
        try:
            client = getClients(request)
            pk = data['pk']
            new_name = data['name']
            node = Node(client, pk)
            node.update_node(name=new_name, del_ind=False)
            if not node.error:
                # Update org name if root node changed
                if node.base.node_type == CONST_RNODE:
                    # Get org by root node and update both org and root node
                    org = Organization.get_org_by_rootnode(client, node.base.node_guid)

                    edit_org = Organization(client, None)
                    edit_org.base = org
                    edit_org.update_org(name=node.base.name)
                    if edit_org.error:
                        return [edit_org.message]
                    if node.save_node() and edit_org.save_org():
                        return [node.base]
                    return ['{"error": "Something went wrong"}']
                else:
                    if node.save_node():
                        return [node.base]
            return [node.message]
        except KeyError:
            return ['{"error": "No valid inputs found"}']

    @staticmethod
    def delete_node(data, request):
        """
        Node deletion
        :param data: Node data
        :return: Response message
        """
        try:
            client = getClients(request)
            pk = data['pk']
            node = Node(client, pk)
            if node.delete_possible():
                # Delete org if root node is deleted
                if node.base.node_type == CONST_RNODE:
                    OrgNames.objects.filter(client=client, object_id=pk).delete()
                OrgAttributesLevel.objects.filter(client=client, object_id=pk).delete()
                OrgCompanies.objects.filter(client=client, object_id=pk).update(object_id=None)
                OrgPorg.objects.filter(client=client, object_id=pk).update(object_id=None)
                OrgPGroup.objects.filter(client=client, object_id=pk).update(object_id=None)
                OrgModel.objects.filter(client=client, object_id=pk).delete()
                org_name = ApiHandler.get_all_org(client, request)
                return org_name
            else:
                return ['{"error": "Delete children first"}']
        except KeyError:
            return ['{"error": "No valid inputs found"}']

    @staticmethod
    def get_node_types(data, request):
        """
        Get different node types available in client (except ROOTNODE)
        :param data: Client data
        :return: Response object
        """
        try:
            update_user_info(request)
            client = global_variables.GLOBAL_CLIENT
            n_types = Node.get_node_types(client)
            if not n_types.count() == 0:
                return n_types
            else:
                return ['{"info": "Node types not found"}']
        except KeyError:
            return ['{"error""": "No client found"}']

    @staticmethod
    def assign_users(data, request):
        """
        User creation
        :param data: User data
        :return: Response object/message
        """
        try:
            client = getClients(request)
            object_id = data['object_id']
            username = data['username']
            first_name = data['first_name']
            last_name = data['last_name']
            new_user = OrgUser(client, None)
            new_user.update_user(object_id=object_id, username=username, first_name=first_name, last_name=last_name)
            res = new_user.save_user()
            if res:
                return [new_user.base]
            else:
                return [new_user.message]
        except KeyError:
            return ['{"error": "No valid inputs found"}']

    @staticmethod
    def get_node(data, request):
        try:
            client = getClients(request)
            guid = data['guid']
            return [Node.get_node(client, guid)]
        except KeyError:
            return ['{"error": "Invalid inputs found"}']

    @staticmethod
    def get_children(data, request):
        try:
            client = getClients(request)
            guid = data['guid']
            return Node.get_children(client, guid)
        except KeyError:
            return ['{"error": "Invalid inputs found"}']

    @staticmethod
    def get_node_details(data, request):
        org_companies_list = {}
        array_list = []
        try:
            client = getClients(request)
            pk = data['pk']
            n_type = data['node_type']
            clnt = OrgClient.get_client(client)
            obj = None
            sel = {'client': clnt, 'del_ind': False}
            if n_type != "":
                # Get the node
                node = Node.get_node(client, pk)
                node_type = node.node_type
                if node_type == CONST_RNODE or node_type == CONST_NODE:
                    return []
                elif node_type == CONST_COMPANY_CODE:
                    obj = OrgCompanies
                    if obj.objects.filter(object_id=node.object_id).exists():
                        sel['object_id'] = node.object_id
                    else:
                        sel['object_id__isnull'] = True
                    node_det = obj.objects.filter(**sel)
                    return node_det
                elif node_type == CONST_PORG:
                    obj = OrgPorg
                    if obj.objects.filter(object_id=node.object_id).exists():
                        sel['object_id'] = node.object_id
                    else:
                        sel['object_id__isnull'] = True
                    node_det = obj.objects.filter(**sel)
                    return node_det
                elif node_type == CONST_PGROUP:
                    obj = OrgPGroup
                    if obj.objects.filter(object_id=node.object_id).exists():
                        sel['object_id'] = node.object_id
                    else:
                        sel['object_id__isnull'] = True
                    node_det = obj.objects.filter(**sel)
                    return node_det
                elif node_type == CONST_USER:
                    obj = UserData
                    sel['object_id'] = node.object_id
                    node_det = obj.objects.filter(**sel)
                    return node_det
                node_det = get_object_or_404(obj, **sel)
                return [node_det]
            else:
                # Get the user
                sel['pk'] = pk
                user = get_object_or_404(UserData, **sel)
                return [user]
        except KeyError:
            return ['{"error": "Invalid inputs found"}']

    @staticmethod
    def modify_node_details(data, request):
        try:
            client = getClients(request)
            pk = data['pk']
            n_type = data['node_type']
            node_detail_flag = data['node_detail_flag']

            clnt = OrgClient.get_client(client)
            obj = None
            sel = {'client': clnt, 'del_ind': False}
            inp = {'client': clnt}
            if n_type != "":
                # Get the node
                node = Node.get_node(client, pk)
                node_type = node.node_type
                if node_type == CONST_RNODE or node_type == CONST_NODE:
                    return []
                elif node_type == CONST_COMPANY_CODE:
                    obj = OrgCompanies
                    node_id = data['company_id']
                    if node_detail_flag:
                        sel['object_id'] = node.object_id
                        inp['name1'] = data['name1']
                        inp['name2'] = data['name2']
                    else:
                        sel['company_id'] = node_id
                        inp['object_id'] = OrgModel.objects.get(object_id=node.object_id)
                        inp['name1'] = data['name1']
                        inp['name2'] = data['name2']
                elif node_type == CONST_PORG:
                    obj = OrgPorg
                    node_id = data['porg_id']
                    if node_detail_flag:
                        sel['object_id'] = node.object_id
                        inp['description'] = data['description']
                    else:
                        sel['porg_id'] = node_id
                        inp['object_id'] = OrgModel.objects.get(object_id=node.object_id)
                        inp['description'] = data['description']
                elif node_type == CONST_PGROUP:
                    obj = OrgPGroup
                    node_id = data['pgroup_id']
                    if node_detail_flag:
                        sel['object_id'] = node.object_id
                        inp['description'] = data['description']
                    else:
                        sel['pgroup_id'] = node_id
                        inp['object_id'] = OrgModel.objects.get(object_id=node.object_id)
                        inp['porg_id'] = get_porg_id(node.object_id)
                        inp['description'] = data['description']
                try:
                    node_det = obj.objects.filter(**sel).update(**inp)
                    return [node_det]
                except obj.DoesNotExist:
                    node_det = obj()
                    node_det.objects.modify(**inp)
                    node_det.save()
                    return [node_det]
            else:
                # Get the user
                sel['pk'] = pk
                user = get_object_or_404(UserData, **sel)
                inp['name1'] = data['name1']
                inp['name2'] = data['name2']
                user.objects.modify(**inp)
                return [user]
                pass
        except KeyError:
            return ['{"error": "Invalid inputs found"}']

    @staticmethod
    def save_node_details(data, request):
        try:
            client = getClients(request)
            pk = data['pk']
            n_type = data['node_type']
            obj = None
            if n_type != "":
                # Get the node
                node = Node.get_node(client, pk)
                node_type = node.node_type
                if node_type == CONST_RNODE or node_type == CONST_NODE:
                    return []
                elif node_type == CONST_COMPANY_CODE:
                    obj = OrgCompanies()
                    obj.object_id = OrgModel.objects.get(object_id=node.object_id, del_ind=False)
                    obj.name1 = data['name1']
                    obj.name2 = data['name2']
                    obj.company_guid = guid_generator()
                    if OrgCompanies.objects.filter(company_id=data['company_id'], client=client,
                                                   del_ind=False).exists():
                        return ['{"error":"Company id already exists"}']
                    obj.company_id = data['company_id']
                elif node_type == CONST_PORG:
                    obj = OrgPorg()
                    parent_node = OrgModel.objects.get(node_guid=node.parent_node_guid)
                    if OrgCompanies.objects.filter(object_id=parent_node.object_id, del_ind=False).exists():
                        company_check = OrgCompanies.objects.get(object_id=parent_node.object_id)
                        obj.company_id = company_check.company_id
                        obj.porg_guid = guid_generator()
                        obj.object_id = OrgModel.objects.get(object_id=node.object_id)
                        if OrgPorg.objects.filter(porg_id=data['porg_id'], client=client, del_ind=False).exists():
                            return ['{"error":"Porg id already exists"}']
                        obj.porg_id = data['porg_id']
                        obj.description = data['description']
                    else:
                        return ['{"error":"Please enter the parent - company details"}']
                elif node_type == CONST_PGROUP:
                    obj = OrgPGroup()
                    parent_porg = OrgModel.objects.get(node_guid=node.parent_node_guid)
                    if OrgPorg.objects.filter(object_id=parent_porg.object_id, del_ind=False).exists():
                        porg_check = OrgPorg.objects.get(object_id=parent_porg.object_id)
                        obj.porg_id = porg_check.porg_id
                        obj.pgroup_guid = guid_generator()
                        obj.object_id = OrgModel.objects.get(object_id=node.object_id)
                        if OrgPGroup.objects.filter(pgroup_id=data['pgroup_id'], client=client, del_ind=False).exists():
                            return ['{"error":"Pgroup id already exists"}']
                        obj.pgroup_id = data['pgroup_id']
                        obj.description = data['description']
                    else:
                        return ['{"error":"Please enter the parent - Purchase organization details"}']
                try:
                    obj.client = OrgClients.objects.get(client=client)
                    obj.del_ind = False
                    obj.save()
                    return ['{"message": "Details saved successfully "}']
                except obj.DoesNotExist:
                    return ['{"error" : " incorrect data passed"}']
            else:
                # Get the user
                return ['{"error" : "Node type not handeled"}']
                pass
        except KeyError:
            return ['{"error": "Invalid inputs found"}']

    @staticmethod
    def get_node_basic_data(data, request):
        """
        Handles basic data tab details
        :param data: Node data
        :return: Response object/message
        """
        try:
            client = getClients(request)
            pk = data['node_guid']
            node_type = data['node_type']
            clnt = OrgClient.get_client(client)
            temp = {'client': clnt, 'del_ind': False}
            if node_type == CONST_RNODE:
                root_guid = OrgNodeTypes.objects.get(client=client, node_type=node_type)
                node_type = root_guid.node_type_guid
            if node_type != "" and node_type is not None:
                node = Node.get_node(client, pk)
                obj = OrgModel
                temp['object_id'] = node.object_id
                node_detail = get_object_or_404(obj, **temp)
                return [node_detail]
            else:
                temp['pk'] = pk
                user = get_object_or_404(UserData, **temp)
                return [user]
        except KeyError:
            return ['{"error": "Invalid inputs found"}']

    # @staticmethod
    # def get_users(data, request):
    #     """
    #     Get users based on the parent node
    #     :param data:  consists of the node object id under which the users will be assigned
    #     :param req: Post
    #     :return: List of users without object id and the users assigned with object id
    #     """
    #     try:
    #         # client = '700'
    #         client = getClients(request)
    #         object_id = data['object_id']
    #         get_node = OrgModel.objects.get(client = client,del_ind =False,object_id =object_id)
    #         get_user_nodes = OrgModel.objects.filter(client=client,del_ind=False,parent_node_guid=get_node.node_guid,node_type =CONST_USER)
    #         print(get_user_nodes)
    #         if get_node.node_type == CONST_NODE:
    #             org_users_object_ids = []
    #             for record in get_user_nodes:
    #                 org_users_object_ids.append(record.object_id)
    #
    #             result = UserData.objects.filter(
    #                 Q(client=client, del_ind=False, object_id=None) | Q(client=client, del_ind=False,
    #                                                                     object_id__in = org_users_object_ids))
    #             return result
    #         else:
    #              return ['{"error": "Cannot add user under this node"}']
    #     except KeyError:
    #         return ['{"error": "No valid inputs found"}']

    @staticmethod
    def object_id_generator(N):
        min = pow(10, N - 1)
        max = pow(10, N) - 1
        return random.randint(min, max)

    @staticmethod
    def assign_group_of_users(data, req):

        # client = '700'
        client = getClients(req)
        get_data = json.loads(data)
        parent_node_object_id = get_data[0]['parent_object_id']
        parent_node = OrgModel.objects.get(client=client, object_id=parent_node_object_id, del_ind=False)
        for user in get_data:
            existing_check = OrgModel.objects.filter(client=client, del_ind=False, name=user['user_name']).exists()
            if existing_check == False and user['assign'] == True:
                # Object id generates
                user_object_id = ApiHandler.object_id_generator(8)

                # Saving Data in to OrgModel tabel
                org_user = OrgModel()
                org_user.client = OrgClients.objects.get(client=client)
                org_user.node_type = CONST_USER
                org_user.node_guid = guid_generator()
                org_user.object_id = user_object_id
                org_user.del_ind = False
                org_user.name = user['user_name']
                org_user.parent_node_guid = parent_node.node_guid
                org_user.save()

                # updating user with object_id in user master data table
                get_employee_name = user['user_name']
                update_user = UserData.objects.get(client=client, username=get_employee_name)
                update_user.object_id = OrgModel.objects.get(object_id=user_object_id)
                update_user.save()

            if user['assign'] == False and existing_check == True:

                # unassigning user in user master data
                get_employee_name = user['user_name']
                update_user_pk = UserData.objects.get(client=client, username=get_employee_name)
                get_user_reference = update_user_pk.object_id_id
                print(get_user_reference)
                update_user = UserData.objects.filter(client=client, username=get_employee_name)
                update_user.update(object_id=None)

                if get_user_reference != None:
                    # delete the entry in org model
                    OrgAttributes.objects.get(client=client, object_id=get_user_reference, del_ind=False).delete()
                    OrgModel.objects.get(client=client, object_id=get_user_reference, del_ind=False).delete()

        result = OrgModel.objects.filter(client=client, del_ind=False, parent_node_guid=parent_node.node_guid)

        return result

    @staticmethod
    def get_assign_unassigned_user(data):
        """

        :param req:
        :return:
        """
        client = global_variables.GLOBAL_CLIENT
        parent_node_guid = data['node_guid']
        node_action = data['node_action']
        if node_action == CONST_UNASSIGN:
            get_user_obj_id = list(
                OrgModel.objects.filter(client=client, del_ind=False, parent_node_guid=parent_node_guid,
                                        node_type=CONST_USER).values_list('object_id', flat=True))
            get_user_details = UserData.objects.filter(client=client, object_id__in=get_user_obj_id)
        else:
            get_user_details = UserData.objects.filter(client=client, object_id=None)
        return get_user_details

    @staticmethod
    def save_assign_unassigned_user(data):
        """

        :param data:
        :return:
        """
        parent_node_guid = data['node_guid']
        node_action = data['node_action']
        user_id_list = data['user_id_list']
        root_node_object_id = data['root_node_object_id']
        client = global_variables.GLOBAL_CLIENT
        result = ApiHandler.save_assign_unassign_data(client, user_id_list, node_action, parent_node_guid,
                                                      root_node_object_id)

        result = django_query_instance.django_filter_only_query(OrgModel,
                                                                {'client': client,
                                                                 'del_ind': False,
                                                                 'parent_node_guid': parent_node_guid})
        return result

    @staticmethod
    def save_assign_unassign_data(client, user_id_list, node_action, parent_node_guid, root_node_object_id):
        result = ''
        for user in user_id_list:
            if node_action == CONST_ASSIGN:
                user_object_id = ApiHandler.object_id_generator(8)
                org_model_instance = OrgModel.objects.get_or_create(object_id=user_object_id,
                                                                    node_guid=guid_generator(),
                                                                    name=user,
                                                                    parent_node_guid=parent_node_guid,
                                                                    node_type=CONST_USER,
                                                                    root_node_object_id=root_node_object_id,
                                                                    del_ind=False,
                                                                    client=OrgClients.objects.get(client=client))
                UserData.objects.filter(client=client,
                                        username=user).update(
                    object_id=OrgModel.objects.get(object_id=org_model_instance[0].object_id))
                result = django_query_instance.django_filter_query(OrgModel,
                                                                   {'client': client,
                                                                    'del_ind': False,
                                                                    'parent_node_guid': parent_node_guid},
                                                                   None,
                                                                   None)
            else:

                user_detail = UserData.objects.get(client=client,
                                                   username=user)
                OrgAttributesLevel.objects.filter(object_id=user_detail.object_id_id).delete()
                UserData.objects.filter(client=client,
                                        username=user).update(object_id=None)
                OrgModel.objects.filter(parent_node_guid=parent_node_guid,
                                        node_type=CONST_USER,
                                        name=user,
                                        del_ind=False,
                                        client=client).delete()
                result = django_query_instance.django_filter_query(OrgModel,
                                                                   {'client': client,
                                                                    'del_ind': False,
                                                                    'parent_node_guid': parent_node_guid},
                                                                   None,
                                                                   None)
        return result


def get_porg_id(pgrp_object_id):
    """

    :param pgrp_object_id:
    :return:
    """
    pgrp_parent_guid = OrgModel.objects.filter(object_id=pgrp_object_id).values_list('parent_node_guid', flat=True)[0]
    porg_object_id = OrgModel.objects.filter(node_guid=pgrp_parent_guid).values_list('object_id', flat=True)[0]
    porg_id = OrgPorg.objects.filter(object_id=porg_object_id).values_list('porg_id', flat=True)[0]
    return porg_id
