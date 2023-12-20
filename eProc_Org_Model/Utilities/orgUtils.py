from django.shortcuts import get_object_or_404
from eProc_Org_Model.Utilities.client import OrgClient


class OrgUtils:
    def __init__(self, klass, client_id, pk):
        """
        Initialization of utility
        :param klass: Name of the class
        :param client_id: Client
        :param pk: Primary key
        """
        client = OrgClient.get_client(client_id)
        if pk is None:
            self.base = klass()
            self.base.client = client
        else:
            self.base = get_object_or_404(klass, client=client, pk=pk, del_ind=False)
        self.error = False
        self.message = {}

    # To set the properties
    def set_base_props(self, key, value):
        setattr(self.base, key, value)

    # To set the error messages
    def set_error(self, msg):
        self.error = True
        self.message = '{"error": "' + msg + '"}'
