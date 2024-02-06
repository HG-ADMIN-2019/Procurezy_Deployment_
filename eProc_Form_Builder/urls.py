from django.urls import path
from .views import *

app_name = 'eProc_Form_Builder'

urlpatterns = [
    path('create-freetext/<str:freetext_id>/', create_or_update_freetext_form, name='create-freetext'),
    path('display-freetext-forms/', display_freetext_forms, name="display-freetext-forms"),
    path('create_update_freetext_form/', create_update_freetext_form, name='create_update_freetext_form'),
    # path('update-freetext-form/', display_fields_to_update, name='update-freetext-form'),
]
