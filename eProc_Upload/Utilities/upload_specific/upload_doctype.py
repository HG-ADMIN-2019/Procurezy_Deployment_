import csv
from django.contrib import messages

from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.models import *
from eProc_Basic.Utilities.messages.messages import *


# # upload Doctype csv data file into timezones db table - Shankar - SP10-19
from eProc_Configuration.models.development_data import DocumentType


def upload_doctype(req, doctype, Test_mode):
    #     """
    #     on uploading of Doctype csv file
    #     1. GET Doctype csv file and store its respective field values into MMD_doctype db table
    #     :param req: UI request
    #     :param timezone: attached csv file data
    #     :param Test_mode : Diagnostics
    #     :return: return true on success, return false on failure
    #     """
    #

    try:

        # If the Test Mode check box is checked then run diagnostics.

        if Test_mode == 'on':

            Test_DB_count_doctype           = 0
            Test_Insert_Count_doctype       = 0
            Test_Update_Count_doctype       = 0
            Test_Delete_Count_doctype       = 0
            Test_File_Count_doctype         = 0
            Test_Delete_Err_Count_doctype   = 0
            Test_doctype_delete_error       = ''
            Test_Duplicate_Count_doctype    = 0
            Test_DB_Duplicate_Count_doctype = 0
            Test_doctype_number_list        = []

            Data_saved                      = ''

            Test_DB_count_doctype = DocumentType.objects.filter ( del_ind=False ).count ()

            # Read thru the file record by record , Assign column based on comma delimter

            for column in csv.reader ( doctype, delimiter=',', quotechar='"' ):

                Test_File_Count_doctype = Test_File_Count_doctype + 1

                del_ind_field = column[2]

                # If the Input file Deletion indicator is "0" (Insert\Update record) and timezone  exist in the timezone table

                if (del_ind_field == '0') and (DocumentType.objects.filter ( document_type=column[0] ).exists ()):
                    queryset_test_upd = DocumentType.objects.filter ( document_type=column[0] )
                    for test in queryset_test_upd:
                        if (test.document_type_desc != column[1] ):
                            Test_Update_Count_doctype = Test_Update_Count_doctype + 1
                        else:
                            Test_Duplicate_Count_doctype = Test_Duplicate_Count_doctype + 1

                # If the Input file Deletion indicator is "0" (Insert\Update record) and timezone key  does not exist in the timezone table

                elif (del_ind_field == '0') and (not (DocumentType.objects.filter ( document_type=column[0] ).exists ())):
                    if column[0] in Test_doctype_number_list:
                        Test_Duplicate_Count_doctype = Test_Duplicate_Count_doctype + 1
                        error_msg = get_message_desc(MSG094)[1]
                        # msgid = 'MSG094'
                        # error_msg = get_msg_desc(msgid)
                        # msg = error_msg['message_desc'][0]
                        # error_msg = msg
                        Test_doctype_errmsg_duplicate = error_msg
                    else:
                        Test_Insert_Count_doctype = Test_Insert_Count_doctype + 1

                # Check  If the Input file Deletion indicator is "1" (Delete record) and if record  exists
                # Check if the record is active on DB.

                if (del_ind_field == '1') and (DocumentType.objects.filter ( document_type=column[0] ).exists ()):
                    queryset_test_del = DocumentType.objects.filter ( document_type=column[0] )
                    for test in queryset_test_del:
                        if test.del_ind == False:
                            Test_Delete_Count_doctype = Test_Delete_Count_doctype + 1

                # Check  If the Input file Deletion indicator is "1" (Delete record) and if record does not exists
                # report as invalid record.

                elif (del_ind_field == '1') and (
                        not (DocumentType.objects.filter ( document_type=column[0] ).exists ())):
                    Test_doctype_delete_error = 'Y'
                    Test_Delete_Err_Count_doctype = Test_Delete_Err_Count_doctype + 1

                # Append the input key to the Array list for checking the next reocrds for dups.

                Test_doctype_number_list.append ( column[0] )

            # Display insert /updated count in the display

            messages.info ( req, 'Test Mode Diagnostics:' )
            messages.info ( req, '-----------------------------' )

            # Number of active records on the Database.
            messages.success ( req, ' Number of Records in Database    : ' + str ( Test_DB_count_doctype ) )
            # Number of records in the Input file.
            messages.success ( req, ' Number of Records in Input file  : ' + str ( Test_File_Count_doctype ) )
            # Total records that need to be inserted.
            messages.success ( req, ' Records to be Inserted           : ' + str ( Test_Insert_Count_doctype ) )
            # Total records that need to be Updated.
            messages.success ( req, ' Records to be Updated            : ' + str ( Test_Update_Count_doctype ) )
            # Total records that need to be Deleted.
            messages.success ( req, ' Records to be Deleted            : ' + str ( Test_Delete_Count_doctype ) )
            # Total records that are duplicate in the input file
            messages.error ( req, ' Duplicate Records                : ' + str ( Test_Duplicate_Count_doctype ) )

            # Display the number of delete records that dont exist on DB

            if Test_doctype_delete_error != '':
                messages.error ( req, ' Input Delete records that dont exist in DB : ' + str (
                    Test_Delete_Err_Count_doctype ) )

            # Display error message for empty file

            if Test_File_Count_doctype == 0:
                messages.error ( req, ' Empty File : Please correct and try again ' )


        elif Test_mode != 'on':

            doctype_line_no             = 0
            doctype_inserted_cnt        = 0
            doctype_updated_cnt         = 0
            doctype_deleted_cnt         = 0
            doctype_DB_count            = 0
            doctype_delete_Err_Count    = 0
            doctype_delete_error        = ''
            Data_saved                  = ''

            for column in csv.reader ( doctype, delimiter=',', quotechar='"' ):
                doctype_line_no = doctype_line_no + 1
                print ( "Document Type Extract Line Number:" + str ( doctype_line_no ) )

                del_ind_field = column[2]

                # If the Deletion indicator in the file = "0" and record does not exist on the DB : INSERT DB

                if (del_ind_field == '0') and (not (DocumentType.objects.filter ( document_type=column[0] ).exists ())):
                    _, created = DocumentType.objects.get_or_create ( document_type=column[0], document_type_desc=column[1],
                                                                  del_ind=column[2] )
                    doctype_inserted_cnt = doctype_inserted_cnt + 1
                    Data_saved = 'Y'

                # If the Deletion indicator in the file = "0" and record  exist on the DB : Update DB

                elif (del_ind_field == '0') and (DocumentType.objects.filter ( document_type=column[0] ).exists ()):
                    queryset_upd = DocumentType.objects.filter ( document_type=column[0] )
                    for test in queryset_upd:
                        if (test.document_type_desc != column[1] ):
                            DocumentType.objects.filter ( document_type=column[0] ).update ( document_type_desc=column[1],
                                                                                     del_ind=column[2] )
                            doctype_updated_cnt = doctype_updated_cnt + 1
                            Data_saved = 'Y'

                # If the Deletion indicator in the file = "1" and record  exist on the DB : Soft Delete(del_ind =0) DB

                if (del_ind_field == '1') and (DocumentType.objects.filter ( document_type=column[0] ).exists ()):
                    queryset_del = DocumentType.objects.filter ( document_type=column[0] )
                    for test in queryset_del:
                        if test.del_ind == False:
                            DocumentType.objects.filter ( document_type=column[0] ).update ( del_ind=1 )
                            doctype_deleted_cnt = doctype_deleted_cnt + 1
                            Data_saved = 'Y'

                elif (del_ind_field == '1') and (not (DocumentType.objects.filter ( document_type=column[0] ).exists ())):
                    doctype_delete_error = 'y'
                    doctype_delete_Err_Count = doctype_delete_Err_Count + 1

            # Display insert /updated count in the display
            doctype_DB_count = DocumentType.objects.filter ( del_ind=False ).count ()



            messages.info ( req, 'Database Upload Results  :')
            messages.info ( req, '-------------------------------' )

            # Display the number of Active records in DB
            messages.success ( req, ' Number of Records in Database    : ' + str ( doctype_DB_count ) )
            # Number of records in the Input file.
            messages.success ( req, ' Number of Records in Input file  : ' + str ( doctype_line_no ) )
            # Display the number of records Inserted
            messages.success ( req, ' Records Inserted      : ' + str ( doctype_inserted_cnt ) )
            # Display the number of records Updated
            messages.success ( req, ' Records Updated       : ' + str ( doctype_updated_cnt ) )
            # Display the number of records Deleted
            messages.success ( req, ' Records Deleted       : ' + str ( doctype_deleted_cnt ) )

            # Display message for empty file
            if doctype_line_no == 0:
                messages.error ( req, ' Empty File : Please correct and try again ' )

            # Display error message if delete record doesnt exist on DB
            if doctype_delete_error != '':
                messages.error ( req,
                                 ' Input Delete records that dont exist in DB : ' + str ( doctype_delete_Err_Count ) )

        if Data_saved == 'Y':
            error_msg = get_message_desc(MSG037)[1]
            # msgid = 'MSG037'
            # error_msg = get_msg_desc(msgid)
            # messages.success(req, error_msg)

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

