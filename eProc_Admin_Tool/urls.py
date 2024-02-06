from django.urls import path
from . import views

# User story : SE10-15 - Admin Tools

# defines the app name sets the URL's to call the respective function
from .views import delete_user, lock_unlock_emp, get_username, delete_org_announcement

app_name = 'eProc_Admin_Tool'

urlpatterns = [
    path('', views.admin_tool, name='admin_tool'),
    path('employee_management/', views.user_search, name='employee_search'),
    path('delete_user/', delete_user, name='delete_user'),
    path('delete_org_announcement/', delete_org_announcement, name='delete_org_announcement'),
    path('lock_unlock_emp/', lock_unlock_emp, name='lock_unlock_emp'),
    path('get_username/', get_username, name='get_username'),
    path('supplier_management/', views.supplier_search, name='supplier_search'),
    path('employee_management/user_details/<str:email>/', views.user_details, name='user_details_page'),
    path('supplier_management/supplier_details/<str:supplier_id>/', views.sup_details, name='sup_details_page'),
    path('admin_report/users', views.user_report, name='user_report'),  # reports_main page
    path('admin_report/approvals', views.approval_report, name='approval_report'),  # approval report_main page
    path('admin_report/documents', views.m_docsearch_meth, name='doc_search_report'),  # Search page
    path('admin_report/account_assignment_categories', views.accnt_report, name='accnt_report'),
    # accounting report_main page
    path('org_announcements/', views.org_announcements_search, name='org_announcements_search'),
    path('org_announcement_details/<str:announcement_guid>/', views.org_announcement_details, name='org_announcement_details'),
    path('extract_employee_template', views.extract_employee_template, name='extract_employee_template'),
    path('extract_supplier_template', views.extract_supplier_template, name='extract_supplier_template'),
    path('admin_report/get_acct_report', views.get_acct_report, name='get_acct_report'),
    path('application_monitoring/documents', views.application_monitoring, name='application_monitoring'),
    path('application_monitoring/emails', views.email_user_monitoring, name='email_user_monitoring'),
    path('check_resend', views.check_resend, name='check_resend'),
    path('clear_filter', views.clear_filter_data, name='clear_filter'),
]
