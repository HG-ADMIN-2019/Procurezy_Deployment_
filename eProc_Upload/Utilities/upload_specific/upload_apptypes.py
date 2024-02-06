import csv
from django.contrib import messages

from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.models import *
from eProc_Basic.Utilities.messages.messages import *


# # upload Apptypes csv data file into Languages db table - Shankar - SP10-19
from eProc_Configuration.models.development_data import *


def upload_apptypes(req, apptypes, Test_mode):
#     """
#     on uploading of Approver Types  csv file
#     1. GET Apptypes csv file and store its respective field values into MMD_APP_TYPES db table
#     :param req: UI request
#     :param Language: attached csv file data
#     :param Test_mode : Diagnostics
#     :return: return true on success, return false on failure
#     """
#

    try:

        # If the Test Mode check box is checked then run diagnostics.

        if Test_mode == 'on'  :

            Test_apptypes_DB_count              = 0
            Test_Insert_Count_apptypes          = 0
            Test_Update_Count_apptypes          = 0
            Test_Duplicate_Count_apptypes       = 0
            Test_Delete_Count_apptypes          = 0
            Test_File_Count_apptypes            = 0
            Test_Delete_Err_Count_apptypes      = 0
            Test_apptypes_delete_error          = ''
            Test_apptypes_number_list           = []

            Data_saved = ''

            Test_apptypes_DB_count = ApproverType.objects.filter(del_ind=False).count ()

            # Read thru the file record by record , Assign column based on comma delimter

            for column in csv.reader ( apptypes, delimiter=',', quotechar='"' ):
                Test_File_Count_apptypes = Test_File_Count_apptypes + 1
                print ( "Approval Types Extract Line Number:" + str ( Test_File_Count_apptypes ) )

                del_ind_field = column[2]

                # If the Input file Deletion indicator is "0" (Insert\Update record)

                if (del_ind_field == '0') and (ApproverType.objects.filter(app_types=column[0]).exists()):
                    queryset_test_upd = ApproverType.objects.filter ( app_types=column[0])
                    for test in queryset_test_upd:
                        if test.app_types != column[1]  :
                            Test_Update_Count_apptypes = Test_Update_Count_apptypes + 1
                        else  :
                            Test_Duplicate_Count_apptypes = Test_Duplicate_Count_apptypes + 1

                # If the Input file Deletion indicator is "0" (Insert\Update record)

                elif (del_ind_field == '0') and (not (ApproverType.objects.filter(app_types=column[0]).exists ())):
                    if column[0] in Test_apptypes_number_list:
                        Test_Duplicate_Count_apptypes = Test_Duplicate_Count_apptypes + 1
                        error_msg = get_message_desc(MSG094)[1]
                        # msgid = 'MSG094'
                        # error_msg = get_msg_desc(msgid)
                        # msg = error_msg['message_desc'][0]
                        # error_msg = msg
                        Test_apptypes_errmsg_duplicate = error_msg
                    else:
                        Test_Insert_Count_apptypes = Test_Insert_Count_apptypes + 1

                # Check  If the Input file Deletion indicator is "1" (Delete record) and if record  exists
                # Check if the record is active on DB.

                if (del_ind_field == '1') and (ApproverType.objects.filter(app_types=column[0]).exists ()):
                    queryset_test_del = ApproverType.objects.filter ( app_types=column[0] )
                    for test in queryset_test_del:
                        if test.del_ind == False    :
                            Test_Delete_Count_apptypes = Test_Delete_Count_apptypes +1

                # Check  If the Input file Deletion indicator is "1" (Delete record) and if record does not exists
                # report as invalid record.


                elif (del_ind_field == '1') and (not(ApproverType.objects.filter(app_types=column[0]).exists ())):
                       Test_apptypes_delete_error = 'Y'
                       Test_Delete_Err_Count_apptypes = Test_Delete_Err_Count_apptypes + 1


                # Append the input key to the Array list for checking the next reocrds for dups.

                Test_apptypes_number_list.append(column[0])

            # Number of active records on the Database.
            messages.info ( req, 'Test Mode Diagnostics:' )
            messages.info ( req, '-----------------------------' )


            #Display insert /updated count in the display
            messages.success ( req, ' Number of Records in Database    : ' + str ( Test_apptypes_DB_count ))
            # Number of records in the Input file.
            messages.success ( req, ' Number of Records in Input file  : ' + str ( Test_File_Count_apptypes ))
            # Total records that need to be inserted.
            messages.success ( req, ' Records to be Inserted           : ' + str ( Test_Insert_Count_apptypes ))
            # Total records that need to be Updated.
            messages.success ( req, ' Records to be Updated            : ' + str ( Test_Update_Count_apptypes ))
            # Total records that need to be Deleted.
            messages.success ( req, ' Records to be Deleted            : ' + str ( Test_Delete_Count_apptypes ))
            # Total records that are duplicate in the input file
            messages.error   ( req, ' Duplicate records                : ' + str ( Test_Duplicate_Count_apptypes ) )

            # Display the number of delete records that dont exist on DB
            if Test_apptypes_delete_error != '':
                messages.error ( req, ' Input Delete records that dont exist in DB : ' + str ( Test_Delete_Err_Count_apptypes ))

            # Display error message for empty file
            if Test_File_Count_apptypes == 0:
                messages.error ( req, ' Empty File : Please correct and try again ' )


        elif Test_mode != 'on' :

            apptypes_line_no = 0
            apptypes_inserted_cnt = 0
            apptypes_updated_cnt = 0
            apptypes_deleted_cnt = 0
            apptypes_duplicate_cnt = 0
            apptypes_DB_count = 0
            apptypes_delete_Err_Count    = 0
            apptypes_delete_error        = ''
            Data_saved          = ''

            for column in csv.reader ( apptypes, delimiter=',', quotechar='"' ):
                apptypes_line_no = apptypes_line_no + 1
                print ( "Approval Types Extract Line Number:" + str ( apptypes_line_no ) )

                del_ind_field = column[2]

                # If the Deletion indicator in the file = "0" and record does not exist on the DB : INSERT DB

                if (del_ind_field == '0') and (not (ApproverType.objects.filter(app_types=column[0]).exists ())):
                    _, created = ApproverType.objects.get_or_create( app_types=column[0], appr_type_desc=column[1],
                                                                      del_ind=column[2] )
                    apptypes_inserted_cnt = apptypes_inserted_cnt +1
                    Data_saved            = 'Y'

                # If the Deletion indicator in the file = "0" and record  exist on the DB : Update DB

                elif (del_ind_field == '0') and (ApproverType.objects.filter(app_types=column[0]).exists()):
                    queryset_upd = ApproverType.objects.filter ( app_types=column[0])
                    for test in queryset_upd:
                            if test.app_types != column[1] :
                                ApproverType.objects.filter ( app_types=column[0] ).update ( appr_type_desc=column[1],
                                                                                        del_ind=column[2] )
                                apptypes_updated_cnt = apptypes_updated_cnt + 1
                                Data_saved            = 'Y'

                # If the Deletion indicator in the file = "1" and record  exist on the DB : Soft Delete(del_ind =0) DB

                if (del_ind_field == '1') and (ApproverType.objects.filter(app_types=column[0]).exists ()):
                    queryset_del = ApproverType.objects.filter ( app_types=column[0] )
                    for test in queryset_del:
                        if test.del_ind == False    :
                            ApproverType.objects.filter( app_types=column[0]).update( del_ind=1)
                            apptypes_deleted_cnt  = apptypes_deleted_cnt +1
                            Data_saved            = 'Y'

                # If the Deletion indicator in the file = "1" and record  does not exist on the DB : Error message

                elif (del_ind_field == '1') and (not (ApproverType.objects.filter (app_types=column[0]).exists ())):
                    apptypes_delete_error = 'Y'
                    apptypes_delete_Err_Count = apptypes_delete_Err_Count + 1



            #Display insert /updated count in the display
            apptypes_DB_count = ApproverType.objects.filter(del_ind=0).count ()


            messages.info ( req, 'Database Upload Results  :')
            messages.info ( req, '-------------------------------' )


            # Display the number of Active records in DB
            messages.success ( req, ' Number of Records in Database    : ' + str ( apptypes_DB_count ))
            # Display the number of  records in file
            messages.success ( req, ' Number of Records in Input file  : ' + str ( apptypes_line_no ))
            # Display the number of records Inserted
            messages.success ( req, ' Records Inserted      : ' + str( apptypes_inserted_cnt ))
            # Display the number of records Updated
            messages.success ( req, ' Records Updated       : ' + str( apptypes_updated_cnt ))
            # Display the number of records Deleted
            messages.success ( req, ' Records Deleted       : ' + str( apptypes_deleted_cnt ))

            if apptypes_line_no == 0:
                messages.error ( req, ' Empty File : Please correct and try again ' )

            # Display error message if delete record doesnt exist on DB
            if apptypes_delete_error != '':
                messages.error ( req,' Input Delete records that dont exist in DB : ' + str ( apptypes_delete_Err_Count ) )


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


