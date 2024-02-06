from django.db.models import Q

from eProc_Basic.Utilities.constants.constants import CONST_COMPANY_CODE, CONST_PORG, CONST_PGROUP, CONST_USER, \
    CONST_RNODE
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.sort_dictionary import sort_list_dictionary_key_values
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import OrgCompanies, OrgPorg, OrgPGroup
from eProc_Org_Model.models import OrgModel, OrgNames
from eProc_Registration.models import UserData
from eProc_User_Settings.Utilities.user_settings_generic import get_object_id_list_user
from eProc_Basic.Utilities.global_defination import global_variables

django_query_instance = DjangoQueries()


class OrgNodesSearch:
    dict_nodes = {}
    counter = 0

    def company_search(self, input):
        """
        Company Code Search
        :param input: Match string
        :return: Search result based on the string passed
        """
        if input == '*':
            result = list(OrgCompanies.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                                      object_id_id__isnull=False, del_ind=False).values_list(
                'object_id', flat=True))
        else:
            result = list(OrgCompanies.objects.filter(
                Q(client=global_variables.GLOBAL_CLIENT, object_id_id__isnull=False, company_id__icontains=input,
                  del_ind=False) |
                Q(client=global_variables.GLOBAL_CLIENT, object_id_id__isnull=False,
                  name1__icontains=input, del_ind=False) | Q(client=global_variables.GLOBAL_CLIENT,
                                                             object_id_id__isnull=False,
                                                             name2__icontains=input, del_ind=False)).values_list(
                'object_id', flat=True))
        org_model_result = list(OrgModel.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                                        name__icontains=input, node_type=CONST_COMPANY_CODE,
                                                        del_ind=False).values_list('object_id', flat=True))
        if org_model_result:
            result += org_model_result

        return result

    def purchase_org_search(self, input):
        """
        Purchase Org Search
        :param input: Match string
        :return: Search result based on the string passed
        """
        if input == '*':
            result = list(OrgPorg.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                                 object_id_id__isnull=False, del_ind=False).values_list('object_id',
                                                                                                        flat=True))
        else:
            result = list(OrgPorg.objects.filter(
                Q(client=global_variables.GLOBAL_CLIENT, object_id_id__isnull=False, porg_id__icontains=input,
                  del_ind=False) |
                Q(client=global_variables.GLOBAL_CLIENT, object_id_id__isnull=False,
                  description__icontains=input, del_ind=False)).values_list('object_id', flat=True))
        org_model_result = list(OrgModel.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                                        name__icontains=input,
                                                        node_type=CONST_PORG, del_ind=False).values_list('object_id',
                                                                                                         flat=True))
        if org_model_result:
            result += org_model_result
        return result

    def purchase_grp_search(self, input):
        """
        Purchase Group Search
        :param input: Match string
        :return: Search result based on the string passed
        """
        if input == '*':
            result = list(OrgPGroup.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                                   object_id_id__isnull=False, del_ind=False).values_list('object_id',
                                                                                                          flat=True))
        else:
            result = list(OrgPGroup.objects.filter(
                Q(client=global_variables.GLOBAL_CLIENT, object_id_id__isnull=False, pgroup_id__icontains=input,
                  del_ind=False) |
                Q(client=global_variables.GLOBAL_CLIENT, object_id_id__isnull=False,
                  description__icontains=input, del_ind=False)).values_list('object_id', flat=True))
        org_model_result = list(OrgModel.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                                        name__icontains=input,
                                                        node_type=CONST_PGROUP,
                                                        del_ind=False).values_list('object_id', flat=True))
        if org_model_result:
            result += org_model_result
        return result

    def org_user_search(self, input):
        """
        User Search
        :param input: Match string
        :return: Search result based on the string passed
        """
        if input == '*':
            result = list(UserData.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                                  object_id_id__isnull=False, del_ind=False).values_list('object_id',
                                                                                                         flat=True))
        else:
            result = list(UserData.objects.filter(
                Q(client=global_variables.GLOBAL_CLIENT, object_id_id__isnull=False, first_name__icontains=input,
                  del_ind=False) |
                Q(client=global_variables.GLOBAL_CLIENT, object_id_id__isnull=False,
                  last_name__icontains=input, del_ind=False) | Q(client=global_variables.GLOBAL_CLIENT,
                                                                 object_id_id__isnull=False,
                                                                 username__icontains=input, del_ind=False)).values_list(
                'object_id', flat=True))
        org_model_result = list(OrgModel.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                                        name__icontains=input,
                                                        node_type=CONST_USER
                                                        , del_ind=False).values_list('object_id', flat=True))
        if org_model_result:
            result += org_model_result

        return result

    def get_node(self, node_id):
        """
        Get the parents chain for the respective searched node
        :param node_id: Searched node
        :return: Parents chain for the searched node
        """
        level = OrgModel.objects.filter(client=global_variables.GLOBAL_CLIENT, object_id=node_id)
        if level[0].parent_node_guid != None and len(level) != 0:
            self.counter = self.counter + 1
            self.dict_nodes[self.counter] = list(level.values_list('object_id', 'name', 'node_guid', 'node_type'))
            parent_node = OrgModel.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                                  node_guid=level[0].parent_node_guid)
            if parent_node[0].parent_node_guid != None:
                return self.get_node(parent_node[0].object_id)
            else:
                self.counter = self.counter + 1
                self.dict_nodes[self.counter] = list(
                    parent_node.values_list('object_id', 'name', 'node_guid', 'node_type'))
                return 0


def get_org_model_detail(object_id):
    """

    """
    node_guid_list = []
    object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT, object_id)
    object_id_list.reverse()
    root_node_name = []
    if object_id_list:

        if OrgModel.objects.filter(object_id=object_id_list[0],
                                   client=global_variables.GLOBAL_CLIENT).exists():
            root_node_name = list(OrgModel.objects.filter(object_id=object_id_list[0],
                                                          client=global_variables.GLOBAL_CLIENT).values_list('name',
                                                                                                             flat=True))[
                0]
        org_model_detail = list(OrgModel.objects.filter(object_id__in=object_id_list,
                                                        client=global_variables.GLOBAL_CLIENT).values('object_id',
                                                                                                      'node_type',
                                                                                                      'name',
                                                                                                      'node_guid',
                                                                                                      'node_type'))
        org_model_detail = sort_list_dictionary_key_values(object_id_list, org_model_detail, 'object_id')
        for org_model_details in org_model_detail:
            org_dictionary = {'node_guid': org_model_details['node_guid'],
                              'node_name': org_model_details['name'],
                              'object_id': org_model_details['object_id']
                              }
            node_guid_list.append(org_dictionary)
    return node_guid_list, object_id_list, root_node_name


def update_node_details(json_data):
    """

    """
    if json_data['node_type'] == CONST_COMPANY_CODE:
        if DjangoQueries.django_existence_check(OrgCompanies, {'client': global_variables.GLOBAL_CLIENT,
                                                               'object_id': json_data['object_id']}):
            DjangoQueries.django_update_or_create_query(OrgCompanies,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'object_id': json_data['object_id']},
                                                        {'name1': json_data['name1'],
                                                         'name2': json_data['name1'],
                                                         'del_ind': False})
        else:
            if json_data['company_id']:
                DjangoQueries.django_update_or_create_query(OrgCompanies,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'company_id': json_data['company_id']},
                                                            {'name1': json_data['name1'],
                                                             'name2': json_data['name1'],
                                                             'object_id': OrgModel.objects.get(
                                                                 object_id=json_data['object_id']),
                                                             'del_ind': False})
    if json_data['node_type'] == CONST_PORG:
        if DjangoQueries.django_existence_check(OrgPorg, {'client': global_variables.GLOBAL_CLIENT,
                                                          'object_id': json_data['object_id']}):
            DjangoQueries.django_update_or_create_query(OrgPorg,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'object_id': json_data['object_id']},
                                                        {'description': json_data['description']})
        else:
            if json_data['porg_id']:
                DjangoQueries.django_update_query(OrgPorg,
                                                  {'client': global_variables.GLOBAL_CLIENT,
                                                   'porg_id': json_data['porg_id']},
                                                  {'description': json_data['description'],
                                                   'object_id': OrgModel.objects.get(
                                                       object_id=json_data['object_id'])})
    if json_data['node_type'] == CONST_PGROUP:
        if DjangoQueries.django_existence_check(OrgPGroup, {'client': global_variables.GLOBAL_CLIENT,
                                                            'object_id': json_data['object_id']}):
            DjangoQueries.django_update_or_create_query(OrgPGroup,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'object_id': json_data['object_id']},
                                                        {'description': json_data['description']})
        else:
            if json_data['pgrp_id']:
                porg_id = get_porg_id_by_pgrp(json_data['object_id'])
                DjangoQueries.django_update_or_create_query(OrgPGroup,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'pgroup_id': json_data['pgrp_id']},
                                                            {'description': json_data['description'],
                                                             'object_id': OrgModel.objects.get(
                                                                 object_id=json_data['object_id']),
                                                             'porg_id': porg_id})


def get_porg_id_by_pgrp(pgrp_object_id):
    """

    """
    porg_object_id = None
    porg_id = None
    pgrp_parent_guid = None
    if django_query_instance.django_existence_check(OrgModel,
                                                    {'object_id': pgrp_object_id,
                                                     'del_ind': False,
                                                     'client': global_variables.GLOBAL_CLIENT}):
        pgrp_parent_guid = django_query_instance.django_filter_value_list_query(OrgModel,
                                                                                {'object_id': pgrp_object_id,
                                                                                 'del_ind': False,
                                                                                 'client': global_variables.GLOBAL_CLIENT},
                                                                                'parent_node_guid')
        if pgrp_parent_guid:
            pgrp_parent_guid = pgrp_parent_guid[0]
            porg_object_id = django_query_instance.django_filter_value_list_query(OrgModel,
                                                                                  {'node_guid': pgrp_parent_guid,
                                                                                   'del_ind': False,
                                                                                   'client': global_variables.GLOBAL_CLIENT},
                                                                                  'object_id')
        if porg_object_id:
            porg_object_id = porg_object_id[0]
            porg_id = django_query_instance.django_filter_value_list_query(OrgPorg,
                                                                           {'object_id': porg_object_id,
                                                                            'del_ind': False,
                                                                            'client': global_variables.GLOBAL_CLIENT},
                                                                           'porg_id')
            if porg_id:
                porg_id = porg_id[0]
    return porg_id
