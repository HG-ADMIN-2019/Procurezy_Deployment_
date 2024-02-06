from eProc_Attributes.Utilities.attributes_generic import OrgAttributeValues
from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import *
from eProc_Configuration.models.development_data import AuthorizationObject, AuthorizationGroup
from eProc_Registration.models import *
from eProc_Shopping_Cart.models import CartItemDetails
from eProc_Suppliers.models import OrgSuppliers
from eProc_User_Settings.Utilities.user_settings_generic import get_object_id_list_user

django_query_instance = DjangoQueries()


def getClients(request):
    client = request.user.client
    return client


def getUserEmailId(request):
    email_id = request.user.email
    return email_id


# To get username for logged in user
def getUsername(request):
    username = request.user.username
    return username


# To get logged in user's object id
def get_login_obj_id(request):
    """
    :param request:
    :return:
    """
    username_object_id = 0
    if request.user.object_id_id:
        username_object_id = request.user.object_id_id
    return username_object_id


def get_user_id_by_email_id(email_id):
    """
    :param email_id:
    :return:
    """
    user_name = django_query_instance.django_filter_value_list_query(UserData, {'email': email_id}, 'username')[0]
    return user_name


# To get total number of items in cart based on user info
def display_cart_counter(username):
    """
    :param username: User info
    :return: Total number of available items in a cart
    """
    return django_query_instance.django_filter_count_query(CartItemDetails, {
        'username': username, 'client': global_variables.GLOBAL_CLIENT
    })


def get_user_currency(request):
    """
    login user currency
    :param request:
    :return:
    """
    return request.user.currency_id_id


def get_user_language(request):
    """
    login user currency
    :param request:
    :return:
    """
    return request.user.language_id


def get_user_timezone(request):
    """
    login user currency
    :param request:
    :return:
    """
    return request.user.time_zone


def get_requester_currency(requester_user_name):
    """
    get requester currency from mum user info
    :param requester_user_name:
    :return:
    """
    currency_id = ''
    if requester_user_name:
        try:
            currency_id = django_query_instance.django_filter_value_list_query(UserData, {
                'username': requester_user_name, 'client': global_variables.GLOBAL_CLIENT
            }, 'currency_id')[0]
        except ValueError:
            currency_id = None

    return currency_id


def update_requester_info(requester_user_name):
    """

    """
    global_variables.GLOBAL_REQUESTER_CURRENCY = get_requester_currency(requester_user_name)
    global_variables.GLOBAL_REQUESTER_LANGUAGE = requester_field_info(requester_user_name, 'language_id')
    global_variables.GLOBAL_REQUESTER_OBJECT_ID = requester_field_info(requester_user_name, 'object_id')


def requester_field_info(requester_user_name, field_name):
    """

    """
    # client = global_variables.GLOBAL_CLIENT field_detail = (list(UserData.objects.filter(
    # username=requester_user_name, client=client).values_list(field_name, flat=True)))[0]

    try:
        client = global_variables.GLOBAL_CLIENT
        field_detail = \
            (list(UserData.objects.filter(username=requester_user_name, client=client).values_list(field_name,
                                                                                                   flat=True)))[
                0]
    except:
        field_detail = None

    return field_detail


def get_country_id():
    return django_query_instance.django_filter_value_list_query(Country, {'del_ind': False}, 'country_code')


def get_currency_list():
    return django_query_instance.django_filter_value_list_query(Currency, {'del_ind': False}, 'currency_id')


def get_registered_org_suppliers(client):
    registered_org_suppliers = []
    get_suppliers_from_master = django_query_instance.django_filter_value_list_query(SupplierMaster, {'client': client,
                                                                                                      'del_ind': False},
                                                                                     'supplier_id')

    for supplier in get_suppliers_from_master:
        if django_query_instance.django_existence_check(OrgSuppliers, {'supplier_id': supplier,
                                                                       'client': client, 'del_ind': False}):
            registered_org_suppliers.append(supplier)

    return registered_org_suppliers


def get_currency_data():
    return django_query_instance.django_filter_query(Currency, {'del_ind': False}, None, ['currency_id', 'description'])


def get_country_data():
    return django_query_instance.django_filter_query(Country, {'del_ind': False}, None,
                                                     ['country_code', 'country_name'])


def get_login_user_roles_by_obj_id(object_id):
    client = global_variables.GLOBAL_CLIENT
    object_id_list = get_object_id_list_user(client, object_id)
    user_role = OrgAttributeValues.get_user_attr_value_list_by_attr_id(object_id_list, CONST_US_ROLE)

    return list(user_role)


def update_user_roles_to_session(request):
    user_roles = get_login_user_roles_by_obj_id(global_variables.GLOBAL_LOGIN_USER_OBJ_ID)
    request.session['user_roles'] = user_roles
    return user_roles


get_auth_grp_desc = {
    CONST_SHOP: 'Shopping',
    CONST_SHOP_PLUS: 'Shopping Plus',
    CONST_SHOP_MANAGER: 'Approvals',
    CONST_SHOP_ASSIST: 'Shopper Assist',
    CONST_SHOP_PURCHASER: 'Purchaser',
    CONST_SHOP_ADMIN: 'Admin'
}


def get_shop_sub_roles(auth_grp_desc):
    """
    """

    shop_auth = django_query_instance.django_filter_value_list_query(AuthorizationGroup,
                                                                     {'auth_grp_desc': auth_grp_desc, 'del_ind': False},
                                                                     'auth_obj_id')

    shop_sub_auth = django_query_instance.django_filter_value_list_query(AuthorizationObject,
                                                                         {'auth_obj_id__in': shop_auth,
                                                                          'del_ind': False}, 'auth_level_ID')

    return shop_sub_auth


def get_all_auth_obj_groups(user_roles):
    auth_group_list = []
    for role in user_roles:
        if role == CONST_SHOP:
            auth_grp_desc = get_auth_grp_desc[CONST_SHOP]

        elif role == CONST_SHOP_PLUS:
            auth_grp_desc = get_auth_grp_desc[CONST_SHOP_PLUS]

        elif role == CONST_SHOP_MANAGER:
            auth_grp_desc = get_auth_grp_desc[CONST_SHOP_MANAGER]

        elif role == CONST_SHOP_ASSIST:
            auth_grp_desc = get_auth_grp_desc[CONST_SHOP_ASSIST]

        elif role == CONST_SHOP_PURCHASER:
            auth_grp_desc = get_auth_grp_desc[CONST_SHOP_PURCHASER]

        else:
            auth_grp_desc = get_auth_grp_desc[CONST_SHOP_ADMIN]

        shop_sub_auth = get_shop_sub_roles(auth_grp_desc)

        auth_group_list = list(set(auth_group_list + shop_sub_auth))

    return auth_group_list


def get_object_id_from_username(username):
    user_data = django_query_instance.django_get_query(UserData, {
        'username': username, 'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
    })

    if user_data is not None:
        return user_data.object_id_id

    return user_data


def get_user_info(username):
    if username:
        user_data = django_query_instance.django_get_query(UserData, {
            'username': username, 'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
        })

        return user_data


def get_super_user_detail_based_on_client(client):
    """

    """
    user_data = django_query_instance.django_filter_query(UserData,
                                                          {'client': client,
                                                           'del_ind': False,
                                                           'is_superuser': True}, ['username'], None)

    return user_data
