import re

from django.db.models import Q


def django_q_query(value, value_list, field):
    """

    """
    django_query = Q()
    if value:
        if value == '*':
            django_query = Q(**{field + '__in': value_list})
        elif '*' in value:
            product_match = re.search(r'[a-zA-Z0-9]+', value)
            if value[0] == '*' and value[-1] == '*':
                django_query = Q(**{field + '__in': value_list}) | Q(**{field + '__icontains': product_match.group(0)})
            elif value[0] == '*':
                django_query = Q(**{field + '__in': value_list}) | Q(**{field + '__iendswith': product_match.group(0)})
            else:
                django_query = Q(**{field + '__in': value_list}) | Q(
                    **{field + '__istartswith': product_match.group(0)})
        else:
            field = field + '__in'
            django_query &= Q(**{field: value_list})
    else:
        field = field + '__in'
        django_query &= Q(**{field: value_list})
    return django_query
