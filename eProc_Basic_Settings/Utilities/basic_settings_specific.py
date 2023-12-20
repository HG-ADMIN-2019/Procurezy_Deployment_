import csv
import datetime
import io

from eProc_Basic.Utilities.constants.constants import CONST_ACTION_ADD, CONST_ACTION_COPY, CONST_ACTION_UPDATE, \
    CONST_ACTION_DELETE
from eProc_Basic.Utilities.functions.camel_case import convert_to_camel_case
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries, bulk_create_entry_db
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG112, MSG113
from eProc_Basic.models import *
from eProc_Configuration.Utilities.application_settings_generic import get_configuration_data
from eProc_Configuration.models import UnitOfMeasures, Currency, Languages, Country, TimeZone, UnspscCategories, \
    basic_data, UnspscCategoriesCust
from eProc_Basic.Utilities.functions.log_function import update_log_info

django_query_instance = DjangoQueries()


class BasicSettingsSave:
    def __init__(self):
        self.current_date_time = datetime.datetime.now()
        self.username = global_variables.GLOBAL_LOGIN_USERNAME
        self.client = global_variables.GLOBAL_CLIENT

    def save_country(self, country_data):
        """

        """
        country_db_list = []
        for country_detail in country_data:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(Country,
                                                                {'country_code': country_detail['country_code']}):
                country_db_dictionary = {'country_code': (country_detail['country_code']).upper(),
                                         'country_name': convert_to_camel_case(country_detail['country_name']),
                                         'country_created_at': self.current_date_time,
                                         'country_created_by': self.username,
                                         'country_changed_at': self.current_date_time,
                                         'country_changed_by': self.username
                                         }
                country_db_list.append(country_db_dictionary)
            else:
                django_query_instance.django_update_query(Country,
                                                          {'country_code': country_detail['country_code']},
                                                          {'country_code': country_detail['country_code'],
                                                           'country_name': convert_to_camel_case(
                                                               country_detail['country_name']),
                                                           'country_changed_at': self.current_date_time,
                                                           'country_changed_by': self.username,
                                                           'del_ind': country_detail['del_ind']})
        bulk_create_entry_db(Country, country_db_list)

    def save_country_data_into_db(self, country_data):
        """

        """
        self.save_country(country_data['data'])
        if country_data['action'] == CONST_ACTION_DELETE:
            msgid = 'MSG113'
        else:
            msgid = 'MSG112'
        message = get_message_desc(msgid)[1]

        upload_response = django_query_instance.django_filter_query(Country, {'del_ind': False}, None,
                                                                    ['country_code', 'country_name'])

        return upload_response, message

    def save_languages(self, language_data):
        """

        """
        language_db_list = []
        for language_detail in language_data:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(Languages,
                                                                {'language_id': language_detail['language_id']}):
                language_db_dictionary = {'language_id': (language_detail['language_id']).upper(),
                                          'description': convert_to_camel_case(language_detail['description']),
                                          'languages_created_at': self.current_date_time,
                                          'languages_created_by': self.username,
                                          'languages_changed_at': self.current_date_time,
                                          'languages_changed_by': self.username,
                                          }
                language_db_list.append(language_db_dictionary)
            else:
                django_query_instance.django_update_query(Languages,
                                                          {'language_id': language_detail['language_id']},
                                                          {'language_id': language_detail['language_id'],
                                                           'description': convert_to_camel_case(
                                                               language_detail['description']),
                                                           'languages_changed_at': self.current_date_time,
                                                           'languages_changed_by': self.username,
                                                           'del_ind': language_detail['del_ind']})
        bulk_create_entry_db(Languages, language_db_list)

    def save_language_data_into_db(self, language_data):
        """

        """
        self.save_languages(language_data['data'])
        if language_data['action'] == CONST_ACTION_DELETE:
            msgid = 'MSG113'
        else:
            msgid = 'MSG112'
        message = get_message_desc(msgid)[1]
        upload_response = get_configuration_data(Languages, {'del_ind': False}, ['language_id', 'description'])

        return upload_response, message

    def save_time_zone(self, timezone_data):
        """

        """
        timezone_db_list = []
        for timezone_detail in timezone_data:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(TimeZone,
                                                                {'time_zone': timezone_detail['time_zone']}):
                timezone_db_dictionary = {'time_zone': (timezone_detail['time_zone']).upper(),
                                          'description': (timezone_detail['description']).upper(),
                                          'utc_difference': (timezone_detail['utc_difference']).upper(),
                                          'daylight_save_rule': (timezone_detail['daylight_save_rule']).upper(),
                                          'time_zone_created_at': self.current_date_time,
                                          'time_zone_created_by': self.username,
                                          'time_zone_changed_at': self.current_date_time,
                                          'time_zone_changed_by': self.username,
                                          'del_ind': timezone_detail['del_ind'],
                                          }
                timezone_db_list.append(timezone_db_dictionary)
            else:
                django_query_instance.django_update_query(TimeZone,
                                                          {'time_zone': timezone_detail['time_zone']},
                                                          {'time_zone': timezone_detail['time_zone'],
                                                           'description':(timezone_detail['description']).upper(),
                                                           'utc_difference': (timezone_detail['utc_difference']).upper(),
                                                           'daylight_save_rule': (timezone_detail['daylight_save_rule']).upper(),
                                                           'time_zone_changed_at': self.current_date_time,
                                                           'time_zone_changed_by': self.username,
                                                           'del_ind': timezone_detail['del_ind']})
        bulk_create_entry_db(TimeZone, timezone_db_list)

    def save_timezone_data_into_db(self, timezone_data):
        """

        """
        self.save_time_zone(timezone_data['data'])
        if timezone_data['action'] == CONST_ACTION_DELETE:
            msgid = 'MSG113'
        else:
            msgid = 'MSG112'
        message = get_message_desc(msgid)[1]

        upload_response = get_configuration_data(TimeZone, {'del_ind': False},
                                                 ['time_zone', 'description', 'utc_difference', 'daylight_save_rule'])

        return upload_response, message

    def save_uom(self, unitofmeasures_data):
        """

        """
        unitofmeasures_db_list = []
        for unitofmeasures_detail in unitofmeasures_data:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(UnitOfMeasures,
                                                                {'uom_id': unitofmeasures_detail['uom_id']}):
                unitofmeasures_db_dictionary = {'uom_id': (unitofmeasures_detail['uom_id']).upper(),
                                                'uom_description': (unitofmeasures_detail['uom_description']).upper(),
                                                'iso_code_id': (unitofmeasures_detail['iso_code_id']).upper(),
                                                'unit_of_measures_created_at': self.current_date_time,
                                                'unit_of_measures_created_by': self.username,
                                                'unit_of_measures_changed_at': self.current_date_time,
                                                'unit_of_measures_changed_by': self.username}
                unitofmeasures_db_list.append(unitofmeasures_db_dictionary)
            else:
                django_query_instance.django_update_query(UnitOfMeasures,
                                                          {'uom_id': unitofmeasures_detail['uom_id']},
                                                          {'uom_id': unitofmeasures_detail['uom_id'],
                                                           'uom_description': (
                                                               unitofmeasures_detail['uom_description']).upper(),
                                                           'iso_code_id': (
                                                               unitofmeasures_detail['iso_code_id']).upper(),
                                                           'unit_of_measures_changed_at': self.current_date_time,
                                                           'unit_of_measures_changed_by': self.username,
                                                           'del_ind': unitofmeasures_detail['del_ind']})
        bulk_create_entry_db(UnitOfMeasures, unitofmeasures_db_list)

    def save_unitofmeasures_data_into_db(self, unitofmeasures_data):
        # save uom data
        self.save_uom(unitofmeasures_data['data'])
        if unitofmeasures_data['action'] == CONST_ACTION_DELETE:
            msgid = 'MSG113'
        else:
            msgid = 'MSG112'
        message = get_message_desc(msgid)[1]
        upload_response = get_configuration_data(UnitOfMeasures, {'del_ind': False},
                                                 ['uom_id', 'uom_description', 'iso_code_id'])

        return upload_response, message

    def save_currency(self, currency_data):
        """

        """
        currency_db_list = []
        for currency_detail in currency_data:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(Currency,
                                                                {'currency_id': currency_detail['currency_id']}):
                currency_db_dictionary = {'currency_id': (currency_detail['currency_id']).upper(),
                                          'description': convert_to_camel_case(currency_detail['description']),
                                          'currency_created_at': self.current_date_time,
                                          'currency_created_by': self.username,
                                          'currency_changed_at': self.current_date_time,
                                          'currency_changed_by': self.username,
                                          'del_ind': currency_detail['del_ind']
                                          }
                currency_db_list.append(currency_db_dictionary)
            else:
                django_query_instance.django_update_query(Currency,
                                                          {'currency_id': currency_detail['currency_id']},
                                                          {'currency_id': currency_detail['currency_id'],
                                                           'description': convert_to_camel_case(
                                                               currency_detail['description']),
                                                           'currency_changed_at': self.current_date_time,
                                                           'currency_changed_by': self.username,
                                                           'del_ind': currency_detail['del_ind']})
        bulk_create_entry_db(Currency, currency_db_list)

    def save_currency_data_into_db(self, currency_data):
        """

        """
        self.save_currency(currency_data['data'])
        if currency_data['action'] == CONST_ACTION_DELETE:
            msgid = 'MSG113'
        else:
            msgid = 'MSG112'
        message = get_message_desc(msgid)[1]
        upload_response = get_configuration_data(Currency, {'del_ind': False}, ['currency_id', 'description'])

        return upload_response, message


def csv_data_arrangement(db_header, data_set_val):
    """
        rearranging the jumbled data from csv
        param: db_header, data_set_val
        return: correct_order_list
    """
    upload_csv_header_data = []
    db_header_value = list(db_header.split(","))
    fin_data_upld = io.StringIO(data_set_val)
    fin_data_upload_header = io.StringIO(data_set_val)

    # Gets the header from the csv file
    for header in csv.reader(fin_data_upload_header, delimiter=',', quotechar='"'):
        upload_csv_header_data.append(header)
    upload_csv_header_data = upload_csv_header_data[0]
    next(fin_data_upld)
    pair_list = []
    print(upload_csv_header_data)
    print(db_header_value)

    # Makes list of required header and index of the same header in csv file
    for i in db_header_value:
        for j in range(len(upload_csv_header_data)):
            pair = []
            if i == upload_csv_header_data[j]:
                pair.append(i)
                pair.append(j)
                pair_list.append(pair)

    print(pair_list)
    correct_order_list = []
    # rearranges the data from csv file in required order
    for header in csv.reader(fin_data_upld, delimiter=',', quotechar='"'):

        data = header
        empty_check = [''] * len(data)
        if data == empty_check:
            continue
        data_dict = []
        for i in range(len(pair_list)):
            j = int(pair_list[i][1])
            data_dict.append(data[j])
        correct_order_list.append(data_dict)

    return correct_order_list


def csv_preview_data(db_header, data_set_val):
    """
        rearranging the jumbled data from csv
        param: db_header, data_set_val
        return: correct_order_list
    """
    upload_csv_header_data = []
    db_header_value = db_header
    fin_data_upld = io.StringIO(data_set_val)
    fin_data_upload_header = io.StringIO(data_set_val)

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
            pair = []
            if db_header['field_name'] == upload_csv_header_data[upload_csv_header]:
                pair_list.append({'field_name': db_header['field_name'], 'field_length': db_header['field_length'],
                                  'field_position': upload_csv_header})

    print(pair_list)
    correct_order_list = []
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

    return correct_order_list


def save_basic_data_into_db(basic_data, Table):
    """
    save basic data to db
    :param basic_data:
    :return:
    """
    if Table == 'upload_country':

        for save_country in basic_data:
            if save_country['del_ind']:
                Country.objects.filter(country_code=save_country['country_code']).update(del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(Country, {
                    'country_code': save_country['country_code'], 'del_ind': False}, 'country_created_at')
                created_by_val = list(django_query_instance.django_filter_value_list_query(Country, {
                    'country_code': save_country['country_code'], 'del_ind': False}, 'country_created_by'))

                log_values = update_log_info(created_at_val, created_by_val)

                if not (Country.objects.filter(country_code=save_country['country_code'],
                                               country_name=save_country['country_name'], del_ind=False).exists()):
                    obj, created = Country.objects.update_or_create(
                        country_code=save_country['country_code'],
                        defaults={'country_code': save_country['country_code'],
                                  'country_name': save_country['country_name'],
                                  'country_created_by': log_values['created_by_val'],
                                  'country_changed_by': log_values['changed_by_val'],
                                  'del_ind': False},
                    )

        Upload_response = list(Country.objects.filter(del_ind=False).values('country_code', 'country_name'))
        # msgid = 'MSG112'
        # error_msg = get_msg_desc(msgid)
        message_desc = get_message_desc('MSG112')[1]
        # msgid = 'MSG113'
        # error_msg1 = get_msg_desc(msgid)
        message_desc1 = get_message_desc('MSG113')[1]
        return Upload_response, message_desc, message_desc1

    elif Table == 'upload_currencies':

        for save_currency in basic_data:
            if save_currency['del_ind']:
                Currency.objects.filter(currency_id=save_currency['currency_id']).update(del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(Currency, {
                    'currency_id': save_currency['currency_id'], 'del_ind': False}, 'currency_created_at')
                created_by_val = list(django_query_instance.django_filter_value_list_query(Currency, {
                    'currency_id': save_currency['currency_id'], 'del_ind': False}, 'currency_created_by'))

                log_values = update_log_info(created_at_val, created_by_val)

                if not (Currency.objects.filter(currency_id=save_currency['currency_id'],
                                                description=save_currency['description'], del_ind=False).exists()):
                    obj, created = Currency.objects.update_or_create(
                        currency_id=save_currency['currency_id'],
                        defaults={'currency_id': save_currency['currency_id'],
                                  'description': save_currency['description'],
                                  'currency_created_by': log_values['created_by_val'],
                                  'currency_changed_by': log_values['changed_by_val'],
                                  'del_ind': False},
                    )

        Upload_response = list(Currency.objects.filter(del_ind=False).values('currency_id', 'description'))
        # msgid = 'MSG112'
        # error_msg = get_msg_desc(msgid)
        error_msg = get_message_desc(MSG112)[1]
        error_msg1 = get_message_desc(MSG113)[1]
        # msgid = 'MSG113'
        # error_msg1 = get_msg_desc(msgid)
        return Upload_response, error_msg, error_msg1


    elif Table == 'upload_languages':

        for save_language in basic_data:
            if save_language['del_ind']:
                Languages.objects.filter(language_id=save_language['language_id']).update(del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(Languages, {
                    'language_id': save_language['language_id'], 'del_ind': False}, 'languages_created_at')
                created_by_val = list(django_query_instance.django_filter_value_list_query(Languages, {
                    'language_id': save_language['language_id'], 'del_ind': False}, 'languages_created_by'))

                log_values = update_log_info(created_at_val, created_by_val)

                if not (Languages.objects.filter(language_id=save_language['language_id'],
                                                 description=save_language['description'], del_ind=False).exists()):
                    obj, created = Languages.objects.update_or_create(
                        language_id=save_language['language_id'],
                        defaults={'language_id': save_language['language_id'],
                                  'description': save_language['description'],
                                  'languages_created_by': log_values['created_by_val'],
                                  'languages_changed_by': log_values['changed_by_val'],
                                  'del_ind': False},
                    )

        Upload_response = list(Languages.objects.filter(del_ind=False).values('language_id', 'description'))

        # msgid = 'MSG112'
        # error_msg = get_msg_desc(msgid)
        # msgid = 'MSG113'
        # error_msg1 = get_msg_desc(msgid)
        error_msg = get_message_desc(MSG112)[1]
        error_msg1 = get_message_desc(MSG113)[1]
        return Upload_response, error_msg, error_msg1

    elif Table == 'upload_ProdCat':

        for save_prodcat in basic_data:
            if save_prodcat['del_ind']:
                UnspscCategories.objects.filter(prod_cat_id=save_prodcat['prod_cat_id']).update(del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(UnspscCategories, {
                    'prod_cat_id': save_prodcat['prod_cat_id'], 'del_ind': False}, 'unspsc_categories_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(UnspscCategories, {
                    'prod_cat_id': save_prodcat['prod_cat_id'], 'del_ind': False}, 'unspsc_categories_created_by')

                log_values = update_log_info(created_at_val, created_by_val)

                if not (
                        UnspscCategories.objects.filter(prod_cat_id=save_prodcat['prod_cat_id'],
                                                        prod_cat_desc=save_prodcat['prod_cat_desc'],
                                                        del_ind=False).exists()):
                    obj, created = UnspscCategories.objects.update_or_create(
                        prod_cat_id=save_prodcat['prod_cat_id'],
                        defaults={'prod_cat_id': save_prodcat['prod_cat_id'],
                                  'prod_cat_desc': save_prodcat['prod_cat_desc'],
                                  'unspsc_categories_created_by': log_values['created_by_val'],
                                  'unspsc_categories_changed_by': log_values['changed_by_val'],
                                  'del_ind': False},
                    )

        Upload_response = list(UnspscCategories.objects.filter(del_ind=False).values('prod_cat_id', 'prod_cat_desc'))

        # msgid = 'MSG112'
        # error_msg = get_msg_desc(msgid)
        # msgid = 'MSG113'
        # error_msg1 = get_msg_desc(msgid)
        error_msg = get_message_desc(MSG112)[1]
        error_msg1 = get_message_desc(MSG113)[1]
        return Upload_response, error_msg, error_msg1

    elif Table == 'upload_timezone':

        for save_timezone in basic_data:
            if save_timezone['del_ind']:
                TimeZone.objects.filter(time_zone=save_timezone['time_zone']).update(del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(TimeZone, {
                    'time_zone': save_timezone['time_zone'], 'del_ind': False}, 'time_zone_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(TimeZone, {
                    'time_zone': save_timezone['time_zone'], 'del_ind': False}, 'time_zone_created_by')

                log_values = update_log_info(created_at_val, created_by_val)

                if not (TimeZone.objects.filter(time_zone=save_timezone['time_zone'],
                                                description=save_timezone['description'],
                                                utc_difference=save_timezone['utc_difference'],
                                                daylight_save_rule=save_timezone['daylight_save_rule'],
                                                del_ind=False).exists()):
                    obj, created = TimeZone.objects.update_or_create(time_zone=save_timezone['time_zone'],
                                                                     defaults={'time_zone': save_timezone['time_zone'],
                                                                               'description': save_timezone[
                                                                                   'description'],
                                                                               'utc_difference': save_timezone[
                                                                                   'utc_difference'],
                                                                               'daylight_save_rule': save_timezone[
                                                                                   'daylight_save_rule'],

                                                                               'time_zone_created_by': log_values[
                                                                                   'created_by_val'],

                                                                               'time_zone_changed_by': log_values[
                                                                                   'changed_by_val'],
                                                                               'del_ind': False},
                                                                     )

        Upload_response = list(
            TimeZone.objects.filter(del_ind=False).values('time_zone', 'description', 'utc_difference',
                                                          'daylight_save_rule'))

        # msgid = 'MSG112'
        # error_msg = get_msg_desc(msgid)
        # msgid = 'MSG113'
        # error_msg1 = get_msg_desc(msgid)
        error_msg = get_message_desc(MSG112)[1]
        error_msg1 = get_message_desc(MSG113)[1]
        return Upload_response, error_msg, error_msg1

    elif Table == 'upload_UOM':

        for save_UOM in basic_data:
            if save_UOM['del_ind']:
                UnitOfMeasures.objects.filter(uom_id=save_UOM['uom_id']).update(del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(UnitOfMeasures, {
                    'uom_id': save_UOM['uom_id'], 'del_ind': False}, 'unit_of_measures_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(UnitOfMeasures, {
                    'uom_id': save_UOM['uom_id'], 'del_ind': False}, 'unit_of_measures_created_by')

                log_values = update_log_info(created_at_val, created_by_val)

                if not (UnitOfMeasures.objects.filter(uom_id=save_UOM['uom_id'],
                                                      uom_description=save_UOM['uom_description'],
                                                      iso_code_id=save_UOM['iso_code_id'],
                                                      del_ind=False).exists()):
                    obj, created = UnitOfMeasures.objects.update_or_create(uom_id=save_UOM['uom_id'],
                                                                           defaults={'uom_id': save_UOM['uom_id'],
                                                                                     'uom_description': save_UOM[
                                                                                         'uom_description'],
                                                                                     'iso_code_id': save_UOM[
                                                                                         'iso_code_id'],
                                                                                     'unit_of_measures_created_by':
                                                                                         log_values[
                                                                                             'created_by_val'],
                                                                                     'unit_of_measures_changed_by':
                                                                                         log_values[
                                                                                             'changed_by_val'],
                                                                                     'del_ind': False},
                                                                           )

        Upload_response = list(
            UnitOfMeasures.objects.filter(del_ind=False).values('uom_id', 'uom_description', 'iso_code_id'))

        # msgid = 'MSG112'
        # error_msg = get_msg_desc(msgid)
        # msgid = 'MSG113'
        # error_msg1 = get_msg_desc(msgid)
        error_msg = get_message_desc(MSG112)[1]
        error_msg1 = get_message_desc(MSG113)[1]
        return Upload_response, error_msg, error_msg1
