from django.urls import path
from .views import *

app_name = 'eProc_Suppliers'

urlpatterns = [
    path('update_suppliers_basic_details/', update_suppliers_basic_details,
         name='update_suppliers_basic_details'),
    path('update_supplier_purch_details/', update_supplier_purch_details, name='update_supplier_purch_details'),
    path('supplier_register/', supplier_registration_form, name='supplier_registration'),
    path('delete_supplier/', delete_supplier, name='delete_supplier'),
    path('supplier_blocking/', supplier_blocking, name='supplier_blocking'),
    path('delete_supplier_org_info/', delete_supplier_org_info, name='delete_supplier_org_info'),
    path('get_supp_org_dropdown/', get_supp_org_dropdown, name='get_supp_org_dropdown'),
]

