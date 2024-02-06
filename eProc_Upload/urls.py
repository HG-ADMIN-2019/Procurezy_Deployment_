from django.urls import path
from . import views

app_name = 'eProc_Upload'

urlpatterns = [

    path('data_upload/', views.data_upload, name='data_upload'), # upload data url
    path('upload_pk_fk/<str:app_name>/<str:table_name>',views.UploadPkFkData,name='upload_table'),
    path('upload/<str:app_name>/<str:table_name>',views.UploadPKData,name='upload_pk_table'),
    path('upload_data/',views.upload_prod_services_data,name='upload_data_table'),
    # Upload
    path ( 'upload_NotifSettings/', views.upload_notifsettings_master, name='upload_notifsettings' ),# upload NotifSettings Data Desc data url (SP12-06- Shankar)
    path ( 'upload_NotifKeywords/', views.upload_notifkeywords_master, name='upload_notifkeywords' ),# upload NotifKeywords Data Desc data url (SP12-06- Shankar)
    path ( 'upload_SystemSettings/', views.upload_systemsettings_master, name='upload_systemsettings' ),# upload upload_systemsettings Data Desc data url (SP12-06- Shankar)


    # Master Data Settings
    path ('upload_User/', views.upload_user_master, name='upload_user'),
    path ('upload_SupplierMaster/', views.upload_supplier_master, name='upload_suppliermaster'),# upload Supplier Master data url (SP11-13- Shankar)

    path ('upload_Productcustcatg/', views.upload_productcustcatg_master, name='upload_productcustcatg'),# upload Product customer Categories data url (SP11-13- Shankar)
    path ('upload_Address/', views.upload_address_master, name='upload_address'),# upload Address data url (SP11-13- Shankar)
    path ('upload_Addressmap/', views.upload_addressmap_master, name='upload_addressmap'),# upload Addressmap data url (SP11-13- Shankar)

    path ('upload_Detglacc/', views.upload_detglacc_master, name='upload_detglacc'),# upload Accounting Data Desc data url (SP11-13- Shankar)
    path ('upload_Apptypes/', views.upload_apptypes_master, name='upload_apptypes' ),# upload App Types data url (SP11-13- Shankar)

    # path ('upload_Wfschema/', views.upload_Wfschema_master, name='upload_wfschema' ),# upload WF Schema data url (SP11-13- Shankar)
    path ('upload_Wfacc/', views.upload_Wfacc_master, name='upload_wfacc' ),# upload WF Acc data url (SP11-13- Shankar)

    # Master Data Settings

    # Org Model Data Settings
    path ( 'upload_orgmodel/', views.upload_orgmodel_master, name='upload_orgmodel' ),  # upload orgmodel data url


    # Transaction Data Settings

    # Transaction Data Settings
    path ( 'upload_sc/', views.upload_sc, name='upload_sc' ),  # upload sc data url
    path ( 'upload_po/', views.upload_po, name='upload_po' ),  # upload po data url
    # Transaction Data Settings
]