from django.shortcuts import get_object_or_404

from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.messages.messages import MSG152, MSG153, MSG154
from eProc_Org_Model.models import OrgModel
from eProc_Org_Model.Utilities.orgUtils import OrgUtils
from eProc_Org_Model.Utilities.validators import Validators
from eProc_Registration.models import UserData


class OrgUser(OrgUtils, Validators):
    """
    Handles Users
    """
    def __init__(self, client_id, pk):
        """
        Initialize a user
        :param client_id: client for which node belongs
        :param pk: primary key of user
        """
        super(OrgUser, self).__init__(UserData, client_id, pk)

    # Function which handles create, update and delete operations related to users
    def update_user(self, **kwargs):
        if self.base.pk is not None:
            # Action is update / delete
            if 'del_ind' in kwargs:
                self.base.del_ind = kwargs.get('del_ind')
            else:
                self.base.username = self.get_user_id(kwargs.get('username', self.base.username))
                self.base.first_name = self.get_name(kwargs.get('first_name', self.base.first_name))
                self.base.last_name = self.get_name(kwargs.get('last_name', self.base.last_name))
            return
        else:
            # Action is create
            for k, v in kwargs.items():
                if k == 'username':
                    self.set_base_props(k, self.get_user_id(v))
                elif k == 'first_name':
                    self.set_base_props(k, self.get_name(v))
                elif k == 'last_name':
                    self.set_base_props(k, self.get_name(v))
                elif k == 'object_id':
                    self.set_base_props(k, self.get_map_id(v))

    # To get the user-id and to validate the user-id
    def get_user_id(self, val):
        if self.alpha_num(val):
            tmp_usrs = UserData.objects.filter(client=self.base.client, username=val, del_ind=False)
            if tmp_usrs.count() == 0:
                return val
            msgid = 'MSG152'
            error_msg = get_message_desc(msgid)[1]

            self.set_error(error_msg)
        else:
            msgid = 'MSG153'
            error_msg = get_message_desc(msgid)[1]

            self.set_error(error_msg)
        return None

    # To get the user name and to validate the user name
    def get_name(self, val):
        if self.alphabets(val):
            return val
        return None

    # To get the map-id for users from the node
    def get_map_id(self, val):
        node = get_object_or_404(OrgModel, client=self.base.client, object_id=val, del_ind=False)
        if node.node_type== 'NODE':
            return val
        msgid = 'MSG154'
        error_msg = get_message_desc(msgid)

        self.set_error(error_msg)
        return None

    # To save the users to user table
    def save_user(self):
        """
        Saves the users
        """
        if not (
                self.base.client is None or
                self.base.username is None or
                self.base.first_name is None or
                self.base.last_name is None or
                self.base.object_id is None or
                self.error
        ):
            self.base.save()
            return True
        return False
