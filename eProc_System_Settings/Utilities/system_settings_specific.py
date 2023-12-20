"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    system_settings_specific.py
Usage:
   saves the system settings from UI
     sys_attributes: gets the respective attribute values for the logged in client and used to integrate them n respective functionality.
Author:
    Soni Vydyula
"""

from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Configuration.models import SystemSettings, SystemAttrValues
from eProc_System_Settings.System_Settings_forms.system_settings_form import SystemSettingsForm


# class attributes:
#     def __init__(self, client, request):
#         self.client = client
#
#         self.sys_attr = SystemSettings.objects.filter(client=client).exists()
#         pwd_policy = []
#         login_attempts = []
#         session_timeout = []
#         msg_display = []
#         theme_color = []
#         pagination_count = []
#         attachment_size = []
#         attachment_extension = []
#         form_data = ''
#         attribute_values = SystemAttrValues.objects.filter().values('pwd_policy', 'login_attempts', 'session_timeout',
#                                                                     'msg_display',
#                                                                     'theme_color', 'pagination_count',
#                                                                     'attachment_size',
#                                                                     'attachment_extension')
#         if attribute_values.count() == 0:
#             attribute = None
#         else:
#             attribute = attribute_values
#         for pwd in attribute_values:
#             pwd_policy.append(pwd['pwd_policy'])
#             login_attempts.append(pwd['login_attempts'])
#             session_timeout.append(pwd['session_timeout'])
#             msg_display.append(pwd['msg_display'])
#             theme_color.append(pwd['theme_color'])
#             pagination_count.append(pwd['pagination_count'])
#             attachment_size.append(pwd['attachment_size'])
#             attachment_extension.append(pwd['attachment_extension'])
#
#         if self.sys_attr:
#             form_data = SystemSettings.objects.get(client=request.user.client_id)
#             if str(form_data.pwd_policy) in pwd_policy:
#                 pwd_policy.remove(str(form_data.pwd_policy))
#             pwd_policy.insert(0, form_data.pwd_policy)
#             login_attempts.remove(int(form_data.login_attempts))
#             login_attempts.insert(0, form_data.login_attempts)
#             session_timeout.remove(int(form_data.session_timeout))
#             session_timeout.insert(0, form_data.session_timeout)
#             msg_display.remove(int(form_data.msg_display))
#             msg_display.insert(0, form_data.msg_display)
#             theme_color.remove(str(form_data.theme_color))
#             theme_color.insert(0, form_data.theme_color)
#             pagination_count.remove(int(form_data.pagination_count))
#             pagination_count.insert(0, form_data.pagination_count)
#             attachment_size.remove(int(form_data.attachment_size))
#             attachment_size.insert(0, form_data.attachment_size)
#             if str(form_data.attachent_extension) in attachment_extension:
#                 attachent_extension = form_data.attachent_extension
#             if form_data.attachent_extension in attachment_extension:
#                 attachment_extension.remove(str(form_data.attachent_extension))
#             attachment_extension.insert(0, form_data.attachent_extension)
#             # Removes the None values if present in list
#             pwd_policy = list(filter(None, pwd_policy))
#             login_attempts = list(filter(None, login_attempts))
#             session_timeout = list(filter(None, session_timeout))
#             msg_display = list(filter(None, msg_display))
#             theme_color = list(filter(None, theme_color))
#             pagination_count = list(filter(None, pagination_count))
#             attachment_size = list(filter(None, attachment_size))
#             attachment_extension = list(filter(None, attachment_extension))
#         else:
#             pwd_policy = list(filter(None, pwd_policy))
#             login_attempts = list(filter(None, login_attempts))
#             session_timeout = list(filter(None, session_timeout))
#             msg_display = list(filter(None, msg_display))
#             theme_color = list(filter(None, theme_color))
#             pagination_count = list(filter(None, pagination_count))
#             attachment_size = list(filter(None, attachment_size))
#             attachment_extension = list(filter(None, attachment_extension))
#         self.pwd_policy = pwd_policy
#         self.login_attempts = login_attempts
#         self.session_timeout = session_timeout
#         self.msg_display = msg_display
#         self.theme_color = theme_color
#         self.pagination_count = pagination_count
#         self.attachment_size = attachment_size
#         self.attachment_extension = attachment_extension
#         self.attribute = attribute
#         self.form_data = form_data
