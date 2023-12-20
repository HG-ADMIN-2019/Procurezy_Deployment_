from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import UnspscCategoriesCust, UnspscCategoriesCustDesc

django_query_instance = DjangoQueries()


# Function to get product category description based on product category Id and display it in drop down
def get_prod_cat1(request, prod_det):
    """
    The variable prod_det is used to store product Id  of an item while updating an item in 1st step of shopping cart wizard
    This function is mainly used to display product category in drop down in limit_order, form_builder,
    """
    prod_cat_cust = django_query_instance.django_filter_value_list_query(UnspscCategoriesCust, {
        'client': global_variables.GLOBAL_CLIENT
    }, 'prod_cat_id')
    prod_cat_cust_desc = django_query_instance.django_filter_query(UnspscCategoriesCustDesc, {
        'prod_cat_id__in': prod_cat_cust,
        'language_id': global_variables.GLOBAL_USER_LANGUAGE,
        'client': global_variables.GLOBAL_CLIENT
    }, None, ['prod_cat_id', 'category_desc'])
    return prod_cat_cust_desc
