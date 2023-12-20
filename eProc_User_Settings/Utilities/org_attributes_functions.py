from eProc_Attributes.models.org_attribute_models import OrgAttributesLevel
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries

django_query_instance = DjangoQueries()


def get_org_attr_level_details(required_field_list, order_by_list, **org_attr_level_filter):
    """

    :param required_field_list:
    :param order_by_list:
    :param org_attr_level_filter:
    :return:
    """

    return django_query_instance.django_filter_query(
        OrgAttributesLevel,
        org_attr_level_filter,
        order_by_list,
        required_field_list
    )
