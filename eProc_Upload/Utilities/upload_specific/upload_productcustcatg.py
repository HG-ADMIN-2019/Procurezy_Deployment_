import csv
from django.contrib import messages
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.models import *
from eProc_Basic.Utilities.messages.messages import *


# # upload Product Cust Cat csv data file into Product Cust Cat db table - Shankar - SP10-19
from eProc_Configuration.models import UnspscCategories, OrgClients, UnspscCategoriesCustDesc


def upload_productcustcatg(req, Prodcustcat, Test_mode):
#     """
#     on uploading of Product Cust Cat  csv file
#     1. GET Product Cust Cat csv file and store its respective field values into MMD_PROD_CUST_CAT db table
#     :param req: UI request
#     :param Language: attached csv file data
#     :param Test_mode : Diagnostics
#     :return: return true on success, return false on failure
#     """
#

    try:

        client = getClients(req)

        # If the Test Mode check box is checked then run diagnostics.

        if Test_mode == 'on'  :

            Test_prodcatcust_DB_count              = 0
            Test_Insert_Count_prodcatcust          = 0
            Test_Update_Count_prodcatcust          = 0
            Test_Duplicate_Count_prodcatcust       = 0
            Test_Delete_Count_prodcatcust          = 0
            Test_File_Count_prodcatcust            = 0
            Test_Delete_Err_Count_prodcatcust      = 0
            Test_prodcatcust_delete_error          = ''
            Test_prodcatcust_number_list           = []


            Data_saved = ''

            Test_prodcatcust_DB_count = UnspscCategoriesCustDesc.objects.filter(del_ind=False).count ()

            # Read thru the file record by record , Assign column based on comma delimter

            for column in csv.reader ( Prodcustcat, delimiter=',', quotechar='"' ):
                Test_File_Count_prodcatcust = Test_File_Count_prodcatcust + 1
                print ( "Product Cust Cat Extract Line Number:" + str ( Test_File_Count_prodcatcust ) )

                del_ind_field = column[2]

                # If the Input file Deletion indicator is "0" (Insert\Update record) and Lang  exist in the Lang table

                if (del_ind_field == '0') and (UnspscCategoriesCustDesc.objects.filter(prod_cat_id=column[1], client=client).exists()):
                    queryset_test_upd = UnspscCategoriesCustDesc.objects.filter ( prod_cat_id=column[1], client=client)
                    for test in queryset_test_upd:
                        if test.description != column[1]  :
                            Test_Update_Count_prodcatcust = Test_Update_Count_prodcatcust + 1
                        else  :
                            Test_Duplicate_Count_prodcatcust = Test_Duplicate_Count_prodcatcust + 1

                # If the Input file Deletion indicator is "0" (Insert\Update record) and Lang key  does not exist in the Lang table

                elif (del_ind_field == '0') and (not (UnspscCategoriesCustDesc.objects.filter(prod_cat_id=column[1], client=client).exists ())):
                    if column[0] in Test_prodcatcust_number_list:
                        Test_Duplicate_Count_prodcatcust = Test_Duplicate_Count_prodcatcust + 1
                        error_msg = get_message_desc(MSG094)[1]
                        # msgid = 'MSG094'
                        # error_msg = get_msg_desc(msgid)
                        # msg = error_msg['message_desc'][0]
                        # error_msg = msg
                        Test_prodcatcust_errmsg_duplicate = error_msg
                    else:
                        Test_Insert_Count_prodcatcust = Test_Insert_Count_prodcatcust + 1

                # Check  If the Input file Deletion indicator is "1" (Delete record) and if record  exists
                # Check if the record is active on DB.

                if (del_ind_field == '1') and (UnspscCategoriesCustDesc.objects.filter(prod_cat_id=column[1], client=client).exists ()):
                    queryset_test_del = UnspscCategoriesCustDesc.objects.filter ( prod_cat_id=column[1], client=client )
                    for test in queryset_test_del:
                        if test.del_ind == False    :
                            Test_Delete_Count_prodcatcust = Test_Delete_Count_prodcatcust +1

                # Check  If the Input file Deletion indicator is "1" (Delete record) and if record does not exists
                # report as invalid record.


                elif (del_ind_field == '1') and (not(UnspscCategoriesCustDesc.objects.filter(prod_cat_id=column[1], client=client).exists ())):
                       Test_prodcatcust_delete_error = 'Y'
                       Test_Delete_Err_Count_prodcatcust = Test_Delete_Err_Count_prodcatcust + 1


                # Append the input key to the Array list for checking the next reocrds for dups.

                Test_prodcatcust_number_list.append(column[0])

            messages.info ( req, 'Test Mode Diagnostics:' )
            messages.info ( req, '-----------------------------' )

            #Display insert /updated count in the display
            messages.success ( req, ' Number of Records in Database    : ' + str ( Test_prodcatcust_DB_count ))
            # Number of records in the Input file.
            messages.success ( req, ' Number of Records in Input file  : ' + str ( Test_File_Count_prodcatcust ))
            # Total records that need to be inserted.
            messages.success ( req, ' Records to be Inserted           : ' + str ( Test_Insert_Count_prodcatcust ))
            # Total records that need to be Updated.
            messages.success ( req, ' Records to be Updated            : ' + str ( Test_Update_Count_prodcatcust ))
            # Total records that need to be Deleted.
            messages.success ( req, ' Records to be Deleted            : ' + str ( Test_Delete_Count_prodcatcust ))
            # Total records that are duplicate in the input file
            messages.error   ( req, ' Duplicate records                : ' + str ( Test_Duplicate_Count_prodcatcust ) )

            # Display the number of delete records that dont exist on DB
            if Test_prodcatcust_delete_error != '':
                messages.error ( req, ' Input Delete records that dont exist in DB : ' + str ( Test_Delete_Err_Count_prodcatcust ))

            # Display error message for empty file
            if Test_File_Count_prodcatcust == 0:
                messages.error ( req, ' Empty File : Please correct and try again ' )


        elif Test_mode != 'on' :

            prodcatcust_line_no = 0
            prodcatcust_inserted_cnt = 0
            prodcatcust_updated_cnt = 0
            prodcatcust_deleted_cnt = 0
            prodcatcust_duplicate_cnt = 0
            Lang_DB_count = 0
            Lang_delete_Err_Count    = 0
            Lang_delete_error        = ''
            Data_saved          = ''

            for column in csv.reader ( Prodcustcat, delimiter=',', quotechar='"' ):
                prodcatcust_line_no = prodcatcust_line_no + 1
                print ( "Product Cust Cat Extract Line Number:" + str ( prodcatcust_line_no ) )

                del_ind_field = column[2]

                # If the Deletion indicator in the file = "0" and record does not exist on the DB : INSERT DB

                if (del_ind_field == '0') and (not (UnspscCategoriesCustDesc.objects.filter(prod_cat_id=column[1], client=client).exists ())):
                    _, created = UnspscCategoriesCustDesc.objects.get_or_create(
                                            prod_cat_id=UnspscCategories.objects.get( prod_cat_id=column[1]),
                                            del_ind=column[2],
                                            client=OrgClients.objects.get(client=client)
                    )
                    prodcatcust_inserted_cnt = prodcatcust_inserted_cnt +1
                    Data_saved            = 'Y'

                # If the Deletion indicator in the file = "0" and record  exist on the DB : Update DB

                elif (del_ind_field == '0') and (UnspscCategoriesCustDesc.objects.filter(prod_cat_id=column[1], client=client).exists()):
                    UnspscCategoriesCustDesc.objects.filter ( prod_cat_id=column[1], client=client ).update \
                                ( client=OrgClients.objects.get ( client=client ), del_ind=column[2] )
                    prodcatcust_updated_cnt = prodcatcust_updated_cnt + 1
                    Data_saved            = 'Y'

                # If the Deletion indicator in the file = "1" and record  exist on the DB : Soft Delete(del_ind =0) DB

                if (del_ind_field == '1') and (UnspscCategoriesCustDesc.objects.filter(prod_cat_id=column[1], client=client).exists ()):
                    queryset_del = UnspscCategoriesCustDesc.objects.filter ( prod_cat_id=column[1], client=client )
                    for test in queryset_del:
                        if test.del_ind == False    :
                            UnspscCategoriesCustDesc.objects.filter( prod_cat_id=column[1], client=client).update( del_ind=1)
                            prodcatcust_deleted_cnt  = prodcatcust_deleted_cnt +1
                            Data_saved            = 'Y'

                # If the Deletion indicator in the file = "1" and record  does not exist on the DB : Error message

                elif (del_ind_field == '1') and (not (UnspscCategoriesCustDesc.objects.filter (prod_cat_id=column[1], client=client).exists ())):
                    Lang_delete_error = 'Y'
                    Lang_delete_Err_Count = Lang_delete_Err_Count + 1



            #Display insert /updated count in the display
            Lang_DB_count = UnspscCategoriesCustDesc.objects.filter(del_ind=0).count ()



            messages.info ( req, 'Database Upload Results  :')
            messages.info ( req, '-------------------------------' )

            # Display the number of Active records in DB
            messages.success ( req, ' Number of Records in Database    : ' + str ( Lang_DB_count ))
            # Display the number of  records in file
            messages.success ( req, ' Number of Records in Input file  : ' + str ( prodcatcust_line_no ))
            # Display the number of records Inserted
            messages.success ( req, ' Records Inserted      : ' + str( prodcatcust_inserted_cnt ))
            # Display the number of records Updated
            messages.success ( req, ' Records Updated       : ' + str( prodcatcust_updated_cnt ))
            # Display the number of records Deleted
            messages.success ( req, ' Records Deleted       : ' + str( prodcatcust_deleted_cnt ))

            if prodcatcust_line_no == 0:
                messages.error ( req, ' Empty File : Please correct and try again ' )

            # Display error message if delete record doesnt exist on DB
            if Lang_delete_error != '':
                messages.error ( req,' Input Delete records that dont exist in DB : ' + str ( Lang_delete_Err_Count ) )


        if Data_saved == 'Y':
            error_msg = get_message_desc(MSG037)[1]
            # msgid = 'MSG037'
            # error_msg = get_msg_desc(msgid)
            messages.success(req, error_msg)
            # messages.success ( req, MSG037 )
        else:
            error_msg = get_message_desc(MSG043)[1]
            # msgid = 'MSG043'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            messages.error(req, error_msg)
            # messages.error ( req, MSG043 )

    except Exception as e:
        print ( e )
        messages.error ( req, 'Error : ' + str(e) )


