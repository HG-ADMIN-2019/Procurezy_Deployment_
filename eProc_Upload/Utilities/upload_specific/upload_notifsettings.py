import csv
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.models import *
from eProc_Configuration.models import OrgClients, NotifSettings
from django.contrib import messages
from eProc_Basic.Utilities.messages.messages import *


# # upload Notification csv data file into timezones db table - Shankar - SP10-19
def upload_notifsettings(req, timezone, Test_mode):
    #     """
    #     on uploading of timezones  csv file
    #     1. GET Notification csv file and store its respective field values into MSS_NOTIF_SETTING db table
    #     :param req: UI request
    #     :param timezone: attached csv file data
    #     :param Test_mode : Diagnostics
    #     :return: return true on success, return false on failure
    #     """
    #

    try:

        client = getClients(req)

        # If the Test Mode check box is checked then run diagnostics.

        if Test_mode == 'on':

            Test_DB_count_notifset = 0
            Test_Insert_Count_notifset = 0
            Test_Update_Count_notifset = 0
            Test_Delete_Count_notifset = 0
            Test_File_Count_notifset = 0
            Test_Delete_Err_Count_notifset = 0
            Test_notifset_delete_error = ''
            Test_Duplicate_Count_notifset = 0
            Test_DB_Duplicate_Count_notifset = 0
            Test_notifset_number_list = []

            Data_saved = ''

            Test_DB_count_notifset = NotifSettings.objects.filter(del_ind=False).count()

            # Read thru the file record by record , Assign column based on comma delimter

            for column in csv.reader(timezone, delimiter=',', quotechar='"'):

                Test_File_Count_notifset = Test_File_Count_notifset + 1

                del_ind_field = column[6]

                # If the Input file Deletion indicator is "0" (Insert\Update record) and timezone  exist in the timezone table

                if (del_ind_field == '0') and (
                NotifSettings.objects.filter(variant_name=column[1], client=client).exists()):
                    queryset_test_upd = NotifSettings.objects.filter(variant_name=column[1], client=client)
                    for test in queryset_test_upd:
                        if (test.notif_subject != column[2] or test.notif_header != column[3] or
                                test.notif_body != column[4] or test.notif_footer != column[5]):
                            Test_Update_Count_notifset = Test_Update_Count_notifset + 1
                        else:
                            Test_Duplicate_Count_notifset = Test_Duplicate_Count_notifset + 1

                # If the Input file Deletion indicator is "0" (Insert\Update record) and timezone key  does not exist in the timezone table

                elif (del_ind_field == '0') and (
                not (NotifSettings.objects.filter(variant_name=column[1], client=client).exists())):
                    if column[0] in Test_notifset_number_list:
                        Test_Duplicate_Count_notifset = Test_Duplicate_Count_notifset + 1
                        error_msg = get_message_desc(MSG094)[1]
                        # msgid = 'MSG094'
                        # error_msg = get_msg_desc(msgid)
                        # msg = error_msg['message_desc'][0]
                        # error_msg = msg
                        Test_notifset_errmsg_duplicate = error_msg
                    else:
                        Test_Insert_Count_notifset = Test_Insert_Count_notifset + 1

                # Check  If the Input file Deletion indicator is "1" (Delete record) and if record  exists
                # Check if the record is active on DB.

                if (del_ind_field == '1') and (
                NotifSettings.objects.filter(variant_name=column[1], client=client).exists()):
                    queryset_test_del = NotifSettings.objects.filter(variant_name=column[1], client=client)
                    for test in queryset_test_del:
                        if test.del_ind == False:
                            Test_Delete_Count_notifset = Test_Delete_Count_notifset + 1

                # Check  If the Input file Deletion indicator is "1" (Delete record) and if record does not exists
                # report as invalid record.

                elif (del_ind_field == '1') and (
                        not (NotifSettings.objects.filter(variant_name=column[1], client=client).exists())):
                    Test_notifset_delete_error = 'Y'
                    Test_Delete_Err_Count_notifset = Test_Delete_Err_Count_notifset + 1

                # Append the input key to the Array list for checking the next reocrds for dups.

                Test_notifset_number_list.append(column[0])

            messages.info(req, 'Test Mode Diagnostics:')
            messages.info(req, '-----------------------------')

            # Display insert /updated count in the display
            # Number of active records on the Database.
            messages.success(req, ' Number of Records in Database    : ' + str(Test_DB_count_notifset))
            # Number of records in the Input file.
            messages.success(req, ' Number of Records in Input file  : ' + str(Test_File_Count_notifset))
            # Total records that need to be inserted.
            messages.success(req, ' Records to be Inserted           : ' + str(Test_Insert_Count_notifset))
            # Total records that need to be Updated.
            messages.success(req, ' Records to be Updated            : ' + str(Test_Update_Count_notifset))
            # Total records that need to be Deleted.
            messages.success(req, ' Records to be Deleted            : ' + str(Test_Delete_Count_notifset))
            # Total records that are duplicate in the input file
            messages.error(req, ' Duplicate Records                : ' + str(Test_Duplicate_Count_notifset))

            # Display the number of delete records that dont exist on DB

            if Test_notifset_delete_error != '':
                messages.error(req, ' Input Delete records that dont exist in DB : ' + str(
                    Test_Delete_Err_Count_notifset))

            # Display error message for empty file

            if Test_File_Count_notifset == 0:
                messages.error(req, ' Empty File : Please correct and try again ')


        elif Test_mode != 'on':

            notifset_line_no = 0
            notifset_inserted_cnt = 0
            notifset_updated_cnt = 0
            notifset_deleted_cnt = 0
            notifset_DB_count = 0
            notifset_delete_Err_Count = 0
            notifset_delete_error = ''
            Data_saved = ''

            for column in csv.reader(timezone, delimiter=',', quotechar='"'):
                notifset_line_no = notifset_line_no + 1
                print("Notif Settings Extract Line Number:" + str(notifset_line_no))

                del_ind_field = column[6]

                # If the Deletion indicator in the file = "0" and record does not exist on the DB : INSERT DB

                if (del_ind_field == '0') and (
                not (NotifSettings.objects.filter(variant_name=column[1], client=client).exists())):
                    _, created = NotifSettings.objects.get_or_create(
                        notif_guid=guid_generator(),
                        variant_name=column[1],
                        notif_subject=column[2],
                        notif_header=column[3],
                        notif_body=column[4],
                        notif_footer=column[5],
                        del_ind=column[6],
                        client=OrgClients.objects.get(client=client)
                    )
                    notifset_inserted_cnt = notifset_inserted_cnt + 1
                    Data_saved = 'Y'

                # If the Deletion indicator in the file = "0" and record  exist on the DB : Update DB

                elif (del_ind_field == '0') and (
                NotifSettings.objects.filter(variant_name=column[1], client=client).exists()):
                    queryset_upd = NotifSettings.objects.filter(variant_name=column[1], client=client)
                    for test in queryset_upd:
                        if (test.notif_subject != column[2] or test.notif_header != column[3] or
                                test.notif_body != column[4] or test.notif_footer != column[5]):
                            NotifSettings.objects.filter(variant_name=column[1], client=client).update(
                                notif_subject=column[2],
                                notif_header=column[3],
                                notif_body=column[4],
                                notif_footer=column[5],
                                del_ind=column[6], )
                            notifset_updated_cnt = notifset_updated_cnt + 1
                            Data_saved = 'Y'

                # If the Deletion indicator in the file = "1" and record  exist on the DB : Soft Delete(del_ind =0) DB

                if (del_ind_field == '1') and (
                NotifSettings.objects.filter(variant_name=column[1], client=client).exists()):
                    queryset_del = NotifSettings.objects.filter(variant_name=column[1], client=client)
                    for test in queryset_del:
                        if test.del_ind == False:
                            NotifSettings.objects.filter(variant_name=column[1], client=client).update(del_ind=1)
                            notifset_deleted_cnt = notifset_deleted_cnt + 1
                            Data_saved = 'Y'

                elif (del_ind_field == '1') and (
                not (NotifSettings.objects.filter(variant_name=column[1], client=client).exists())):
                    notifset_delete_error = 'y'
                    notifset_delete_Err_Count = notifset_delete_Err_Count + 1

            # Display insert /updated count in the display
            notifset_DB_count = NotifSettings.objects.filter(del_ind=False).count()

            messages.info(req, 'Database Upload Results  :')
            messages.info(req, '-------------------------------')

            # Display the number of Active records in DB
            messages.success(req, ' Number of Records in Database    : ' + str(notifset_DB_count))
            # Number of records in the Input file.
            messages.success(req, ' Number of Records in Input file  : ' + str(notifset_line_no))
            # Display the number of records Inserted
            messages.success(req, ' Records Inserted      : ' + str(notifset_inserted_cnt))
            # Display the number of records Updated
            messages.success(req, ' Records Updated       : ' + str(notifset_updated_cnt))
            # Display the number of records Deleted
            messages.success(req, ' Records Deleted       : ' + str(notifset_deleted_cnt))

            # Display message for empty file
            if notifset_line_no == 0:
                messages.error(req, ' Empty File : Please correct and try again ')

            # Display error message if delete record doesnt exist on DB
            if notifset_delete_error != '':
                messages.error(req,
                               ' Input Delete records that dont exist in DB : ' + str(notifset_delete_Err_Count))

        if Data_saved == 'Y':
            error_msg = get_message_desc(MSG037)[1]
            # msgid = 'MSG037'
            # error_msg = get_msg_desc(msgid)
            messages.success(req, error_msg)
            # # messages.success ( req, MSG037 )
        else:
            error_msg = get_message_desc(MSG043)[1]
            # msgid = 'MSG043'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            messages.error(req, error_msg)
            # messages.error ( req, MSG043 )

    except Exception as e:
        print(e)
        messages.error(req, 'Error : ' + str(e))
