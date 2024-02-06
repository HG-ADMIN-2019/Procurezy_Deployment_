from django.urls import path

from .Utilities.functions.messages_config import get_message_description
from .views import *

app_name = 'eProc_Basic'

urlpatterns = [
    path('private_policy', private_policies, name='private_policy'),
    path('terms_of_use', terms_of_use, name='terms_of_use'),
    path('get_message_description', get_message_description, name='get_message_description'),
]
