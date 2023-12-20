import csv
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.models import *
from eProc_Configuration.models import Currency, UnspscCategories, OrgClients, OrgCompanies, \
    DetermineGLAccount
from eProc_Configuration.models.development_data import *
from django.contrib import messages
from eProc_Basic.Utilities.messages.messages import *


# upload Det Gl Acc csv data file into MMD_DET_GL_ACC db table - Shankar - SP12-06
def upload_detglacc(req, detglacc, Test_mode):
    """
    on uploading of MMD_DET_GL_ACC  csv file
    1. GET Det Gl Acc csv file and store its respective field values into MMD_DET_GL_ACC db table
    :param req: UI request
    :param Detglacc: attached csv file data
    :param Test_mode : Diagnostics
    :return: return true on success, return false on failure
    """

    try:

        client = getClients(req)
        # If the Test Mode check box is checked then run diagnostics.

        if Test_mode == 'on':

            # Diagnostics mode variables
            Test_DB_count_detglacc = 0
            Test_Insert_Count_detglacc = 0
            Test_Update_Count_detglacc = 0
            Test_Delete_Count_detglacc = 0
            Test_File_Count_detglacc = 0
            Test_Delete_Err_Count_detglacc = 0
            Test_Duplicate_Count_detglacc = 0
            Test_detglacc_delete_error = ''
            Test_detglacc_number_list = []
            Test_detglacc_error_flag = ''
            Data_saved = ''

            Test_DB_count_detglacc = DetermineGLAccount.objects.filter(del_ind=False).count()

            # Read thru the file record by record , Assign column based on comma delimter

            for column in csv.reader(detglacc, delimiter=',', quotechar='"'):

                Test_File_Count_detglacc = Test_File_Count_detglacc + 1
                del_ind_field = column[5]

                print("Determine GL Account  Extract Line Number:" + str(Test_File_Count_detglacc))

                # Check if the Currency code in the Det Gl Acc Input file has an entry in the Country table.

                if not (Currency.objects.filter(currency_id=column[7]).exists()):
                    Test_detglacc_errmsg_currency = 'Parent Record Not Found on Currency table'
                    messages.error(req,
                                   Test_detglacc_errmsg_currency + ' @Line Number : ' + str(Test_File_Count_detglacc))
                    Test_detglacc_error_flag = 'Y'

                # Check if the Language ID in the detglacc Input file has an entry in the UnspscCategories table.

                if not (UnspscCategories.objects.filter(prod_cat_id=column[8]).exists()):
                    Test_detglacc_errmsg_prodcat = 'Parent Record Not Found on Product Category table'
                    messages.error(req,
                                   Test_detglacc_errmsg_prodcat + ' @Line Number : ' + str(Test_File_Count_detglacc))
                    Test_detglacc_error_flag = 'Y'

                # Check if the AccountAssignmentCategory in the detglacc Input file has an entry in the AccountAssignmentCategory table.

                if not (AccountAssignmentCategory.objects.filter(account_assign_cat=column[6]).exists()):
                    Test_detglacc_errmsg_accasscat = 'Parent Record Not Found on Acccount Assignment Category table'
                    messages.error(req, Test_detglacc_errmsg_accasscat + ' @Line Number : ' + str(
                        Test_File_Count_detglacc))
                    Test_detglacc_error_flag = 'Y'

                # Check if the Company id in the detglacc Input file has an entry in the OrgCompanies table.

                if not (OrgCompanies.objects.filter(company_id=column[4]).exists()):
                    Test_detglacc_errmsg_accasscat = 'Parent Record Not Found on OrgCompanies table'
                    messages.error(req, Test_detglacc_errmsg_accasscat + ' @Line Number : ' + str(
                        Test_File_Count_detglacc))
                    Test_detglacc_error_flag = 'Y'

                # If any Parent table does not have an entry for value in detglacc file , Raise an Error
                if Test_detglacc_error_flag != '':
                    continue

                # If the Input file Deletion indicator is "0" (Insert\Update record)

                if (del_ind_field == '0') and (
                DetermineGLAccount.objects.filter(gl_acc_num=column[2], client=client).exists()):
                    queryset_test_upd = DetermineGLAccount.objects.filter(gl_acc_num=column[2], client=client)
                    for test in queryset_test_upd:
                        if (test.from_value != column[0] or test.to_value != column[1] or test.default != column[3]
                                or test.company_id != column[4] or test.del_ind != column[
                                    5] or test.account_assign_cat != column[6]
                                or test.currency_id != column[7] or test.prod_cat_id != column[8]):

                            Test_Update_Count_detglacc = Test_Update_Count_detglacc + 1
                        else:
                            Test_Duplicate_Count_detglacc = Test_Duplicate_Count_detglacc + 1

                # If the Input file Deletion indicator is "0" (Insert\Update record)
                elif (del_ind_field == '0') and (
                        not (DetermineGLAccount.objects.filter(gl_acc_num=column[2], client=client).exists())):
                    if column[3] in Test_detglacc_number_list:
                        Test_Duplicate_Count_detglacc = Test_Duplicate_Count_detglacc + 1
                        error_msg = get_message_desc(MSG094)[1]
                        # msgid = 'MSG094'
                        # error_msg = get_msg_desc(msgid)
                        # msg = error_msg['message_desc'][0]
                        # error_msg = msg
                        Test_detglacc_errmsg_duplicate = error_msg
                    # Else the record is a valid Insert record update insert count
                    else:
                        Test_Insert_Count_detglacc = Test_Insert_Count_detglacc + 1

                # Check  If the Input file Deletion indicator is "1" (Delete record) and if record  exists
                # Check if the record is active on DB.

                if (del_ind_field == '1') and (
                DetermineGLAccount.objects.filter(gl_acc_num=column[2], client=client).exists()):
                    queryset_test_del = DetermineGLAccount.objects.filter(gl_acc_num=column[2], client=client)
                    for test in queryset_test_del:
                        if test.del_ind == False:
                            Test_Delete_Count_detglacc = Test_Delete_Count_detglacc + 1

                # Check  If the Input file Deletion indicator is "1" (Delete record) and if record does not exists
                # report as invalid record.

                elif (del_ind_field == '1') and (
                        not (DetermineGLAccount.objects.filter(gl_account=column[2], client=client).exists())):
                    Test_detglacc_delete_error = 'Y'
                    Test_Delete_Err_Count_detglacc = Test_Delete_Err_Count_detglacc + 1

                # Append the input key to the Array list for checking the next reocrds for dups.

                Test_detglacc_number_list.append(column[0])

            # Display insert /updated count in the display

            messages.info(req, 'Test Mode Diagnostics:')
            messages.info(req, '-----------------------------')

            # Number of active records on the Database.
            messages.success(req, ' Number of Records in Database    : ' + str(Test_DB_count_detglacc))
            # Number of records in the Input file.
            messages.success(req, ' Number of Records in Input file  : ' + str(Test_File_Count_detglacc))
            # Total records that need to be inserted.
            messages.success(req, ' Records to be Inserted           : ' + str(Test_Insert_Count_detglacc))
            # Total records that need to be Updated.
            messages.success(req, ' Records to be Updated            : ' + str(Test_Update_Count_detglacc))
            # Total records that need to be Deleted.
            messages.success(req, ' Records to be Deleted            : ' + str(Test_Delete_Count_detglacc))
            # Total records that are duplicate in the input file
            messages.error(req, ' Duplicate Records                : ' + str(Test_Duplicate_Count_detglacc))

            # Display the number of delete records that dont exist on DB
            if Test_detglacc_delete_error == 'Y':
                messages.error(req, ' Input Delete records that dont exist in DB : ' + str(
                    Test_Delete_Err_Count_detglacc))

            # Display error message for empty file
            if Test_File_Count_detglacc == 0:
                messages.error(req, ' Empty File : Please correct and try again ')


        elif Test_mode != 'on':

            detglacc_line_no = 0
            detglacc_inserted_cnt = 0
            detglacc_updated_cnt = 0
            detglacc_deleted_cnt = 0
            detglacc_DB_count = 0
            detglacc_delete_Err_Count = 0
            detglacc_delete_error = ''
            detglacc_error_flag = ''
            Data_saved = ''

            for column in csv.reader(detglacc, delimiter=',', quotechar='"'):
                detglacc_line_no = detglacc_line_no + 1
                print("Spend Limit  Extract Line Number:" + str(detglacc_line_no))

                del_ind_field = column[5]

                # Check if the Currency code in the Det Gl Acc Input file has an entry in the Country table.

                if not (Currency.objects.filter(currency_id=column[7]).exists()):
                    Test_detglacc_errmsg_currency = 'Parent Record Not Found on Currency table'
                    messages.error(req,
                                   Test_detglacc_errmsg_currency + ' @Line Number : ' + str(detglacc_line_no))
                    detglacc_error_flag = 'Y'

                # Check if the Language ID in the detglacc Input file has an entry in the UnspscCategories table.

                if not (UnspscCategories.objects.filter(prod_cat_id=column[8]).exists()):
                    Test_detglacc_errmsg_prodcat = 'Parent Record Not Found on Product Category table'
                    messages.error(req,
                                   Test_detglacc_errmsg_prodcat + ' @Line Number : ' + str(detglacc_line_no))
                    detglacc_error_flag = 'Y'

                # Check if the AccountAssignmentCategory in the detglacc Input file has an entry in the AccountAssignmentCategory table.

                if not (AccountAssignmentCategory.objects.filter(account_assign_cat=column[6]).exists()):
                    Test_detglacc_errmsg_accasscat = 'Parent Record Not Found on Acccount Assignment Category table'
                    messages.error(req, Test_detglacc_errmsg_accasscat + ' @Line Number : ' + str(
                        detglacc_line_no))
                    detglacc_error_flag = 'Y'

                # Check if the Company id in the detglacc Input file has an entry in the OrgCompanies table.

                if not (OrgCompanies.objects.filter(company_id=column[4]).exists()):
                    Test_detglacc_errmsg_accasscat = 'Parent Record Not Found on OrgCompanies table'
                    messages.error(req, Test_detglacc_errmsg_accasscat + ' @Line Number : ' + str(
                        detglacc_line_no))
                    detglacc_error_flag = 'Y'

                # If any Parent table does not have an entry for value in detglacc file , Raise an Error
                if detglacc_error_flag != '':
                    continue

                # If the Deletion indicator in the file = "0" and record does not exist on the DB : INSERT DB

                if (del_ind_field == '0') and (
                not (DetermineGLAccount.objects.filter(gl_acc_num=column[2], client=client).exists())):
                    _, created = DetermineGLAccount.objects.get_or_create(
                        det_gl_acc_guid=guid_generator(),
                        item_from_value=column[0],
                        item_to_value=column[1],
                        gl_acc_num=column[2],
                        default=column[3],
                        company_id=OrgCompanies.objects.get(company_id=column[4]),
                        del_ind=column[5],
                        account_assign_cat=AccountAssignmentCategory.objects.get(account_assign_cat=column[6]),
                        currency_id=Currency.objects.get(currency_id=column[7]),
                        prod_cat_id=UnspscCategories.objects.get(prod_cat_id=column[8]),
                        client=OrgClients.objects.get(client=client)
                    )
                    detglacc_inserted_cnt = detglacc_inserted_cnt + 1
                    Data_saved = 'Y'

                # If the Deletion indicator in the file = "0" and record  exist on the DB : Update DB

                elif (del_ind_field == '0') and (
                DetermineGLAccount.objects.filter(gl_acc_num=column[2], client=client).exists()):
                    queryset_upd = DetermineGLAccount.objects.filter(gl_acc_num=column[2], client=client)
                    DetermineGLAccount.objects.filter(gl_acc_num=column[2], client=client).update(
                        item_from_value=column[0],
                        item_to_value=column[1],
                        gl_acc_num=column[2],
                        default=column[3],
                        company_id=OrgCompanies.objects.get(company_id=column[4]),
                        del_ind=column[5],
                        account_assign_cat=AccountAssignmentCategory.objects.get(account_assign_cat=column[6]),
                        currency_id=Currency.objects.get(currency_id=column[7]),
                        prod_cat_id=UnspscCategories.objects.get(prod_cat_id=column[8]),
                    )

                    detglacc_updated_cnt = detglacc_updated_cnt + 1
                    Data_saved = 'Y'

                # If the Deletion indicator in the file = "1" and record  exist on the DB : Soft Delete(del_ind =0) DB

                if (del_ind_field == '1') and (
                DetermineGLAccount.objects.filter(gl_acc_num=column[2], client=client).exists()):
                    queryset_del = DetermineGLAccount.objects.filter(gl_acc_num=column[2], client=client)
                    for test in queryset_del:
                        if test.del_ind == False:
                            DetermineGLAccount.objects.filter(gl_acc_num=column[2], client=client).update(del_ind=1)
                            detglacc_deleted_cnt = detglacc_deleted_cnt + 1
                            Data_saved = 'Y'

                # If the Deletion indicator in the file = "1" and record  does not exist on the DB : Error message

                elif (del_ind_field == '1') and (
                not (DetermineGLAccount.objects.filter(gl_acc_num=column[2], client=client).exists())):
                    detglacc_delete_error = 'Y'
                    detglacc_delete_Err_Count = detglacc_delete_Err_Count + 1

            # Display insert /updated count in the display
            detglacc_DB_count = DetermineGLAccount.objects.filter(del_ind=False).count()

            messages.info(req, 'Database Upload Results  :')
            messages.info(req, '-------------------------------')

            # Display the number of Active records in DB
            messages.success(req, ' Number of Active Records in Database    : ' + str(detglacc_DB_count))
            # Display the number of records Inserted
            messages.success(req, ' Records Inserted      : ' + str(detglacc_inserted_cnt))
            # Display the number of records Updated
            messages.success(req, ' Records Updated       : ' + str(detglacc_updated_cnt))
            # Display the number of records Deleted
            messages.success(req, ' Records Deleted       : ' + str(detglacc_deleted_cnt))

            # Display message for empty file
            if detglacc_line_no == 0:
                messages.error(req, ' Empty File : Please correct and try again ')
                Data_saved = ''

            # Display error message if delete record doesnt exist on DB
            if detglacc_delete_error != '':
                messages.error(req, ' Input Delete records that dont exist in DB : ' + str(detglacc_delete_Err_Count))

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
        print(e)
        messages.error(req, 'Error : ' + str(e))
