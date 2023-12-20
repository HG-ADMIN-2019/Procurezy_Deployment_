from django.urls import path
from .import views

app_name = 'eProc_Generate_PDF'

urlpatterns = [

    path('', views.render_pdf_view, name='render_pdf_view'),
]