import csv
import uuid
import logging
from datetime import datetime
from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.db.models import Q

from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.models import *
from django.contrib import messages
from eProc_Basic.Utilities.messages.messages import *


# upload Org Model csv data file into MMD_ORG_MODEL db table - Shankar - SP11-13
from eProc_Configuration.models import OrgClients


def upload_orgmodel(req, Orgmodel ,Test_mode):
    """
    on uploading of OrgModel csv file
    1. GET Org Model csv file and store its respective field values into MMD_ORG_MODEL db table
    :param req: UI request
    :param Address: attached csv file data
    :param Test_mode : Diagnostics
    :return: return true on success, return false on failure
    """
    try:

        client = getClients(req)


        # If the Test Mode check box is checked then run diagnostics.
        if Test_mode == 'on':

            # Diagnostics mode variables
            Test_orgmodel_errmsg_country = ''
            Test_orgmodel_errmsg_Language = ''
            Test_orgmodel_errmsg_timezone = ''
            Test_orgmodel_errmsg_duplicate = ''
            Test_orgmodel_error_flag = ''
            Test_orgmodel_DB_count = 0
            Test_Insert_Count_orgmodel = 0
            Test_Update_Count_orgmodel = 0
            Test_Delete_Count_orgmodel = 0
            Test_Duplicate_Count_orgmodel = 0
            Test_File_Count_orgmodel = 0
            Test_Delete_Err_Count_orgmodel = 0
            Test_orgmodel_delete_error = ''
            Test_orgmodel_number_list = []

            Data_saved = ''
            Test_orgmodel_DB_count = OrgModel.objects.filter ( del_ind=False ).count ()

            # Read thru the file record by record , Assign column based on comma delimter
            for column in csv.reader ( Orgmodel, delimiter=',', quotechar='"' ):

                Test_File_Count_orgmodel = Test_File_Count_orgmodel + 1
                del_ind_field = column[4]


                # If the Input file Deletion indicator is "0" (Insert\Update record) and Address\Client key  does not exist in the OrgModeltable

                if (del_ind_field == '0') and (not (OrgModel.objects.filter( object_id=column[0],client=client ).exists ())):
                    if column[1] in Test_orgmodel_number_list:
                        Test_Duplicate_Count_orgmodel = Test_Duplicate_Count_orgmodel + 1
                        error_msg = get_message_desc(MSG094)[1]
                        # msgid = 'MSG094'
                        # error_msg = get_msg_desc(msgid)
                        # msg = error_msg['message_desc'][0]
                        # error_msg = msg
                        Test_orgmodel_errmsg_duplicate = error_msg
                    else:
                        Test_Insert_Count_orgmodel = Test_Insert_Count_orgmodel + 1


                # If the Input file Deletion indicator is "0" (Insert\Update record) and Address\Client key  exist in the OrgModeltable

                # Check if the record on table needs to be updated.
                elif (del_ind_field == '0') and (OrgModel.objects.filter ( object_id=column[0] ,client=client ).exists ()):
                    queryset_test_upd = OrgModel.objects.filter ( object_id=column[0],client=client )
                    for test in queryset_test_upd:

                        if (  test.name  != column[1]    or    test.node_type != column[2]
                                or   test.del_ind != column[3]   ):

                            Test_Update_Count_orgmodel = Test_Update_Count_orgmodel + 1

                # if the record on table is same as input record. increment the Duplicates count
                        else :

                            Test_Duplicate_Count_orgmodel = Test_Duplicate_Count_orgmodel + 1
                            error_msg = get_message_desc(MSG094)[1]
                            # msgid = 'MSG094'
                            # error_msg = get_msg_desc(msgid)
                            # msg = error_msg['message_desc'][0]
                            # error_msg = msg
                            Test_orgmodel_errmsg_duplicate = error_msg


                # If the Input file Deletion indicator is "1" (Delete record) and Address\Client key  exist in the OrgModeltable

                if (del_ind_field == '1') and (OrgModel.objects.filter ( object_id=column[0],client=client ).exists ()):
                    queryset_test_del = OrgModel.objects.filter ( object_id=column[0],client=client )

                # If the Deletion indicator is set to False (active record) , increment Delete counts
                    for test in queryset_test_del:
                        if test.del_ind == False:
                            Test_Delete_Count_orgmodel = Test_Delete_Count_orgmodel + 1

                # If the Input file Deletion indicator is "1" (Delete record) and Address\Client key  does not exist in the OrgModeltable.
                # Raise delete error

                elif (del_ind_field == '1') and (not (OrgModel.objects.filter ( object_id=column[0],client=client ).exists ())):
                    Test_orgmodel_delete_error = 'Y'
                    Test_Delete_Err_Count_orgmodel = Test_Delete_Err_Count_orgmodel + 1

                # Append the processed record to the array list , for validation of next record.
                Test_orgmodel_number_list.append ( column[0] )

            # Display insert /updated count in the display

            messages.info ( req, 'Test Mode Diagnostics:' )
            messages.info ( req, '-----------------------------' )

            # Number of active records on the Database.
            messages.success ( req, ' Number of Records in Database    : ' + str ( Test_orgmodel_DB_count ) )
            # Number of records in the Input file.
            messages.success ( req, ' Number of Records in Input file  : ' + str ( Test_File_Count_orgmodel ) )
            # Total records that need to be inserted.
            messages.success ( req, ' Records to be Inserted           : ' + str ( Test_Insert_Count_orgmodel ) )
            # Total records that need to be Updated.
            messages.success ( req, ' Records to be Updated            : ' + str ( Test_Update_Count_orgmodel ) )
            # Total records that need to be Deleted.
            messages.success ( req, ' Records to be Deleted            : ' + str ( Test_Delete_Count_orgmodel ) )
            # Total records that are duplicate in the input file
            messages.error ( req, ' Duplicate Records                : ' + str ( Test_Duplicate_Count_orgmodel ) )


            # Display error message for delete records that dont exist in the DB
            if Test_orgmodel_delete_error != '':
                messages.error ( req,
                                 ' Input Delete records that dont exist in DB : ' + str ( Test_Delete_Err_Count_orgmodel ) )

            # Display error message for Empty input file
            if Test_File_Count_orgmodel == 0:
                messages.error ( req, ' Empty File : Please correct and try again ' )


        # If the Test Mode check box is Un-checked , Do File processing.

        if Test_mode != 'on':

            client = getClients ( req )
            Orgmodel_line_no = 0
            Orgmodel_inserted_cnt = 0
            Orgmodel_updated_cnt = 0
            Orgmodel_deleted_cnt = 0
            Orgmodel_duplicate_cnt = 0
            Orgmodel_DB_count = 0
            Orgmodel_delete_Err_Count = 0
            Orgmodel_delete_error = ''

            Data_saved = ''

            # Read thru the file record by record , Assign column based on comma delimter

            for column in csv.reader ( Orgmodel, delimiter=',', quotechar='"' ):
                Orgmodel_line_no = Orgmodel_line_no + 1
                print ( "OrgModel Extract Line Number:" + str ( Orgmodel_line_no ) )

                Orgmodel_errmsg_country = ''
                Orgmodel_errmsg_Language = ''
                Orgmodel_errmsg_timezone = ''
                Orgmodel_errmsg_duplicate = ''
                Orgmodel_error_flag = ''
                del_ind_field = column[3]


                # If the Input file Deletion indicator is "0" (Insert\Update record) and Address\Client key  does not exist in the OrgModeltable

                if (del_ind_field == '0') and (not (OrgModel.objects.filter ( object_id=column[0],client=client)).exists()):
                    # get Addresss data from attached file and store it to MMD_ORG_MODEL db table
                    _, created= OrgModel.objects.get_or_create (
                        object_id=column[0],
                        node_guid=guid_generator(),
                        name=column[1],
                        parent_node_guid='NULL',
                        node_type=column[2],
                        del_ind=column[3],
                        client=OrgClients.objects.get ( client=client )
                    )

                    Orgmodel_inserted_cnt = Orgmodel_inserted_cnt + 1
                    Data_saved = 'Y'

                # If the Input file Deletion indicator is "0" (Insert\Update record) and Address\Client key  exist in the OrgModeltable

                elif (del_ind_field == '0') and (OrgModel.objects.filter ( object_id=column[0], client=client ).exists ()):
                    queryset_test_upd = OrgModel.objects.filter ( object_id=column[0], client=client )
                    for test in queryset_test_upd:

                        if (test.name != column[1] or test.node_type != column[2]
                                or test.del_ind != column[3]):

                            OrgModel.objects.filter ( object_id=column[0],client=client).update(
                                                        name=column[1],
                                                        node_type=column[2],
                                                        del_ind=column[3])
                            Orgmodel_updated_cnt = Orgmodel_updated_cnt + 1
                            Data_saved = 'Y'

                        else :

                            Orgmodel_duplicate_cnt = Orgmodel_duplicate_cnt +1
                            error_msg = get_message_desc(MSG094)[1]
                            # msgid = 'MSG094'
                            # error_msg = get_msg_desc(msgid)
                            # msg = error_msg['message_desc'][0]
                            # error_msg = msg
                            Orgmodel_errmsg_duplicate = error_msg
                            Orgmodel_error_flag = 'Y'

                # If the Input file Deletion indicator is "1" (Delete record) and Address\Client key  exist in the OrgModeltable

                if (del_ind_field == '1') and (OrgModel.objects.filter ( object_id=column[0], client=client ).exists ()):
                    queryset_del = OrgModel.objects.filter ( object_id=column[0], client=client )
                    for test in queryset_del:
                        if test.del_ind == False:
                            OrgModel.objects.filter ( object_id=column[0], client=client ).update ( del_ind=1 )
                            Orgmodel_deleted_cnt = Orgmodel_deleted_cnt + 1
                            Data_saved = 'Y'

                # If the Input file Deletion indicator is "1" (Delete record) and Address\Client key  does not exist in the OrgModeltable.
                # Raise delete error

                elif (del_ind_field == '1') and (not (OrgModel.objects.filter ( object_id=column[0], client=client ).exists ())):
                    Orgmodel_delete_error = 'Y'
                    Orgmodel_delete_Err_Count = Orgmodel_delete_Err_Count + 1


            # Messages Summarising of processing of input file.

            messages.info ( req, 'Database Upload Results  :')
            messages.info ( req, '-------------------------------' )

            Orgmodel_DB_count = OrgModel.objects.filter ( del_ind=0 ).count ()
            messages.success ( req, ' Number of Records in Database    : ' + str ( Orgmodel_DB_count ) )
            messages.success ( req, ' Records Inserted      : ' + str ( Orgmodel_inserted_cnt ) )
            messages.success ( req, ' Records Updated       : ' + str ( Orgmodel_updated_cnt ) )
            messages.success ( req, ' Records Deleted       : ' + str ( Orgmodel_deleted_cnt ) )
            messages.success ( req, ' No change Records       : ' + str ( Orgmodel_duplicate_cnt ) )

            if Orgmodel_line_no == 0:
                messages.error ( req, ' Empty File : Please correct and try again ' )
                Data_saved = ''
            if Orgmodel_delete_error != '' :
                messages.error ( req,
                                 ' Input Delete records that dont exist in DB : ' + str ( Orgmodel_delete_Err_Count ) )




        if Data_saved != 'Y':
            error_msg = get_message_desc(MSG043)[1]
            # msgid = 'MSG043'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            messages.error(req, error_msg)
            # messages.error ( req, MSG043 )
        else:
            error_msg = get_message_desc(MSG037)[1]
            # msgid = 'MSG037'
            # error_msg = get_msg_desc(msgid)
            messages.success(req, error_msg)
            # messages.success ( req, MSG037 )


    except Exception as e:
        print ( e )
        messages.error ( req, 'Error : ' + str ( e ) )


