import csv
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.models import *
from eProc_Configuration.models import OrgClients, SystemSettings
from django.contrib import messages
from eProc_Basic.Utilities.messages.messages import *




# upload System Settings csv data file into MSS_SYSTEM_SETTINGS db table - Shankar - SP12-06



# def upload_systemsettings(req, systemsettings ,Test_mode):
#     """
#     on uploading of MSS_SYSTEM_SETTINGS  csv file
#     1. GET System Settings  csv file and store its respective field values into MSS_SYSTEM_SETTINGS db table
#     :param req: UI request
#     :param systemsettings: attached csv file data
#     :param Test_mode : Diagnostics
#     :return: return true on success, return false on failure
#     """
#
#     try:
#
#         client = getClients(req)
#         # If the Test Mode check box is checked then run diagnostics.
#
#         if Test_mode == 'on':
#
#             # Diagnostics mode variables
#             Test_DB_count_systemsettings           = 0
#             Test_Insert_Count_systemsettings       = 0
#             Test_Update_Count_systemsettings       = 0
#             Test_Delete_Count_systemsettings       = 0
#             Test_File_Count_systemsettings         = 0
#             Test_Delete_Err_Count_systemsettings   = 0
#             Test_Duplicate_Count_systemsettings    = 0
#             Test_systemsettings_delete_error       = ''
#             Test_systemsettings_number_list        = []
#
#             Data_saved = ''
#
#             Test_DB_count_systemsettings = SystemSettings.objects.filter().count ()
#
#             # Read thru the file record by record , Assign column based on comma delimter
#
#             for column in csv.reader ( systemsettings, delimiter=',', quotechar='"' ):
#
#                 Test_File_Count_systemsettings = Test_File_Count_systemsettings + 1
#                 del_ind_field = column[14]
#
#                 print ( "System Settings  Extract Line Number:" + str ( Test_File_Count_systemsettings ) )
#
#                 # If the Input file Deletion indicator is "0" (Insert\Update record) and Country  exist in the Country table
#
#                 if (del_ind_field == '0') and (SystemSettings.objects.filter (
#                         pwd_policy 	        =column[11]
#                         ,login_attempts 	=column[8]
#                         ,session_timeout 	=column[12]
#                         ,msg_display 		=column[9]
#                         ,theme_color 		=column[13]
#                         ,pagination_count	=column[10]
#                         ,attachment_size 	=column[7]
#                         ,attachment_extension =column[6]
#                         ,attribute_09 		=column[0]
#                         ,attribute_10 		=column[1]
#                         ,attribute_11 		=column[2]
#                         ,attribute_12 		=column[3]
#                         ,attribute_13 		=column[4]
#                         ,attribute_14 		=column[5]
#                         , client=client       ).exists()):
#                     queryset_test_upd = SystemSettings.objects.filter (
#                         pwd_policy 	=column[11]
#                         ,login_attempts 	=column[8]
#                         ,session_timeout 	=column[12]
#                         ,msg_display 		=column[9]
#                         ,theme_color 		=column[13]
#                         ,pagination_count	=column[10]
#                         ,attachment_size 	=column[7]
#                         ,attachment_extension =column[6]
#                         ,attribute_09 		=column[0]
#                         ,attribute_10 		=column[1]
#                         ,attribute_11 		=column[2]
#                         ,attribute_12 		=column[3]
#                         ,attribute_13 		=column[4]
#                         ,attribute_14 		=column[5]
#                         , client=client                )
#                     for test in queryset_test_upd:
#                         if (test.pwd_policy 		!=column[11]
#                             or test.login_attempts 	!=column[8]
#                             or test.session_timeout !=column[12]
#                             or test.msg_display 	!=column[9]
#                             or test.theme_color 	!=column[13]
#                             or test.pagination_count !=column[10]
#                             or test.attachment_size !=column[7]
#                             or test.attachment_extension !=column[6]
#                             or test.attribute_09 		!=column[0]
#                             or test.attribute_10 		!=column[1]
#                             or test.attribute_11 		!=column[2]
#                             or test.attribute_12 		!=column[3]
#                             or test.attribute_13 		!=column[4]
#                             or test.attribute_14 	!=column[5]):
#
#                             Test_Update_Count_systemsettings = Test_Update_Count_systemsettings + 1
#                         else :
#                             Test_Duplicate_Count_systemsettings = Test_Duplicate_Count_systemsettings + 1
#
#                 # If the Input file Deletion indicator is "0" (Insert\Update record) and country key  does not exist in the country table
#                 elif (del_ind_field == '0') and (not (SystemSettings.objects.filter (
#                          pwd_policy 	   =column[11]
#                         ,login_attempts 	=column[8]
#                         ,session_timeout 	=column[12]
#                         ,msg_display 		=column[9]
#                         ,theme_color 		=column[13]
#                         ,pagination_count	=column[10]
#                         ,attachment_size 	=column[7]
#                         ,attachment_extension =column[6]
#                         ,attribute_09 		=column[0]
#                         ,attribute_10 		=column[1]
#                         ,attribute_11 		=column[2]
#                         ,attribute_12 		=column[3]
#                         ,attribute_13 		=column[4]
#                         ,attribute_14 		=column[5]
#                         , client=client )).exists()):
#
#                         Test_Insert_Count_systemsettings = Test_Insert_Count_systemsettings + 1
#
#                 else:
#                         Test_Duplicate_Count_systemsettings = Test_Duplicate_Count_systemsettings + 1
#                         Test_systemsettings_errmsg_duplicate = MSG094
#
#     # Check  If the Input file Deletion indicator is "1" (Delete record) and if record  exists
#                 # Check if the record is active on DB.
#
#                 if (del_ind_field == '1') and (SystemSettings.objects.filter (
#                          pwd_policy 	    =column[11]
#                         ,login_attempts 	=column[8]
#                         ,session_timeout 	=column[12]
#                         ,msg_display 		=column[9]
#                         ,theme_color 		=column[13]
#                         ,pagination_count	=column[10]
#                         ,attachment_size 	=column[7]
#                         ,attachment_extension =column[6]
#                         ,attribute_09 		=column[0]
#                         ,attribute_10 		=column[1]
#                         ,attribute_11 		=column[2]
#                         ,attribute_12 		=column[3]
#                         ,attribute_13 		=column[4]
#                         ,attribute_14 		=column[5]
#                         , client=client )).exists():
#                             Test_Delete_Count_systemsettings = Test_Delete_Count_systemsettings + 1
#
#                 # Check  If the Input file Deletion indicator is "1" (Delete record) and if record does not exists
#                 # report as invalid record.
#
#
#                 elif (del_ind_field == '1') and (
#                         not (SystemSettings.objects.filter (
#                             pwd_policy 	        =column[11]
#                             ,login_attempts 	=column[8]
#                             ,session_timeout 	=column[12]
#                             ,msg_display 		=column[9]
#                             ,theme_color 		=column[13]
#                             ,pagination_count	=column[10]
#                             ,attachment_size 	=column[7]
#                             ,attachment_extension =column[6]
#                             ,attribute_09 		=column[0]
#                             ,attribute_10 		=column[1]
#                             ,attribute_11 		=column[2]
#                             ,attribute_12 		=column[3]
#                             ,attribute_13 		=column[4]
#                             ,attribute_14 		=column[5] )).exists ()):
#                     Test_systemsettings_delete_error = 'Y'
#                     Test_Delete_Err_Count_systemsettings = Test_Delete_Err_Count_systemsettings + 1
#
#                 # Append the input key to the Array list for checking the next reocrds for dups.
#
#
#             # Display insert /updated count in the display
#
#             # Number of active records on the Database.
#             messages.success ( req, ' Number of Records in Database    : ' + str ( Test_DB_count_systemsettings ) )
#             # Number of records in the Input file.
#             messages.success ( req, ' Number of Records in Input file  : ' + str ( Test_File_Count_systemsettings ) )
#             # Total records that need to be inserted.
#             messages.success ( req, ' Records to be Inserted           : ' + str ( Test_Insert_Count_systemsettings ) )
#             # Total records that need to be Updated.
#             messages.success ( req, ' Records to be Updated            : ' + str ( Test_Update_Count_systemsettings ) )
#             # Total records that need to be Deleted.
#             messages.success ( req, ' Records to be Deleted            : ' + str ( Test_Delete_Count_systemsettings ) )
#             # Total records that are duplicate in the input file
#             messages.error ( req, ' Duplicate Records                : ' + str ( Test_Duplicate_Count_systemsettings ) )
#
#             # Display the number of delete records that dont exist on DB
#             if Test_systemsettings_delete_error == 'Y':
#                 messages.error ( req, ' Input Delete records that dont exist in DB : ' + str (
#                     Test_Delete_Err_Count_systemsettings ) )
#
#             # Display error message for empty file
#             if Test_File_Count_systemsettings == 0:
#                 messages.error ( req, ' Empty File : Please correct and try again ' )
#
#
#         elif Test_mode != 'on':
#
#             systemsettings_line_no             = 0
#             systemsettings_inserted_cnt        = 0
#             systemsettings_updated_cnt         = 0
#             systemsettings_deleted_cnt         = 0
#             systemsettings_DB_count            = 0
#             systemsettings_delete_Err_Count    = 0
#             systemsettings_delete_error        = ''
#             Data_saved                          =''
#
#             for column in csv.reader ( systemsettings, delimiter=',', quotechar='"' ):
#                 systemsettings_line_no = systemsettings_line_no + 1
#                 print ( "System Settings  Extract Line Number:" + str ( systemsettings_line_no ) )
#
#                 del_ind_field = column[14]
#
#
#
#                 # If the Deletion indicator in the file = "0" and record does not exist on the DB : INSERT DB
#
#                 if (del_ind_field == '0') and (not (SystemSettings.objects.filter (
#                          pwd_policy 	=column[11]
#                         ,login_attempts 	=column[8]
#                         ,session_timeout 	=column[12]
#                         ,msg_display 		=column[9]
#                         ,theme_color 		=column[13]
#                         ,pagination_count	=column[10]
#                         ,attachment_size 	=column[7]
#                         ,attachment_extension =column[6]
#                         ,attribute_09 		=column[0]
#                         ,attribute_10 		=column[1]
#                         ,attribute_11 		=column[2]
#                         ,attribute_12 		=column[3]
#                         ,attribute_13 		=column[4]
#                         ,attribute_14 		=column[5]
#                         , client=client ).exists())):
#                     _, created = SystemSettings.objects.get_or_create (
#                                      guid = guid_generator()
#                                     ,pwd_policy 		=column[11]
#                                     ,login_attempts 	=column[8]
#                                     ,session_timeout 	=column[12]
#                                     ,msg_display 		=column[9]
#                                     ,theme_color 		=column[13]
#                                     ,pagination_count	=column[10]
#                                     ,attachment_size 	=column[7]
#                                     ,attachment_extension =column[6]
#                                     ,attribute_09 		=column[0]
#                                     ,attribute_10 		=column[1]
#                                     ,attribute_11 		=column[2]
#                                     ,attribute_12 		=column[3]
#                                     ,attribute_13 		=column[4]
#                                     ,attribute_14 		=column[5]
#                                     , client=OrgClients.objects.get ( client=client))
#
#                     systemsettings_inserted_cnt = systemsettings_inserted_cnt + 1
#                     Data_saved = 'Y'
#
#                 # If the Deletion indicator in the file = "0" and record  exist on the DB : Update DB
#
#                 elif (del_ind_field == '0') and (SystemSettings.objects.filter (
#                          pwd_policy 	=column[11]
#                         ,login_attempts 	=column[8]
#                         ,session_timeout 	=column[12]
#                         ,msg_display 		=column[9]
#                         ,theme_color 		=column[13]
#                         ,pagination_count	=column[10]
#                         ,attachment_size 	=column[7]
#                         ,attachment_extension =column[6]
#                         ,attribute_09 		=column[0]
#                         ,attribute_10 		=column[1]
#                         ,attribute_11 		=column[2]
#                         ,attribute_12 		=column[3]
#                         ,attribute_13 		=column[4]
#                         ,attribute_14 		=column[5])).exists ():
#                     SystemSettings.objects.filter (
#                         pwd_policy 	        =column[11]
#                         ,login_attempts 	=column[8]
#                         ,session_timeout 	=column[12]
#                         ,msg_display 		=column[9]
#                         ,theme_color 		=column[13]
#                         ,pagination_count	=column[10]
#                         ,attachment_size 	=column[7]
#                         ,attachment_extension =column[6]
#                         ,attribute_09 		=column[0]
#                         ,attribute_10 		=column[1]
#                         ,attribute_11 		=column[2]
#                         ,attribute_12 		=column[3]
#                         ,attribute_13 		=column[4]
#                         ,attribute_14 		=column[5]
#                         ,client=OrgClients.objects.get ( client=client )
#                     )
#
#                     systemsettings_updated_cnt = systemsettings_updated_cnt + 1
#                     Data_saved = 'Y'
#
#                 # If the Deletion indicator in the file = "1" and record  exist on the DB : Soft Delete(del_ind =0) DB
#
#                 if (del_ind_field == '1') and (SystemSettings.objects.filter (
#                          pwd_policy 	=column[11]
#                         ,login_attempts 	=column[8]
#                         ,session_timeout 	=column[12]
#                         ,msg_display 		=column[9]
#                         ,theme_color 		=column[13]
#                         ,pagination_count	=column[10]
#                         ,attachment_size 	=column[7]
#                         ,attachment_extension =column[6]
#                         ,attribute_09 		=column[0]
#                         ,attribute_10 		=column[1]
#                         ,attribute_11 		=column[2]
#                         ,attribute_12 		=column[3]
#                         ,attribute_13 		=column[4]
#                         ,attribute_14 		=column[5] ).exists ()):
#                     queryset_del = SystemSettings.objects.filter(
#                         pwd_policy          =column[11]
#                         ,login_attempts 	=column[8]
#                         ,session_timeout 	=column[12]
#                         ,msg_display 		=column[9]
#                         ,theme_color 		=column[13]
#                         ,pagination_count	    =column[10]
#                         ,attachment_size 	=column[7]
#                         ,attachment_extension  =column[6]
#                         ,attribute_09 		=column[0]
#                         ,attribute_10 		=column[1]
#                         ,attribute_11 		=column[2]
#                         ,attribute_12 		=column[3]
#                         ,attribute_13 		=column[4]
#                         ,attribute_14 		=column[5]).delete()
#
#                     systemsettings_deleted_cnt = systemsettings_deleted_cnt + 1
#                     Data_saved = 'Y'
#
#                 # If the Deletion indicator in the file = "1" and record  does not exist on the DB : Error message
#
#                 elif (del_ind_field == '1') and (not (SystemSettings.objects.filter (
#                         pwd_policy          =column[11]
#                         ,login_attempts 	=column[8]
#                         ,session_timeout 	=column[12]
#                         ,msg_display 		=column[9]
#                         ,theme_color 		=column[13]
#                         ,pagination_count	    =column[10]
#                         ,attachment_size 	=column[7]
#                         ,attachment_extension  =column[6]
#                         ,attribute_09 		=column[0]
#                         ,attribute_10 		=column[1]
#                         ,attribute_11 		=column[2]
#                         ,attribute_12 		=column[3]
#                         ,attribute_13 		=column[4]
#                         ,attribute_14 		=column[5]).exists ())):
#                     systemsettings_delete_error = 'Y'
#                     systemsettings_delete_Err_Count = systemsettings_delete_Err_Count + 1
#
#
#             # Display insert /updated count in the display
#             systemsettings_DB_count = SystemSettings.objects.filter ().count ()
#
#             # Display the number of Active records in DB
#             messages.success ( req, ' Number of Active Records in Database    : ' + str ( systemsettings_DB_count ) )
#             # Display the number of records Inserted
#             messages.success ( req, ' Records Inserted      : ' + str ( systemsettings_inserted_cnt ) )
#             # Display the number of records Updated
#             messages.success ( req, ' Records Updated       : ' + str ( systemsettings_updated_cnt ) )
#             # Display the number of records Deleted
#             messages.success ( req, ' Records Deleted       : ' + str ( systemsettings_deleted_cnt ) )
#
#             # Display message for empty file
#             if systemsettings_line_no == 0:
#                 messages.error ( req, ' Empty File : Please correct and try again ' )
#                 Data_saved = ''
#
#             # Display error message if delete record doesnt exist on DB
#             if systemsettings_delete_error != '':
#                 messages.error ( req,' Input Delete records that dont exist in DB : ' + str ( systemsettings_delete_Err_Count ) )
#
#
#         if Data_saved == 'Y':
#             messages.success ( req, MSG037 )
#         else:
#             messages.error ( req, MSG043 )
#
#
#
#     except Exception as e:
#         print ( e )
#         messages.error ( req,'Error : ' + str(e) )

