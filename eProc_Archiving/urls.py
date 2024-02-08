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
    path('detail/popdf/attachments/download', views.arch_downloadattach, name='attach_download1'),  # Download attachments


]
