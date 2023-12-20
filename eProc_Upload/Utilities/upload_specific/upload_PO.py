
"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    upload_specific.py
Usage:
    stores extracted data into respective db table
    1. upload_SC -store sc extract(.csv) data into MSS_SC_HEADER,MSS_SC_ITEM,MSS_SC_APPROVAL,MSS_SC_ACCOUNTING db tables
    2. upload_PO -store PO extract(.csv) data into MSS_PO_HEADER,MSS_PO_ITEM,MSS_PO_APPROVAL,MSS_PO_ACCOUNTING db tables
    3. upload_user- store user extract(.csv) data into MMD_USER_INFO db tables
    4. upload_supplier - store supplier master extract(.csv) data into MMD_SUPPLIER_SEARCH db tables

Author:
    Deepika K/Shreyas
"""

import csv
import uuid
import logging
from datetime import datetime
from decimal import Decimal

from django.contrib import messages
from django.db.models import Q

from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.type_casting import get_date_value, str_decimal
from eProc_Basic.Utilities.messages.messages import *
from eProc_Basic.models import *
from eProc_Configuration.models import OrgClients
from eProc_Purchase_Order.models import *


def upload_PO(req, PO_Data, Test_mode):
    """
    on uploading of PO extracted csv file
    1. filter and get HEAD data from csv file and store its respective field values into MSS_PO_HEADER db table
    2. filter and get ITEM data from csv file and store its respective field values into MSS_PO_ITEM db table
    3. filter and get APP data from csv file and store its respective field values into MSS_PO_APPROVAL db table
    4. filter and get ACC data from csv file and store its respective field values into MSS_PO_ACCOUNTING db table
    :param req: UI request
    :param PO_Data: attached csv file data
    :return: return true on success, return false on failure
    """
    try:
        po_line_no = 0
        client = getClients ( req )
        created = False
        for column in csv.reader ( PO_Data, delimiter=',', quotechar='"' ):
            po_line_no = po_line_no + 1
            print ( "PO Extract Line Number:" + str ( po_line_no ) )
            if (column[0] == "HEAD" or column[0] == "\ufeffHEAD"):
                # Store PoHeader data only if PoHeader guid is not present in PoHeader db table
                if (not (PoHeader.objects.filter ( guid=column[1] ).exists () or PoHeader.objects.filter (
                        doc_number=column[2] ).exists ())):
                    _, created = PoHeader.objects.update_or_create ( guid=column[1], doc_number=column[2],
                                                                     version_type=column[3], version_num=column[4],
                                                                     description=column[5],
                                                                     total_value=column[6], currency=column[7],
                                                                     requester=column[8], status=column[9],
                                                                     created_at=get_date_value ( column[10] ),
                                                                     created_by=column[11],
                                                                     changed_at=get_date_value ( column[12] ),
                                                                     changed_by=column[13],
                                                                     ordered_at=get_date_value ( column[14] ),
                                                                     time_zone=column[15],
                                                                     item_cat=column[16], limit=column[17],
                                                                     expected_value=str_decimal ( column[18] ),
                                                                     unlimited=column[19],
                                                                     supplier_id=column[20],
                                                                     client=OrgClients.objects.get ( client=client ) )
                    if (not created):
                        return False
                # if doc_num exist then add doc_num_1
                elif (PoHeader.objects.filter ( doc_number=column[2] ).exists () and not (
                        PoHeader.objects.filter ( guid=column[1] ).exists ())):
                    doc = 1
                    # if doc_number_doc exist then increment doc value
                    while (PoHeader.objects.filter ( doc_number=(column[2] + '_' + str ( doc )) ).exists ()):
                        doc = doc + 1
                        print ( 'doc no exist' )
                    _, created = PoHeader.objects.update_or_create ( guid=column[1],
                                                                     doc_number=(column[2] + '_' + str ( doc )),
                                                                     version_type=column[3], version_num=column[4],
                                                                     description=column[5],
                                                                     total_value=column[6], currency=column[7],
                                                                     requester=column[8], status=column[9],
                                                                     created_at=get_date_value ( column[10] ),
                                                                     created_by=column[11],
                                                                     changed_at=get_date_value ( column[12] ),
                                                                     changed_by=column[13],
                                                                     ordered_at=get_date_value ( column[14] ),
                                                                     time_zone=column[15],
                                                                     item_cat=column[16], limit=column[17],
                                                                     expected_value=str_decimal ( column[18] ),
                                                                     unlimited=column[19],
                                                                     supplier_id=column[20],
                                                                     client=OrgClients.objects.get ( client=client ) )

                    if (not created):
                        return False
            elif (column[0] == "ITEM"):
                #  Store PoItem data only if  PoHeader guid present in PoHeader db table or PoItem guid is not present in PoItem db table
                if (PoHeader.objects.filter ( guid=column[2] ).exists () and not (
                        PoItem.objects.filter ( guid=column[1] ).exists ())):
                    _, created = PoItem.objects.update_or_create ( guid=column[1],
                                                                   header_guid=PoHeader.objects.get ( guid=column[2] ),
                                                                   po_item_num=column[3], sc_num=column[4],
                                                                   sc_header_guid=column[5],
                                                                   item_num=str_decimal ( column[6] ),
                                                                   sc_item_guid=column[7], prod_description=column[8],
                                                                   comp_code=column[9], purch_grp=column[10],
                                                                   purch_org=column[11],
                                                                   item_del_date=get_date_value ( column[12] ),
                                                                   prod_cat=column[13],
                                                                   hiring_level=column[14], hiring_role=column[15],
                                                                   hiring_skill=column[16], prod_type=column[17],
                                                                   catalog_id=column[18],
                                                                   unspsc=column[19], fin_entry_ind=column[20],
                                                                   quantity=column[21],
                                                                   price=str_decimal ( column[22] ),
                                                                   price_unit=column[23],
                                                                   unit=column[24],
                                                                   gross_price=str_decimal ( column[25] ),
                                                                   gr_ind=column[26],
                                                                   supp_prod_num=column[27], manu_part_num=column[28],
                                                                   manu_code_num=column[29],
                                                                   ctr_num=column[30], supp_ord_addr=column[31],
                                                                   goods_recep=column[32], bill_to_addr_num=column[33],
                                                                   ship_to_addr_num=column[34],
                                                                   del_srm_purch_doc=column[35], manu_name=column[36],
                                                                   del_time_days=column[37], internal_note=column[38],
                                                                   client=OrgClients.objects.get ( client=client ) )
                    if (not created):
                        return False
            elif (column[0] == "ACC"):
                #  Store PoAccounting data only if PoItem guid present in PoItem db table or PoAccounting guid is not present in PoAccounting db table
                if (PoItem.objects.filter ( guid=column[2] ).exists () and not (
                        PoAccounting.objects.filter ( guid=column[1] ).exists ())):
                    _, created = PoAccounting.objects.update_or_create ( guid=column[1],
                                                                         item_guid=PoItem.objects.get (
                                                                             guid=column[2] ),
                                                                         acc_item_num=str_decimal ( column[3] ),
                                                                         acc_cat=column[4],
                                                                         dist_perc=column[5], gl_acc_num=column[6],
                                                                         cost_center=column[7],
                                                                         internal_order=column[8],
                                                                         generic_acc_ass=column[9],
                                                                         wbs_ele=column[10], project=column[11],
                                                                         task_id=column[12],
                                                                         client=OrgClients.objects.get (
                                                                             client=client ) )
                    if (not created):
                        return False
            elif (column[0] == "APP"):
                #  Store PoApproval data only if PoHeader guid present in PoHeader db table
                if (PoHeader.objects.filter ( guid=column[1] ).exists ()):
                    _, created = PoApproval.objects.update_or_create ( guid=uuid.uuid4 ().hex.upper (),
                                                                       header_guid=PoHeader.objects.get (
                                                                           guid=column[1] ),
                                                                       step_num=column[2], app_desc=column[3],
                                                                       proc_lvl_sts=column[4],
                                                                       app_sts=column[5], app_id=column[6],
                                                                       received_time=get_date_value ( column[7] ),
                                                                       proc_time=get_date_value ( column[8] ),
                                                                       time_zone=column[9],
                                                                       client=OrgClients.objects.get ( client=client ) )
                    if (not created):
                        return False

        PoHeader_DB_count = PoHeader.objects.filter.count ()
        PoItem_DB_count = PoItem.objects.filter.count ()
        PoAccounting_DB_count= PoAccounting.objects.filter.count ()

        messages.success ( req, ' Number of Records PO Header in Database    : ' + str ( PoHeader_DB_count ) )
        messages.success ( req, ' Number of Records PO Item in Database    : ' + str ( PoItem_DB_count ) )
        messages.success ( req, ' Number of Records PO Accounting in Database    : ' + str ( PoAccounting_DB_count ) )


        return True
    except Exception as e:
        print ( e )
        return False

