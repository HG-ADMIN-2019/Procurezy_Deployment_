from django.shortcuts import get_object_or_404

from eProc_Configuration.models.development_data import OrgClients


class OrgClient:
    """
    Handle client data
    """
    @staticmethod
    def get_client(client):
        """
        Queries for client
        :param client: client ID
        :return: Returns OrgClients instance
        """
        return get_object_or_404(OrgClients, pk=client)
