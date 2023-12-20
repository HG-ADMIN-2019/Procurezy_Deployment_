from django.urls import path
from eProc_Supplier_Order_Management.views.supplier_order_management_views import *
from . import views
app_name = 'eProc_Supplier_Order_Management'
# Defining the mapping between URLs and views
urlpatterns = [
    path('po_extract', po_extract, name='po_extract'),
    path('my_order_doc_details/<encrypted_guid>', views.som_po_detail, name='som_po_doc_details'),
    path('upload_som', upload_som, name='upload_som'),
]