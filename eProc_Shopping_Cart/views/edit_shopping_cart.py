from django.db import transaction
from django.http.response import JsonResponse

from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Shopping_Cart.Utilities.save_order_edit_sc import EditShoppingCart
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import get_manger_detail, save_approver_detail
from eProc_Shopping_Cart.context_processors import update_user_info


@transaction.atomic
def edit_saved_shopping_cart(request):
    update_user_info(request)
    edit_sc = EditShoppingCart(request)
    if 'delete_sc' in request.POST:
        header_guid = request.POST.get('header_guid')
        edit_sc.delete_sc(header_guid)

        return JsonResponse({'message': ''})
    else:
        del_item_guid = request.POST.get('del_item_guid')
        total_value = request.POST.get('total_value')
        header_guid = request.POST.get('header_guid')
        delete_info = edit_sc.delete_item_from_sc(del_item_guid, total_value, header_guid)
        save_approver_detail(header_guid)
        return JsonResponse({'total_value': delete_info[0], 'count': delete_info[1]})
