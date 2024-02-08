import os
import re
from django.db.models import Q
from django.http import Http404
# from eProc_Basic.Utilities.db_queries import getClients
# from eProc_Configure_Comp_Code.models import CompanyGrpUser, CompanyCodeGrp
from Majjaka_eProcure import settings
from eProc_Archiving.models import arch_ScHeader, ConfHeader, arch_PoHeader, arch_PoItem, arch_ScItem, ConfItem, \
    arch_SupplierSearch, ConfAccounting, arch_PoApproval, arch_PoAccounting, arch_ScAccounting, arch_ScApproval, \
    arch_CompanyCodeGrp, arch_CompanyGrpUser
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Configuration.models.application_data import CompanyGrpUser, CompanyCodeGrp

# from eProc_Doc_Search.models import ScHeader, PoHeader, SupplierSearch, ConfHeader, ScItem, PoItem, ConfItem
from eProc_Registration.models.registration_model import UserData


class DBQueries:
    def arch_get_hdr_data_by_objid(self, obj, objid, client):
        header_list = obj.objects.filter(doc_number=objid, client=client).order_by('doc_number')
        header_guid_list = list(obj.objects.filter(doc_number=objid, client=client).values_list('guid', flat=True))
        return header_list, header_guid_list

    def arch_get_hdr_data_by_fields(self, client, obj, supp_query, creator_query, requester_query, **kwargs):
        header_list = obj.objects.filter(supp_query, creator_query, requester_query, client=client, **kwargs).order_by(
            'doc_number')
        header_guid_list = list(
            obj.objects.filter(supp_query, creator_query, requester_query, client=client, **kwargs).values_list('guid',
                                                                                                                flat=True))
        return header_list, header_guid_list

    def get_hdr_data_by_po_number(self, obj, po_number, client):
        return obj.objects.filter(po_doc_number=po_number, client=client)


def arch_get_hdr_data(request, doc_type, doc_num, from_date, to_date, supplier, created_by, requester, po_number):
    client = getClients(request)
    if doc_type == 'SC':
        hdr_obj = arch_ScHeader
        hdr_inst = DBQueries()
    elif doc_type == 'PO':
        hdr_obj = arch_PoHeader
        hdr_inst = DBQueries()
    elif doc_type == 'CONF':
        hdr_obj = ConfHeader
        hdr_inst = DBQueries()
    else:
        raise Http404
    result = None
    supp_query = Q()
    creator_query = Q()
    requester_query = Q()
    args_list = {}
    header_guid = []

    if doc_num is not None and doc_num != '':
        result, header_guid = hdr_inst.arch_get_hdr_data_by_objid(hdr_obj, doc_num, client)

    elif po_number is not None and po_number != '':
        result = hdr_inst.get_hdr_data_by_po_number(hdr_obj, po_number, client)

    else:
        if from_date is not None and to_date is not None and from_date != '' and to_date != '':
            args_list['created_at__gte'] = from_date
            args_list['created_at__lte'] = to_date
        if (doc_type == 'PO' or doc_type == 'CONF') and supplier is not None and supplier != '':
            if '*' in supplier:
                supp_list = arch_SupplierSearch.get_suppid_by_first_name(supplier)
                supplier_match = re.search(r'[a-zA-Z0-9]+', supplier)
                if supplier[0] == '*' and supplier[-1] == '*':
                    supp_query |= Q(supplier_id__in=supp_list) | Q(supplier_id__icontains=supplier_match.group(0))
                elif supplier[0] == '*':
                    supp_query |= Q(supplier_id__in=supp_list) | Q(supplier_id__iendswith=supplier_match.group(0))
                else:
                    supp_query |= Q(supplier_id__in=supp_list) | Q(supplier_id__istartswith=supplier_match.group(0))
            else:
                supp_list = arch_SupplierSearch.get_suppid_by_first_name(supplier)
                supp_list.append(supplier)
                args_list['supplier_id__in'] = supp_list
        if created_by is not None and created_by != '':
            if '*' in created_by:
                user_list = UserData.get_usrid_by_first_name(created_by)
                creater_match = re.search(r'[a-zA-Z0-9]+', created_by)
                if created_by[0] == '*' and created_by[-1] == '*':
                    creator_query |= Q(created_by__in=user_list) | Q(created_by__contains=creater_match.group(0))
                elif created_by[0] == '*':
                    creator_query |= Q(created_by__in=user_list) | Q(created_by__endswith=creater_match.group(0))
                else:
                    creator_query |= Q(created_by__in=user_list) | Q(created_by__startswith=creater_match.group(0))
            else:
                user_list = UserData.get_usrid_by_first_name(created_by)
                user_list.append(created_by)
                args_list['created_by__in'] = user_list
        if requester is not None and requester != '':
            if '*' in requester:
                user_list = UserData.get_usrid_by_first_name(requester)
                requester_match = re.search(r'[a-zA-Z0-9]+', requester)
                if requester[0] == '*' and requester[-1] == '*':
                    requester_query |= Q(requester__in=user_list) | Q(requester__icontains=requester_match.group(0))
                elif requester[0] == '*':
                    requester_query |= Q(requester__in=user_list) | Q(requester__iendswith=requester_match.group(0))
                else:
                    requester_query |= Q(requester__in=user_list) | Q(requester__istartswith=requester_match.group(0))
            else:
                user_list = UserData.get_usrid_by_first_name(requester)
                user_list.append(requester)
                args_list['requester__in'] = user_list
        result, header_guid = hdr_inst.arch_get_hdr_data_by_fields(client, hdr_obj, supp_query, creator_query,
                                                                   requester_query,
                                                                   **(args_list))
    return result, header_guid


def get_cocode_list(login_username, client):
    """

    :param login_username:
    :return:
    """
    cmp_grp = list(arch_CompanyGrpUser.objects.filter(username=login_username, client=client, del_ind=False).values_list(
        'company_grp_id', flat=True))
    co_code_list = list(
        arch_CompanyCodeGrp.objects.filter(company_grp_id__in=cmp_grp, client=client, del_ind=False).values_list(
            'company_code_id', flat=True))
    return co_code_list


def get_sc_header_list(co_code_list, client, header_guid, hdr_obj, item_obj):
    """

    :param co_code_list:
    :param client:
    :return:
    """
    item_header_guid = list(
        item_obj.objects.filter(comp_code__in=co_code_list, client=client, header_guid__in=header_guid).values_list(
            'header_guid', flat=True))
    result = hdr_obj.objects.filter(guid__in=item_header_guid, client=client).order_by('doc_number')
    return result


def get_cocode_filter(client, login_username, header_guid, doc_type):
    """

    :param client:
    :param login_username:
    :param header_guid:
    :return:
    """
    co_code_list = get_cocode_list(login_username, client)
    hdr_obj = ''
    item_obj = ''
    if doc_type == 'SC':
        hdr_obj = arch_ScHeader
        item_obj = arch_ScItem
        hdr_inst = DBQueries()
    elif doc_type == 'PO':
        hdr_obj = arch_PoHeader
        item_obj = arch_PoItem
        hdr_inst = DBQueries()
    elif doc_type == 'CONF':
        hdr_obj = ConfHeader
        item_obj = ConfItem
        hdr_inst = DBQueries()
    else:
        raise Http404
    result = get_sc_header_list(co_code_list, client, header_guid, hdr_obj, item_obj)
    return result


def get_doc_details(type, hdr_guid):
    appr_data = []
    if type == 'SC':
        hdr_obj = arch_ScHeader()
        itm_obj = arch_ScItem()
        acc_obj = arch_ScAccounting()
        appr_obj = arch_ScApproval()
    elif type == 'PO':
        hdr_obj = arch_PoHeader()
        itm_obj = arch_PoItem()
        acc_obj = arch_PoAccounting()
        appr_obj = arch_PoApproval()
    elif type == 'CONF':
        hdr_obj = ConfHeader()
        itm_obj = ConfItem()
        acc_obj = ConfAccounting()
    else:
        raise Http404
    hdr_data = hdr_obj.get_hdr_data_by_guid(hdr_guid)
    itm_data = itm_obj.get_itms_by_guid(hdr_guid)
    itm_guids = []
    for item in itm_data:
        itm_guids.append(getattr(item, 'guid'))
    acc_data = acc_obj.get_acc_data_by_guid(itm_guids)
    if type == 'CONF':
        return {'hdr_data': hdr_data, 'itm_data': itm_data, 'acc_data': acc_data, 'appr_data': appr_data}
    else:
        appr_data = appr_obj.get_apprs_by_guid(hdr_guid)
        return {'hdr_data': hdr_data, 'itm_data': itm_data, 'acc_data': acc_data, 'appr_data': appr_data}


# To convert date entered in search page to database field format
def convert_date_to_str(self, date_val):
    return date_val.replace("-", "") + "000000"


# Get attachments by path
class arch_GetAttachments:
    po_attachments = []

    def get_attachments(self, request, hdr_guid):
        client = getClients(request)
        print("Client:", client)
        self.po_attachments = []
        hdr_obj = arch_PoHeader()
        objid = hdr_obj.get_objid_by_guid(hdr_guid)
        attach_dir = os.path.join(settings.MEDIA_ROOT, settings.ATTACH_PATH, str(client), 'Attachments')

        attach_file_path = None
        if os.path.exists(attach_dir):
            dir_list = os.listdir(attach_dir)
            for dir_name in dir_list:
                tmp_file = os.path.join(attach_dir, dir_name)
                if os.path.isfile(tmp_file):  # Check if it's a file directly in Attachments
                    attach_file_path = attach_dir
                    break
                elif os.path.isdir(tmp_file):
                    sub_path = os.path.join(tmp_file, objid)
                    if os.path.exists(sub_path):
                        attach_file_path = sub_path
                        print("Attachment directory found:", attach_file_path)
                        break

        if attach_file_path is not None and os.path.isdir(attach_file_path):
            self.get_all_files(attach_file_path)
        print("Attachment directory path:", attach_file_path)
        print("PO Attachments:", self.po_attachments)
        return self.po_attachments

    # Get all files inside the attachments and popdf's
    def get_all_files(self, path):
        if os.path.exists(path):
            if os.path.isfile(path):
                modified_path = path.replace('&', '%26')
                self.po_attachments.append((modified_path, os.path.basename(path)))
            elif os.path.isdir(path):
                for subfile in os.listdir(path):
                    subfile_path = os.path.join(path, subfile)  # Use os.path.join for path concatenation
                    self.get_all_files(subfile_path)  # Recursively call get_all_files for subdirectories

    # Get POPDF files by Header guid
    def arch_get_popdf(self, request, hdr_guid):
        file_set = set()  # Use a set to store unique file names
        file_list = []
        objid = arch_PoHeader.get_objid_by_guid(hdr_guid)
        client = getClients(request)  # To get the logged-in user's client

        # Construct the pdf_path similar to attachment path
        pdf_path = os.path.join(settings.MEDIA_ROOT, settings.ATTACH_PATH, str(client), 'POPDF', 'PO_' + objid)

        if os.path.exists(pdf_path):
            directory = os.listdir(pdf_path)
            for files in directory:
                fname = os.path.join(pdf_path, files)
                fname = fname.replace('&', '%26')

                # Check for duplicates before adding to the list
                if files not in file_set:
                    pdf = (fname, files)
                    file_list.append(pdf)
                    file_set.add(files)
        print("PDF directory path:", pdf_path)
        print("POPDF List:", file_list)
        return file_list

