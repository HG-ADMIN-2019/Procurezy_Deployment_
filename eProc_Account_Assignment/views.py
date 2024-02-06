from django.http import JsonResponse
from eProc_Account_Assignment.Utilities.account_assignment_generic import AccountAssignment, \
    AccountAssignmentCategoryDetails, get_gl_acc_value, get_attribute_id_based_on_acc
from eProc_Account_Assignment.Utilities.account_assignment_specific import ACCValueDesc
from eProc_Basic.Utilities.constants.constants import CONST_CO_CODE
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Shopping_Cart.context_processors import update_user_info, update_user_obj_id_list_info
from eProc_User_Settings.Utilities.user_settings_generic import get_object_id_list_user, get_attr_value


def change_acc_assignment_cat(request):
    update_user_info(request)
    update_user_obj_id_list_info()
    user_object_id_list = global_variables.USER_OBJ_ID_LIST
    item_total_value = 0
    if request.method == 'POST':
        company_code = request.POST.get('default_company_code')
        account_assignment_type = request.POST.get('acc_type')
        item_prod_cat = request.POST.get('item_prod_cat')
        item_value = request.POST.get('item_total_value')
        if item_value:
            item_total_value = float(request.POST.get('item_total_value'))
        item_currency = request.POST.get('item_currency')
        item_language = global_variables.GLOBAL_REQUESTER_LANGUAGE
        ajax_context = AccountAssignment(user_object_id_list).change_account_assignment_category(account_assignment_type,
                                                                                                 company_code,
                                                                                                 item_prod_cat,
                                                                                                 item_total_value,
                                                                                                 item_currency,
                                                                                                 item_language)

        return JsonResponse(ajax_context)


def gl_acc_detail(request):
    """

    """
    update_user_info(request)
    gl_acc_desc = {}
    item_detail_list = {'value': request.POST.get('value'),
                        'prod_cat': request.POST.get('prod_cat'), 'acc': request.POST.get('acc')}
    object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT, global_variables.GLOBAL_LOGIN_USER_OBJ_ID)
    edit_flag = False
    company_code = get_attr_value(global_variables.GLOBAL_CLIENT, CONST_CO_CODE, object_id_list, edit_flag)
    gl_acc_details = get_gl_acc_value(item_detail_list, company_code)
    gl_acc_desc['gl_acc_details'] = gl_acc_details

    return JsonResponse(gl_acc_desc, safe=False)


def search_acc_value(request):
    """

    """
    update_user_info(request)
    account_assignment_cat = request.POST.get('acc_type')
    company_code = request.POST.get('default_company_code')
    attribute_id = get_attribute_id_based_on_acc(account_assignment_cat)
    object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT, global_variables.GLOBAL_LOGIN_USER_OBJ_ID)
    append_acc_value_desc = ACCValueDesc.get_acc_values_and_desc_append_list(object_id_list,attribute_id,company_code,account_assignment_cat)
    acc_value_desc ={'append_acc_value_desc':append_acc_value_desc}
    return JsonResponse(acc_value_desc)

