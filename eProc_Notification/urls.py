from django.urls import path
from . import views

app_name = 'eProc_Notification'

urlpatterns = [
    path('get_notification_detail/', views.get_notification_detail, name="get_notification_detail"),
    path('update_read_status/', views.update_read_status, name="update_read_status"),
    path('set_notification_important/', views.set_notification_important, name="set_notification_important"),
    path('delete_notification/', views.delete_notification, name="delete_notification")

]