from eProc_Attributes.models.org_attribute_models import OrgAttributesLevel
from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Org_Model.models import OrgModel
from eProc_Registration.models import UserData

django_query_instance = DjangoQueries()


class ShopOnBehalfOf:
    def __init__(self, user_object_id):
        self.sobo_users = []
        self.user_object_id = user_object_id
        self.user_object_id_list = []

    def get_username_from_object_id(self, object_id_list):
        django_query_instance.django_filter_value_list_query(UserData, {'object_id__in': object_id_list}, 'username')
        self.sobo_users = django_query_instance.django_filter_value_list_query(UserData,
                                                                               {'object_id__in': object_id_list},
                                                                               'username')

        return self.sobo_users

    def get_sobo_users(self):
        get_obj_id_list = django_query_instance.django_filter_value_list_query(OrgAttributesLevel, {
            'attribute_id': CONST_SOBO, 'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
        }, 'low')

        get_node_type = django_query_instance.django_filter_only_query(OrgModel, {
            'object_id__in': get_obj_id_list, 'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
        })

        for org_info in get_node_type:
            if org_info.node_type == CONST_NODE:
                parent_guid = org_info.node_guid
                self.user_object_id_list = django_query_instance.django_filter_value_list_query(OrgModel, {
                    'parent_node_guid': parent_guid, 'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
                }, 'object_id')

                # Removing login users object ID
                if global_variables.GLOBAL_LOGIN_USER_OBJ_ID in self.user_object_id_list:
                    self.user_object_id_list.remove(global_variables.GLOBAL_LOGIN_USER_OBJ_ID)

        # Get users based on login user object id
        self.user_object_id_list = self.user_object_id_list + django_query_instance.django_filter_value_list_query(OrgAttributesLevel, {
            'attribute_id': CONST_SOBO, 'object_id': self.user_object_id, 'client': global_variables.GLOBAL_CLIENT,
            'del_ind': False
        }, 'low')

        self.user_object_id_list = list(map(int, self.user_object_id_list))
        sobo_users = self.get_username_from_object_id(list(set(self.user_object_id_list)))

        return sobo_users
