"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    upload_supplier.py

Usage:
    Uploads the supplier data
Author:
    Soni Vydyula- MEP-189
"""

import csv
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Configuration.models import Currency, Languages, Country, OrgClients, SupplierMaster
from django.contrib import messages
from eProc_Basic.Utilities.messages.messages import *
from eProc_Org_Model.models import OrgModel


def upload_suppliermaster(req, suppliermaster, Test_mode):
    """
    on uploading of MMD_DET_GL_ACC  csv file
    1. GET Supplier Master csv file and store its respective field values into MMD_DET_GL_ACC db table
    :param req: UI request
    :param suppliermaster: attached csv file data
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

        for column in csv.reader(suppliermaster, delimiter=',', quotechar='"'):
            error_flag = ''
            File_Count = File_Count + 1
            del_ind_field = column[25]

            # Check if the country code in the Address Input file has an entry in the Country table.
            error_msg = get_message_desc(MSG091)[1]
            # msgid = 'MSG091'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            if not (Currency.objects.filter(currency_id=column[28]).exists()):

                errmsg = error_msg
                # errmsg = MSG091
                messages.error(req,
                               errmsg + ' @Line Number : ' + str(File_Count))
                error_flag = 'Y'
                print("Supplier Master  Extract Line Number:" + str(File_Count))
                error_msg = get_message_desc(MSG091)[1]
                # msgid = 'MSG091'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg

            if not (Country.objects.filter(country_code=column[27]).exists()):

                errmsg = error_msg
                # errmsg = MSG091

                error_flag = 'Y'
                # suppliermaster_errmsg_country = 'Parent Record Not Found on Country table'
                messages.error(req, errmsg + ' @Line Number : ' + str(
                    File_Count))
                error_msg = get_message_desc(MSG092)[1]
                # msgid = 'MSG092'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg

            if not (Languages.objects.filter(language_id=column[29]).exists()):
                error_flag = 'Y'

                errmsg = error_msg
                # errmsg = MSG092
                # suppliermaster_errmsg_language = 'Parent Record Not Found on Languages table'
                messages.error(req, errmsg + ' @Line Number : ' + str(
                    File_Count))

                # if SupplierMaster.objects.filter(supplier_id=column[0], client=client).exists():
                #     errmsg_duplicate = 'Duplicate record exists on Supplier ID and Client.'
                #     messages.error(req, errmsg_duplicate + ' @Line Number : ' + str(
                #         File_Count))
                #
                #     error_flag = 'Y'
                #
                # if SupplierMaster.objects.filter(email=column[10], client=client).exists():
                #     errmsg_duplicate = 'Duplicate record exists on Email ID and Client.'
                #     messages.error(req, errmsg_duplicate + ' @Line Number : ' + str(
                #         File_Count))

                error_flag = 'Y'

            if error_flag != '':
                continue

            # If the Test Mode check box is checked then run diagnostics.
            if Test_mode == 'on':

                DB_count = SupplierMaster.objects.filter(del_ind=False).count()

                # Read thru the file record by record , Assign column based on comma delimter

                # If the Input file Deletion indicator is "0" (Insert\Update record) and Address\Client key  does not exist in the Address table

                if (del_ind_field == '0') and (
                        SupplierMaster.objects.filter(supplier_id=column[0], client=client).exists()):
                    queryset_test_upd = SupplierMaster.objects.filter(supplier_id=column[0], client=client)
                    for test in queryset_test_upd:

                        if (test.supp_type != column[1] or test.name1 != column[2] or test.name2 != column[3] or
                                test.city != column[4] or test.postal_code != column[5] or test.street != column[6] or
                                test.landline != column[7] or test.mobile_num != column[8] or test.fax != column[9] or
                                test.email != column[10] or test.email1 != column[11] or test.email2 != column[12]
                                or test.email3 != column[13] or test.email4 != column[14] or test.email5 != column[
                                    15] or
                                test.output_medium != column[16] or test.search_term1 != column[
                                    17] or test.search_term2 !=
                                column[18] or
                                test.duns_number != column[19] or test.block_date != column[20] or test.block != column[
                                    21]
                                or test.working_days != column[22] or
                                test.is_active != column[23] or test.del_ind != column[
                                    25] or test.registration_number != column[24] or
                                test.currency_id != column[28] or test.country_code != column[27] or test.language_id !=
                                column[29]):

                            Update_Count = Update_Count + 1
                        else:
                            Duplicate_Count = Duplicate_Count + 1

                # If the Input file Deletion indicator is "0" (Insert\Update record) and Address\Client key  exist in the Address table

                # Check if the record on table needs to be updated.
                elif (del_ind_field == '0') and (
                        not (SupplierMaster.objects.filter(supplier_id=column[0], client=client).exists())):
                    if column[0] in number_list:
                        Duplicate_Count = Duplicate_Count + 1
                        error_msg = get_message_desc(MSG094)[1]
                        # msgid = 'MSG094'
                        # error_msg = get_msg_desc(msgid)
                        # msg = error_msg['message_desc'][0]
                        # error_msg = msg
                        errmsg = error_msg
                    # Else the record is a valid Insert record update insert count
                    else:
                        Insert_Count = Insert_Count + 1

                # If the Input file Deletion indicator is "1" (Delete record) and Address\Client key  exist in the Address table

                if (del_ind_field == '1') and (
                        SupplierMaster.objects.filter(supplier_id=column[0], client=client).exists()):
                    queryset_test_del = SupplierMaster.objects.filter(supplier_id=column[0], client=client)
                    for test in queryset_test_del:
                        if test.del_ind == False:
                            Delete_Count = Delete_Count + 1

                # If the Input file Deletion indicator is "1" (Delete record) and Address\Client key  does not exist in the Address table.
                # Raise delete error

                elif (del_ind_field == '1') and (
                        not (SupplierMaster.objects.filter(supplier_id=column[0], client=client).exists())):
                    delete_error = 'Y'
                    Delete_Err_Count = Delete_Err_Count + 1

                # Append the processed record to the array list , for validation of next record.
                number_list.append(column[1])

            # If the Test Mode check box is Un-checked , Do File processing.

            if Test_mode != 'on':

                if (del_ind_field == '0') and (
                        not (SupplierMaster.objects.filter(supplier_id=column[0], client=client).exists())):
                    _, created = SupplierMaster.objects.get_or_create(
                        supp_guid=guid_generator(),
                        supplier_id=column[0],
                        supp_type=column[1],
                        name1=column[2],
                        name2=column[3],
                        city=column[4],
                        postal_code=column[5],
                        street=column[6],
                        landline=column[7],
                        mobile_num=column[8],
                        fax=column[9],
                        email=column[10],
                        email1=column[11], email2=column[12], email3=column[13], email4=column[14], email5=column[15],
                        output_medium=column[16],
                        search_term1=column[17],
                        search_term2=column[18],
                        duns_number=column[19],
                        block_date=column[20],
                        block=column[21],
                        working_days=column[22],
                        is_active=column[23],
                        del_ind=column[25],
                        registration_number=column[24],
                        currency_id=Currency.objects.get(currency_id=column[28]),
                        client=OrgClients.objects.get(client=client),
                        country_code=Country.objects.get(
                            country_code=column[27]),
                        language_id=Languages.objects.get(
                            language_id=column[29]))

                    Insert_Count = Insert_Count + 1
                    Data_saved = 'Y'

                # If the Input file Deletion indicator is "0" (Insert\Update record) and Address\Client key  exist in the Address table

                elif (del_ind_field == '0') and (
                        SupplierMaster.objects.filter(supplier_id=column[0], client=client).exists()):
                    SupplierMaster.objects.filter(supplier_id=column[0], client=client).update(
                        supp_guid=guid_generator(),
                        supplier_id=column[0],
                        supp_type=column[1],
                        name1=column[2],
                        name2=column[3],
                        city=column[4],
                        postal_code=column[5],
                        street=column[6],
                        landline=column[7],
                        mobile_num=column[8],
                        fax=column[9],
                        email=column[10],
                        email1=column[11], email2=column[12], email3=column[13], email4=column[14], email5=column[15],
                        output_medium=column[16],
                        search_term1=column[17],
                        search_term2=column[18],
                        duns_number=column[19],
                        block_date=column[20],
                        block=column[21],
                        working_days=column[22],
                        is_active=column[23],
                        del_ind=column[25],
                        registration_number=column[24],
                        currency_id=Currency.objects.get(currency_id=column[28]),
                        client=OrgClients.objects.get(client=client),
                        country_code=Country.objects.get(
                            country_code=column[27]),
                        language_id=Languages.objects.get(
                            language_id=column[29])
                    )
                    Update_Count = Update_Count + 1
                    Data_saved = 'Y'

                    # If the Input file Deletion indicator is "1" (Delete record) and Address\Client key  exist in the Address table

                    if (del_ind_field == '1') and (
                            SupplierMaster.objects.filter(supplier_id=column[0], client=client).exists()):
                        queryset_del = SupplierMaster.objects.filter(supplier_id=column[0], client=client)
                        for test in queryset_del:
                            if not test.del_ind:
                                SupplierMaster.objects.filter(supplier_id=column[0], client=client).update(del_ind=1)
                                Delete_Count = Delete_Count + 1
                                Data_saved = 'Y'

                    # If the Deletion indicator in the file = "1" and record  does not exist on the DB : Error message

                    elif (del_ind_field == '1') and (
                            not (SupplierMaster.objects.filter(supplier_id=column[0], client=client).exists())):
                        delete_error = 'Y'
                        Delete_Err_Count = Delete_Err_Count + 1

                # Display insert /updated count in the display
                DB_count = SupplierMaster.objects.filter(del_ind=False).count()

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
            messages.success(req, error_msg)
            # messages.success(req, MSG037)


    except Exception as e:
        print(e)
        messages.error(req, 'Error : ' + str(e))


def upload_suppliermaster_new(req, suppliermaster, Test_mode):
    """
    on uploading of MMD_DET_GL_ACC  csv file
    1. GET Supplier Master csv file and store its respective field values into MMD_DET_GL_ACC db table
    :param req: UI request
    :param suppliermaster: attached csv file data
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
    check_messages = {}
    try:

        client = getClients(req)
        error_msg = get_message_desc(MSG091)[1]
        # msgid = 'MSG091'
        # error_msg = get_msg_desc(msgid)
        # msg = error_msg['message_desc'][0]
        # error_msg = msg
        for column in suppliermaster:
            error_flag = ''
            File_Count = File_Count + 1
            del_ind_field = column[29]

            # Check if the country code in the Address Input file has an entry in the Country table.

            if not (Currency.objects.filter(currency_id=column[32]).exists()):

                errmsg = error_msg
                # errmsg = MSG091

                messages.error(req,
                               errmsg + ' @Line Number : ' + str(File_Count))
                error_flag = 'Y'
                print("Supplier Master  Extract Line Number:" + str(File_Count))

            if not (Country.objects.filter(country_code=column[31]).exists()):

                errmsg = error_msg
                # errmsg = MSG091

                error_flag = 'Y'
                # suppliermaster_errmsg_country = 'Parent Record Not Found on Country table'
                messages.error(req, errmsg + ' @Line Number : ' + str(
                    File_Count))

            if not (Languages.objects.filter(language_id=column[33]).exists()):
                error_msg = get_message_desc(MSG092)[1]
                error_flag = 'Y'
                # msgid = 'MSG092'
                # error_msg = get_msg_desc(msgid)
                errmsg = error_msg
                # msg = error_msg['message_desc'][0]
                # error_msg = msg
                # errmsg = MSG092
                # suppliermaster_errmsg_language = 'Parent Record Not Found on Languages table'
                messages.error(req, errmsg + ' @Line Number : ' + str(
                    File_Count))

                # if SupplierMaster.objects.filter(supplier_id=column[0], client=client).exists():
                #     errmsg_duplicate = 'Duplicate record exists on Supplier ID and Client.'
                #     messages.error(req, errmsg_duplicate + ' @Line Number : ' + str(
                #         File_Count))
                #
                #     error_flag = 'Y'
                #
                # if SupplierMaster.objects.filter(email=column[10], client=client).exists():
                #     errmsg_duplicate = 'Duplicate record exists on Email ID and Client.'
                #     messages.error(req, errmsg_duplicate + ' @Line Number : ' + str(
                #         File_Count))

                error_flag = 'Y'

            if error_flag != '':
                continue

            # If the Test Mode check box is checked then run diagnostics.
            if Test_mode == 'on':

                DB_count = SupplierMaster.objects.filter(del_ind=False).count()

                # Read thru the file record by record , Assign column based on comma delimter

                # If the Input file Deletion indicator is "0" (Insert\Update record) and Address\Client key  does not exist in the Address table

                if (del_ind_field == '0') and (
                        SupplierMaster.objects.filter(supplier_id=column[0], client=client).exists()):
                    queryset_test_upd = SupplierMaster.objects.filter(supplier_id=column[0], client=client)
                    for test in queryset_test_upd:

                        if (test.supp_type != column[1] or test.name1 != column[2] or test.name2 != column[3] or
                                test.city != column[4] or test.postal_code != column[5] or test.street != column[6] or
                                test.landline != column[7] or test.mobile_num != column[8] or test.fax != column[9] or
                                test.email != column[10] or test.email1 != column[11] or test.email2 != column[12]
                                or test.email3 != column[13] or test.email4 != column[14] or test.email5 != column[
                                    15] or
                                test.output_medium != column[16] or test.search_term1 != column[
                                    17] or test.search_term2 !=
                                column[18] or
                                test.duns_number != column[19] or test.block_date != column[20] or test.block != column[
                                    21]
                                or test.working_days != column[22] or
                                test.is_active != column[23] or test.del_ind != column[
                                    29] or test.registration_number != column[24] or
                                test.currency_id != column[32] or test.country_code != column[31] or test.language_id !=
                                column[33]):

                            Update_Count = Update_Count + 1
                        else:
                            Duplicate_Count = Duplicate_Count + 1

                # If the Input file Deletion indicator is "0" (Insert\Update record) and Address\Client key  exist in
                # the Address table

                # Check if the record on table needs to be updated.
                elif (del_ind_field == '0') and (
                        not (SupplierMaster.objects.filter(supplier_id=column[0], client=client).exists())):
                    if column[0] in number_list:
                        Duplicate_Count = Duplicate_Count + 1
                        error_msg = get_message_desc(MSG094)[1]
                        # msgid = 'MSG094'
                        # error_msg = get_msg_desc(msgid)
                        # msg = error_msg['message_desc'][0]
                        # error_msg = msg
                        errmsg = error_msg
                    # Else the record is a valid Insert record update insert count
                    else:
                        Insert_Count = Insert_Count + 1

                # If the Input file Deletion indicator is "1" (Delete record) and Address\Client key  exist in the Address table

                if (del_ind_field == '1') and (
                        SupplierMaster.objects.filter(supplier_id=column[0], client=client).exists()):
                    queryset_test_del = SupplierMaster.objects.filter(supplier_id=column[0], client=client)
                    for test in queryset_test_del:
                        if test.del_ind == False:
                            Delete_Count = Delete_Count + 1

                # If the Input file Deletion indicator is "1" (Delete record) and Address\Client key  does not exist in the Address table.
                # Raise delete error

                elif (del_ind_field == '1') and (
                        not (SupplierMaster.objects.filter(supplier_id=column[0], client=client).exists())):
                    delete_error = 'Y'
                    Delete_Err_Count = Delete_Err_Count + 1

                # Append the processed record to the array list , for validation of next record.
                number_list.append(column[1])
                check_messages['db_count'] = DB_count
                check_messages['file_count'] = File_Count
                check_messages['duplicate_count'] = Duplicate_Count
                check_messages['insert_count'] = Insert_Count
                check_messages['update_count'] = Update_Count
                check_messages['delete_count'] = Delete_Count

            return check_messages
    except Exception as e:
        print(e)
        messages.error(req, 'Error : ' + str(e))
