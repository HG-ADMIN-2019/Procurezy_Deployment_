from datetime import datetime
import csv
from django.db.models import Max, Q
from decimal import Decimal
import uuid

from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.type_casting import get_date_value, str_decimal
from eProc_Basic.Utilities.db_queries import getClients
from eProc_Archiving.models import arch_CountryCompCode, arch_ScHeader, arch_ScItem, arch_ScAccounting, arch_ScApproval, \
    arch_PoHeader, arch_PoItem, arch_PoAccounting, arch_PoApproval, ConfHeader, ConfItem, ConfAccounting, \
    arch_UserSearch, arch_SupplierSearch, arch_CompanyCode
from eProc_Configuration.models import OrgClients, Country
from eProc_Doc_Search.models import *
from eProc_Basic.models import *


class UploadScPO:

    def upload_SC(self, request, SC_Data):
        try:
            client = getClients(request)
            sc_line_no=0
            for column in csv.reader(SC_Data, delimiter=',', quotechar='"'):
                sc_line_no = sc_line_no+1
                print("SC Extract Line Number:" + str(sc_line_no))
                # get SC Header data from attached file and store it to SC header db table
                if column[0] == "HEAD" or column[0] == "\ufeffHEAD":
                    # Store ScHeader data only if ScHeader guid is not present in ScHeader db table
                    if not(arch_ScHeader.objects.filter(guid=column[1]).exists()):
                        _, created = arch_ScHeader.objects.update_or_create(guid=column[1],
                                                                       doc_number=column[2], description=column[3],
                                                                       total_value=column[4], currency=column[5],
                                                                       requester=column[6], status=column[7],
                                                                       created_at=get_date_value(column[8]),
                                                                       created_by=column[9],
                                                                       changed_at=get_date_value(column[10]),
                                                                       changed_by=column[11],
                                                                       ordered_at=get_date_value(column[12]),
                                                                       time_zone=column[13], client=OrgClients.objects.get(client=client))
                        if not created:
                            return False
                # get SC item data from attached file and store it to SC item db table
                elif column[0] == "ITEM":
                    #  Store ScItem data only if  ScHeader guid present in ScHeader db table or ScItem guid is not present in ScItem db table
                    if (arch_ScHeader.objects.filter(guid=column[2]).exists()) and (not (arch_ScItem.objects.filter(guid=column[1]).exists())):
                        _, created = arch_ScItem.objects.update_or_create(guid=column[1],
                                                                     header_guid=arch_ScHeader.objects.get(guid=column[2]),
                                                                     client = OrgClients.objects.get(client=client),
                                                                     item_num=column[3], po_num=column[4],
                                                                     po_item_num=column[5],
                                                                     prod_description=column[6], comp_code=column[7],
                                                                     purch_grp=column[8], purch_org=column[9],
                                                                     supplier_id=column[10],
                                                                     item_cat=column[11], prod_cat=column[12],
                                                                     hiring_level=column[13], hiring_role=column[14],
                                                                     hiring_skill=column[15],
                                                                     prod_type=column[16], catalog_id=column[17],
                                                                     unspsc=column[18],
                                                                     fin_entry_ind=column[19], item_del_date=get_date_value(column[20]),
                                                                     quantity=column[21], price=str_decimal(column[22]),
                                                                     price_unit=column[23],
                                                                     unit=column[24], gross_price=str_decimal(column[25]),
                                                                     overall_limit=str_decimal(column[26]),
                                                                     expected_value=str_decimal(column[27]),
                                                                     undef_limit=str_decimal(column[28]),
                                                                     gr_ind=column[29], dis_rej_ind=column[30],
                                                                     supp_prod_num=column[31],
                                                                     manu_part_num=column[32], manu_code_num=column[33],
                                                                     status=column[34], ctr_num=column[35],
                                                                     supp_ord_addr=column[36],
                                                                     goods_recep=column[37], bill_to_addr_num=column[38],
                                                                     ship_to_addr_num=column[39],
                                                                     manu_name=column[40],
                                                                     supp_txt=column[41], internal_note=column[42])
                        if (not created):
                            return False
                # get SC Accounting data from attached file and store it to SC Accounting db table
                elif (column[0] == "ACC"):
                    #  Store ScAccounting data only if ScItem guid present in ScItem db table or ScAccounting guid is not present in ScAccounting db table
                    if ((arch_ScItem.objects.filter(guid=column[2]).exists()) and (not (arch_ScAccounting.objects.filter(guid=column[1]).exists()))):
                        _, created = arch_ScAccounting.objects.update_or_create(guid=column[1],
                                                                           item_guid=arch_ScItem.objects.get(guid=column[2]),
                                                                           acc_item_num=Decimal(column[3]), acc_cat=column[4],
                                                                           dist_perc=column[5], gl_acc_num=column[6],
                                                                           cost_center=column[7], internal_order=column[8],
                                                                           generic_acc_ass=column[9],
                                                                           wbs_ele=column[10], project=column[11],
                                                                           task_id=column[12],client=OrgClients.objects.get(client=client))
                        if (not created):
                            return False
                # get SC Approval data from attached file and store it to SC Approval db table
                elif (column[0] == "APP"):
                    #  Store ScApproval data only if ScHeader guid present in ScHeader db table
                    if ( not (arch_ScApproval.objects.filter(Q(header_guid=column[1]) & Q(step_num=column[2]) & Q(app_desc=column[3])
                                                        & Q(proc_lvl_sts=column[4])&Q(app_sts=column[5]) & Q(app_id=column[6]) &
                                                        Q(recevied_time=get_date_value(column[7]))& Q(proc_time=get_date_value(column[8])) &
                                                        Q(time_zone=column[9])).exists())):
                        _, created = arch_ScApproval.objects.update_or_create(guid=uuid.uuid4().hex.upper(),
                                                                         header_guid=arch_ScHeader.objects.get(guid=column[1]),
                                                                         step_num=column[2], app_desc=column[3],
                                                                         proc_lvl_sts=column[4],
                                                                         app_sts=column[5], app_id=column[6],
                                                                         recevied_time=get_date_value(column[7]),
                                                                         proc_time=get_date_value(column[8]),
                                                                         time_zone=column[9],client=OrgClients.objects.get(client=client))
                        if (not created):
                            return False
            return True
        except Exception as e:
            print(e)
            return False

        return False

    def upload_PO(self,request,PO_Data):
        try:
            po_line_no=0
            client = getClients(request)
            created=False
            for column in csv.reader(PO_Data, delimiter=',', quotechar='"'):
                po_line_no=po_line_no+1
                print("PO Extract Line Number:" + str(po_line_no))
                if (column[0] == "HEAD" or column[0] == "\ufeffHEAD"):
                    # Store PoHeader data only if PoHeader guid is not present in PoHeader db table
                    if (not (arch_PoHeader.objects.filter(guid=column[1]).exists() or arch_PoHeader.objects.filter(doc_number=column[2]).exists() ) ):
                        _, created = arch_PoHeader.objects.update_or_create(guid=column[1], doc_number=column[2],
                                                                       version_type=column[3], version_num=column[4],
                                                                       description=column[5],
                                                                       total_value=column[6], currency=column[7],
                                                                       requester=column[8], status=column[9],
                                                                       created_at=get_date_value(column[10]),
                                                                       created_by=column[11], changed_at=get_date_value(column[12]),
                                                                       changed_by=column[13], ordered_at=get_date_value(column[14]),
                                                                       time_zone=column[15],
                                                                       item_cat=column[16], limit=column[17],
                                                                       expected_value=str_decimal(column[18]), unlimited=column[19],
                                                                       supplier_id=column[20],client=OrgClients.objects.get(client=client))
                        if (not created):
                            return False
                    # if doc_num exist then add doc_num_1
                    elif(arch_PoHeader.objects.filter(doc_number=column[2]).exists() and not (arch_PoHeader.objects.filter(guid=column[1]).exists())):
                        doc=1
                        # if doc_number_doc exist then increment doc value
                        while(arch_PoHeader.objects.filter(doc_number=(column[2]+'_'+str(doc))).exists() ):
                            doc=doc+1
                            print('doc no exist')
                        _, created = arch_PoHeader.objects.update_or_create(guid=column[1], doc_number=(column[2]+'_'+str(doc)),
                                                                       version_type=column[3], version_num=column[4],
                                                                       description=column[5],
                                                                       total_value=column[6], currency=column[7],
                                                                       requester=column[8], status=column[9],
                                                                       created_at=get_date_value(column[10]),
                                                                       created_by=column[11],
                                                                       changed_at=get_date_value(column[12]),
                                                                       changed_by=column[13],
                                                                       ordered_at=get_date_value(column[14]),
                                                                       time_zone=column[15],
                                                                       item_cat=column[16], limit=column[17],
                                                                       expected_value=str_decimal(column[18]),
                                                                       unlimited=column[19],
                                                                       supplier_id=column[20],
                                                                       client=OrgClients.objects.get(client=client))

                        if (not created):
                            return False
                elif (column[0] == "ITEM"):
                    #  Store PoItem data only if  PoHeader guid present in PoHeader db table or PoItem guid is not present in PoItem db table
                    if (arch_PoHeader.objects.filter(guid=column[2]).exists() and not(arch_PoItem.objects.filter(guid=column[1]).exists())):
                        _, created = arch_PoItem.objects.update_or_create(guid=column[1],
                                                                     header_guid=arch_PoHeader.objects.get(guid=column[2]),
                                                                     po_item_num=column[3], sc_num=column[4],
                                                                     sc_header_guid=column[5], item_num=str_decimal(column[6]),
                                                                     sc_item_guid=column[7], prod_description=column[8],
                                                                     comp_code=column[9], purch_grp=column[10],
                                                                     purch_org=column[11], item_del_date=get_date_value(column[12]),
                                                                     prod_cat=column[13],
                                                                     hiring_level=column[14], hiring_role=column[15],
                                                                     hiring_skill=column[16], prod_type=column[17],
                                                                     catalog_id=column[18],
                                                                     unspsc=column[19], fin_entry_ind=column[20],
                                                                     quantity=column[21], price=str_decimal(column[22]),
                                                                     price_unit=column[23],
                                                                     unit=column[24],
                                                                     gross_price=str_decimal(column[25]), gr_ind=column[26],
                                                                     supp_prod_num=column[27], manu_part_num=column[28],
                                                                     manu_code_num=column[29],
                                                                     ctr_num=column[30], supp_ord_addr=column[31],
                                                                     goods_recep=column[32], bill_to_addr_num=column[33],
                                                                     ship_to_addr_num=column[34],
                                                                     del_srm_purch_doc=column[35], manu_name=column[36],
                                                                     del_time_days=column[37], internal_note=column[38],client=OrgClients.objects.get(client=client))
                        if (not created):
                            return False
                elif (column[0] == "ACC"):
                    #  Store PoAccounting data only if PoItem guid present in PoItem db table or PoAccounting guid is not present in PoAccounting db table
                    if (arch_PoItem.objects.filter(guid=column[2]).exists() and not(arch_PoAccounting.objects.filter(guid=column[1]).exists()) ):
                        _, created = arch_PoAccounting.objects.update_or_create(guid=column[1],
                                                                           item_guid=arch_PoItem.objects.get(guid=column[2]),
                                                                           acc_item_num=str_decimal(column[3]), acc_cat=column[4],
                                                                           dist_perc=column[5], gl_acc_num=column[6],
                                                                           cost_center=column[7], internal_order=column[8],
                                                                           generic_acc_ass=column[9],
                                                                           wbs_ele=column[10], project=column[11],
                                                                           task_id=column[12],client=OrgClients.objects.get(client=client))
                        if (not created):
                            return False
                elif (column[0] == "APP"):
                    #  Store PoApproval data only if PoHeader guid present in PoHeader db table
                    if (arch_PoHeader.objects.filter(guid=column[1]).exists()):
                        _, created = arch_PoApproval.objects.update_or_create(guid=uuid.uuid4().hex.upper(),
                                                                         header_guid=arch_PoHeader.objects.get(guid=column[1]),
                                                                         step_num=column[2], app_desc=column[3],
                                                                         proc_lvl_sts=column[4],
                                                                         app_sts=column[5], app_id=column[6],
                                                                         recevied_time=get_date_value(column[7]), proc_time=get_date_value(column[8]),
                                                                         time_zone=column[9],client=OrgClients.objects.get(client=client))
                        if (not created):
                            return False

            return True
        except Exception as e:
            print(e)
            return False

    def upload_confirmation(self,req,PO_Data):
        try:
            confirmation_line_no=0
            client = getClients(req)
            created=False
            for column in csv.reader(PO_Data, delimiter=',', quotechar='"'):
                confirmation_line_no=confirmation_line_no+1
                print("Confirmation Extract Line Number:" + str(confirmation_line_no))
                if (column[0] == "HEAD" or column[0] == "\ufeffHEAD"):
                    # Store PoHeader data only if PoHeader guid is not present in PoHeader db table
                    if (not (ConfHeader.objects.filter(guid=column[1]).exists() or ConfHeader.objects.filter(doc_number=column[2]).exists() ) ):
                        _, created = ConfHeader.objects.update_or_create(guid=column[1],
                                                                         doc_number=column[2],
                                                                         conf_sub_type=column[3],
                                                                         description=column[4],
                                                                         total_value=column[5],
                                                                         currency=column[6],
                                                                         requester=column[7],
                                                                         status=column[8],
                                                                         created_at=get_date_value(column[9]),
                                                                         created_by=column[10],
                                                                         changed_at=get_date_value(column[11]),
                                                                         changed_by=column[12],
                                                                         ordered_at=get_date_value(column[13]),
                                                                         time_zone=column[14],
                                                                         supplier_id=column[15],
                                                                         supplier_name = column[16],
                                                                         conf_movement=column[17],
                                                                         po_doc_number=column[18],
                                                                         del_ind = False,
                                                                         client=OrgClients.objects.get(client=client))
                        if (not created):
                            return False
                    # if doc_num exist then add doc_num_1
                    elif(ConfHeader.objects.filter(doc_number=column[2]).exists() and not (ConfHeader.objects.filter(guid=column[1]).exists())):
                        doc=1
                        # if doc_number_doc exist then increment doc value
                        while(ConfHeader.objects.filter(doc_number=(column[2]+'_'+str(doc))).exists() ):
                            doc=doc+1
                            print('doc no exist')
                        ConfHeader.objects.update_or_create(guid=column[1],
                                                            doc_number=(column[2]+'_'+str(doc)),
                                                            conf_sub_type=column[3],
                                                            description=column[4],
                                                            total_value=column[5],
                                                            currency=column[6],
                                                            requester=column[7],
                                                            status=column[8],
                                                            created_at=get_date_value(column[9]),
                                                            created_by=column[10],
                                                            changed_at=get_date_value(column[11]),
                                                            changed_by=column[12],
                                                            ordered_at=get_date_value(column[13]),
                                                            time_zone=column[14],
                                                            supplier_id=column[15],
                                                            supplier_name=column[16],
                                                            conf_movement=column[17],
                                                            po_doc_number=column[18],
                                                            del_ind=False,
                                                            client=OrgClients.objects.get(client=client))

                        if (not created):
                            return False
                elif (column[0] == "ITEM"):
                    #  Store PoItem data only if  PoHeader guid present in PoHeader db table or PoItem guid is not present in PoItem db table
                    if (ConfHeader.objects.filter(guid=column[2]).exists() and not(ConfItem.objects.filter(guid=column[1]).exists())):
                        _, created = ConfItem.objects.update_or_create(guid=column[1],
                                                                       header_guid=ConfHeader.objects.get(guid=column[2]),
                                                                       item_num = column[3],
                                                                       po_item_num=column[4],
                                                                       ref_item_guid=column[5],
                                                                       prod_description=column[6],
                                                                       comp_code=column[7],
                                                                       purch_grp=column[8],
                                                                       purch_org=column[9],
                                                                       po_item_del_date=get_date_value(column[10]),
                                                                       del_note_date = get_date_value(column[11]),
                                                                       prod_cat=column[12],
                                                                       prod_type=column[13],
                                                                       catalog_id=column[14],
                                                                       unspsc=column[15],
                                                                       quantity=column[16],
                                                                       price=column[17],
                                                                       price_unit=column[18],
                                                                       unit=column[19],
                                                                       gross_price=column[20],
                                                                       supp_prod_num=column[21],
                                                                       manu_part_num=column[22],
                                                                       manu_code_num=column[23],
                                                                       ctr_num=column[24],
                                                                       goods_recep=column[25],
                                                                       del_ind = False,
                                                                       client=OrgClients.objects.get(client=client))
                        if (not created):
                            return False
                elif (column[0] == "ACC"):
                    #  Store PoAccounting data only if PoItem guid present in PoItem db table or PoAccounting guid is not present in PoAccounting db table
                    if (ConfItem.objects.filter(guid=column[2]).exists() and not(ConfAccounting.objects.filter(guid=column[1]).exists()) ):
                        _, created = ConfAccounting.objects.update_or_create(guid=column[1],
                                                                             item_guid=ConfItem.objects.get(guid=column[2]),
                                                                             acc_item_num=int(column[3]),
                                                                             acc_cat=column[4],
                                                                             dist_perc=column[5],
                                                                             gl_acc_num=column[6],
                                                                             cost_center=column[7],
                                                                             internal_order=column[8],
                                                                             generic_acc_ass=column[9],
                                                                             wbs_ele=column[10],
                                                                             project=column[11],
                                                                             task_id=column[12],
                                                                             del_ind = False,
                                                                             client=OrgClients.objects.get(client=client))
                        if (not created):
                            return False

            return True
        except Exception as e:
            print(e)
            return False

    # upload user extracted date into UserSearch db table
    def upload_user(self, request,User_Data):
        try:
            client = getClients(request)
            user_line_no=0
            for column in csv.reader(User_Data, delimiter=',', quotechar='"'):
                user_line_no = user_line_no+1
                print("User Extract Line Number:" + str(user_line_no))
                if (not (arch_UserSearch.objects.filter(Q(username=column[0]) & Q(client=client)).exists())):
                    # get User data from attached file and store it to User db table
                    _, created = arch_UserSearch.objects.update_or_create(username=(column[0]),first_name=column[9],last_name=column[1],map_id=uuid.uuid4().hex[:8].upper(),
                                                                    client=OrgClients.objects.get(client=client))

            return True
        except Exception as e:
            print(e)
            return False

        return False

    # upload Supplier extracted date into SupplierSearch db table
    def upload_supplier(self, request,supplier_Data):
        try:
            client = getClients(request)
            supplier_line_no=0
            for column in csv.reader(supplier_Data, delimiter=',', quotechar='"'):
                supplier_line_no = supplier_line_no+1
                print("Supplier Extract Line Number:" + str(supplier_line_no))
                if (not (arch_SupplierSearch.objects.filter(Q(supplier_id=column[1]) & Q(client=client)).exists())):
                    _, created = arch_SupplierSearch.objects.update_or_create(supplier_id=(column[1]),  first_name=column[3],
                                                                    last_name=column[4],map_id=uuid.uuid4().hex[:8].upper(),client=OrgClients.objects.get(client=client))
            return True
        except Exception as e:
            print(e)
            return False

        return False

        # upload Supplier extracted date into SupplierSearch db table
    def upload_country_ccode(self, request, supplier_Data):
        try:
            client = getClients(request)
            supplier_line_no = 0
            for column in csv.reader(supplier_Data, delimiter=',', quotechar='"'):
                supplier_line_no = supplier_line_no + 1
                print("country cmp code Extract Line Number:" + str(supplier_line_no))
                if (not (arch_CountryCompCode.objects.filter(company_code_id=column[0],client=client).exists())):
                    _, created = arch_CountryCompCode.objects.update_or_create(country_comp_code_guid = guid_generator(),
                                                                          company_code_id=(column[0]),
                                                                          country = Country.objects.get(country_code=column[1]),
                                                                          del_ind =False,
                                                                          client=OrgClients.objects.get(client=client))
            return True
        except Exception as e:
            print(e)
            return False

    def Upload_country(self, request,country_data):
        try:
            client = getClients(request)
            country_line_no = 0
            for column in csv.reader(country_data, delimiter=',', quotechar='"'):
                country_line_no = country_line_no + 1
                print("country cmp code Extract Line Number:" + str(country_line_no))
                print(country_data)
                if (not (Country.objects.filter(country_code=column[0]).exists())):
                    _, created = Country.objects.update_or_create(country_code = column[0],
                                                                  country_name = column[1],
                                                                  del_ind =False )
            return True
        except Exception as e:
            print(e)
            return False

    def Upload_cocode(self, request, ccode_data):
        try:
            client = getClients(request)
            supplier_line_no = 0
            for column in csv.reader(ccode_data, delimiter=',', quotechar='"'):
                supplier_line_no = supplier_line_no + 1
                print("country cmp code Extract Line Number:" + str(supplier_line_no))
                print(ccode_data)
                if (not (arch_CompanyCode.objects.filter(company_code_id=column[0],client=client).exists())):
                    _, created = arch_CompanyCode.objects.update_or_create(company_code_guid = guid_generator(),
                                                                          company_code_id=column[0],
                                                                          company_code_desc = column[1],
                                                                          del_ind =False,
                                                                          client=OrgClients.objects.get(client=client))
            return True
        except Exception as e:
            print(e)
            return False

