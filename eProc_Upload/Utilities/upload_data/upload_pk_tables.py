import csv
import io

from django.apps import apps
from django.contrib import messages
from django.contrib.auth import get_user_model

from eProc_Basic.Utilities.functions.exclude_check import check_for_exclude
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.models import *
from eProc_Basic.Utilities.messages.messages import *
from eProc_Basic.Utilities.constants.constants import *


class CompareTableHeader:
    model = ''
    csv_headers = ''
    app_name = ''
    table_name = ''
    csv_header = []
    header_data = ''
    model_name = ''
    field_name = []

    def basic_header_condition(self):
        self.csv_header = []
        self.field_name = []
        # Gets the model name by taking the table name from UI
        self.model_name = apps.get_model(self.app_name, self.table_name)
        pk_field = self.model_name._meta.pk.name  # Gets the primary key

        # gets the headers of the csv file
        counter_flag = True
        for header in csv.reader(self.header_data, delimiter=',', quotechar='"'):
            if counter_flag:
                self.csv_headers = header
                counter_flag = False
                break
            else:
                break
        # Gets the respective field names of the model for the csv headers
        err_msg = ''
        exclude_list = ['CREATED_BY', 'CREATED_AT', 'CHANGED_BY', 'CHANGED_AT', 'created_by', 'created_at',
                        'changed_by', 'changed_at', 'GUID', 'SOURCE_SYSTEM', 'client_id', 'CLIENT_ID', 'source_system',
                        'CATALOG_ITEM']
        if self.table_name == 'OrgPorg':
            porg_exclude = ['COMPANY_ID', 'OBJECT_ID']
            exclude_list.append('COMPANY_ID')
            exclude_list.append('OBJECT_ID')
        if self.table_name == 'OrgPGroup':
            exclude_list.append('COMPANY_ID')
            exclude_list.append('PORG_ID')
            exclude_list.append('OBJECT_ID')
        if self.table_name == 'UserData':
            exclude_list.append('PERSON_NO')
            exclude_list.append('FORM_OF_ADDRESS')
            exclude_list.append('GENDER')
            exclude_list.append('PASSWORD')
            exclude_list.append('DATE_JOINED')
            exclude_list.append('FIRST_LOGIN')
            exclude_list.append('LAST_LOGIN')
            exclude_list.append('IS_ACTIVE')
            exclude_list.append('IS_SUPERUSER')
            exclude_list.append('IS_STAFF')
            exclude_list.append('LOGIN_ATTEMPTS')
            exclude_list.append('PWD_LOCKED')
            exclude_list.append('USER_LOCKED')
            exclude_list.append('SSO_USER')
            exclude_list.append('VALID_FROM')
            exclude_list.append('VALID_TO')
            exclude_list.append('OBJECT_ID')
        if self.table_name == 'SupplierMaster':
            exclude_list.append('EMAIL1')
            exclude_list.append('EMAIL2')
            exclude_list.append('EMAIL3')
            exclude_list.append('EMAIL4')
            exclude_list.append('EMAIL5')
            exclude_list.append('BLOCK DATE')
            exclude_list.append('BLOCK')
            exclude_list.append('DELIVERY_DAYS')
            exclude_list.append('IS_ACTIVE')
            exclude_list.append('COMPANY_ID')
            exclude_list.append('SUPPLIER_MASTER_SOURCE_SYSTEM')
            exclude_list.append('PREF_ROUTING')
            exclude_list.append('LOCK_DATE')
            exclude_list.append('GLOBAL_DUNS')
            exclude_list.append('DOMESTIC_DUNS')
            exclude_list.append('ICS_CODE')
            exclude_list.append('INTERNAL_IND')
            exclude_list.append('SBA_CODE')
            exclude_list.append('ETHNICITY')
            exclude_list.append('HUBZONE')
            exclude_list.append('NO_VEND_TEXT')
            exclude_list.append('AGR_REG_NO')
            exclude_list.append('NO_MULT_ADDR')

        field_details = []
        for field in self.model_name._meta.fields:
            tmp = field.get_attname_column()
            print(tmp[1])
            exclude_flag = check_for_exclude(exclude_list, tmp[1])
            if not exclude_flag:
                field_details.append({'field_name': field.column, 'field_length': field.max_length})
                self.field_name.append(field.column)
                if tmp[1] not in self.csv_headers:
                    msgid = 'MSG114'
                    error_msg = get_message_desc(msgid)[1]
                    err_msg = error_msg
                    return err_msg, field_details
        return err_msg, field_details

    def basic_header_condition_fk(self):
        self.csv_header = []

        db_header_value = list(self.db_header.split(","))

        # Gets the model name by taking the table name from UI
        self.model_name = apps.get_model(self.app_name, self.table_name)
        pk_field = self.model_name._meta.pk.name  # Gets the primary key

        # gets the headers of the csv file
        counter_flag = True
        for header in csv.reader(self.header_data, delimiter=',', quotechar='"'):
            if counter_flag:
                self.csv_headers = header
                counter_flag = False
                break
            else:
                break
        # Gets the respective field names of the model for the csv headers
        err_msg = ''
        for field in db_header_value:
            tmp = field
            if tmp not in self.csv_headers:
                msgid = 'MSG114'
                error_msg = get_message_desc(msgid)[1]
                err_msg = error_msg
            return err_msg
        return err_msg

    def csv_preview_data(self, db_header, data_set_val):
        """
            rearranging the jumbled data from csv
            param: db_header, data_set_val
            return: correct_order_list
        """
        upload_csv_header_data = []
        db_header_value = db_header
        fin_data_upld = io.StringIO(data_set_val)
        fin_data_upload_header = io.StringIO(data_set_val)
        correct_order_list = []
        error_message = None
        # Gets the header from the csv file
        for header in csv.reader(fin_data_upload_header, delimiter=',', quotechar='"'):
            upload_csv_header_data.append(header)
        upload_csv_header_data = upload_csv_header_data[0]
        next(fin_data_upld)
        pair_list = []
        print(upload_csv_header_data)
        print(db_header_value)

        # Makes list of required header and index of the same header in csv file
        for db_header in db_header_value:
            for upload_csv_header in range(len(upload_csv_header_data)):
                # if upload_csv_header_data[upload_csv_header] not in self.field_name:
                #     if upload_csv_header_data[upload_csv_header] != 'PRODUCT_IMAGE_PATH':
                #         msgid = 'MSG189'
                #         error_msg = get_message_desc(msgid)[1]
                #
                #         error_message = error_msg
                #         print(upload_csv_header_data[upload_csv_header])
                #         print(self.field_name)
                #         return error_message, correct_order_list
                # pair = []
                if db_header['field_name'] == upload_csv_header_data[upload_csv_header]:
                    pair_list.append({'field_name': db_header['field_name'], 'field_length': db_header['field_length'],
                                      'field_position': upload_csv_header})

        print(pair_list)

        # rearranges the data from csv file in required order
        for header in csv.reader(fin_data_upld, delimiter=',', quotechar='"'):

            data = header
            empty_check = [''] * len(data)
            if data == empty_check:
                continue
            data_dict = []
            for i in range(len(pair_list)):
                j = int(pair_list[i]['field_position'])
                field_data = data[j]
                if pair_list[i]['field_length']:
                    data_dict.append(field_data[:pair_list[i]['field_length']])
                else:
                    data_dict.append(field_data)
            correct_order_list.append(data_dict)

        return error_message, correct_order_list


class UploadBasicTables:
    def __init__(self, request):
        self.request = request

    # Global variables declared and used in complete class
    model = ''
    field_index = ''
    del_index = 0
    del_field = ''
    csv_headers = ''
    pk_index = ''
    filter_field = ''
    app_name = ''
    table_name = ''
    fk_index = ''
    fk_field = ''
    csv_header = []
    fk = []
    fk_exists = []
    no_fk = []
    keys = []
    related_model_pk = []
    field_index_check2 = ''
    field_index_check3 = ''
    field_index_check4 = ''
    field_index_check5 = ''
    field_index_check6 = ''
    field_index_check7 = ''
    test_mode = ''
    related_model = ''
    header_data = ''
    unique_keys = []
    model_name = ''
    rel_model_pk_field = ''
    rel_model_pk_index = 0
    field_name1 = ''
    field_name2 = ''
    field_name3 = ''
    field_name4 = ''
    field_name7 = ''
    #
    DB_count = 0
    Insert_Count = 0
    Update_Count = 0
    Delete_Count = 0
    invalid_count = 0
    File_Count = 0
    Delete_Err_Count = 0
    Duplicate_Count = 0
    delete_error = ''
    number_list = []
    columns = {}
    del_column = {}
    del_ind_field = ''
    Data_saved = ''
    Applimdesc_line_no = ''
    data_dict = {}
    data_check = {}
    fk_check = {}
    line_no = 0
    indexes = []
    fields = []
    client = 0
    company_field = ''
    company_index = 0

    def basic_table_conditions(self):
        self.csv_header = []
        # Gets the model name by taking the table name from UI
        self.model_name = apps.get_model(self.app_name, self.table_name)
        pk_field = self.model_name._meta.pk.name  # Gets the primary key

        # gets the headers of the csv file
        counter_flag = True
        for header in csv.reader(self.header_data, delimiter=',', quotechar='"'):
            if counter_flag:
                self.csv_headers = header
                counter_flag = False
                break
            else:
                break
        # Gets the respective field names of the model for the csv headers
        for field in self.model_name._meta.fields:
            tmp = field.get_attname_column()
            if tmp[1] in self.csv_headers:
                self.csv_header.append(tmp[0])

        # Gets the index for the primary key and del_ind as these are used across the function
        for index, field_name in enumerate(self.csv_header):
            if field_name == pk_field:
                self.pk_index = index
                self.filter_field = field_name

            if field_name == 'del_ind':
                self.del_index = index
                self.del_field = field_name

                break

        upload = self.upload_noguid_pk_data()

    def upload_noguid_pk_data(self):

        try:
            self.columns = {}
            # Gets the count of table
            self.DB_count = self.model_name.objects.filter(del_ind=False).count()

            # Read thru the file record by record , Assign column based on comma delimter
            field_name1 = self.field_name1
            field_name7 = self.field_name7
            for column_data in csv.reader(self.header_data, delimiter=',', quotechar='"'):
                data = column_data
                print(self.Update_Count)
                print(self.del_column[self.del_field])
                for index, field_name in enumerate(self.csv_header):
                    self.data_dict[field_name] = data[index]

                self.File_Count = self.File_Count + 1
                self.del_column[self.del_field] = column_data[self.del_index]

                # Checks if the data exists in the tables
                self.columns[self.filter_field] = column_data[self.pk_index]
                new_data = self.model_name.objects.filter(**self.columns)
                check_query = new_data.exists()

                if self.test_mode == 'on':
                    # if del_ind = 0 and data doesnt exists in table then insert or get the dupicate count
                    if (self.del_column[self.del_field] == '0') and (not check_query):
                        if self.columns[self.filter_field] in self.number_list:
                            self.Duplicate_Count = self.Duplicate_Count + 1
                            error_msg = get_message_desc(MSG094)[1]
                            # msgid = 'MSG094'
                            # error_msg = get_msg_desc(msgid)
                            # msg = error_msg['message_desc'][0]
                            # error_msg = msg
                            errmsg_duplicate = error_msg
                            errmsg_duplicate = error_msg
                        else:
                            self.Insert_Count = self.Insert_Count + 1

                    # If the Input file Deletion indicator is "0" (Insert\Update record) and data  does not exist in
                    # the table
                    elif (self.del_column[self.del_field] == '0') and check_query:
                        if not (self.model_name.objects.filter(**self.data_dict)):
                            self.Update_Count = self.Update_Count + 1

                    # Check  If the Input file Deletion indicator is "1" (Delete record) and if record  exists
                    # Check if the record is active on DB.

                    if (self.del_column[self.del_field] == '1') and check_query:
                        for test in new_data:
                            if not test.del_ind:
                                self.Delete_Count = self.Delete_Count + 1

                    self.number_list.append(column_data[0])

                elif self.test_mode != 'on':

                    # If the Deletion indicator in the file = "0" and record does not exist on the DB : INSERT DB

                    if (self.del_column[self.del_field] == '0') and (not check_query):
                        _, created = self.model_name.objects.get_or_create(**self.data_dict)
                        self.Insert_Count = self.Insert_Count + 1
                        self.Data_saved = 'Y'

                    # If the Deletion indicator in the file = "0" and record  exist on the DB : Update DB

                    elif (self.del_column[self.del_field] == '0') and check_query:
                        if not (self.model_name.objects.filter(**self.data_dict)):
                            new_data.update(**self.data_dict)
                            self.Update_Count = self.Update_Count + 1

                            self.Data_saved = 'Y'

                    # If the Deletion indicator in the file = "1" and record  exist on the DB : Soft Delete(del_ind =0) DB

                    if (self.del_column[self.del_field] == '1') and check_query:
                        for test in new_data:
                            if not test.del_ind:
                                new_data.update(del_ind=1)
                                self.Delete_Count = self.Delete_Count + 1
                                self.Data_saved = 'Y'

                # If the Deletion indicator in the file = "1" and record  does not exist on the DB : Error message

                if (self.del_column[self.del_field] == '1') and (not check_query):
                    delete_error = 'Y'
                    self.Delete_Err_Count = self.Delete_Err_Count + 1

            # Display insert /updated count in the display
            self.DB_count = self.model_name.objects.filter(del_ind=False).count()

            # -------------------------------------------------------------------------------------#
            #         messages displayed for Test and normal mode

            messages.info(self.request, 'Database Upload Results  :')
            messages.info(self.request, '-------------------------------')

            # # Display the number of Active records in DB
            messages.success(self.request, ' Number of Active Records in Database    : ' + str(self.DB_count))
            # Number of records in the Input file.
            messages.success(self.request, ' Number of Records in Input file  : ' + str(self.File_Count))
            # Display the number of records Inserted
            messages.success(self.request, ' Records to be Inserted or Inserted    : ' + str(self.Insert_Count))
            # Display the number of records Updated
            messages.success(self.request, ' Records to be Updated or Updated      : ' + str(self.Update_Count))
            # Display the number of records Deleted
            messages.success(self.request, ' Records to be Deleted or deleted      : ' + str(self.Delete_Count))

            # # Total records that are duplicate in the input file
            messages.error(self.request, ' Duplicate Records                : ' + str(self.Duplicate_Count))

            # Display message for empty file
            if self.File_Count == 0:
                messages.error(self.request, ' Empty File : Please correct and try again ')
                Data_saved = ''

            # Display error message if delete record doesnt exist on DB
            if self.delete_error != '':
                messages.error(self.request,
                               ' Input Delete records that dont exist in DB : ' + str(self.Delete_Err_Count))

            if self.Data_saved == 'Y':
                error_msg = get_message_desc(MSG037)[1]
                # msgid = 'MSG037'
                # error_msg = get_msg_desc(msgid)

                messages.success(self.request, error_msg)
                # messages.success(self.request, MSG037)
            else:
                error_msg = get_message_desc(MSG043)[1]
                # msgid = 'MSG043'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg

                messages.error(self.request, error_msg)
                # messages.error(self.request, MSG043)


        except Exception as e:
            print(e)
            messages.error(self.request, 'Error : ' + str(e))

    # **************************************************************************************************************

    def basic_table_new_conditions(self, country_array, country_header):

        check_messages = {}
        self.csv_header = []
        self.number_list = []
        self.data_dict = {}
        # Gets the model name by taking the table name from UI
        self.model_name = apps.get_model(self.app_name, self.table_name)
        pk_field = self.model_name._meta.pk.name  # Gets the primary key

        # gets the headers of the csv file
        self.csv_headers = country_header
        counter_flag = True

        # Gets the respective field names of the model for the csv headers
        for field in self.model_name._meta.fields:
            tmp = field.get_attname_column()
            if tmp[1] in self.csv_headers:
                self.csv_header.append(tmp[0])
        # Gets the index for the primary key and del_ind as these are used across the function
        for index, field_name in enumerate(self.csv_header):
            if field_name == pk_field:
                self.pk_index = index
                self.filter_field = field_name

            if field_name == 'del_ind':
                self.del_index = index
                self.del_field = field_name

                break

        try:
            self.columns = {}
            # Gets the count of table
            self.DB_count = self.model_name.objects.filter(del_ind=False).count()

            # Read thru the file record by record , Assign column based on comma delimter
            field_name1 = self.field_name1
            field_name7 = self.field_name7
            for column_data in country_array:
                data = column_data
                for index, field_name in enumerate(self.csv_header):
                    self.data_dict[field_name] = data[index]

                self.File_Count = self.File_Count + 1
                self.del_column[self.del_field] = column_data[self.del_index]

                # Checks if the data exists in the tables
                self.columns[self.filter_field] = column_data[self.pk_index]
                new_data = self.model_name.objects.filter(**self.columns).values()
                check_query = new_data.exists()

                # If the Deletion indicator in the pop-up = "0" and record repeats in pop up - Duplicate Count
                if self.columns[self.filter_field] in self.number_list:
                    self.Duplicate_Count = self.Duplicate_Count + 1
                    error_msg = get_message_desc(MSG094)[1]
                    # msgid = 'MSG094'
                    # error_msg = get_msg_desc(msgid)
                    # msg = error_msg['message_desc'][0]
                    # error_msg = msg
                    errmsg_duplicate = error_msg
                    # errmsg_duplicate = MSG094

                # If the Deletion indicator in the pop-up = "0" and record does not exist on the DB - Insert Count
                elif (self.del_column[self.del_field] == '0') and (not check_query):
                    self.Insert_Count = self.Insert_Count + 1
                elif (self.del_column[self.del_field] == '0') and check_query and new_data[0]['del_ind']:
                    self.Insert_Count = self.Insert_Count + 1
                elif (self.del_column[self.del_field] == '0') and check_query and not new_data[0]['del_ind']:
                    # If the Deletion indicator in the pop-up = "0" and record  exist on the DB - Update Count
                    if not (self.model_name.objects.filter(**self.data_dict)):
                        self.Update_Count = self.Update_Count + 1
                elif (self.del_column[self.del_field] == '1') and (not check_query):
                    self.invalid_count = self.invalid_count + 1
                # If the Deletion indicator in the pop-up = "1" and record  exist on the DB - Delete Count
                if (self.del_column[self.del_field] == '1') and check_query:
                    for test in new_data:
                        if not test['del_ind']:
                            self.Delete_Count = self.Delete_Count + 1

                self.number_list.append(column_data[0])

            check_messages['db_count'] = self.DB_count
            check_messages['file_count'] = self.File_Count
            check_messages['duplicate_count'] = self.Duplicate_Count
            check_messages['insert_count'] = self.Insert_Count
            check_messages['update_count'] = self.Update_Count
            check_messages['delete_count'] = self.Delete_Count
            check_messages['invalid_count'] = self.invalid_count

            db_count_message = get_message_desc('MSG193')[1] + str(self.DB_count)
            file_count_message = get_message_desc('MSG194')[1] + str(self.File_Count)
            delete_count_message = get_message_desc('MSG197')[1] + str(self.Delete_Count)
            invalid_count_message = get_message_desc('MSG199')[1] + str(self.invalid_count)
            duplicate_count_message = get_message_desc('MSG198')[1] + str(self.Duplicate_Count)
            update_count_message = get_message_desc('MSG196')[1] + str(self.Update_Count)
            insert_count_message = get_message_desc('MSG195')[1] + str(self.Insert_Count)
            message = [db_count_message, file_count_message, insert_count_message, update_count_message,
                       duplicate_count_message, delete_count_message, invalid_count_message]
            check_messages['messages'] = message

            return check_messages

        except Exception as e:
            print(e)
            messages.error(self.request, 'Error : ' + str(e))
