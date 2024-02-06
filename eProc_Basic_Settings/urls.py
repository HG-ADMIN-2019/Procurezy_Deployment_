from django.urls import path
from .views import *
from .views.basic_settings import check_data, upload_countries

app_name = 'eProc_Basic_Settings'

urlpatterns = [
    path('export', extract_country_data, name='extract_country_data'),
    path('extract_country_template', extract_country_template, name='extract_country_template'),
    path('extract_client_data', extract_client_data, name='extract_client_data'),
    path('extract_document_data', extract_document_data, name='extract_document_data'),
    path('extract_calendar_data', extract_calendar_data, name='extract_calendar_data'),
    path('extract_calendar_holiday_data', extract_calendar_holiday_data, name='extract_calendar_holiday_data'),
    path('export_product_category', extract_product_category_data, name='extract_product_category_data'),
    path('export_languages', extract_language_data, name='extract_language_data'),
    path('extract_language_template', extract_language_template, name='extract_language_template'),
    path('export_currency', extract_currency_data, name='extract_currency_data'),
    path('read_pdf', read_pdf, name='read_pdf'),
    path('srm_currency_converter_p02', srm_currency_converter_p02, name='srm_currency_converter_p02'),
    path('srm_currency_converter_e7p', srm_currency_converter_e7p, name='srm_currency_converter_e7p'),
    path('Scheduling', Scheduling, name='Scheduling'),
    path('stop_job', stop_job, name='stop_job'),


    path('work_item_extract', work_item_extract, name='work_item_extract'),
    path('work_item_doc_num_extract', work_item_doc_num_extract, name='work_item_doc_num_extract'),

    path('export_timezone_data', extract_timezone_data, name='extract_timezone_data'),
    path('extract_timezone_template', extract_timezone_template, name='extract_timezone_template'),
    path('extract_currency_template', extract_currency_template, name='extract_currency_template'),
    path('export_unitofmeasure', extract_unitofmeasure_data, name='extract_unitofmeasure_data'),
    path('extract_unitofmeasure_template', extract_unitofmeasure_template, name='extract_unitofmeasure_template'),
    path('export_product_details', extract_product_details, name='extract_product_details'),
    path('download_product_template', download_product_template, name='download_product_template'),
    path('export_emp', extract_employee_data, name='extract_employee_data'),
    path('export_supplier', extract_supplier_data, name='extract_supplier_data'),
    path('countries/', upload_countries, name='upload_countries'),
    path('data_upload/', data_upload, name='data_upload'),
    path('check_data/', check_data, name='check_data'),
    path('currencies/', upload_currencies, name='upload_currencies'),
    path('srm_currency/', srm_currency, name='srm_currency'),
    path('languages/', upload_languages, name='upload_languages'),
    path('timezones/', upload_timezone, name='upload_timezone'),
    path('unit_of_measures/', upload_unit_of_measure, name='upload_unit_of_measure'),
    path('upload_data_display', upload_data_display, name='upload_data_display'),
    path('ACC_values', account_ass_values, name='account_ass_values'),
    path('purch_Cockpit', purch_Cockpit, name='purch_Cockpit'),
    path('save_basic_data', save_basic_data, name='save_basic_data'),
    path('create_update_basic_data', create_update_basic_data, name='create_update_basic_data'),

]
