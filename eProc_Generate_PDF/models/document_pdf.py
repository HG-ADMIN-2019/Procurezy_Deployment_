import os
from datetime import date

from django.db import models

from eProc_Configuration.models import OrgClients


class DocumentPdf(models.Model):
    def get_file_path(self, filename):
        return os.path.join('po_pdf', (OrgClients.objects.get(client=self.client)).__str__(),
                            date.today().year.__str__(), date.today().strftime("%B"), self.doc_num,
                            filename)

    document_pdf_guid = models.CharField(db_column='DOCUMENT_PDF_GUID', primary_key=True, max_length=32)
    doc_num = models.CharField(db_column='DOC_NUMBER', max_length=10, blank=False, null=False,
                               verbose_name='DOC Number')
    doc_file = models.FileField(db_column='DOC_FILE', upload_to=get_file_path, null=False)
    document_pdf_created_at = models.DateTimeField(db_column='DOCUMENT_PDF_CREATED_AT', blank=False, null=True)
    document_pdf_created_by = models.CharField(db_column='DOCUMENT_PDF_CREATED_BY', max_length=12, blank=False,
                                               null=True)
    document_pdf_changed_at = models.DateTimeField(db_column='DOCUMENT_PDF_CHANGED_AT', blank=True, null=True)
    document_pdf_changed_by = models.CharField(db_column='DOCUMENT_PDF_CHANGED_BY', max_length=12, blank=False,
                                               null=True)
    document_pdf_source_system = models.CharField(db_column='DOCUMENT_PDF_SOURCE_SYSTEM', max_length=20)
    document_pdf_destination_system = models.CharField(db_column='DOCUMENT_PDF_DESTINATION_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    document_type = models.ForeignKey('eProc_Configuration.DocumentType', db_column='DOCUMENT_TYPE',
                                      on_delete=models.PROTECT, default=None)

    class Meta:
        db_table = 'MTD_DOCUMENT_PDF'
        managed = True

class DocumentsPdf(models.Model):
    documents_pdf_guid = models.CharField(db_column='DOCUMENTS_PDF_GUID', primary_key=True, max_length=32)
    doc_num = models.CharField(db_column='DOC_NUMBER', max_length=10, blank=False, null=False,
                               verbose_name='DOC Number')
    doc_path = models.CharField(db_column='DOC_FILE', max_length=200, blank=False, null=False)
    documents_pdf_created_at = models.DateTimeField(db_column='DOCUMENTS_PDF_CREATED_AT', blank=False, null=True)
    documents_pdf_created_by = models.CharField(db_column='DOCUMENTS_PDF_CREATED_BY', max_length=12, blank=False,
                                               null=True)
    documents_pdf_changed_at = models.DateTimeField(db_column='DOCUMENTS_PDF_CHANGED_AT', blank=True, null=True)
    documents_pdf_changed_by = models.CharField(db_column='DOCUMENTS_PDF_CHANGED_BY', max_length=12, blank=False,
                                               null=True)
    documents_pdf_source_system = models.CharField(db_column='DOCUMENTS_PDF_SOURCE_SYSTEM', max_length=20)
    documents_pdf_destination_system = models.CharField(db_column='DOCUMENTS_PDF_DESTINATION_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    document_type = models.ForeignKey('eProc_Configuration.DocumentType', db_column='DOCUMENT_TYPE',
                                      on_delete=models.PROTECT, default=None)

    class Meta:
        db_table = 'MTD_DOCUMENTS_PDF'
        managed = True
