import os
import uuid
from datetime import date
from io import BytesIO
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf import pisa

from eProc_Basic.Utilities.constants.constants import CONST_DOC_TYPE_PO
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import DocumentType, OrgClients
from eProc_Generate_PDF.models import DocumentsPdf

django_query_instance = DjangoQueries()


def save_pdf(params: dict):
    """

    """
    template = get_template("po_pdf_mockup.html")
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
    file_name = str(params['doc_number'])
    path = str(settings.BASE_DIR) + f'/media/po_pdf/{global_variables.GLOBAL_CLIENT}/{file_name}.pdf'
    directory = os.path.join(str(settings.BASE_DIR), 'media', 'po_pdf',
                             (OrgClients.objects.get(client=global_variables.GLOBAL_CLIENT)).__str__(),
                             date.today().year.__str__(), date.today().strftime("%B"), file_name)
    path = os.path.join(directory, file_name + '.pdf')
    if not os.path.exists(directory):
        os.makedirs(directory)
    count = 1
    while os.path.exists(path):
        path = str(settings.BASE_DIR) + f'/media/po_pdf/{global_variables.GLOBAL_CLIENT}/{file_name}-{count}.pdf'
        print("save pdf path", path)

        count = count + 1
    try:
        folder_path = os.path.join('po_pdf', (OrgClients.objects.get(client=global_variables.GLOBAL_CLIENT)).__str__(),
                                   date.today().year.__str__(), date.today().strftime("%B"), file_name,
                                   file_name + '.pdf')
        with open(path, 'wb+') as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
            django_query_instance.django_create_query(DocumentsPdf,
                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                       'doc_num': file_name,
                                                       'documents_pdf_guid': guid_generator(),
                                                       'document_type': django_query_instance.django_get_query(
                                                           DocumentType,
                                                           {'document_type': CONST_DOC_TYPE_PO,
                                                            }),
                                                       'doc_path': folder_path
                                                       })
    except Exception as e:
        print(e)
    if pdf.error:
        return '', False, path
    print("save pdf path", path)
    return file_name, True, path
