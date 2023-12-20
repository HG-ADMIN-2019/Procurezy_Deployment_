from django.db import models


class Notifications(models.Model):
    """
    Contains user  notifications
    """
    notification_id = models.CharField(primary_key=True, db_column='NOTIFICATION_ID', max_length=32, null=False)
    username = models.CharField(db_column='USERNAME', null=True, unique=False, max_length=16)
    notification_type_id = models.CharField(db_column='NOTIFICATION_TYPE_ID', max_length=12, null=False)
    values = models.CharField(db_column='VALUES', max_length=30, null=False)
    read_status = models.BooleanField(default=False, null=False, db_column='READ_STATUS')
    object_id = models.PositiveIntegerField(db_column='OBJECT_ID', null=True)
    star_notif_flag = models.BooleanField(default=False, null=False, db_column='STAR_NOTIF_FLAG')
    notif_created_by = models.CharField(db_column='NOTIF_CREATED_BY', max_length=30, null=True)
    notif_created_at = models.DateTimeField(db_column='NOTIF_CREATED_AT', blank=True, null=True)
    notif_changed_by = models.CharField(db_column='NOTIF_CHANGED_BY', max_length=30, null=True)
    notif_changed_at = models.DateTimeField(db_column='NOTIF_CHANGED_AT', blank=True, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = "MTD_NOTIFICATIONS"
        managed = True
