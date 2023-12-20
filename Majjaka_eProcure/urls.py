"""Majjaka_eProcure URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# URL file for handling search and users app path

# Importing Django standard library
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Defining the mapping between URLs and views
urlpatterns = [
    path('admin/', admin.site.urls),                                    # Admin page
    path('', include('eProc_Login.urls')),
    path('', include('django.contrib.auth.urls')),                      # Forgot password urls
    path('upload/', include('eProc_Upload.urls')),                      # Upload SC PO data
    path('shop/', include('eProc_Shopping_Cart.urls'), name='shop'),
    path('notes_attachments/', include('eProc_Notes_Attachments.urls')),
    path('search/', include('eProc_Doc_Search.urls')),
    path('doc_details/', include('eProc_Doc_Details.urls')),
    path('usersettings/', include('eProc_User_Settings.urls'), name='usersettings'),
    path('register/', include('eProc_Registration.urls')),
    path('Reports/', include('eProc_Reports.urls')),
    path('Rfq/', include('eProc_Rfq.urls')),
    path('admin_tool/', include('eProc_Admin_Tool.urls')),
    path('org_model/', include('eProc_Org_Model.urls')),
    path('eProc_User_Admin/', include('eProc_User_Admin.urls')),
    path('system_setting/', include('eProc_System_Settings.urls')),
    path('attributes/', include('eProc_Attributes.urls')),
    path('configuration/', include('eProc_Configuration.urls')),
    path('purchaser_cockpit/', include('eProc_Purchaser_Cockpit.urls'), name='purchaser_cockpit'),
    path('shop/', include('eProc_Catalog.urls')),
    path('workflow/', include('eProc_Workflow.urls'), name='workflow'),
    path('connector/', include('eProc_SAP_Connector.urls')),
    path('generate_pdf/', include('eProc_Generate_PDF.urls')),
    path('configure-freetext/', include('eProc_Form_Builder.urls')),
    path('notification/', include('eProc_Notification.urls')),
    path('chat/', include('eProc_Chat.urls')),
    path('sobo/', include('eProc_SOBO.urls')),
    path('account_assignment/', include('eProc_Account_Assignment.urls')),
    path('home/', include('eProc_Shop_Home.urls')),
    path('add_item/', include('eProc_Add_Item.urls')),
    path('support/', include('eProc_Org_Support.urls')),
    path('search/', include('eProc_Doc_Search_and_Display.urls')),
    path('users/', include('eProc_Users.urls')),
    path('suppliers/', include('eProc_Suppliers.urls')),
    path('manage-content/', include('eProc_Manage_Content.urls')),
    path('emails/', include('eProc_Emails.urls')),
    path('configuration/basic_settings/', include('eProc_Basic_Settings.urls')),
    path('Majjaka-Shop/', include('eProc_Basic.urls')),
    path('configuration/master_settings/', include('eProc_Master_Settings.urls')),
    path('configuration/application_settings/', include('eProc_Application_Settings.urls')),
    path('message-settings/', include('eProc_Messages.urls')),
    path('purchase_order/', include('eProc_Purchase_Order.urls')),
    path('configuration_check/', include('eProc_Configuration_Check.urls')),
    path('generate_otp/', include('eProc_Generate_OTP.urls')),
    path('setup_new_client/', include('eProc_New_Client_Setup.urls')),
    path('timesheet/', include('eProc_Time_Sheet.urls')),
    path('projects/', include('eProc_Projects.urls')),
    path('som/', include('eProc_Supplier_Order_Management.urls')),
    path('marketing/', include('eProc_Marketing.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
