from django.db import models

# Create your models here.


class OrgAttributesLevel(models.Model):
    """
    Contains attributes mapping in org levels
    """
    attr_level_guid = models.CharField(db_column='ATTR_LEVEL_GUID', max_length=32, verbose_name='Attribute level guid',
                                       primary_key=True)
    version_number = models.PositiveIntegerField(db_column='VERSION_NUMBER', null=False, verbose_name='version_number')
    object_type = models.CharField(db_column='OBJECT_TYPE', max_length=2, null=False, verbose_name='object type')
    start_date = models.DateTimeField(db_column='START_DATE', null=True, verbose_name='start date')
    end_date = models.DateTimeField(db_column='END_DATE', null=True, verbose_name='end_date')
    status = models.CharField(db_column='STATUS', max_length=1, null=True, verbose_name='Planning status')
    low = models.CharField(db_column='LOW', max_length=60, null=True, verbose_name='Attribute value')
    high = models.CharField(db_column='HIGH', max_length=60, null=True, verbose_name='Attribute values to')
    attr_level_exclude = models.BooleanField(default=False, null=False, db_column='ATTR_LEVEL_EXCLUDE')
    attr_level_default = models.BooleanField(default=False, null=False, db_column='ATTR_LEVEL_DEFAULT')
    org_attr_created_at = models.DateTimeField(db_column='ORG_ATTR_CREATED_AT', blank=True, null=True)
    org_attr_created_by = models.CharField(db_column='ORG_ATTR_CREATED_BY', max_length=30, null=True)
    org_attr_changed_at = models.DateTimeField(db_column='ORG_ATTR_CHANGED_AT', blank=True, null=True)
    org_attr_changed_by = models.CharField(db_column='ORG_ATTR_CHANGED_BY', max_length=30, null=True)
    attribute_value_desc = models.CharField(db_column='attribute_value_desc', max_length=150, null=True,
                                            verbose_name='Attribute Value Desc')
    extended_value = models.CharField(db_column='EXTENDED_VALUE', max_length=70, null=True,
                                      verbose_name='Extended Value')
    del_ind = models.BooleanField(default=False, null=False)
    attribute_id = models.ForeignKey('eProc_Configuration.OrgAttributes', on_delete=models.PROTECT, db_column='ATTRIBUTE_ID', null=False,
                                     verbose_name='attribute_id')
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    object_id = models.ForeignKey('eProc_Org_Model.OrgModel', db_column='OBJECT_ID', on_delete=models.PROTECT,
                                  null=False)

    class Meta:
        db_table = "MTD_ORG_ATTR_LEVEL"
        managed = True

    def __str__(self):
        return str(self.attribute_id) if self.attribute_id else ''