from currency_converter import CurrencyConverter


# Function to convert currencies using CurrencyConverter package
def convert_currency(value, from_currency, to_currency):
    """
    :param value:
    :param from_currency:
    :param to_currency:
    :return:
    """
    try:
        return round(CurrencyConverter().convert(value, from_currency, to_currency), 2)
    except ValueError as e:
        return value
        # return None
