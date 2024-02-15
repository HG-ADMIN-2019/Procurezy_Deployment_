from django.db import models


class CountryCompCode(models.Model):
    """
    Contains company code description
    """
    country_comp_code_guid = models.CharField(db_column='COMPANY_GUID', primary_key=True, max_length=32)
    company_code_id = models.CharField(db_column='COMPANY_CODE_ID', max_length=20, null=False)
    country = models.ForeignKey('eProc_Basic.Country', db_column='COUNTRY', on_delete=models.PROTECT, null=False)
    client = models.ForeignKey('eProc_Basic.OrgClients', db_column='CLIENT', on_delete=models.PROTECT, null=False)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "MSS_COUNTRY_COMP_CODE"
        unique_together = ('client', 'company_code_id')
        managed = True


class CompanyGrpUser(models.Model):
    """
    Contains company code description
    """
    company_grp_user_guid = models.CharField(db_column='COMPANY_GUID', primary_key=True, max_length=32)
    company_grp_id = models.CharField(db_column='COMPANY_GRP_ID', max_length=20, null=False)
    username = models.CharField(db_column='USERNAME', max_length=16, null=False)
    client = models.ForeignKey('eProc_Basic.OrgClients', db_column='Client', on_delete=models.PROTECT, null=False)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "MSS_COMP_CODE_GRP_USER"
        managed = True

    def __str__(self):
        return self.company_grp_id


class CompanyCodeGrp(models.Model):
    """
    Contains company code description
    """
    company_grp_guid = models.CharField(db_column='COMPANY_GUID', primary_key=True, max_length=32)
    company_grp_id = models.CharField(db_column='COMPANY_GRP_ID', max_length=20, null=False)
    company_code_id = models.CharField(db_column='COMPANY_CODE_ID', max_length=20, null=False)
    client = models.ForeignKey('eProc_Basic.OrgClients', db_column='CLIENT', on_delete=models.PROTECT, null=False)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "MSS_COMP_CODE_GRP"
        managed = True

    def __str__(self):
        return self.company_grp_id
