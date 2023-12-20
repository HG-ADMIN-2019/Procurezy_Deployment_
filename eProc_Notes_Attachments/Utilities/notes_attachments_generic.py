from django.http import FileResponse, Http404
from eProc_Basic.Utilities.constants.constants import CONST_DOC_TYPE_SC, CONST_APPROVER_NOTE
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import *
from eProc_Configuration.models.development_data import DocumentType
from eProc_Notes_Attachments.models import Attachments, Notes

django_query_instance = DjangoQueries()


# To download pdf
def download(path):
    if os.path.exists(path):
        stream = open(path, 'rb')
        return FileResponse(stream, as_attachment=True, filename=os.path.basename(path))
    raise Http404


# Function to save attachment data
def save_attachment_data(header_guid, doc_number, attachment_name, attachment_data, attachment_type, doc_format,
                         item_guid, item_num):
    """
    :param item_num:
    :param header_guid:
    :param doc_number:
    :param attachment_name:
    :param attachment_data:
    :param attachment_type:
    :param doc_format:
    :param item_guid:
    :return:
    """
    
    django_query_instance.django_create_query(Attachments, {
        'guid': guid_generator(),
        'client': django_query_instance.django_get_query(OrgClients, {'client': global_variables.GLOBAL_CLIENT}),
        'document_type': django_query_instance.django_get_query(DocumentType, {'document_type': CONST_DOC_TYPE_SC}),
        'header_guid': header_guid,
        'item_num': item_num,
        'doc_num': str(doc_number),
        'title': attachment_name,
        'doc_file': attachment_data,
        'attach_type_flag': attachment_type,
        'doc_format': doc_format,
        'item_guid': item_guid
    })


# Function to save approval note
def save_approval_note(counter, client, header_guid, doc_number, approval_note):
    """
    :param counter:
    :param client:
    :param header_guid:
    :param doc_number:
    :param approval_note:
    :return:
    """
    if counter == 0:
        django_query_instance.django_create_query(Notes, {
            'guid': guid_generator(),
            'client_id': django_query_instance.django_get_query(OrgClients, {'client': client}),
            'header_guid': header_guid, 'doc_num': doc_number,
            'document_type': django_query_instance.django_get_query(DocumentType, {'document_type': CONST_DOC_TYPE_SC}),
            'note_type': CONST_APPROVER_NOTE,
            'note_text': approval_note,
            'item_num': 0
        })


# Function to save internal and supplier note
def save_internal_supplier_note(client, item_guid, doc_number, item_num, note_type, text_data):
    """
    :param client:
    :param item_guid:
    :param doc_number:
    :param item_num:
    :param note_type:
    :param text_data:
    :return:
    """
    django_query_instance.django_create_query(Notes, {
        'guid': guid_generator(),
        'client_id': django_query_instance.django_get_query(OrgClients, {'client': client}),
        'item_guid': item_guid,
        'item_num': item_num,
        'doc_num': doc_number,
        'document_type': django_query_instance.django_get_query(DocumentType, {'document_type': CONST_DOC_TYPE_SC}),
        'note_type': note_type,
        'note_text': text_data
    })
