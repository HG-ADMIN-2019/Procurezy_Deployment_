import re
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Configuration.models.basic_data import Languages
from eProc_Configuration.models.master_data import OrgCompanies
from eProc_Configuration.models.development_data import *
from eProc_Registration.models.registration_model import UserData

django_query_instance = DjangoQueries()


def get_companylist(req):
    client = getClients(req)
    company_list = OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id', 'name1')
    return list(company_list)


def get_companyDetails(req):
    client = getClients(req)
    return django_query_instance.django_filter_only_query(OrgCompanies, {'client': client, 'del_ind': False})


def get_account_assignlist(req):
    return django_query_instance.django_filter_value_list_query(AccountAssignmentCategory, {'del_ind': False},
                                                                'account_assign_cat')


def get_account_assignvalues(req):
    result = django_query_instance.django_filter_query(AccountAssignmentCategory, {'del_ind': False},
                                                       None, ['account_assign_cat', 'description'])
    return result


def get_langlist(req):
    return django_query_instance.django_filter_query(Languages, {'del_ind': False}, None, None)


def get_usrid_by_username(username: object, active) -> object:
    if '*' in username and active is not None:
        uname = re.search(r'[a-zA-Z0-9]+', username)
        if username[0] == '*' and username[-1] == '*':
            queryset = django_query_instance.django_filter_only_query(UserData, {'username__icontains': uname.group(0),
                                                                                 'is_active': active})
        elif username[0] == '*':
            queryset = django_query_instance.django_filter_only_query(UserData, {'username__iendswith': uname.group(0),
                                                                                 'is_active': active})
        else:
            queryset = django_query_instance.django_filter_only_query(UserData,
                                                                      {'username__istartswith': uname.group(0),
                                                                       'is_active': active})
    else:
        queryset = django_query_instance.django_filter_only_query(UserData, {'username': username,
                                                                             'is_active': active})

    return queryset
