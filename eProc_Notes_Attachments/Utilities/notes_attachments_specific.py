"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    notes_attachments_specific.py
Usage:
    Consists of validation functions and some special character handling functions
    1. validation for checking a string contains Mathematical symbols
    2. Function that replaces tab space
    3. Function that replaces the new line character

Author:
    Shilpa Ellur
"""
from eProc_Basic.Utilities.constants.constants import CONST_DOC_TYPE_SC
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Configuration.models import OrgClients
from eProc_Configuration.models.development_data import DocumentType

django_query_instance = DjangoQueries()


def attach_instance_save(client, instance):
    instance.client = django_query_instance.django_get_query(OrgClients, {'client': client})
    instance.document_type = django_query_instance.django_get_query(DocumentType, {'document_type': CONST_DOC_TYPE_SC})
    instance.guid = guid_generator()
    instance.save()


def notes_instance_save(frmst, client):
    frmst.guid = guid_generator()
    frmst.client = django_query_instance.django_get_query(OrgClients, {'client': client})
    frmst.document_type = django_query_instance.django_get_query(DocumentType, {'document_type': CONST_DOC_TYPE_SC})
    frmst.del_ind = '0'
    frmst.save()
