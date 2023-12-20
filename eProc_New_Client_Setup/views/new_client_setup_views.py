import datetime

from django.contrib.auth.hashers import make_password
from django.db.models import ProtectedError
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from eProc_Attributes.Utilities.attributes_specific import save_attr_id_data_into_db
from eProc_Basic.Utilities.constants.constants import CONST_PWD, CONST_ASSIGN, CONST_US_ROLE, CONST_SHOP_ADMIN, \
    CONST_NODE
from eProc_Basic.Utilities.functions.camel_case import convert_to_camel_case
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import get_super_user_detail_based_on_client
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.messages_config import get_message_desc, get_message_desc_without_client
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import OrgClients
from eProc_Generate_OTP.Utilities.generate_otp_generic import authentication_check, otp_generator
from eProc_Generate_OTP.models import OtpGenerator
from eProc_New_Client_Setup.Utilities.new_client_setup_specific import InitialSetupClient, \
    create_organization_structure, get_client_data, delete_client_from_db, delete_application_setup_client
from eProc_Org_Model.Utilities.apiHandler import ApiHandler
from eProc_Org_Model.models import OrgModel
from eProc_Registration.Registration_Forms.user_registration_form import RegForm, UserRegForm
from eProc_Registration.Utilities.registration_specific import RegFncts
from eProc_Registration.models import UserData

django_query_instance = DjangoQueries()
JsonParser_obj = JsonParser()


def new_client_setup(request):
    """

    """
    client_data = get_client_data()
    django_query_instance.django_update_query(OtpGenerator,
                                              {'del_ind': False},
                                              {'otp': None})

    context = {'client_details': client_data, 'inc_nav': True, 'inc_footer': True}
    return render(request, 'new_client_setup.html', context)


def save_new_client(request):
    """

    """
    message = None
    client_detail = JsonParser_obj.get_json_from_req(request)
    if not django_query_instance.django_existence_check(OrgClients,
                                                        {'client': client_detail['client_id'],
                                                         'del_ind': False}):
        django_query_instance.django_create_query(OrgClients,
                                                  {'client': client_detail['client_id'],
                                                   'description': client_detail['client_description'],
                                                   'org_clients_created_at': datetime.datetime.now(),
                                                   'org_clients_created_by': 'DEEPIKA',
                                                   })
        message = "Client data saved successfully"
        error_message_status = False
    else:
        message = "Client data already exists"
        error_message_status = True
    client_data = get_client_data()
    return JsonResponse({'message': message,
                         'client_data': client_data,
                         'error_message_status': error_message_status}, safe=False)


def set_up_new_client(request):
    """

    """
    message = None
    client_id = JsonParser_obj.get_json_from_req(request)
    initial_setup_client = InitialSetupClient(client_id)
    delete_application_setup_client(client_id)
    # save basic data
    initial_setup_client.initial_save_basic_data()
    # save application data
    initial_setup_client.initial_save_application_data()
    client_data = get_client_data()
    return JsonResponse({'client_data': client_data}, safe=False)


def create_org_model(request):
    """

    """
    client_id = JsonParser_obj.get_json_from_req(request)
    create_organization_structure(client_id)
    client_data = get_client_data()
    return JsonResponse({'client_data': client_data}, safe=False)


def admin_authentication(request):
    """

    """
    email = request.POST.get('email')
    password = request.POST.get('password')
    user_data = {'email': email, 'password': password}
    authentication_flag, error_msg = authentication_check(user_data)

    if authentication_flag:
        otp_generator(email)
    auth_data = {'authentication_flag': authentication_flag, 'error_msg': error_msg}
    return JsonResponse({'auth_data': auth_data}, status=201)


def new_client_user_registration(request, client_id):
    username = ''
    email_id = ''

    reg_form = UserRegForm()

    if request.method == 'POST':
        reg_form = UserRegForm(request.POST or None)

        if reg_form.is_valid():
            new_user = reg_form.save(commit=False)
            username = new_user.username
            new_user.client_id = django_query_instance.django_get_query(OrgClients, {'client': client_id})
            email_id = new_user.email
            new_user.is_superuser = True
            new_user.password = make_password(CONST_PWD)
            new_user.password2 = make_password(CONST_PWD)
            new_user.save()
        if username:
            if client_id:
                client_detail = django_query_instance.django_get_query(OrgClients,
                                                                       {'client': client_id})
                node_name = 'NODE_' + str(client_id)
                node_name = node_name.capitalize()
                org_model_detail = django_query_instance.django_get_query(OrgModel,
                                                                          {'client': client_id,
                                                                           'name': node_name,
                                                                           'node_type': CONST_NODE
                                                                           })
                if org_model_detail:
                    result = ApiHandler.save_assign_unassign_data(client_detail, [username], CONST_ASSIGN,
                                                                  org_model_detail.node_guid,
                                                                  org_model_detail.root_node_object_id)

                    if result:
                        user_detail = django_query_instance.django_get_query(UserData,
                                                                             {'email': email_id})
                        attr_id_data = [{'attribute_id': CONST_US_ROLE,
                                         'value': CONST_SHOP_ADMIN,
                                         'attr_level_default': 1,
                                         'inherit': 0,
                                         'attr_level_exclude': 0,
                                         'object_id': user_detail.object_id_id}]
                        save_attr_id_data_into_db(attr_id_data, user_detail.object_id_id, client_id)
                        return HttpResponseRedirect('/setup_new_client/new_client_setup/')

    context = {'inc_nav': True, 'inc_footer': True, 'reg_form': reg_form}

    return render(request, 'new_client_user_registration.html', context)


def view_users(request):
    """

    """
    client_id = request.POST.get('client_id')
    user_data = get_super_user_detail_based_on_client(client_id)
    return JsonResponse({'user_data': user_data}, status=201)


def update_client_description(request):
    """

    """
    client_id = request.POST.get('client_id')
    description = request.POST.get('description')
    django_query_instance.django_update_query(OrgClients,
                                              {'client': client_id}, {'description': description})
    return JsonResponse({}, status=201)


def delete_client(request):
    """

    """
    client_id = request.POST.get('client_id')
    delete_client_from_db(client_id)
    client_data = get_client_data()
    return JsonResponse({'client_data': client_data}, safe=False)

