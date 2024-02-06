from django.urls import path
from . import views


app_name = 'eProc_Account_Assignment'

urlpatterns = [
    path('change_acc_assignment_cat/', views.change_acc_assignment_cat, name='change_acc_assignment_cat'),
    path('gl_acc_detail/', views.gl_acc_detail, name='gl_acc_detail'),
    path('search_acc_value/', views.search_acc_value, name='search_acc_value'),

]
