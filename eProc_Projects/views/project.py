from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render, redirect
from eProc_Basic.Utilities.constants.constants import CONST_COFIG_UI_MESSAGE_LIST, CONST_TIME_SHEET_UI_MESSAGE_LIST
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.guid_generator import dynamic_guid_generator
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.messages_config import get_message_desc
from eProc_Basic.Utilities.functions.randam_generator import random_alpha_numeric
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages import messages
from eProc_Configuration.Utilities.application_settings_generic import get_ui_messages
from eProc_Configuration.models.application_data import ProjectDetails
from eProc_Projects.Utilities.project_generic import project_search
from eProc_Projects.Utilities.project_specific import save_project_to_db, get_project_filter_list
from eProc_Registration.Registration_Forms.user_registration_form import RegForm
from eProc_Registration.Utilities.registration_specific import RegFncts
from eProc_Shopping_Cart.context_processors import update_user_info

JsonParser_obj = JsonParser()
django_query_instance = DjangoQueries()

@login_required
def time_sheet(req):
    """
    :param req:
    :return:
    """
    context = {
        'inc_nav': True,
        'inc_footer': True,
    }
    return render(req, 'create_project/create_project.html', context)


def proj_user_search(request):
    """

    """
    # Fetch Project data
    project_id = django_query_instance.django_filter_query(ProjectDetails, {'del_ind': False}, None,
                                                           ['project_detail_guid',
                                                            'project_id',
                                                            'project_desc',
                                                            'project_name',
                                                            'start_date',
                                                            'end_date'])
    messages_list = get_ui_messages(CONST_TIME_SHEET_UI_MESSAGE_LIST)
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'project_id': project_id,
        'messages_list': messages_list,
        'is_slide_menu': True,
        'is_timesheet_active': True
    }

    return render(request, 'create_project/enter_project_categories.html', context)



@login_required
def proj_register_page(request):
    """
    :param request: Request data from UI
    :return: render user_register.html
    """
    global error_msg
    message_desc = ''
    update_user_info(request)
    reg_form = RegForm()
    if request.method == 'POST':
        reg_form = RegForm(request.POST or None)

        if reg_form.is_valid():
            new_project = reg_form.save(commit=False)
            password = random_alpha_numeric(8)
            new_project.password = make_password(password)
            new_project.password2 = make_password(password)
            project_id = request.POST['project_id']
            if django_query_instance.django_existence_check(ProjectDetails,
                                                            {'project_id': project_id,
                                                             'del_ind': False}):
                error_msg = 'Project Id exists'
            else:
                is_created = RegFncts.create_project(request, new_project, global_variables.GLOBAL_CLIENT, password)
                if is_created:
                    # msgid = 'MSG017'
                    # error_msg = get_msg_desc(msgid)
                    # msg = error_msg['message_desc'][0]
                    # error_msg = msg
                    message_desc = get_message_desc('MSG017')[1]
                messages.success(request, message_desc)

                # messages.success(request, MSG017)
                return redirect('eProc_Projects:proj_register_page')

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'reg_form': reg_form,
    }

    return render(request, 'create_project/enter_project_categories.html', context)


def save_project_db(request):
    """

    :param request:
    :return:
    """
    update_user_info(request)
    project_data = JsonParser_obj.get_json_from_req(request)
    project_data_response = save_project_to_db(project_data)
    return JsonResponse(project_data_response, safe=False)


def generate_guid(request):
    """

        """
    project = {}
    project['project_id'] = dynamic_guid_generator(4)
    return JsonResponse(project, safe=False)


def delete_project(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    project_data = JsonParser_obj.get_json_from_req(request)
    django_query_instance.django_update_query(ProjectDetails,
                                              {'project_id__in': project_data['data'],
                                               'client': global_variables.GLOBAL_CLIENT},
                                              {'del_ind': True})

    project_results = django_query_instance.django_filter_query(ProjectDetails, {
        'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
    }, None, None)
    response = {'project_results': project_results, 'success_message': "project deleted"}
    return JsonResponse(response, safe=False)


def project_config(request):
    """

    """
    update_user_info(request)
    project_query = []
    if request.method == 'GET':
        filter_query = {'client': global_variables.GLOBAL_CLIENT, 'del_ind': False}
        project_query = get_project_filter_list(filter_query, 10)
    elif request.method == 'POST' and request.is_ajax():
        project_details = JsonParser().get_json_from_req(request)
        project_details_query = project_search(**project_details)
        return JsonResponse(project_details_query, safe=False)

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_content_mgmnt_active': True,
        'project_query': project_query
    }
    return render(request,
                  'create_project/enter_project_categories.html', context)
