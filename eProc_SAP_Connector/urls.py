from django.urls import path
from . import views

app_name = 'eProc_SAP_Connector'

# Defining the mapping between URLs and views
urlpatterns = [
     path('get_sap_connect/', views.get_sap_connect, name='get_sap_connect'),
     path('create_connection/', views.create_connection, name='create_connection'),
     path('get_connection/',views.get_connection,name='get_connection'),
     path('delete_connections/',views.delete_connections,name='delete_connections'),
     path('Connections/',views.Connections,name='Connections'),
    ]