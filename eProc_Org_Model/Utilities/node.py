import random

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404

from eProc_Basic.Utilities.constants.constants import CONST_RNODE, CONST_NODE, CONST_PGROUP, CONST_COMPANY_CODE, \
    CONST_PORG, CONST_NODE_TYPES_LIST
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.messages.messages import MSG135, MSG136, MSG137, MSG138, MSG139, MSG140, MSG141, MSG142, \
    MSG143, MSG144, MSG145, MSG146, MSG147, MSG148
from eProc_Configuration.models.development_data import OrgNodeTypes
from eProc_Org_Model.models import OrgModel

from eProc_Org_Model.Utilities.client import OrgClient
from eProc_Org_Model.Utilities.orgUtils import OrgUtils
from eProc_Org_Model.Utilities.validators import Validators


class Node(OrgUtils, Validators):
    """
    Handles Organization Model
    """

    def __init__(self, client_id, pk):
        """
        Initialize a node
        :param client_id: client for which node belongs
        :param pk: primary key of node
        """
        super(Node, self).__init__(OrgModel, client_id, pk)

    # Function which handles create, update and delete operations related to Node/sub-nodes
    def update_node(self, **kwargs):
        if 'del_ind' in kwargs:
            # first check action is delete/update
            self.base.del_ind = kwargs.get('del_ind')
            if self.base.del_ind:
                if not self.delete_possible():
                    self.base.del_ind = False
            self.base.name = self.get_node_name(kwargs.get('name', self.base.name))
            return
        else:
            # Action is create
            for k, v in kwargs.items():
                if k == 'name':
                    self.set_base_props(k, self.get_node_name(v))
                elif k == 'node_type':
                    self.set_base_props(k, self.get_node_type(v))
                elif k == 'parent_node_guid':
                    self.set_base_props(k, self.get_parent_node(v))
                elif k == 'object_id':
                    self.set_base_props(k, self.get_node_map_id(v))
                elif k == 'node_guid':
                    self.set_base_props(k, self.get_node_guid(v))
                elif k == 'root_node_object_id':
                    if v:
                        self.set_base_props(k, v)
                    else:
                        self.set_base_props(k, self.base.object_id)


    def delete_possible(self):
        """
        Checks for existence of children for the node
        :return: True/False
        """
        nodes = OrgModel.objects.filter(parent_node_guid=self.base.node_guid, del_ind=False)
        if nodes.count() != 0:
            msgid = 'MSG135'
            error_msg = get_msg_desc(msgid)
            msg = error_msg['message_desc'][0]
            error_msg = msg
            self.set_error(error_msg)
            return False
        return True

    def get_node_name(self, name):
        """
        Node name validation
        :param name: Name of the node
        :return: Node name
        """
        if self.name_valid(name):
            return name
        msgid = 'MSG136'
        error_msg = get_msg_desc(msgid)
        msg = error_msg['message_desc'][0]
        error_msg = msg
        self.set_error(error_msg)
        return None

    def get_node_type(self, pk):
        """
        Get the node-type of a node
        :param pk: primary key of a node
        :return: Response object
        """
        if (pk is None) or (pk == ""):
            # Find ROOTNODE type
            node_type_value = get_object_or_404(OrgNodeTypes, client=self.base.client, node_type=CONST_RNODE,
                                                del_ind=False)
            return node_type_value.node_type
        not_root_node = get_object_or_404(OrgNodeTypes, ~Q(node_type=CONST_RNODE), client=self.base.client,
                                          node_type=pk, del_ind=False)
        return not_root_node.node_type

    # Checks the node-type position where should it exist
    def check_node_type(self):

        # Don't allow root node below the nodes
        if self.base.node_type == CONST_RNODE:
            if self.base.parent_node is not None:
                msgid = 'MSG137'
                error_msg = get_msg_desc(msgid)
                msg = error_msg['message_desc'][0]
                error_msg = msg
                self.set_error(error_msg)
            return
        tree_types = Node.read_tree_up(self.base)

        # Don't allow any nodes under P_GROUP except NODE
        if self.base.node_type != CONST_NODE:
            if CONST_PGROUP in tree_types:
                msgid = 'MSG138'
                error_msg = get_message_desc(msgid)[1]

                self.set_error(error_msg)

        # Allow P_GROUP only under P_ORG
        if self.base.node_type == CONST_PGROUP:
            if CONST_PORG not in tree_types:
                msgid = 'MSG139'
                error_msg = get_message_desc(msgid)[1]

                self.set_error(error_msg)

        # Don't allow any nodes under P_ORG except NODE and P_GROUP
        if self.base.node_type != CONST_NODE:
            if self.base.node_type != CONST_PGROUP:
                if self.base.node_type != CONST_COMPANY_CODE:
                    if CONST_PORG in tree_types:
                        msgid = 'MSG140'
                        error_msg = get_message_desc(msgid)[1]

                        self.set_error(error_msg)

        # Don't allow CC under CC
        if self.base.node_type == CONST_COMPANY_CODE:
            if CONST_COMPANY_CODE in tree_types:
                msgid = 'MSG141'
                error_msg = get_message_desc(msgid)

                self.set_error(error_msg)

        # Don't allow P_ORG under P_ORG
        if self.base.node_type == CONST_PORG:
            if CONST_PORG in tree_types:
                msgid = 'MSG142'
                error_msg = get_message_desc(msgid)[1]

                self.set_error(error_msg)

    # To get the parent node of the current node
    def get_parent_node(self, guid):
        try:
            if guid is not None:
                parent_node_guid = OrgModel.objects.filter(client=self.base.client, node_guid=guid, del_ind=False)
                if parent_node_guid.count() != 0:
                    return guid
                msgid = 'MSG143'
                error_msg = get_message_desc(msgid)[1]

                self.set_error(error_msg)
                self.set_error(error_msg)
        except ValidationError:
            msgid = 'MSG144'
            error_msg = get_message_desc(msgid)[1]

            self.set_error(error_msg)
        return None

    def get_node_guid(self, guid_value):
        guid_value = guid_generator()
        return guid_value

    # To get the map-id for the node
    def get_node_map_id(self, object_id):
        if object_id is None:
            while True:
                # Generate random string of alphanumeric format 'ROOT_XXX' where XXX is calculated dynamically
                tmp_str = self.randN(8)
                # Check if map_id already exists in the particular client
                if not self.check_map_id_exist(tmp_str):
                    return tmp_str
        if self.alpha_num(object_id):
            if not self.check_map_id_exist(object_id):
                if len(object_id) <= 8:
                    return object_id
                else:
                    msgid = 'MSG145'
                    error_msg = get_message_desc(msgid)[1]

                    self.set_error(error_msg)
            else:
                msgid = 'MSG146'
                error_msg = get_message_desc(msgid)[1]

                self.set_error(error_msg)
        else:
            msgid = 'MSG147'
            error_msg = get_message_desc(msgid)[1]

            self.set_error(error_msg)
        return None

    # To check whether map-id already exist for that client or not
    def check_map_id_exist(self, name):
        tmp_node = OrgModel.objects.filter(client=self.base.client, object_id=name, del_ind=False)
        if tmp_node.count() == 0:
            return False
        return True

    def randN(self, N):
        min = pow(10, N - 1)
        max = pow(10, N) - 1
        return random.randint(min, max)

    # To set node name
    def set_node_name(self):
        if self.base.node_type == CONST_RNODE:
            self.base.name = self.base.name.upper()
        else:
            self.base.name = self.base.name.capitalize()

    def save_node(self):
        """
        Saves the node
        """
        if not (
                self.base.client is None or
                self.base.node_guid is None or
                self.base.name is None or
                self.base.node_type is None or
                self.base.object_id is None
        ):
            self.set_node_name()
            if self.base.node_type == CONST_RNODE:
                if self.base.parent_node_guid is not None:
                    msgid = 'MSG148'
                    error_msg = get_message_desc(msgid)[1]

                    self.set_error(error_msg)
            else:
                if self.base.parent_node_guid is not None:
                    if self.alpha_num(self.base.object_id):
                        self.check_node_type()
                    else:
                        msgid = 'MSG147'
                        error_msg = get_message_desc(msgid)[1]

                        self.set_error(error_msg)
                else:
                    msgid = 'MSG143'
                    error_msg = get_msg_desc(msgid)[1]

                    self.set_error(error_msg)
            if not self.error:
                self.base.save()
                return True
        return False

    @staticmethod
    def read_tree_up(cur_node):
        tree_struct = []
        while cur_node.parent_node_guid is not None:
            cur_node = OrgModel.objects.get(node_guid=cur_node.parent_node_guid)
            tree_struct.append(cur_node)
        tree_types = []
        for item in tree_struct:
            tree_types.append(item.node_type)
        return tree_types

    # To get node types of a client
    @staticmethod
    def get_node_types(client_id):
        return OrgNodeTypes.objects.filter(client=client_id, node_type__in=CONST_NODE_TYPES_LIST, del_ind=False)

    @staticmethod
    def get_node(client_id, guid):
        try:
            client = OrgClient.get_client(client_id)
            node = get_object_or_404(OrgModel, client=client, node_guid=guid, del_ind=False)
            return node
        except:
            return '{"error": "No node found"}'

    @staticmethod
    def get_children(client_id, guid):
        try:
            client = OrgClient.get_client(client_id)
            node = OrgModel.objects.filter(client=client, parent_node_guid=guid, del_ind=False)
            if node.exists():
                return node
            else:
                return ['{"error": "No children found"}']
        except:
            return ['{"error": "no valid input"}']
