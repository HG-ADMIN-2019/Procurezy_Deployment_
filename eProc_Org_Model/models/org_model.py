from django.db import models


class OrgNames(models.Model):
    """
    Table contains all organizations names
    """
    root_node = models.CharField(db_column='ROOT_NODE', primary_key=True, max_length=32)
    name = models.CharField(db_column='NAME', max_length=60, null=False)
    org_names_created_by = models.CharField(db_column='ORG_NAMES_CREATED_BY', max_length=30, null=True)
    org_names_created_at = models.DateTimeField(db_column='ORG_NAMES_CREATED_AT', max_length=50, null=True)
    org_names_changed_by = models.CharField(db_column='ORG_NAMES_CHANGED_BY', max_length=30, null=True)
    org_names_changed_at = models.DateTimeField(db_column='ORG_NAMES_CHANGED_AT', max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    object_id = models.ForeignKey('eProc_Org_Model.OrgModel', db_column='OBJECT_ID', on_delete=models.PROTECT,
                                  null=True)

    class Meta:
        unique_together = ('client', 'name')
        db_table = "MTD_ORG_NAMES"
        managed = True

    def __str__(self):
        return self.name


class OrgModel(models.Model):
    """
    Table contains all nodes of org structure
    """
    object_id = models.PositiveBigIntegerField(db_column='OBJECT_ID', primary_key=True)
    node_guid = models.CharField(unique=True, db_column='NODE_GUID', max_length=32)
    name = models.CharField(db_column='NAME', max_length=60, null=False)
    parent_node_guid = models.CharField(db_column='PARENT_NODE_GUID', max_length=32, null=True)
    node_type = models.CharField(db_column='NODE_TYPE', max_length=10, null=False)
    root_node_object_id = models.PositiveIntegerField(db_column='ROOT_NODE_OBJECT_ID',null=True)
    del_ind = models.BooleanField(default=False, null=False)
    org_model_created_at = models.DateTimeField(db_column='ORG_MODEL_CREATED_AT', blank=True, null=True)
    org_model_created_by = models.CharField(db_column='ORG_MODEL_CREATED_BY', max_length=30, null=True)
    org_model_changed_at = models.DateTimeField(db_column='ORG_MODEL_CHANGED_AT', blank=True, null=True)
    org_model_changed_by = models.CharField(db_column='ORG_MODEL_CHANGED_BY', max_length=30, null=True)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = "MTD_ORG_MODEL"
        managed = True

    def __str__(self):
        return "%s %s" % (self.object_id, self.name)
