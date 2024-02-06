from django.urls import path
from . import views

app_name = 'eProc_Purchaser_Cockpit'

urlpatterns = [
    path('incomplete_form/<str:guid>', views.incomplete_form, name='incomplete_form'),
    path('sc_item_field_filter/', views.sc_item_field_filter, name='sc_item_field_filter'),
    path('rfq/', views.rfq_details, name='rfq_details'),
    path('generate_po/', views.generate_po, name='generate_po'),
    path('PO_grouping/', views.PO_grouping, name='PO_grouping'),
]