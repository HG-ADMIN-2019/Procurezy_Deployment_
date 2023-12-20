import csv
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.models import *
from eProc_Configuration.models import Currency, WorkflowACC
from eProc_Configuration.models.development_data import *
from django.contrib import messages
from eProc_Basic.Utilities.messages.messages import *


# upload Workflow ACC  csv data file into MMD_WF_ACC  db table - Shankar - SP12-06
def upload_wfacc(req, wfacc, Test_mode):
    """
    on uploading of MMD_WF_ACC   csv file
    1. GET Address Map csv file and store its respective field values into MMD_WF_ACC  db table
    :param req: UI request
    :param wfacc: attached csv file data
    :param Test_mode : Diagnostics
    :return: return true on success, return false on failure
    """

    try:

        client = getClients(req)
        # If the Test Mode check box is checked then run diagnostics.

        if Test_mode == 'on':

            # Diagnostics mode variables
            Test_DB_count_wfacc = 0
            Test_Insert_Count_wfacc = 0
            Test_Update_Count_wfacc = 0
            Test_Delete_Count_wfacc = 0
            Test_File_Count_wfacc = 0
            Test_Delete_Err_Count_wfacc = 0
            Test_Duplicate_Count_wfacc = 0
            Test_wfacc_delete_error = ''
            Test_wfacc_number_list = []

            Data_saved = ''

            Test_DB_count_wfacc = WorkflowACC.objects.filter(del_ind=False).count()

            # Read thru the file record by record , Assign column based on comma delimter

            for column in csv.reader(wfacc, delimiter=',', quotechar='"'):

                Test_File_Count_wfacc = Test_File_Count_wfacc + 1
                del_ind_field = column[8]

                print("Workflow ACC  Extract Line Number:" + str(Test_File_Count_wfacc))

                Test_Wfacc_errmsg_Accasscat = ''
                Test_Wfacc_errmsg_Currency = ''
                Test_Wfacc_error_flag = ''

                if not (AccountAssignmentCategory.objects.filter(account_assign_cat=column[5]).exists()):
                    Test_Wfacc_errmsg_Accasscat = 'Parent Record Not Found on Account Assignment Category table for account_assign_cat'
                    messages.error(req, Test_Wfacc_errmsg_Accasscat + ' @Line Number : '
                                   + str(Test_File_Count_wfacc))
                    Wfacc_error_flag = 'Y'

                if not (AccountAssignmentCategory.objects.filter(account_assign_cat=column[6]).exists()):
                    Test_Wfacc_errmsg_Accasscat = 'Parent Record Not Found on Account Assignment Category table for sup_account_assign_cat'
                    messages.error(req, Test_Wfacc_errmsg_Accasscat + ' @Line Number : '
                                   + str(Test_File_Count_wfacc))
                    Wfacc_error_flag = 'Y'

                if not (Currency.objects.filter(object_id=column[3]).exists()):
                    Test_Wfacc_errmsg_Currency = 'Parent Record Not Found on Currency table'
                    messages.error(req, Test_Wfacc_errmsg_Currency + ' @Line Number : '
                                   + str(Test_File_Count_wfacc))
                    Wfacc_error_flag = 'Y'

                if Wfacc_error_flag != '':
                    continue

                # If the Input file Deletion indicator is "0" (Insert\Update record) and Country  exist in the Country table

                if (del_ind_field == '0') and (WorkflowACC.objects.filter(app_username=column[0],
                                                                          acc_value=column[1],
                                                                          company_id=column[3],
                                                                          account_assign_cat=column[5],
                                                                          currency_id=column[7],
                                                                          client=client,
                                                                          del_ind=0).exists()):
                    queryset_test_upd = WorkflowACC.objects.filter(app_username=column[0],
                                                                   acc_value=column[1],
                                                                   company_id=column[3],
                                                                   account_assign_cat=column[5],
                                                                   currency_id=column[7],
                                                                   client=client,
                                                                   del_ind=0)
                    for test in queryset_test_upd:
                        if test.sup_acc_value != column[2] or test.sup_company_id != column[
                            4] or test.sup_account_assign_cat != column[6]:
                            Test_Update_Count_wfacc = Test_Update_Count_wfacc + 1
                        else:
                            Test_Duplicate_Count_wfacc = Test_Duplicate_Count_wfacc + 1

                # If the Input file Deletion indicator is "0" (Insert\Update record) and country key  does not exist in the country table
                elif (del_ind_field == '0') and (
                        not (WorkflowACC.objects.filter(app_username=column[0],
                                                        acc_value=column[1],
                                                        company_id=column[3],
                                                        account_assign_cat=column[5],
                                                        currency_id=column[7],
                                                        client=client,
                                                        del_ind=0).exists())):
                    if column[0] in Test_wfacc_number_list:
                        Test_Duplicate_Count_wfacc = Test_Duplicate_Count_wfacc + 1
                        error_msg = get_message_desc(MSG094)[1]
                        # msgid = 'MSG094'
                        # error_msg = get_msg_desc(msgid)
                        # msg = error_msg['message_desc'][0]
                        # error_msg = msg
                        Test_wfacc_errmsg_duplicate = error_msg
                    # Else the record is a valid Insert record update insert count
                    else:
                        Test_Insert_Count_wfacc = Test_Insert_Count_wfacc + 1

                # Check  If the Input file Deletion indicator is "1" (Delete record) and if record  exists
                # Check if the record is active on DB.

                if (del_ind_field == '1') and (WorkflowACC.objects.filter(app_username=column[0],
                                                                          acc_value=column[1],
                                                                          company_id=column[3],
                                                                          account_assign_cat=column[5],
                                                                          currency_id=column[7],
                                                                          client=client,
                                                                          del_ind=0).exists()):
                    queryset_test_del = WorkflowACC.objects.filter(app_username=column[0],
                                                                   acc_value=column[1],
                                                                   company_id=column[3],
                                                                   account_assign_cat=column[5],
                                                                   currency_id=column[7],
                                                                   client=client,
                                                                   del_ind=0)
                    for test in queryset_test_del:
                        if test.del_ind == False:
                            Test_Delete_Count_wfacc = Test_Delete_Count_wfacc + 1

                # Check  If the Input file Deletion indicator is "1" (Delete record) and if record does not exists
                # report as invalid record.

                elif (del_ind_field == '1') and (
                        not (WorkflowACC.objects.filter(app_username=column[0],
                                                        acc_value=column[1],
                                                        company_id=column[3],
                                                        account_assign_cat=column[5],
                                                        currency_id=column[7],
                                                        client=client,
                                                        del_ind=0).exists())):
                    Test_wfacc_delete_error = 'Y'
                    Test_Delete_Err_Count_wfacc = Test_Delete_Err_Count_wfacc + 1

                # Append the input key to the Array list for checking the next reocrds for dups.

                Test_wfacc_number_list.append(column[0])

            # Display insert /updated count in the display

            messages.info(req, 'Test Mode Diagnostics:')
            messages.info(req, '-----------------------------')

            # Number of active records on the Database.
            messages.success(req, ' Number of Records in Database    : ' + str(Test_DB_count_wfacc))
            # Number of records in the Input file.
            messages.success(req, ' Number of Records in Input file  : ' + str(Test_File_Count_wfacc))
            # Total records that need to be inserted.
            messages.success(req, ' Records to be Inserted           : ' + str(Test_Insert_Count_wfacc))
            # Total records that need to be Updated.
            messages.success(req, ' Records to be Updated            : ' + str(Test_Update_Count_wfacc))
            # Total records that need to be Deleted.
            messages.success(req, ' Records to be Deleted            : ' + str(Test_Delete_Count_wfacc))
            # Total records that are duplicate in the input file
            messages.error(req, ' Duplicate Records                : ' + str(Test_Duplicate_Count_wfacc))

            # Display the number of delete records that dont exist on DB
            if Test_wfacc_delete_error == 'Y':
                messages.error(req, ' Input Delete records that dont exist in DB : ' + str(
                    Test_Delete_Err_Count_wfacc))

            # Display error message for empty file
            if Test_File_Count_wfacc == 0:
                messages.error(req, ' Empty File : Please correct and try again ')


        elif Test_mode != 'on':

            Wfacc_line_no = 0
            Wfacc_inserted_cnt = 0
            Wfacc_updated_cnt = 0
            Wfacc_deleted_cnt = 0
            Wfacc_DB_count = 0
            Wfacc_delete_Err_Count = 0
            Wfacc_delete_error = ''
            Data_saved = ''

            for column in csv.reader(wfacc, delimiter=',', quotechar='"'):
                Wfacc_line_no = Wfacc_line_no + 1
                print("Workflow ACC  Extract Line Number:" + str(Wfacc_line_no))

                del_ind_field = column[8]

                Wfacc_errmsg_Accasscat = ''
                Wfacc_errmsg_Currency = ''
                Wfacc_error_flag = ''

                if not (AccountAssignmentCategory.objects.filter(account_assign_cat=column[5]).exists()):
                    # Wfacc_errmsg_Companies = 'Parent Record Not Found on Wfacc table'
                    Wfacc_errmsg_Accasscat = 'Parent Record Not Found on Account Assignment Category table for account_assign_cat'
                    messages.error(req, Wfacc_errmsg_Accasscat + ' @Line Number : '
                                   + str(Wfacc_line_no))
                    Wfacc_error_flag = 'Y'

                if not (AccountAssignmentCategory.objects.filter(account_assign_cat=column[6]).exists()):
                    Wfacc_errmsg_SupAccasscat = 'Parent Record Not Found on Account Assignment Category table for sup_account_assign_cat'
                    messages.error(req, Wfacc_errmsg_SupAccasscat + ' @Line Number : '
                                   + str(Wfacc_line_no))
                    Wfacc_error_flag = 'Y'

                if not (Currency.objects.filter(currency_id=column[7]).exists()):
                    Wfacc_errmsg_Currency = 'Parent Record Not Found on Currency table'
                    messages.error(req, Wfacc_errmsg_Currency + ' @Line Number : '
                                   + str(Wfacc_line_no))
                    Wfacc_error_flag = 'Y'

                if Wfacc_error_flag != '':
                    continue

                # If the Deletion indicator in the file = "0" and record does not exist on the DB : INSERT DB

                if (del_ind_field == '0') and (not (WorkflowACC.objects.filter(app_username=column[0],
                                                                               acc_value=column[1],
                                                                               company_id=column[3],
                                                                               account_assign_cat=column[5],
                                                                               currency_id=column[7],
                                                                               client=client,
                                                                               del_ind=0).exists())):
                    _, created = WorkflowACC.objects.get_or_create(workflow_acc_guid=guid_generator(),
                                                                   app_username=column[0],
                                                                   acc_value=column[1],
                                                                   sup_acc_value=column[2],
                                                                   company_id=column[3],
                                                                   sup_company_id=column[4],
                                                                   account_assign_cat=AccountAssignmentCategory.objects.get(
                                                                       account_assign_cat=column[5]),
                                                                   sup_account_assign_cat=AccountAssignmentCategory.objects.get(
                                                                       account_assign_cat=column[6]),
                                                                   currency_id=Currency.objects.get(
                                                                       currency_id=column[7]),
                                                                   client=client,
                                                                   del_ind=0)
                    Wfacc_inserted_cnt = Wfacc_inserted_cnt + 1
                    Data_saved = 'Y'

                # If the Deletion indicator in the file = "0" and record  exist on the DB : Update DB

                elif (del_ind_field == '0') and (WorkflowACC.objects.filter(app_username=column[0],
                                                                            acc_value=column[1],
                                                                            company_id=column[3],
                                                                            account_assign_cat=column[5],
                                                                            currency_id=column[7],
                                                                            client=client,
                                                                            del_ind=0).exists()):
                    queryset_upd = WorkflowACC.objects.filter(app_username=column[0],
                                                              acc_value=column[1],
                                                              company_id=column[3],
                                                              account_assign_cat=column[5],
                                                              currency_id=column[7],
                                                              client=client,
                                                              del_ind=0)
                    for test in queryset_upd:
                        if test.sup_acc_value != column[2] or test.sup_company_id != column[
                            4] or test.sup_account_assign_cat != column[6]:
                            WorkflowACC.objects.filter(app_username=column[0],
                                                       acc_value=column[1],
                                                       company_id=column[3],
                                                       account_assign_cat=column[5],
                                                       currency_id=column[7],
                                                       client=client,
                                                       del_ind=0).update(
                                app_username=column[0],
                                acc_value=column[1],
                                sup_acc_value=column[2],
                                company_id=column[3],
                                sup_company_id=column[4],
                                account_assign_cat=AccountAssignmentCategory.objects.get(account_assign_cat=column[5]),
                                sup_account_assign_cat=AccountAssignmentCategory.objects.get(
                                    account_assign_cat=column[6]),
                                currency_id=Currency.objects.get(currency_id=column[7]),
                                client=client,
                                del_ind=0)

                            Wfacc_updated_cnt = Wfacc_updated_cnt + 1
                            Data_saved = 'Y'

                # If the Deletion indicator in the file = "1" and record  exist on the DB : Soft Delete(del_ind =0) DB

                if (del_ind_field == '1') and (WorkflowACC.objects.filter(app_username=column[0],
                                                                          acc_value=column[1],
                                                                          company_id=column[3],
                                                                          account_assign_cat=column[5],
                                                                          currency_id=column[7],
                                                                          client=client,
                                                                          del_ind=0).exists()):
                    queryset_del = WorkflowACC.objects.filter(app_username=column[0],
                                                              acc_value=column[1],
                                                              company_id=column[3],
                                                              account_assign_cat=column[5],
                                                              currency_id=column[7],
                                                              client=client,
                                                              del_ind=0)
                    for test in queryset_del:
                        if test.del_ind == False:
                            WorkflowACC.objects.filter(app_username=column[0],
                                                       acc_value=column[1],
                                                       company_id=column[3],
                                                       account_assign_cat=column[5],
                                                       currency_id=column[7],
                                                       client=client,
                                                       del_ind=0).update(del_ind=1)
                            Wfacc_deleted_cnt = Wfacc_deleted_cnt + 1
                            Data_saved = 'Y'

                # If the Deletion indicator in the file = "1" and record  does not exist on the DB : Error message

                elif (del_ind_field == '1') and (not (WorkflowACC.objects.filter(
                        app_username=column[0],
                        acc_value=column[1],
                        company_id=column[3],
                        account_assign_cat=column[5],
                        currency_id=column[7],
                        client=client,
                        del_ind=0).exists())):
                    Wfacc_delete_error = 'Y'
                    Wfacc_delete_Err_Count = Wfacc_delete_Err_Count + 1

            # Display insert /updated count in the display
            Wfacc_DB_count = WorkflowACC.objects.filter(del_ind=False).count()

            messages.info(req, 'Database Upload Results  :')
            messages.info(req, '-------------------------------')

            # Display the number of Active records in DB
            messages.success(req, ' Number of Active Records in Database    : ' + str(Wfacc_DB_count))
            # Display the number of records Inserted
            messages.success(req, ' Records Inserted      : ' + str(Wfacc_inserted_cnt))
            # Display the number of records Updated
            messages.success(req, ' Records Updated       : ' + str(Wfacc_updated_cnt))
            # Display the number of records Deleted
            messages.success(req, ' Records Deleted       : ' + str(Wfacc_deleted_cnt))

            # Display message for empty file
            if Wfacc_line_no == 0:
                messages.error(req, ' Empty File : Please correct and try again ')
                Data_saved = ''

            # Display error message if delete record doesnt exist on DB
            if Wfacc_delete_error != '':
                messages.error(req, ' Input Delete records that dont exist in DB : ' + str(Wfacc_delete_Err_Count))

        if Data_saved == 'Y':
            msgid = 'message_type'
            error_msg = get_message_desc(msgid)[0]
            messages.success(req, error_msg)
            # messages.success ( req, message_type )
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
