import csv
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.models import *
from eProc_Configuration.models import OrgClients, OrgAddressMap

from django.contrib import messages
from eProc_Basic.Utilities.messages.messages import *


# upload Address Map csv data file into MMD_ADDRESS_MAP db table - Shankar - SP12-06
def upload_addressmap(req, addressmap, Test_mode):
    """
    on uploading of MMD_ADDRESS_MAP  csv file
    1. GET Address Map csv file and store its respective field values into MMD_ADDRESS_MAP db table
    :param req: UI request
    :param addressmap: attached csv file data
    :param Test_mode : Diagnostics
    :return: return true on success, return false on failure
    """

    try:

        client = getClients(req)
        # If the Test Mode check box is checked then run diagnostics.

        if Test_mode == 'on':

            # Diagnostics mode variables
            Test_DB_count_addressmap = 0
            Test_Insert_Count_addressmap = 0
            Test_Update_Count_addressmap = 0
            Test_Delete_Count_addressmap = 0
            Test_File_Count_addressmap = 0
            Test_Delete_Err_Count_addressmap = 0
            Test_Duplicate_Count_addressmap = 0
            Test_addressmap_delete_error = ''
            Test_addressmap_number_list = []

            Data_saved = ''

            Test_DB_count_addressmap = OrgAddressMap.objects.filter(del_ind=False).count()

            # Read thru the file record by record , Assign column based on comma delimter

            for column in csv.reader(addressmap, delimiter=',', quotechar='"'):

                Test_File_Count_addressmap = Test_File_Count_addressmap + 1
                del_ind_field = column[2]

                print("Address Map Extract Line Number:" + str(Test_File_Count_addressmap))

                # If the Input file Deletion indicator is "0" (Insert\Update record)

                if (del_ind_field == '0') and (
                OrgAddressMap.objects.filter(address_number=column[1], client=client).exists()):
                    queryset_test_upd = OrgAddressMap.objects.filter(address_number=column[0], client=client)
                    for test in queryset_test_upd:
                        if test.address_type != column[0]:
                            Test_Update_Count_addressmap = Test_Update_Count_addressmap + 1
                        else:
                            Test_Duplicate_Count_addressmap = Test_Duplicate_Count_addressmap + 1

                # If the Input file Deletion indicator is "0" (Insert\Update record)
                elif (del_ind_field == '0') and (
                        not (OrgAddressMap.objects.filter(address_number=column[1], client=client).exists())):
                    if column[1] in Test_addressmap_number_list:
                        Test_Duplicate_Count_addressmap = Test_Duplicate_Count_addressmap + 1
                        error_msg = get_message_desc(MSG094)[1]
                        # msgid = 'MSG094'
                        # error_msg = get_msg_desc(msgid)
                        # msg = error_msg['message_desc'][0]
                        # error_msg = msg
                        Test_addressmap_errmsg_duplicate = error_msg
                    # Else the record is a valid Insert record update insert count
                    else:
                        Test_Insert_Count_addressmap = Test_Insert_Count_addressmap + 1

                # Check  If the Input file Deletion indicator is "1" (Delete record) and if record  exists
                # Check if the record is active on DB.

                if (del_ind_field == '1') and (
                OrgAddressMap.objects.filter(address_number=column[1], client=client).exists()):
                    queryset_test_del = OrgAddressMap.objects.filter(address_number=column[1], client=client)
                    for test in queryset_test_del:
                        if test.del_ind == False:
                            Test_Delete_Count_addressmap = Test_Delete_Count_addressmap + 1

                # Check  If the Input file Deletion indicator is "1" (Delete record) and if record does not exists
                # report as invalid record.

                elif (del_ind_field == '1') and (
                        not (OrgAddressMap.objects.filter(address_number=column[1], client=client).exists())):
                    Test_addressmap_delete_error = 'Y'
                    Test_Delete_Err_Count_addressmap = Test_Delete_Err_Count_addressmap + 1

                # Append the input key to the Array list for checking the next reocrds for dups.

                Test_addressmap_number_list.append(column[1])

            # Display insert /updated count in the display

            # Number of active records on the Database.
            messages.info(req, 'Test Mode Diagnostics:')
            messages.info(req, '-----------------------------')

            # Number of active records on the Database.
            messages.success(req, ' Number of Records in Database    : ' + str(Test_DB_count_addressmap))
            # Number of records in the Input file.
            messages.success(req, ' Number of Records in Input file  : ' + str(Test_File_Count_addressmap))
            # Total records that need to be inserted.
            messages.success(req, ' Records to be Inserted           : ' + str(Test_Insert_Count_addressmap))
            # Total records that need to be Updated.
            messages.success(req, ' Records to be Updated            : ' + str(Test_Update_Count_addressmap))
            # Total records that need to be Deleted.
            messages.success(req, ' Records to be Deleted            : ' + str(Test_Delete_Count_addressmap))
            # Total records that are duplicate in the input file
            messages.error(req, ' Duplicate Records                : ' + str(Test_Duplicate_Count_addressmap))

            # Display the number of delete records that dont exist on DB
            if Test_addressmap_delete_error == 'Y':
                messages.error(req, ' Input Delete records that dont exist in DB : ' + str(
                    Test_Delete_Err_Count_addressmap))

            # Display error message for empty file
            if Test_File_Count_addressmap == 0:
                messages.error(req, ' Empty File : Please correct and try again ')


        elif Test_mode != 'on':

            addressmap_line_no = 0
            addressmap_inserted_cnt = 0
            addressmap_updated_cnt = 0
            addressmap_deleted_cnt = 0
            addressmap_DB_count = 0
            addressmap_delete_Err_Count = 0
            addressmap_delete_error = ''
            Data_saved = ''

            for column in csv.reader(addressmap, delimiter=',', quotechar='"'):
                addressmap_line_no = addressmap_line_no + 1
                print("Address Map Extract Line Number:" + str(addressmap_line_no))

                del_ind_field = column[2]

                # If the Deletion indicator in the file = "0" and record does not exist on the DB : INSERT DB

                if (del_ind_field == '0') and (
                not (OrgAddressMap.objects.filter(address_number=column[1], client=client).exists())):
                    _, created = OrgAddressMap.objects.get_or_create(address_type=column[0],
                                                                     address_guid=guid_generator(),
                                                                     address_number=column[1],
                                                                     del_ind=column[2],
                                                                     client=OrgClients.objects.get(client=client)
                                                                     )

                    addressmap_inserted_cnt = addressmap_inserted_cnt + 1
                    Data_saved = 'Y'

                # If the Deletion indicator in the file = "0" and record  exist on the DB : Update DB

                elif (del_ind_field == '0') and (
                OrgAddressMap.objects.filter(address_number=column[1], client=client).exists()):
                    queryset_upd = OrgAddressMap.objects.filter(address_number=column[1], client=client)
                    for test in queryset_upd:
                        OrgAddressMap.objects.filter(address_number=column[1], client=client).update(
                            address_type=column[0],
                            del_ind=column[2]
                        )

                        addressmap_updated_cnt = addressmap_updated_cnt + 1
                        Data_saved = 'Y'

                # If the Deletion indicator in the file = "1" and record  exist on the DB : Soft Delete(del_ind =0) DB

                if (del_ind_field == '1') and (
                OrgAddressMap.objects.filter(address_number=column[1], client=client).exists()):
                    queryset_del = OrgAddressMap.objects.filter(address_number=column[1], client=client)
                    for test in queryset_del:
                        if test.del_ind == False:
                            OrgAddressMap.objects.filter(address_number=column[1], client=client).update(del_ind=1)
                            addressmap_deleted_cnt = addressmap_deleted_cnt + 1
                            Data_saved = 'Y'

                # If the Deletion indicator in the file = "1" and record  does not exist on the DB : Error message

                elif (del_ind_field == '1') and (
                not (OrgAddressMap.objects.filter(address_number=column[1], client=client).exists())):
                    addressmap_delete_error = 'Y'
                    addressmap_delete_Err_Count = addressmap_delete_Err_Count + 1

            # Display insert /updated count in the display
            addressmap_DB_count = OrgAddressMap.objects.filter(del_ind=False).count()

            messages.info(req, 'Database Upload Results  :')
            messages.info(req, '-------------------------------')

            # Display the number of Active records in DB
            messages.success(req, ' Number of Active Records in Database    : ' + str(addressmap_DB_count))
            # Display the number of records Inserted
            messages.success(req, ' Records Inserted      : ' + str(addressmap_inserted_cnt))
            # Display the number of records Updated
            messages.success(req, ' Records Updated       : ' + str(addressmap_updated_cnt))
            # Display the number of records Deleted
            messages.success(req, ' Records Deleted       : ' + str(addressmap_deleted_cnt))

            # Display message for empty file
            if addressmap_line_no == 0:
                messages.error(req, ' Empty File : Please correct and try again ')
                Data_saved = ''

            # Display error message if delete record doesnt exist on DB
            if addressmap_delete_error != '':
                messages.error(req, ' Input Delete records that dont exist in DB : ' + str(addressmap_delete_Err_Count))

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
        print(e)
        messages.error(req, 'Error : ' + str(e))
