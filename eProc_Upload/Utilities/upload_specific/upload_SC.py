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
from eProc_Shopping_Cart.models import ScHeader, ScItem, ScAccounting, ScApproval


def upload_SC(req, SC_Data, Test_mode):
    """
    on uploading of SC extracted csv file
    1. filter and get HEAD data from csv file and store its respective field value into MSS_SC_HEADER db table
    2. filter and get ITEM data from csv file and store its respective field value into MSS_SC_ITEM db table
    3. filter and get APP data from csv file and store its respective field value into MSS_SC_APPROVAL db table
    4. filter and get ACC data from csv file and store its respective field value into MSS_SC_ACCOUNTING db table
    :param req: UI request
    :param SC_Data: attached csv file data
    :return: return true on success, return false on failure
    """
    try:
        client = getClients ( req )
        sc_line_no = 0
        for column in csv.reader ( SC_Data, delimiter=',', quotechar='"' ):
            sc_line_no = sc_line_no + 1
            print ( "SC Extract Line Number:" + str ( sc_line_no ) )
            # get SC Header data from attached file and store it to SC header db table
            if (column[0] == "HEAD" or column[0] == "\ufeffHEAD"):
                # Store ScHeader data only if ScHeader guid is not present in ScHeader db table
                if (not (ScHeader.objects.filter ( guid=column[1] ).exists ())):
                    _, created = ScHeader.objects.update_or_create ( guid=column[1],
                                                                     doc_number=column[2], description=column[3],
                                                                     total_value=column[4], currency=column[5],
                                                                     requester=column[6], status=column[7],
                                                                     created_at=get_date_value ( column[8] ),
                                                                     created_by=column[9],
                                                                     changed_at=get_date_value ( column[10] ),
                                                                     changed_by=column[11],
                                                                     ordered_at=get_date_value ( column[12] ),
                                                                     time_zone=column[13],
                                                                     client=OrgClients.objects.get ( client=client ) )
                    if (not created):
                        return False
            # get SC item data from attached file and store it to SC item db table
            elif (column[0] == "ITEM"):
                #  Store ScItem data only if  ScHeader guid present in ScHeader db table or ScItem guid is not present in ScItem db table
                if ((ScHeader.objects.filter ( guid=column[2] ).exists ()) and (
                        not (ScItem.objects.filter ( guid=column[1] ).exists ()))):
                    _, created = ScItem.objects.update_or_create ( guid=column[1],
                                                                   header_guid=ScHeader.objects.get ( guid=column[2] ),
                                                                   client=OrgClients.objects.get ( client=client ),
                                                                   item_num=column[3], po_num=column[4],
                                                                   po_item_num=column[5],
                                                                   prod_cat_desc=column[6], comp_code=column[7],
                                                                   purch_grp=column[8], purch_org=column[9],
                                                                   supplier_id=column[10],
                                                                   item_cat=column[11], prod_cat=column[12],
                                                                   hiring_level=column[13], hiring_role=column[14],
                                                                   hiring_skill=column[15],
                                                                   prod_type=column[16], catalog_id=column[17],
                                                                   unspsc=column[18],
                                                                   fin_entry_ind=column[19],
                                                                   item_del_date=get_date_value ( column[20] ),
                                                                   quantity=column[21],
                                                                   price=str_decimal ( column[22] ),
                                                                   price_unit=column[23],
                                                                   unit=column[24],
                                                                   gross_price=str_decimal ( column[25] ),
                                                                   overall_limit=str_decimal ( column[26] ),
                                                                   expected_value=str_decimal ( column[27] ),
                                                                   undef_limit=str_decimal ( column[28] ),
                                                                   gr_ind=column[29], dis_rej_ind=column[30],
                                                                   supp_prod_num=column[31],
                                                                   manu_part_num=column[32], manu_code_num=column[33],
                                                                   status=column[34], ctr_num=column[35],
                                                                   supp_ord_addr=column[36],
                                                                   goods_recep=column[37], bill_to_addr_num=column[38],
                                                                   ship_to_addr_num=column[39],
                                                                   manu_name=column[40],
                                                                   supp_txt=column[41], internal_note=column[42] )
                    if (not created):
                        return False
            # get SC Accounting data from attached file and store it to SC Accounting db table
            elif (column[0] == "ACC"):
                #  Store ScAccounting data only if ScItem guid present in ScItem db table or ScAccounting guid is not present in ScAccounting db table
                if ((ScItem.objects.filter ( guid=column[2] ).exists ()) and (
                        not (ScAccounting.objects.filter ( guid=column[1] ).exists ()))):
                    _, created = ScAccounting.objects.update_or_create ( guid=column[1],
                                                                         item_guid=ScItem.objects.get (
                                                                             guid=column[2] ),
                                                                         acc_item_num=Decimal ( column[3] ),
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
            # get SC Approval data from attached file and store it to SC Approval db table
            elif (column[0] == "APP"):
                #  Store ScApproval data only if ScHeader guid present in ScHeader db table

                #  Store ScApproval data only if ScHeader guid present in ScHeader db table
                if (
                        not (ScApproval.objects.filter (
                            Q ( header_guid=column[1] ) & Q ( step_num=column[2] ) & Q ( app_desc=column[3] )
                            & Q ( proc_lvl_sts=column[4] ) & Q ( app_sts=column[5] ) & Q (
                                app_id=column[6] ) &
                            Q ( received_time=get_date_value ( column[7] ) ) & Q (
                                proc_time=get_date_value ( column[8] ) ) &
                            Q ( time_zone=column[9] ) ).exists ())):
                    _, created = ScApproval.objects.update_or_create ( guid=uuid.uuid4 ().hex.upper (),
                                                                       header_guid=ScHeader.objects.get (
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


        ScHeader_DB_count = ScHeader.objects.filter().count()
        ScItem_DB_count = ScItem.objects.filter().count()
        ScAccounting_DB_count= ScAccounting.objects.filter().count()
        ScApproval_DB_count= ScApproval.objects.filter().count()

        messages.success ( req, ' Number of Records in SC Header DB     : ' + str ( ScHeader_DB_count ) )
        messages.success ( req, ' Number of Records in SC Item DB       : ' + str ( ScItem_DB_count ) )
        messages.success ( req, ' Number of Records in SC Accounting DB : ' + str ( ScAccounting_DB_count ) )
        messages.success ( req, ' Number of Records in SC APP DB        : ' + str ( ScApproval_DB_count ) )

        return True
    except Exception as e:
        print ( e )
        return False

    return False

