from django.urls import path
from . import views

app_name = 'eProc_New_Client_Setup'
# Defining the mapping between URLs and views
urlpatterns = [

    path('new_client_setup/', views.new_client_setup, name='new_client_setup'),
    path('save_new_client/', views.save_new_client, name='save_new_client'),
    path('set_up_new_client/', views.set_up_new_client, name='set_up_new_client'),
    path('create_org_model/', views.create_org_model, name='create_org_model'),
    path('admin_authentication/', views.admin_authentication, name='admin_authentication'),
    path('new_client_user_registration/<str:client_id>/', views.new_client_user_registration,
         name='new_client_user_registration'),
    path('view_users/', views.view_users,
         name='view_users'),
    path('update_client_description/', views.update_client_description,name='update_client_description'),
    path('delete_client/', views.delete_client,name='delete_client'),


]
