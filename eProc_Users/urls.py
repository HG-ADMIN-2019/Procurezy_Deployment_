from django.urls import path

from .Utilities.user_generic import get_emp_data_onload
from .views import *


app_name = 'eProc_Users'

urlpatterns = [
    path('register_user/', register_page, name='register_page'),
    path('update_user_basic_details/', update_user_basic_details, name='update_user_basic_details'),
    path('get_emp_data_onload/', get_emp_data_onload, name='get_emp_data_onload'),
]
