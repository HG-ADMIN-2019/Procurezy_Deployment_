import csv

from eProc_Basic.Utilities.functions.get_db_query import getClients
from django.contrib import messages

from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.messages.messages import *
from eProc_Basic.Utilities.messages.messages import MSG094
from eProc_Configuration.models import *


def upload_prod_services(request, productsdetail, Test_mode):
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

        client = getClients(request)

        # If the Test Mode check box is checked then run diagnostics.

        # Read thru the file record by record , Assign column based on comma delimiter

        for column in csv.reader(productsdetail, delimiter=',', quotechar='"'):
            File_Count = File_Count + 1
            print("Product Details Extract Line Number:" + str(File_Count))

            del_ind_field = column[31]

            # Checks for the dropdown fileds values existence

            if not (SupplierMaster.objects.filter(supplier_id=column[4], client=client).exists()):
                errmsg = 'Parent Record Not Found on SupplierMaster table for supplier_id'
                messages.error(request, errmsg + ' @Line Number : '
                               + str(File_Count))
                error_flag = 'Y'
            if not (Catalogs.objects.filter(catalog_id=column[15], client=client).exists()):
                errmsg = 'Parent Record Not Found on catalogs table for catalog_id'
                messages.error(request, errmsg + ' @Line Number : '
                               + str(File_Count))
                error_flag = 'Y'
            if not (UnitOfMeasures.objects.filter(uom_id=column[19]).exists()):
                errmsg = 'Parent Record Not Found on unit table for uom_id'
                messages.error(request, errmsg + ' @Line Number : '
                               + str(File_Count))
                error_flag = 'Y'
            if not (Currency.objects.filter(currency_id=column[22]).exists()):
                errmsg = 'Parent Record Not Found on unit table for uom_id'
                messages.error(request, errmsg + ' @Line Number : '
                               + str(File_Count))
                error_flag = 'Y'
            if not (Country.objects.filter(country_code=column[6]).exists()):
                errmsg = 'Parent Record Not Found on unit table for uom_id'
                messages.error(request, errmsg + ' @Line Number : '
                               + str(File_Count))
                error_flag = 'Y'
            if not (Languages.objects.filter(language_id=column[12]).exists()):
                errmsg = 'Parent Record Not Found on unit table for uom_id'
                messages.error(request, errmsg + ' @Line Number : '
                               + str(File_Count))
                error_flag = 'Y'

            # Checks for the mandatory fields values
            if column[0] == '' or column[1] == '' or column[20] == '' or column[17] == '' or column[23] == '' or column[24] == '':
                errmsg = 'Mandatory field values cannot be blank'
                messages.error(request, errmsg + ' @Line Number : '
                               + str(File_Count))
                error_flag = 'Y'
            elif column[0] == '0' or column[1] == '0' or column[20] == '0' or column[17] == '0' or column[23] == '0' or column[24] == '0':
                errmsg = 'Mandatory field values cannot be blank'
                messages.error(request, errmsg + ' @Line Number : '
                               + str(File_Count))
                error_flag = 'Y'

            if error_flag != '':
                continue

            # checks for test mode
            if Test_mode == 'on':
                DB_count = ProductsDetail.objects.filter(del_ind=False).count()
                if (del_ind_field == '0') and \
                        (ProductsDetail.objects.filter(product_id=column[0], client=client).exists()):
                    queryset_test_upd = ProductsDetail.objects.filter(product_id=column[0], client=client)
                    for test in queryset_test_upd:
                        if test.short_desc != column[1] or test.long_desc != column[2]:
                            Update_Count = Update_Count + 1
                        else:
                            Duplicate_Count = Duplicate_Count + 1

                # If the Input file Deletion indicator is "0" (Insert\Update record)

                elif (del_ind_field == '0') and (
                        not (ProductsDetail.objects.filter(product_id=column[0], client=client).exists())):
                    if column[0] in number_list:
                        Duplicate_Count = Duplicate_Count + 1
                        error_msg = get_message_desc(MSG094)[1]
                        # msgid = 'MSG094'
                        # error_msg = get_msg_desc(msgid)
                        # msg = error_msg['message_desc'][0]
                        # error_msg = msg
                        errmsg_duplicate = error_msg
                    else:
                        Insert_Count = Insert_Count + 1

                # Check  If the Input file Deletion indicator is "1" (Delete record) and if record  exists
                # Check if the record is active on DB.

                if (del_ind_field == '1') and (
                        ProductsDetail.objects.filter(product_id=column[0], client=client).exists()):
                    queryset_test_del = ProductsDetail.objects.filter(product_id=column[0], client=client)
                    for test in queryset_test_del:
                        if not test.del_ind:
                            Delete_Count = Delete_Count + 1

                # Check  If the Input file Deletion indicator is "1" (Delete record) and if record does not exists
                # report as invalid record.

                elif (del_ind_field == '1') and (
                        not (ProductsDetail.objects.filter(product_id=column[0], client=client).exists())):
                    delete_error = 'Y'
                    Delete_Err_Count = Delete_Err_Count + 1

                # Append the input key to the Array list for checking the next reocrds for dups.

                number_list.append(column[0])

            elif Test_mode != 'on':

                del_ind_field = column[31]

                # If the Deletion indicator in the file = "0" and record does not exist on the DB : INSERT DB

                if (del_ind_field == '0') and (
                        not (ProductsDetail.objects.filter(product_id=column[0], client=client).exists())):
                    _, created = ProductsDetail.objects.get_or_create(catalog_item=guid_generator(),
                                                                      product_id=column[0],
                                                                      short_desc=column[1],
                                                                      long_desc=column[2],
                                                                      supp_prod_num=column[3],
                                                                      supplier_id=column[4],
                                                                      unspsc=UnspscCategories.objects.get(
                                                                          prod_cat_id=column[5]),
                                                                      country_of_origin=Country.objects.get(
                                                                          country_code=column[6]),
                                                                      search_term1=column[7],
                                                                      search_term2=column[8], manufacturer=column[9],
                                                                      brand=column[10],
                                                                      offer_key=column[11],
                                                                      language=Languages.objects.get(
                                                                          language_id=column[12]),
                                                                      price_on_request=column[13], manu_part_num=column[14],
                                                                      catalog_id=column[15],
                                                                      product_type=column[16], lead_time=column[17],
                                                                      quantity_avail=column[18],
                                                                      unit=UnitOfMeasures.objects.get(
                                                                          uom_id=column[19]), price=column[20],
                                                                      price_unit=column[21],
                                                                      currency=Currency.objects.get(
                                                                          currency_id=column[22]),
                                                                      prod_cat_id=column[23], quantity_min=column[24],
                                                                      created_at=column[25],
                                                                      created_by=column[26], changed_at=column[27],
                                                                      changed_by=column[28],
                                                                      ctr_num=column[29], ctr_item_num=column[30],
                                                                      del_ind=column[31],
                                                                      client=OrgClients.objects.get(client=client)
                                                                      )
                    Insert_Count = Insert_Count + 1
                    Data_saved = 'Y'

                # If the Deletion indicator in the file = "0" and record  exist on the DB : Update DB

                elif (del_ind_field == '0') and (
                        ProductsDetail.objects.filter(product_id=column[0], client=client).exists()):
                    queryset_upd = ProductsDetail.objects.filter(product_id=column[0], client=client)
                    for test in queryset_upd:
                        if test.short_desc != column[1] or test.long_desc != column[2]:
                            ProductsDetail.objects.filter(product_id=column[0], client=client).update(
                                product_id=column[0],
                                short_desc=column[1],
                                long_desc=column[2],
                                supp_prod_num=column[3],
                                supplier_id=column[4],
                                unspsc=UnspscCategories.objects.get(prod_cat_id=column[5]),
                                country_of_origin=Country.objects.get(country_code=column[6]),
                                search_term1=column[7],
                                search_term2=column[8], manufacturer=column[9], brand=column[10],
                                offer_key=column[11], language=Languages.objects.get(language_id=column[12]),
                                price_on_request=column[13], manu_part_num=column[14],
                                catalog_id=column[15],
                                product_type=column[16], lead_time=column[17], quantity_avail=column[18],
                                unit=UnitOfMeasures.objects.get(uom_id=column[19]), price=column[20],
                                price_unit=column[21],
                                currency=Currency.objects.get(currency_id=column[22]),
                                prod_cat_id=column[23], quantity_min=column[24], created_at=column[25],
                                created_by=column[26], changed_at=column[27], changed_by=column[28],
                                ctr_num=column[29], ctr_item_num=column[30],
                                del_ind=column[31],
                                client=OrgClients.objects.get(client=client)
                            )
                            Update_Count = Update_Count + 1
                            Data_saved = 'Y'

                # If the Deletion indicator in the file = "1" and record  exist on the DB : Soft Delete(del_ind =0) DB

                if (del_ind_field == '1') and (
                        ProductsDetail.objects.filter(product_id=column[0], client=client).exists()):
                    queryset_del = ProductsDetail.objects.filter(product_id=column[0], client=client)
                    for test in queryset_del:
                        if not test.del_ind:
                            ProductsDetail.objects.filter(product_id=column[0],
                                                          short_desc=column[1],
                                                          long_desc=column[2],
                                                          supp_prod_num=column[3],
                                                          supplier_id=column[4],
                                                          unspsc=UnspscCategories.objects.get(prod_cat_id=column[5]),
                                                          country_of_origin=Country.objects.get(country_code=column[6]),
                                                          search_term1=column[7],
                                                          search_term2=column[8], manufacturer=column[9],
                                                          brand=column[10],
                                                          offer_key=column[11],
                                                          language=Languages.objects.get(language_id=column[12]),
                                                          price_on_request=column[13], manu_part_num=column[14],
                                                          catalog_id=column[15],
                                                          product_type=column[16], lead_time=column[17],
                                                          quantity_avail=column[18],
                                                          unit=UnitOfMeasures.objects.get(uom_id=column[19]),
                                                          price=column[20], price_unit=column[21],
                                                          currency=Currency.objects.get(currency_id=column[22]),
                                                          prod_cat_id=column[23], quantity_min=column[24],
                                                          created_at=column[25],
                                                          created_by=column[26], changed_at=column[27],
                                                          changed_by=column[28],
                                                          ctr_num=column[29], ctr_item_num=column[30],
                                                          client=OrgClients.objects.get(client=client)
                                                          ).update(del_ind=True)
                            Delete_Count = Delete_Count + 1
                            Data_saved = 'Y'

                # If the Deletion indicator in the file = "1" and record  does not exist on the DB : Error message

                elif (del_ind_field == '1') and (
                        not (ProductsDetail.objects.filter(product_id=column[0], client=client).exists())):
                    delete_error = 'Y'
                    Delete_Err_Count = Delete_Err_Count + 1

                # Display insert /updated count in the display
                DB_count = ProductsDetail.objects.filter(del_ind=0).count()

        messages.info(request, 'Database Upload Results  :')
        messages.info(request, '-------------------------------')

        # Display the number of Active records in DB
        messages.success(request, ' Number of Records in Database    : ' + str(DB_count))
        # Display the number of  records in file
        messages.success(request, ' Number of Records in Input file  : ' + str(File_Count))
        # Display the number of records Inserted
        messages.success(request, ' Records Inserted      : ' + str(Insert_Count))
        # Display the number of records Updated
        messages.success(request, ' Records Updated       : ' + str(Update_Count))
        # Display the number of records Deleted
        messages.success(request, ' Records Deleted       : ' + str(Delete_Count))

        if File_Count == 0:
            messages.error(request, ' Empty File : Please correct and try again ')

        # Display error message if delete record doesnt exist on DB
        if delete_error != '':
            messages.error(request, ' Input Delete records that dont exist in DB : ' + str(Delete_Err_Count))

        if Data_saved == 'Y':
            error_msg = get_message_desc(MSG037)[1]
            # msgid = 'MSG037'
            # error_msg = get_msg_desc(msgid)
            messages.success(request, error_msg)
            # messages.success(request, MSG037)
        else:
            error_msg = get_message_desc(MSG043)[1]
            # msgid = 'MSG043'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            messages.error(request, error_msg)
            # messages.error(request, MSG043)

    except Exception as e:
        print(e)
        messages.error(request, 'Error : ' + str(e))
