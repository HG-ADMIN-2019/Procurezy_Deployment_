"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    upload_basic_pk_fk_tables.py

Usage:
    File which handles the generic code for uploading basic tables data
    basic_table_conditions() : Gets the respective field names and details required to upload the data which has no foreign keys
                                and no guid generations while creating the data.
    upload_noguid_pk_data() : Generic function which uploads the data which has only primary key relation and no other keys or guid generation.
    guids_table_conditions() : Gets the complete details of the model(table) which is being uploaded which has the guid as pk.
    upload_guids_pk_fk_data() : Generic function to upload data which has only PK , FK keys.Guid as PK and client as FK.
                                NO primary checks before inserting or updating entries to the table.
Author:
    Soni Vydyula- Generic code for Upload Functionality - MEP-117
"""

import csv
from django.apps import apps
from django.contrib import messages
from django.contrib.auth import get_user_model

from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.models import *
from eProc_Basic.Utilities.messages.messages import *
from eProc_Configuration.models import OrgClients, OrgCompanies
from eProc_Configuration.models.development_data import AuthorizationObject, UserRoles


def non_match_elements(fk, unique_keys):
    unique_check = []
    for i in fk:
        if i not in unique_keys:
            unique_check = i
    return unique_check


def DictListUpdate(res, fk_dict):
    for key, value in fk_dict.items():
        for key1, value1 in res.items():
            if key == key1:
                res.update(fk_dict)
    return res


class UploadPkFkTables:
    # Global variables declared and used in complete class
    model = ''
    field_index = ''
    del_index = 0
    del_field = ''
    csv_headers = ''
    pk_index = ''
    filter_field = ''
    request = ''
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

    def guids_table_conditions(self):
        unique_check = []
        pk_of_fk_model = []
        self.csv_header = []
        self.fk = []
        fks = []
        # Gets the model name by taking the table name from UI
        self.model_name = apps.get_model(self.app_name, self.table_name)

        # Gets the unique keys
        keys = self.model_name._meta.unique_together
        unique_key = [element for tupl in keys for element in tupl]
        if unique_key:
            unique_values = unique_key.remove('client')

        # gets the headers of the csv file
        counter_flag = True
        for header in csv.reader(self.header_data, delimiter=',', quotechar='"'):
            if counter_flag:
                self.csv_headers = header
                counter_flag = False
                break
            else:
                break
        # gets Foreign keys of the respective model
        for field in self.model_name._meta.fields:
            if field.get_internal_type() == 'ForeignKey':
                res = field.get_attname_column()
                res = res[0][:-3]
                self.fk.append(res)
        if self.fk:
            if 'client' in self.fk:
                fks = self.fk.remove('client')

        # Gets the respective field names of the model for the csv headers
        for field in self.model_name._meta.fields:
            tmp = field.get_attname_column()
            if tmp[1] in self.csv_headers:
                if field.get_internal_type() == 'ForeignKey':
                    tmp = tmp[0][:-3]
                    self.csv_header.append(tmp)
                else:
                    self.csv_header.append(tmp[0])

        self.unique_keys = sorted(unique_key, key=lambda x: self.csv_header.index(x))

        # gets the non matched field names from fk and unique keys
        unique_check = non_match_elements(self.fk, self.unique_keys)
        if unique_check:
            self.related_model = self.model_name._meta.get_field(unique_check).related_model

            for index, field_name in enumerate(self.csv_header):
                if field_name == unique_check:
                    self.rel_model_pk_index = index
                    self.rel_model_pk_field = field_name

        self.indexes = []
        self.fields = []
        for index, field_name in enumerate(self.unique_keys):
            self.indexes.append(index)
            self.fields.append(field_name)
        # gets the field name and index of del_ind
        for index, field_name in enumerate(self.csv_header):
            if field_name == 'company_id':
                self.company_field = field_name
                self.company_index = index

            if field_name == 'auth_obj_id':
                self.fk_index = index
                self.fk_field = field_name
            if field_name == 'role':
                self.fk_index = index
                self.fk_field = field_name
            if field_name == 'del_ind':
                self.del_index = index
                self.del_field = field_name
                break

        # for index,field_name in enumerate(self.fk):

        if self.table_name == 'SpendLimitValue' or self.table_name == 'ApproverLimitValue' or self.table_name == 'AccountingDataDesc' or \
                self.table_name == 'AccountingData' or self.table_name == 'OrgPorg' or self.table_name == 'OrgPGroup':
            for index, field_name in enumerate(self.csv_header):
                if self.table_name == 'AccountingData':
                    if field_name == 'account_assign_cat':
                        self.field_index = index
                        self.rel_model_pk_index = index
                        self.rel_model_pk_field = field_name
                        break
                if self.table_name == 'OrgPorg':
                    if field_name == 'description':
                        self.field_index = index
                    if field_name == 'company_id':
                        self.field_index_check2 = index
                    if field_name == 'object_id':
                        self.field_index_check3 = index
                        self.rel_model_pk_index = index
                        self.rel_model_pk_field = field_name
                        break
                if self.table_name == 'OrgPGroup':
                    if field_name == 'description':
                        self.field_index = index
                    if field_name == 'porg_id':
                        self.field_index_check2 = index
                    if field_name == 'object_id':
                        self.field_index_check3 = index
                        self.rel_model_pk_index = index
                        self.rel_model_pk_field = field_name
                        break

            upload = self.upload_master_data()
        else:
            upload = self.upload_guids_pk_fk_data()

    def upload_guids_pk_fk_data(self):
        self.client = getClients(self.request)
        try:
            self.columns = {}
            update_check = {}

            # Gets the count of table
            self.DB_count = self.model_name.objects.filter(del_ind=False).count()

            # Read thru the file record by record , Assign column based on comma delimiter
            for column_data in csv.reader(self.header_data, delimiter=',', quotechar='"'):
                data = column_data
                for index, field_name in enumerate(self.csv_header):
                    self.data_dict[field_name] = data[index]
                    if not field_name == 'del_ind':
                        update_check[field_name] = data[index]

                self.File_Count = self.File_Count + 1
                self.del_column[self.del_field] = column_data[self.del_index]

                # Checks if the data exists in the tables
                # self.columns[self.filter_field] = column_data[self.pk_index]
                if self.table_name == 'AuthorizationGroup':
                    new_data = self.model_name.objects.filter(**update_check)
                    self.data_dict.pop('auth_obj_id', None)
                elif self.table_name == 'Authorization':
                    new_data = self.model_name.objects.filter(client=self.client, **update_check)
                    self.data_dict.pop('role', None)
                else:
                    new_data = self.model_name.objects.filter(client=self.client, **update_check)

                check_query = new_data.exists()

                if self.test_mode == 'on':
                    # if del_ind = 0 and data doesnt exists in table then insert or get the dupicate count
                    if (self.del_column[self.del_field] == '0') and (not check_query):
                        self.Insert_Count = self.Insert_Count + 1

                    # If the Input file Deletion indicator is "0" (Insert\Update record) and data  does not exist in the table
                    elif (self.del_column[self.del_field] == '0') and check_query:
                        if not (self.model_name.objects.filter(**self.data_dict)):
                            self.Update_Count = self.Update_Count + 1
                        else:
                            self.Duplicate_Count = self.Duplicate_Count + 1

                    # Check  If the Input file Deletion indicator is "1" (Delete record) and if record  exists
                    # Check if the record is active on DB.

                    if (self.del_column[self.del_field] == '1') and check_query:
                        for test in new_data:
                            if not test.del_ind:
                                self.Delete_Count = self.Delete_Count + 1


                elif self.test_mode != 'on':

                    obj_id = {}
                    # If the Deletion indicator in the file = "0" and record does not exist on the DB : INSERT DB
                    if (self.del_column[self.del_field] == '0') and (not check_query):
                        if not (self.table_name == 'AuthorizationGroup' or self.table_name == 'Authorization'):
                            _, created = self.model_name.objects.get_or_create(pk=guid_generator(),
                                                                               client=OrgClients.objects.get(
                                                                                   client=self.client),
                                                                               **self.data_dict)
                        elif self.table_name == 'Authorization':
                            obj_id[self.fk_field] = column_data[self.fk_index]
                            _, created = self.model_name.objects.get_or_create(pk=guid_generator(),
                                                                               client=OrgClients.objects.get(
                                                                                   client=self.client),
                                                                               role=UserRoles.objects.get(**obj_id),
                                                                               **self.data_dict)
                        else:
                            obj_id[self.fk_field] = column_data[self.fk_index]
                            _, created = self.model_name.objects.get_or_create(pk=guid_generator(),
                                                                               auth_obj_id=AuthorizationObject.objects.get(
                                                                                   **obj_id), **self.data_dict)
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

                messages.success(self.request, error_msg)
                # messages.success(self.request, MSG037)
            else:
                error_msg = get_message_desc(MSG043)[1]
                # msgid = 'MSG043'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg

                messages.success(self.request, error_msg)

                # messages.error(self.request, MSG043)


        except Exception as e:
            print(e)
            messages.error(self.request, 'Error : ' + str(e))

    def upload_master_data(self):
        self.client = getClients(self.request)
        try:

            # Gets the count of table
            self.DB_count = self.model_name.objects.filter(del_ind=False).count()

            # Read thru the file record by record , Assign column based on comma delimter
            # if self.related_model.objects.filter().exists():
            for column_data in csv.reader(self.header_data, delimiter=',', quotechar='"'):
                self.line_no = self.line_no + 1
                print(" Extract Line Number:" + str(self.line_no))
                data = column_data
                # assigns the respective fieldnames and values in the dictionary
                for index, field_name in enumerate(self.csv_header):
                    self.error_flag = ''
                    for index1, field_name1 in enumerate(self.unique_keys):
                        if field_name == field_name1:
                            int_index = self.csv_header.index(field_name1)
                            self.data_check[field_name] = data[int_index]

                rel_model = {}
                company = {}
                # condtion for primary checks for related primary key tables entries exists or not
                rel_model[self.rel_model_pk_field] = column_data[self.rel_model_pk_index]
                company[self.company_field] = column_data[self.company_index]
                if (self.table_name == 'AccountingDataDesc') or (self.table_name == 'AccountingData'):
                    if not (OrgCompanies.objects.filter(**company).exists()):
                        error_msg = get_message_desc(MSG099)[1]
                        # msgid = 'MSG099'
                        # error_msg = get_msg_desc(msgid)
                        # msg = error_msg['message_desc'][0]
                        # error_msg = msg
                        errmsg_Company = error_msg
                        messages.error(self.request,
                                       errmsg_Company + ' @Line Number : ' + str(
                                           self.File_Count))

                        self.error_flag = 'Y'
                else:
                    if not (self.related_model.objects.filter(**rel_model).exists()):
                        print("error")
                        self.error_flag = 'Y'
                # checks if unique together keys values exists or not
                if self.model_name.objects.filter(**self.data_check).exists():
                    Applimdesc_errmsg_unique = 'Duplicate found on Unique key '
                    messages.error(self.request, Applimdesc_errmsg_unique + ' @Line Number : ' + str(
                        self.line_no))
                    # self.error_flag = 'Y'
                if self.error_flag == 'Y':
                    continue

                fk_dict = {}
                res = {}
                update_check = {}
                data = column_data
                # Assign the data to dictionary which is used while creating or updating the table
                for index, field_name in enumerate(self.csv_header):
                    self.data_dict[field_name] = data[index]
                    res = self.data_dict
                    if not field_name == 'del_ind':
                        update_check[field_name] = data[index]
                    # gets the data of foreign keys from the respective primary key table
                    for index2, field_name2 in enumerate(self.fk):
                        self.fk_check = {}
                        if field_name == field_name2:
                            fk_index = self.csv_header.index(field_name2)
                            self.fk_check[field_name] = data[fk_index]
                            fk_model = self.model_name._meta.get_field(field_name2).related_model
                            tmp1 = fk_model.objects.get(**self.fk_check)
                            fk_dict[field_name2] = tmp1
                            tmp = DictListUpdate(res, fk_dict)

                # gets the file count
                self.File_Count = self.File_Count + 1
                # assigns the del_ind value to check in further conditions
                self.del_column[self.del_field] = column_data[self.del_index]

                # Checks if the data exists in the tables
                new_data = self.model_name.objects.filter(**update_check)
                check_query = new_data.exists()

                if self.test_mode == 'on':
                    # if del_ind = 0 and data doesnt exists in table then insert or get the dupicate count
                    if (self.del_column[self.del_field] == '0') and (not check_query):
                        self.Insert_Count = self.Insert_Count + 1

                    # If the Input file Deletion indicator is "0" (Insert\Update record) and data  does not exist in the table
                    elif (self.del_column[self.del_field] == '0') and check_query:
                        for field_name in new_data:
                            if self.table_name == 'AccountingData':
                                if field_name != column_data[self.field_index]:
                                    self.Update_Count = self.Update_Count + 1
                            elif self.table_name == 'OrgPorg':
                                if field_name != column_data[self.field_index] or field_name != column_data[
                                    self.field_index_check2] or \
                                        field_name != column_data[self.field_index_check3]:
                                    self.Update_Count = self.Update_Count + 1
                            else:
                                self.Duplicate_Count = self.Duplicate_Count + 1

                    # Check  If the Input file Deletion indicator is "1" (Delete record) and if record  exists
                    # Check if the record is active on DB.

                    if (self.del_column[self.del_field] == '1') and check_query:
                        for test in new_data:
                            if not test.del_ind:
                                self.Delete_Count = self.Delete_Count + 1


                elif self.test_mode != 'on':

                    # If the Deletion indicator in the file = "0" and record does not exist on the DB : INSERT DB

                    if (self.del_column[self.del_field] == '0') and (not check_query):
                        _, created = self.model_name.objects.get_or_create(pk=guid_generator(), client=self.client,
                                                                           **self.data_dict)
                        self.Insert_Count = self.Insert_Count + 1
                        self.Data_saved = 'Y'

                    # If the Deletion indicator in the file = "0" and record  exist on the DB : Update DB

                    elif (self.del_column[self.del_field] == '0') and check_query:
                        for field_name in new_data:
                            if self.table_name == 'AccountingData':
                                if field_name != column_data[self.field_index]:
                                    new_data.update(**self.data_dict)
                                    self.Update_Count = self.Update_Count + 1
                                    self.Data_saved = 'Y'
                            elif self.table_name == 'OrgPorg':
                                if field_name != column_data[self.field_index] or field_name != column_data[
                                    self.field_index_check2] or \
                                        field_name != column_data[self.field_index_check3]:
                                    new_data.update(**self.data_dict)
                                    self.Update_Count = self.Update_Count + 1
                                    self.Data_saved = 'Y'
                        if not (self.model_name.objects.filter(**self.data_dict)):
                            new_data.update(**self.del_column)
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
                    self.delete_error = 'Y'
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

                messages.success(self.request, error_msg)
                # messages.error(self.request, MSG043)


        except Exception as e:
            print(e)
            messages.error(self.request, 'Error : ' + str(e))

    def upload_master_data_new(self, popup_data_list, db_header_data, client):
        unique_check = []
        pk_of_fk_model = []
        self.csv_header = []
        self.fk = []
        fks = []
        check_messages = {}
        # Gets the model name by taking the table name from UI
        self.model_name = apps.get_model(self.app_name, self.table_name)

        # Gets the unique keys
        keys = self.model_name._meta.unique_together
        unique_key = [element for tupl in keys for element in tupl]
        if unique_key:
            unique_values = unique_key.remove('client')

        # gets the headers of the csv file
        self.csv_headers = db_header_data
        # counter_flag = True
        # for header in db_header_data:
        #     if counter_flag:
        #         self.csv_headers = header
        #         counter_flag = False
        #         break
        #     else:
        #         break
        # gets Foreign keys of the respective model
        for field in self.model_name._meta.fields:
            if field.get_internal_type() == 'ForeignKey':
                res = field.get_attname_column()
                res = res[0][:-3]
                self.fk.append(res)
        if self.fk:
            if 'client' in self.fk:
                fks = self.fk.remove('client')

        # Gets the respective field names of the model for the csv headers
        for field in self.model_name._meta.fields:
            tmp = field.get_attname_column()
            if tmp[1] in self.csv_headers:
                if field.get_internal_type() == 'ForeignKey':
                    tmp = tmp[0][:-3]
                    self.csv_header.append(tmp)
                else:
                    self.csv_header.append(tmp[0])

        self.unique_keys = sorted(unique_key, key=lambda x: self.csv_header.index(x))

        # gets the non matched field names from fk and unique keys
        unique_check = non_match_elements(self.fk, self.unique_keys)
        if unique_check:
            self.related_model = self.model_name._meta.get_field(unique_check).related_model

            for index, field_name in enumerate(self.csv_header):
                if field_name == unique_check:
                    self.rel_model_pk_index = index
                    self.rel_model_pk_field = field_name

        self.indexes = []
        self.fields = []
        for index, field_name in enumerate(self.unique_keys):
            self.indexes.append(index)
            self.fields.append(field_name)
        # gets the field name and index of del_ind
        for index, field_name in enumerate(self.csv_header):
            if field_name == 'company_id':
                self.company_field = field_name
                self.company_index = index

            if field_name == 'auth_obj_id':
                self.fk_index = index
                self.fk_field = field_name
            if field_name == 'role':
                self.fk_index = index
                self.fk_field = field_name
            if field_name == 'del_ind':
                self.del_index = index
                self.del_field = field_name
                break

        # for index,field_name in enumerate(self.fk):

        if self.table_name == 'SpendLimitValue' or self.table_name == 'ApproverLimitValue' or self.table_name == 'AccountingDataDesc' or \
                self.table_name == 'AccountingData' or self.table_name == 'OrgPorg' or self.table_name == 'OrgPGroup':
            for index, field_name in enumerate(self.csv_header):
                if self.table_name == 'AccountingData':
                    if field_name == 'account_assign_cat':
                        self.field_index = index
                        self.rel_model_pk_index = index
                        self.rel_model_pk_field = field_name
                        break
                if self.table_name == 'OrgPorg':
                    if field_name == 'description':
                        self.field_index = index
                    if field_name == 'company_id':
                        self.field_index_check2 = index
                    if field_name == 'object_id':
                        self.field_index_check3 = index
                        self.rel_model_pk_index = index
                        self.rel_model_pk_field = field_name
                        break
                if self.table_name == 'OrgPGroup':
                    if field_name == 'description':
                        self.field_index = index
                    if field_name == 'porg_id':
                        self.field_index_check2 = index
                    if field_name == 'object_id':
                        self.field_index_check3 = index
                        self.rel_model_pk_index = index
                        self.rel_model_pk_field = field_name
                        break
        self.client = client

        try:
            self.client = client
            # Gets the count of table
            self.DB_count = self.model_name.objects.filter(del_ind=False).count()

            # Read thru the file record by record , Assign column based on comma delimter
            # if self.related_model.objects.filter().exists():
            for column_data in popup_data_list:
                self.line_no = self.line_no + 1
                print(" Extract Line Number:" + str(self.line_no))
                data = column_data
                # assigns the respective fieldnames and values in the dictionary
                for index, field_name in enumerate(self.csv_header):
                    self.error_flag = ''
                    for index1, field_name1 in enumerate(self.unique_keys):
                        if field_name == field_name1:
                            int_index = self.csv_header.index(field_name1)
                            self.data_check[field_name] = data[int_index]

                rel_model = {}
                company = {}
                # condtion for primary checks for related primary key tables entries exists or not
                rel_model[self.rel_model_pk_field] = column_data[self.rel_model_pk_index]
                company[self.company_field] = column_data[self.company_index]
                print(company)
                if (self.table_name == 'AccountingDataDesc') or (self.table_name == 'AccountingData'):
                    if not (OrgCompanies.objects.filter(**company).exists()):
                        error_msg = get_message_desc(MSG099)[1]
                        # msgid = 'MSG099'
                        # error_msg = get_msg_desc(msgid)
                        # msg = error_msg['message_desc'][0]
                        # error_msg = msg
                        errmsg_Company = error_msg
                        messages.error(self.request,
                                       errmsg_Company + ' @Line Number : ' + str(
                                           self.File_Count))

                        self.error_flag = 'Y'
                else:
                    if not (self.related_model.objects.filter(**rel_model).exists()):
                        print("error")
                        self.error_flag = 'Y'
                # checks if unique together keys values exists or not
                # if self.model_name.objects.filter(**self.data_check).exists():
                #     self.Duplicate_Count = self.Duplicate_Count + 1

                # self.error_flag = 'Y'
                if self.error_flag == 'Y':
                    continue

                fk_dict = {}
                res = {}
                update_check = {}
                data = column_data
                # Assign the data to dictionary which is used while creating or updating the table
                for index, field_name in enumerate(self.csv_header):
                    self.data_dict[field_name] = data[index]
                    res = self.data_dict
                    if not field_name == 'del_ind':
                        update_check[field_name] = data[index]
                    # gets the data of foreign keys from the respective primary key table
                    for index2, field_name2 in enumerate(self.fk):
                        self.fk_check = {}
                        if field_name == field_name2:
                            fk_index = self.csv_header.index(field_name2)
                            self.fk_check[field_name] = data[fk_index]
                            fk_model = self.model_name._meta.get_field(field_name2).related_model
                            tmp1 = fk_model.objects.get(**self.fk_check)
                            fk_dict[field_name2] = tmp1
                            tmp = DictListUpdate(res, fk_dict)

                # gets the file count
                self.File_Count = self.File_Count + 1
                # assigns the del_ind value to check in further conditions
                self.del_column[self.del_field] = column_data[self.del_index]

                # Checks if the data exists in the tables
                new_data = self.model_name.objects.filter(**update_check)
                check_query = new_data.exists()

                # if del_ind = 0 and data doesnt exists in table then insert or get the dupicate count
                if (self.del_column[self.del_field] == '0') and (not check_query):
                    self.Insert_Count = self.Insert_Count + 1

                # If the Input file Deletion indicator is "0" (Insert\Update record) and data  does not exist in the table
                elif (self.del_column[self.del_field] == '0') and check_query:
                    for field_name in new_data:
                        if self.table_name == 'AccountingData':
                            if field_name != column_data[self.field_index]:
                                self.Update_Count = self.Update_Count + 1
                        elif self.table_name == 'OrgPorg':
                            if field_name != column_data[self.field_index] or field_name != column_data[
                                self.field_index_check2] or \
                                    field_name != column_data[self.field_index_check3]:
                                self.Update_Count = self.Update_Count + 1
                        else:
                            pass

                # Check  If the Input file Deletion indicator is "1" (Delete record) and if record  exists
                # Check if the record is active on DB.

                if (self.del_column[self.del_field] == '1') and check_query:
                    for test in new_data:
                        if not test.del_ind:
                            self.Delete_Count = self.Delete_Count + 1

            check_messages['db_count'] = self.DB_count
            check_messages['file_count'] = self.File_Count
            check_messages['duplicate_count'] = self.Duplicate_Count
            check_messages['insert_count'] = self.Insert_Count
            check_messages['update_count'] = self.Update_Count
            check_messages['delete_count'] = self.Delete_Count

            print(check_messages)

            return check_messages


        except Exception as e:
            print(e)
            messages.error(self.request, 'Error : ' + str(e))

    def basic_table_new_conditions(self, popup_data_list, db_header_data, client):
        unique_check = []
        pk_of_fk_model = []
        self.csv_header = []
        self.csv_headers = []
        self.fk = []
        fks = []
        check_messages = {}
        # Gets the model name by taking the table name from UI
        self.model_name = apps.get_model(self.app_name, self.table_name)

        # Gets the unique keys
        keys = self.model_name._meta.unique_together
        unique_key = [element for tupl in keys for element in tupl]
        if unique_key:
            unique_values = unique_key.remove('client')

        # gets the headers of the csv file
        self.csv_headers = db_header_data
        # counter_flag = True
        # for header in db_header_data:
        #     if counter_flag:
        #         self.csv_headers = header
        #         counter_flag = False
        #         break
        #     else:
        #         break
        # gets Foreign keys of the respective model
        for field in self.model_name._meta.fields:
            if field.get_internal_type() == 'ForeignKey':
                res = field.get_attname_column()
                res = res[0][:-3]
                self.fk.append(res)
        if self.fk:
            if 'client' in self.fk:
                fks = self.fk.remove('client')

        # Gets the respective field names of the model for the csv headers
        for field in self.model_name._meta.fields:
            tmp = field.get_attname_column()
            if tmp[1] in self.csv_headers:
                if field.get_internal_type() == 'ForeignKey':
                    tmp = tmp[0][:-3]
                    self.csv_header.append(tmp)
                else:
                    self.csv_header.append(tmp[0])

        self.unique_keys = sorted(unique_key, key=lambda x: self.csv_header.index(x))

        # gets the non matched field names from fk and unique keys
        unique_check = non_match_elements(self.fk, self.unique_keys)
        if unique_check:
            self.related_model = self.model_name._meta.get_field(unique_check).related_model

            for index, field_name in enumerate(self.csv_header):
                if field_name == unique_check:
                    self.rel_model_pk_index = index
                    self.rel_model_pk_field = field_name

        self.indexes = []
        self.fields = []
        for index, field_name in enumerate(self.unique_keys):
            self.indexes.append(index)
            self.fields.append(field_name)
        # gets the field name and index of del_ind
        for index, field_name in enumerate(self.csv_header):
            if field_name == 'company_id':
                self.company_field = field_name
                self.company_index = index

            if field_name == 'auth_obj_id':
                self.fk_index = index
                self.fk_field = field_name
            if field_name == 'role':
                self.fk_index = index
                self.fk_field = field_name
            if field_name == 'del_ind':
                self.del_index = index
                self.del_field = field_name
                break

        # for index,field_name in enumerate(self.fk):

        if self.table_name == 'SpendLimitValue' or self.table_name == 'ApproverLimitValue' or self.table_name == 'AccountingDataDesc' or \
                self.table_name == 'AccountingData' or self.table_name == 'OrgPorg' or self.table_name == 'OrgPGroup':
            for index, field_name in enumerate(self.csv_header):
                if self.table_name == 'AccountingData':
                    if field_name == 'account_assign_cat':
                        self.field_index = index
                        self.rel_model_pk_index = index
                        self.rel_model_pk_field = field_name
                        break
                if self.table_name == 'OrgPorg':
                    if field_name == 'description':
                        self.field_index = index
                    if field_name == 'company_id':
                        self.field_index_check2 = index
                    if field_name == 'object_id':
                        self.field_index_check3 = index
                        self.rel_model_pk_index = index
                        self.rel_model_pk_field = field_name
                        break
                if self.table_name == 'OrgPGroup':
                    if field_name == 'description':
                        self.field_index = index
                    if field_name == 'porg_id':
                        self.field_index_check2 = index
                    if field_name == 'object_id':
                        self.field_index_check3 = index
                        self.rel_model_pk_index = index
                        self.rel_model_pk_field = field_name
                        break

        self.client = client
        try:
            self.columns = {}
            update_check = {}

            # Gets the count of table
            self.DB_count = self.model_name.objects.filter(del_ind=False).count()

            # Read thru the file record by record , Assign column based on comma delimiter
            for column_data in popup_data_list:
                data = column_data
                for index, field_name in enumerate(self.csv_header):
                    self.data_dict[field_name] = data[index]
                    if not field_name == 'del_ind':
                        update_check[field_name] = data[index]

                self.File_Count = self.File_Count + 1
                self.del_column[self.del_field] = column_data[self.del_index]

                # Checks if the data exists in the tables
                # self.columns[self.filter_field] = column_data[self.pk_index]
                if self.table_name == 'AuthorizationGroup':
                    new_data = self.model_name.objects.filter(**update_check)
                    self.data_dict.pop('auth_obj_id', None)
                elif self.table_name == 'Authorization':
                    new_data = self.model_name.objects.filter(client=self.client, **update_check)
                    self.data_dict.pop('role', None)
                else:
                    new_data = self.model_name.objects.filter(client=self.client, **update_check)

                check_query = new_data.exists()

                # if del_ind = 0 and data doesnt exists in table then insert or get the dupicate count
                if (self.del_column[self.del_field] == '0') and (not check_query):
                    self.Insert_Count = self.Insert_Count + 1

                # If the Input file Deletion indicator is "0" (Insert\Update record) and data  does not exist in the table
                elif (self.del_column[self.del_field] == '0') and check_query:
                    if not (self.model_name.objects.filter(**self.data_dict)):
                        self.Update_Count = self.Update_Count + 1
                    else:
                        self.Duplicate_Count = self.Duplicate_Count + 1

                # Check  If the Input file Deletion indicator is "1" (Delete record) and if record  exists
                # Check if the record is active on DB.

                if (self.del_column[self.del_field] == '1') and check_query:
                    for test in new_data:
                        if not test.del_ind:
                            self.Delete_Count = self.Delete_Count + 1

            check_messages['db_count'] = self.DB_count
            check_messages['file_count'] = self.File_Count
            check_messages['duplicate_count'] = self.Duplicate_Count
            check_messages['insert_count'] = self.Insert_Count
            check_messages['update_count'] = self.Update_Count
            check_messages['delete_count'] = self.Delete_Count

            print(check_messages)

            return check_messages

        except Exception as e:
            print(e)
            messages.error(self.request, 'Error : ' + str(e))

    def guids_table_condition(self):
        unique_check = []
        pk_of_fk_model = []
        self.csv_header = []
        self.fk = []
        fks = []
        # Gets the model name by taking the table name from UI
        self.model_name = apps.get_model(self.app_name, self.table_name)

        # Gets the unique keys
        keys = self.model_name._meta.unique_together
        unique_key = [element for tupl in keys for element in tupl]
        if unique_key:
            unique_values = unique_key.remove('client')

        # gets the headers of the csv file
        counter_flag = True
        for header in csv.reader(self.header_data, delimiter=',', quotechar='"'):
            if counter_flag:
                self.csv_headers = header
                counter_flag = False
                break
            else:
                break
        # gets Foreign keys of the respective model
        for field in self.model_name._meta.fields:
            if field.get_internal_type() == 'ForeignKey':
                res = field.get_attname_column()
                res = res[0][:-3]
                self.fk.append(res)
        if self.fk:
            if 'client' in self.fk:
                fks = self.fk.remove('client')

        # Gets the respective field names of the model for the csv headers
        for field in self.model_name._meta.fields:
            tmp = field.get_attname_column()
            if tmp[1] in self.csv_headers:
                if field.get_internal_type() == 'ForeignKey':
                    tmp = tmp[0][:-3]
                    self.csv_header.append(tmp)
                else:
                    self.csv_header.append(tmp[0])

        self.unique_keys = sorted(unique_key, key=lambda x: self.csv_header.index(x))

        # gets the non matched field names from fk and unique keys
        unique_check = non_match_elements(self.fk, self.unique_keys)
        if unique_check:
            self.related_model = self.model_name._meta.get_field(unique_check).related_model

            for index, field_name in enumerate(self.csv_header):
                if field_name == unique_check:
                    self.rel_model_pk_index = index
                    self.rel_model_pk_field = field_name

        self.indexes = []
        self.fields = []
        for index, field_name in enumerate(self.unique_keys):
            self.indexes.append(index)
            self.fields.append(field_name)
        # gets the field name and index of del_ind
        for index, field_name in enumerate(self.csv_header):
            if field_name == 'company_id':
                self.company_field = field_name
                self.company_index = index

            if field_name == 'auth_obj_id':
                self.fk_index = index
                self.fk_field = field_name
            if field_name == 'role':
                self.fk_index = index
                self.fk_field = field_name
            if field_name == 'del_ind':
                self.del_index = index
                self.del_field = field_name
                break

        # for index,field_name in enumerate(self.fk):

        if self.table_name == 'SpendLimitValue' or self.table_name == 'ApproverLimitValue' or self.table_name == 'AccountingDataDesc' or \
                self.table_name == 'AccountingData' or self.table_name == 'OrgPorg' or self.table_name == 'OrgPGroup':
            for index, field_name in enumerate(self.csv_header):
                if self.table_name == 'AccountingData':
                    if field_name == 'account_assign_cat':
                        self.field_index = index
                        self.rel_model_pk_index = index
                        self.rel_model_pk_field = field_name
                        break
                if self.table_name == 'OrgPorg':
                    if field_name == 'description':
                        self.field_index = index
                    if field_name == 'company_id':
                        self.field_index_check2 = index
                    if field_name == 'object_id':
                        self.field_index_check3 = index
                        self.rel_model_pk_index = index
                        self.rel_model_pk_field = field_name
                        break
                if self.table_name == 'OrgPGroup':
                    if field_name == 'description':
                        self.field_index = index
                    if field_name == 'porg_id':
                        self.field_index_check2 = index
                    if field_name == 'object_id':
                        self.field_index_check3 = index
                        self.rel_model_pk_index = index
                        self.rel_model_pk_field = field_name
                        break

            upload = self.upload_master_data()
        else:
            upload = self.upload_guids_pk_fk_data()
