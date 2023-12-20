
from eProc_Configuration.models import *


def get_masterdata(req):
    timezone_array = []
    currency_array = []
    language_array = []
    country_array = []

    # Get all the languages from the db table
    language_list = Languages.objects.all()
    # Loop at the language table and read only the language id to show in the html
    for language_val in language_list:
        language_array.append(language_val.language_id)

    # Get all the currencies from the db table
    currency_list = Currency.objects.all()
    # Loop at the currency table and read only the currency id to show in html
    for currency_val in currency_list:
        currency_array.append(currency_val.currency_id)

    # Get all the timezones from the table
    timezone_list = TimeZone.objects.all()
    # Loop at the timezone table and read only the timezone id
    for timezone_val in timezone_list:
        timezone_array.append(timezone_val.time_zone)

    # Get all the country codes from the db table
    country_list = Country.objects.all()
    # Loop at the country table and read only the country id to show in html
    for country_val in country_list:
        country_array.append(country_val.country_code)

    return timezone_array, currency_array, language_array, country_array
