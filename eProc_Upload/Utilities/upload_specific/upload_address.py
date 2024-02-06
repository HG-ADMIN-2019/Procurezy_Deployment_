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


# upload Address csv data file into MMD_ADDRESS db table - Shankar - SP11-13
from eProc_Configuration.models import Languages, Country, TimeZone, OrgClients, OrgAddress


def upload_address(req, Address ,Test_mode):
    """
    on uploading of Address  csv file
    1. GET Address csv file and store its respective field values into MMD_ADDRESS db table
    :param req: UI request
    :param Address: attached csv file data
    :param Test_mode : Diagnostics
    :return: return true on success, return false on failure
    """
    try:

        client = getClients(req)


        # If the Test Mode check box is checked then run diagnostics.
        if Test_mode == 'on':

            # Diagnostics mode variables
            Test_Address_errmsg_country = ''
            Test_Address_errmsg_Language = ''
            Test_Address_errmsg_timezone = ''
            Test_Address_errmsg_duplicate = ''
            Test_Address_error_flag = ''
            Test_Addr_DB_count = 0
            Test_Insert_Count_Addr = 0
            Test_Update_Count_Addr = 0
            Test_Delete_Count_Addr = 0
            Test_Duplicate_Count_Addr = 0
            Test_File_Count_Addr = 0
            Test_Delete_Err_Count_Addr = 0
            Test_Addr_delete_error = ''
            Test_Address_number_list = []

            Data_saved = ''
            Test_Addr_DB_count = OrgAddress.objects.filter ( del_ind=False ).count ()

            # Read thru the file record by record , Assign column based on comma delimter
            for column in csv.reader ( Address, delimiter=',', quotechar='"' ):

                Test_File_Count_Addr = Test_File_Count_Addr + 1
                del_ind_field = column[14]

                # Check if the country code in the Address Input file has an entry in the Country table.

                if not (Country.objects.filter ( country_code=column[15] ).exists ()):
                    error_msg = get_message_desc(MSG041)[1]
                    # msgid = 'MSG041'
                    # error_msg = get_msg_desc(msgid)
                    # msg = error_msg['message_desc'][0]
                    # error_msg = msg
                    # Test_Address_errmsg_country = MSG041
                    Test_Address_errmsg_country = error_msg
                    messages.error ( req, Test_Address_errmsg_country + ' @Line Number : ' + str ( Test_File_Count_Addr ) )
                    Test_Address_error_flag = 'Y'
                    # Address_errmsg_country = 'Parent Record Not Found on Country table'

                # Check if the Language ID in the Address Input file has an entry in the Languages table.

                if not (Languages.objects.filter ( language_id=column[16] ).exists ()):
                    error_msg = get_message_desc(MSG092)[1]
                    # msgid = 'MSG092'
                    # error_msg = get_msg_desc(msgid)
                    # msg = error_msg['message_desc'][0]
                    # error_msg = msg

                    # Test_Address_errmsg_Language = error_msg
                    Test_Address_errmsg_Language = error_msg
                    messages.error ( req, Test_Address_errmsg_Language + ' @Line Number : ' + str ( Test_File_Count_Addr ) )
                    Test_Address_error_flag = 'Y'
                    # Address_errmsg_Language = 'Parent Record Not Found on Addresss table'

                # Check if the Timezone in the Address Input file has an entry in the TimeZone table.

                if not (TimeZone.objects.filter ( time_zone=column[17] ).exists ()):
                    error_msg = get_message_desc(MSG093)[1]
                    # msgid = 'MSG093'
                    # error_msg = get_msg_desc(msgid)
                    # msg = error_msg['message_desc'][0]
                    # error_msg = msg
                    Test_Address_errmsg_timezone = error_msg
                    # Test_Address_errmsg_timezone = MSG093
                    messages.error(req, Test_Address_errmsg_timezone + ' @Line Number : ' + str ( Test_File_Count_Addr ) )
                    Test_Address_error_flag = 'Y'

                # If any Parent table does not have an entry for value in Address file , Raise an Error
                if Test_Address_error_flag != '':
                    continue

                # If the Input file Deletion indicator is "0" (Insert\Update record) and Address\Client key  does not exist in the Address table

                if (del_ind_field == '0') and (not (OrgAddress.objects.filter( address_number=column[0],client=client ).exists ())):
                    if column[0] in Test_Address_number_list:
                        Test_Duplicate_Count_Addr = Test_Duplicate_Count_Addr + 1
                        error_msg = get_message_desc(MSG094)[1]
                        # msgid = 'MSG094'
                        # error_msg = get_msg_desc(msgid)
                        # msg = error_msg['message_desc'][0]
                        # error_msg = msg
                        Test_Address_errmsg_duplicate = error_msg
                    else:
                        Test_Insert_Count_Addr = Test_Insert_Count_Addr + 1


                # If the Input file Deletion indicator is "0" (Insert\Update record) and Address\Client key  exist in the Address table

                # Check if the record on table needs to be updated.
                if (del_ind_field == '0') and (OrgAddress.objects.filter ( address_number=column[0] ,client=client ).exists ()):
                    queryset_test_upd = OrgAddress.objects.filter ( address_number=column[0],client=client )
                    for test in queryset_test_upd:

                        if ( test.title != column[1] or  test.name1 != column[2]
                            or   test.name2 != column[3]    or   test.street != column[4]  or   test.area != column[5]
                            or   test.landmark != column[6] or test.city != column[7]      or   test.postal_code != column[8]
                            or   test.region != column[9]  or test.mobile_number != column[10] or   test.telephone_number != column[11]
                            or   test.fax_number != column[12]  or   test.email != column[13] or test.del_ind !=column[14]   ):


                            Test_Update_Count_Addr = Test_Update_Count_Addr + 1

                # if the record on table is same as input record. increment the Duplicates count
                        else :

                            Test_Duplicate_Count_Addr = Test_Duplicate_Count_Addr + 1
                            error_msg = get_message_desc(MSG094)[1]
                            # msgid = 'MSG094'
                            # error_msg = get_msg_desc(msgid)
                            # msg = error_msg['message_desc'][0]
                            # error_msg = msg
                            Test_Address_errmsg_duplicate = error_msg


                # If the Input file Deletion indicator is "1" (Delete record) and Address\Client key  exist in the Address table

                if (del_ind_field == '1') and (OrgAddress.objects.filter ( address_number=column[0],client=client ).exists ()):
                    queryset_test_del = OrgAddress.objects.filter ( address_number=column[0],client=client )

                # If the Deletion indicator is set to False (active record) , increment Delete counts
                    for test in queryset_test_del:
                        if test.del_ind == False:
                            Test_Delete_Count_Addr = Test_Delete_Count_Addr + 1

                # If the Input file Deletion indicator is "1" (Delete record) and Address\Client key  does not exist in the Address table.
                # Raise delete error

                if (del_ind_field == '1') and (not (OrgAddress.objects.filter ( address_number=column[0],client=client ).exists ())):
                    Test_Addr_delete_error = 'Y'
                    Test_Delete_Err_Count_Addr = Test_Delete_Err_Count_Addr + 1

                # Append the processed record to the array list , for validation of next record.
                Test_Address_number_list.append ( column[0] )


            messages.info ( req, 'Test Mode Diagnostics:' )
            messages.info ( req, '----------------------------- ' )

            # Display insert /updated count in the display
            # Number of active records on the Database.
            messages.success ( req, ' Number of Records in Database    : ' + str ( Test_Addr_DB_count ) )
            # Number of records in the Input file.
            messages.success ( req, ' Number of Records in Input file  : ' + str ( Test_File_Count_Addr ) )
            # Total records that need to be inserted.
            messages.success ( req, ' Records to be Inserted           : ' + str ( Test_Insert_Count_Addr ) )
            # Total records that need to be Updated.
            messages.success ( req, ' Records to be Updated            : ' + str ( Test_Update_Count_Addr ) )
            # Total records that need to be Deleted.
            messages.success ( req, ' Records to be Deleted            : ' + str ( Test_Delete_Count_Addr ) )
            # Total records that are duplicate in the input file
            messages.error ( req, ' Duplicate Records                : ' + str ( Test_Duplicate_Count_Addr ) )


            # Display error message for delete records that dont exist in the DB
            if Test_Addr_delete_error != '':
                messages.error ( req,
                                 ' Input Delete records that dont exist in DB : ' + str ( Test_Delete_Err_Count_Addr ) )

            # Display error message for Empty input file
            if Test_File_Count_Addr == 0:
                messages.error ( req, ' Empty File : Please correct and try again ' )


        # If the Test Mode check box is Un-checked , Do File processing.

        if Test_mode != 'on':

            client = getClients ( req )
            Address_line_no = 0
            Address_inserted_cnt = 0
            Address_updated_cnt = 0
            Address_deleted_cnt = 0
            Address_duplicate_cnt = 0
            Addr_DB_count = 0
            Address_delete_Err_Count = 0
            Address_delete_error = ''

            Data_saved = ''

            # Read thru the file record by record , Assign column based on comma delimter

            for column in csv.reader ( Address, delimiter=',', quotechar='"' ):
                Address_line_no = Address_line_no + 1
                print ( "Address Extract Line Number:" + str ( Address_line_no ) )

                Address_errmsg_country = ''
                Address_errmsg_Language = ''
                Address_errmsg_timezone = ''
                Address_errmsg_duplicate = ''
                Address_error_flag = ''
                del_ind_field = column[14]
                Data_saved = ''

                # Check if the country code in the Address Input file has an entry in the Country table.

                if not (Country.objects.filter ( country_code=column[15] ).exists ()):
                    error_msg = get_message_desc(MSG041)[1]
                    # msgid = 'MSG041'
                    # error_msg = get_msg_desc(msgid)
                    # msg = error_msg['message_desc'][0]
                    # error_msg = msg
                    Address_errmsg_country = error_msg
                    # Address_errmsg_country = MSG041
                    messages.error ( req, Address_errmsg_country + ' @Line Number : ' + str ( Address_line_no ) )
                    Address_error_flag = 'Y'

                # Check if the Language ID in the Address Input file has an entry in the Languages table.

                if not (Languages.objects.filter ( language_id=column[16] ).exists ()):
                    error_msg = get_message_desc(MSG092)[1]
                    # msgid = 'MSG092'
                    # error_msg = get_msg_desc(msgid)
                    # msg = error_msg['message_desc'][0]
                    # error_msg = msg
                    Address_errmsg_Language = error_msg
                    # Address_errmsg_Language = MSG092
                    messages.error ( req, Address_errmsg_Language + ' @Line Number : ' + str ( Address_line_no ) )
                    Address_error_flag = 'Y'

               # Check if the Timezone in the Address Input file has an entry in the TimeZone table.

                if not (TimeZone.objects.filter ( time_zone=column[17] ).exists ()):
                    error_msg = get_message_desc(MSG093)[1]
                    # msgid = 'MSG093'
                    # error_msg = get_msg_desc(msgid)
                    # msg = error_msg['message_desc'][0]
                    # error_msg = msg
                    Address_errmsg_timezone = error_msg
                    # Address_errmsg_timezone = MSG093
                    messages.error ( req, Address_errmsg_timezone + ' @Line Number : ' + str ( Address_line_no ) )
                    Address_error_flag = 'Y'

                # If any Parent table does not have an entry for value in Address file , Raise an Error

                if Address_error_flag != '':
                    continue

                # If the Input file Deletion indicator is "0" (Insert\Update record) and Address\Client key  does not exist in the Address table

                if (del_ind_field == '0') and (not (OrgAddress.objects.filter ( address_number=column[0],client=client)).exists()):
                    # get Addresss data from attached file and store it to MMD_ADDRESS db table
                    _, created= OrgAddress.objects.get_or_create (
                        address_guid=guid_generator (),
                        # address_guid=column[0],
                        address_number=column[0],
                        title=column[1],
                        name1=column[2],
                        name2=column[3],
                        street=column[4],
                        area=column[5],
                        landmark=column[6],
                        city=column[7],
                        postal_code=column[8],
                        region=column[9],
                        mobile_number=column[10],
                        telephone_number=column[11],
                        fax_number=column[12],
                        email=column[13],
                        del_ind=column[14],
                        client=OrgClients.objects.get ( client=client ),
                        country_code=Country.objects.get (country_code=column[15] ),
                        language_id=Languages.objects.get (language_id=column[16] ),
                        time_zone=TimeZone.objects.get (time_zone=column[17] )
                    )

                    Address_inserted_cnt = Address_inserted_cnt + 1
                    Data_saved = 'Y'

                # If the Input file Deletion indicator is "0" (Insert\Update record) and Address\Client key  exist in the Address table

                if (del_ind_field == '0') and (OrgAddress.objects.filter ( address_number=column[0], client=client ).exists ()):

                    queryset_test_upd = OrgAddress.objects.filter ( address_number=column[0], client=client )

                    for test in queryset_test_upd:

                        if ( test.title != column[1] or  test.name1 != column[2]
                            or   test.name2 != column[3]    or   test.street != column[4]  or   test.area != column[5]
                            or   test.landmark != column[6] or test.city != column[7]      or   test.postal_code != column[8]
                            or   test.region != column[9]  or test.mobile_number != column[10] or   test.telephone_number != column[11]
                            or   test.fax_number != column[12]  or   test.email != column[13] or test.del_ind !=column[14]   ):

                                OrgAddress.objects.filter ( address_number=column[0],client=client).update(
                                                            title=column[1],
                                                            name1=column[2],
                                                            name2=column[3],
                                                            street=column[4],
                                                            area=column[5],
                                                            landmark=column[6],
                                                            city=column[7],
                                                            postal_code=column[8],
                                                            region=column[9],
                                                            mobile_number=column[10],
                                                            telephone_number=column[11],
                                                            fax_number=column[12],
                                                            email=column[13],
                                                            del_ind=column[14],  )

                                Address_updated_cnt = Address_updated_cnt + 1
                                Data_saved = 'Y'

                        else :

                            Address_duplicate_cnt = Address_duplicate_cnt +1
                            error_msg = get_message_desc(MSG094)[1]
                            # msgid = 'MSG094'
                            # error_msg = get_msg_desc(msgid)
                            # msg = error_msg['message_desc'][0]
                            # error_msg = msg
                            Address_errmsg_duplicate = error_msg
                            Address_error_flag = 'Y'

                # If the Input file Deletion indicator is "1" (Delete record) and Address\Client key  exist in the Address table

                if (del_ind_field == '1') and (OrgAddress.objects.filter ( address_number=column[0], client=client ).exists ()):
                    queryset_del = OrgAddress.objects.filter ( address_number=column[0], client=client )
                    for test in queryset_del:
                        if test.del_ind == False:
                            OrgAddress.objects.filter ( address_number=column[0], client=client ).update ( del_ind=1 )
                            Address_deleted_cnt = Address_deleted_cnt + 1
                            Data_saved = 'Y'

                # If the Input file Deletion indicator is "1" (Delete record) and Address\Client key  does not exist in the Address table.
                # Raise delete error

                if (del_ind_field == '1') and (not (OrgAddress.objects.filter ( address_number=column[0], client=client ).exists ())):
                    Address_delete_error = 'Y'
                    Address_delete_Err_Count = Address_delete_Err_Count + 1


            # Messages Summarising of processing of input file.
            messages.info ( req, 'Database Upload Results  :')
            messages.info ( req, '-------------------------------' )

            Addr_DB_count = OrgAddress.objects.filter ( del_ind=0 ).count ()
            messages.success ( req, ' Number of Records in Database    : ' + str ( Addr_DB_count ) )
            messages.success ( req, ' Records Inserted      : ' + str ( Address_inserted_cnt ) )
            messages.success ( req, ' Records Updated       : ' + str ( Address_updated_cnt ) )
            messages.success ( req, ' Records Deleted       : ' + str ( Address_deleted_cnt ) )
            messages.success ( req, ' No change Records       : ' + str ( Address_duplicate_cnt ) )

            if Address_line_no == 0:
                messages.error ( req, ' Empty File : Please correct and try again ' )
                Data_saved = ''
            if Address_delete_error != '' :
                messages.error ( req,
                                 ' Input Delete records that dont exist in DB : ' + str ( Address_delete_Err_Count ) )




        if Data_saved != 'Y':
            error_msg = get_message_desc(MSG043)[1]
            # msgid = 'MSG043'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            messages.error(req, error_msg)
            # messages.error ( req, MSG043 )
        else:
            error_msg = get_message_desc(MSG037)[1]
            # msgid = 'MSG037'
            # error_msg = get_msg_desc(msgid)
            messages.success(req, error_msg)
            # messages.success ( req, MSG037 )


    except Exception as e:
        print ( e )
        messages.error ( req, 'Error : ' + str ( e ) )


