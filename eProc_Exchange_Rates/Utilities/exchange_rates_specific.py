from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Configuration.models import SpendLimitValue

django_query_instance = DjangoQueries()


def get_currency_by_max_spending_value(default_cmp_code, client, spend_code_id):
    """
    :param max_spending_value:
    :param client:
    :return:
    """
    spd_curr = ''
    spender_currency = django_query_instance.django_filter_value_list_query(SpendLimitValue,
                                                                            {'spend_code_id': spend_code_id[0],
                                                                                'client': client,
                                                                                'company_id': default_cmp_code},
                                                                            'currency_id')
    if spender_currency:
        spd_curr = spender_currency[0]

    return spd_curr
