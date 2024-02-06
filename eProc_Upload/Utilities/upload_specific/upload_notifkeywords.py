import csv
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from django.contrib import messages

from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.models import *
from eProc_Configuration.models import OrgClients, NotifKeywords
from eProc_Basic.Utilities.messages.messages import *


# # upload NotifKeywords csv data file into MSS_NOTIF_KEYWORD db table - Shankar - SP10-19
def upload_notifkeywords(req, notifkeywords, Test_mode):
    #     """
    #     on uploading of timezones  csv file
    #     1. GET NotifKeywords csv file and store its respective field values into MSS_NOTIF_KEYWORD db table
    #     :param req: UI request
    #     :param NotifKeywords: attached csv file data
    #     :param Test_mode : Diagnostics
    #     :return: return true on success, return false on failure
    #     """
    #

    try:

        client=getClients(req)

        # If the Test Mode check box is checked then run diagnostics.


        if Test_mode == 'on':

            Test_DB_count_notifkeywords = 0
            Test_Insert_Count_notifkeywords = 0
            Test_Update_Count_notifkeywords = 0
            Test_Delete_Count_notifkeywords = 0
            Test_File_Count_notifkeywords = 0
            Test_Delete_Err_Count_notifkeywords = 0
            Test_notifkeywords_delete_error = ''
            Test_Duplicate_Count_notifkeywords = 0
            Test_DB_Duplicate_Count_notifkeywords = 0
            Test_notifkeywords_number_list = []

            Data_saved = ''

            Test_DB_count_notifkeywords = NotifKeywords.objects.filter ( del_ind=False ).count ()

            # Read thru the file record by record , Assign column based on comma delimter

            for column in csv.reader ( notifkeywords, delimiter=',', quotechar='"' ):

                Test_File_Count_notifkeywords = Test_File_Count_notifkeywords + 1

                del_ind_field = column[2]

                # If the Input file Deletion indicator is "0" (Insert\Update record) and timezone key  does not exist in the timezone table

                if (del_ind_field == '0') and (not (NotifKeywords.objects.filter ( variant_name= column[0], client=client ).exists ())):
                        Test_Insert_Count_notifkeywords = Test_Insert_Count_notifkeywords + 1

                # Check  If the Input file Deletion indicator is "1" (Delete record) and if record  exists
                # Check if the record is active on DB.

                if (del_ind_field == '1') and (NotifKeywords.objects.filter ( variant_name= column[0], client=client ).exists ()):
                    queryset_test_del = NotifKeywords.objects.filter ( variant_name= column[0], client=client )
                    for test in queryset_test_del:
                        if test.del_ind == False:
                            Test_Delete_Count_notifkeywords = Test_Delete_Count_notifkeywords + 1

                # Check  If the Input file Deletion indicator is "1" (Delete record) and if record does not exists
                # report as invalid record.

                elif (del_ind_field == '1') and (
                        not (NotifKeywords.objects.filter ( variant_name= column[0], client=client ).exists ())):
                    Test_notifkeywords_delete_error = 'Y'
                    Test_Delete_Err_Count_notifkeywords = Test_Delete_Err_Count_notifkeywords + 1

                # Append the input key to the Array list for checking the next reocrds for dups.

                Test_notifkeywords_number_list.append ( column[0] )



            messages.info ( req, 'Test Mode Diagnostics:' )
            messages.info ( req, '-----------------------------' )

            # Display insert /updated count in the display
            # Number of active records on the Database.
            messages.success ( req, ' Number of Records in Database    : ' + str ( Test_DB_count_notifkeywords ) )
            # Number of records in the Input file.
            messages.success ( req, ' Number of Records in Input file  : ' + str ( Test_File_Count_notifkeywords ) )
            # Total records that need to be inserted.
            messages.success ( req, ' Records to be Inserted           : ' + str ( Test_Insert_Count_notifkeywords ) )
            # Total records that need to be Deleted.
            messages.success ( req, ' Records to be Deleted            : ' + str ( Test_Delete_Count_notifkeywords ) )

            # Display the number of delete records that dont exist on DB

            if Test_notifkeywords_delete_error != '':
                messages.error ( req, ' Input Delete records that dont exist in DB : ' + str (
                    Test_Delete_Err_Count_notifkeywords ) )

            # Display error message for empty file

            if Test_File_Count_notifkeywords == 0:
                messages.error ( req, ' Empty File : Please correct and try again ' )


        elif Test_mode != 'on':

            notifkeywords_line_no = 0
            notifkeywords_inserted_cnt = 0
            notifkeywords_updated_cnt = 0
            notifkeywords_deleted_cnt = 0
            notifkeywords_DB_count = 0
            notifkeywords_delete_Err_Count = 0
            notifkeywords_delete_error = ''
            Data_saved = ''

            for column in csv.reader ( notifkeywords, delimiter=',', quotechar='"' ):
                notifkeywords_line_no = notifkeywords_line_no + 1
                print ( "Notif Keywords Extract Line Number:" + str ( notifkeywords_line_no ) )

                del_ind_field = column[2]

                # If the Deletion indicator in the file = "0" and record does not exist on the DB : INSERT DB

                if (del_ind_field == '0') :
                    _, created = NotifKeywords.objects.get_or_create (
                        notif_keyword_guid=guid_generator (),
                        variant_name=column[0],
                        keyword=column[1],
                        del_ind=column[2],
                        client=OrgClients.objects.get ( client=client )  )
                    notifkeywords_inserted_cnt = notifkeywords_inserted_cnt + 1
                    Data_saved = 'Y'

                # If the Deletion indicator in the file = "1" and record  exist on the DB : Soft Delete(del_ind =0) DB

                if (del_ind_field == '1') and (NotifKeywords.objects.filter ( variant_name= column[0], client=client ).exists ()):
                    queryset_del = NotifKeywords.objects.filter ( variant_name= column[0], client=client )
                    for test in queryset_del:
                        if test.del_ind == False:
                            NotifKeywords.objects.filter ( variant_name= column[0], client=client ).update ( del_ind=1 )
                            notifkeywords_deleted_cnt = notifkeywords_deleted_cnt + 1
                            Data_saved = 'Y'

                elif (del_ind_field == '1') and (not (NotifKeywords.objects.filter ( variant_name= column[0], client=client ).exists ())):
                    notifkeywords_delete_error = 'y'
                    notifkeywords_delete_Err_Count = notifkeywords_delete_Err_Count + 1

            # Display insert /updated count in the display
            notifkeywords_DB_count = NotifKeywords.objects.filter ( del_ind=False ).count ()


            messages.info ( req, 'Database Upload Results  :')
            messages.info ( req, '-------------------------------' )

            # Display the number of Active records in DB
            messages.success ( req, ' Number of Records in Database    : ' + str ( notifkeywords_DB_count ) )
            # Number of records in the Input file.
            messages.success ( req, ' Number of Records in Input file  : ' + str ( notifkeywords_line_no ) )
            # Display the number of records Inserted
            messages.success ( req, ' Records Inserted      : ' + str ( notifkeywords_inserted_cnt ) )
            # Display the number of records Deleted
            messages.success ( req, ' Records Deleted       : ' + str ( notifkeywords_deleted_cnt ) )

            # Display message for empty file
            if notifkeywords_line_no == 0:
                messages.error ( req, ' Empty File : Please correct and try again ' )

            # Display error message if delete record doesnt exist on DB
            if notifkeywords_delete_error != '':
                messages.error ( req,
                                 ' Input Delete records that dont exist in DB : ' + str ( notifkeywords_delete_Err_Count ) )

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
        messages.error ( req, 'Error : ' + str ( e ) )

