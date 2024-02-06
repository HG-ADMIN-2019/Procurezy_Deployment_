from django.urls import path
from . import views

app_name = 'eProc_Generate_OTP'

urlpatterns = [
    path('generate_otp', views.generate_otp, name='generate_otp'),
    path('reset_otp/', views.reset_otp, name='reset_otp'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('otp_verification_views/', views.otp_verification_views, name='otp_verification_views'),
]