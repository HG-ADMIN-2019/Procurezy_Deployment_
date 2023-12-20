from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Configuration.models import *


django_query_instance = DjangoQueries()


# def get_attachments_info(context, client):
#     attachment_extension = []
#     if django_query_instance.django_existence_check(SystemSettings, {'client': client}):
#         system_settings = django_query_instance.django_get_query(SystemSettings, {'client': client})
#         for extensions in system_settings.attachent_extension.split(','):
#             attachment_extension.append(extensions)
#         context['attachment_size'] = system_settings.attachment_size
#         context['attachment_extension'] = attachment_extension
#     return context
