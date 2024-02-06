from django.urls import path

from . import views


app_name = 'eProc_Org_Support'

urlpatterns = [
    path('org_announcement_save/', views.org_announcement_save, name='org_announcement_save'),
    path('update_org_announcement_details/', views.update_org_announcement_details, name='update_org_announcement_details'),
    path('org_support_save/', views.org_support_save, name='org_support_save'),
    path('get_support_data/', views.get_support_data, name='get_support_data'),
    path('org_support_config/', views.org_support_config, name='org_support_config'),
    path('update_org_support_details/', views.update_org_support_details, name='update_org_support_details'),
    path('customer_support_chat/', views.customer_support_chat, name='customer_support_chat'),
    path('delete_table_row/', views.delete_table_row, name='delete_table_row'),
    path('active_inactive_org/', views.active_inactive_org, name='active_inactive_org'),
]