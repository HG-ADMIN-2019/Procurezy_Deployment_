"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    upload_user.py

Usage:
    Uploads the users data
Author:
    Soni Vydyula-  MEP-133
"""

import csv
from datetime import datetime
from django.contrib.auth.hashers import make_password
from eProc_Basic.Utilities.functions.get_db_query import getClients
from django.contrib import messages

from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.messages.messages import *
from eProc_Configuration.models import Currency, Languages, TimeZone, OrgClients
from eProc_Registration.models import UserData


def upload_user(req, User_Data, Test_mode):
    """
    on uploading of User Info csv file
    1. GET User Info file and store its respective field values into MUM_USER_INFO db table
    :param req: UI request
    :param Address: attached csv file data
    :param Test_mode : Diagnostics
    :return: return true on success, return false on failure

    """
    global errmsg
    DB_count = 0
    Insert_Count = 0
    Update_Count = 0
    Delete_Count = 0
    File_Count = 0
    Delete_Err_Count = 0
    Duplicate_Count = 0
    delete_error = ''
    number_list = []
    Data_saved = ''
    error_flag = ''
    try:

        client = getClients(req)

        for column in csv.reader(User_Data, delimiter=',', quotechar='"'):

            File_Count = File_Count + 1
            del_ind_field = column[21]

            # Check if the country code in the Address Input file has an entry in the Country table.

            if not (Currency.objects.filter(currency_id=column[23]).exists()):
                error_msg = get_message_desc(MSG091)[1]
                # msgid = 'MSG091'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg
                errmsg = error_msg
                # errmsg = MSG091
                messages.error(req,
                               errmsg + ' @Line Number : ' + str(File_Count))
                Test_Userinf_error_flag = 'Y'
                # Userinf_errmsg_currency = 'Parent Record Not Found on Country table'

            # Check if the Language ID in the Address Input file has an entry in the Languages table.

            if not (Languages.objects.filter(language_id=column[24]).exists()):
                error_msg = get_message_desc(MSG092)[1]
                # msgid = 'MSG092'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg
                errmsg = error_msg
                # errmsg = MSG092
                messages.error(req,
                               errmsg + ' @Line Number : ' + str(File_Count))
                error_flag = 'Y'
                # Userinf_errmsg_Language = 'Parent Record Not Found on Addresss table'

            # Check if the Timezone in the Address Input file has an entry in the TimeZone table.

            if not (TimeZone.objects.filter(time_zone=column[26]).exists()):
                error_msg = get_message_desc(MSG093)[1]
                # msgid = 'MSG093'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg
                errmsg = error_msg
                # errmsg = MSG093
                messages.error(req,
                               errmsg + ' @Line Number : ' + str(File_Count))
                error_flag = 'Y'

            # If any Parent table does not have an entry for value in Address file , Raise an Error
            if error_flag != '':
                continue

            # If the Test Mode check box is checked then run diagnostics.
            if Test_mode == 'on':

                DB_count = UserData.objects.filter(del_ind=False).count()

                # Read thru the file record by record , Assign column based on comma delimter

                # If the Input file Deletion indicator is "0" (Insert\Update record) and Address\Client key  does not exist in the Address table

                if (del_ind_field == '0') and (
                        not (UserData.objects.filter(username=column[1], client=client).exists())):
                    if column[1] in number_list:
                        Duplicate_Count = Duplicate_Count + 1
                        error_msg = get_message_desc(MSG094)[1]
                        # msgid = 'MSG094'
                        # error_msg = get_msg_desc(msgid)
                        # msg = error_msg['message_desc'][0]
                        # error_msg = msg
                        errmsg = error_msg
                    else:
                        Insert_Count = Insert_Count + 1

                # If the Input file Deletion indicator is "0" (Insert\Update record) and Address\Client key  exist in the Address table

                # Check if the record on table needs to be updated.
                if (del_ind_field == '0') and (UserData.objects.filter(username=column[1], client=client).exists()):
                    queryset_test_upd = UserData.objects.filter(username=column[1], client=client)
                    for test in queryset_test_upd:

                        if (test.first_name != column[3] or test.last_name != column[4] or test.email != column[5]
                                or test.phone_num != column[6] or test.password != column[7] or test.language_id !=
                                column[24]
                                or test.time_zone != column[26] or test.date_joined != column[8] or test.first_login !=
                                column[9]
                                or test.last_login != column[10] or test.is_active != column[11] or test.is_superuser !=
                                column[12]
                                or test.is_staff != column[13] or test.date_format != column[14] or test.employee_id !=
                                column[15]
                                or test.decimal_notation != column[16] or test.currency_id != column[
                                    22] or test.del_ind != column[17]
                                or test.user_type != column[18] or test.login_attempts != column[
                                    19] or test.user_locked != column[20]
                                or test.pwd_locked != column[21] or test.sso_user != column[22] or test.object_id !=
                                column[23]):

                            Update_Count = Update_Count + 1

                        # if the record on table is same as input record. increment the Duplicates count
                        else:

                            Duplicate_Count = Duplicate_Count + 1
                            error_msg = get_message_desc(MSG094)[1]
                            # msgid = 'MSG094'
                            # error_msg = get_msg_desc(msgid)
                            # msg = error_msg['message_desc'][0]
                            # error_msg = msg
                            errmsg = error_msg

                # If the Input file Deletion indicator is "1" (Delete record) and Address\Client key  exist in the Address table

                if (del_ind_field == '1') and (UserData.objects.filter(username=column[1], client=client).exists()):
                    queryset_test_del = UserData.objects.filter(username=column[1], client=client)

                    # If the Deletion indicator is set to False (active record) , increment Delete counts
                    for test in queryset_test_del:
                        if test.del_ind == False:
                            Delete_Count = Delete_Count + 1

                # If the Input file Deletion indicator is "1" (Delete record) and Address\Client key  does not exist in the Address table.
                # Raise delete error

                if (del_ind_field == '1') and (
                        not (UserData.objects.filter(username=column[1], client=client).exists())):
                    delete_error = 'Y'
                    Delete_Err_Count = Delete_Err_Count + 1

                # Append the processed record to the array list , for validation of next record.
                number_list.append(column[1])

            # If the Test Mode check box is Un-checked , Do File processing.

            if Test_mode != 'on':

                # Read thru the file record by record , Assign column based on comma delimter

                Date_Initial = datetime(1000, 1, 1, 00, 00, 00, 000000)

                # file_first_login
                # file_date_joined
                # file_last_login

                if column[7] == 'NULL':
                    column[7] = Date_Initial
                if column[8] == 'NULL':
                    column[8] = Date_Initial
                if column[9] == 'NULL':
                    column[9] = Date_Initial
                if column[13] == 'NULL':
                    column[13] = Date_Initial
                if column[5] == 'NULL':
                    column[5] = 0

                # If the Input file Deletion indicator is "0" (Insert\Update record) and Address\Client key  does not exist in the Address table

                if (del_ind_field == '0') and (
                        not (UserData.objects.filter(username=column[0], client=client)).exists()):
                    password = make_password(column[6])
                    # get Address data from attached file and store it to MUM_USER_INFO db table
                    _, created = UserData.objects.get_or_create(
                        username=column[1],
                        form_of_address=column[2],
                        first_name=column[3],
                        last_name=column[4],
                        email=column[0],
                        phone_num=column[5],
                        password=password,
                        language_id=Languages.objects.get(language_id=column[24]),
                        time_zone=TimeZone.objects.get(time_zone=column[26]),
                        date_joined=column[7],
                        first_login=column[8],
                        last_login=column[9],
                        is_active=column[10],
                        is_superuser=column[11],
                        is_staff=column[12],
                        date_format=column[13],
                        employee_id=column[14],
                        decimal_notation=column[15],
                        currency_id=Currency.objects.get(currency_id=column[23]),
                        del_ind=column[21],
                        user_type=column[16],
                        login_attempts=column[17],
                        user_locked=column[18],
                        pwd_locked=column[19],
                        sso_user=column[20],
                        # object_id=column[25],
                        client=OrgClients.objects.get(client=client)
                    )

                    Insert_Count = Insert_Count + 1
                    Data_saved = 'Y'

                # If the Input file Deletion indicator is "0" (Insert\Update record) and Address\Client key  exist in the Address table

                if (del_ind_field == '0') and (UserData.objects.filter(username=column[0], client=client).exists()):

                    queryset_test_upd = UserData.objects.filter(username=column[0], client=client)

                    for test in queryset_test_upd:

                        if (test.first_name != column[3] or test.last_name != column[4] or test.email != column[5]
                                or test.phone_num != column[6] or test.password != column[7] or test.language_id !=
                                column[24]
                                or test.time_zone != column[26] or test.date_joined != column[8] or test.first_login !=
                                column[9]
                                or test.last_login != column[10] or test.is_active != column[11] or test.is_superuser !=
                                column[12]
                                or test.is_staff != column[13] or test.date_format != column[14] or test.employee_id !=
                                column[15]
                                or test.decimal_notation != column[16] or test.currency_id != column[
                                    22] or test.del_ind != column[17]
                                or test.user_type != column[18] or test.login_attempts != column[
                                    19] or test.user_locked != column[20]
                                or test.pwd_locked != column[21] or test.sso_user != column[22] or test.object_id !=
                                column[23]):

                            UserData.objects.filter(
                                username=column[1],
                                form_of_address=column[2],
                                first_name=column[3],
                                last_name=column[4],
                                email=column[0],
                                phone_num=column[5],
                                password=column[6],
                                language_id=Languages.objects.get(language_id=column[24]),
                                time_zone=TimeZone.objects.get(time_zone=column[26]),
                                date_joined=column[7],
                                first_login=column[8],
                                last_login=column[9],
                                is_active=column[10],
                                is_superuser=column[11],
                                is_staff=column[12],
                                date_format=column[13],
                                employee_id=column[14],
                                decimal_notation=column[15],
                                currency_id=Currency.objects.get(currency_id=column[23]),
                                del_ind=column[21],
                                user_type=column[16],
                                login_attempts=column[17],
                                user_locked=column[18],
                                pwd_locked=column[19],
                                sso_user=column[20],
                                object_id=column[25],
                                client=OrgClients.objects.get(client=client)).update()

                            Update_Count = Update_Count + 1
                            Data_saved = 'Y'

                        else:

                            Duplicate_Count = Duplicate_Count + 1
                            error_msg = get_message_desc(MSG094)[1]
                            # msgid = 'MSG094'
                            # error_msg = get_msg_desc(msgid)
                            # msg = error_msg['message_desc'][0]
                            # error_msg = msg
                            errmsg_duplicate = error_msg
                            error_flag = 'Y'

                # If the Input file Deletion indicator is "1" (Delete record) and Address\Client key  exist in the Address table

                if (del_ind_field == '1') and (UserData.objects.filter(username=column[1], client=client).exists()):
                    queryset_del = UserData.objects.filter(username=column[1], client=client)
                    for test in queryset_del:
                        if test.del_ind == False:
                            UserData.objects.filter(username=column[1], client=client).update(del_ind=1)
                            Delete_Count = Delete_Count + 1
                            Data_saved = 'Y'

                # If the Input file Deletion indicator is "1" (Delete record) and Address\Client key  does not exist in the Address table.
                # Raise delete error

                if (del_ind_field == '1') and (
                        not (UserData.objects.filter(username=column[1], client=client).exists())):
                    delete_error = 'Y'
                    Delete_Err_Count = Delete_Err_Count + 1

            # Messages Summarising of processing of input file.

            Addr_DB_count = UserData.objects.filter(del_ind=0).count()

        messages.info(req, 'Database Upload Results  :')
        messages.info(req, '-------------------------------')

        messages.success(req, ' Number of Records in Database    : ' + str(DB_count))
        messages.success(req, ' Records Inserted      : ' + str(Insert_Count))
        messages.success(req, ' Records Updated       : ' + str(Update_Count))
        messages.success(req, ' Records Deleted       : ' + str(Delete_Count))
        messages.success(req, ' No change Records       : ' + str(Duplicate_Count))

        if File_Count == 0:
            messages.error(req, ' Empty File : Please correct and try again ')
            Data_saved = ''
        if delete_error != '':
            messages.error(req,
                           ' Input Delete records that dont exist in DB : ' + str(Delete_Err_Count))

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
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            messages.success(req, error_msg)
            # messages.success(req, MSG037)


    except Exception as e:
        print(e)
        messages.error(req, 'Error : ' + str(e))
