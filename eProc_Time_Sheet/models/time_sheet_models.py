from django.db import models


class ProjectEfforts(models.Model):
    project_efforts_guid = models.CharField(db_column='PROJECT_EFFORTS_GUID', primary_key=True, max_length=32)
    project_id = models.CharField(db_column='PROJECT_ID', max_length=20)
    username = models.CharField(db_column='USERNAME', null=False, max_length=16)
    calender_id = models.CharField(db_column='CALENDER_ID', max_length=10)
    project_category = models.CharField(db_column='PROJECT_CATEGORY', null=False, blank=False, max_length=100)
    effort = models.PositiveIntegerField(db_column='EFFORT', null=True)
    effort_day = models.CharField(db_column='EFFORT_DAY', null=True, blank=True, max_length=10)
    effort_date = models.DateField(db_column='EFFORT_DATE', null=False)
    effort_week = models.PositiveIntegerField(db_column='EFFORT_WEEK', null=True)
    effort_year = models.PositiveIntegerField(db_column='EFFORT_YEAR', null=True)
    effort_description = models.CharField(db_column='EFFORT_DESCRIPTION', null=False, max_length=255)
    project_efforts_created_by = models.CharField(db_column='PROJECT_EFFORTS_CREATED_BY',
                                                  max_length=30,
                                                  null=True)
    project_efforts_created_at = models.DateTimeField(db_column='PROJECT_EFFORTS_CREATED_AT',
                                                      max_length=50,
                                                      null=True)
    project_efforts_changed_by = models.CharField(db_column='PROJECT_EFFORTS_CHANGED_BY',
                                                  max_length=30,
                                                  null=True)
    project_efforts_changed_at = models.DateTimeField(db_column='project_efforts_changed_at',
                                                      max_length=50,
                                                      null=True)
    del_ind = models.BooleanField(db_column='DEL_IND', default=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        managed = True
        db_table = 'MTD_PROJECT_EFFORTS'
