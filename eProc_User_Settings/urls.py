from django.urls import path
from . import views

app_name = 'eProc_User_Settings'

urlpatterns = [
    path('purchase_settings/', views.purchase_settings, name='purchase_settings'),       # User setting url
    path('personal_settings_edit/', views.personal_settings_edit, name='personal_settings') ,#Personal settings url
    path('personal_settings_display/', views.personal_settings_display, name='personal_settings_display'), #Personal settings url
    path('save_purchase_settings/', views.save_purchase_settings, name='save_purchase_settings'),       # User setting url
    path('get_porg_pgrp/', views.get_porg_pgrp, name='get_porg_pgrp'),
]