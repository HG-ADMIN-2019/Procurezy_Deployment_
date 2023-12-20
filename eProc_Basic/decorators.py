from django.http import HttpResponseForbidden
from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.get_db_query import update_user_roles_to_session, get_all_auth_obj_groups, \
    get_shop_sub_roles


class CheckForAuthorisations:
    def __init__(self, user_roles, check_auth_type, shop_sub_auth):
        self.check_auth_type = check_auth_type
        self.shop_sub_auth = shop_sub_auth

    def authorize_shop_and_shop_plus_views(self):
        if self.check_auth_type in self.shop_sub_auth:
            return True
        else:
            return False


# Validating view functions for both shopper and shopper plus role
def validate_shop_and_shop_plus_role(check_auth):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            """
            Wrapper with arguments to invoke the method
            """
            if 'user_roles' in request.session:
                user_roles = request.session['user_roles']
            else:
                user_roles = update_user_roles_to_session(request)

            # If the document is opened from completion step it checks if the user as SHOP_ASSIST role
            if 'flag' in kwargs:
                if kwargs['flag'] == 'True':
                    if CONST_SHOP_ASSIST in user_roles:
                        return view_method(request, *args, **kwargs)
                    else:
                        return HttpResponseForbidden()

            if CONST_SHOP_PLUS in user_roles:
                shop_sub_auth_id = 'Shopping Plus'

            elif CONST_SHOP in user_roles:
                shop_sub_auth_id = 'Shopping'
            else:
                return HttpResponseForbidden()

            shop_sub_auth = get_shop_sub_roles(shop_sub_auth_id)
            check_auth_instance = CheckForAuthorisations(user_roles, check_auth, shop_sub_auth)
            is_authorized = check_auth_instance.authorize_shop_and_shop_plus_views()
            if is_authorized:
                return view_method(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()

        return _arguments_wrapper
    return _method_wrapper


def authorize_view(check_auth):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            """
            Wrapper with arguments to invoke the method
            """
            if 'user_roles' in request.session:
                user_roles = request.session['user_roles']
            else:
                user_roles = update_user_roles_to_session(request)

            # If the document is opened from completion step it checks if the user as SHOP_ASSIST role
            if check_auth == CONST_MY_ORDER:
                if 'flag' in kwargs:
                    if kwargs['flag'] == 'True':
                        if CONST_SHOP_ASSIST in user_roles:
                            return view_method(request, *args, **kwargs)
                        else:
                            return HttpResponseForbidden()

            shop_sub_auth = get_all_auth_obj_groups(user_roles)

            check_auth_instance = CheckForAuthorisations(user_roles, check_auth, shop_sub_auth)
            is_authorized = check_auth_instance.authorize_shop_and_shop_plus_views()
            if is_authorized:
                return view_method(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()

        return _arguments_wrapper

    return _method_wrapper
