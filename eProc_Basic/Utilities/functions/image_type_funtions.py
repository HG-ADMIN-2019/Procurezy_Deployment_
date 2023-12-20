from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Configuration.models.development_data import ImagesType

django_query_instance = DjangoQueries()


def get_image_type(image_type):
    """

    :param image_type:
    :return:
    """
    if django_query_instance.django_existence_check(ImagesType, {'image_type': image_type}):
        image_type = django_query_instance.django_filter_value_list_query(ImagesType,
                                                                          {'image_type': image_type}, 'image_type')[0]

    return image_type
