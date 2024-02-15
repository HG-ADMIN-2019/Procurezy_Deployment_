# URL file for handling '/search' path (search app)

from django.urls import path
from . import views

app_name = 'eProc_Archiving'

# Defining the mapping between URLs and views
urlpatterns = [
    path('', views.docsearch, name='docsearch'),                                             # Search page
    path('Archiving/detail/<str:type>/<str:guid>/', views.m_det_meth, name='doc_details'),                   # Details page
    path('detail/popdf/<str:guid>', views.arch_attachmentspage, name='attach_page'),  # Attachments page
    path('document_info/<str:doc_type>/<str:doc_number>', views.get_doc_det_by_doc_num, name='document_info'),
    path('detail/popdf/attachments/download', views.arch_downloadattach, name='attach_download1'),# Download attachments
    path('data_upload/', views.data_upload, name='data_upload'),
    path('upload_sc/', views.upload_sc, name='upload_sc'),
    path('upload_po/', views.upload_po, name='upload_po'),
    path('upload_confirmation/', views.upload_confirmation, name='upload_confirmation'),
    path('upload_user/', views.upload_user, name='upload_user'),
    path('upload_supplier_master/', views.upload_supplier_master, name='upload_supplier_master'),
    path('upload_country_cocode/', views.upload_country_cocode, name='upload_country_cocode'),
    path('upload_country/', views.upload_country, name='upload_country'),
    path('upload_cocode/', views.upload_cocode, name='upload_cocode'),


]
