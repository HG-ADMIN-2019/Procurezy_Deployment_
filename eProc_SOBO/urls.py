from django.urls import path
from .views import *

app_name = 'eProc_SOBO'

urlpatterns = [
    path('get_sobo_users/', get_sobo_users, name='get_sobo_users')
]
