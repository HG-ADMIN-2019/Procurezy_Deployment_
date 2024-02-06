from django.db.models import Q
from django.http import JsonResponse

from eProc_Basic.Utilities.functions.django_q_query import django_q_query
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import encrypt
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import FieldTypeDescription, OrgPorg
from eProc_Registration.models import UserData

django_query_instance = DjangoQueries()


def user_detail_search(**kwargs):
    """

    """
    search_query = {}
    client = global_variables.GLOBAL_CLIENT
    username_query = Q()
    first_name_query = Q()
    last_name_query = Q()
    email_query = Q()
    user_type_query = Q()
    employee_id_query = Q()
    pwd_locked_query = Q()
    user_locked_query = Q()
    is_active_query = Q()
    instance = UserData()
    for key, value in kwargs.items():
        value_list = []
        if value:
            if key == 'username':
                if '*' not in value:
                    value_list = [value]
                username_query = django_q_query(value, value_list, 'username')
            if key == 'first_name':
                if '*' not in value:
                    value_list = [value]
                first_name_query = django_q_query(value, value_list, 'first_name')
            if key == 'last_name':
                if '*' not in value:
                    value_list = [value]
                last_name_query = django_q_query(value, value_list, 'last_name')
            if key == 'email':
                if '*' not in value:
                    value_list = [value]
                email_query = django_q_query(value, value_list, 'email')
            if key == 'user_type':
                if '*' not in value:
                    value_list = [value]
                if value == 'All':
                    value_list = ['Buyer', 'Support']
                user_type_query = django_q_query(value, value_list, 'user_type')
            if key == 'employee_id':
                if '*' not in value:
                    value_list = [value]
                employee_id_query = django_q_query(value, value_list, 'employee_id')
            if key == 'pwd_locked':
                value = '1'
                value_list = '1'
                pwd_locked_query = django_q_query(value, value_list, 'pwd_locked')
            if key == 'user_locked':
                value = '1'
                value_list = '1'
                user_locked_query = django_q_query(value, value_list, 'user_locked')
            if key == 'is_active':
                value = '0'
                value_list = '0'
                is_active_query = django_q_query(value, value_list, 'is_active')

    user_details_query = list(instance.get_user_details_by_fields(client,
                                                                  instance,
                                                                  username_query,
                                                                  first_name_query,
                                                                  last_name_query,
                                                                  email_query,
                                                                  user_type_query,
                                                                  employee_id_query,
                                                                  pwd_locked_query,
                                                                  user_locked_query,
                                                                  is_active_query
                                                                  ))
    return user_details_query


def get_usertype_values():
    dropdown_usertype_values = list(
        FieldTypeDescription.objects.filter(field_name='user_type', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'
                                                                                          ))
    return dropdown_usertype_values


def get_emp_data():
    employee_results = django_query_instance.django_filter_query(UserData,
                                                                 {'client': global_variables.GLOBAL_CLIENT,
                                                                  'del_ind': False, 'is_active': True},
                                                                 None, None)

    for emails in employee_results:
        encrypt_email = encrypt(emails['email'])
        emails['encrypted_email'] = encrypt_email
    return employee_results


def get_emp_data_onload(request):
    employee_results = django_query_instance.django_filter_query(UserData,
                                                                 {'client': global_variables.GLOBAL_CLIENT,
                                                                  'del_ind': False, 'is_active': True},
                                                                 None, None)

    for emails in employee_results:
        encrypted_email1 = encrypt(emails['email'])
        emails['encrypted_email'] = encrypted_email1
    count = len(employee_results)
    data = {'employee_results': employee_results, 'count': count}
    return JsonResponse(data, safe=False)


global encrypted_email


def emp_search_data(search_fields):
    employee_results = user_detail_search(**search_fields)
    for user_email in employee_results:
        encrypted_email = encrypt(user_email['email'])
        user_email['encrypted_email'] = encrypted_email

    return employee_results


def set_search_data(value):
    if value == 'on':
        value = True
    else:
        value = False
    return value


def get_supplier_type_values():
    dropdown_suptype_values = list(
        FieldTypeDescription.objects.filter(field_name='supplier_type', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'
                                                                                          ))
    return dropdown_suptype_values


def get_output_medium_values():
    dropdown_output_med_values = list(
        FieldTypeDescription.objects.filter(field_name='output_medium', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'
                                                                                          ))
    return dropdown_output_med_values
