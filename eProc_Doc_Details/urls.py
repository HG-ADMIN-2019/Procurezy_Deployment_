# URL file for handling '/search' path (search app)

from django.urls import path
from . import views
from .views.details import proceed_checkout

app_name = 'eProc_Doc_Details'

# Defining the mapping between URLs and views
urlpatterns = [
    path('<str:flag>/<str:type>/<str:guid>/<mode>/<access_type>', views.docDetails, name='doc_details'),
    path('my_order_document_detail/<str:encrypt_sc_header_guid>/<access_type>', views.my_order_document_detail, name='my_order_document_detail'),
    path('my_order_doc_details/<str:flag>/<str:type>/<str:guid>/<mode>/<access_type>', views.my_order_doc_details, name='my_order_doc_details'),
    path('detail/popdf/attachments/download', views.downloadattach,  name='attach_download'),
    path('manager_popup', views.get_manager_data,  name='manager_popup'),
    path('update_sc', views.update_sc,  name='update_sc'),
    path('manger_detail', views.manger_detail,  name='manger_detail'),
    path('trigger_wf', views.trigger_wf,  name='trigger_wf'),
    path('get_highest_item', views.get_highest_item,  name='get_highest_item'),
    path('update_delivery_date', views.update_delivery_date, name='update_delivery_date'),
    path('delete_attachments/', views.delete_attachments, name='delete_attachments'),
    path('auto_complete_goods_receiver', views.auto_complete_goods_receiver, name='auto_complete_goods_receiver'),
    path('update_user_name', views.update_user_name, name='update_user_name'),
    path('update_saved_item/', views.update_saved_item, name='update_saved_item'),
    path('proceed_checkout/<str:encrypt_sc_header_guid>', proceed_checkout, name='proceed_checkout'),
]
