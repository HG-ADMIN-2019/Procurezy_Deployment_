from django.urls import path
from . import views

app_name = 'eProc_Attributes'

urlpatterns = [
    path('org_attr', views.org_attributes, name='org_attr'),
    path('delete_popup/<int:pk>', views.delete_popup, name='delete_popup'),
    path('dropdown_list', views.dropdown_list, name='dropdown_list'),
    path('update_popup', views.update_popup, name='update_popup'),
    path('save_table', views.save_table, name='save_table'),
    path('save_deleted_attr', views.save_deleted_attr, name='save_deleted_attr'),
    path('attr_id_list', views.attr_id_list, name='attr_id_list'),
    path('extended_attr', views.extended_attr, name='extended_attr'),
    path('save_ext_attr', views.save_ext_attr, name='save_ext_attr'),
    path('save_porg_company_id', views.save_porg_company_id, name='save_porg_company_id'),

]