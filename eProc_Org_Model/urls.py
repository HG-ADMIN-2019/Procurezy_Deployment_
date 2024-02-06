from django.urls import path
from . import views
from .views import *

app_name = 'eProc_Org_Model'

urlpatterns = [
    path('org_structure/', views.org_model_ui, name='org_structure'),
    path('filter_nodes/', views.org_nodes_filter_fun, name='org_nodes_filter'),
    path('filter_nodes_position/', views.get_node_tree_strcture, name='org_node_tree_structure'),
    path('org/<str:action>', HandleOrg.as_view(), name="org_handle"),  # Refers to org related actions
    path('node/<str:action>', HandleNode.as_view(), name="node_handle"),  # Refers to node related actions
    path('users/<str:action>', HandleUsers.as_view(), name="user_handle"),  # Refers to users related actions
    path('node-types/getall', HandleNodeTypes.as_view(), name="node_types_handle"),  # Refers to node-types
    path('basic-data/<str:action>', HandleBasicData.as_view(), name="basicdata_tab"),  # Refers to basic data tab
    path('details/<str:action>', HandleDetails.as_view(), name="details_tab"),  # Refers to details tab
    path('get_all_orgs', get_all_organisations, name='get_all_orgs'),
    path('get_all_children', get_children, name='get_all_children'),
    path('get_all_node_types', get_node_types, name='get_all_node_types'),
    path('org_node_detail', org_node_detail, name='org_node_detail'),
    path('save_basic_details_ajax_call', save_basic_details_ajax_call, name="save_basic_details_ajax_call"),
    path('org_model_information', org_model_information, name="org_model_information"),



]