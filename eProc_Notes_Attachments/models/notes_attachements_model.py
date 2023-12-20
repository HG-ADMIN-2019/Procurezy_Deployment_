from datetime import date
import os
from django.db import models

from Majjaka_eProcure import settings
from eProc_Configuration.models import OrgClients


class Attachments(models.Model):
    def get_file_path(self, filename):
        return os.path.join('attachments', (OrgClients.objects.get(client=self.client)).__str__(),
                            date.today().year.__str__(), date.today().strftime("%B"), self.doc_num, self.item_guid,
                            filename)

    guid = models.CharField(db_column='guid', primary_key=True, max_length=32)
    item_num = models.PositiveIntegerField(db_column='ITEM_NUM', blank=False, null=False, verbose_name='Item Number',default=0)
    header_guid = models.CharField(db_column='HEADER_GUID', max_length=32, null=False)
    item_guid = models.CharField(db_column='ITEM_GUID', max_length=32, null=True, blank=True)
    doc_num = models.CharField(db_column='DOC_NUMBER', max_length=10, blank=False, null=False,verbose_name='DOC Number')
    title = models.CharField(db_column='TITLE', max_length=20, null=False, blank=False)
    doc_file = models.FileField(db_column='DOC_FILE', upload_to=get_file_path, null=False)
    attach_type_flag = models.CharField(db_column='ATTACH_TYPE_FLAG', max_length=1, null=False, blank=False)
    doc_format = models.CharField(db_column='DOC_FORMAT', null=False, max_length=255)
    attachments_created_at = models.DateTimeField(db_column='ATTACHMENTS_CREATED_AT', blank=False, null=True)
    attachments_created_by = models.CharField(db_column='ATTACHMENTS_CREATED_BY', max_length=12, blank=False,
                                              null=True)
    attachments_changed_at = models.DateTimeField(db_column='ATTACHMENTS_CHANGED_AT', blank=True, null=True)
    attachments_changed_by = models.CharField(db_column='ATTACHMENTS_CHANGED_BY', max_length=12, blank=False,
                                              null=True)
    attachments_source_system = models.CharField(db_column='ATTACHMENTS_SOURCE_SYSTEM', max_length=20)
    attachments_destination_system = models.CharField(db_column='ATTACHMENTS_DESTINATION_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    document_type = models.ForeignKey('eProc_Configuration.DocumentType', db_column='DOCUMENT_TYPE',on_delete=models.PROTECT,default=None)

    class Meta:
        db_table = 'MTD_ATTACHMENTS'
        managed = True


class Notes(models.Model):
    guid = models.CharField(db_column='NOTE_GUID', primary_key=True, max_length=32)
    item_num = models.PositiveIntegerField(db_column='ITEM_NUM', blank=False, null=False, verbose_name='Item Number',default=0)
    header_guid = models.CharField(db_column='HEADER_GUID', max_length=32, null=True)
    item_guid = models.CharField(db_column='ITEM_GUID', max_length=32, null=True, blank=True)
    doc_num = models.CharField(db_column='DOC_NUMBER', max_length=10, blank=True, null=True, verbose_name='DOC Number')
    note_type = models.CharField(db_column='NOTE_TYPE', max_length=20, null=True)
    note_type_flag = models.CharField(db_column='NOTE_TYPE_FLAG', null=True, max_length=1)
    note_text = models.CharField(db_column='NOTE_TEXT', null=True, max_length=1000)
    notes_created_at = models.DateTimeField(db_column='NOTES_CREATED_AT', blank=False, null=True)
    notes_created_by = models.CharField(db_column='NOTES_CREATED_BY', max_length=12, blank=False, null=True)
    notes_changed_at = models.DateTimeField(db_column='NOTES_CHANGED_AT', blank=True, null=True)
    notes_changed_by = models.CharField(db_column='NOTES_CHANGED_BY', max_length=12, blank=False, null=True)
    notes_source_system = models.CharField(db_column='NOTES_SOURCE_SYSTEM', max_length=20)
    notes_destination_system = models.CharField(db_column='NOTES_DESTINATION_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    document_type = models.ForeignKey('eProc_Configuration.DocumentType', db_column='DOCUMENT_TYPE',on_delete=models.PROTECT,default=None)

    class Meta:
        db_table = 'MTD_NOTES'
        managed = True
