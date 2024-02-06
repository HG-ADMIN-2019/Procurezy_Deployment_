from django.shortcuts import get_object_or_404

from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.messages.messages import MSG150, MSG151
from eProc_Org_Model.models import OrgNames, OrgModel

from eProc_Org_Model.Utilities.client import OrgClient
from eProc_Org_Model.Utilities.orgUtils import OrgUtils
from eProc_Org_Model.Utilities.validators import Validators


class Organization(OrgUtils, Validators):
    """
    Handles Organization
    """

    def __init__(self, client_id, pk):
        """
        Initialize a organization
        :param client_id: client for which organization belongs
        :param pk: primary key of org
        """
        super(Organization, self).__init__(OrgNames, client_id, pk)

    # Function which handles create, update and delete operations related to org name
    def update_org(self, **kwargs):
        # start deepika changes
        # if self.base.pk is not None:
        #     # Action is update / delete
        #     if 'del_ind' in kwargs:
        #         self.base.del_ind = kwargs.get('del_ind')
        #     else:
        #         self.base.name = self.get_org_name(kwargs.get('name', self.base.name))
        #     return
        # else:
        # end deepika
        # Action is create
        for k, v in kwargs.items():
            if k == 'name':
                self.set_base_props(k, self.get_org_name(v))
            elif k == 'root_node':
                self.set_base_props(k, v)
            elif k == 'object_id':
                object_id = OrgModel.objects.get(object_id=v)
                self.set_base_props(k, object_id)
            if 'del_ind' in kwargs:
                self.base.del_ind = kwargs.get('del_ind')

    # To get a Org name
    def get_org_name(self, name):
        # Check if org_name already exist
        tmp_list = OrgNames.objects.filter(client=self.base.client, name=name)
        if tmp_list.count() == 0:
            # Check for org_name validity
            if not self.name_valid(name):
                msgid = 'MSG150'
                error_msg = get_message_desc(msgid)[1]

                self.set_error(error_msg)
                return None
            return name.upper()
        msgid = 'MSG151'
        error_msg = get_message_desc(msgid)[1]

        self.set_error(error_msg)
        return None

    # To get a org by root-node
    @staticmethod
    def get_org_by_rootnode(client_id, guid):
        client = OrgClient.get_client(client_id)
        return get_object_or_404(OrgNames, client=client, root_node=guid, del_ind=False)

    # To get all org
    @staticmethod
    def get_all_org(client_id):
        """
        Get all the organization for client
        :param client_id: client which org belongs to
        :return: Queryset containing org list
        """
        client = OrgClient.get_client(client_id)
        orgs = OrgNames.objects.filter(client=client, del_ind=False)
        if orgs.count() == 0:
            return orgs
        return orgs

    # To save the org
    def save_org(self):
        """
        Save the organization
        """
        if not (self.base.name is None or self.base.root_node is None or self.error):
            self.base.save()
            return True
        return False
