from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from eProc_Notes_Attachments.views import *

app_name = 'eProc_Notes_Attachments'

urlpatterns = [
    path('attachments/', attach_list, name='attachments'),
    path('attachments/upload', upload_attach, name='upload_attach'),  # urls to add attachments and retrieve attachments
    path('notes/', add_notes, name='notes'),
    path('detail/popdf/<str:guid>', attachmentspage, name='attach_page'),  # Attachments page
    path('detail/popdf/attachments', attach, name='downloadattach'),                        # Download PDF
    path('detail/popdf/attachments/download', downloadattach,  name='attach_download'),     # Download attachments
]

# Start of SC-PR-US13
# These lines of code creates dynamic url for attachments

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# End of SC-PR-US13
