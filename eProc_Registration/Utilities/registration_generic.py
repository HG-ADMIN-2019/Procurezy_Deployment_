import datetime

from django.http import JsonResponse

from eProc_Basic.Utilities.constants.constants import CONST_SUPPLIER_IMAGE_TYPE
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import encrypt
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.image_type_funtions import get_image_type
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG190, MSG191, MSG177
from eProc_Configuration.models import OrgClients, ImagesUpload, SupplierMaster, Country, Currency, Languages

JsonParser_obj = JsonParser()
django_query_instance = DjangoQueries()


def save_supplier_image(supplier_file, supplier_id, supplier_image_name):
    image_type = get_image_type(CONST_SUPPLIER_IMAGE_TYPE)
    client = global_variables.GLOBAL_CLIENT
    if image_type:
        if django_query_instance.django_existence_check(ImagesUpload, {
            'image_id': supplier_id,
            'client': client,
            'image_type': image_type
        }):

            supplier_image_guid = django_query_instance.django_filter_value_list_query(ImagesUpload, {
                'image_id': supplier_id, 'client': client, 'image_type': image_type
            }, 'images_upload_guid')

            for image_guid in supplier_image_guid:
                django_query_instance.django_get_query(ImagesUpload,
                                                       {'images_upload_guid': image_guid}).image_url.delete(save=True)
                django_query_instance.django_get_query(ImagesUpload, {'images_upload_guid': image_guid}).delete()

    django_query_instance.django_create_query(ImagesUpload, {
        'images_upload_guid': guid_generator(),
        'client': django_query_instance.django_get_query(OrgClients, {'client': client}),
        'image_id': supplier_id,
        'image_url': supplier_file,
        'image_name': supplier_image_name,
        'image_default': True,
        'image_type': CONST_SUPPLIER_IMAGE_TYPE,
        'created_at': datetime.date.today(),
        'created_by': global_variables.GLOBAL_LOGIN_USERNAME
    })


def save_supplier_data(request):
    """

    """
    message = {}
    update_supplier_guid = ''
    supplier_details = {}
    status = request.POST.get('status')
    supplier_details['supplier_id'] = request.POST.get('supplier_id')
    supplier_details['supp_type'] = request.POST.get('supplier_type')
    supplier_details['registration_number'] = request.POST.get('registration_number')
    supplier_details['name1'] = request.POST.get('name1')
    supplier_details['name2'] = request.POST.get('name2')
    supplier_details['language_id'] = request.POST.get('language_id')
    supplier_details['city'] = request.POST.get('city_id')
    supplier_details['postal_code'] = request.POST.get('postal_code_id')
    supplier_details['street'] = request.POST.get('street_id')
    supplier_details['country_code'] = request.POST.get('country_code_id')
    supplier_details['currency_id'] = request.POST.get('currency_id')
    supplier_details['landline'] = request.POST.get('landline_id')
    supplier_details['mobile_num'] = request.POST.get('mobile_num_id')
    supplier_details['fax'] = request.POST.get('fax_id')
    supplier_details['email'] = request.POST.get('email_id')
    supplier_details['search_term1'] = request.POST.get('search_term1_id')
    supplier_details['search_term2'] = request.POST.get('search_term2_id')
    supplier_details['delivery_days'] = request.POST.get('working_days_id')
    supplier_details['duns_number'] = request.POST.get('duns_number_id')
    supplier_details['output_medium'] = request.POST.get('output_medium_id')
    encrypted_supp = encrypt(supplier_details['supplier_id'])
    if status in ['UPDATE', 'update']:
        if django_query_instance.django_existence_check(SupplierMaster,
                                                        {'supplier_id': supplier_details['supplier_id'],
                                                         'client': global_variables.GLOBAL_CLIENT,
                                                         'del_ind': False}):
            django_query_instance.django_update_query(SupplierMaster,
                                                      {'supplier_id': supplier_details['supplier_id'],
                                                       'client': global_variables.GLOBAL_CLIENT,
                                                       'del_ind': False}, supplier_details)
            msgid = 'MSG177'
            error_msg = get_message_desc(msgid)[1]

            message['type'] = 'success'
            return error_msg, encrypted_supp, message
    else:
        if django_query_instance.django_existence_check(SupplierMaster,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'supplier_id': supplier_details['supplier_id'],
                                                         'del_ind': False}):
            msgid = 'MSG190'
            error_msg = get_message_desc(msgid)[1]

            message['type'] = 'error'
            return error_msg, encrypted_supp, message
        elif django_query_instance.django_existence_check(SupplierMaster,
                                                          {'client': global_variables.GLOBAL_CLIENT,
                                                           'registration_number': supplier_details[
                                                               'registration_number'],
                                                           'del_ind': False}):
            msgid = 'MSG191'
            error_msg = get_message_desc(msgid)[1]

            message['type'] = 'error'
            return error_msg, encrypted_supp, message
        elif django_query_instance.django_existence_check(SupplierMaster,
                                                          {'client': global_variables.GLOBAL_CLIENT,
                                                           'email': supplier_details[
                                                               'email'],
                                                           'del_ind': False}):
            msgid = 'MSG0121'
            error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            error_msg = 'Supplier Email Already Exists'
            message['type'] = 'error'
            return error_msg, encrypted_supp, message
        else:
            supplier_details['supp_guid'] = guid_generator()
            supplier_details['client'] = global_variables.GLOBAL_CLIENT
            supplier_details['country_code'] = django_query_instance.django_get_query(Country, {
                'country_code': supplier_details['country_code']})
            supplier_details['currency_id'] = django_query_instance.django_get_query(Currency, {
                'currency_id': supplier_details['currency_id']})
            supplier_details['language_id'] = django_query_instance.django_get_query(Languages, {
                'language_id': supplier_details['language_id']})
            django_query_instance.django_create_query(SupplierMaster,
                                                      supplier_details)
            msgid = 'MSG177'
            error_msg = get_message_desc(msgid)[1]
            message['type'] = 'success'

    return error_msg, encrypted_supp, message
