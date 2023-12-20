from django.urls import path

from . import views

app_name = 'eProc_Purchase_Order'

urlpatterns = [
    path('my_order_doc_details/<encrypted_guid>', views.po_doc_details, name='po_doc_details'),
    path('po_pdf/<str:doc_number>/', views.generate_po_details_pdf, name='generate_po_details_pdf')
]