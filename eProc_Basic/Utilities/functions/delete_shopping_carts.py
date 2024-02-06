import os
import shutil

from Majjaka_eProcure import settings
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Doc_Details.Utilities.details_generic import GetAttachments
from eProc_Form_Builder.models import EformFieldData
from eProc_Notes_Attachments.models import Attachments, Notes
from eProc_Purchase_Order.models import PoHeader, PoItem, PoAccounting, PoAddresses, PoApproval, PoPotentialApproval
from eProc_Shopping_Cart.models import ScItem, PurchasingData, ScAccounting, ScAddresses, ScApproval, ScHeader, \
    ScPotentialApproval, PurchasingUser

django_query_instance = DjangoQueries()


def delete_all_attachments():
    """

    """
    attachment_data_guid = django_query_instance.django_filter_value_list_query(Attachments,
                                                                                {
                                                                                    'client': global_variables.GLOBAL_CLIENT,
                                                                                }, 'guid')
    for attach_data in attachment_data_guid:

        file_path = Attachments.objects.get(guid=attach_data)
        get_file_path = file_path.doc_file
        dir_pa = str(get_file_path).rsplit(str(file_path.doc_num), 1)[0]
        media_path = settings.MEDIA_ROOT
        file_path.delete()
        # File path
        absolute_path = media_path + '\\' + str(get_file_path)
        # Directory path
        dir_path = media_path + '\\' + dir_pa + file_path.doc_num
        count = Attachments.objects.filter(doc_num=file_path.doc_num).count()
        if count > 0:
            if os.path.exists(absolute_path):
                os.remove(absolute_path)
        else:
            shutil.rmtree(dir_path)


def delete_po_table(filter_criteria):
    """

    """
    django_query_instance.django_filter_delete_query(PurchasingUser, filter_criteria)

    django_query_instance.django_filter_delete_query(PurchasingData, filter_criteria)

    django_query_instance.django_filter_delete_query(Attachments, filter_criteria)

    django_query_instance.django_filter_delete_query(Notes, filter_criteria)

    django_query_instance.django_filter_delete_query(PoAccounting, filter_criteria)

    django_query_instance.django_filter_delete_query(PoAddresses, filter_criteria)

    django_query_instance.django_filter_delete_query(EformFieldData, filter_criteria)

    django_query_instance.django_update_query(ScItem, filter_criteria,
                                              {'po_item_guid': None})

    django_query_instance.django_filter_delete_query(PoItem, filter_criteria)
    django_query_instance.django_filter_delete_query(PoPotentialApproval, filter_criteria)
    django_query_instance.django_filter_delete_query(PoApproval, filter_criteria)
    django_query_instance.django_filter_delete_query(PoAccounting, filter_criteria)
    django_query_instance.django_filter_delete_query(PoAddresses, filter_criteria)
    django_query_instance.django_filter_delete_query(PoHeader, filter_criteria)


def delete_po_pdf():
    """

    """
    location = str(settings.BASE_DIR) + '/media/po_pdf/' + str(global_variables.GLOBAL_CLIENT)
    po_doc_numbers = django_query_instance.django_filter_value_list_query(PoHeader,
                                                                         {'client':global_variables.GLOBAL_CLIENT},
                                                                         'doc_number')
    for po_doc_number in po_doc_numbers:
        file_name = po_doc_number+'.pdf'
        path = os.path.join(location, file_name)
        if os.path.exists(path):
            os.remove(path)


def delete_transaction_data(filter_criteria):
    delete_all_attachments()
    delete_po_pdf()
    delete_po_table(filter_criteria)
    delete_sc_table(filter_criteria)


def delete_sc_table(filter_criteria):
    django_query_instance.django_filter_delete_query(ScAccounting, filter_criteria)
    django_query_instance.django_filter_delete_query(ScAddresses, filter_criteria)
    django_query_instance.django_filter_delete_query(ScItem, filter_criteria)
    django_query_instance.django_filter_delete_query(ScPotentialApproval, filter_criteria)
    django_query_instance.django_filter_delete_query(ScApproval, filter_criteria)
    django_query_instance.django_filter_delete_query(ScHeader, filter_criteria)
