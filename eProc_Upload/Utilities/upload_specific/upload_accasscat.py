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

# upload Accounting Data csv data file into MMD_ACC_AST_CAT db table - Shankar - SP11-13
from eProc_Configuration.models.development_data import *


def upload_accasscat(req, accascat, Test_mode):
    """
    on uploading of AccountAssignmentCategory  csv file
    1. GET Accounting Data csv file and store its respective field values into MMD_ACC_AST_CAT db table
    :param req: UI request
    :param AccountAssignmentCategory: attached csv file data
    :param Test_mode : Diagnostics
    :return: return true on success, return false on failure
    """
    try:

        # If the Test Mode check box is checked then run diagnostics.
        if Test_mode == 'on':

            # Diagnostics mode variables
            Test_Insert_Count_accasscat = 0
            Test_Update_Count_accasscat = 0
            Test_Delete_Count_accasscat = 0
            Test_Duplicate_Count_accasscat = 0
            Test_File_Count_accasscat = 0
            Test_Delete_Err_Count_accasscat = 0
            Test_accasscat_delete_error = ''
            Test_accasscat_number_list = []
            Data_saved = ''

            Test_accasscat_DB_count = AccountAssignmentCategory.objects.filter(del_ind=False).count()

            # Read thru the file record by record , Assign column based on comma delimiter

            for column in csv.reader(accascat, delimiter=',', quotechar='"'):

                Test_File_Count_accasscat = Test_File_Count_accasscat + 1
                del_ind_field = column[2]

                # If the Input file Deletion indicator is "0" (Insert\Update record) and accasscat  exist in the accasscat table

                if (del_ind_field == '0') and (
                not (AccountAssignmentCategory.objects.filter(account_assign_cat=column[0]).exists())):
                    if column[0] in Test_accasscat_number_list:
                        Test_Duplicate_Count_accasscat = Test_Duplicate_Count_accasscat + 1
                        error_msg = get_message_desc(MSG094)[1]
                        # msgid = 'MSG094'
                        # error_msg = get_msg_desc(msgid)
                        # msg = error_msg['message_desc'][0]
                        # error_msg = msg

                        Test_accasscat_errmsg_duplicate = error_msg
                    else:
                        Test_Insert_Count_accasscat = Test_Insert_Count_accasscat + 1


                # If the Input file Deletion indicator is "0" (Insert\Update record) and AccountAssignmentCategory key  exist in the AccountAssignmentCategory table

                elif (del_ind_field == '0') and (
                AccountAssignmentCategory.objects.filter(account_assign_cat=column[0], del_ind=0).exists()):
                    queryset_test_upd = AccountAssignmentCategory.objects.filter(account_assign_cat=column[0])
                    for test in queryset_test_upd:
                        if (test.description != column[1]):
                            Test_Update_Count_accasscat = Test_Update_Count_accasscat + 1
                        else:
                            Test_Duplicate_Count_accasscat = Test_Duplicate_Count_accasscat + 1
                            error_msg = get_message_desc(MSG094)[1]
                            # msgid = 'MSG094'
                            # error_msg = get_msg_desc(msgid)
                            # msg = error_msg['message_desc'][0]
                            # error_msg = msg
                            Test_accasscat_errmsg_duplicate = error_msg

                # If the Input file Deletion indicator is "1" (Delete record) and AccountAssignmentCategory key  exist in the AccountAssignmentCategory table

                if (del_ind_field == '1') and (
                AccountAssignmentCategory.objects.filter(account_assign_cat=column[0], del_ind=0).exists()):
                    queryset_test_del = AccountAssignmentCategory.objects.filter(account_assign_cat=column[0])

                    # If the Deletion indicator is set to False (active record) , increment Delete counts
                    for test in queryset_test_del:
                        if test.del_ind == False:
                            Test_Delete_Count_accasscat = Test_Delete_Count_accasscat + 1

                # If the Input file Deletion indicator is "1" (Delete record) and AccountAssignmentCategory key  does not exist in the AccountAssignmentCategory table.
                # Raise delete error

                elif (del_ind_field == '1') and (
                not (AccountAssignmentCategory.objects.filter(account_assign_cat=column[0], del_ind=0).exists())):
                    Test_accasscat_delete_error = 'Y'
                    Test_Delete_Err_Count_accasscat = Test_Delete_Err_Count_accasscat + 1

                # Append the processed record to the array list , for validation of next record.
                Test_accasscat_number_list.append(column[0])
                print(Test_accasscat_number_list)
            # Display insert /updated count in the display

            # Number of active records on the Database.
            messages.info(req, 'Test Mode Diagnostics:')
            messages.info(req, '----------------------------- ')

            # Number of active records on the Database.
            messages.success(req, ' Number of Records in Database    : ' + str(Test_accasscat_DB_count))
            # Number of records in the Input file.
            messages.success(req, ' Number of Records in Input file  : ' + str(Test_File_Count_accasscat))
            # Total records that need to be inserted.
            messages.success(req, ' Records to be Inserted           : ' + str(Test_Insert_Count_accasscat))
            # Total records that need to be Updated.
            messages.success(req, ' Records to be Updated            : ' + str(Test_Update_Count_accasscat))
            # Total records that need to be Deleted.
            messages.success(req, ' Records to be Deleted            : ' + str(Test_Delete_Count_accasscat))
            # Total records that are duplicate in the input file
            messages.error(req, ' Duplicate Records                : ' + str(Test_Duplicate_Count_accasscat))

            # Display error message for delete records that dont exist in the DB
            if Test_accasscat_delete_error != '':
                messages.error(req,
                               ' Input Delete records that dont exist in DB : ' + str(Test_Delete_Err_Count_accasscat))

            # Display error message for Empty input file
            if Test_File_Count_accasscat == 0:
                messages.error(req, ' Empty File : Please correct and try again ')

        # If the Test Mode check box is Un-checked , Do File processing.

        if Test_mode != 'on':

            accasscat_line_no = 0
            accasscat_inserted_cnt = 0
            accasscat_updated_cnt = 0
            accasscat_deleted_cnt = 0
            accasscat_duplicate_cnt = 0
            Addr_DB_count = 0
            accasscat_delete_Err_Count = 0
            accasscat_delete_error = ''
            accasscat_line_no = 0
            Data_saved = ''

            # Read thru the file record by record , Assign column based on comma delimter

            for column in csv.reader(accascat, delimiter=',', quotechar='"'):
                accasscat_line_no = accasscat_line_no + 1

                print("AccountAssignmentCategory Extract Line Number:" + str(accasscat_line_no))

                accasscat_errmsg_duplicate = ''
                accasscat_error_flag = ''
                del_ind_field = column[2]

                # If the Input file Deletion indicator is "0" (Insert\Update record) and AccountAssignmentCategory key  does not exist in the AccountAssignmentCategory table

                if (del_ind_field == '0') and (
                not (AccountAssignmentCategory.objects.filter(account_assign_cat=column[0], del_ind=0)).exists()):
                    # get AccountAssignmentCategorys data from attached file and store it to MMD_ACC_AST_CAT db table
                    _, Created = AccountAssignmentCategory.objects.get_or_create(
                        account_assign_cat=column[0],
                        description=column[1],
                        del_ind=column[2]
                    )
                    accasscat_inserted_cnt = accasscat_inserted_cnt + 1
                    Data_saved = 'Y'

                # If the Input file Deletion indicator is "0" (Insert\Update record) and AccountAssignmentCategory key  exist in the AccountAssignmentCategory table

                if (del_ind_field == '0') and (
                AccountAssignmentCategory.objects.filter(account_assign_cat=column[0], del_ind=0).exists()):
                    queryset_test_upd = AccountAssignmentCategory.objects.filter(account_assign_cat=column[0])
                    for test in queryset_test_upd:
                        if (test.description != column[1]):
                            AccountAssignmentCategory.objects.filter(account_assign_cat=column[0]).update(
                                description=column[1],
                                del_ind=column[2])
                            accasscat_updated_cnt = accasscat_updated_cnt + 1
                            Data_saved = 'Y'
                        else:
                            accasscat_duplicate_cnt = accasscat_duplicate_cnt + 1
                            error_msg = get_message_desc(MSG094)[1]
                            # msgid = 'MSG094'
                            # error_msg = get_msg_desc(msgid)
                            # msg = error_msg['message_desc'][0]
                            # error_msg = msg
                            accasscat_errmsg_duplicate = error_msg
                            accasscat_error_flag = 'Y'

                # If the Input file Deletion indicator is "1" (Delete record) and AccountAssignmentCategory key  exist in the AccountAssignmentCategory table

                if (del_ind_field == '1') and (
                AccountAssignmentCategory.objects.filter(account_assign_cat=column[0], del_ind=0).exists()):
                    AccountAssignmentCategory.objects.filter(account_assign_cat=column[0], del_ind=0).update(del_ind=1)
                    accasscat_deleted_cnt = accasscat_deleted_cnt + 1
                    Data_saved = 'Y'

                # If the Input file Deletion indicator is "1" (Delete record) and AccountAssignmentCategory key  does not exist in the AccountAssignmentCategory table.
                # Raise delete error

                if (del_ind_field == '1') and (
                not (AccountAssignmentCategory.objects.filter(account_assign_cat=column[0]).exists())):
                    accasscat_delete_error = 'Y'
                    accasscat_delete_Err_Count = accasscat_delete_Err_Count + 1

            # Messages Summarising of processing of input file.\
            messages.info(req, 'Database Upload Results  :')
            messages.info(req, '-------------------------------')

            accasscat_DB_count = AccountAssignmentCategory.objects.filter(del_ind=0).count()
            # Display the number of Active records in DB
            messages.success(req, ' Number of Records in Database    : ' + str(accasscat_DB_count))
            # Number of records in the Input file.
            messages.success(req, ' Number of Records in Input file  : ' + str(accasscat_line_no))
            # Display the number of records Inserted
            messages.success(req, ' Records Inserted      : ' + str(accasscat_inserted_cnt))
            # Display the number of records Updated
            messages.success(req, ' Records Updated       : ' + str(accasscat_updated_cnt))
            # Display the number of records Deleted
            messages.success(req, ' Records Deleted       : ' + str(accasscat_deleted_cnt))

            if accasscat_line_no == 0:
                messages.error(req, ' Empty File : Please correct and try again ')

            if accasscat_delete_error != '':
                messages.error(req, ' Input Delete records that dont exist in DB : ' + str(accasscat_delete_Err_Count))

        if Data_saved != 'Y':
            error_msg = get_message_desc(MSG043)[1]
            # msgid = 'MSG043'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            messages.error(req, error_msg)
            # messages.error(req, MSG043)
        else:
            error_msg = get_message_desc(MSG037)[1]
            # msgid = 'MSG037'
            # error_msg = get_msg_desc(msgid)
            messages.success(req, error_msg)

            # messages.success(req, MSG037)


    except Exception as e:
        print(e)
        messages.error(req, 'Error : ' + str(e))


def upload_accasscat_new(accascat):
    """
    on uploading of AccountAssignmentCategory  csv file
    1. GET Accounting Data csv file and store its respective field values into MMD_ACC_AST_CAT db table
    :param req: UI request
    :param AccountAssignmentCategory: attached csv file data
    :param Test_mode : Diagnostics
    :return: return true on success, return false on failure
    """
    check_messages = []

    try:
        # Diagnostics mode variables
        Test_Insert_Count_accasscat = 0
        Test_Update_Count_accasscat = 0
        Test_Delete_Count_accasscat = 0
        Test_Duplicate_Count_accasscat = 0
        Test_File_Count_accasscat = 0
        Test_Delete_Err_Count_accasscat = 0
        Test_accasscat_delete_error = ''
        Test_accasscat_number_list = []
        Data_saved = ''

        Test_accasscat_DB_count = AccountAssignmentCategory.objects.filter(del_ind=False).count()

        # Read thru the file record by record , Assign column based on comma delimiter

        for column in accascat:
            print(column)

            Test_File_Count_accasscat = Test_File_Count_accasscat + 1
            del_ind_field = column[5]

            # If the Input file Deletion indicator is "0" (Insert\Update record) and accasscat  exist in the accasscat table

            if (del_ind_field == '0') and (
                    not (AccountAssignmentCategory.objects.filter(account_assign_cat=column[0]).exists())):
                if column[0] in Test_accasscat_number_list:
                    Test_Duplicate_Count_accasscat = Test_Duplicate_Count_accasscat + 1
                    error_msg = get_message_desc(MSG094)[1]
                    # msgid = 'MSG094'
                    # error_msg = get_msg_desc(msgid)
                    # msg = error_msg['message_desc'][0]
                    # error_msg = msg
                    Test_accasscat_errmsg_duplicate = error_msg
                else:
                    Test_Insert_Count_accasscat = Test_Insert_Count_accasscat + 1


            # If the Input file Deletion indicator is "0" (Insert\Update record) and AccountAssignmentCategory key  exist in the AccountAssignmentCategory table

            elif (del_ind_field == '0') and (
                    AccountAssignmentCategory.objects.filter(account_assign_cat=column[0], del_ind=0).exists()):
                queryset_test_upd = AccountAssignmentCategory.objects.filter(account_assign_cat=column[0])
                for test in queryset_test_upd:
                    if (test.description != column[1]):
                        Test_Update_Count_accasscat = Test_Update_Count_accasscat + 1
                    else:
                        Test_Duplicate_Count_accasscat = Test_Duplicate_Count_accasscat + 1
                        error_msg = get_message_desc(MSG094)[1]
                        # msgid = 'MSG094'
                        # error_msg = get_msg_desc(msgid)
                        # msg = error_msg['message_desc'][0]
                        # error_msg = msg
                        Test_accasscat_errmsg_duplicate = error_msg

            # If the Input file Deletion indicator is "1" (Delete record) and AccountAssignmentCategory key  exist in the AccountAssignmentCategory table

            if (del_ind_field == '1') and (
                    AccountAssignmentCategory.objects.filter(account_assign_cat=column[0], del_ind=0).exists()):
                queryset_test_del = AccountAssignmentCategory.objects.filter(account_assign_cat=column[0])

                # If the Deletion indicator is set to False (active record) , increment Delete counts
                for test in queryset_test_del:
                    if test.del_ind == False:
                        Test_Delete_Count_accasscat = Test_Delete_Count_accasscat + 1

            # If the Input file Deletion indicator is "1" (Delete record) and AccountAssignmentCategory key  does not exist in the AccountAssignmentCategory table.
            # Raise delete error

            elif (del_ind_field == '1') and (
                    not (AccountAssignmentCategory.objects.filter(account_assign_cat=column[0], del_ind=0).exists())):
                Test_accasscat_delete_error = 'Y'
                Test_Delete_Err_Count_accasscat = Test_Delete_Err_Count_accasscat + 1

            # Append the processed record to the array list , for validation of next record.
            Test_accasscat_number_list.append(column[0])
            print(Test_accasscat_number_list)
            print(Test_Insert_Count_accasscat)

            check_messages['db_count'] = Test_accasscat_DB_count
            check_messages['file_count'] = Test_File_Count_accasscat
            check_messages['duplicate_count'] = Test_Duplicate_Count_accasscat
            check_messages['insert_count'] = Test_Insert_Count_accasscat
            check_messages['update_count'] = Test_Update_Count_accasscat
            check_messages['delete_count'] = Test_Delete_Err_Count_accasscat

        return check_messages

    except Exception as e:
        print(e)
        messages.error('Error : ' + str(e))
