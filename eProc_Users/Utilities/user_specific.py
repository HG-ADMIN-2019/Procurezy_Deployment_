from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Registration.models import UserData

django_query_instance = DjangoQueries()


def get_user_list_by_input(request):
    inp_emp_id = request.POST.get('employee_id')
    inp_first_name = request.POST.get('first_name')
    inp_last_name = request.POST.get('last_name')
    inp_user_locked = request.POST.get('user_locked')
    inp_pwd_locked = request.POST.get('password_locked')
    inp_username = request.POST.get('username')
    inp_active = request.POST.get('active')

    args_list = {}
    client = getClients(request)

    if inp_emp_id is not None and inp_emp_id != '':
        args_list['employee_id'] = inp_emp_id

    if inp_first_name is not None and inp_first_name != '':
        args_list['first_name'] = inp_first_name

    if inp_last_name is not None and inp_last_name != '':
        args_list['last_name'] = inp_last_name

    if inp_user_locked is not None and inp_user_locked != '':
        if inp_user_locked == 'on':
            inp_user_locked = True
        else:
            inp_user_locked = False

        args_list['user_locked'] = inp_user_locked

    if inp_pwd_locked is not None and inp_pwd_locked != '':
        if inp_pwd_locked == 'on':
            inp_pwd_locked = True
        else:
            inp_pwd_locked = False

        args_list['pwd_locked'] = inp_pwd_locked

    if inp_active is not None and inp_active != '':
        if inp_active == 'on':
            inp_active = True
        else:
            inp_active = False

        args_list['is_active'] = inp_active

    if inp_username is not None and inp_username != '':
        args_list['username'] = inp_username

    args_list['client'] = client
    args_list['del_ind'] = False

    result = django_query_instance.django_filter_only_query(UserData, args_list)

    return result
