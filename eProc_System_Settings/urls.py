# Urls for the functions in system settings app
from django.urls import path
from eProc_System_Settings.views import system_settings

app_name = 'eProc_System_Settings'

urlpatterns = [
    # path('settings/', system_settings.system_settings, name='settings'),
    path('system_settings/', system_settings.system_settings_new, name='system_settings_new'),
]