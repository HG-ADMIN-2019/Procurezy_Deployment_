from django.db.models import Q

from eProc_Basic.Utilities.functions.django_q_query import django_q_query
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import ProjectDetails


def project_search(**kwargs):
    """

    """
    project_id_query = Q()
    project_desc_query = Q()
    project_name_query = Q()
    instance = ProjectDetails()
    search_count = kwargs.get('search_count', 10)
    for key, value in kwargs.items():
        value_list = []
        if value:
            if '*' not in value:
                value_list = [value]
            if key == 'project_id':
                project_id_query = django_q_query(value, value_list, 'project_id')
            if key == 'project_desc':
                project_desc_query = django_q_query(value, value_list, 'project_desc')
            if key == 'project_name':
                project_name_query = django_q_query(value, value_list, 'project_name')
            if key == 'search_count':
                search_count = int(value)

    project_details_query = list(instance.get_project_fields(global_variables.GLOBAL_CLIENT,
                                                             project_id_query,
                                                             project_desc_query,
                                                             project_name_query,
                                                             search_count))
    return project_details_query
