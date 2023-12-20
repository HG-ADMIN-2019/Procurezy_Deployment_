from django.urls import path
from . import views
from .views import create_update_application_data, create_update_delete_flags

app_name = 'eProc_Configuration'

urlpatterns = [
    path('', views.app_setting, name='app_setting'),
    path('latest', views.app_setting_latest, name='app_setting_latest'),
    path('data_upload_fk/', views.data_upload_fk, name='data_upload_fk'),
    path('check_data_fk/', views.check_data_fk, name='check_data_fk'),
    path('save_catalog_data/', views.save_catalog_data, name='save_catalog_data'),
    path('save_productservice_data/', views.save_productservice_data, name='save_productservice_data'),
    path('save_app_settings_data', views.save_app_settings_data, name='save_app_settings_data'),
    path('create_update_application_data', views.create_update_application_data, name='create_update_application_data'),
    path('create_update_delete_flags/', create_update_delete_flags, name='create_update_delete_flags'),
    path('get_holiday_from_calenderid', views.get_holiday_from_calenderid, name='get_holiday_from_calenderid'),
    path('basic_settings', views.basic_settings, name='basic_settings'),
    path('application_settings', views.application_data_configuration, name='application_data_configuration'),
    path('master_settings', views.master_data_configuration, name='master_data_configuration'),
    path('transaction_data_configuration', views.transaction_data_configuration, name='transaction_data_configuration'),
    # path('dropdown_document_type', views.dropdown_document_type, name='dropdown_document_type'),
    path('update_po_criteria_dropdown', views.update_po_criteria_dropdown, name='update_po_criteria_dropdown'),
    path('get_dropdown_data', views.get_dropdown_data, name='get_dropdown_data'),
]
