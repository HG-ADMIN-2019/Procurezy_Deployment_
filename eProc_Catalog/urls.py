from django.urls import path
from eProc_Catalog import views

app_name = 'eProc_Catalog'

# Defining the mapping between URLs and views
urlpatterns = [
     path('products_services/<str:catalog_id>/<str:document_number>', views.get_catalog_list, name='get_catalogs'),   # get static catalogues
     path('create_catalog/', views.create_catalog, name='create_catalog'),                 # create catalog
     path('app_catalogs_list', views.get_app_catalogs, name='app_catalogs_list'),          # get list of existing catlaogs in application settings
     path('catalogs_not_assigned', views.get_catalogs_not_used, name='catalogs_not_ass'),  # gets the list of catalogs which ara deleteable
     path('delete_catalogs/', views.delete_catalogs, name='delete_catalogs'),
     path('product_service_list', views.product_form_required_data, name='product_service_list'),
     path('add_product', views.add_product_or_service, name='add_product'),
     path('products_services/<str:selected_catalog>/<str:search_type>/<str:search_id>/<str:document_number>',
          views.get_products_services_on_select, name='select_prds_services'),
     path('catalogs/', views.get_all_catalogs, name='get_all_catalogs'),
     path('get_prod_details/', views.get_prod_details, name='get_prod_details'),
     path('get_product_service_prod_details/', views.get_product_service_prod_details, name='get_product_service_prod_details'),
     path('get_image_detail/', views.get_image_detail, name='get_image_detail'),
     path('auto_completion_search/', views.auto_completion_search, name='auto_completion_search'),
     # path('get_product_service_prod_details/<str:product_id>/<str:catalog_id>', views.get_product_service_product_details, name='get_product_service_product_details'),
     # path('get_search_result/<str:selected_catalog>/<str:document_number>', views.get_search_result, name='get_search_result'),


]
