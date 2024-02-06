from django.urls import path
from . import views

app_name = 'eProc_Configuration_Check'

urlpatterns = [

    path('check_cust_unspsc_category_desc',views.check_cust_unspsc_category_desc,name='check_cust_unspsc_category_desc'),
    path('check_cust_unspsc_category',views.check_cust_unspsc_category,name='check_cust_unspsc_category'),
    path('check_acc_assign_desc',views.check_acc_assign_desc,name='check_acc_assign_desc'),
    path('check_acc_assign_values',views.check_acc_assign_values,name='check_acc_assign_values'),
    path('check_gl_acc_data',views.check_gl_acc_data,name='check_gl_acc_data'),
    path('check_company', views.check_company, name='check_company'),
    path('check_purchaseorg', views.check_purchaseorg, name='check_purchaseorg'),
    path('check_purchasegrp', views.check_purchasegrp, name='check_purchasegrp'),
    path('check_approvaltype', views.check_approvaltype, name='check_approvaltype'),
    path('check_workflowschema', views.check_workflowschema, name='check_workflowschema'),
    path('check_spendlimit_value', views.check_spendlimit_value, name='check_spendlimit_value'),
    path('check_spending_limit', views.check_spending_limit, name='check_spending_limit'),
    path('check_approvlimit_value', views.check_approvlimit_value, name='check_approvlimit_value'),
    path('check_approv_limit', views.check_approv_limit, name='check_approv_limit'),
    path('check_workflow_acc', views.check_workflow_acc, name='check_workflow_acc'),
    path('check_address_types', views.check_address_types, name='check_address_types'),
    path('check_address', views.check_address, name='check_address'),
    path('check_inco_terms', views.check_inco_terms, name='check_inco_terms'),
    path('check_paymentterm_desc', views.check_paymentterm_desc, name='check_paymentterm_desc'),
    path('check_country', views.check_country, name='check_country'),
    path('check_currency', views.check_currency, name='check_currency'),
    path('check_language', views.check_language, name='check_language'),
    path('check_UOM', views.check_UOM, name='check_UOM'),
    path('check_Timezone', views.check_Timezone, name='check_Timezone'),
    path('check_Employee', views.check_Employee, name='check_Employee')

]
