from django.db import models


class DBQueriesOrgannsmt:
    @staticmethod
    def get_annsmt_details_by_fields(client, obj, subject_query, status_query, priority_query):
        return list(OrgAnnouncements.objects.filter(subject_query, status_query, priority_query, client=client,
                                                    del_ind=False).values().order_by('announcement_id'))


class OrgAnnouncements(models.Model, DBQueriesOrgannsmt):
    unique_announcement_id = models.CharField(db_column='UNIQUE_ANNOUNCEMENT_ID', primary_key=True, max_length=32,
                                              null=False, default=None)
    announcement_id = models.CharField(db_column='ANNOUNCEMENT_ID', null=True, max_length=10)
    announcement_subject = models.CharField(db_column='ANNOUNCEMENT_SUBJECT', null=False, max_length=225)
    announcement_description = models.CharField(db_column='ANNOUNCEMENT_DESCRIPTION', null=False, max_length=1000)
    announcement_type = models.CharField(db_column='ANNOUNCEMENT_TYPE', null=True, max_length=50)
    status = models.CharField(db_column='STATUS', null=False, max_length=30)
    priority = models.CharField(db_column='PRIORITY', null=False, max_length=30)
    announcement_from_date = models.DateTimeField(db_column='ANNOUNCEMENT_FROM_DATE', blank=True, null=True)
    announcement_to_date = models.DateTimeField(db_column='ANNOUNCEMENT_TO_DATE', blank=True, null=True)
    announcements_created_at = models.DateTimeField(db_column='ANNOUNCEMENTS_CREATED_AT', blank=True, null=True)
    announcements_created_by = models.CharField(db_column='ANNOUNCEMENTS_CREATED_BY', max_length=16, null=True)
    announcements_changed_at = models.DateTimeField(db_column='ANNOUNCEMENTS_CHANGED_AT', blank=True, null=True)
    announcements_changed_by = models.CharField(db_column='ANNOUNCEMENTS_CHANGED_BY', max_length=16, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    object_id = models.ForeignKey('eProc_Org_Model.OrgModel', db_column='OBJECT_ID', on_delete=models.PROTECT,
                                  null=True)

    class Meta:
        managed = True
        db_table = 'MTD_ORG_ANNOUNCEMENTS'


class OrgSupport(models.Model):
    org_support_guid = models.CharField(db_column='ORG_SUPPORT_GUID', max_length=32, primary_key=True)
    org_support_types = models.CharField(db_column='ORG_SUPPORT_TYPES', max_length=50)
    org_support_email = models.CharField(db_column='ORG_SUPPORT_EMAIL', max_length=50)
    org_support_number = models.CharField(db_column='ORG_SUPPORT_NUMBER', max_length=20)
    username = models.CharField(db_column='USERNAME', null=True, max_length=16)
    org_support_created_at = models.DateTimeField(db_column='ORG_SUPPORT_CREATED_AT', blank=False, null=True)
    org_support_created_by = models.CharField(db_column='ORG_SUPPORT_CREATED_BY', max_length=16, blank=False, null=True)
    org_support_changed_at = models.DateTimeField(db_column='ORG_SUPPORT_CHANGED_AT', blank=True, null=True)
    org_support_changed_by = models.CharField(db_column='ORG_SUPPORT_CHANGED_BY', max_length=16, blank=False, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    object_id = models.ForeignKey('eProc_Org_Model.OrgModel', db_column='OBJECT_ID', on_delete=models.PROTECT,
                                  null=True)

    class Meta:
        db_table = "MTD_ORG_SUPPORT"
        managed = True
