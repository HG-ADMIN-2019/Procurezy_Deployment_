from django.db import models


class EmailUserMonitoring(models.Model):
    """

    """
    email_user_monitoring_guid = models.CharField(db_column='EMAIL_USER_MONITORING_GUID', primary_key=True,
                                                  max_length=32)
    object_type = models.CharField(db_column='OBJECT_TYPE', max_length=20, null=False)
    username = models.CharField(db_column='USERNAME', max_length=20, null=False)
    sender_email = models.EmailField(db_column='SENDER_EMAIL', max_length=100, null=False)
    receiver_email = models.EmailField(db_column='RECEIVER_EMAIL', max_length=100, null=False)
    email_status = models.PositiveIntegerField(db_column='EMAIL_STATUS', null=False)
    error_type = models.CharField(db_column='ERROR_TYPE', max_length=20, null=True)
    email_user_monitoring_created_by = models.CharField(db_column='EMAIL_USER_MONITORING_CREATED_BY', max_length=30,
                                                        null=True)
    email_user_monitoring_created_at = models.DateTimeField(db_column='EMAIL_USER_MONITORING_CREATED_AT', max_length=50,
                                                            auto_now_add=True,
                                                            null=True)
    email_user_monitoring_changed_by = models.CharField(db_column='EMAIL_USER_MONITORING_CHANGED_BY', max_length=30,
                                                        null=True)
    email_user_monitoring_changed_at = models.DateTimeField(db_column='EMAIL_USER_MONITORING_CHANGED_AT', max_length=50,
                                                            auto_now=True,
                                                            null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    email_contents_guid = models.ForeignKey('eProc_Configuration.EmailContents', db_column='EMAIL_CONTENTS_GUID',
                                            on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = 'MTD_EMAIL_USER_MONITORING'


class EmailDocumentMonitoring(models.Model):
    """

    """
    email_document_monitoring_guid = models.CharField(db_column='EMAIL_DOCUMENT_MONITORING_GUID', primary_key=True,
                                                      max_length=32)
    object_type = models.CharField(db_column='OBJECT_TYPE', max_length=20, null=False)
    doc_type = models.CharField(db_column='DOC_TYPE', max_length=10, null=False)
    doc_number = models.CharField(db_column='DOC_NUMBER', max_length=10, blank=False, null=False)
    sender_email = models.EmailField(db_column='SENDER_EMAIL', max_length=100, null=False)
    receiver_email = models.EmailField(db_column='RECEIVER_EMAIL', max_length=100, null=False)
    email_status = models.PositiveIntegerField(db_column='EMAIL_STATUS', null=False)
    error_type = models.CharField(db_column='ERROR_TYPE', max_length=20, null=True)
    email_document_monitoring_created_by = models.CharField(db_column='EMAIL_DOCUMENT_MONITORING_CREATED_BY',
                                                            max_length=30,
                                                            null=True)
    email_document_monitoring_created_at = models.DateTimeField(db_column='EMAIL_DOCUMENT_MONITORING_CREATED_AT',
                                                                max_length=50,
                                                                auto_now_add=True,
                                                                null=True)
    email_document_monitoring_changed_by = models.CharField(db_column='EMAIL_DOCUMENT_MONITORING_CHANGED_BY',
                                                            max_length=30,
                                                            null=True)
    email_document_monitoring_changed_at = models.DateTimeField(db_column='EMAIL_DOCUMENT_MONITORING_CHANGED_AT',
                                                                max_length=50,
                                                                auto_now=True,
                                                                null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    email_contents_guid = models.ForeignKey('eProc_Configuration.EmailContents', db_column='EMAIL_CONTENTS_GUID',
                                            on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = 'MTD_EMAIL_DOCUMENT_MONITORING'


class EmailSupplierMonitoring(models.Model):
    """

    """
    email_supplier_monitoring_guid = models.CharField(db_column='EMAIL_SUPPLIER_MONITORING_GUID', primary_key=True,
                                                      max_length=32)
    object_type = models.CharField(db_column='OBJECT_TYPE', max_length=20, null=False)
    doc_type = models.CharField(db_column='DOC_TYPE', max_length=10, null=False)
    doc_number = models.CharField(db_column='DOC_NUMBER', max_length=10, blank=False, null=False)
    sender_email = models.EmailField(db_column='SENDER_EMAIL', max_length=100, null=False)
    receiver_email = models.EmailField(db_column='RECEIVER_EMAIL', max_length=100, null=False)
    email_status = models.PositiveIntegerField(db_column='EMAIL_STATUS', null=False)
    error_type = models.CharField(db_column='ERROR_TYPE', max_length=20, null=True)
    email_supplier_monitoring_created_by = models.CharField(db_column='EMAIL_SUPPLIER_MONITORING_CREATED_BY',
                                                            max_length=30,
                                                            null=True)
    email_supplier_monitoring_created_at = models.DateTimeField(db_column='EMAIL_SUPPLIER_MONITORING_CREATED_AT',
                                                                max_length=50,
                                                                auto_now_add=True,
                                                                null=True)
    email_supplier_monitoring_changed_by = models.CharField(db_column='EMAIL_SUPPLIER_MONITORING_CHANGED_BY',
                                                            max_length=30,
                                                            null=True)
    email_supplier_monitoring_changed_at = models.DateTimeField(db_column='EMAIL_SUPPLIER_MONITORING_CHANGED_AT',
                                                                max_length=50,
                                                                auto_now=True,
                                                                null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    email_contents_guid = models.ForeignKey('eProc_Configuration.EmailContents', db_column='EMAIL_CONTENTS_GUID',
                                            on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = 'MTD_EMAIL_SUPPLIER_MONITORING'
