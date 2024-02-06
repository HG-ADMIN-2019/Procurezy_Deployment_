from django.http import JsonResponse, HttpResponse
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_SOBO.Utilities.sobo_specific import ShopOnBehalfOf
from eProc_Shopping_Cart.context_processors import update_user_info


# @authorize_view(CONST_SOBO)
def get_sobo_users(request):
    update_user_info(request)
    if request.is_ajax():
        sobo_users = ShopOnBehalfOf(global_variables.GLOBAL_LOGIN_USER_OBJ_ID).get_sobo_users()
        return JsonResponse({'username_list': sobo_users}, status=200)

    return HttpResponse('Success')
