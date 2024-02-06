from django.urls import path
from . import views

app_name = 'eProc_Doc_Search'
urlpatterns = [
    path('get_sc_app_data', views.get_sc_app_data, name='get_sc_app_data'),
    path('sc_pdf/<str:doc_number>/', views.generate_sc_details_pdf, name='generate_sc_details_pdf'),
]
