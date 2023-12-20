from django.urls import path
from .views import *

app_name = 'eProc_Manage_Content'

urlpatterns = [
    path('product_and_service_config', product_and_service_config, name='product_and_service_config'),
    path('catalog_config', catalog_config, name='catalog_config'),
    path('save_catalog_db', save_catalog_db, name='save_catalog_db'),
    path('get_assign_unassign_product', get_assign_unassign_product, name='get_assign_unassign_product'),
    path('assign_unassign_product_data', assign_unassign_product_data, name='assign_unassign_product_data'),
    path('generate_guid', generate_guid, name='generate_guid'),
    path('upload_catalog', upload_catalog, name='upload_catalog'),
    path('product_details/<str:product_id>/', get_product_details, name='get_product_details'),
    path('save_product_details_spec_images_eform', save_product_details_spec_images_eform, name='save_product_details_spec_images_eform'),
    path('upload_product_data', upload_product_data, name='upload_product_data'),
    path('check_product_detail', check_product_detail, name='check_product_detail'),
    path('activate_deactivate_catalog', activate_deactivate_catalog, name='activate_deactivate_catalog'),
    path('save_data_upload', save_data_upload, name='save_data_upload'),
    path('get_image_details', get_image_details, name='get_image_details'),
    path('delete_freetext_form/', delete_freetext_form, name='delete_freetext_form'),
    path('delete_product/', delete_product, name='delete_product'),
]
